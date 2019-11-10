#This is the python script to be run on the client's end and to be
#used in the kivy-based gui set up for the aforementioned client
import hashlib
from datetime import date
import Pyro5.api
from Pyro5.core import locate_ns

import encryption as enc
import Block
import yaml
import schedule
import time

first_stream = open("config.yaml", 'r')
first_temp = yaml.load(first_stream, Loader=yaml.SafeLoader)


def printEntityIDQuestion():
    print("Just a test")


def readEntityID():
    return "Test"


if(first_temp['Initial Setup'] == 'Yes'):
    global chain
    chain = Block.HackathonChain()
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
    temp = yaml.load(stream, Loader = yaml.SafeLoader)
    if (prior_config != temp):
        global config
        config = temp
        prior_config = temp
        print(config)

def newRequest(doctype, orig, vendor, requestee):
    chain.add_block(doctype, None, date.today(), orig, vendor, requestee)

def completeRequest():
    print("Nothing")


def exit():
    global exit_status
    exit_status = 1

prior_config = {'Initial'}
config = {'First'}
numRequests = 0
exit_status = 0
chain = []
EntityId = 'Initial'

schedule.every(2).seconds.do(read)
with Pyro5.api.Daemon(host=Block.HOST_IP, port=Block.HOST_PORT) as daemon:
    chain_uri = daemon.register(chain)
    with locate_ns() as ns:
        ns.register("Block.HackathonChain."+EntityId, chain_uri)
    daemon.requestLoop()

while exit_status == 0:
    schedule.run_pending()
    time.sleep(1)