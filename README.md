pybOTL
=======

This is the Python reference implementation of bOTL. 

You can use bOTL in your code by simply including the file bOTL.py . Have a look at main.py for an example of how to use it (and find more detail in the tests).

The spec of bOTL is included below (currently incomplete).

But here's an example of its use:

    levent = {
        "key": "key1",
        "type": "new user",
        "dtOccured": 12345678,
        "assertingprincipalkey": "key2",
        "detail": {
            "key": "key3",
            "name": "Fred Bloggs"
            },
        "clientkey": "key4",
        }
    
    lclient = {
        "key": "key4",
        "clientname": "thingco"
        }
    
    lsource = {
        "event": levent,
        "client": lclient
        }
    
    ltransform = {
        "Type": "Person",
        "LastUpdate": "#.event .dtOccured",
        "Name": "#.event >name",
        "Client": {
            "key": "#.event .clientkey",
            "name": "#>clientname"       
            },
        "NameDoneInAMoreComplexWay": {
            "ref": ">detail",
            "id": "eventdetail",
            "transform": {
                "NameAgain": "#!eventdetail >name"
                }
            }
        }

    ltarget = bOTL.Transform(lsource, ltransform)
    ltargetJson = json.dumps(ltarget, indent=4)
    
    print ltargetJson

Here's the result:

	{
	    "LastUpdate": 12345678, 
	    "NameDoneInAMoreComplexWay": {
	        "NameAgain": "Fred Bloggs"
	    }, 
	    "Client": {
	        "name": "thingco", 
	        "key": "key4"
	    }, 
	    "Type": "Person", 
	    "Name": "Fred Bloggs"
	}


# bOTL Object Transformation Language

revision 0.2

This language is a subset of JSON. Its purpose is to define transformations on objects made up of combinations of simple values, lists and dictionaries, to other such objects.

See the June 30 2012 revision for the previous, quite different version.

## Objects

For purposes of bOTL, an object is a combination of simple values, lists (sequences, arrays) and dictionaries (maps, hashes, javascript objects).

Object: Single | List | Dictionary

Single: Instances of any one of a list of simple types. Boolean, Integer, Float, String, and the special value null.

List: A list/array/sequence of Object

Dictionary: A set of string “Keys”, each paired with a Value. Values are Objects.

This kind of structure appears especially in many dynamic languages, and is the object structure that “stringifies” to JSON, and what JSON is parsed into.

## Transforms

A bOTL Transform is itself specified in a subset of the Object format above. The best format for interchange will be as JSON, but technically it can be specified in anything that can be transformed to the appropriate Object structure. Throughout this document Python Literal Notation is used.

Transform: Literal Value | Literal Array | Literal Dict | Simple Selector | Complex Selector

Transformations are performed as follows:

    import bOTL
    
    source = ... some object ...
    transform = ... some transform ...
    
    target = bOTL.Transform(source, transform)

### Literal Value

    Literal Value: literal string | “lit=” + literal string | literal int | literal float | literal bool | null

The simplest transform is a literal value. It produces this literal value no matter what input is provided.

eg: 

    >>> import bOTL
    >>> source = { "thing": "something" }
    >>> transform = 5
    >>> print bOTL.Transform(source, transform)
    5

The "lit=" notation is an escape notation; it allows you to have a literal string beginning with a hash, without it being mistaken for a selector.

eg:

    >>> import bOTL
    >>> source = { "thing": "something" }
    >>> transform = "lit=#.thing"
    >>> print bOTL.Transform(source, transform)
    #.thing

### Literal Array

    Literal Array: List of Transform 
      # in JSON or Python literal notation this would be “[“ [ Transform { “,” Transform } ] “]” 

A literal array is reproduced in the output. Note that its elements are treated recursively as Transforms.

eg:

    >>> import bOTL
    >>> source = { "thing": "something" }
    >>> transform = [5, "lit=#.thing", "#.thing"]
    >>> print bOTL.Transform(source, transform)
    [5, '#.thing', 'something']

Note that the third element in the example uses a simple selector, which operates on the source object, and is explained below.

### Literal Dict

    Literal Dict: Dict of key=Literal String, value=Transform pairs. If any key is prepended with “__lit__” then that is removed when calculating the transform (see Evaluation below).
    
A literal dictionary is reproduced in the output. Note that its keys are literal strings, and values are Transforms.

eg:

    >>> import bOTL
    >>> source = { "thing": "something" }
    >>> transform = { "newthing": "#.thing" }
    >>> print bOTL.Transform(source, transform)
    {'newthing': 'something'}
    
Any dictionary which is a valid Complex Selector (see below) is not a literal dictionary. Use the "__lit__" escape notation on the key "ref" (ie: "__lit__ref") if you wish to force the dictionary to be considered a literal dictionary and not a complex selector.

### Selector Expression

Selector Expressions are used by Simple Selectors and Complex Selectors, described below.

A Selector Expression is a way of selecting a list of elements from the source.

Selector Expressions are structured as a list of Selector Atoms, separated by ' ' (space). 

    Selector Expression: [ Selector Atom { ' '  Selector Atom } ]
    
Selector atoms are the atomic units of selection in a selector expression. 

