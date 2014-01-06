import testjsonschemabase

class testConstructorTransform (testjsonschemabase.TestJsonSchemaBase):
	def test1(self):
		linputSource = { 
			"type": "constructor", 
			"selector": ".thing >that",
			"transform": 5
		}
		self.dotest(linputSource)

	def test2(self):
		linputSource = { 
			"type": "constructor", 
			"transform": 5,
			"other": 4
		}
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)

	def test3(self):
		linputSource = { 
			"type": "traversal", 
			"scope": "freddo",
			"transform": 5
		}
		self.dotest(linputSource)

	def test4(self):
		linputSource = { 
			"type": "constructor", 
			"id": "freddo"
		}
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)

	def test5(self):
		linputSource = { 
			"type": "constructor", 
			"rules": []
		}
		self.dotest(linputSource)

	def test6(self):
		linputSource = { 
			"type": "constructor", 
			"rules": [
				{}
			]
		}
		self.dotest(linputSource)

	def test7(self):
		linputSource = { 
			"type": "constructor", 
			"rules": [
				{
					"match": "thing"
				}
			]
		}
		self.dotest(linputSource)

	def test8(self):
		linputSource = { 
			"type": "merge", 
			"rules": [
				{
					"transform": "thing"
				}
			]
		}
		self.dotest(linputSource)

	def test9(self):
		linputSource = { 
			"type": "merge", 
			"rules": [
				{
					"match": "thing",
					"transform": { "stuff": "#!freddo" }
				}
			]
		}
		self.dotest(linputSource)

	def test10(self):
		linputSource = { 
			"type": "constructor", 
			"rules": [
				{
					"match": "thing",
					"other": "thing"
				}
			]
		}
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
