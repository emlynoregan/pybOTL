import testjsonschemabase

class testLonghandArrayV (testjsonschemabase.TestJsonSchemaBase):

	def test1(self):
		linputSource = { "type": "array", "value": []}
		self.dotest(linputSource)
		
	def test2(self):
		linputSource = { "type": "array" }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test3(self):
		linputSource = { "type": "array", "valuex": [1, 2] }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
		
	def test4(self):
		linputSource = { "type": "array", "value": ["thing"], "other": True }
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)

	def test5(self):
		linputSource = { "type": "array", "value": [1, 2]}
		self.dotest(linputSource)

	def test6(self):
		linputSource = { "type": "array", "value": [ { "type": "array", "value": [1] } ]}
		self.dotest(linputSource)

				