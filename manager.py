import peer
import random
import time
import numpy as np

class Manager:
    #simulation_time = time.time()
    
    def __init__(self, peer):
        self.peer = peer
        self.env.process(self.run())

    def __repr__(self):
        return "ConnectionManager(%s)" % self.peer.name

    @property
    def env(self):
        return self.peer.env

    @property
    def connected_peers(self):
        return self.peer.connections.keys()

    def simulate(self):
        # CASE: too few peers
        #if random.randint(0,1):
        #    self.peer.generateTransaction()
        #check the time constraint before generating the txn

        if (self.peer.sim_time - self.peer.lasttransactiontime ) >= float(np.random.poisson(5,1)[0])/1000:
            self.peer.generateTransaction()

        #call the create block function with some distribution to keep a check on
        # rate of block arrival
        if (self.peer.sim_time - self.peer.lastblocktime ) >= float(np.random.poisson(self.peer.Tk_mean,1)[0])/1000: #hasnt heard a block, so create one
            self.peer.createBlock() #if it hasn't heard a block in tk+Tk time
            
        #if len(self.peer.blk_queue.keys()): #a block has arrived, so it must broadcast
        #    self.peer.broadcast()

    def run(self):
        while True:
            self.peer.sim_time = time.time()
            self.simulate()
            yield self.env.timeout(1)




