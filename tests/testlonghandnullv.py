import testjsonschemabase

class testLonghandNullV (testjsonschemabase.TestJsonSchemaBase):

	def test1(self):
		linputSource = { "type": "null" }
		self.dotest(linputSource)
		
	def test2(self):
		linputSource = { "type": "null", "value": 2 }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)


