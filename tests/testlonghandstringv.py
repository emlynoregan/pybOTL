import testjsonschemabase

class testLonghandStringV (testjsonschemabase.TestJsonSchemaBase):

	def test1(self):
		linputSource = { "type": "string", "value": "x"}
		self.dotest(linputSource)
		
	def test2(self):
		linputSource = { "type": "string" }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test3(self):
		linputSource = { "type": "string", "valuex": "1" }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test4(self):
		linputSource = { "type": "string", "value": "4", "other": True }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)

	def test5(self):
		linputSource = { "type": "string", "value": 3.5}
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)

	def test6(self):
		linputSource = { "type": "string", "value": "" }
		self.dotest(linputSource)

