import network
import sys
import errno
import gc
import uos as os
import utime as time
import ujson as json
import ubinascii as binascii

from machine import unique_id
from http_handler import HttpHandler
from network import WLAN, AP_IF, STA_IF, hostname
from micropython import const

CACHE_FILENAME = const('cache.json')

class OpenGate:
    def __init__(self):
        self.__start_server()

    def __connect_sta(self, ssid, password):
        wlan = WLAN(STA_IF)
        wlan.active(True)
        wlan.config(pm=0xa11140)
        wlan.connect(ssid, password)
        
        for i in range(10):
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            print('waiting for connection...')
            time.sleep(1)
        
        if wlan.status() != 3:
            self.__init_ap()
        else:
            print('connected')
            status = wlan.ifconfig()
            print('ip = ' + status[0])
            handler = HttpHandler(status[0], CACHE_FILENAME)
            handler.listen()
            
        self.__set_hostname()

    def __init_ap(self):
        ssid = 'Sesame-' + binascii.hexlify(unique_id()).decode()
        
        ap = WLAN(AP_IF)
        ap.config(essid=ssid, password='123456789')
        ap.active(True)
        
        status = ap.ifconfig()
        
        print('Access point active')
        print(status)
        
        handler = HttpHandler(status[0], CACHE_FILENAME)
        handler.listen()
        
        self.__set_hostname()

    def __set_hostname(self):
        hostname('sesame')
        print('network hostname: ', hostname())

    def __restart(self):
        gc.collect()
        app.shutdown()
        time.sleep(5)
        self.__start_server()

    def __start_server(self):
        if CACHE_FILENAME not in os.listdir():
            self.__init_ap()
        else:
            with open(CACHE_FILENAME, 'r') as cache:
                data = json.load(cache)
                cache.close()
              
                ssid = data['ssid']
                password = data['password']
                
                self.__connect_sta(ssid, password)

        gc.enable()
        gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
        gc.collect()
