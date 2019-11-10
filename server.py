#This is the python script that runs on the server-end. This code is to be never be
#shared with anyone else for it permits access to sensitive information.

import hashlib
import datetime
from Pyro5.api import expose, behavior, Daemon
import encryption as enc
import Block
import yaml
import schedule
import time

config = {}
exit_status = 0


def read():
    stream = open("config.yaml", 'r')
    config = yaml.load(stream, Loader=yaml.SafeLoader)
    print(config)



def exit():
    global exit_status
    exit_status = 1


schedule.every(2).seconds.do(read)

while exit_status == 0:
    schedule.run_pending()
    time.sleep(1)
