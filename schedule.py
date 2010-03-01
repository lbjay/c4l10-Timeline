#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from rdflib import ConjunctiveGraph, Literal, URIRef
import lxml
import datetime
from time import mktime
import namespaces as ns

base_uri = 'http://irc.code4lib.org/'

#g = rdflib.ConjunctiveGraph('Sleepycat')
#g.open('store', create=True)

events = [
    ('Registration / coffee', 
     datetime.datetime(2010, 2, 22, 8, 0),
     datetime.datetime(2010, 2, 22, 9, 0), None),
    ('Morning Sessions', 
     datetime.datetime(2010, 2, 22, 9, 0),
     datetime.datetime(2010, 2, 22, 12, 0), None),
    ('Lunch (on your own)', 
     datetime.datetime(2010, 2, 22, 12, 0),
     datetime.datetime(2010, 2, 22, 13, 30), None),
    ('Afternoon Sessions', 
     datetime.datetime(2010, 2, 22, 13, 30),
     datetime.datetime(2010, 2, 22, 16, 30), None),

    ('Registration / Breakfast',
     datetime.datetime(2010, 2, 23, 8, 0),
     datetime.datetime(2010, 2, 23, 9, 0), None),
    ('Orientation / Housekeeping',
     datetime.datetime(2010, 2, 23, 9, 0),
     datetime.datetime(2010, 2, 23, 9, 15), None),
    ('Keynote #1: Cathy Marshall',
     datetime.datetime(2010, 2, 23, 9, 15),
     datetime.datetime(2010, 2, 23, 10, 0),
     '/conference/2010/marshall'),
    ('Cloud4Lib',
     datetime.datetime(2010, 2, 23, 10, 0),
     datetime.datetime(2010, 2, 23, 10, 20),
     '/conference/2010/frumkin_reese'),
    ('The Linked Library Data Cloud: Stop talking and start doing',
     datetime.datetime(2010, 2, 23, 10, 20),
     datetime.datetime(2010, 2, 23, 10, 40),
     '/conference/2010/singer'),
    ('Break',
     datetime.datetime(2010, 2, 23, 10, 40),
     datetime.datetime(2010, 2, 23, 11, 0), None),
    ('Do It Yourself Cloud Computing with Apache and R',
     datetime.datetime(2010, 2, 23, 11, 0),
     datetime.datetime(2010, 2, 23, 11, 20),
     '/conference/2010/dekker'),
    ('Public Datasets in the Cloud',
     datetime.datetime(2010, 2, 23, 11, 20),
     datetime.datetime(2010, 2, 23, 11, 40),
     '/conference/2010/klien_metz'),
    ('7 Ways to Enhance Library Interfaces with OCLC Web Services',
     datetime.datetime(2010, 2, 23, 11, 40),
     datetime.datetime(2010, 2, 23, 12, 0),
     '/conference/2010/frumkin_reese'),
    ('Lunch',
     datetime.datetime(2010, 2, 23, 12, 0),
     datetime.datetime(2010, 2, 23, 13, 0), None),
    ('Taking Control of Library Metadata and Websites Using the eXtensible Catalog',
     datetime.datetime(2010, 2, 23, 13, 0),
     datetime.datetime(2010, 2, 23, 13, 20),
     '/conference/2010/bowen'),
    (u'Matching Dirty Data – Yet Another Wheel',
     datetime.datetime(2010, 2, 23, 13, 20),
     datetime.datetime(2010, 2, 23, 13, 40),
     '/conference/2010/young_sherwood'),
    ('HIVE: A New Tool for Working With Vocabularies',
     datetime.datetime(2010, 2, 23, 13, 40),
     datetime.datetime(2010, 2, 23, 14, 0),
     '/conference/2010/scherle_aguera'),
    ('Metadata Editing – A Truly Extensible Solution',
     datetime.datetime(2010, 2, 23, 14, 0),
     datetime.datetime(2010, 2, 23, 14, 20),
     '/conference/2010/kennedy_chandek-stark'),
    ('Break',
     datetime.datetime(2010, 2, 23, 14, 20),
     datetime.datetime(2010, 2, 23, 14, 40), None),
    ('Lightning Talks 1',
     datetime.datetime(2010, 2, 23, 14, 40),
     datetime.datetime(2010, 2, 23, 15, 50), None),
    ('Breakout Sessions 1',
     datetime.datetime(2010, 2, 23, 15, 50),
     datetime.datetime(2010, 2, 23, 17, 0), None),
    ('Daily Wrap Up',
     datetime.datetime(2010, 2, 23, 17, 0),
     datetime.datetime(2010, 2, 23, 17, 15), None),

    ('Breakfast',
     datetime.datetime(2010, 2, 24, 8, 0),
     datetime.datetime(2010, 2, 24, 9, 0), None),
    ('Housekeeping / Intros',
     datetime.datetime(2010, 2, 24, 9, 0),
     datetime.datetime(2010, 2, 24, 9, 15), None),
    ('Iterative Development Done Simply',
     datetime.datetime(2010, 2, 24, 9, 15),
     datetime.datetime(2010, 2, 24, 9, 35),
     '/conference/2010/lynema'),
    ('Vampires vs. Werewolves: Ending the War Between Developers and Sysadmins with Puppet',
     datetime.datetime(2010, 2, 24, 9, 35),
     datetime.datetime(2010, 2, 24, 9, 55),
     '/conference/2010/sadler'),
    ('I Am Not Your Mother: Write Your Test Code',
     datetime.datetime(2010, 2, 24, 9, 55),
     datetime.datetime(2010, 2, 24, 10, 15),
     '/conference/2010/dushay_mene_keck'),
    ('Break',
     datetime.datetime(2010, 2, 24, 10, 15),
     datetime.datetime(2010, 2, 24, 10, 35), None),
    ('Media, Blacklight, and Viewers Like You',
     datetime.datetime(2010, 2, 24, 10, 35),
     datetime.datetime(2010, 2, 24, 10, 55),
     '/conference/2010/beer'),
    ('Becoming Truly Innovative: Migrating from Millennium to Koha',
     datetime.datetime(2010, 2, 24, 10, 55),
     datetime.datetime(2010, 2, 24, 11, 15),
     '/conference/2010/beer'),
    ('Ask Anything!',
     datetime.datetime(2010, 2, 24, 11, 15),
     datetime.datetime(2010, 2, 24, 12, 0),
     '/conference/2010/chudnov'),
    ('Lunch',
     datetime.datetime(2010, 2, 24, 12, 0),
     datetime.datetime(2010, 2, 24, 13, 0), None),
    ('A Better Advanced Search',
     datetime.datetime(2010, 2, 24, 13, 0),
     datetime.datetime(2010, 2, 24, 13, 20),
     '/conference/2010/dushay_keck'),
    ('Drupal 7: A more powerful platform for building library applications',
     datetime.datetime(2010, 2, 24, 13, 20),
     datetime.datetime(2010, 2, 24, 13, 40),
     '/conference/2010/gordon'),
    ('Enhancing Discoverability With Virtual Shelf Browse',
     datetime.datetime(2010, 2, 24, 13, 40),
     datetime.datetime(2010, 2, 24, 14, 0),
     '/conference/2010/orphanides_lown_lynema'),
    ('How to Implement A Virtual Bookshelf With Solr',
     datetime.datetime(2010, 2, 24, 14, 0),
     datetime.datetime(2010, 2, 24, 14, 20),
     '/conference/2010/dushay_keck'),
    ('Break',
     datetime.datetime(2010, 2, 24, 14, 20),
     datetime.datetime(2010, 2, 24, 14, 40), None),
    ('Lightning Talks 2',
     datetime.datetime(2010, 2, 24, 14, 40),
     datetime.datetime(2010, 2, 24, 15, 50), None),
    ('Breakout Sessions 2',
     datetime.datetime(2010, 2, 24, 15, 50),
     datetime.datetime(2010, 2, 24, 17, 0), None),
    ('Daily Wrap Up',
     datetime.datetime(2010, 2, 24, 17, 0),
     datetime.datetime(2010, 2, 24, 17, 15), None),

    ('Breakfast',
     datetime.datetime(2010, 2, 25, 8, 0),
     datetime.datetime(2010, 2, 25, 9, 0), None),
    ('Housekeeping',
     datetime.datetime(2010, 2, 25, 9, 0),
     datetime.datetime(2010, 2, 25, 9, 15), None),
    ('Keynote #2: Paul Jones',
     datetime.datetime(2010, 2, 25, 9, 15),
     datetime.datetime(2010, 2, 25, 10, 0),
     '/conference/2010/marshall'),
    ('Break',
     datetime.datetime(2010, 2, 25, 10, 0),
     datetime.datetime(2010, 2, 25, 10, 15), None),
    ('Lightning Talks 3',
     datetime.datetime(2010, 2, 25, 10, 15),
     datetime.datetime(2010, 2, 25, 11, 0), None),
    ('You Either Surf or You Fight: Integrating Library Services With Google Wave',
     datetime.datetime(2010, 2, 25, 11, 0),
     datetime.datetime(2010, 2, 25, 11, 20),
     '/conference/2010/hannan'),
    ('library/mobile: Developing a Mobile Catalog',
     datetime.datetime(2010, 2, 25, 11, 20),
     datetime.datetime(2010, 2, 25, 11, 40),
     '/conference/2010/griggs'),
    ('Mobile Web App Design: Getting Started',
     datetime.datetime(2010, 2, 25, 11, 40),
     datetime.datetime(2010, 2, 25, 12, 0),
     '/conference/2010/doran'),
    ('Wrap-Up',
     datetime.datetime(2010, 2, 25, 12, 0),
     datetime.datetime(2010, 2, 25, 12, 15), None),
]

