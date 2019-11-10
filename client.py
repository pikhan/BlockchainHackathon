#This is the python script to be run on the client's end and to be
#used in the kivy-based gui set up for the aforementioned client
import hashlib
import datetime
from Pyro5.api import expose, behavior, Daemon
import encryption as enc
import Block.py