import errno
import logging
import sys
import socket
import os

host = socket.gethostname()

def setup_logging(loglevel, logfile):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if numeric_level is None:
        raise ValueError("Invalid log level: %s" % loglevel)
    
    log_format = "[%(asctime)s] {0}/%(levelname)s/%(name)s: %(message)s".format(host)
    logging.basicConfig(level=numeric_level, filename=logfile, format=log_format)
    
    sys.stderr = StdErrWrapper()
    sys.stdout = StdOutWrapper()


def format_logfile(pattern, context):
    """
    Format the logfile according to the pattern and context e.g.

        >>> format_logfile("results/{locustfile}/result_{date}.json", {"locustfile": "homepage", "date": datetime.now().isoformat()})
        >>> "results/homepage/result_2015-09-08T20:29:48.json"

    The pattern can contain no keywords at all for a static path.

    :type pattern: str
    :param pattern: Template file format pattern; keywords denoted by curly braces, e.g. "{keyword}"
    :type context: dict
    :param context: Keyword variables
    :rtype: str
    :return: The formatted logfile name
    """
    for k, v in context.iteritems():
        pattern = pattern.replace("{%s}" % k, str(v))
    return pattern


def save_logfile(path, data):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError, e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise
    with open(path, 'w') as f:
        f.write(data)


stdout_logger = logging.getLogger("stdout")
stderr_logger = logging.getLogger("stderr")

class StdOutWrapper(object):
    """
    Wrapper for stdout
    """
    def write(self, s):
        stdout_logger.info(s.strip())

class StdErrWrapper(object):
    """
    Wrapper for stderr
    """
    def write(self, s):
        stderr_logger.error(s.strip())

# set up logger for the statistics tables
console_logger = logging.getLogger("console_logger")
# create console handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
# formatter that doesn't include anything but the message
sh.setFormatter(logging.Formatter('%(message)s'))
console_logger.addHandler(sh)
console_logger.propagate = False

# configure python-requests log level
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)
