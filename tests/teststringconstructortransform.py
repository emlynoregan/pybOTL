import testjsonschemabase

class testStringConstructorTransformV (testjsonschemabase.TestJsonSchemaBase):

	def test1(self):
		linputSource = "#.thing  .thing2 >that"
		self.dotest(linputSource)

	def test2(self):
		linputSource = "#x.thing  .thing2 >that"
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)

	def test3(self):
		linputSource = "#"
		self.dotest(linputSource)

	def test4(self):
		linputSource = "#   ."
		self.dotest(linputSource)

	def test5(self):
		linputSource = "# .x"
		self.dotest(linputSource)

	def test6(self):
		linputSource = "# .x >y zz"
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)

	def test7(self):
		linputSource = [ { "thing": "# .x" } ]
		self.dotest(linputSource)

	def test8(self):
		linputSource = [ { "thing": "# x" } ]
		self.assertRaises(testjsonschemabase.ValidationError, self.dotest, linputSource)
