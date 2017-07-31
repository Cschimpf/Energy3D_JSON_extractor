from StudentFiles import studentFILES
from csvWRTR import csvFILE
import pandas as pd

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
		self.dataframe = self.create_dataframe(self.students_avail, self.types_avail)
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










		



