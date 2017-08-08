from StudentFiles import studentFILES
from csvWRTR import csvFILE
import pandas as pd
import datetime

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
	def __init__(self, std_files, types_avail):
		self.std_files = std_files
		self.students_avail = None 
		self.types_avail = types_avail
		self.dataframe = None 
		
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

	def create_dataframe(self, data_index, col_list):
		return pd.DataFrame(index = data_index, columns = col_list)

	def create_data_vector(self):
		data_vector = {}
		for entry in self.types_avail:
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





class data_formatter_rawcount(data_formatter):
	def __init__(self, std_files, types_avail):
		super().__init__(std_files, types_avail)

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
		self.dataframe = self.create_dataframe(self.students_avail, self.types_avail) #you might want to shift it so Student column is added here or would that be obnoxious? Hmm
		for key, val in self.std_files.recordlist.items():
			dvector = self.create_data_vector()
			for subkey, subval in val.items():
				if subval[0] != None:
					for tree in subval[0].actTREES:
						self.incr_data_vector(dvector, tree.cargo)
			for action, count in dvector.items():
				self.insert_df_value(key, action, count)


	def print_dataframe(self):
		csvfile = csvFILE()
		csvfile.fulldir = self.writedir 
		labelrow = self.types_avail
		labelrow.insert(0, 'Student')
		csvfile.csvWRTR(labelrow)
		for xrow in self.students_avail:
			dvector_row = list(self.dataframe.loc[xrow])
			dvector_row.insert(0, xrow)
			csvfile.csvWRTR(dvector_row)


class data_formatter_action_density(data_formatter):
	def __init__(self, std_files, types_avail):
		super().__init__(std_files, types_avail)
		

	def export_dataframe(self):
		self.populate_dataframe()
		self.print_dataframe()

	def populate_dataframe(self):
		self.students_avail = self.sort_datalist(self.retrieve_col_list())
		self.dataframe = self.create_dataframe(self.students_avail, ['Action Density'])
		
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
						elif time_diff.days == 0 and time_diff.seconds < 1800 and tree.cargo not in ignored_actions:
							time_count = time_count + time_diff.seconds
						prev_time = datetime.datetime.strptime(tree.datetime,  "%Y-%m-%d %H:%M:%S")
						#here will also need to check is this an analysis tasks? if not then how compute time? 
						#should there be some time attributes on the data_formatter object itself to keep things
						#easier?
						#And should there be a check as to when the previous time point and the new one is greater
						#than 30 minutes of inactivity>??
			if action_count > 0 and time_count > 0:
				action_density = action_count/time_count #divided by some time measure 
			self.insert_df_value(key, 'Action Density', action_density)

	def print_dataframe(self):
		csvfile = csvFILE()
		csvfile.fulldir = self.writedir 
		csvfile.csvWRTR(['Student', 'Action Density']) #will need to think about how to abstract this when its just one variable
		for xrow in self.students_avail:               # is this even the right venue for this or should variable creation be elsewhere?
			dvector_row = list(self.dataframe.loc[xrow])
			dvector_row.insert(0, xrow)
			csvfile.csvWRTR(dvector_row)










		



