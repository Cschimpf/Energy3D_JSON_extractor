'''
a class that navigates an unknown json data structure and will call actNAV for processing activities
'''
import json 
from actNAV import *
from ActORCHARD import actORCHARD, actTREE
#will you need to import ActORCHARD if some class types will end up here from actNAV?

class jsonNAV(object):
	'''
	need to figure out if this module will open the JSON or a separate fileHNDLR will, and pass it here
	I am leaning toward a separate fileHNDLR, especially for the future when this may be attached to a web
	front end, you may want these things separate

	Some questions. How should it process through the json before it reaches the activities?
	'''
	rpt_keys = ["Timestamp", "Project", "File"]
	
		

	@property
	def jsonfile(self):
		return self._jsonfile
	@jsonfile.setter
	def jsonfile(self, jsonfile):
		try:
			if jsonfile == None: #in case there is a time where you want nothing here, in transition. Note will throw an error if object.jsonfile is called
				print("Warning, no current JSON file in the JSON navigator")
				self._jsonfile = jsonfile 
			elif type(jsonfile) != dict:
				raise TypeError("JSON navigator JSON files should be python dictionaries")
			elif type(jsonfile['Activities']) == list:
				self._jsonfile = jsonfile 
		except:
			raise ValueError("Assigned JSON file does not appear to be in E3D format")


	def jsonSC4NNR(self, extract = False): #should there be a mode here for extracting full entries and appending date, time and file name?
		anav, aorchard = actNAV(), actORCHARD()
		for entry in self.pullLOG():
			actkey, actval = self.findACTKEY(entry)
			if extract == False and actkey != "":
				aorchard.planTREE(anav.actSC4NNR(actkey, actval)) #make a temp change here
				#aorchard.planTYPE(anav.actSC4NNR(actkey, actval), fkey, fval)
			elif actkey != "":
				temp_orch = anav.actSC4NNR(actkey, actval)
				aorchard.planTREE(self.setDATETIME(entry, temp_orch), extract)
			
		return aorchard

	def findACTKEY(self, act_entry):
		'''
		I believe one activity entry is being sent here and
		then the 
		'''
		if self.checkFORKEY(act_entry):
			for key, val in act_entry.items():
				if key not in jsonNAV.rpt_keys:
					return key, val 
		else:
			return "", {}

	def checkFORKEY(self, act_entry):
		for key, val in act_entry.items():
			if key not in jsonNAV.rpt_keys:
				return True
		return False 

	def pullLOG(self):
		try:
			for key, val in self.jsonfile.items():
				return val #returns dictionary associated with the "Activity" category in JSON

		except:
			raise NoJSONFile("There is no JSON file set on the JSON Navigator") #you may want to update this to useful text for a user in the future, like a warning to set the jsonfile first

	def setDATETIME(self, act_entry, tree_obj):
		'''
		This attaches a datetime from
		timestap to each tree. It is in
		use for the current version of the 
		extractor
		'''
		tree_obj.datetime = act_entry['Timestamp']
		return tree_obj

	def	jsonEXTR4CTR(self):
		print('extract manager')

class NoJSONFile(Exception):
	pass


		
		
	