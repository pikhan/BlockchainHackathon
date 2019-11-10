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

prior_config = {'Initial'}
config = {'First'}
numRequests = 0
exit_status = 0
chain = []

first_stream = open("config.yaml", 'r')
first_temp = yaml.load(stream, Loader=yaml.SafeLoader)
if(first_temp['Initial Setup'] == 'Yes'):
    chain = Block.HackathonChain()
    with open('config.yaml') as f:
        doc = yaml.load(f)
    doc['Initial Setup'] = state

    with open('file_to_edit.yaml', 'w') as f:
        yaml.dump(doc, f)

def read():
    stream = open("config.yaml", 'r')
    global prior_config
    temp = yaml.load(stream, Loader = yaml.SafeLoader)
    if (prior_config != temp):
        global config
        config = temp
        prior_config = temp
        print(config)

def newRequest(doctype, orig, vendor, requestee):
    chain.add_block(doctype, None, date.today(), orig, vendor, requestee)

def completeRequest():
    


def exit():
    global exit_status
    exit_status = 1

schedule.every(2).seconds.do(read)

while exit_status == 0:
    schedule.run_pending()
    time.sleep(1)