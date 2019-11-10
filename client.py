#This is the python script to be run on the client's end and to be
#used in the kivy-based gui set up for the aforementioned client
import hashlib
from datetime import date
from Pyro5.api import expose, behavior, Daemon
import encryption as enc
import Block
import yaml
import schedule
import time

prior_config = {}
config = {}
exit_status = 0

def read():
    stream = open("config.yaml", 'r')
    if prior_config != yaml.load(stream, Loader = yaml.SafeLoader):
        global config
        config = yaml.load(stream, Loader = yaml.SafeLoader)

def newRequest():


def exit():
    global exit_status
    exit_status = 1

schedule.every(2).seconds.do(read)

while exit_status == 0:
    schedule.run_pending()
    time.sleep(1)