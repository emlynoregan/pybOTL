#!/usr/bin/env python

import sys
import os
import jsonschema
import json

def Main():
    arglen = len(sys.argv)
    if arglen < 3 or arglen > 3:
        print "Usage: validateschema.py schemafile inputfile"
        sys.exit(1)
    
    lschemaFileName = sys.argv[1]
    linputFileName = sys.argv[2]
    
    def ReadFileAsString(aFileName):
    	retval = None
    	lFile = open(aFileName)
    	try:
    		retval = lFile.read()
    	finally:
    		lFile.close()
    	return retval
    
    lschema = ReadFileAsString(lschemaFileName)
    if lschema is None:
        print "No schema provided"
        sys.exit(1)
    
    linput = ReadFileAsString(linputFileName)
    if linput is None:
        print "No input provided"
        sys.exit(1)
    
    lschemaJson = json.loads(lschema)
    linputJson = json.loads(linput)
    
    print "*************************************"
    print "*********  Schema *******************"
    print "*************************************"
    print ""
    print lschemaJson
    print ""
    print "*************************************"
    print "*********  Input ********************"
    print "*************************************"
    print ""
    print linputJson
    print ""
    print "*************************************"
    print "*********  Validating ***************"
    print "*************************************"
    print ""
    
    try:
    	jsonschema.validate(linputJson, lschemaJson)
    	print "*********  Success ***************"
    
    except Exception, ex:
    	print "Failed: %s" % ex
    

if __name__ == '__main__':
    Main()