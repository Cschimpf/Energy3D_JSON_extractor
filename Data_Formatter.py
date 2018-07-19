from StudentFiles import studentFILES
from csvWRTR import csvFILE
from ActORCHARD import actTREE
import pandas as pd
import datetime, json
from copy import deepcopy

class data_formatter(object):
	'''
	std_files are an extracted studentFiles class
	and types_avail is the available types
	from the data (full). Right now there is
	no filtering being passed to this so that
	will have to be addressed and may need an 
	extra variable for studentFiles and the
	current list of selected students
	'''
	def __init__(self, std_files, types_avail, filtered = False):
		self.std_files = std_files
		self.students_avail = None 
		self.types_avail = types_avail
		if filtered: #pull this out later as a decorator 
			self.types_filter = self.openUserFilterJSON(filtered) #this comes from user upload
			self.filter_labels() #this also seems to create a types_avail_filter
		else:
			self.types_filter = None
		#self.types_avail_filtered = None #this is set by self.filter_labels above
		self.dataframe = None 
		self.dataframe_filtered = None

		
		
	@property #what will be sent here is a dir + student no (e.g. a25) + jsonfname (now with csv extension)
	def writedir(self):
		return self._writedir 

	@writedir.setter #may want to extend this decorator so it accepts different kind of file types for subclasses
	def writedir(self, dirname): 
		'''
		checks if there is a .csv
		extension, adds if not
		'''
		if dirname.find('.csv') == -1:
			self._writedir = dirname + '.csv'
		else:
			self._writedir = dirname

	def sort_datalist(self, datalist):
		return sorted(datalist)

	def set_dataframes(self, data_index, col_list, datatype = 'int'):
		self.dataframe = self.create_dataframe(data_index, col_list, datatype)
		self.dataframe_filtered = deepcopy(self.dataframe) #you may be able to remove this???

	def create_dataframe(self, data_index, col_list, datatype = 'int'):
		return pd.DataFrame(index = data_index, columns = col_list, dtype=datatype)

	def reset_filtered_dataframe(self):
		if self.dataframe == None:
			raise DataFrameNotSet("Dataframe not set, cannot operate on dataframe")
		self.dataframe_filtered = self.dataframe[:]

	def collapse_dataframe_cols(self):
		#if self.dataframe or self.dataframe_filtered == None:
			#raise DataFrameNotSet("Dataframe not set, cannot operate on dataframe")
		for key, val in self.types_filter.items():
			merged_values = []
			while len(self.dataframe.index) != len(merged_values):
				merged_values.append(0)
			for action_type in val:
				temp_col = list(self.dataframe[action_type]) #converted to list for ease of addition

				for i in range(0, len(self.dataframe.index)):
					merged_values[i] = merged_values[i] + temp_col[i]
				#deleting the column of out the copy dataframe
				del self.dataframe[action_type]
			self.dataframe[key] = merged_values 


	def collapse_dataframe_rows(self):
		#if self.dataframe or self.dataframe_filtered == None:
			#raise DataFrameNotSet("Dataframe not set, cannot operate on dataframe")
		for key, val in self.types_filter.items():
			merged_values = []
			while len(self.types_avail_filtered) != len(merged_values):
				merged_values.append(0)
			for action_type in val:
				temp_col = list(self.dataframe.loc[action_type]) #converted to list for ease of addition
				for i in range(0, len(self.types_avail_filtered)):
					merged_values[i] = merged_values[i] + temp_col[i]
				#deleting the column of out the copy dataframe
				self.dataframe= self.dataframe.drop(action_type)
			#temp_df =  pd.DataFrame(merged_values, index = [key], columns = self.types_avail_filtered)
			
			self.dataframe.loc[key] = merged_values

	def filter_labels(self):
		filtered_labels =[]
		for key, val in self.types_filter.items():
			filtered_labels.append(key)

		for action_type in self.types_avail:
			if self.check_if_filtered(action_type) == False:
				filtered_labels.append(action_type)
		self.types_avail_filtered = sorted(filtered_labels)

	def check_if_filtered(self, action):
		for key, val in self.types_filter.items():
			if action in val:
				return True 
		return False 

	def create_data_vector(self, keylist):
		data_vector = {}
		for entry in keylist:
			data_vector[entry] = 0
		return data_vector

	def incr_data_vector(self, data_vector, key):
		data_vector[key] +=1


	def insert_df_value(self, xrow, ycol, val):
		#if self.dataframe == None:
			#return #the only time this should be a problem is if my code is wrong, should there be an error here?
		self.dataframe.set_value(xrow, ycol, val)
		

	def retrieve_col_list(self):
		return list(self.std_files.recordlist.keys())

	def openUserFilterJSON(self, filtered):
		'''This is a temporary solution to importing
		the filter, but I think it can be used to open what the 
		user sends in'''
		jsonfile = json.load(open(filtered))
		return jsonfile 





