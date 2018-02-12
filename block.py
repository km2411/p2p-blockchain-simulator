import time

class Block:
	size = 5 # number of transactions

	def __init__(self, listofTransactions):#self.blkid = #increment a global txid plus current time
		self.timestamp = time.time()
		self.blkid = hashlib.md5(str(self.timestamp)).hexdigest()
		self.transactions = listofTransactions
		
	def __repr__(self):
		return str(self.blkid)
