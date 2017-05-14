'''
a class that navigates an unknown (and unique set of) activities  of the Energy3D JSON data structure
'''
from ActORCHARD import actORCHARD, actTREE

class actNAV:

	def __init__(self, mode = 'mapping'):
		
		self.typedict = {
			dict : dictNAV(),
			list : listNAV(),
			str : strNAV(),
			int : discreteNAV(),
			float : discreteNAV(),
			bool : discreteNAV()
		}
		
		#these are no longer necessary I think? 
		self.mode = mode  #map/extract
		
	def actSC4NNR(self, actkey, actval): 
		'''
		This creates a root tree based off the actkey sent, then loops through the dictionary
		in actval, creating subtrees and then calling the addBR4NCH method to add them 
		to the root tree. The root is returned to whatever calls the scanner. 
		'''

		root = actTREE(actkey)
		if type(actval) != dict:
			branch = actTREE(actval)
			self.addBR4NCH(root, branch)
		else:
			for subkey, subval in actval.items():
				branch = self.typedict[self.actTYPR(subval)].procTYPE(subkey, subval)
				self.addBR4NCH(root, branch)
		#for attr, value in root.__dict__.items():
			#print(attr, value)
		return root 
			
	def actTYPR(self, valtype):
		#actSC4NNR calls this within the loops to get the type of a given val from key/val pair and call
		#the appropriate submethod
		return type(valtype)

	def addBR4NCH(self, rootobj, branchobj):
		'''
		This looks for an empty spot in the tree being added to
		and then assigns a branch_obj to it. Because it
		is searching through a dictionary, it may not add to branches in order
		'''
		branch_pos = []
		for attr, value in rootobj.__dict__.items():
			if value == None and attr != 'datetime':
				branch_pos.append(attr)
				break
		for attr in branch_pos:
			rootobj.__dict__[attr] = branchobj


	def procTYPE(self, subkey, subval):
		raise NotImplementedError("Subclass must implement abstract method")
		
class dictNAV(actNAV):
	'''Subclass of actNAV'''
	def __init__(self):
		pass
		
	def procTYPE(self, subkey, subval):
		tempact = actNAV()
		branch = tempact.actSC4NNR(subkey, subval)
		return branch 

class listNAV(actNAV):
	def __init__(self):
		pass 

	def procTYPE(self, subkey, subval):
		'''
		
		'''
		if type(subval[0]) == dict:
			branch = dictNAV().procTYPE(subkey, subval[0])
			return branch 
		else:
			tempact = actNAV()
			branch = tempact.typedict[self.actTYPR(subval[0])].procTYPE(subkey, subval)
			return branch 

class strNAV(actNAV):
	def __init__(self):
		pass
		
	def procTYPE(self, subkey, subval):
		return actTREE(subkey, actTREE(subval))

class discreteNAV(actNAV):
	def __init__(self):
		pass
		
	def procTYPE(self, subkey, subval):
		return actTREE(subkey, actTREE(subval))
		
