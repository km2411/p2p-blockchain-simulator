import simpy
from messages import BaseMessage
from transaction import transaction
import random
import block

class Connection(object):
    """
    Models the data transfer between peers and the implied latency
    """

    def __init__(self, env, sender, receiver):
        self.env = env
        self.sender = sender
        self.receiver = receiver
        self.start_time = env.now

    def __repr__(self):
        return '<Connection %r -> %r>' % (self.sender, self.receiver)

    @property
    def round_trip(self):
        # basically backbone latency
        # evenly distributed pseudo random round trip times
        rt_min, rt_max = 10, 300 # ms
        return (rt_min + (id(self.sender) + id(self.receiver)) % (rt_max-rt_min)) / 1000.

    @property
    def bandwidth(self):
        return min(self.sender.bandwidth_ul, self.receiver.bandwidth_dl)

    def send(self, msg, connect=False):
        """
        fire and forget
        i.e. we don't get notified if the message was not delivered

        connect : deliver message even if not connected yet
        """
        def _transfer():
            bytes = msg.size
            delay = bytes / self.sender.bandwidth_ul
            delay += bytes / self.receiver.bandwidth_dl
            delay += self.round_trip / 2
            yield self.env.timeout(delay)
            if self.receiver.is_connected(msg.sender) or connect:
                self.receiver.msg_queue.put(msg)
#                print self, 'delivered', msg
#        print self, 'transfering', msg
        self.env.process(_transfer())


class BaseService(object):
    """
    Added to Peers to provide services like
    - connection management
    - monitoring
    - working on tasks

    """
    def handle_message(self, receiving_peer, msg):
        "this callable is added as a listener to Peer.listeners"
        pass

KBit = 1024 / 8

class Peer(object):

    #default bandwidth, but we update it at the time of creation.
    bandwidth_ul = 2400 * KBit # bytes/sec
    bandwidth_dl = 16000 * KBit # bytes/sec

    def __init__(self, name, peer_type, env):
        self.name = name
        self.type = peer_type
        self.unspentTransactions = []
        self.balance = 100
        self.env = env
        self.connections = dict()
        self.msg_queue = simpy.Store(env)       
        self.active = True
        self.services = [] # Service.handle_message(self, msg) called on message
        self.disconnect_callbacks = []
        env.process(self.run())

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

    def receive(self, msg):
#        print self, 'received', msg
        assert isinstance(msg, BaseMessage)
        for s in self.services:
            assert isinstance(s, BaseService)
            s.handle_message(self, msg)

    def send(self, receiver, msg):
        # fire and forget
        assert msg.sender == self
        self.connections[receiver].send(msg)

    def broadcast(self, msg):
        for other in self.connections:
            self.send(other, msg)

    def generateTransaction(self):
        #peer should know of all the nodes in the network to whom it can send coins
        #global peers
        #l = len(peers)
        #r = random.randint(0,l) #peer can generate a transaction to himself too
        receiver = self
        for other in self.connections:
            if random.randint(0,1):
                receiver = other
                break

        sender=self.name
        if self.balance < 1:
            print "insufficient balance"
            return

        coins = random.randint(1,self.balance)
        tx = transaction(self.name, receiver, coins)
        self.broadcast(tx)
        print tx        
        return 

    def createBlock(self):
        #check to see if it has number of unspent transactions >= required block size
        #select the transactions sorted on timestamp
        if len(self.unspentTransactions) < 5:
            print 'wait for more transactions'
            return 
            
        lisofTransactions = self.unspentTransactions[:5]
        self.unspentTransactions = self.unspentTransactions[5:] 
        newBlock = block(lisofTransactions)
        self.broadcast(newBlock)
        #have to update the balance, the mining fees once the block gets added to the chain   
        return 

    def run(self):
        while True:
            # check network for new messages
            #print self, 'waiting for message'
            r = random.randint(0,1)
            if r:
                self.generateTransaction()
                print str(self.name) + " generating txn"

            msg = yield self.msg_queue.get()
            self.receive(msg)

