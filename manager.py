import peer
import random
import time
import numpy as np
import operator

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
        #check the time constraint before generating the txn

        if (self.peer.sim_time - self.peer.lasttransactiontime ) >= float(np.random.poisson(5,1)[0])/1000:
            self.peer.generateTransaction()

        #call the create block function with some distribution to keep a check on
        # rate of block arrival
        if (self.peer.sim_time - self.peer.lastBlockArrTime) >= float(np.random.poisson(self.peer.Tk_mean,1)[0])/1000: #hasnt heard a block, so create one
            self.peer.createBlock() #if it hasn't heard a block in tk+Tk time

        #if len(self.peer.blk_queue.keys()): #a block has arrived, so it must broadcast
        #    self.peer.broadcast()

        #check if all the nodes have the block last propogated

    def getConsensus(self):
        blocks_on_nw = {}
        listofblocks_nw = []
        majority = 1 + len(self.all_peers)/2
        
        for p in self.all_peers:
            #case when the block has not yet reached a peer
            #in that case we wait to get consensus or do it by majority
            x = p.blk_queue #sort the blk_queue for all on arrival time
            sorted_x = sorted(x.items(), key=operator.itemgetter(1))
            latestblock = sorted_x[0][0]
            listofblocks_nw.append(next((x for x in p.listofBlock if x.blkid == latestblock),[]))
            
            if latestblock in blocks_on_nw.keys():
                l = [p]
                l.extend(blocks_on_nw[latestblock])  #no of peers having this block
                blocks_on_nw[latestblock] = l #append peer to listofpeers having that block
            
            else:
                blocks_on_nw[latestblock] = [p]

        if len(blocks_on_nw.keys()) == 1: #no fork 
            #check if majority satisfied ,update timestamp of block after adding
            if len(blocks_on_nw[latestblock]) >= majority:
                #add to global chain, local chain of peers, update balance, UTXO, pop blk_q
                self.peer.globalChain.addBlock(next((x for x in listofblocks_nw if x.blkid == latestblock), None))
            else:
                self.getConsensus() #try again 
        else:#resolve fork

    def run(self):
        while True:
            self.peer.sim_time = time.time()
            self.simulate()
            self.getConsensus()
            yield self.env.timeout(1)




