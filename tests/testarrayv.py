import testbotlbase

class testArrayV (testbotlbase.TestBOTLBase):

	def test1(self):
		linputSource = []
		self.doschematest(linputSource)
		
	def test2(self):
		linputSource = [1, 2, "x"]
		self.doschematest(linputSource)

	def test3(self):
		linputSource = [1, 2, {"type": "thingo"}]
		self.assertRaises(testbotlbase.ValidationError, self.doschematest, linputSource)

	def test4(self):
		linputSource = [1, 2, {"type": "literal", "value": 3}]
		self.doschematest(linputSource)
