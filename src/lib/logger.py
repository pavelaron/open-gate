import utime as time
import uio as io
import uos as os
import sys

from micropython import const

LOGFILE = const('log.txt')
LOGFILE_BACKUP = const('log-backup.txt')

class Logger:
    def __init__(self, error):
        try:
            self.__log(error)
        except Exception as exception:
            print(exception)

    def __log(self, error):
        self.__cleanup()
        
        now = time.localtime()
        stamp = '[{}-{:02d}-{:02d}, {:02d}:{:02d}:{:02d}]' \
                .format(now[0], now[1], now[2], now[3], now[4], now[5])
        
        with open(LOGFILE, 'a') as log:
            if error is not Exception:
                log.write('{}:\n{}\n\n'.format(stamp, str(error)))
            else:
                buf = io.StringIO()
                sys.print_exception(error, buf)
                
                log.write('{}:\n{}\n\n'.format(stamp, buf.getvalue()))

            log.close()

    def __cleanup(self):
        files = os.listdir()
        
        if LOGFILE not in files:
            return
            
        size = os.stat(LOGFILE)[6]
        if size < 5 * 1024:
            return
        
        if LOGFILE_BACKUP in files:
            os.remove(LOGFILE_BACKUP)
            
        os.rename(LOGFILE, LOGFILE_BACKUP)
