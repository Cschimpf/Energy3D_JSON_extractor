#from Extract_Transform_Model import extract_transform_model as extr_model
from ActORCHARD import actORCHARD, actTREE
from copy import deepcopy

class filter(object):
	def __init__(self, m_ref):
		self.model_ref = m_ref
		#self.filtered_model = extract_transform_model()



	@property
	def student_file_filter(self):
		return self._student_file_filter

	@student_file_filter.setter
	def student_file_filter(self, students):
		if isinstance(students, dict):
			self._student_file_filter = students
		else:
			#raise error
			pass


	@property
	def type_filter(self):
		return self._type_filter

	@type_filter.setter
	def type_filter(self, types):
		if isinstance(types, list):
			self._type_filter = types
		else:
			#raise error
			pass
			
	def filters_reset(self, type=True, s_file = True):
		if type == True:
			self._type_filter = []
		if s_file == True:
			self._student_file_filter = {}

	def filter_student_files(self, use_filtered = False):
		'''
		This filters out students or student files.
		This could proceed by deleting entries.
		Or by rebuilding a studentFILES() object 
		with the unfiltered entries. Right now
		for small numbers it simply deletes.
		'''
		if use_fitered == False:
			new_student_records = deepcopy(self.model_ref.student_records) 
		else:
			new_student_records = deepcopy(self.model_ref.filtered_model.student_records)
		#new_student_records = studentFILES() #holdover for when rebuilding functionality is added
		for key, val in self.model_ref.student_records.recordlist.items():
			if key in self.student_file_filter.keys() and len(val.keys()) == len(self.student_file_filter[key]):
				del new_student_records.recordlist[key] #need to delete from this but run through full model to avoid dict size changing mid op, will give python error
				continue
			elif key not in self.student_file_filter.keys():
				continue 
			else:
				for subkey, subval in val.items():
					if subkey in self.student_file_filter[key]:
						del new_student_records.recordlist[key][subkey]
		return new_student_records

	def filter_student_file_types(self, use_filtered = False):
		if use_filtered == False:
			new_student_records = deepcopy(self.model_ref.student_records)
		else:
			new_student_records = deepcopy(self.model_ref.filtered_model.student_records)
		for key, val in new_student_records.recordlist.items():
			for subkey, subval in val.items():
				newtreelist = []
				if subval[0] != None:
					for tree in subval[0].actTREES:
						if tree.cargo not in self.type_filter:
							newtreelist.append(tree)
					temp_orchard = actORCHARD()
					temp_orchard.actTREES = newtreelist
					new_student_records.recordlist[key][subkey] = [temp_orchard]
		return new_student_records



#*****************************DISCARDED CODE******************************************
	# @property
	# def file_filter(self):
	# 	return self._file_filter

	# @file_filter.setter
	# def file_filter(self, files):
	# 	if isinstance(files, list):
	# 		self._file_filter = files
	# 	else:
	# 		#raise error
	# 		pass