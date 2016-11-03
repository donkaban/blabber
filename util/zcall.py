import sys
import os
import subprocess
import datetime
import logger

log = logger.get("UTL")


def zcall(cmd, col='@d', log_prefix='',return_ret_code=False):
    def out_adapt(msg, col):
        if msg == '':
            return

    proc = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=os.environ.copy())

    std_iterator = iter(proc.stdout.readline, b"")
    err_iterator = iter(proc.stderr.readline, b"")
    while proc.poll() is None:
        for line in std_iterator:
            log.dbg(log_prefix + col + line, endl='')
        for line in err_iterator:
            log.err(log_prefix + col + line, endl='')

    if return_ret_code:
        return proc.returncode
    return proc.returncode == 0


if __name__ == '__main__':

    zcall('ls -la')
    zcall('git status')