import time

class transaction:

    def __init__(self, sender,receiver, coins):
        #self.txid = #incremented global txid + current time
        self.sender = sender
        self.receiver = receiver
        self.coins = coins
        self.timestamp = time.time()
#
    def __repr__(self):
        #TxnID: ID x pays ID y C coins
        return str(self.txid) + ": " + str(self.sender) + " pays " + str(self.receiver) + str(self.coins) +" coins"

