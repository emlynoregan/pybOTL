import unittest
import bOTL1

class testTokenizeSelectorExpression (unittest.TestCase):
	def dotest(self, aInput, aExpected):
		loutput = bOTL1.TokenizeSelectorExpression(aInput)
		if aExpected is None:
			self.assertIsNone(loutput)
		else:
			self.assertListEqual(aExpected, loutput)
		
	def test1(self):
		linput = ".thing :anotherthing !athirdthing"
		lexpected = [".thing", ":anotherthing", "!athirdthing"]
		self.dotest(linput, lexpected)
		
	def test2(self):
		linput = ""
		lexpected = []
		self.dotest(linput, lexpected)

	def test3(self):
		linput = " "
		lexpected = []
		self.dotest(linput, lexpected)

	def test4(self):
		linput = " :thing4"
		lexpected = [":thing4"]
		self.dotest(linput, lexpected)

	def test5(self):
		linput = " :thing4   qwer "
		lexpected = [":thing4", "qwer"]
		self.dotest(linput, lexpected)

	def test6(self):
		linput = None
		lexpected = None
		self.dotest(linput, lexpected)
