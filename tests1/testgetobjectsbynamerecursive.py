import unittest
import bOTL1

class testGetObjectsByNameRecursive (unittest.TestCase):
	def dotest(self, aInputSource, aInputName, aExpected):
		loutput = bOTL1.GetObjectsByNameRecursive(aInputSource, aInputName)
		
		self.assertItemsEqual(aExpected, loutput)
		
	def test1(self):
		linputSource = { "name": "fred bloggs" }
		linputName = "name"
		lexpected = [ "fred bloggs" ]
		self.dotest(linputSource, linputName, lexpected)

	def test2(self):
		linputSource = { "name": "fred bloggs" }
		linputName = "address"
		lexpected = [ ]
		self.dotest(linputSource, linputName, lexpected)

	def test3(self):
		linputSource = { "name": "fred bloggs", "thing": { "name": "george"} }
		linputName = "name"
		lexpected = [ "fred bloggs", "george" ]
		self.dotest(linputSource, linputName, lexpected)

	def test4(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputName = "name"
		lexpected = [ "fred bloggs", "george" ]
		self.dotest(linputSource, linputName, lexpected)
