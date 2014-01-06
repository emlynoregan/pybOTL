import unittest
import bOTL1

class testProcessLiteralString (unittest.TestCase):
	def dotest(self, aInputSource, aInputLiteralString, aExpected):
		loutput = bOTL1.ProcessLiteralString(aInputSource, aInputLiteralString, {})
		
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

	def test6(self):
		linputSource = \
			{ 
				"name": "fred bloggs",
				"num": 5, 
				"thing": [
					{"something": "other"}, 
					{ "name": "george"}
				] 
			}
		linputLiteralString = "{{.num}}"
		lexpected = "5"
		self.dotest(linputSource, linputLiteralString, lexpected)

	def test7(self):
		linputSource = \
			{ 
				"name": "fred bloggs", 
				"thing": [
					{"something": "other"}, 
					{ "name": "george"}
				] 
			}
		linputLiteralString = "{{.thing}}"
		lexpected = "[{'something': 'other'}, {'name': 'george'}]"
		self.dotest(linputSource, linputLiteralString, lexpected)

