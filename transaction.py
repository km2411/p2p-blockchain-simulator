import time
import random

class transaction:

    def __init__(self, sender,receiver, coins):
        self.txid = random.randint(1,100)#incremented global txid + current time
        self.sender = sender
        self.receiver = receiver
        self.coins = coins
        self.timestamp = time.time()
        self.size = len(repr(self))

    def __repr__(self):
        #TxnID: ID x pays ID y C coins
        return str(self.txid) + ": " + str(self.sender) + " pays " + str(self.receiver.name) + " " + str(self.coins) +" coins"

