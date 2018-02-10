import time

class block:
	size = 5 # number of transactions

	def __init__(self, listofTransactions):#self.blkid = #increment a global txid plus current time
		self.transactions = listofTransactions
		self.timestamp = time.time()

	def __repr__(self):
		return str(self.blkid)
