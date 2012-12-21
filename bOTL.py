import re

def Transform(aSource, aTransform, aScope = {}):
    ltargetvalue = None
    
    ltargetlist = TransformList(aSource, aTransform, aScope)
    if ltargetlist:
        ltargetvalue = ltargetlist[0]
    
    return ltargetvalue

def TransformList(aSource, aTransform, aScope):
    ltargetlist = []
    
    if IsLiteralValue(aTransform):
        if IsLiteralString(aTransform):
            ltargetvalue = RemoveLiteralStringPrefix(aTransform)
        else:
            ltargetvalue = aTransform
        ltargetlist.append(ltargetvalue)
    elif IsLiteralArray(aTransform) or IsLiteralTuple(aTransform):
        ltargetvalue = []
        for ltransformElement in aTransform:
            lchildTargetList = TransformList(aSource, ltransformElement, aScope)
            ltargetvalue.extend(lchildTargetList)
        ltargetlist.append(ltargetvalue)
    elif IsLiteralDict(aTransform):
        ltargetvalue = {}
        for lkey, lvalue in aTransform.iteritems():
            lchildTargetValue = Transform(aSource, lvalue, aScope)
            ltargetvalue[lkey] = lchildTargetValue
        ltargetlist.append(ltargetvalue)
    elif IsSimpleRef(aTransform):
        lselectorexpression = GetSelectorExpressionFromSimpleRef(aTransform)
        ltargetlist = EvaluateSelectorExpression(aSource, lselectorexpression, aScope)
    elif IsComplexRef(aTransform):
        
        ## need to remove "_lit_" prefixes here.
        
        lselectorexpression = aTransform["ref"]
        lselectorsourcelist = EvaluateSelectorExpression(aSource, lselectorexpression, aScope)
        
        if "transform" in aTransform:
            # we're going to transform every selected object
            for lselectorsourceobject in lselectorsourcelist:
                if "id" in aTransform:
                    lchildscope = {}
                    lchildscope.update(aScope) # shallow clone
                    lchildscope[aTransform["id"]] = lselectorsourceobject
                else:
                    lchildscope = aScope
                
                lchildTargetList = TransformList(aSource, aTransform["transform"], lchildscope)
                ltargetlist.extend(lchildTargetList)
        else:
            # no transform, just return all the source objects we found.
            ltargetlist.extend(lselectorsourcelist)
    
    return ltargetlist

def EvaluateSelectorExpression(aSource, aSelectorExpression, aScope):
    lselectedlist = []
    
    lselectorterms = TokenizeSelectorExpression(aSelectorExpression)
    
    if lselectorterms:
        lselectedlist = EvaluateSelector(aSource, lselectorterms[0], lselectorterms[1:], aScope)
    else:
        lselectedlist.append(aSource)
        
    return lselectedlist

def EvaluateSelector(aSource, aSelectorTerm, aFollowingSelectorTerms, aScope):
    llocalselectedlist = []
    
    lselectortermtype, lselectortermvalue = ParseSelectorTerm(aSelectorTerm)
    
    if lselectortermtype == ".":
        if IsLiteralDict(aSource) and lselectortermvalue in aSource:
            llocalselectedlist.append(aSource[lselectortermvalue])
    elif lselectortermtype == ":":
        llocalselectedlist = GetObjectsByNameRecursive(aSource, lselectortermvalue)
    elif lselectortermtype == "@":
        llocalselectedlist = ApplyIndexExpressionToArray(aSource, lselectortermvalue)
    elif lselectortermtype == "!":
        if IsLiteralDict(aScope) and lselectortermvalue in aScope:
            llocalselectedlist.append(aScope[lselectortermvalue])
            
    lselectedlist = []
    if aFollowingSelectorTerms:
        lnextSelectorTerm = aFollowingSelectorTerms[0]
        lnextFollowingSelectorTerms = aFollowingSelectorTerms[1:]
        for llocalselectedobject in llocalselectedlist:
            lchildselectedlist = EvaluateSelector(llocalselectedobject, lnextSelectorTerm, lnextFollowingSelectorTerms, aScope)
            for lchildselectedobject in lchildselectedlist:
                if not lchildselectedobject in lselectedlist:
                    lselectedlist.append(lchildselectedobject)
    else:
        for llocalselectedobject in llocalselectedlist:
            if not llocalselectedobject in lselectedlist:
                lselectedlist.append(llocalselectedobject)
    
    return lselectedlist
    
