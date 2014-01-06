import jsonschema
import sys, os
import json
import re

def ReadFileAsString(aFileName):
    retval = None
    lFile = open(aFileName)
    try:
        retval = lFile.read()
    finally:
        lFile.close()
    return retval

lpath = os.path.dirname(__file__)
lfilename = os.path.join(lpath, "bOTL.schema")
lbotlSchemaString = ReadFileAsString(lfilename)
if not lbotlSchemaString:
    raise Exception("No schema found")
_schema = json.loads(lbotlSchemaString)
lbotlSchemaString = None

def _getTransformCandidates():
    retval = [
            litem["$ref"] for litem in _schema["definitions"]["transform"]["anyOf"] if litem["$ref"] != "#/definitions/literaltransform"
        ]
    
    retval.extend([
            litem["$ref"] for litem in _schema["definitions"]["literaltransform"]["anyOf"]
        ])
    
    return retval
_transformCandidates = _getTransformCandidates()

def Transform(aSource, aTransform, aScope = {}):
    ltargetvalue = None
    
    ltargetlist = TransformList2(aSource, aTransform, aScope)
    if ltargetlist:
        ltargetvalue = ltargetlist[0]
    
    return ltargetvalue

def TransformList(aSource, aTransform, aScope):
    global _transformCandidates

    ltargetlist = []

    lorigref = _schema["$ref"]
    try:
        for lcandidate in _transformCandidates:
            _schema["$ref"] = lcandidate
            lfound = False
            try:
                jsonschema.validate(aTransform, _schema)
                lfound = True
            except:
                pass
            if lfound:
                lcandidateSplit = lcandidate.split("/")
                lfunctionName = "Process_%s" % lcandidateSplit[len(lcandidateSplit)-1] 
                lfunction = globals()[lfunctionName] if lfunctionName in globals() else None
                if not lfunction:
                    raise Exception("Internal Error; No such function %s" % lfunctionName)
                lresultList = lfunction(aSource, aTransform, aScope)
                ltargetlist.extend(lresultList)
                break
    finally:
        _schema["$ref"] = lorigref
        
    return ltargetlist

def TransformList2(aSource, aTransform, aScope):
    global _transformCandidates

    lfunction = IdentifyTransform(aTransform)
    if not lfunction:
        raise Exception("Cannot identify transform: %s" % aTransform)
    
    ltargetlist = lfunction(aSource, aTransform, aScope)
            
    return ltargetlist
        
def Process_literalv(aSource, aTransform, aScope):
    return [ aTransform["value"] ]

def Process_arrayv(aSource, aTransform, aScope):
    retval = [lresult for litem in aTransform for lresult in TransformList2(aSource, litem, aScope)]
    return [ retval ]
    
def Process_longhandarrayv(aSource, aTransform, aScope):
    retval = [lresult for litem in aTransform["value"] for lresult in TransformList2(aSource, litem, aScope)]
    return [ retval ]

def Process_objectv(aSource, aTransform, aScope):
    retval = {}
    for lrawkey in aTransform.keys():
        lkey = Process_stringv(aSource, lrawkey, aScope)[0]
        lvalue = Transform(aSource, aTransform[lrawkey], aScope)
        retval[lkey] = lvalue
    return [ retval ]
    
def Process_longhandobjectv(aSource, aTransform, aScope):
    retval = {}
    for lkey in aTransform["value"].keys():
        lvalue = Transform(aSource, aTransform["value"][lkey], aScope)
        retval[lkey] = lvalue
    return [ retval ]

def Process_integerv(aSource, aTransform, aScope):
    return [ aTransform ]
    
def Process_longhandintegerv(aSource, aTransform, aScope):
    return [ aTransform["value"] ]

def Process_numberv(aSource, aTransform, aScope):
    return [ aTransform ] # it's just a number

def Process_longhandnumberv(aSource, aTransform, aScope):
    return [ aTransform["value"] ]

def Process_nullv(aSource, aTransform, aScope):
    return [ None ]

def Process_longhandnullv(aSource, aTransform, aScope):
    return [ None ]

def Process_stringv(aSource, aTransform, aScope):
    retval = None

    # do selector substitutions here
    lworkingCopyOfString = aTransform
    
    # find a substitution
    lregex = re.compile("{{(.*?)}}")
    lmatch = lregex.search(lworkingCopyOfString)
    while lmatch:
        lselectorExpression = lmatch.group(1)
        lselectedlist = EvaluateSelectorExpression([ aSource ], lselectorExpression, aScope)
        if not lselectedlist:
            lreplacevalue = ""
        else:
            lreplacevalue = unicode(lselectedlist[0])
        
        lworkingCopyOfString = lworkingCopyOfString.replace("{{%s}}" % lselectorExpression, lreplacevalue)
        #
        # get next match
        lmatch = lregex.search(lworkingCopyOfString) # should now be a new string

    return [ lworkingCopyOfString ]

