import os
import time
import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

TEK_ROLLING_PERIOD = 144
TIME_WINDOW = 10 # (minutes)

backend = default_backend()

def computeRpiKey(tek):
  salt = None 
  info = 'EN-RPIK'.encode('UTF-8') 
  hkdf = HKDF(algorithm=hashes.SHA256(),length=16,salt=salt,info=info, backend=backend)
  rpiKey = hkdf.derive(tek) 
  return(rpiKey)
  
def computeAemKey(tek):
  salt = None 
  info = 'EN-AEMK'.encode('UTF-8') 
  hkdf = HKDF(algorithm=hashes.SHA256(),length=16,salt=salt,info=info, backend=backend)
  aemKey = hkdf.derive(tek) 
  return(aemKey)

def computeRpi(rpiKey, intervalNumber):
  cipher = Cipher(algorithms.AES(rpiKey), modes.ECB(), backend=backend)
  encryptor = cipher.encryptor()
  paddedData = 'EN-RPI'.encode('UTF-8') + 0x000000000000.to_bytes(6, byteorder = 'little') + intervalNumber.to_bytes(4, byteorder = 'little')
  rpi = encryptor.update(paddedData) + encryptor.finalize()
  return(rpi)
  
def computeAem(aemKey, rpi):
  cipher = Cipher(algorithms.AES(aemKey), modes.CTR(rpi), backend=backend)
  encryptor = cipher.encryptor()
  metadata = b'40030000'  # todo: make versioning and transmit power configurable 
  aem = encryptor.update(metadata) + encryptor.finalize()
  return(aem)

def deriveRpiAndAem(tek, intervalNumber):
  rpiKey = computeRpiKey(tek)
  aemKey = computeAemKey(tek)

  rpi = computeRpi(rpiKey, intervalNumber)
  aem = computeAem(aemKey, rpi)

  return(rpi, aem)


def computeInterval(epochTime):
  return(int(epochTime/(60*TIME_WINDOW))) 

def decryptRpi(rpi, rpiKey):
  cipher = Cipher(algorithms.AES(rpiKey), modes.ECB(), backend=backend)
  decryptor = cipher.decryptor()
  decryptedRpi = decryptor.update(rpi) + decryptor.finalize()
  return(decryptedRpi)

def decryptAem(aem, aemKey, rpi):
  cipher = Cipher(algorithms.AES(aemKey), modes.CTR(rpi), backend=backend)
  decryptor = cipher.decryptor()
  decryptedAem = decryptor.update(aem) + decryptor.finalize()
  return(decryptedAem)

def getBits(byte, indices):
  bits = ""
  for i in indices: 
    bits = bits + str((byte >> i) & 1)
  return(bits)

def printMetadata(metadata):
  version = metadata[0]
  print("   Major version: " + getBits(version, [7,6]))
  print("   Minor version: " + getBits(version, [5,4]))
  print("   Reserved (Versioning): " + getBits(version, range(4)))
  transmitPower = metadata[1] 
  print("   Transmit Power: " + str(transmitPower))
  reserved = metadata[2:4].hex()
  print("   Reserved (Unspecified): " + reserved)


teks = [b'\xf5\x1a\x26\xc6\x90\x63\x98\x28\x8f\x08\x21\x04\x9d\x6a\x5c\x6a', b'\x55\x96\x4a\x05\x12\xaf\xb1\x68\x20\xf3\xeb\xfc\x96\x4b\xc8\x53', b'\x3b\x06\x1d\xb1\x28\xb5\x48\x4e\x53\xb5\x6f\xaf\x71\x43\x0e\x05', b'\x75\xe5\x8e\x12\x0d\xe1\x14\xb4\xb7\xc7\x49\x73\x56\x70\xbd\xa2', b'\x26\xdf\x20\x4c\x72\x7b\xdb\x07\x8b\x2e\xff\xa5\x46\x0b\x7c\xdd', b'\x2e\xdc\x48\xba\x63\x88\x7e\x04\x0d\xe6\x8d\xa6\x5e\xd5\x58\x50', b'\xf1\x52\x6f\x6e\x64\x4b\xef\x6f\x90\x5f\x9d\xc3\x17\x72\xa6\xc7']

possibleRpis = [b'\x22\x3a\x7d\xf8\x99\x2b\xef\x14\xbf\x74\x2c\xce\x08\x9f\xd1\x13', b'\x95\x08\x25\xde\xf5\xc6\xce\xfb\xe4\x2a\xa6\x97\x27\xda\x9f\x99'] 
possibleAems = [b'\x45\xb6\x1e\x3a', b'\xf9\xc5\x2a\x5f']

epochTime = 1593786600 # 14:30 UTC July 3, 2020
baseIntervalNumber = computeInterval(epochTime) 

for tek in teks:
  for intervalNumber in range(baseIntervalNumber - 20, baseIntervalNumber + 20):
    computedRpi, computedAem = deriveRpiAndAem(tek, intervalNumber)
    if computedRpi in possibleRpis:
      print("\n\nComputed RPI matched detected RPI")
      print("Interval number: " + str(intervalNumber))
      print("RPI: " + computedRpi.hex())
      print("TEK: " + tek.hex())
      aem = possibleAems[possibleRpis.index(computedRpi)]
      aemKey = computeAemKey(tek)
      metadata = decryptAem(aem, aemKey, computedRpi)
      print("AEM: " + aem.hex())
      print("Decrypted Metadata: " + metadata.hex())
      printMetadata(metadata)


