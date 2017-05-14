from jsonHNDLR import jsonHNDLR
import csv

class csvFILE(object):
	def __init__(self):
		self.mode = 'w'


	@property #what will be sent here is a dir + student no (e.g. a25) + jsonfname (now with csv extension)
	def fulldir(self):
		return self._fulldir 

	@fulldir.setter 
	def fulldir(self, dirname):
 		self._fulldir = self.procDir(dirname)

	def fileExists(self): 
		try:
			with open(self.fulldir, newline = '\n') as csvfile:
				pass
			csvfile.close()
			self.mode = 'a' 
		except FileNotFoundError as e:
			print(e)
			self.mode = 'w'

	def procDir(self, dirname):
		return dirname.replace("\\", "/")


	def csvWRTR(self, *args):
		self.fileExists()
		with open(self.fulldir, self.mode, newline = '\n') as csvfile:
			outputwriter = csv.writer(csvfile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
			outputwriter.writerow(args)
		csvfile.close()

		
