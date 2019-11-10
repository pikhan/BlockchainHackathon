# This is the python script to be run on the server's end and to be
# executed only on the server machine, that is not on the GUI end product
import hashlib
from datetime import date
import Pyro4


import encryption as enc
import Block
import yaml
import schedule
import time

chain = Block.HackathonChain()

first_stream = open("config.yaml", 'r')
first_temp = yaml.load(first_stream, Loader=yaml.SafeLoader)


def printEntityIDQuestion():
    print("Just a test")


def readEntityID():
    return "Test"


if (first_temp['Initial Setup'] == 'Yes'):
    with open('config.yaml') as f:
        doc = yaml.load(f)
    doc['Initial Setup'] = 'No'
    with open('file_to_edit.yaml', 'w') as f:
        yaml.dump(doc, f)
    printEntityIDQuestion()
    global EntityId
    EntityId = readEntityID()


def read():
    stream = open("config.yaml", 'r')
    global prior_config
    temp = yaml.load(stream, Loader=yaml.SafeLoader)
    if (prior_config != temp):
        global config
        config = temp
        prior_config = temp
        print(config)


def newRequest(doctype, orig, vendor, requestee):
    chain.add_block(doctype, None, date.today(), orig, vendor, requestee)


def completeRequest():
    print("Nothing")

newRequest(Block.dd_type.text)
def exit():
    global exit_status
    exit_status = 1


prior_config = {'Initial'}
config = {'First'}
numRequests = 0
exit_status = 0
EntityId = 'Initial'

schedule.every(2).seconds.do(read)
Pyro4.config.HOST = "127.0.0.1"
Pyro4.Daemon.serveSimple(
        {
            chain: EntityId+".chain"
        },
        ns = True)

while exit_status == 0:
    schedule.run_pending()
    time.sleep(1)
