from ActORCHARD import actORCHARD, actTREE
from StudentFiles import studentFILES
from datetime import datetime 
from csvWRTR import csvFILE
import json 

class treePROC:
	def __init__(self):
		self.write_record = []
		self.data_vers = {} #this will act as a storing house for data versions of the record list, with the name of the transformation as key and data as val

	def printRECS(self, recordlist):
		for student, recordfiles in recordlist.items():
			for record, entries in recordfiles.items():
				csv_f = csvFILE() 
				csv_f.fulldir = "C:/Users/Corey Schimpf/Documents/Next Step Learning/AHS2016/A_filt_time" + "/" + student + "/" + record[:-5] +'.csv' #you will need to later set something to get rid of the .json
				print(student, record, len(entries[0].actTREES))
				for tree in entries[0].actTREES:
					self.write_record = []
					self.procREC([], [tree])
					csv_f.csvWRTR(self.write_record)
					

		



		#processing a single record AKA a single tree, here will use entry for a record
		#first it calls the retrieve branches method on the act tree and gets the 
		#special branches and the node branches
		#then it somehow distinguishes between the time and name special branches
		#and appends them to the print_record list. 
		#then it loops through the entries in store_branch
		#and for each actTREE is opens itself again? or at least calls retrievebranches
		#
	#2016-06-17 11:25:32
		pass
	def procREC(self, info_branch, store_branch):
		'''
		First call should put tree in store_branch
		'''
		#temporarily add a condition that processes blanks from the entries[0].actTREES to put in a blank line in the csv? maybe just return immediately if the "tree" is of a fixed type?
		if len(info_branch) > 1:
			info_branch = self.sortINFO(info_branch)
		for entry in info_branch:
			self.write_record.append(entry)
		for entry in store_branch:
			newinfo, newstore = entry.retrieveBranches()
			self.procREC(newinfo, newstore)

	def sortINFO(self, info_branch):
		for info in info_branch:
			if self.detectDateTime(info):
				return info_branch
			else:
				return [info_branch[1], info_branch[0]]
	def detectDateTime(self, string):
		try:
			return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
		except:
			return False 

	def detectTimeLag(self, t1, t2, lag = 3600):
		'''
		for now assume that t2 is the later time
		'''
		d1, d2 = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S'), datetime.strptime(t2, '%Y-%m-%d %H:%M:%S') #uses the formatting inherit to E3D
		delta = d2 - d1 
		if delta.seconds <= lag:
			return True
		else:
			return False 

class dataVER(object):
	'''
	this will store alternative processed versions
	of the recordslist, which will be checked
	if it exists for printing when printing is 
	called through this module or will it
	be checked outside of the module?
	'''
	def __init__(self, t_type):
		self.trans_type = ''
		self.mod_records = studentFILES()

	@property
	def mod_records(self):
		return self._mod_records
	@mod_records.setter
	def mod_records(self, mod_rec): #in the future I will add controls to this hence its a decorator 
		self._mod_records = mod_rec

class filter:
	'''
	an abstract class from which other 
	filters will inherit
	'''
	def __init__(self, types, recordlist):
		self.types = types
		self.unmod_records = recordlist 

class activityFilter(filter):
	def __init__(self, types, recordlist, activities = []):
		super().__init__(types, recordlist)
		self.activities = activities
		self.liveVER = dataVER(types) 
		self.filter_queue = []
		self.lametrick = False #dummy line
		self.count_queue = [] #dummy line


	def applyFilter(self, noise_tol = 1, camera = False):
		self.setActFilter('Solar') #this is just a forced selection for now
		self.activities.append('blank') #dummy line
		for student, recordfiles in self.unmod_records.recordlist.items():
			self.liveVER.mod_records.addStudent(student)
			for record, entries in recordfiles.items():
				a_orch = actORCHARD()
				for tree in entries[0].actTREES:
					if self.Filtering(tree.cargo, noise_tol, camera) and self.lametrick: #dummyline 
						blank = actTREE("addblankline") #dummy line
						a_orch.planTREE(blank, True) #dummy line
						a_orch.planTREE(tree, True) #dummy line
					elif self.Filtering(tree.cargo, noise_tol, camera):
						a_orch.planTREE(tree, True) #will need to think of another term for planTREE parameter 'extract'
							
				if a_orch.actTREES and self.meetMin(a_orch.actTREES):
					self.liveVER.mod_records.addRecord(student, record, a_orch)
				self.clearQueue()


		#each file will be processed and IF there is at least one record matching the criteria in activities it will be added to the modded recordlist in liveVER
		#will need a constructor method that adds records to liveVER
	#a method for setting the activities. maybe in the future this can be a decorator? or should it be a method?
	def setActFilter(self, option ='', user_spec = []):
		if user_spec:
			print('Not Implemented')
			pass #do something with the list specified by the user
		elif option: #for handling this later when user_spec is implemented, you can just specify the parameter user_spec = [some_items]
			with open("C:/Users/Corey Schimpf/Documents/Python/ActivityStyles.json", 'r') as j:
				j_obj = json.load(j)
				builtin = j_obj["Built-in Styles"]
				self.activities = builtin[option]
                	

	#method for evaulating then adding or clearing the filter_queue
	def Filtering(self, act, noise_tol, camera = False):
		self.lametrick = False #dummy line

		if act in self.activities:
			if len(self.filter_queue) > noise_tol: #dummy line
				self.lametrick = True #dummy line
			self.clearQueue()
			return True 
		elif camera and act == 'Camera':
			return True 
		elif len(self.filter_queue) < noise_tol:
			self.filter_queue.append(act)
			return True
		else:
			self.filter_queue.append(act)
			
			self.count_queue.append(len(self.filter_queue))
			return False 
	def clearQueue(self):
		self.filter_queue = []

	#this says there must be at least 1 record to save the processed record, this may be something users want to control
	def meetMin(self, entries, min = 1):
		threshold = 0
		for tree in entries:
			if tree.cargo in self.activities:
				threshold +=1 
			if threshold >= min:
				return True 
		else:
			return False 