def Process_longhandstringv(aSource, aTransform, aScope):
    return Process_stringv(aSource, aTransform["value"], aScope)

def Process_stringconstructortransform(aSource, aTransform, aScope):
    lselectorExpression = GetSelectorExpressionFromStringConstructorTransform(aTransform)
    retval = EvaluateSelectorExpression([ aSource ], lselectorExpression, dict(aScope))
    return retval
    
def Process_complextransform(aSource, aTransform, aScope):
    retval = []
    
    if "transform" in aTransform:
        ltransform = dict(aTransform)

        ltransformRule = {"transform": ltransform["transform"] }
        del ltransform["transform"]
        
        if "scope" in aTransform:
            ltransformRule["scope"] = ltransform["scope"]
        
        ltransform["rules"] = [ ltransformRule ]
    else:
        ltransform = aTransform
    
    lscope = dict(aScope)
    
    if "selector" in ltransform:
        linputList = EvaluateSelectorExpression([ aSource ], ltransform["selector"], lscope)
    else:
        linputList = [ aSource ]
        
    for linput in linputList:
#        lscope2 = dict(lscope)
#        if "scope" in ltransform:
#            lscope2[ltransform["scope"]] = linput
        if ltransform["type"] == "traversal":
            retval.append(PerformTraversal(aSource, linput, ltransform, lscope))
        else:
            retval.append(PerformConstructor(aSource, linput, ltransform, lscope))
    
    if ltransform["type"] == "merge":
        retval = PerformMerge(retval)
    
    return retval

_complexTypeCandidates = set(["merge", "constructor", "traversal"])
_simpleTypeCandidates = {
    "literal": (Process_literalv, ["type", "value"], None),
    "array": (Process_longhandarrayv, ["type", "value"], None),
    "object": (Process_longhandobjectv, ["type", "value"], None),
    "integer": (Process_longhandintegerv, ["type", "value"], lambda aTrans: "value" in aTrans and IsInteger(aTrans["value"])),
    "integer": (Process_longhandnumberv, ["type", "value"], lambda aTrans: "value" in aTrans and IsFloat(aTrans["value"])),
    "null": (Process_longhandnullv, ["type"], None),
    "string": (Process_longhandstringv, ["type", "value"], lambda aTrans: "value" in aTrans and IsString(aTrans["value"])),
    "merge": Process_complextransform,
    "constructor": Process_complextransform,
    "traversal": Process_complextransform
}

def IdentifyTransform(aTransform):        
    retval = None

    if IsNull(aTransform):
        retval = Process_nullv
    elif IsFloat(aTransform):
        retval = Process_numberv
    elif IsInteger(aTransform):
        retval = Process_integerv
    elif IsString(aTransform):
        if aTransform[:1] == "#":
            retval = Process_stringconstructortransform
        else:
            retval = Process_stringv
    elif IsDict(aTransform):
        if "type" in aTransform:
            if aTransform["type"] in _complexTypeCandidates:
                lkeys = set(aTransform.keys())
                if "transform" in aTransform:
                    lkeys.difference_update(set(["type", "transform", "scope", "selector"]))
                    if lkeys:
                        raise Exception("Unexpected keys in complex transform: %s" % lkeys)
                    if "selector" in aTransform and not IsString(aTransform["selector"]):
                        raise Exception("selector must be a string: %s" % aTransform["selector"])
                    if "scope" in aTransform and not IsString(aTransform["scope"]):
                        raise Exception("scope must be a string: %s" % aTransform["scope"])
                    retval = Process_complextransform
                else:
                    if not "rules" in lkeys:
                        raise Exception("Required property 'rules' missing from transform")
                    lkeys.difference_update(set(["type", "rules", "selector"]))
                    if lkeys:
                        raise Exception("Unexpected keys in complex transform: %s" % lkeys)
                    if "selector" in aTransform and not IsString(aTransform["selector"]):
                        raise Exception("selector must be a string: %s" % aTransform["selector"])
                    if not IsArray(aTransform["rules"]):
                        raise Exception("rules must be an array but is %s" % type(aTransform["rules"]))
                    for litem in aTransform["rules"]:
                        if not IsDict(litem):
                            raise Exception("rules element must be dict but is %s" % type(litem))
                        lkeys = set(litem.keys())
                        lkeys.difference_update(set(["match", "transform", "scope"]))
                        if lkeys:
                            raise Exception("Unexpected keys in complex transform: %s" % lkeys)
                        if "scope" in aTransform and not IsString(aTransform["scope"]):
                            raise Exception("scope must be a string: %s" % aTransform["scope"])
                    retval = Process_complextransform
            elif aTransform["type"] in _simpleTypeCandidates:
                ltypeRule = _simpleTypeCandidates[aTransform["type"]]
                lkeys = set(aTransform.keys())
                if not lkeys.issuperset(set(ltypeRule[1])):
                    raise Exception("Required fields %s not all present in simple transform" % ltypeRule[1])
                lkeys.difference_update(set(ltypeRule[1]))
                if lkeys:
                    raise Exception("Unexpected keys in simple transform: %s" % lkeys)
                if ltypeRule[2] and ltypeRule[2](aTransform):
                    raise Exception("Validation rule failed for simple transform: %s" % aTransform)
                retval = ltypeRule[0]
            else:
                raise Exception("Unknown type '%s'" % aTransform["type"])
        else:
            retval = Process_objectv
    elif IsArray(aTransform):
        retval = Process_arrayv
    
    return retval

