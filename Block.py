import hashlib
import datetime


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


# class for our Chain
class HackathonChain:
    def __init__(self): # initializes the block chain with a Genesis block
        self.blocks = [self.get_genesis_block()]

    def get_genesis_block(self):
        return HackathonBlock(0,
                              datetime.datetime.utcnow(),
                              'Genesis',
                              'arbitrary')

    def add_block(self, data):
        self.blocks.append(HackathonBlock(len(self.blocks),
                                          datetime.datetime.utcnow(),
                                          data,
                                          self.blocks[len(self.blocks) - 1].hash))

    def get_chain_size(self):  # exclude genesis block
        return len(self.blocks) - 1

    def get_block_data(self, index):
        return self.blocks[index].get_data()


if __name__ == "__main__":
    print("Asuh")
    chain = HackathonChain()
    print(chain.get_block_data(0))
    chain.add_block('Equifax')
    print(chain.get_block_data(1))
    print("Peace")