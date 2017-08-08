from jsonHNDLR import jsonHNDLR
from jsonNAV import jsonNAV, NoJSONFile
from ActORCHARD import actORCHARD, actTREE
from StudentFiles import studentFILES
from TreeProc import treePROC, dataVER, activityFilter
from actNAV import * 
from Filter import filter
from Data_Formatter import * #this name likely needs to change maybe to data exporter 
from copy import deepcopy
import time 

class extract_transform_model(object):
	def __init__(self):
		self.filter_ref = filter(self)
		self.filtered_model = extract_transform_instance(self)
		self.machine_state = state_machine()


	def update_model_instance(self, filters = {}):
		self.model_instance = deepcopy(self)

		#for filter_items in 


	@property 
	def user_filelist(self):
		return self._user_filelist

	@user_filelist.setter
	def user_filelist(self, flist):
		if isinstance(flist, list) and isinstance(flist[0], list):
			self._user_filelist = flist
		else:
			#raise error?
			pass
	def user_filelist_sublist_check(self, flist):
		try: #think about the best way to check and stop if not isinstance(flist[i], list)
			for entry in flist:
				pass
		except:
			pass

	@property 
	def types_available(self):
		return self._types_available

	@types_available.setter
	def types_available(self, typeslist):
		if isinstance(typeslist, list):
			self._types_available = typeslist
		else:
			#raise error?
			pass

	@property
	def student_records(self):
		return self._student_records

	@student_records.setter
	def student_records(self, srecords):
		if isinstance(srecords, studentFILES):
			self._student_records = srecords
		else:
			#raise error
			pass

	@property
	def json_handler(self):
		return self._json_handler

	@json_handler.setter
	def json_handler(self, hndlr_obj):
		if isinstance(hndlr_obj, jsonHNDLR):
			self._json_handler = hndlr_obj
		else:
			#raise error
			pass
	def scan_for_types(self):
		types_available = []
		for jsonpaths in self.user_filelist:
			orchard = actORCHARD()
			jnav, jnav.jsonfile = jsonNAV(), self.json_handler.openJSON(jsonpaths[0], jsonpaths[1]) #for now I am not looping through anything, just checking integration of all the modules  
			if jnav.jsonfile:
				orchard = jnav.jsonSC4NNR()
				for entry in orchard.actTREES:
					if entry.cargo not in types_available: 
						types_available.append(entry.cargo)
		self.types_available = types_available 
		self.filter_ref.filters_reset() #running a scan will reset the filters back to nothing 

	def extract_types(self):
		'''
		This seems to run without
		any reference to types available,
		should it work this way?
		'''
		student_files = studentFILES()
		for jsonpaths in self.user_filelist:
			student_files.addStudent(jsonpaths[1])
			jnav, jnav.jsonfile = jsonNAV(), self.json_handler.openJSON(jsonpaths[0], jsonpaths[1])
			if jnav.jsonfile:
				orchard = jnav.jsonSC4NNR(True)
			else:
				orchard = None
			student_files.addRecord(jsonpaths[1], jsonpaths[0], orchard)

		self.student_records = student_files
		print(len(self.student_records.recordlist))
		filespresent = []
		for key, val in self.student_records.recordlist.items():
			missing = 0
			for x, y in val.items():
				if y == [None]:
					missing +=1
			filespresent.append([key, missing])
		for entry in filespresent:
			print(entry)
		print(list(self.student_records.recordlist.keys()))
		self.filtered_model.instance_scheduler()
        
		#need to add something here in case
		#type_filter has been set so its post processed and inserted into the model instance below

	def export_data(self, writedir):
		'''
		At some point this will need to be generalized
		for all sorts of exporting but for now
		it only links to the rawcount exporter
		'''
		#in the future this should call some general function for handling different
		#kinds of exports 
		data_formatter = data_formatter_rawcount(self.student_records, self.types_available)
		data_formatter.writedir = writedir 
		data_formatter.export_dataframe()

	def export_action_density(self, writedir):
		'''
		Unsustainable to make separate methods for all of these
		just a temporary solution. This will export action
		density for csv through the data_formatter. This is
		more like variable creation?? Should it be 
		stored or handled separately from export data?
		'''
		data_formatter = data_formatter_action_density(self.student_records, self.types_available)
		data_formatter.writedir = writedir
		data_formatter.export_dataframe()

