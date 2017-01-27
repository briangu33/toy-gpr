class ObjFunc:
	
	def __init__(self, func):
		self.func = func

	def __call__(self, x):
		return self.func(x)