class data_formatter_rawcount(data_formatter):
	def __init__(self, std_files, types_avail, filtered = False):
		super().__init__(std_files, types_avail, filtered)

	def export_dataframe(self):
		self.populate_dataframe()
		self.print_dataframe()

	def populate_dataframe(self):
		'''
		this should be polymorphic
		but may implement that later
		all of the data_formatter 
		classes should have a populate
		method
		'''
		self.students_avail, self.types_avail = self.sort_datalist(self.retrieve_col_list()), self.sort_datalist(self.types_avail) #you could make these decorators and heve them self sort upon being set
		self.set_dataframes(self.students_avail, self.types_avail) #you might want to shift it so Student column is added here or would that be obnoxious? Hmm
		for key, val in self.std_files.recordlist.items():
			dvector = self.create_data_vector(self.types_avail)
			for subkey, subval in val.items():
				if subval[0] != None:
					for tree in subval[0].actTREES:
						self.incr_data_vector(dvector, tree.cargo)
			for action, count in dvector.items():
				self.insert_df_value(key, action, count)
		if self.types_filter:
			self.collapse_dataframe_cols()
			self.dataframe = self.dataframe.reindex_axis(sorted(self.dataframe.columns), axis=1)
			self.dataframe.sort_index(inplace = True)


	def print_dataframe(self):
		csvfile = csvFILE()
		csvfile.fulldir = self.writedir 
		if not self.types_filter:
			labelrow = self.types_avail
		else:
			labelrow = self.types_avail_filtered
		labelrow.insert(0, 'Student')
		csvfile.csvWRTR(labelrow)
		for xrow in self.students_avail:
			dvector_row = list(self.dataframe.loc[xrow])
			dvector_row.insert(0, xrow)
			csvfile.csvWRTR(dvector_row)