c4l_base_uri = 'http://code4lib.org'
c4l_sched_uri = 'http://code4lib.org/conference/2010/schedule'

if __name__ == '__main__':
    g = ConjunctiveGraph()
    ns.bind_graph(g)
    for (title, start, end, uri) in events:

        if uri:
            talkid = URIRef(uri, base=c4l_base_uri)
            event_type = ns.swc.TalkEvent
        else:
            talkid = URIRef("%s#%s" % (c4l_sched_uri, title.replace(' ', '_')))
            if title == 'Break':
                event_type = ns.swc.BreakEvent
            elif title in ['Lunch', 'Breakfast']:
                event_type = ns.swc.MealEvent
            elif title.startswith('Lightnight'):
                event_type = ns.swc.TalkEvent
            else:
                event_type = ns.swc.OrganizedEvent

        startseconds = int(mktime(start.timetuple()))
        endseconds = int(mktime(end.timetuple()))
        start = Literal(startseconds, datatype=ns.xsd.int)
        end = Literal(endseconds, datatype=ns.xsd.int)
        title = Literal(title)
        print (talkid, start, end, title)

#        g.add((talkid, rdfs.type, event_type))
#        g.add((talkid, rdfs.type, ical.Vevent))
#        g.add((talkid, dce.title, title))
#        g.add((

            



    


    
