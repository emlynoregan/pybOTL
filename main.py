#!/usr/bin/env python

import bOTL
import json
def Main():
    
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