class data_formatter_sequence_count(data_formatter):
	def __init__(self, std_files, types_avail, filtered = False, order = 1):
		super().__init__(std_files, types_avail, filtered)
		self.order = order #originally intended to be the order of the markov model
		self.full_dimensions = None

	def export_dataframe(self):
		self.populate_dataframe()
		#self.print_dataframe()

	def populate_dataframe(self):
		self.students_avail, self.types_avail = self.sort_datalist(self.retrieve_col_list()), self.sort_datalist(self.types_avail)
		
		self.full_dimensions = self.create_state_sequence(self.types_avail, self.order)#note this temporarily hardcoded in the model	
		dimensions = self.set_dataframe_order()
		for key, val in self.std_files.recordlist.items():
			dvector = self.create_data_vector(dimensions)
			for subkey, subval in val.items():
				if subval[0] != None:
					tree_history = []
					for tree in subval[0].actTREES:

						if len(tree_history[-self.order:]) == self.order:
							temp_action = self.combine_action_sequence(tree_history[-self.order:], tree.cargo)
							self.incr_data_vector(dvector, temp_action)

						#closing out
						tree_history.append(tree.cargo)

			for action, count in dvector.items():
				pastaction, nextaction = self.separate_action_sequence(action)
				self.insert_df_value(pastaction, nextaction, count)
			if self.types_filter:
				self.collapse_dataframe_cols()
				self.collapse_dataframe_rows()
				#self.dataframe = self.dataframe_filtered[:]
				self.dataframe = self.dataframe.reindex_axis(sorted(self.dataframe.columns), axis=1)
				self.dataframe.sort_index(inplace = True)
			self.print_dataframe(key, dimensions) #key here is student number, need to turn true if you want filter on
			dimensions = self.set_dataframe_order()
			#now you need to call print and write this out

	def print_dataframe(self, student, dimensions):
		csvfile = csvFILE()
		csvfile.fulldir = self.modify_save_path(student)
		if not self.types_filter: 
			labelrow = self.types_avail[:]
		else:
			labelrow = self.types_avail_filtered[:] # the slicing is to avoid messing with the original list
		labelrow.insert(0, 'Last Action')
		csvfile.csvWRTR(labelrow)
		#*****need to have a better way to handle this but for now*****
		if not self.types_filter:
			for xrow in self.types_avail:
				dvector_row = list(self.dataframe.loc[xrow])
				dvector_row.insert(0, xrow) #
				csvfile.csvWRTR(dvector_row)
		else:
			for xrow in self.types_avail_filtered:
				dvector_row = list(self.dataframe.loc[xrow])
				dvector_row.insert(0, xrow) #
				csvfile.csvWRTR(dvector_row)

	def modify_save_path(self, student):
		index = self.writedir.rfind('.')
		return self.writedir[:index] + '_' + student + self.writedir[index:]


	def create_state_sequence(self, input_seq, runs, output_seq = []):
		'''
		The append list is simply the existing self.types_avail list
		this way the argument doesn't have to be passed over and over
		'''
		templist =[]
		for actions in input_seq:
			for item in self.types_avail: 
				temp_actions = actions + "." + item 
				templist.append(temp_actions)
		#closing out block
		output_seq.extend(templist)
		runs -=1 
		if runs == 0:
			return output_seq
		else:
			output_seq = self.create_state_sequence(templist, runs, output_seq)
			return output_seq

	def combine_action_sequence(self, history_list, current_action):
		combined = ''
		for item in history_list:
			if combined == '':
				combined = combined + item +'.'
			else:
				combined = combined + item + '.'

		combined = combined + current_action
		return combined 

	def separate_action_sequence(self, combined_action):
		breakdex = combined_action.rfind('.')
		return combined_action[:breakdex], combined_action[breakdex+1:]

	def set_dataframe_order(self):
		if self.order == 1:
			self.set_dataframes(self.types_avail, self.types_avail)
			dimensions = self.full_dimensions
		else:
			startdex, enddex = self.find_loworder_seq_end(self.full_dimensions)
			self.set_dataframes(self.full_dimensions[startdex:enddex], self.types_avail)
			dimensions = self.full_dimensions[enddex:]
		return dimensions

	def find_loworder_seq_end(self, full_seq):
		'''this should only be called if order > 1
		'''
		startdex = 'undefined'
		for i in range(0, len(full_seq)):
			if full_seq[i].count('.') == self.order:
				return startdex, i 
			if full_seq[i].count('.') == self.order - 1 and startdex == 'undefined':
				startdex = i


class data_formatter_action_basket(data_formatter):
	def __init__(self, std_files, types_avail, filtered = False):
		super().__init__(std_files, types_avail, filtered)
		self.joinstring =", "
		self.datatype = 'object'

	def export_dataframe(self):
		self.populate_dataframe()
		self.print_dataframe()

	def populate_dataframe(self):
		self.students_avail, self.types_avail = self.sort_datalist(self.retrieve_col_list()), self.sort_datalist(self.types_avail) #you could make these decorators and heve them self sort upon being set
		self.set_dataframes(self.students_avail, ['Action Basket'], self.datatype) #the only column is Action Basket
		for key, val in self.std_files.recordlist.items():
			action_basket = []
			for subkey, subval in val.items():
				if subval[0] != None:
					for tree in subval[0].actTREES:
						if tree.cargo not in action_basket:
							action_basket.append(tree.cargo)
			if self.types_filter:
				pass#do something to filter action_basket into new categories, no need to operate on dataframe as there is only one column
			merged_basket = self.mergeBasketItems(self.joinstring, action_basket)
			self.insert_df_value(key, 'Action Basket', merged_basket)
		
	def print_dataframe(self):
		csvfile = csvFILE()
		csvfile.fulldir = self.writedir 
		labelrow = ['Student', 'Action Basket']
		csvfile.csvWRTR(labelrow)
		for xrow in self.students_avail:
			dvector_row = list(self.dataframe.loc[xrow])
			dvector_row.insert(0, xrow)
			csvfile.csvWRTR(dvector_row)


	def mergeBasketItems(self, joinstring, basket):
		return joinstring.join(basket)