class extract_transform_instance(extract_transform_model):
	'''a sublcass of the extract_transform_model
	   which stores a filtered version of the full model.
	   NOTE: Do not assign a filter to the subclass as 
	   the filter decorator creates a new subclass'''

	#subclass_filter_dict = {'Student Names': '_student_records', 'System Files': '_user_filelist', 'Action Types': '_types_available'}
	def __init__(self, parent):
		#instance_scheduler(filters, parent_obj)
		self.parent = parent

	def instance_scheduler(self):
		model_attrs, filter_attrs = self.identify_attrs()
		print("ready to schedule....")
		print(model_attrs)
		print(filter_attrs)
		if len(model_attrs) == 0 or len(filter_attrs) == 0:
			return 
		elif "_student_records" in model_attrs and len(filter_attrs) ==2:
			print("student records and both filters")
			if not self.parent.machine_state.compare_applied_new_type(self.parent.filter_ref.type_filter):
				self._student_records = self.parent.filter_ref.filter_student_file_types()
				self.parent.machine_state.applied_type_filter = self.parent.filter_ref.type_filter
				self.CHECK_TYPE_FILTER()
			if not self.parent.machine_state.compare_applied_new_sfile(self.parent.filter_ref.student_file_filter): 
				self._student_records = self.parent.filter_ref.filter_student_files()
				self.parent.machine_state.applied_sfile_filter = self.parent.filter_ref.student_file_filter
				self.CHECK_FILE_FILTER()

		elif "_student_records" in model_attrs and "_type_filter" in filter_attrs:
			print("student records and type filter")
			if not self.parent.machine_state.compare_applied_new_type(self.parent.filter_ref.type_filter):
				self._student_records = self.parent.filter_ref.filter_student_file_types()
				self.parent.machine_state.applied_type_filter = self.parent.filter_ref.type_filter
				self.CHECK_TYPE_FILTER()

		elif "_student_records" in model_attrs and "_student_file_filter" in filter_attrs:
			print("student_records and student file filter")
			if not self.parent.machine_state.compare_applied_new_sfile(self.parent.filter_ref.student_file_filter): 
				self._student_records = self.parent.filter_ref.filter_student_files()
				self.parent.machine_state.applied_sfile_filter = self.parent.filter_ref.student_file_filter
				self.CHECK_FILE_FILTER()
			


	def CHECK_FILE_FILTER(self):
		for key, val in self.parent._student_records.recordlist.items():
			print(key)
			for subkey, subval in val.items():
				print(subkey)
		print('\n', '\n', '\n', '\n', '\n', '\n')
		for key, val in self._student_records.recordlist.items():
			print(key)
			for subkey, subval in val.items():
				print(subkey)

	def CHECK_TYPE_FILTER(self):
		for key, val in self.parent._student_records.recordlist.items():
			for subkey, subval in val.items():
				if subval[0] != None:
					print(key, subkey, len(subval[0].actTREES))
		print('\n', '\n', '\n', '\n', '\n', '\n')
		for key, val in self._student_records.recordlist.items():
			for subkey, subval in val.items():
				if subval[0] != None:
					print(key, subkey, len(subval[0].actTREES))

	def identify_attrs(self):
		model_attrs = []
		filter_attrs = []
		zero_state = []
		for attr, value in self.parent.__dict__.items():
			if attr == "_student_records":
				model_attrs.append(attr)
				break 
		for attr, value in self.parent.filter_ref.__dict__.items():
			if attr[0]== "_" and len(value) != 0 or attr[0] == "_" and self.parent.machine_state.check_if_filtered():
				filter_attrs.append(attr)
		return model_attrs, filter_attrs

class state_machine:
	def __init__(self):
		self.applied_type_filter = []
		self.applied_sfile_filter = {}

	def check_if_filtered(self, sfile = False, typef = False):
		if sfile:
			return len(self.applied_sfile_filter) 
		if typef:
			return len(self.applied_type_filter)

	def compare_applied_new_type(self, new_type):
		if len(self.applied_type_filter) != len(new_type):
			return False #they are not the same, can't be with different size
		for entry in new_type:
			if entry not in self.applied_type_filter:
				return False 
		return True 

	def compare_applied_new_sfile(self, sfile):
		if len(self.applied_sfile_filter.keys()) != len(sfile.keys()):
			return False
		for key, val in sfile.items():
			if len(val) != len(self.applied_sfile_filter[key]):
				return False 
		for key, val in sfile.items():
			if key not in self.applied_sfile_filter.keys():
				return False
			for entry in val:
				if entry not in self.applied_sfile_filter[key]:
					return False
		return True 







class NoFile(Exception):
	pass

class WrongType(Exception):
	pass
#*****************************DISCARDED CODE******************************************
	# @property
	# def filtermap(self):
	# 	return self._filtermap

	# @filtermap.setter
	# def filtermap(self, filters = {}):
	# 	try:
	# 		if isinstance(filters, dict) and self.filtermap:
	# 			print("map here!")
	# 			self._filtermap = filters
	# 			#self.update_model_instance(filters)
	# 	except:
	# 		if isinstance(filters, list):
	# 			self._filtermap = filters

	# for items in present_attrs:
		# 	self.eval(items[1]) = eval('parent_obj'+eval(items[1]))

	#def count_filters(self, filters):
	# 	total = 0
	# 	for key, val in filters.items():
	# 		total = total + len(val)
	# 	return total 