#!/usr/bin/env python

import sys
import datetime

_COL_TBL = {
    '@W': '\033[97m',  # white
    '@R': '\033[91m',  # lt red
    '@Y': '\033[93m',  # lt yellow
    '@G': '\033[92m',  # lt green
    '@C': '\033[96m',  # lt cyan
    '@B': '\033[94m',  # lt blue
    '@P': '\033[95m',  # lt purple
    '@D': '\033[37m',  # lt gray
    '@d': '\033[90m',  # gray'
    '@r': '\033[31m',  # red
    '@y': '\033[33m',  # yellow
    '@g': '\033[32m',  # green
    '@c': '\033[36m',  # cyan
    '@b': '\033[34m',  # blue
    '@p': '\033[35m',  # purple

}


class Logger(object):
    def __init__(self, tag):
        self.tag = str(tag)

    @staticmethod
    def fmt(msg):
        for c in _COL_TBL:
            if c in msg:
                msg = msg.replace(c, _COL_TBL[c])
        return msg + '\033[0m'

    def raw(self, msg, endl='\n'):
        sys.stdout.write(self.fmt(msg) + endl)
        sys.stdout.flush()

    def prn(self, msg, prefix='> ', endl='\n'):
        msg = '%s [%s][%s] %s%s' % (
            prefix, datetime.datetime.now().strftime('%H:%M:%S'), self.tag, msg, endl)
        sys.stdout.write(self.fmt(msg))
        sys.stdout.flush()

    def nfo(self, msg, endl='\n'):
        self.prn(msg,
                 prefix='@cI ',
                 endl=endl)

    def wrn(self, msg, endl='\n'):
        self.prn(msg,
                 prefix='@yW ',
                 endl=endl)

    def err(self, msg, endl='\n'):
        self.prn(msg,
                 prefix='@rE ',
                 endl=endl)

    def dbg(self, msg, endl='\n'):
        self.prn(msg,
                 prefix='@dD ',
                 endl=endl)

    def fatal(self, msg, endl='\n'):
        self.prn(msg,
                 prefix='@RF ',
                 endl=endl)
        raise RuntimeError(self.fmt(msg))

    def checker(self, msg, checker, ok=' @gSUCCESS', bad=' @rFAILED'):
        res = ok if checker else bad
        self.nfo(msg + res)

    def progress(self, it, prefix='', size=60, annot=[]):
        if not it or 0 == len(it):
            self.fatal("logger::progress  invalid arg it")
            return
        count = len(it)

        def _show(_i):
            x = int(size * _i / count)
            self.raw("%s[%s%s] %i/%i @p%-20s" %
                     (prefix, '#' * x, '.' * (size - x), _i, count,
                      annot[_i] if len(annot) > _i else ''), endl='\r')

        _show(0)
        for i, item in enumerate(it):
            yield item
            _show(i + 1)
        sys.stdout.write("\n")
        sys.stdout.flush()

    def self_test(self):
        import time
        self.prn(
            '@rRED @p PURPLE @y YELLOW @g GREEN @c CYAN @b BLUE @d DARK ')
        self.prn(
            '@RRED @P PURPLE @Y YELLOW @G GREEN @C CYAN @B BLUE @D DARK ')

        self.dbg('It is debug message')
        self.nfo('It is info  message')
        self.wrn('It is warn  message')
        self.err('It is error message')

        for x in xrange(10):
            self.checker('pass: @B' + str(x), (x % 2 == 0))

        for i in self.progress(xrange(15), "progress: "):
            time.sleep(0.4)


def get(tag):
    return Logger(tag)


# test




if __name__ == '__main__':
    log = get('LOG')
    log.self_test()