class data_formatter_action_stream(data_formatter):
	def __init__(self, std_files, types_avail, filtered = False):
		super().__init__(std_files, types_avail, filtered)
		self.label_rows = ['Energy3D File', 'Day', 'Abs Time', 'Rel Time', 'Action Name', 'Construction', 'Visual Analysis', 'Numeric Analysis', 'Optimization']
		#above is hardcoded for now, may be a submitable list later on
	def export_dataframe(self):
		self.populate_dataframe()
		#self.print_dataframe()

	def populate_dataframe(self):
		'''
		this is a rough cut due to limited time
		'''
		self.students_avail, self.types_avail = self.sort_datalist(self.retrieve_col_list()), self.sort_datalist(self.types_avail) 
		 
		for key, val in self.std_files.recordlist.items():
			start_time = None
			self.set_dataframes([], self.label_rows) 
			for subkey, subval in val.items():
				if subval[0] != None:
					for tree in subval[0].actTREES:
						#need to do many things here
						dvector = []
						dvector.append(tree.ng3file)
						temp_datetime = datetime.datetime.strptime(tree.datetime, "%Y-%m-%d %H:%M:%S")
						if start_time == None: #this needs to come first so first run through start_time will be set
							start_time = temp_datetime
							last_time = temp_datetime
							last_day = temp_datetime.day 
						if temp_datetime.day != last_day:
							start_time = temp_datetime
						last_day = temp_datetime.day
						dvector.append("{}-{}-{}".format(temp_datetime.month, temp_datetime.day, temp_datetime.year))
						dvector.append("{}:{}:{}".format(temp_datetime.hour, temp_datetime.minute, temp_datetime.second))

						current_rel_time = temp_datetime - start_time
						time_gap = temp_datetime - last_time
						if current_rel_time.seconds > 0 and time_gap.seconds < 7200:
							current_rel_time = round(current_rel_time.seconds/60, 2) #to keep this from going crazy round to two digits
						elif time_gap.seconds >= 7200:
							current_rel_time = 0
							start_time = temp_datetime
						else:
							#print('current_rel_time', current_rel_time.seconds)
							current_rel_time = current_rel_time.seconds #needed to add this so I wouldn't have to guess to include seconds below for the append
						last_time = temp_datetime
						dvector.append(current_rel_time)
						dvector.append(tree.cargo)
						category_values = self.identify_action_category(tree.cargo)
						for item in ['Construction', 'Visual Analysis', 'Numeric Analysis', 'Optimization']:#very rough here, hardcoding
							dvector.append(category_values[item])
						if sum(category_values.values()) > 0:
							temp_df = pd.DataFrame([dvector], columns = self.label_rows)
							self.dataframe = self.dataframe.append(temp_df)
						else:
							pass #mostly here just to track that this is apass
			self.print_dataframe(key)#something here
				


	def print_dataframe(self, student):
		csvfile = csvFILE()
		csvfile.fulldir = self.modify_save_path(student)
		labelrow = self.label_rows
		csvfile.csvWRTR(labelrow)
		for index, row in self.dataframe.iterrows():
		
			#dvector_row = list(self.dataframe.loc[xrow])
			#dvector_row.insert(0, xrow)
			csvfile.csvWRTR(list(row))

	def modify_save_path(self, student):
		index = self.writedir.rfind('.')
		return self.writedir[:index] + '_' + student + self.writedir[index:]

	def identify_action_category(self, action):
		categories = {'Construction' : 0, 'Visual Analysis': 0, 'Numeric Analysis' :0, 'Optimization' : 0}
		
		for key, val in self.types_filter.items():
			if action in val:
				categories[key] = 1
				break
		return(categories)



