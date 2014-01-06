import testjsonschemabase

class testLiteralV (testjsonschemabase.TestJsonSchemaBase):

	def test1(self):
		linputSource = { "type": "literal", "value": "x"}
		self.dotest(linputSource)
		
	def test2(self):
		linputSource = { "type": "literal" }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test3(self):
		linputSource = { "type": "literal", "valuex": "thing" }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test4(self):
		linputSource = { "type": "literal", "value": "thing", "other": True }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
				