import unittest
import bOTL

class testProcessLiteralString (unittest.TestCase):
	def dotest(self, aInputSource, aInputLiteralString, aExpected):
		loutput = bOTL.ProcessLiteralString(aInputSource, aInputLiteralString, {})
		
		self.assertEqual(aExpected, loutput)
		
	def test1(self):
		linputSource = \
			{ 
				"name": "fred bloggs", 
				"thing": [
					{"something": "other"}, 
					{ "name": "george"}
				] 
			}
		linputLiteralString = "Fred"
		lexpected = "Fred"
		self.dotest(linputSource, linputLiteralString, lexpected)
		
	def test2(self):
		linputSource = \
			{ 
				"name": "fred bloggs", 
				"thing": [
					{"something": "other"}, 
					{ "name": "george"}
				] 
			}
		linputLiteralString = "{{.name}}"
		lexpected = "fred bloggs"
		self.dotest(linputSource, linputLiteralString, lexpected)
		
	def test3(self):
		linputSource = \
			{ 
				"name": "fred bloggs", 
				"thing": [
					{"something": "other"}, 
					{ "name": "george"}
				] 
			}
		linputLiteralString = "x{{.name}}y"
		lexpected = "xfred bloggsy"
		self.dotest(linputSource, linputLiteralString, lexpected)

	def test4(self):
		linputSource = \
			{ 
				"givenname": "Fred",
				"surname": "Bloggs"
			}
		linputLiteralString = "{{.surname}}, {{.givenname}}"
		lexpected = "Bloggs, Fred"
		self.dotest(linputSource, linputLiteralString, lexpected)
		
	def test5(self):
		linputSource = \
			{ 
				"name": "fred bloggs", 
				"thing": [
					{"something": "other"}, 
					{ "name": "george"}
				] 
			}
		linputLiteralString = "({{>something}}): ({{.thing >name}})"
		lexpected = "(other): (george)"
		self.dotest(linputSource, linputLiteralString, lexpected)

