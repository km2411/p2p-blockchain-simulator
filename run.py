import random
import simpy
import sys
from peer import  Peer
from manager import Manager
import numpy as np

# No. of peers
n = int(sys.argv[1])
Peer.num_peers = n
SIM_DURATION = 240
#Mbits = 8*1000000
VISUALIZATION = False
#VISUALIZATION = True

def initializePeer(peer_id, peer_type, env):
    return Peer(peer_id, peer_type, env)
    
def createPeers(peer_server, numOfPeers):
    peers = []
    # set z 
    z = 50
    for i in range(numOfPeers):
        if i < int(numOfPeers * (z / 100)):
            p = initializePeer('p%d' % i, 'slow', env)
        else:
            p = initializePeer('p%d' % i, 'fast', env)

        #p.connect(peer_server)
        peers.append(p)
        
        '''
        if p.type == 'slow':
            p.bandwidth_upload = p.bandwidth_download = 5 * Mbits
        else:
            p.bandwidth_upload = p.bandwidth_download = 100 * Mbits
        '''
    return peers

env = simpy.Environment()

#make a peer server, a boot node which is slow in nature
pserver = initializePeer('PeerServer', 'slow', env)

#intilize the distributions
#dist to select number of connections for a peer 
peers = createPeers(pserver, n)
Peer.all_peers=peers
#print "Peers..." + str(Peer.all_peers)
print("Starting Simulator")
print "Peers Connecting...."
for p in peers:
    while len(p.connections.keys()) < 1 + np.random.binomial(n,0.5,1):
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
for p in Peer.all_peers:
    filename = p.name + ".txt"
    f = open(filename,'w')
    f.write('[ "None", ')
    for b in p.blk_queue.keys():
        f.write("'")
        f.write(str(b))
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