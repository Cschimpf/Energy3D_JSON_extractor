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

	#NOTE THE TEMPORARY ADDITION OF REMOVE_LIST = [] THIS WAS DONE FOR REMOVING CAMERA ACTIONS FOR ANALYSIS OF MARKOV CHAINS
	def jsonSC4NNR(self, remove_list = [], extract = False): #should there be a mode here for extracting full entries and appending date, time and file name?
		anav, aorchard = actNAV(), actORCHARD()
		for entry in self.pullLOG():
			actkey, actval = self.findACTKEY(entry, remove_list)
			if extract == False and actkey != "":
				aorchard.planTREE(anav.actSC4NNR(actkey, actval)) #make a temp change here
				#aorchard.planTYPE(anav.actSC4NNR(actkey, actval), fkey, fval)
			elif actkey != "":
				temp_orch = anav.actSC4NNR(actkey, actval)
				aorchard.planTREE(self.setMetaData(entry, temp_orch), extract)
			
		return aorchard

	def findACTKEY(self, act_entry, remove_list = []):
		'''
		Note the temporary inclusion of remove_list
		to forward filter out actions
		'''
		if self.checkFORKEY(act_entry, remove_list):
			for key, val in act_entry.items():
				if key not in jsonNAV.rpt_keys: #and key not in remove_list:
					return key, val 
		else:
			return "", {}

	def checkFORKEY(self, act_entry, remove_list = []):
		for key, val in act_entry.items():
			if key not in jsonNAV.rpt_keys and key not in remove_list:
				return True
		return False 

	def pullLOG(self):
		try:
			for key, val in self.jsonfile.items():
				return val #returns dictionary associated with the "Activity" category in JSON

		except:
			raise NoJSONFile("There is no JSON file set on the JSON Navigator") #you may want to update this to useful text for a user in the future, like a warning to set the jsonfile first

	def setMetaData(self, act_entry, tree_obj):
		'''
		This attaches a datetime and filename from
		timestap and file to each tree. It is in
		use for the current version of the 
		extractor. May need to be generalized or allowed to fail 
		for some earlier versions of E3D. Not sure file is always consistent name
		'''
		tree_obj.datetime = act_entry['Timestamp']
		tree_obj.ng3file = act_entry['File']
		return tree_obj

	def	jsonEXTR4CTR(self):
		print('extract manager')

class NoJSONFile(Exception):
	pass


		
		
	