A selector atom operates on a list of elements (references into the source), and returns another list of elements (references into the source.

The selector atom is applied to each element in the input list, in order, and the elements of the resulting list (a selector atom can return multiple results) are added to the output list, unless any value already appears in the output list (in which case it is discarded). 

eg: if a selector atom returns [4, 5, 6] and the output list already contains 5, then the 4 will be appended, the 5 will not be (already in the list), the 6 will be appended, resulting in [5, 4, 6].

The leftmost selector atom in a selector list operates on a single element list, containing the root of the source.

Each other selector atom operates on the output of the selector atom to the left, and provides its output to the selector atom to the right.

The output of the rightmost selector atom is the output of the selector expression.

If there are no selector atoms, the identity transform is performed (ie: output is input).

#### Allowed Selector Atoms

* "." keyname: If the input is a dict, and has a key "keyname", then the result list is a single element list containing the value of that key. Otherwise it is the empty list.
* ">" keyname: Traverse the input recursively. Anywhere a key "keyname" is found in a dictionary, the value is added to the result list. Empty list if none are found.
* "!" scopevar: Complex selectors can tie a scope variable to a position in the source. This atom disregards its input, and instead returns a list containing just the value of the scope variable scopevar. If there is no such variable, it returns the empty list.
* "@" slice: If the input is not an array, returns the empty list. If it is an array, it evaluates the specified slice (python array slice notation) and returns that list.

eg: ".first .second >third" is a selector expression. The selector atoms beginning with "." mean we are expecting dictionaries as inputs, looking for keys with the name provided after the ".", and returning the values of those keys, or nothing if there is no such key. The ">" at the front of the last selector atom says we want to recursively search for the key "third".

Given the source {"first": {"second": {"third": 3, "x":{"third": "three", "last": 99}}}}, we evaluate the selector expression as follows.

    Selector 0: ".first"
    Input = [ {"first": {"second": {"third": 3, "x":{"third": "three", "last": 99}}}} ]  <- a list containing the source
    Output = [ {"second": {"third": 3, "x":{"third": "three", "last": 99}}} ] <- the value of "first"
    
    Selector 1: ".second"
    Input = [ {"second": {"third": 3, "x":{"third": "three", "last": 99}}} ]
    Output = [ {"third": 3, "x":{"third": "three", "last": 99}} ] <- the value of "second"

    Selector 3: ">third"
    Input = [ {"third": 3, "x":{"third": "three", "last": 99}} ] 
    Output = [ "three", 3 ] <- the values of "third" in both places where it appears.

So Selector Expressions always evaluate to a list, even if that list has zero elements. 

### Selectors

Selectors evaluate a selector expression, and do something with the results. If the selector appears inside a literal array, then the elements of the result list will be appended to the literal array in the target, in order. However, if the containing selector appears anywhere else, then if the list is empty the result returned is null, otherwise it is element zero. 

Selectors come in two forms: Simple and Complex.

### Simple Selector
 
    Simple Selector: String, “#” + Selector Expression

A simple selector is a string; a '#' followed by a selector expression.

The simple selector is evaluated by evaluating the selector expression (as above) and returning either the first element, or appending all elements into an array, depending on context (see Selectors above).

eg 1: The transform below is at the root level (ie: the result is not inside a literal array). So only one element is returned.

    >>> source={"first": {"second": {"third": 3, "x":{"third": "three", "last": 99}}}}
    >>> transform="#.first .second >third"
    >>> print bOTL.Transform(source, transform)
    three

eg 2: The transform below is inside a literal array. So all elements selected are returned as elements of that array.

    >>> source={"first": {"second": {"third": 3, "x":{"third": "three", "last": 99}}}}
    >>> transform=[ "a", "#.first .second >third", "b" ]
    >>> print bOTL.Transform(source, transform)
    ['a', 'three', 3, 'b']

The Simple Selector "#" is the identity transform.

### Complex Selector

    Complex Selector: Dict containing the following key / value pairs:
  	key=”ref”, value=String, Selector Expression (required)
	key=”id”, value=String, Scope Variable name (optional)
	key=”transform”, value=Transform, optional. If omitted, an identity transform is performed.

The purpose of a complex selector is to apply a selector expression, but where a simple selector simply returns the output of the expression, a complex selector applies a given transform to each element of the output of the selector expression, and returns the flattened result of all these transforms.

A complex selector is a dict, with a triple of "ref", "id" and "transform".

The value of "ref" is the selector expression as a string. Note: do not use a leading "#".

The value of "id", if present, is a scope variable name. That name is available inside the transform, as a scope variable, relating to the element being transformed.

The value of "transform" is the transform to apply to each elemented selected by the selector expression. If not present, the identity transform is used.

So, 
    "#.thing" 
    
is equivalent to

    {
        "ref": ".thing"
    }

eg: The transform below returns all elements as in the simple selector examples above, but wraps each element in its own dict { "value": ... }

    >>> source={"first": {"second": {"third": 3, "x":{"third": "three", "last": 99}}}}
    >>> transform=[ "a", { "ref": ".first .second >third", "id": "elem", "transform": { "value": "#!elem" } }, "b" ]
    >>> print bOTL.Transform(source, transform)
    ['a', {'value': 'three'}, {'value': 3}, 'b']

