import time
import hashlib

class Block:
	size = 10 # limit on number of transactions
	def __init__(self, listofTransactions, miner):
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
		for b in self.listofBlocks:
			if newBlock.blkid == b.blkid:
				print "adding a block already present"
				return

		lastblkid = self.listofBlocks[len(self.listofBlocks)-1].blkid
		newBlock.parentlink = lastblkid
		self.listofBlocks.append(newBlock)
		return 

	def getLast(self):
		return self.listofBlocks[len(self.listofBlocks)-1]

	def removeLast(self):
		self.listofBlocks = self.listofBlocks[:len(self.listofBlocks)-1]
		return 

	def displayChain(self):
		l=0
		while  l < len(self.listofBlocks):
			print "parent: " + str(self.listofBlocks[l].parentlink) + " <------ block :"+	str(self.listofBlocks[l].blkid)
			l+=1
		return 