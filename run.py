import random
import simpy
import sys
from peer import  Peer
from peermanager import ConnectionManager
from peermanager import PingHandler
from peermanager import PeerRequestHandler
from disruptions import Downtime
from disruptions import Slowdown

# No. of peers
n = int(sys.argv[1])
SIM_DURATION = 1/100
Mbits = 1000000
#VISUALIZATION = False
VISUALIZATION = True

def initializePeer(peer_id, peer_type, env):
    p = Peer(peer_id, peer_type, env)
    #now append what all services you want for a peer
    p.services.append(ConnectionManager(p))
    p.services.append(PeerRequestHandler())
    p.services.append(PingHandler())
    p.services.append(Downtime(env, p))
    p.services.append(Slowdown(env, p))
    return p


def createPeers(peer_server, numOfPeers):
    peers = []
    # set z 
    z = 50
    for i in range(numOfPeers):
        if i < int(numOfPeers * (z / 100)):
            p = initializePeer('p%d' % i, 'slow', env)
        else:
            p = initializePeer('p%d' % i, 'fast', env)

        # connect to server
        connection_manager = p.services[0]
        print connection_manager
        connection_manager.connect_peer(peer_server)

        peers.append(p)
    
    # set DSL bandwidth
    for p in peers:
        if p.type == 'slow':
            p.bandwidth_upload = p.bandwidth_download = 5 * Mbits
        else:
            p.bandwidth_upload = p.bandwidth_download = 100 * Mbits

    return peers

env = simpy.Environment()

#make a peer server, a boot node which is slow in nature
pserver = initializePeer('PeerServer', 'slow', env)
pserver.bandwidth_upload = pserver.bandwidth_download = 5 * Mbits

peers = createPeers(pserver, n)

print("Starting Simulator")
if VISUALIZATION:
    from animate import Visualizer
    Visualizer(env, peers)
else:
    env.run(until=SIM_DURATION)
