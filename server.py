#This is the python script that runs on the server-end. This code is to be never be
#shared with anyone else for it permits access to sensitive information.

import hashlib
import datetime
from Pyro5.api import expose, behavior, Daemon
import encryption as enc
import Block
import yaml

def main():
    stream = open("config.yaml", 'r')
    config_options = yaml.load(stream, Loader = yaml.SafeLoader)
    if config_options['initial_setup'] == 0:
        createMasterBlockchain()
        for i in range(config_options['Number of Entities']-1)
            createLocalBlockchain()

if __name__ == "__main__":
    main()