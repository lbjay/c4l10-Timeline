#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from rdflib import ConjunctiveGraph, Literal, URIRef
import lxml
import datetime
from time import mktime

import namespaces as ns
from graphstore import g

base_uri = 'http://irc.code4lib.org/'

events = [
    ('Registration / coffee', 
     ns.swc.MealEvent,
     datetime.datetime(2010, 2, 22, 8, 0),
     datetime.datetime(2010, 2, 22, 9, 0), 
     'preconf_coffee'),
    ('Morning Sessions', 
     ns.swc.OrganizedEvent,
     datetime.datetime(2010, 2, 22, 9, 0),
     datetime.datetime(2010, 2, 22, 12, 0), 
     'preconf_morning'),
    ('Lunch (on your own)', 
     ns.swc.MealEvent,
     datetime.datetime(2010, 2, 22, 12, 0),
     datetime.datetime(2010, 2, 22, 13, 30), 
     'preconf_lunch'),
    ('Afternoon Sessions', 
     ns.swc.OrganizedEvent,
     datetime.datetime(2010, 2, 22, 13, 30),
     datetime.datetime(2010, 2, 22, 16, 30), 
     'preconf_afternoon'),

    ('Registration / Breakfast',
     ns.swc.MealEvent,
     datetime.datetime(2010, 2, 23, 8, 0),
     datetime.datetime(2010, 2, 23, 9, 0), 
     'breakfast_day1'),
    ('Orientation / Housekeeping',
     ns.swc.OrganizedEvent,
     datetime.datetime(2010, 2, 23, 9, 0),
     datetime.datetime(2010, 2, 23, 9, 15), 
     'intro_day1'),
    ('Keynote #1: Cathy Marshall',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 23, 9, 15),
     datetime.datetime(2010, 2, 23, 10, 0),
     'marshall'),
    ('Cloud4Lib',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 23, 10, 0),
     datetime.datetime(2010, 2, 23, 10, 20),
     'frumkin_reese'),
    ('The Linked Library Data Cloud: Stop talking and start doing',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 23, 10, 20),
     datetime.datetime(2010, 2, 23, 10, 40),
     'singer'),
    ('Break',
     ns.swc.BreakEvent,
     datetime.datetime(2010, 2, 23, 10, 40),
     datetime.datetime(2010, 2, 23, 11, 0), 
     'break1_day1'),
    ('Do It Yourself Cloud Computing with Apache and R',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 23, 11, 0),
     datetime.datetime(2010, 2, 23, 11, 20),
     'dekker'),
    ('Public Datasets in the Cloud',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 23, 11, 20),
     datetime.datetime(2010, 2, 23, 11, 40),
     'klien_metz'),
    ('7 Ways to Enhance Library Interfaces with OCLC Web Services',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 23, 11, 40),
     datetime.datetime(2010, 2, 23, 12, 0),
     'frumkin_reese'),
    ('Lunch',
     ns.swc.MealEvent,
     datetime.datetime(2010, 2, 23, 12, 0),
     datetime.datetime(2010, 2, 23, 13, 0), 
     'lunch_day1'),
    ('Taking Control of Library Metadata and Websites Using the eXtensible Catalog',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 23, 13, 0),
     datetime.datetime(2010, 2, 23, 13, 20),
     'bowen'),
    (u'Matching Dirty Data – Yet Another Wheel',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 23, 13, 20),
     datetime.datetime(2010, 2, 23, 13, 40),
     'young_sherwood'),
    ('HIVE: A New Tool for Working With Vocabularies',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 23, 13, 40),
     datetime.datetime(2010, 2, 23, 14, 0),
     'scherle_aguera'),
    ('Metadata Editing – A Truly Extensible Solution',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 23, 14, 0),
     datetime.datetime(2010, 2, 23, 14, 20),
     'kennedy_chandek-stark'),
    ('Break',
     ns.swc.BreakEvent,
     datetime.datetime(2010, 2, 23, 14, 20),
     datetime.datetime(2010, 2, 23, 14, 40), 
     'break2_day1'),
    ('Lightning Talks 1',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 23, 14, 40),
     datetime.datetime(2010, 2, 23, 15, 50), 
     'ltalks_day1'),
    ('Breakout Sessions 1',
     ns.swc.OrganizedEvent,
     datetime.datetime(2010, 2, 23, 15, 50),
     datetime.datetime(2010, 2, 23, 17, 0), 
     'breakout_day1'),
    ('Daily Wrap Up',
     ns.swc.OrganizedEvent,
     datetime.datetime(2010, 2, 23, 17, 0),
     datetime.datetime(2010, 2, 23, 17, 15), 
     'wrapup_day1'),

    ('Breakfast',
     ns.swc.MealEvent,
     datetime.datetime(2010, 2, 24, 8, 0),
     datetime.datetime(2010, 2, 24, 9, 0), 
     'breakfast_day2'),
    ('Housekeeping / Intros',
     ns.swc.OrganizedEvent,
     datetime.datetime(2010, 2, 24, 9, 0),
     datetime.datetime(2010, 2, 24, 9, 15), 
     'intro_day2'),
    ('Iterative Development Done Simply',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 24, 9, 15),
     datetime.datetime(2010, 2, 24, 9, 35),
     'lynema'),
    ('Vampires vs. Werewolves: Ending the War Between Developers and Sysadmins with Puppet',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 24, 9, 35),
     datetime.datetime(2010, 2, 24, 9, 55),
     'sadler'),
    ('I Am Not Your Mother: Write Your Test Code',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 24, 9, 55),
     datetime.datetime(2010, 2, 24, 10, 15),
     'dushay_mene_keck'),
    ('Break',
     ns.swc.BreakEvent,
     datetime.datetime(2010, 2, 24, 10, 15),
     datetime.datetime(2010, 2, 24, 10, 35), 
     'break1_day2'),
    ('Media, Blacklight, and Viewers Like You',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 24, 10, 35),
     datetime.datetime(2010, 2, 24, 10, 55),
     'beer'),
    ('Becoming Truly Innovative: Migrating from Millennium to Koha',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 24, 10, 55),
     datetime.datetime(2010, 2, 24, 11, 15),
     'beer'),
    ('Ask Anything!',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 24, 11, 15),
     datetime.datetime(2010, 2, 24, 12, 0),
     'chudnov'),
    ('Lunch',
     ns.swc.MealEvent,
     datetime.datetime(2010, 2, 24, 12, 0),
     datetime.datetime(2010, 2, 24, 13, 0), 
     'lunch_day2'),
    ('A Better Advanced Search',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 24, 13, 0),
     datetime.datetime(2010, 2, 24, 13, 20),
     'dushay_keck'),
    ('Drupal 7: A more powerful platform for building library applications',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 24, 13, 20),
     datetime.datetime(2010, 2, 24, 13, 40),
     'gordon'),
    ('Enhancing Discoverability With Virtual Shelf Browse',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 24, 13, 40),
     datetime.datetime(2010, 2, 24, 14, 0),
     'orphanides_lown_lynema'),
    ('How to Implement A Virtual Bookshelf With Solr',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 24, 14, 0),
     datetime.datetime(2010, 2, 24, 14, 20),
     'dushay_keck'),
    ('Break',
     ns.swc.BreakEvent,
     datetime.datetime(2010, 2, 24, 14, 20),
     datetime.datetime(2010, 2, 24, 14, 40), 
     'break2_day2'),
    ('Lightning Talks 2',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 24, 14, 40),
     datetime.datetime(2010, 2, 24, 15, 50), 
     'ltalks_day2'),
    ('Breakout Sessions 2',
     ns.swc.OrganizedEvent,
     datetime.datetime(2010, 2, 24, 15, 50),
     datetime.datetime(2010, 2, 24, 17, 0), 
     'breakout_day2'),
    ('Daily Wrap Up',
     ns.swc.OrganizedEvent,
     datetime.datetime(2010, 2, 24, 17, 0),
     datetime.datetime(2010, 2, 24, 17, 15), 
     'wrapup_day2'),

    ('Breakfast',
     ns.swc.MealEvent,
     datetime.datetime(2010, 2, 25, 8, 0),
     datetime.datetime(2010, 2, 25, 9, 0), 
     'breakfast_day3'),
    ('Housekeeping',
     ns.swc.OrganizedEvent,
     datetime.datetime(2010, 2, 25, 9, 0),
     datetime.datetime(2010, 2, 25, 9, 15), 
     'intro_day3'),
    ('Keynote #2: Paul Jones',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 25, 9, 15),
     datetime.datetime(2010, 2, 25, 10, 0),
     'jones'),
    ('Break',
     ns.swc.BreakEvent,
     datetime.datetime(2010, 2, 25, 10, 0),
     datetime.datetime(2010, 2, 25, 10, 15), 
     'break1_day3'),
    ('Lightning Talks 3',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 25, 10, 15),
     datetime.datetime(2010, 2, 25, 11, 0), 
     'ltalks_day3'),
    ('You Either Surf or You Fight: Integrating Library Services With Google Wave',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 25, 11, 0),
     datetime.datetime(2010, 2, 25, 11, 20),
     'hannan'),
    ('library/mobile: Developing a Mobile Catalog',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 25, 11, 20),
     datetime.datetime(2010, 2, 25, 11, 40),
     'griggs'),
    ('Mobile Web App Design: Getting Started',
     ns.swc.TalkEvent,
     datetime.datetime(2010, 2, 25, 11, 40),
     datetime.datetime(2010, 2, 25, 12, 0),
     'doran'),
    ('Wrap-Up',
     ns.swc.OrganizedEvent,
     datetime.datetime(2010, 2, 25, 12, 0),
     datetime.datetime(2010, 2, 25, 12, 15), 
     'wrapup_day3'),
]

if __name__ == '__main__':
    for (title, etype, start, end, shortname) in events:
        talkid = URIRef(shortname, base=ns.c4l10_base_uri)
        title = Literal(title)
        print (talkid, etype, start, end, title)

        g.add((talkid, rdfs.type, etype))
        g.add((talkid, rdfs.type, ical.Vevent))
        g.add((talkid, dce.title, title))
        g.add((talkid, ical.Dtsart, start))


            



    


    
