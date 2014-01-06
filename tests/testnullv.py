import testjsonschemabase

class testNullV (testjsonschemabase.TestJsonSchemaBase):

	def test1(self):
		linputSource = None
		self.dotest(linputSource)
		
