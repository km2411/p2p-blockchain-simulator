from peer import BaseService, Connection

class manager:
  
    ping_interval = 1

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
        if random.randint(0,1):
                print str(self.name) + " generating txn"
                self.generateTransaction()

    def run(self):
        while True:
            self.simulate()
            yield self.env.timeout(self.ping_interval)




