class studentFILES(object):
	def __init__(self):
		self.recordlist = {}

	def addStudent(self, s_id):
		if not self.checkID(s_id, self.recordlist):
			self.recordlist[s_id] = {}
		else:
			print("Warning {} Student Record Already Exists".format(s_id))

	def addRecord(self, s_id, fname, entries):
		if not self.checkRecord(s_id, fname):
			self.recordlist[s_id][fname] = [entries]
		else:
			self.recordlist[s_id][fname].append(entries) #will add more entries if has same fname, but this not really ever the case?
		
		#will need a check if student already in dictionary to prevent overwriting
		#may want some check to see if file record for a student contains anything
		#or not, otherwise you might give some warning and pass it 
		#where will the subdictionaries and dictionary entry with student + records 
		#be made? Here or in jsonNAV? Seems to make more sense the methods are here
		#will there need to be a separate method for making sub records and
		#a full students record?
		pass


	def checkID(self, n_id, records):  #could change this to check Item and have it check both for students and for records
		for name, record in records.items():
			if name == n_id:
				return True	
		return False 		 
	def checkRecord(self, s_id, fname):
		if self.checkID(s_id, self.recordlist): #check if student exists
			return self.checkID(fname, self.recordlist[s_id]) #seems to check if record(fname) exists
		else:
			raise KeyError("No Student Record Exists for {}".format(s_id))
				 


			




