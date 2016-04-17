import unittest

import sys

import time
import numpy as np

from urh.cythonext import hackrf

class TestHackRF(unittest.TestCase):
    def callback_fun(self, buffer):
        out = []
        for i in range(0,len(buffer), 4):
            try:
                r = np.fromstring(buffer[i:i+2], dtype=np.float16)/32767.5
                i = np.fromstring(buffer[i+2:i+4], dtype=np.float16)/32767.5
            except ValueError:
                continue
            if r and i:
                print(r,i)
            #out.append(complex(float(buffer[i:i+1])/32767.5, float(buffer[i+2:i+3])/32767.5))

        return 0


    def test_set_rx(self):
        hackrf.setup()
        hackrf.set_freq(433.92e6)
        print(hackrf.is_streaming())
        hackrf.start_rx_mode(self.callback_fun)
        #time.sleep(1)
        while hackrf.is_streaming():
            pass
         #   #time.sleep(0.1)
        hackrf.stop_rx_mode()

    def test_fromstring(self):
        buffer = b'\xfa\xfa\xff\xfa\xff\xf0\xff\xfa'
        r = np.empty(len(buffer)//4, dtype=np.float16)
        i = np.empty(len(buffer)//4, dtype=np.float16)
        c = np.empty(len(buffer)//4, dtype=np.complex64)

        for j in range(0, len(buffer), 4):
            r[j//4] = np.frombuffer(buffer[j:j + 2], dtype=np.float16) / 32767.5
            i[j//4] = np.frombuffer(buffer[j + 2:j + 4], dtype=np.float16) / 32767.5
        #r2 = np.fromstring(buffer[], dtype=np.float16) / 32767.5
        c.real = r
        c.imag = i
        print(c)
        #x,y = np.frombuffer(buffer, dtype=[('x', np.float16), ('y', np.float16)])