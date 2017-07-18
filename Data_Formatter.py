from StudentFiles import studentFILES
import pandas as pd

class data_formatter(object):
	def __init__(self, std_files, types_avail):
		self.std_files = std_files
		self.types_avail = types_avail
		self.dataframe = None 

	def sort_datalist(self, datalist):
		return sorted(datalist)

	def create_dataframe(self, data_index, col_list):
		return pd.DataFrame(index = data_index, columns = col_list)

	def insert_df_value(self, xrow, ycol, val):
		if self.dataframe == None:
			return #the only time this should be a problem is if my code is wrong, should there be an error here?
		self.dataframe.set_value(xrow, ycol, val)



class data_formatter_rawcount(data_formatter):
	pass 
		



