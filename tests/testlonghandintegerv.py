import testjsonschemabase

class testLonghandIntegerV (testjsonschemabase.TestJsonSchemaBase):

	def test1(self):
		linputSource = { "type": "integer", "value": 0}
		self.dotest(linputSource)
		
	def test2(self):
		linputSource = { "type": "integer" }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test3(self):
		linputSource = { "type": "integer", "valuex": 1 }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test4(self):
		linputSource = { "type": "integer", "value": 2, "other": True }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)

	def test5(self):
		linputSource = { "type": "integer", "value": 3.5}
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)

