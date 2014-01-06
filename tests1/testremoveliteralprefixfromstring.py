import unittest
import bOTL1

class testRemoveLiteralPrefixFromString (unittest.TestCase):
	def dotest(self, aInput, aExpected):
		loutput = bOTL1.RemoveLiteralPrefixFromString(aInput)
		
		self.assertEqual(aExpected, loutput)
		
	def test1(self):
		linput = "lit=A String"
		lexpected = "A String"
		self.dotest(linput, lexpected)

	def test2(self):
		linput = "A String"
		lexpected = "A String"
		self.dotest(linput, lexpected)

	def test3(self):
		linput = ""
		lexpected = ""
		self.dotest(linput, lexpected)

	def test4(self):
		linput = None
		lexpected = None
		self.dotest(linput, lexpected)

