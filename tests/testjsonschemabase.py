import unittest
import sys, os
import json
try:
	import jsonschema
except:
	def fixpath():
	    lcurrent = sys.path[len(sys.path)-1]
	    lparent = os.path.dirname(lcurrent)
	    sys.path.append(lparent)
	fixpath()
	import jsonschema

ValidationError = jsonschema.ValidationError

class TestJsonSchemaBase (unittest.TestCase):
	_schema = None
	
	def ReadFileAsString(self, aFileName):
		retval = None
		lFile = open(aFileName)
		try:
			retval = lFile.read()
		finally:
			lFile.close()
		return retval

	def setUp(self):
		lpath = sys.path[len(sys.path)-1]
		lfilename = os.path.join(lpath, os.path.join("bOTL", "bOTL.schema"))
		lschemaStr = self.ReadFileAsString(lfilename)
		if not lschemaStr:
			raise Exception("No schema found")
		self._schema = json.loads(lschemaStr)
		
	def dotest(self, aInputSource):
		jsonschema.validate(aInputSource, self._schema)
		
