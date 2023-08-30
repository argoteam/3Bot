import datetime
import json
from colorama import Fore, Style, init
import os

init(autoreset=True)

BOLD_ON = "\033[1m"
BOLD_OFF = "\033[0m"

class LogLevels:
    DEBUG = 1
    INFO = 5
    WARN = 20
    ERROR = 50
    CRITICAL = 1000 # highest

loggers = {}

# ! here because its used right after

def get_bot_path():
    return \
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), ".."))

config = {
    "longest_cls_len": 0,
    "longest-logger-name": 35,
    "logging-path": os.path.join(get_bot_path(), "logs"),
    "logging_level": LogLevels.INFO,
    "optimal_leng": 35
}

log_colors = {
    "DEBUG": Fore.BLUE,
    "INFO": Fore.GREEN,
    "WARN": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.RED
}

BYTE_CONV_RATES = {
    ("B", "B"): 1,
    ("B", "KB"): 1000,
    ("KB", "MB"): 1000,
    ("MB", "GB"): 1000,
    ("B", "MB"): 1000**2,
    ("B", "GB"): 1000**3
}

def fit_logger_cls(name, length):
    if len(name) <= length: return name
     
    to_shorten = len(name) - length + 1
    name = name[to_shorten:]
    # check if a dot is leading:
    if name.startswith("."): name = name[1:]
    name = "…" + name
    return name


def set_level(level):
    try:
        config["logging_level"] = level
    except:
        raise ValueError("Invalid logging level")

def get_level():
    return getattr(LogLevels, config["logging_level"], None)

def get_level_from_string(level):
    return getattr(LogLevels, level, None)

def is_level_logged(level):
    if level < config["logging_level"]:
        return False
    return True

def remove_underscores(label):
    if label.startswith("__") and label.endswith("__"):
        return label[2:-2]
    return label

def weight(x):
    try:
        # get weight from file name
        components = x.strip(".log").split("-")
        weight = 10000 * int(components[2]) + 100 * int(components[1]) + int(components[0])
        return weight
    except:
        return -1

def dir_size(dir_):
    size = 0
    with os.scandir(dir_) as files:
        for entry in files:
            if entry.is_file():
                size += entry.stat().st_size
            elif entry.is_dir():
                size += dir_size(entry.path)
    return size

def convert_bytes(size, fmt, goal):
    conv = BYTE_CONV_RATES[(fmt, goal)]
    return (size / conv, goal)

def save_logs(msg):
    log_dir = config["logging-path"]
    limit = (10, "MB")
    
    # open a file corresponding to the current date
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    file_format = date + ".log"
    content = ""
    try:
        with open(os.path.join(log_dir, file_format), mode="r") as f:
            content = f.read()
    except: pass
    with open(os.path.join(log_dir, file_format), mode="w") as f:
        f.write(content + msg + "\n")
    
    if limit:
        lmt, byte = limit
        # sort files using a custom weight for sorting
        # ! weight = 1000Y + 10M + D
        filenames = []
        for _,_,files in os.walk(log_dir):
            filenames.extend(files)
        filenames = sorted(filenames, key=lambda x: weight(x))
        # get size of files
        sizes = dir_size(log_dir)
        # check if over limit
        sizes = convert_bytes(sizes, "B", byte)
        if sizes[0] > float(int(lmt)):
            # delete files until limit is not over
            while sizes[0] > float(int(lmt)):
                os.remove(filenames[0])
                del filenames[0]
                sizes = convert_bytes(dir_size(log_dir), "B", byte)

# @decorator
def LogClass(cls):
    """A decorator that adds logging functionality to the "decorated" class"""
    def wrapper(*args, **kwargs):
        fullpath = remove_underscores(cls.__module__) + "." + cls.__name__

        return cls(*args, **kwargs, logger=Logger(name=fullpath))
    return wrapper


class Logger:
    """
    Logger
    ----------------------------

    Logger is a class that provides logging at the next level.
    """

    def __init__(self, name: str = None):
        self.name = "null"
        if name:
            self.name = name
            loggers[self.name] = self

    @classmethod
    def get(cls, logger_name: str = None):
        if not logger_name:
            raise ValueError("You must provide a logger name to get it")
        
        try:
            logger = loggers[logger_name]
        except:
            try:
                cls.name = logger_name
                loggers[cls.name] = cls
                return cls
            except:
                raise ValueError("No logger found with name '{}'".format(logger_name))

        return logger

    # logging part, yay
    def _log(self, log_type, message):
        color = log_colors[log_type]
        longest_logger_name = config["optimal_leng"]
        msg = ""
        fit = fit_logger_cls(self.name, config['optimal_leng'])
        if log_type == "CRITICAL":
            msg = f"{Fore.RED}{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')[:-3]} {fit}{' '*(longest_logger_name+1-len(fit))}CRITICAL : {message}"
        else:
            msg = f"{Style.DIM}{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')[:-3]}{Style.RESET_ALL} {Fore.CYAN}{fit}{' '*(longest_logger_name+1-len(fit))}{color}{BOLD_ON}{log_type}{BOLD_OFF}{' '*(5-len(log_type))}{Fore.WHITE}{Style.RESET_ALL} : {message}"
        if is_level_logged(get_level_from_string(log_type)):
            print(msg)
            save_logs(msg)

    def debug(self, message):
        self._log("DEBUG", message)
        
    def info(self, message):
        self._log("INFO", message)

    def warn(self, message):
        self._log("WARN", message)
    
    def error(self, message):
        self._log("ERROR", message)
    
    def critical(self, message):
        self._log("CRITICAL", message)


# print_logs: @deprecated
try:
    os.mkdir(config["logging-path"])
except: pass