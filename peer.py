import simpy
from transaction import Transaction
import random
import numpy as np
from block import Block
from block import BlockChain
import time

class Connection(object):
    """
    Models the data transfer between peers and the implied latency
    """

    def __init__(self, env, sender, receiver):
        self.env = env
        self.sender = sender
        self.receiver = receiver
  
    def __repr__(self):
        return '<Connection %r -> %r>' % (self.sender, self.receiver)

class Peer(object):

    UTXO = [] #unspent txn pool 
    sim_time = time.time() #this is the global time in seconds 
    pij = np.random.uniform(10,500)
    dij = 96*1000 #bits
    genesisBlock = Block([],None)
    genesisBlock.blkid = '00000000000000000000000000000000'
    globalChain = BlockChain(genesisBlock) #initialize a blockchain with genesis block
    all_peers = []
    AVG_BLK_ARR_TIME = len(all_peers)*3000 #no. of peers*max_delay
   
    def __init__(self, name, peer_type, env):
        self.name = name
        self.type = peer_type
        self.unspentTransactions = []
        self.balance = 100
        self.lasttransactiontime = self.sim_time
        self.lisofBlocks = [self.genesisBlock]
        self.lastBlockHeard = self.genesisBlock #default time of genesis block
        self.lastBlockArrTime = self.sim_time
        self.localChain = self.globalChain
        self.Tk_mean = float(np.random.poisson(self.AVG_BLK_ARR_TIME,1)[0]) #average arrival time of a block proportion to cpu power
        self.env = env
        self.connections = dict()
        self.txn_queue = {}    
        self.blk_queue = {}    
          
        #self.env.process(self.run())

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)
    
    def connect(self, other):
        if not self.is_connected(other):
            print "%r connecting to %r" % (self, other)
            self.connections[other] = Connection(self.env, self, other)
            if not other.is_connected(self):
                other.connect(self)

    def is_connected(self, other):
        return other in self.connections

    def computeDelay(self,other,msg):
        size = 0 
        if isinstance(msg,Block):
            size = 8*pow(10,6) #bits

        delay = self.pij
        cij = 5*pow(10,3) #bits per ms

        if self.type == other.type == 'fast':
            cij = 100*pow(10,3)

        prop = float(size)/cij
        queing = float(self.dij)/cij

        delay += prop + queing #in ms
        #check the resolution of the delay
        return float(delay)/1000 

    def broadcast(self, msg, delay):
        #print "message is :" + str(msg)
        
        if isinstance(msg,Transaction):
            for other in self.connections:
                if not(other == self):
                    if msg not in other.unspentTransactions:
                        other.unspentTransactions.append(msg)
                        arrival_time = delay + self.computeDelay(other,msg)
                        other.lasttransactiontime = arrival_time
                        other.txn_queue[msg.txid] = arrival_time
                        other.broadcast(msg, arrival_time)

                        if other.name == 'p1':
                            #print "Updated Transactions for p1"
                            #print other.unspentTransactions
                            pass
        #broadcast a block        
        else:
            for other in self.connections:
                if not(other == self):
                    if msg.blkid not in other.blk_queue.keys():
                        arrival_time = delay + self.computeDelay(other,msg)
                        #detect fork here by checking the arrival time and lastblock time
                        flag = other.detectFork(msg, arrival_time) #boolean
                        if not flag:
                            other.updateChain(msg,arrival_time)
                            other.blk_queue[msg.blkid] = arrival_time
                            other.broadcast(msg, arrival_time)
                        
                        if other.name == 'p1':
                            print "Block heard by p1"
                            print other.blk_queue
    
    def detectFork(self, msg, arrival_time):
        #same parentlink with different arrival times, different block, resolve fork with latest
        if msg.parentlink == self.lastBlockHeard.parentlink:
            if arrival_time > self.lastBlockArrTime:
                self.lisofBlocks.append(msg) #select the chain with first arrived block
                self.lastBlockHeard = msg
                self.lastBlockArrTime = arrival_time
                self.blk_queue[msg.blkid] = arrival_time
                self.broadcast(msg, arrival_time)
                return True  #just add the new block to the list and broadcast
            else:
                self.resolveFork(msg, arrival_time) #extend with msg block
                self.lisofBlocks.append(msg) #select the chain with first arrived block
                self.blk_queue[msg.blkid] = arrival_time
                self.broadcast(msg, arrival_time)

        return False
    
    def resolveFork(self, msg, arrival_time):
        #here we remove the last block from the localchain and add msg
        self.localChain.removeLast()
        self.localChain.addBlock(msg)
        
    def updateChain(self,newBlock,arrTime):
        newBlock.parentlink = self.lastBlockHeard.blkid
        self.lisofBlocks.append(newBlock)
        self.localChain.addBlock(newBlock)
        self.lastBlockArrTime = newBlock.arrTime
        
    def generateTransaction(self):
        receiver = self
      
        for other in self.connections:
            #select a random peer to whom to pay the coins
            if random.randint(0,1) and other.name !='PeerServer':
                receiver = other
                break
                
        sender=self.name
       
        if self.balance < 1:
            print "insufficient balance"
            return

        coins = random.randint(1,self.balance)
        #update balance    

        tx = Transaction(self.name, receiver, coins)
        self.lasttransactiontime = time.time()
        #add the new transaction to the unspent pool 
        self.UTXO.append(tx)

        if self.name == 'p1':
            self.unspentTransactions.append(tx)
            #print "Sender List"
            #print self.unspentTransactions
        self.broadcast(tx, tx.timestamp)
        #print str(self.name) + " generating transaction--> TX" + str(tx)        
        return 

    def updateUTXO(self):
        return

    def createBlock(self):
        #check to see if it has number of unspent transactions >= required block size
        #select the transactions sorted on timestamp
        print str(self) + " is mining...."
       
        if len(self.unspentTransactions) == 0:
            #check in the UTXO
            self.unspentTransactions.extend(self.UTXO)
            if len(self.unspentTransactions) == 0:
                print 'There are no unspent transactions'
                return 
        #add the transactions to the block, max 10

        lisofTransactions = self.unspentTransactions[:10]
        self.unspentTransactions = self.unspentTransactions[10:] 
       
        newBlock = Block(lisofTransactions,self)
        newBlock.parentlink = self.lastBlockHeard.blkid
        self.lisofBlocks.append(newBlock)
        self.blk_queue[newBlock.blkid] = newBlock.timestamp
        self.localChain.addBlock(newBlock)
        self.lastBlockArrTime = newBlock.timestamp
        self.broadcast(newBlock, newBlock.timestamp)
        #mark the txns in the UTXO spent
        #have to update the balance, the mining fees once the block gets added to the chain   
        return 