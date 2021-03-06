import unittest
import testbotlbase

class testApplyIndexExpressionToArray (testbotlbase.TestBOTLBase):
		
	def test1(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "2"
		lexpected = ["thing3"]
		self.doapplyindexexpressiontoarraytest(linputSource, linputIndexExpression, lexpected)

	def test2(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "4"
		lexpected = []
		self.doapplyindexexpressiontoarraytest(linputSource, linputIndexExpression, lexpected)

	def test3(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "fred"
		lexpected = []
		self.doapplyindexexpressiontoarraytest(linputSource, linputIndexExpression, lexpected)

	def test4(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = ":2"
		lexpected = ["thing1", "thing2"]
		self.doapplyindexexpressiontoarraytest(linputSource, linputIndexExpression, lexpected)

	def test5(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "2:"
		lexpected = ["thing3", "thing4"]
		self.doapplyindexexpressiontoarraytest(linputSource, linputIndexExpression, lexpected)

	def test6(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "1:3"
		lexpected = ["thing2", "thing3"]
		self.doapplyindexexpressiontoarraytest(linputSource, linputIndexExpression, lexpected)

	def test7(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = ":"
		lexpected = linputSource
		self.doapplyindexexpressiontoarraytest(linputSource, linputIndexExpression, lexpected)

	def test8(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "7:"
		lexpected = []
		self.doapplyindexexpressiontoarraytest(linputSource, linputIndexExpression, lexpected)

	def test9(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "-1:"
		lexpected = ["thing4"]
		self.doapplyindexexpressiontoarraytest(linputSource, linputIndexExpression, lexpected)

	def test10(self):
		linputSource = ["thing1", "thing2", "thing3", "thing4"]
		linputIndexExpression = "1::2"
		lexpected = ["thing2", "thing4"]
		self.doapplyindexexpressiontoarraytest(linputSource, linputIndexExpression, lexpected)
