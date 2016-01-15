from collections import namedtuple

configresult = namedtuple('ConfigResult', ['success', 'warnmsgs', 'errmsgs', 'data'])

ParseResult =  namedtuple('ParseResult', ['warnmsgs', 'errmsgs', 'data'])

