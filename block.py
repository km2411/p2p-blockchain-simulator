import time
import hashlib

class Block:
	size = 10 # number of transactions
	def __init__(self, listofTransactions, miner):#self.blkid = #increment a global txid plus current time
		self.timestamp = time.time()
		self.blkid = hashlib.md5(str(self.timestamp)).hexdigest()
		self.transactions = listofTransactions
		self.miner = miner
		self.parentlink = None

	def __repr__(self):
		return str(self.blkid)

class BlockChain:
	listofBlocks = []

	def __init__(self, newBlock):
		self.newBlock = newBlock
		self.listofBlocks.append(self.newBlock)

	def addBlock(self,newBlock):
			
	def displayChain(self):
		while len(self.listofBlocks):
			print self.listofBlocks[0].blkid
			print self.listofBlocks[0]
			self.listofBlocks = self.listofBlocks[1:]
