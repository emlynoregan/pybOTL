import testjsonschemabase

class testObjectV (testjsonschemabase.TestJsonSchemaBase):

	def test1(self):
		linputSource = { "fred": "a", "wilma": "b"}
		self.dotest(linputSource)
		
	def test2(self):
		linputSource = { "type": "xyz", "thing": 2 }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test3(self):
		linputSource = { "type": 3, "x": [1, 2] }
		self.dotest(linputSource)
		
	def test4(self):
		linputSource = { }
		self.dotest(linputSource)
