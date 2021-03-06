import testbotlbase

class testTransform (testbotlbase.TestBOTLBase):
        
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
                    "#>name" 
                ] 
            }
        lexpected = \
            { 
                "names": [ 
                    "george", 
                    "fred bloggs" 
                ] 
            } # need an object comparison that is tolerant of list order
        self.dobotltest(linputSource, linputTransform, lexpected)


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
                    "#>wontfindthis",
                    "#>name",
                    "#>surname" 
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
        self.dobotltest(linputSource, linputTransform, lexpected)

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
            "LastUpdate": "#.event .dtOccured",
            "Name": "#.event >name",
            "Client": {
                "key": "#.event .clientkey",
                "name": "#>clientname"     
                },
            "NameDoneInAMoreComplexWay": {
                "type": "constructor",
                "selector": ">detail",
                "scope": "eventdetail",
                "transform": {
                    "NameAgain": "#!eventdetail >name"
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
            
        self.dobotltest(linputSource, linputTransform, lexpected)

    def test4(self):
        linputSource = \
            { 
                "name": "fred bloggs", 
                "thing": [
                    {"something": "other", "surname": "goober"}, 
                    { "name": "george"},
                    { "thingo": "pink"},
                    { "stuff": "noober"},
                    { "stuff": 5}
                ] 
            }
        linputTransform = \
            { 
                "names": [ 
                    "#>thing @0 .surname",
                    "#>thingo",
                    {
                        "type": "constructor",
                        "selector": ">thing @-2:",
                        "scope": "item",
                        "transform": "#!item .stuff"
                    }
                ] 
            }
        lexpected = \
            { 
                "names": ['goober', 'pink', 'noober', 5]
            } # need an object comparison that is tolerant of list order
        self.dobotltest(linputSource, linputTransform, lexpected)

    def test5(self):

        linputSource = self.GetTwitterJson()
        
        linputTransform = \
            { 
                "urls": [
#                   "ref=:urls @:" 
                    {
                        "type": "constructor",
                        "selector": ">urls @:",
                        "scope": "x",
                        "transform": {
                                "url": "#!x >url",
                                "display_url": "#!x >display_url"
                            }
                    }
                ] 
            }
        lexpected = \
            {
                'urls': [
                    {'display_url': 'bit.ly/q9fyz9', 'url': 'http://t.co/L9JXJ2ee'},
                    {'display_url': 'dlvr.it/pfFfj', 'url': 'http://t.co/fyL8Rs5f'},
                    {'display_url': 'married2travel.com/2600/san-franc\\u2026', 'url': 'http://t.co/KfzEqOWM'}
                ]
            }

        self.dobotltest(linputSource, linputTransform, lexpected)

    def test6(self):

        linputSource = self.GetTwitterJson()
        
        linputTransform = \
            {
                "results": [
                    {
                        "type": "constructor",
                        "selector": ">results @:",
                        "scope": "r",
                        "transform": {
                            "urls": [
                                {
                                    "type": "constructor",
                                    "selector": "!r >urls @:",
                                    "scope": "u",
                                    "transform": {
                                            "url": "{{!u >url}}",
                                            "display_url": "{{!u >display_url}}",
                                            "created": "#!r .created_at",
                                            "user": "{{!r .from_user}} ({{!r .from_user_id_str}})"
                                        }
                                }
                            ]
                        }
                    }
                ] 
            }
            
        lexpected = \
            {
                "results": [
                    {
                        "urls": [
                            {
                                "url": "http://t.co/L9JXJ2ee", 
                                "display_url": "bit.ly/q9fyz9", 
                                "user": "SFist (14093707)",
                                "created": "Thu, 06 Oct 2011 19:36:17 +0000"
                            }
                        ]
                    }, 
                    {
                        "urls": []
                    }, 
                    {
                        "urls": []
                    }, 
                    {
                        "urls": []
                    }, 
                    {
                        "urls": []
                    }, 
                    {
                        "urls": []
                    }, 
                    {
                        "urls": [
                            {
                                "url": "http://t.co/fyL8Rs5f", 
                                "display_url": "dlvr.it/pfFfj", 
                                "user": "johnnyfuncheap (20717004)", 
                                "created": "Thu, 06 Oct 2011 22:38:22 +0000"
                            }
                        ]
                    }, 
                    {
                        "urls": [
                            {
                                "url": "http://t.co/KfzEqOWM", 
                                "display_url": "married2travel.com/2600/san-franc\u2026", 
                                "user": "espenorio (52736683)", 
                                "created": "Thu, 06 Oct 2011 22:37:28 +0000"
                            }
                        ]
                    }
                ]
            }

        self.dobotltest(linputSource, linputTransform, lexpected)


    def test7(self):

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
                "type": "traversal",
                "rules": [
                    {
                        "match": {"type": "string", "pattern": "^george$"},
                        "scope": "g",
                        "transform": {
                            "First Name": "#!g",
                            "Last Name": "{{!g}}son",
                            "Url": "http://{{!g}}.example.com",
                            "{{!g}}thing": "thingo"
                        }
                    }
                ]
            }
            
        lexpected = \
            { 
                "name": "fred bloggs", 
                "thing": [
                    {"something": "other"}, 
                    { 
                        "name": {
                            "First Name": "george",
                            "Last Name": "georgeson",
                            "Url": "http://george.example.com",
                            "georgething": "thingo"
                        }
                    }
                ] 
            }

        self.dobotltest(linputSource, linputTransform, lexpected)

    def test8(self):
        linputSource = \
            {
               "publicassessmentdefinition":{
                  "key":"bc22ed67-c1c2-4415-2999-9ef6c7d0180e-pub"
               }
            }        
    
        linputTransform = \
            {
              "type": "traversal",
              "rules": [
                {
                  "keymatch": "publicassessmentdefinition",
                  "delete": True
                }
              ]
            }            
    
        lexpected = \
            { 
            }
    
        self.dobotltest(linputSource, linputTransform, lexpected)


    def GetTwitterJson(self):
        return \
{
  "completed_in":0.031,
  "max_id":122078461840982016,
  "max_id_str":"122078461840982016",
  "next_page":"?page=2&max_id=122078461840982016&q=blue%20angels&rpp=5",
  "page":1,
  "query":"blue+angels",
  "refresh_url":"?since_id=122078461840982016&q=blue%20angels",
  "results":[
    {
      "created_at":"Thu, 06 Oct 2011 19:36:17 +0000",
      "entities":{
        "urls":[
          {
            "url":"http://t.co/L9JXJ2ee",
            "expanded_url":"http://bit.ly/q9fyz9",
            "display_url":"bit.ly/q9fyz9",
            "indices":[
              37,
              57
            ]
          }
        ]
      },
      "from_user":"SFist",
      "from_user_id":14093707,
      "from_user_id_str":"14093707",
      "geo":None,
      "id":122032448266698752,
      "id_str":"122032448266698752",
      "iso_language_code":"en",
      "metadata":{
        "recent_retweets":3,
        "result_type":"popular"
      },
      "profile_image_url":"http://a3.twimg.com/profile_images/51584619/SFist07_normal.jpg",
      "source":"&lt;a href=&quot;http://twitter.com/tweetbutton&quot; rel=&quot;nofollow&quot;&gt;Tweet Button&lt;/a&gt;",
      "text":"Reminder: Blue Angels practice today http://t.co/L9JXJ2ee",
      "to_user_id":None,
      "to_user_id_str":None
    },
    {
      "created_at":"Thu, 06 Oct 2011 19:41:12 +0000",
      "entities":{
 
      },
      "from_user":"masters212",
      "from_user_id":2242041,
      "from_user_id_str":"2242041",
      "geo":None,
      "id":122033683212419072,
      "id_str":"122033683212419072",
      "iso_language_code":"en",
      "metadata":{
        "recent_retweets":1,
        "result_type":"popular"
      },
      "profile_image_url":"http://a3.twimg.com/profile_images/488532540/rachel25final_normal.jpg",
      "source":"&lt;a href=&quot;http://twitter.com/&quot;&gt;web&lt;/a&gt;",
      "text":"Starting to hear Blue Angels... Not such angels with all of the noise and carbon pollution.",
      "to_user_id":None,
      "to_user_id_str":None
    },
    {
      "created_at":"Thu, 06 Oct 2011 19:39:52 +0000",
      "entities":{
 
      },
      "from_user":"SFBayBridge",
      "from_user_id":182107587,
      "from_user_id_str":"182107587",
      "geo":None,
      "id":122033350327279617,
      "id_str":"122033350327279617",
      "iso_language_code":"en",
      "metadata":{
        "recent_retweets":1,
        "result_type":"popular"
      },
      "profile_image_url":"http://a0.twimg.com/profile_images/1162882917/bbtwitternew_normal.jpg",
      "source":"&lt;a href=&quot;http://twitter.com/&quot;&gt;web&lt;/a&gt;",
      "text":"BZZZzzzZzZzzzZZZZZzZz WHAT? I CAN'T HEAR YOU. THERE ARE BLUE ANGELS. ZZZzzZZZ!",
      "to_user_id":None,
      "to_user_id_str":None
    },
    {
      "created_at":"Thu, 06 Oct 2011 22:39:08 +0000",
      "entities":{
 
      },
      "from_user":"OnDST",
      "from_user_id":265656068,
      "from_user_id_str":"265656068",
      "geo":None,
      "id":122078461840982016,
      "id_str":"122078461840982016",
      "iso_language_code":"nl",
      "metadata":{
        "result_type":"recent"
      },
      "profile_image_url":"http://a3.twimg.com/profile_images/1271597598/OnDST_normal.jpg",
      "source":"&lt;a href=&quot;http://dlvr.it&quot; rel=&quot;nofollow&quot;&gt;dlvr.it&lt;/a&gt;",
      "text":"SF Fleet Week to open with Blue Angels flyovers | Student ...",
      "to_user_id":None,
      "to_user_id_str":None
    },
    {
      "created_at":"Thu, 06 Oct 2011 22:38:51 +0000",
      "entities":{
 
      },
      "from_user":"gusbumper",
      "from_user_id":15912539,
      "from_user_id_str":"15912539",
      "geo":None,
      "id":122078393641603072,
      "id_str":"122078393641603072",
      "iso_language_code":"en",
      "metadata":{
        "result_type":"recent"
      },
      "profile_image_url":"http://a2.twimg.com/profile_images/832286946/pho_normal.jpg",
      "source":"&lt;a href=&quot;http://itunes.apple.com/us/app/twitter/id409789998?mt=12&quot; rel=&quot;nofollow&quot;&gt;Twitter for Mac&lt;/a&gt;",
      "text":"RT @gzahnd: WAKE UP HIPPIES, THE BLUE ANGELS ARE IN TOWN!",
      "to_user_id":None,
      "to_user_id_str":None
    },
    {
      "created_at":"Thu, 06 Oct 2011 22:38:31 +0000",
      "entities":{
 
      },
      "from_user":"LUVTQUILT",
      "from_user_id":32653550,
      "from_user_id_str":"32653550",
      "geo":None,
      "id":122078309004742656,
      "id_str":"122078309004742656",
      "iso_language_code":"en",
      "metadata":{
        "result_type":"recent"
      },
      "profile_image_url":"http://a1.twimg.com/profile_images/1188428056/IMG00007-20100521-1647_1__normal.jpg",
      "source":"&lt;a href=&quot;http://ubersocial.com&quot; rel=&quot;nofollow&quot;&gt;\u00DCberSocial for BlackBerry&lt;/a&gt;",
      "text":"Thursday - Just watched the Blue Angels practice over SF Bay Impressive! What a background.  GGB & Alcatraz. ;) .",
      "to_user_id":None,
      "to_user_id_str":None
    },
    {
      "created_at":"Thu, 06 Oct 2011 22:38:22 +0000",
      "entities":{
        "urls":[
          {
            "url":"http://t.co/fyL8Rs5f",
            "expanded_url":"http://dlvr.it/pfFfj",
            "display_url":"dlvr.it/pfFfj",
            "indices":[
              52,
              72
            ]
          }
        ]
      },
      "from_user":"johnnyfuncheap",
      "from_user_id":20717004,
      "from_user_id_str":"20717004",
      "geo":None,
      "id":122078271478317056,
      "id_str":"122078271478317056",
      "iso_language_code":"en",
      "metadata":{
        "result_type":"recent"
      },
      "profile_image_url":"http://a0.twimg.com/profile_images/1130541908/funcheap_icon_twitter_normal.gif",
      "source":"&lt;a href=&quot;http://dlvr.it&quot; rel=&quot;nofollow&quot;&gt;dlvr.it&lt;/a&gt;",
      "text":"10/8/11: Blue Angels Wine Tasting | Treasure Island http://t.co/fyL8Rs5f",
      "to_user_id":None,
      "to_user_id_str":None
    },
    {
      "created_at":"Thu, 06 Oct 2011 22:37:28 +0000",
      "entities":{
        "urls":[
          {
            "url":"http://t.co/KfzEqOWM",
            "expanded_url":"http://married2travel.com/2600/san-francisco-day3-golden-gate-park-pier-39-blue-angels/",
            "display_url":"married2travel.com/2600/san-franc\u2026",
            "indices":[
              47,
              67
            ]
          }
        ]
      },
      "from_user":"espenorio",
      "from_user_id":52736683,
      "from_user_id_str":"52736683",
      "geo":None,
      "id":122078043664695296,
      "id_str":"122078043664695296",
      "iso_language_code":"en",
      "metadata":{
        "result_type":"recent"
      },
      "profile_image_url":"http://a0.twimg.com/profile_images/1574863913/sheil_normal.png",
      "source":"&lt;a href=&quot;http://twitter.com/&quot;&gt;web&lt;/a&gt;",
      "text":"San Francisco 2010 Fleet week photos and video http://t.co/KfzEqOWM",
      "to_user_id":None,
      "to_user_id_str":None
    }
  ],
  "results_per_page":5,
  "since_id":0,
  "since_id_str":"0"
}

