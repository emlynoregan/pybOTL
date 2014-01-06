import testjsonschemabase

class testLonghandIntegerV (testjsonschemabase.TestJsonSchemaBase):

	def test1(self):
		linputSource = { "type": "number", "value": 0}
		self.dotest(linputSource)
		
	def test2(self):
		linputSource = { "type": "number" }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test3(self):
		linputSource = { "type": "number", "valuex": 1 }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test4(self):
		linputSource = { "type": "number", "value": 2.0, "other": True }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)

	def test5(self):
		linputSource = { "type": "number", "value": 3.5}
		self.dotest(linputSource)

