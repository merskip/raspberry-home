from threading import currentThread

from datetime import datetime


class Logger:

    def __init__(self, name: str):
        self.name = name
        self._start_time = None

    def start_timer(self):
        self._start_time = datetime.now()

    def error(self, message: str):
        self._log("ERROR", message)

    def warning(self, message: str):
        self._log("WARNING", message)

    def info(self, message: str):
        self._log("INFO", message)

    def debug(self, message: str):
        self._log("DEBUG", message)

    def verbose(self, message: str):
        self._log("VERBOSE", message)

    def _log(self, level: str, message: str, error: Exception = None):
        time = datetime.now()
        thread = currentThread()
        text = "%s [%s] [%s] [%s] %s" % (time.isoformat(), thread.name, self.name, level, message)
        if error is not None:
            text += "Error: %s" % error
        if self._start_time is not None:
            text += " (in %s)" % (time - self._start_time)
            self._start_time = None
        print(self._get_color_begin(level) + text + self._get_color_end())

    def _get_color_begin(self, level: str) -> str:
        if level == "VERBOSE":
            return "\x1B[37m"
        elif level == "DEBUG":
            return "\x1B[37m"
        elif level == "INFO":
            return "\x1B[36m"
        elif level == "WARNING":
            return "\x1B[33m"
        elif level == "ERROR":
            return "\x1B[31m"
        else:
            return ""

    def _get_color_end(self) -> str:
        return "\x1B[0m"
