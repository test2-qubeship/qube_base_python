# flake8: noqa
# pylint: skip-file
import logging
from logging.handlers import RotatingFileHandler
import colorlog

# Create the logger
# pylint: disable=invalid-name
Log = logging.getLogger()

# time formatter - date - time - UTC offset
# e.g. "08/16/1988 21:30:00 +1030"
# see time formatter documentation for more
date_format = "%m/%d/%Y %H:%M:%S %z"
'''
https://docs.python.org/2/library/logging.html
15.7.2. Logging Levels
Level Numeric value
CRITICAL  50
ERROR 40
WARNING 30
INFO  20
DEBUG 10
NOTSET  0
'''


def configure(level, logfile=None, with_time=False):
    """ Configure logger which dumps log on terminal

  :param with_time:
  :param level: logging level: info, warning, verbose...
  :type level: logging level
  :param logfile: log file name, default to None
  :type logfile: string
  :return: None
  :rtype: None
  """
    Log.setLevel(level)
    # if logfile is specified, FileHandler is used
    if logfile is not None:
        if with_time:
            log_format = "%(asctime)s:%(levelname)s: %(message)s"
        else:
            log_format = "%(levelname)s: %(message)s"
        formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(formatter)
        Log.addHandler(file_handler)
    # otherwise, use StreamHandler to output to stream (stdout, stderr...)
    else:
        if with_time:
            log_format = ("%(log_color)s%(levelname)s:%(module)s-%(name)s-"
                          "%(funcName)s:%(reset)s %(asctime)s %(message)s")
        else:
            log_format = ("%(log_color)s%(levelname)s:%(module)s-"
                          "%(name)s-%(funcName)s:%(reset)s %(message)s")
        # pylint: disable=redefined-variable-type
        formatter = colorlog.ColoredFormatter(fmt=log_format,
                                              datefmt=date_format)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        Log.addHandler(stream_handler)


def init_rotating_logger(level, logfile, max_files, max_bytes):
    """Initializes a rotating logger

    It also makes sure that any StreamHandler is removed,
    so as to avoid stdout/stderr constipation issues
  """
    logging.basicConfig()

    root_logger = logging.getLogger()
    log_format = "%(asctime)s:%(levelname)s:%(filename)s: %(message)s"

    root_logger.setLevel(level)
    handler = RotatingFileHandler(logfile, maxBytes=max_bytes,
                                  backupCount=max_files)
    handler.setFormatter(logging.Formatter(fmt=log_format,
                                           datefmt=date_format))
    root_logger.addHandler(handler)

    for handler in root_logger.handlers:
        root_logger.debug("Associated handlers - " + str(handler))
        if isinstance(handler, logging.StreamHandler):
            root_logger.debug("Removing StreamHandler: " + str(handler))
            root_logger.handlers.remove(handler)


def configure_logging(loglevel=logging.INFO, with_time=False):
    configure(loglevel, with_time=with_time)


def set_logging_level(cl_args, with_time=False):
    """simply set verbose level based on command-line args

  :param with_time:
  :param cl_args: CLI arguments
  :type cl_args: dict
  :return: None
  :rtype: None
  """

    logfile = cl_args['logfile']

    if cl_args['verbose']:
        configure(logging.DEBUG, logfile=logfile, with_time=with_time)
    else:
        configure(logging.INFO, logfile=logfile, with_time=with_time)
