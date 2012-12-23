#!/usr/bin/env python

import bOTL
import json
import sys

def Main():
    
    if len(sys.argv) >= 3:
        with open(sys.argv[1]) as fp:
            lsource = json.loads(fp.read())
        with open(sys.argv[2]) as fp:
            ltransform = json.loads(fp.read())
    else:
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
            "LastUpdate": "ref=.event .dtOccured",
            "Name": "ref=.event :name",
            "Client": {
                "key": "ref=.event .clientkey",
                "name": "ref=:clientname"       
                },
            "NameDoneInAMoreComplexWay": {
                "ref": ":detail",
                "id": "eventdetail",
                "transform": {
                    "NameAgain": "ref=!eventdetail :name"
                    }
                }
            }

    ltarget = bOTL.Transform(lsource, ltransform)
    ltargetJson = json.dumps(ltarget, indent=4)
    
    print ltargetJson

if __name__ == '__main__':
    Main()
