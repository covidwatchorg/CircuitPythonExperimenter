# logging

import time




class Logger:
    def __init__(self):
        self._buffer = ""
        self.line_end = "\n"
        self.max_buffer_size = 1000
        _set_max_age_s(10)
        _clear_age_timer()

    # stale buffers
    def _set_max_age_s(self,s):
        self.max_buffer_age_s = s
        self._max_buffer_age_ns = int(s*1000.0) * 1_000_000

    def _clear_age_timer(self):
        self._buffer_old_time_ns = time.monotonic_ns() + self._max_buffer_age_ns

    def _is_old(self):
        return time.monotonic_ns() > self._max_buffer_age_ns and self._buffer

    # big buffers
    def _is_big(self):
        return len(self._buffer) > self_max_buffer_size

    # logging
    def flush(self):
        self._log()
        self._buffer = ""

    def log(self, s):
        if s and not self._buffer:
            _clear_age_timer()
        self._buffer += str(s) + self.line_end
        if self.is_big() or self._is_old():
            self.flush()

    def spin(self):
        if self._is_old():
            self.flush()

    def __enter__(self):
        return self

    def __exit__(self):
        self.flush()
        return False

    def _log(self):
        pass


class ConsoleLogger(Logger):
    """logs to wherever print() goes"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _log(self):
        print(self._buffer, end='')


class FileLogger(Logger):
    def __init__(self, path, **kwargs):
        super().__init__(**kwargs)
        self.path = path

    def _log(self):
        with open(self.path, "a") as f:
            f.write(self.buffer)


class SecondsLogger():
    """logger built out of another that prepends seconds to entries"""
    def __init__(self, logger, formatter="{:9.3} s: "):
        self._logger = logger
        self._fmt = formatter
        self._base_ns = time.monotonic_ns()

    def _prefix(self):
        delta_ns = time.monotonic_ns() - self._base_ns
        return self._fmt.format(0.000_000_001 * delta_ns)

    def log(self,s):
        self._logger.log(self._prefix() + s)

    def flush(self):
        self._logger.flush()

    def spin(self):
        self._logger.spin()


class CompositeLogger():
    """logger that logs to all of the specified loggers  """
    def __init__(self, *args):
        self._loggers = args

    def log(self, s):
        for logger in self._loggers:
            logger.log(s)

    def flush(self):
        for logger in self._loggers:
            logger.flush()

    def spin(self):
        for logger in self._loggers:
            logger.spin()