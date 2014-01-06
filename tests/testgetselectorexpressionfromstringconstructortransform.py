import unittest
import testbotlbase

class testGetSelectorExpressionFromStringConstructorTransform (testbotlbase.TestBOTLBase):
		
		
	def test1(self):
		linput = "#>selector >expression"
		lexpected = ">selector >expression"
		self.doselectorexpressiontest(linput, lexpected)

	def test2(self):
		linput = ">selector >expression"
		lexpected = None
		self.doselectorexpressiontest(linput, lexpected)

	def test3(self):
		linput = ""
		lexpected = None
		self.doselectorexpressiontest(linput, lexpected)

	def test4(self):
		linput = None
		lexpected = None
		self.doselectorexpressiontest(linput, lexpected)

