import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# key class
class HackathonKeyBlock:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
                                public_exponent=65537,
                                key_size=2048,
                                backend=default_backend()
                            )
        self.public_key = self.private_key.public_key()


# key chain class
class HackathonKeyChain:
    def __init__(self):
        self.key_blocks = [self.get_genesis_key()]

    def get_genesis_key(self):
        return HackathonKeyBlock()

    def add_key_block(self):
        self.key_blocks.append(HackathonKeyBlock())