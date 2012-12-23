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

A bOTL Transform is itself specified in a subset of the Object format above. The best format for interchange will be as JSON, but technically it can be specified in anything that can be transformed to the appropriate Object structure (for example, Python literal notation).

Transform: Literal Value | Literal Array | Literal Dict | Simple Ref | Complex Ref

Literal Value: literal string | “lit=” + literal string | literal int | literal float | literal bool | null

Literal Array: List of Transform   # in JSON this would be “[“ [ Transform { “,” Transform } ] “]” 

Literal Dict: Dict of key=Literal String, value=Transform pairs. If any key is prepended with “__lit__” then that is removed when calculating the transform (see Evaluation below).
 
Simple Selector: String: “#” + Selector Expression

Complex Selector: Dict containing the following key / value pairs:
  	key=”ref”, value=Selector Expression, required.
	key=”id”, value=simple string, optional, an id which can be used to refer to an element selected by this expression (see Evaluation below). 
	key=”transform”, value=Transform, optional. If omitted, an identity transform is performed.

Selector Expression: Selector Term { “ “ Selector Term }

Selector Term: # below, “name” is a literal string.
“.” name   # selects the value for the name from the current level.
“>” name   # selects all values for the name from the current level or below, recursive
“@” index expr  # selects all values from the current level list. Index expr uses python array slice notation
“!” id  # selects the object given the id “id” by a containing Complex Selector.

