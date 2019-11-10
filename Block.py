import hashlib
import datetime
from Pyro5.api import expose, behavior, Daemon


# class for containing our data to put inside the block
# dd --> due diligence
class HackathonData:
    def __init__(self, dd_type, dd_doc, dd_date, orig_fi_id, vendor_id, req_fi_id):
        self.dd_type = dd_type
        self.dd_doc = dd_doc  # should be .pdf or some kind of file like that
        self.dd_date = dd_date
        self.orig_fi_id = orig_fi_id
        self.vendor_id = vendor_id
        self.req_fi_id = req_fi_id

    def print_all_data(self):
        print("Type of Due Diligence:", self.dd_type)
        print("Document:", self.dd_doc)
        print("Date Completed:", self.dd_date)
        print("Original FI:", self.orig_fi_id)
        print("3rd Party Vendor:", self.vendor_id)
        print("Requesting FI:", self.req_fi_id)


# class for our actual Block
class HackathonBlock:
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.hashing()

    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.prev_hash).encode('utf-8'))
        return key.hexdigest()

    def get_index(self):
        return self.index

    def get_timestamp(self):
        return self.timestamp

    def get_data(self):
        return self.data

    def get_prev_hash(self):
        return self.prev_hash

    def get_hash(self):
        return self.hash

    def print_data(self):
        self.data.print_all_data()


# class for our Chain
@expose
@behavior(instance_mode="single")
class HackathonChain:
    def __init__(self):  # initializes the block chain with a Genesis block
        self.blocks = [self.get_genesis_block()]

    def get_genesis_block(self):
        return HackathonBlock(0,
                              datetime.datetime.utcnow(),
                              'Genesis',
                              'arbitrary')

    def add_block(self, dd_type, dd_doc, dd_date, orig_fi_id, vendor_id, req_fi_id):
        self.blocks.append(HackathonBlock(len(self.blocks),
                                          datetime.datetime.utcnow(),
                                          HackathonData(dd_type, dd_doc, dd_date, orig_fi_id, vendor_id, req_fi_id),
                                          self.blocks[len(self.blocks) - 1].hash))

    def get_chain_size(self):  # exclude genesis block
        return len(self.blocks) - 1

    def get_block_data(self, index):
        return self.blocks[index].get_data()

    def print_block_data(self, index):
        self.blocks[index].print_data()


def main():
    print("@ top")
    chain = HackathonChain()
    chain.add_block('SSAE18 Soc2', 'audit.pdf', '10/27/2018', 'Equifax', 'Amazon', 'FICO')
    chain.print_block_data(1)
    print("@ exit")
    Daemon.serveSimple(
            {
                HackathonChain: "genesis.hackathonchain"
            },
            ns=False)


if __name__ == "__main__":
    main()
