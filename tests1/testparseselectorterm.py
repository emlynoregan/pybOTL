import unittest
import bOTL1

class testParseSelectorTerm (unittest.TestCase):
	def dotest(self, aInput, aExpected):
		loutput = bOTL1.ParseSelectorTerm(aInput)
		if aExpected == None:
			self.assertIsNone(loutput)
		else:
			self.assertTupleEqual(aExpected, loutput)
		
	def test1(self):
		linput = ".thing"
		lexpected = (".", "thing")
		self.dotest(linput, lexpected)
		
	def test2(self):
		linput = "."
		lexpected = (".", "")
		self.dotest(linput, lexpected)
				
	def test3(self):
		linput = "x"
		lexpected = ("x", "")
		self.dotest(linput, lexpected)

	def test4(self):
		linput = ""
		lexpected = ("", "")
		self.dotest(linput, lexpected)

	def test5(self):
		linput = None
		lexpected = ("", "")
		self.dotest(linput, lexpected)
								