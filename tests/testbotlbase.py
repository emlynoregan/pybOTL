import unittest
import os, sys
try:
	import jsonschema
	import bOTL
except:
	def fixpath():
	    lcurrent = sys.path[len(sys.path)-1]
	    lparent = os.path.dirname(lcurrent)
	    sys.path.append(lparent)
	fixpath()
	import jsonschema
	import bOTL
import cProfile

ValidationError = jsonschema.ValidationError

class TestBOTLBase (unittest.TestCase):
    def doschematest(self, aInputSource):
        jsonschema.validate(aInputSource, bOTL._schema)
        
    def dobotltest(self, aSource, aTransform, aExpected):
        def _dobotltest(aSource, aTransform, aExpected):
            loutput = bOTL.Transform(aSource, aTransform)
            print "here"
            
            if aExpected is None:
                self.assertIsNone(loutput)
            else:
                self.assertEqual(aExpected, loutput)

        print aTransform                
        llocals = locals()
        lglobals = globals()
        lglobals["_dobotltest"] = _dobotltest
        print "1"
        cProfile.runctx("_dobotltest(aSource, aTransform, aExpected)", lglobals, llocals)
        print "2"

#    def dobotltest(self, aSource, aTransform, aExpected):
#        loutput = bOTL.Transform(aSource, aTransform)
#        
#        if aExpected is None:
#            self.assertIsNone(loutput)
#        else:
#            self.assertEqual(aExpected, loutput)
        
    def doselectorexpressiontest(self, aInput, aExpected):
        loutput = bOTL.GetSelectorExpressionFromStringConstructorTransform(aInput)
		
        self.assertEqual(aExpected, loutput)
		
    def doparseselectortermtest(self, aInput, aExpected):
        loutput = bOTL.ParseSelectorTerm(aInput)
        if aExpected == None:
            self.assertIsNone(loutput)
        else:
            self.assertTupleEqual(aExpected, loutput)
			
    def doapplyindexexpressiontoarraytest(self, aInputSource, aInputIndexExpression, aExpected):
        loutput = bOTL.ApplyIndexExpressionToArray(aInputSource, aInputIndexExpression)

        self.assertListEqual(aExpected, loutput)
		
    def doevaluateselectorexpressiontest(self, aInputSource, aInputSelectorExpression, aExpected):
        loutput = bOTL.EvaluateSelectorExpression([ aInputSource ], aInputSelectorExpression)
		
        if aExpected is None:
            self.assertIsNone(loutput)
        else:
            self.assertItemsEqual(aExpected, loutput)

    def dogetobjectsbynamerecursivetest(self, aInputSource, aInputName, aExpected):
        loutput = bOTL.GetObjectsByNameRecursive(aInputSource, aInputName)
		
        self.assertItemsEqual(aExpected, loutput)

    def dotokenizeselectorexpressiontest(self, aInput, aExpected):
        loutput = bOTL.TokenizeSelectorExpression(aInput)
        if aExpected is None:
            self.assertIsNone(loutput)
        else:
            self.assertListEqual(aExpected, loutput)


		
