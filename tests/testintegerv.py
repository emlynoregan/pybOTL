import testjsonschemabase

class testIntegerV (testjsonschemabase.TestJsonSchemaBase):

	def test1(self):
		linputSource = 3
		self.dotest(linputSource)