def _iPerformConstructor(aSource, aInput, aTransform, aScope):
    retval = None
    lmatch = False
    for lrule in aTransform["rules"]:
        lscope = dict(aScope) 
        if "scope" in lrule:
            lscope[lrule["scope"]] = aInput
        if "match" in lrule:
            try:
                jsonschema.validate(aInput, lrule["match"])
                lmatch = True
            except:
                pass
        else:
            lmatch = True
        if lmatch:
            if "transform" in lrule:
                retval = Transform(aSource, lrule["transform"], lscope)
            else:
                retval = aInput
            break
        
    return (lmatch, retval)

def PerformConstructor(aSource, aInput, aTransform, aScope):
    lmatch, retval = _iPerformConstructor(aSource, aInput, aTransform, aScope)
    return retval

def PerformTraversal(aSource, aInput, aTransform, aScope):
    lmatch, retval = _iPerformConstructor(aSource, aInput, aTransform, aScope)
    
    if not lmatch:
        if IsDict(aInput):
            retval = {}
            for lkey in aInput.keys():
                retval[lkey] = PerformTraversal(aSource, aInput[lkey], aTransform, aScope)
        elif IsArray(aInput):
            retval = [PerformTraversal(aSource, litem, aTransform, aScope) for litem in aInput]
        else:
            retval = aInput
        
    return retval        

def PerformMerge(aList):
    retval = None
    if aList:
        for litem in aList:
            if not retval:
                if IsDict(litem):
                    retval = dict(litem)
                if IsArray(litem) or IsTuple(litem):
                    retval = list(litem)
                else:
                    retval = litem
            else:
                if IsDict(retval) and IsDict(litem):
                    for lkey in litem.keys():
                        retval[lkey] = litem[lkey]
                elif IsArray(retval) and (IsArray(litem) or IsTuple(litem)):
                    retval.extend(litem)
    return retval
                
                        
                    

def EvaluateSelectorExpression(aSourceList, aSelectorExpression, aScope = {}):
    lselectedlist = None
    
    if not aSelectorExpression is None:
        lselectedlist = []
        
        lselectorterms = TokenizeSelectorExpression(aSelectorExpression)
        
        if lselectorterms:
            lselectedlist = EvaluateSelector(aSourceList, lselectorterms[0], lselectorterms[1:], aScope)
        else:
            lselectedlist = aSourceList
        
    return lselectedlist

