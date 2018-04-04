import random
import simpy
import sys
from peer import  Peer
from manager import Manager
import numpy as np

n = int(sys.argv[1]) # No. of peers
z = int(sys.argv[2]) #percent of slow nodes
txn_interval_mean = int(sys.argv[3]) #in ms
mean_Tk = int(sys.argv[4]) #in ms
mean_links = int(sys.argv[5]) #mean for binomial dist., higher the value, denser is the network
SIM_DURATION = int(sys.argv[6]) #in ms
VISUALIZATION = False

Peer.mean_Tk = mean_Tk #default (3000*n) ms
Peer.txn_interval_mean = txn_interval_mean #default 10 ms

def initializePeer(peer_id, peer_type, env):
    return Peer(peer_id, peer_type, env)
    
def createPeers(peer_server, numOfPeers):
    peers = []
    for i in range(numOfPeers):
        if i <= int(numOfPeers * (float(z) / 100)):
            p = initializePeer('p%d' % i, 'slow', env)
        else:
            p = initializePeer('p%d' % i, 'fast', env)
        #p.connect(peer_server)
        peers.append(p)
    return peers

env = simpy.Environment()

#make a peer server, a boot node which is slow in nature
pserver = initializePeer('PeerServer', 'slow', env)

#dist to select number of connections for a peer 
peers = createPeers(pserver, n)
Peer.all_peers=peers

print("Starting Simulator")
print "Peers Connecting...."

for p in peers:
    links = 1 + np.random.binomial(n,float(mean_links)/100,1)
    while len(p.connections.keys()) < links:
        for other in peers:
            prob = random.randint(0,1)
            if prob and (p != other):
                p.connect(other)
        
    m = Manager(p)
    m.simulate()

if VISUALIZATION:
    from animate import Visualizer
    Visualizer(env, peers)
else:
    env.run(until=SIM_DURATION)

print "simulation has ended..."

#output each node's tree to a file
for p in Peer.all_peers:
    print p, p.type
    filename = p.name + ".txt"
    f = open(filename,'w')
    f.write('[ "None", ')
    for b in p.blk_queue.keys():
        f.write("'")
        f.write(str(b))
        #f.write(str(" ArrTime : ")str(p.blk_queue[b]))
        f.write("'")
        f.write(',')
    f.write(']')
    f.write('\n')
    f.write('[')    
    f.write('\n')
    count =0
    for b in p.listofBlocks:
        f.write('{ from:')
        if b.parentlink ==None:
            f.write("'None'")
        else:
            arr_time_parent = str(p.blk_queue[b.parentlink])
            f.write("'")
            f.write(str(b.parentlink))# +" "+ arr_time_parent)
            f.write("'")
        f.write(', to:')
        if b.blkid =='00000000000000000000000000000000':
            f.write("'00000000000000000000000000000000'")
        else:
            arr_time_block = str(p.blk_queue[b.blkid])
            f.write("'")
            f.write(str(b.blkid))# +" "+ arr_time_block)
            f.write("'")
        edge = 'e'+str(count)
        f.write(", name: '")
        f.write(edge)
        f.write("'},")
        f.write('\n')
    f.write(']')
    f.close()