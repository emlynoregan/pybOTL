import unittest
import testbotlbase

class testEvaluateSelectorExpression (testbotlbase.TestBOTLBase):
		
	def test1(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ">name"
		lexpected = [ "fred bloggs", "george" ]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)

	def test2(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ""
		lexpected = [ linputSource ]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)

	def test3(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = "x"
		lexpected = [ ]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)

	def test4(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = None
		lexpected = None
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)

	def test5(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ".thing >name"
		lexpected = [ "george" ]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)

	def test6(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ".thing"
		lexpected = [[{"something": "other"}, { "name": "george"}]]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)

	def test7(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ".thing @1"
		lexpected = [ { "name": "george"} ]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)
	
	def test8(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ".thing @1 .name"
		lexpected = [ "george" ]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)
	
	def test9(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ".thing @7 .name"
		lexpected = [  ]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)
	
	def test10(self):
		linputSource = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		linputSelectorExpression = "@2:5"
		lexpected = [3, 4, 5]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)
	
	def test11(self):
		linputSource = [1, 2, 2, 2, 3]
		linputSelectorExpression = "@:"
		lexpected = [1, 2, 2, 2, 3]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)

	def test12(self):
		linputSource = [1, 2, 2, 2, 3]
		linputSelectorExpression = "@: ^"
		lexpected = [1, 2, 3]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)

	def test13(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = "%"
		lexpected = ["name", "thing"]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)
		
	def test13(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = "?dict % *dict"
		lexpected = ["fred bloggs", [{"something": "other"}, { "name": "george"}]]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)
		
	def test14(self):
		linputSource = { "name": "fred bloggs", "thing": [{"something": "other"}, { "name": "george"}] }
		linputSelectorExpression = ">name &"
		lexpected = [ [ "george", "fred bloggs" ] ]
		self.doevaluateselectorexpressiontest(linputSource, linputSelectorExpression, lexpected)
		