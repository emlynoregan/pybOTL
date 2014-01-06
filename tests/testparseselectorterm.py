import unittest
import testbotlbase

class testParseSelectorTerm (testbotlbase.TestBOTLBase):
		
	def test1(self):
		linput = ".thing"
		lexpected = (".", "thing")
		self.doparseselectortermtest(linput, lexpected)
		
	def test2(self):
		linput = "."
		lexpected = (".", "")
		self.doparseselectortermtest(linput, lexpected)
				
	def test3(self):
		linput = "x"
		lexpected = ("x", "")
		self.doparseselectortermtest(linput, lexpected)

	def test4(self):
		linput = ""
		lexpected = ("", "")
		self.doparseselectortermtest(linput, lexpected)

	def test5(self):
		linput = None
		lexpected = ("", "")
		self.doparseselectortermtest(linput, lexpected)
								