import machine

from open_gate import OpenGate
from logger import Logger

if __name__ == '__main__':
    try:
        OpenGate()
    except KeyboardInterrupt:
        pass
    except Exception as error:
        Logger(error)
        machine.reset()