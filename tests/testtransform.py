import unittest
import bOTL

class testTransform (unittest.TestCase):
	def dotest(self, aInputSource, aInputTransform, aExpected):
		loutput = bOTL.Transform(aInputSource, aInputTransform)
		
		if aExpected is None:
			self.assertIsNone(loutput)
		else:
			self.assertEqual(aExpected, loutput)
		
	def test1(self):
		linputSource = \
			{ 
				"name": "fred bloggs", 
				"thing": [
					{"something": "other"}, 
					{ "name": "george"}
				] 
			}
		linputTransform = \
			{ 
				"names": [ 
					"ref=:name" 
				] 
			}
		lexpected = \
			{ 
				"names": [ 
					"george", 
					"fred bloggs" 
				] 
			} # need an object comparison that is tolerant of list order
		self.dotest(linputSource, linputTransform, lexpected)


	def test2(self):
		linputSource = \
			{ 
				"name": "fred bloggs", 
				"thing": [
					{"something": "other", "surname": "goober"}, 
					{ "name": "george"}
				] 
			}
		linputTransform = \
			{ 
				"names": [ 
					"ref=:wontfindthis",
					"ref=:name",
					"ref=:surname" 
				] 
			}
		lexpected = \
			{ 
				"names": [ 
					"george", 
					"fred bloggs",
					"goober" 
				] 
			} # need an object comparison that is tolerant of list order
		self.dotest(linputSource, linputTransform, lexpected)

	def test3(self):
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
		
		linputSource = \
			{
			"event": levent,
			"client": lclient
			}
			
		linputTransform = \
			{
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

		lexpected = \
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
			
		self.dotest(linputSource, linputTransform, lexpected)
