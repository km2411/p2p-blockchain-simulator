Simulation of a P2P Cryptocurrency Network

Features
======================
For the assignment we have used a python package 'SimPy' to do discrete event simulation in time. 

We demonstrate a simulation of
- random peer connections in the network 
- random transaction generation by each peer with a value chosen from poisson distribution
- broadcasting the messages (transactions/blocks) in a loopless manner
- simulating network latencies based on propogation delay, message size, link speeds of nodes, and queing delay
- random block creating with arrival times chosen from a poisson distribution
- propogation of blocks on the block chain
- addition of blocks to a local blockchain of a node and resolution of forks based on block arrival time, the chain with first arrived one is extended.

Project Structure
======================
Classes Defined:

1. Peer - to define a peer, create a p2p network 
2. Manager - to simulate each peer in time, a peer manager
3. Transaction 
4. Block
5. Blockchain
6. Connection - to create a connection bw 2 peers

Usage
======================
Input Parameter:

1. n =  No. of peers
2. z = percent of slow nodes
3. txn_interval_mean = mean for dist. to choose arrival time from, in ms
4. mean_Tk = mean value for dist. for choosing Tk for each node,in ms
5. mean_links = mean for binomial dist., higher the value, denser is the network
6. SIM_DURATION = duration of simulation in ms

To start the simulation-

1. In the project folder, '$python run.py' [with proper arguments].
2. To see the network graph, set VISUALIZATION = True in 'run.py', this can be done to check if the graph is connected/ dissconnected.
3. At the end of the simulation, for each peer, file having tree at the node is created in the project folder.
