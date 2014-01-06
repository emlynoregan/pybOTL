import unittest
import bOTL1

class testApplyIndexExpressionToArray (unittest.TestCase):
	def dotest(self, aInputSource, aInputIndexExpression, aExpected):
		loutput = bOTL1.ApplyIndexExpressionToArray(aInputSource, aInputIndexExpression)
		
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

	def test4(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = ":2"
		lexpected = ["thing1", "thing2"]
		self.dotest(linputSource, linputIndexExpression, lexpected)

	def test5(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "2:"
		lexpected = ["thing3", "thing4"]
		self.dotest(linputSource, linputIndexExpression, lexpected)

	def test6(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "1:3"
		lexpected = ["thing2", "thing3"]
		self.dotest(linputSource, linputIndexExpression, lexpected)

	def test7(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = ":"
		lexpected = linputSource
		self.dotest(linputSource, linputIndexExpression, lexpected)

	def test8(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "7:"
		lexpected = []
		self.dotest(linputSource, linputIndexExpression, lexpected)

	def test9(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "-1:"
		lexpected = ["thing4"]
		self.dotest(linputSource, linputIndexExpression, lexpected)

	def test10(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "1::2"
		lexpected = ["thing2", "thing4"]
		self.dotest(linputSource, linputIndexExpression, lexpected)