class var_formatter_action_density(data_formatter):
	def __init__(self, std_files, types_avail):
		super().__init__(std_files, types_avail)
		

	def export_dataframe(self):
		self.populate_dataframe()
		self.print_dataframe()

	def populate_dataframe(self):
		self.students_avail = self.sort_datalist(self.retrieve_col_list())
		self.set_dataframes(self.students_avail, ['Action Density'])
		
		ignored_actions = ['DailyEnergyGraph', 'EnergyAnnualAnalysis', 'PvAnnualAnalysis', 'GroupAnnualAnalysis', 'GroupDailyAnalysis', 'PvDailyAnalysis', 'SolarAnnualAnalysis', 'SolarDailyAnalysis']

		for key, val in self.std_files.recordlist.items():
			action_count = 0
			time_count = 0
			action_density = 0
			for subkey, subval in val.items():
				if subval[0] != None and subval[0].actTREES != []:
					#print(subval[0].actTREES)
					prev_time = datetime.datetime.strptime(subval[0].actTREES[0].datetime, "%Y-%m-%d %H:%M:%S")
					for tree in subval[0].actTREES:
						action_count += 1
						time_diff = datetime.datetime.strptime(tree.datetime, "%Y-%m-%d %H:%M:%S") - prev_time
						if time_diff.days == 0 and time_diff.seconds == 0:
							continue 
						elif time_diff.days == 0 and time_diff.seconds < 1800 and tree.cargo not in ignored_actions:# and prev_time.day >= 14:
							time_count = time_count + time_diff.seconds
						prev_time = datetime.datetime.strptime(tree.datetime,  "%Y-%m-%d %H:%M:%S")
						#here will also need to check is this an analysis tasks? if not then how compute time? 
						#should there be some time attributes on the data_formatter object itself to keep things
						#easier?
						#And should there be a check as to when the previous time point and the new one is greater
						#than 30 minutes of inactivity>??
			if action_count > 0 and time_count > 0:
				action_density = (action_count/time_count)*100 #divided by some time measure
				print(action_count/time_count)
			self.insert_df_value(key, 'Action Density', round(action_density, 4))


	def print_dataframe(self):
		csvfile = csvFILE()
		csvfile.fulldir = self.writedir 
		csvfile.csvWRTR(['Student', 'Action Density']) #will need to think about how to abstract this when its just one variable
		for xrow in self.students_avail:               # is this even the right venue for this or should variable creation be elsewhere?
			dvector_row = list(self.dataframe.loc[xrow])
			dvector_row.insert(0, xrow)
			csvfile.csvWRTR(dvector_row)


class var_formatter_attribute_extension(data_formatter):
	def __init__(self, std_files, types_avail, extend_type, extend_depth = 1):
		super().__init__(std_files, types_avail)
		self.extend_type = extend_type
		self.extend_depth = extend_depth
		self.extend_types = []

		self.students_avail, self.types_avail = self.sort_datalist(self.retrieve_col_list()), self.sort_datalist(self.types_avail) #you could make these decorators and heve them self sort upon being set
		self.extend_types_avail()

	def extend_types_avail(self):
		extended_types = []
		for key, val in self.std_files.recordlist.items():
			for subkey, subval in val.items():
				if subval[0] != None:
					
					for tree in subval[0].actTREES:
						if tree.cargo == self.extend_type:
							name_extension = self.identify_subtree_names(tree)
							if len(name_extension) > 1 or len(name_extension) == 0:
								raise ExcessiveSubNames("There are too few or too many subnames to append to Action's name")
							else:
								tempname = tree.cargo + ' ' + name_extension[0]
								if tempname not in extended_types:
									extended_types.append(tempname)
		self.extend_types = extended_types
						

	def identify_subtree_names(self, tree):
		branchname = []
		for attr, value in tree.__dict__.items():
			#print('mytree', attr, value)
			if value != None and attr not in ['datetime', 'cargo'] and isinstance(tree, actTREE):
				branchname.append(value.cargo)
		return branchname

	def export_dataframe(self):
		self.populate_dataframe()
		self.print_dataframe()

	def populate_dataframe(self):
		self.set_dataframes(self.students_avail, self.extend_types)
		for key, val in self.std_files.recordlist.items():
			dvector = self.create_data_vector(self.extend_types)
			for subkey, subval in val.items():
				if subval[0] != None:
					
					for tree in subval[0].actTREES:
						if tree.cargo == self.extend_type:
							name_extension = self.identify_subtree_names(tree)
							tempname = tree.cargo + ' ' + name_extension[0]
							self.incr_data_vector(dvector, tempname)


			for action, count in dvector.items():
				self.insert_df_value(key, action, count)




	def print_dataframe(self):
		csvfile = csvFILE()
		csvfile.fulldir = self.writedir 
		labelrow = self.extend_types
		labelrow.insert(0, 'Student')
		csvfile.csvWRTR(labelrow)
		for xrow in self.students_avail:
			dvector_row = list(self.dataframe.loc[xrow])
			dvector_row.insert(0, xrow)
			csvfile.csvWRTR(dvector_row)




class ExcessiveSubNames(Exception):
	pass

class DataFrameNotSet(Exception):
	pass












		



