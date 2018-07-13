class actORCHARD:
	def __init__(self):
		self.actTREES = []
		#self.actTYPES = {}

	def findTREE(self, tree_obj):
		'''
		this will be a check so we don't scan activities that already exist in the ORCHARD
		'''
		for trees in self.actTREES:
			if trees.cargo == tree_obj.cargo:
				return True
		return False 

	def planTREE(self, tree_obj, extract = False):
		'''
		will need to think harder how actTREE will have access to actORCHARD's attribute, should this be some other way??)
		'''
		if extract == False and not self.findTREE(tree_obj):
			self.actTREES.append(tree_obj) #for scan mode, only unique types are added 
		else:
			self.actTREES.append(tree_obj) #when extract is True, all cases are added


	def planTYPE(self, tree_obj, fkey, fval):
		ptype = ["Resize Building", "Move Building"]
			
		if tree_obj.cargo in ptype:

			self.actTYPES[tree_obj] = fval + " " + fkey


class actTREE:
	def __init__(self, cargo, branch1=None, branch2=None, branch3=None, branch4=None, branch5=None, branch6=None, branch7=None, branch8=None, branch9=None, datetime=None, ng3file=None):
		self.cargo = cargo
		self.branch1  = branch1
		self.branch2  = branch2
		self.branch3  = branch3
		self.branch4  = branch4
		self.branch5  = branch5
		self.branch6  = branch6
		self.branch7  = branch7
		self.branch8  = branch8
		self.branch9  = branch9
		self.datetime = datetime #at least for now this will circumvent having to make a new datatype just for extraction 
		self.ng3file = ng3file #for now this allows us to capture the ng3 file being operated on too
        

	def __str__(self):
		return str("This is a {} tree".format(self.cargo))


	def topofTREE(self):
		for attr, value in self:
			if isinstance(value, actTREE):
				return False
		return True 

	def retrieveBranches(self):
		s_branch = ["datetime", "cargo"]
		info_branch, store_branch = [], []
		for attr, value in self.__dict__.items():
			if attr in s_branch and value != None:
				info_branch.append(value)
			elif value != None:
				store_branch.append(value)
		return info_branch, store_branch





	def delENTRY(self, key):
		'''
		Should this delENTRY be generalized to delete for all the lists above? 
		'''
		del self.active_level[len(self.active_level)-1][key]
		if self.active_level[len(self.active_level) - 1] == {}:
			del self.active_level[len(self.active_level)-1]
			
		
	