def EvaluateSelector(aSourceList, aSelectorTerm, aFollowingSelectorTerms, aScope):
    llocalselectedlist = []
    
    lselectortermtype, lselectortermvalue = ParseSelectorTerm(aSelectorTerm)
    
    if lselectortermtype == ".":
        llocalselectedlist = [lsource[lselectortermvalue] for lsource in aSourceList if IsDict(lsource) and lselectortermvalue in lsource]
    elif lselectortermtype == ">":
        for lsource in aSourceList:
            llocalselectedlist.extend(GetObjectsByNameRecursive(lsource, lselectortermvalue))
    elif lselectortermtype == "@":
        for lsource in aSourceList:
            llocalselectedlist.extend(ApplyIndexExpressionToArray(lsource, lselectortermvalue))
    elif lselectortermtype == "!":
        if IsDict(aScope) and lselectortermvalue in aScope:
            llocalselectedlist.append(aScope[lselectortermvalue])
    elif lselectortermtype == "%":
        for lsource in aSourceList:
            if IsDict(lsource):
                llocalselectedlist.extend(lsource.keys())
    elif lselectortermtype == "&":
        llocalselectedlist = [ aSourceList ]
    elif lselectortermtype == "*":
        if IsDict(aScope) and lselectortermvalue in aScope:
            lscopeValue = aScope[lselectortermvalue]
            if IsDict(lscopeValue):
                for lsource in aSourceList:
                    if lsource in lscopeValue:
                        llocalselectedlist.append(lscopeValue[lsource])
    elif lselectortermtype == "^":
        llocalselectedlist = list(set(aSourceList))
    elif lselectortermtype == "?":
        if IsDict(aScope) and aSourceList and lselectortermvalue:
            aScope[lselectortermvalue] = aSourceList[0]
        llocalselectedlist = aSourceList
            
    lselectedlist = []
    if aFollowingSelectorTerms:
        lnextSelectorTerm = aFollowingSelectorTerms[0]
        lnextFollowingSelectorTerms = aFollowingSelectorTerms[1:]
        lselectedlist = EvaluateSelector(llocalselectedlist, lnextSelectorTerm, lnextFollowingSelectorTerms, aScope)
    else:
        lselectedlist = llocalselectedlist
    
    return lselectedlist
    
def TokenizeSelectorExpression(aSelectorExpression):
    retval = None
    if not aSelectorExpression is None:
        retval = []
        lselectorExpressionTrimmed = aSelectorExpression.strip()
        if lselectorExpressionTrimmed:
            retval = re.split(r'\s+', lselectorExpressionTrimmed)
    return retval

def ParseSelectorTerm(aSelectorTerm):
    lselectortermtype = ""
    lselectortermvalue = ""

    if aSelectorTerm:
        lselectortermtype = aSelectorTerm[0]
        lselectortermvalue = aSelectorTerm[1:]
        
    return lselectortermtype, lselectortermvalue

def GetObjectsByNameRecursive(aSource, aName):
    lselectedobjects = []
    
    if IsDict(aSource):
        for lkey, lvalue in aSource.iteritems():
            if lkey == aName:
                lselectedobjects.append(aSource[aName])
            lselectedobjects.extend(GetObjectsByNameRecursive(lvalue, aName))
    elif IsArray(aSource) or IsTuple(aSource):
        for lchild in aSource:
            lselectedobjects.extend(GetObjectsByNameRecursive(lchild, aName))
    
    return lselectedobjects

def ApplyIndexExpressionToArray(aSource, aIndexExpression):
    retval = []
    lindexTerms = aIndexExpression.split(":")
    if (IsArray(aSource) or IsTuple(aSource)) and lindexTerms and len(lindexTerms) > 0:
        lstart = None
        lend = None
        lstep = None

        if len(lindexTerms) >= 1:
            try:
                lstart = int(lindexTerms[0])
            except:
                pass
        if len(lindexTerms) >= 2:
            try:
                lend = int(lindexTerms[1])
            except:
                pass
        
        if len(lindexTerms) >= 3:
            try:
                lstep = int(lindexTerms[2])
            except:
                pass

        if lstep is None:
            lstep = 1


        if len(lindexTerms) == 1:
            try:
                retval.append(aSource[lstart])
            except:
                pass
            
        elif len(lindexTerms) >= 2:
            try:
                if lstart is None:
                    if lend is None:
                        retval = aSource[::lstep]
                    else:
                        retval = aSource[:lend:lstep]
                else:
                    if lend is None:
                        retval = aSource[lstart::lstep]
                    else:
                        retval = aSource[lstart:lend:lstep]
            except:
                pass

    return retval

def GetSelectorExpressionFromStringConstructorTransform(aSimpleRefString):
    retval = None
    
    if IsString(aSimpleRefString) and aSimpleRefString[:1] == "#":
        retval = aSimpleRefString[1:]

    return retval

def IsDict(aTransform):
    retval = isinstance(aTransform, dict)
    
    return retval

def IsArray(aTransform):
    retval = isinstance(aTransform, list)
    
    return retval

def IsTuple(aTransform):
    retval = isinstance(aTransform, tuple)
    
    return retval

def IsString(aTransform):
    retval = isinstance(aTransform, basestring)

    return retval

def IsInteger(aTransform):
    retval = isinstance(aTransform, ( int, long ) )
    
    return retval
    
def IsFloat(aTransform):
    retval = isinstance(aTransform, ( float ) )
    
    return retval
    
def IsNull(aTransform):
    retval = aTransform is None
    
    return retval