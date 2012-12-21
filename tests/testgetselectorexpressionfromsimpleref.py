import unittest
import bOTL

class testGetSelectorExpressionFromSimpleRef (unittest.TestCase):
	def dotest(self, aInput, aExpected):
		loutput = bOTL.GetSelectorExpressionFromSimpleRef(aInput)
		
		self.assertEqual(aExpected, loutput)
		
	def test1(self):
		linput = "ref=:selector :expression"
		lexpected = ":selector :expression"
		self.dotest(linput, lexpected)

	def test2(self):
		linput = ":selector :expression"
		lexpected = None
		self.dotest(linput, lexpected)

	def test3(self):
		linput = ""
		lexpected = None
		self.dotest(linput, lexpected)

	def test4(self):
		linput = None
		lexpected = None
		self.dotest(linput, lexpected)