def TokenizeSelectorExpression(aSelectorExpression):
    retval = re.split(r'\s+', aSelectorExpression)
    return retval

def ParseSelectorTerm(aSelectorTerm):
    lselectortermtype = None
    lselectortermvalue = None

    if aSelectorTerm:
        lselectortermtype = aSelectorTerm[0]
        lselectortermvalue = aSelectorTerm[1:]
        
    return lselectortermtype, lselectortermvalue
    
def GetObjectsByNameRecursive(aSource, aName):
    lselectedobjects = []
    
    if IsLiteralDict(aSource):
        if aName in aSource:
            lselectedobjects.append(aSource[aName])
        else:
            for lvalue in aSource.values():
                lselectedobjects.extend(GetObjectsByNameRecursive(lvalue, aName))
    elif IsLiteralArray(aSource) or IsLiteralTuple(aSource):
        if aName in aSource:
            lselectedobjects.append(aSource[aName])
        else:
            for lchild in aSource:
                lselectedobjects.extend(GetObjectsByNameRecursive(lchild, aName))
    
    return lselectedobjects

def ApplyIndexExpressionToArray(aSource, aName):
    retval = []
    try:
        lindex = int(aName)
        retval.append(aSource[lindex])
    except:
        pass
    return retval

def IsLiteralValue(aTransform):
    retval = IsLiteralString(aTransform) or \
            IsLiteralInt(aTransform) or \
            IsLiteralFloat(aTransform) or \
            IsLiteralBool(aTransform) or \
            IsLiteralNull(aTransform)
        
    return retval

def IsLiteralString(aTransform):
    retval = isinstance(aTransform, basestring)
    
    if retval:
        retval = not (aTransform[:4] == "ref=") # a string that starts with "ref=" is a SimpleRef.
    
    return retval

def IsLiteralInt(aTransform):
    retval = isinstance( aTransform, ( int, long ) )
    
    return retval

def IsLiteralFloat(aTransform):
    retval = isinstance(aTransform, float)
    
    return retval

def IsLiteralBool(aTransform):
    retval = isinstance(aTransform, bool)
    
    return retval

def IsLiteralNull(aTransform):
    retval = aTransform is None
    
    return retval

# also allow tuples here
def IsLiteralArray(aTransform):
    retval = isinstance(aTransform, list)
    
    return retval

def IsLiteralTuple(aTransform):
    retval = isinstance(aTransform, tuple)
    
    return retval

def IsLiteralDict(aTransform):
    retval = isinstance(aTransform, dict)
    
    if retval:
        retval = not "ref" in aTransform # if it has "ref" in it, then it's a complex transform
    
    return retval


def IsSimpleRef(aTransform):
    retval = isinstance(aTransform, basestring)
    
    if retval:
        retval = (aTransform[:4] == "ref=") # a string that starts with "ref=" is a SimpleRef.
    
    return retval

def IsComplexRef(aTransform):
    retval = isinstance(aTransform, dict)
    
    if retval:
        retval = "ref" in aTransform
    
    return retval

def RemoveLiteralStringPrefix(aLiteralString):
    if (aLiteralString[:4] == "lit="):
        retval = aLiteralString[4:]
    else:
        retval = aLiteralString
    return retval

def GetSelectorExpressionFromSimpleRef(aSimpleRefString):
    if (aSimpleRefString[:4] == "ref="):
        retval = aSimpleRefString[4:]
    else:
        retval = aSimpleRefString
    return retval

if __name__ == '__main__':
    print "Try running ./main.py"