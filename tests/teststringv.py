import testbotlbase

class testStringV (testbotlbase.TestBOTLBase):

	def test1(self):
		linputSource = "123"
		self.doschematest(linputSource)
		
	def test2(self):
		linputSource = ""
		self.doschematest(linputSource)

	def test3(self):
		linputSource = "#123"
		self.assertRaises(testjsonschemabase.ValidationError, self.doschematest, linputSource)

	def test10(self):
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
		self.dobotltest(linputSource, linputLiteralString, lexpected)
		
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
		self.dobotltest(linputSource, linputLiteralString, lexpected)
		
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
		self.dobotltest(linputSource, linputLiteralString, lexpected)

	def test4(self):
		linputSource = \
			{ 
				"givenname": "Fred",
				"surname": "Bloggs"
			}
		linputLiteralString = "{{.surname}}, {{.givenname}}"
		lexpected = "Bloggs, Fred"
		self.dobotltest(linputSource, linputLiteralString, lexpected)
		
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
		self.dobotltest(linputSource, linputLiteralString, lexpected)

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
		self.dobotltest(linputSource, linputLiteralString, lexpected)

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
		self.dobotltest(linputSource, linputLiteralString, lexpected)

