import testjsonschemabase

class testLonghandObjectV (testjsonschemabase.TestJsonSchemaBase):

	def test1(self):
		linputSource = { "type": "object", "value": {}}
		self.dotest(linputSource)
		
	def test2(self):
		linputSource = { "type": "object", "value": [] }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)

	def test3(self):
		linputSource = { "type": "object" }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test4(self):
		linputSource = { "type": "object", "valuex": {"x": 1} }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test5(self):
		linputSource = { "type": "object", "value": {"thing": 3}, "other": True }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)

	def test6(self):
		linputSource = { "type": "object", "value": {"thing": {"type": "xyz"}}}
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		

				