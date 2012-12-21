import unittest
import bOTL

class testRemoveLiteralPrefixFromDict (unittest.TestCase):
	def dotest(self, aInput, aExpected):
		loutput = bOTL.RemoveLiteralPrefixFromDict(aInput)
		
		if aExpected is None:
			self.assertIsNone(loutput)
		else:
			self.assertDictEqual(aExpected, loutput)
		
	def test1(self):
		linput = {"thing":"other"}
		lexpected = {"thing":"other"}
		self.dotest(linput, lexpected)

	def test2(self):
		linput = {"_lit_thing":"other"}
		lexpected = {"thing":"other"}
		self.dotest(linput, lexpected)

	def test3(self):
		linput = {}
		lexpected = {}
		self.dotest(linput, lexpected)

	def test4(self):
		linput = None
		lexpected = None
		self.dotest(linput, lexpected)

