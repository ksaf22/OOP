from typing import Protocol, List
import re
import sys
import socket


class LogFilterProtocol(Protocol):
    def match(self, text: str) -> bool:
        pass

class LogHandlerProtocol(Protocol):
    def handle(self, text: str):
        pass


class SimpleLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str):
        self.pattern = pattern

    def match(self, text: str) -> bool:
        return self.pattern in text

class ReLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str):
        self.regex = re.compile(pattern)

    def match(self, text: str) -> bool:
        return bool(self.regex.search(text))

class FileHandler(LogHandlerProtocol):
    def __init__(self, filename: str):
        self.filename = filename

    def _handle(self, text: str):
        with open(self.filename, "a") as f:
            f.write(text + "\n")

    def handle(self, text: str):
        try:
            return self._handle(text)
        except Exception:
            ...

class SocketHandler(LogHandlerProtocol):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def handle(self, text: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(text.encode())


class ConsoleHandler(LogHandlerProtocol):
    def handle(self, text: str):
        print(text)


class SyslogHandler(LogHandlerProtocol):
    def handle(self, text: str):
        sys.stderr.write(text + "\n")


class Logger:
    def __init__(self, _filters: List[LogFilterProtocol], _handlers: List[LogHandlerProtocol]):
        self.__filters = _filters
        self.__handlers = _handlers

    def log(self, text: str):
        if all(f.match(text) for f in self.__filters):
            for handler in self.__handlers:
                handler.handle(text)


if __name__ == "__main__":
    filters = [SimpleLogFilter("ERROR"), ReLogFilter(r"\d+")]
    handlers = [ConsoleHandler(), FileHandler("logs.txt")]
    logger = Logger(filters, handlers)

    logger.log("ERROR: 404")
    logger.log("ERROR: be careful")
    logger.log("WARNING: 500")
