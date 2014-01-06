import testbotlbase

class testTokenizeSelectorExpression (testbotlbase.TestBOTLBase):
		
	def test1(self):
		linput = ".thing :anotherthing !athirdthing"
		lexpected = [".thing", ":anotherthing", "!athirdthing"]
		self.dotokenizeselectorexpressiontest(linput, lexpected)
		
	def test2(self):
		linput = ""
		lexpected = []
		self.dotokenizeselectorexpressiontest(linput, lexpected)

	def test3(self):
		linput = " "
		lexpected = []
		self.dotokenizeselectorexpressiontest(linput, lexpected)

	def test4(self):
		linput = " :thing4"
		lexpected = [":thing4"]
		self.dotokenizeselectorexpressiontest(linput, lexpected)

	def test5(self):
		linput = " :thing4   qwer "
		lexpected = [":thing4", "qwer"]
		self.dotokenizeselectorexpressiontest(linput, lexpected)

	def test6(self):
		linput = None
		lexpected = None
		self.dotokenizeselectorexpressiontest(linput, lexpected)
