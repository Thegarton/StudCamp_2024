from builtins import bytes, int

import os
import time
import threading
from threading import Timer
from subprocess import call


from led_function import LED
led = LED()

import xr_config as cfg
#led.rainbow(3)
#     # for i in range(1, 3):
#     #     led.epilepsy(i)
led.set_ledgroup(cfg.POWER_LIGHT, 8, cfg.COLOR['black'])
led.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
    #time.sleep(1)
    # car_light.set_ledgroup(cfg.POWER_LIGHT, 6, cfg.COLOR['orange'])
    # time.sleep(5)
    # car_light.set_ledgroup(cfg.POWER_LIGHT, 2, cfg.COLOR['red'])
    # time.sleep(5)