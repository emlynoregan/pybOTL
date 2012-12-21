import unittest
import bOTL

class testApplyIndexExpressionToArray (unittest.TestCase):
	def dotest(self, aInputSource, aInputIndexExpression, aExpected):
		loutput = bOTL.ApplyIndexExpressionToArray(aInputSource, aInputIndexExpression)
		
		self.assertListEqual(aExpected, loutput)
		
	def test1(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "2"
		lexpected = ["thing3"]
		self.dotest(linputSource, linputIndexExpression, lexpected)

	def test2(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "4"
		lexpected = []
		self.dotest(linputSource, linputIndexExpression, lexpected)

	def test3(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "fred"
		lexpected = []
		self.dotest(linputSource, linputIndexExpression, lexpected)

