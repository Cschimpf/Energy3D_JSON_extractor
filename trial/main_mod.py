class dudclass(object):

	def __init__(self):
		pass

	@property 
	def dumb(self):
		return self._dumb 

	@dumb.setter
	def dumb(self, value):
		print(value)
		self._dumb = value 


class dudjr(dudclass):

	def __init__(self):
		pass