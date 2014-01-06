import testbotlbase

class testNumberV (testbotlbase.TestBOTLBase):

	def test1(self):
		linputSource = 3.5
		self.doschematest(linputSource)
		
	def test1(self):
		result = self.dobotltest(None, 3.5, 3.5)
