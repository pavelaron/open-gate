import machine

from sesame import Sesame
from logger import Logger

if __name__ == '__main__':
    try:
        Sesame()
    except KeyboardInterrupt:
        pass
    except Exception as error:
        Logger(error)
        machine.reset()