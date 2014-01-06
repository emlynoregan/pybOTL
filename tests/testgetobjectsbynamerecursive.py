import testbotlbase

class testGetObjectsByNameRecursive (testbotlbase.TestBOTLBase):
		
	def test1(self):
		linputSource = { "name": "fred bloggs" }
		linputName = "name"
		lexpected = [ "fred bloggs" ]
		self.dogetobjectsbynamerecursivetest(linputSource, linputName, lexpected)

	def test2(self):
		linputSource = { "name": "fred bloggs" }
		linputName = "address"
		lexpected = [ ]
		self.dogetobjectsbynamerecursivetest(linputSource, linputName, lexpected)

	def test3(self):
		linputSource = { "name": "fred bloggs", "thing": { "name": "george"} }
		linputName = "name"
		lexpected = [ "fred bloggs", "george" ]
		self.dogetobjectsbynamerecursivetest(linputSource, linputName, lexpected)

	def test4(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputName = "name"
		lexpected = [ "fred bloggs", "george" ]
		self.dogetobjectsbynamerecursivetest(linputSource, linputName, lexpected)

	def test5(self):
		linputSource = { "name": { "name": "fred bloggs"}}
		linputName = "name"
		lexpected = [ { "name": "fred bloggs"}, "fred bloggs" ]
		self.dogetobjectsbynamerecursivetest(linputSource, linputName, lexpected)
