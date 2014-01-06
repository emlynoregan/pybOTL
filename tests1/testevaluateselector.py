import unittest
import bOTL1

class testEvaluateSelectorExpression (unittest.TestCase):
	def dotest(self, aInputSource, aInputSelectorExpression, aExpected):
		loutput = bOTL1.EvaluateSelectorExpression(aInputSource, aInputSelectorExpression)
		
		if aExpected is None:
			self.assertIsNone(loutput)
		else:
			self.assertItemsEqual(aExpected, loutput)
		
	def test1(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ">name"
		lexpected = [ "fred bloggs", "george" ]
		self.dotest(linputSource, linputSelectorExpression, lexpected)

	def test2(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ""
		lexpected = [ linputSource ]
		self.dotest(linputSource, linputSelectorExpression, lexpected)

	def test3(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = "x"
		lexpected = [ ]
		self.dotest(linputSource, linputSelectorExpression, lexpected)

	def test4(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = None
		lexpected = None
		self.dotest(linputSource, linputSelectorExpression, lexpected)

	def test5(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ".thing >name"
		lexpected = [ "george" ]
		self.dotest(linputSource, linputSelectorExpression, lexpected)

	def test6(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ".thing"
		lexpected = [[{"something": "other"}, { "name": "george"}]]
		self.dotest(linputSource, linputSelectorExpression, lexpected)

	def test7(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ".thing @1"
		lexpected = [ { "name": "george"} ]
		self.dotest(linputSource, linputSelectorExpression, lexpected)
	
	def test8(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ".thing @1 .name"
		lexpected = [ "george" ]
		self.dotest(linputSource, linputSelectorExpression, lexpected)
	
	def test9(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ".thing @7 .name"
		lexpected = [  ]
		self.dotest(linputSource, linputSelectorExpression, lexpected)
	
	def test10(self):
		linputSource = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		linputSelectorExpression = "@2:5"
		lexpected = [3, 4, 5]
		self.dotest(linputSource, linputSelectorExpression, lexpected)
	

