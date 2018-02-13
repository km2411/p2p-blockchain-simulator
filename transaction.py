import time
import random
import hashlib

class Transaction:

    def __init__(self, sender,receiver, coins):
        self.timestamp = time.time()
        self.txid = hashlib.md5(str(random.randint(1,100))+str(self.timestamp)).hexdigest()#incremented global txid + current time
        self.sender = sender
        self.receiver = receiver
        self.coins = coins
        self.status = False #transaction not included in the block
        #self.size = len(repr(self))
    
    def __repr__(self):
        #TxnID: ID x pays ID y C coins
        #rint "timestamp: " + str(self.timestamp)
        return str(self.txid) + ": " + str(self.sender) + " pays " + str(self.receiver.name) + " " + str(self.coins) +" coins"

