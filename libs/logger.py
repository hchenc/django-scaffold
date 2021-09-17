import logging
import json
import six
import threading
import weakref

from django.utils.log import CallbackFilter


class SafeDict(dict):
    def __getitem__(self, key):
        try:
            return super(SafeDict, self).__getitem__(key)
        except KeyError:
            return ''


class BaseLogger(object):
    def __init__(self, name):
        self._logger = logging.getLogger(name)
        self._context = dict()

    def bind(self, **kwargs):
        self._context.update(kwargs)

    def unbind(self, *args):
        for arg in args:
            self._context.pop(arg, None)

    def unbind_all(self):
        self._context.clear()

    def log(self, level, msg, exc_info=None, extra=None, **kwargs):
        load = SafeDict(self._context)
        load.update(kwargs)
        # data in load will be used to generate log message with msg
        if load:
            self._logger.log(level, msg, load, exc_info=exc_info, extra=extra)
        else:
            self._logger.log(level, msg, exc_info=exc_info, extra=extra)


class Logger(BaseLogger):
    def debug(self, *args, **kwargs):
        return self.log(logging.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        return self.log(logging.INFO, *args, **kwargs)

    def warn(self, *args, **kwargs):
        return self.log(logging.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        return self.log(logging.ERROR, *args, **kwargs)

    def exception(self, *args, **kwargs):
        kwargs['exc_info'] = True
        return self.error(*args, **kwargs)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        message = super(JsonFormatter, self).format(record)
        if isinstance(record.args, dict):
            data = dict(record.args)
        else:
            data = {}
        data['message'] = message
        data['created'] = str(int(round(record.created * 1000)))
        data['levelname'] = record.levelname
        formatted = json.dumps(data)
        return formatted


class StreamFormatter(logging.Formatter):
    def make_kv_str(self, data):
        return ''.join(map(
            lambda items: '\n> {x:10}: {y}'.format(x=items[0], y=items[1]),
            six.iteritems(data)
        ))

    def format(self, record):
        if isinstance(record.args, dict):
            data = dict(record.args)
        else:
            data = {}
        record.kvdata = self.make_kv_str(data)
        message = super(StreamFormatter, self).format(record)
        return message


def getLogger(name):
    return Logger(name)


def get_thread_logger(name='request'):
    """This function will return one certain logger by current thread id.
    You should keep a reference of the logger, for example, an attribute
    of a session object such as Django Request, or a variable in your
    main function.
    """
    ident = threading.current_thread().ident
    if ident not in thread_loggers:
        # this assignment is necessary to keep a strong reference
        log = Logger(name)
        thread_loggers[ident] = log
    return thread_loggers[ident]


thread_loggers = weakref.WeakValueDictionary()
