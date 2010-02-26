
import sys
import re
from rdflib import ConjunctiveGraph, Literal, URIRef
import lxml
from datetime import datetime
from namespaces import *

base_uri = 'http://irc.code4lib.org/'

g = rdflib.ConjunctiveGraph('Sleepycat')
g.open('store', create=True)

preconfs = [
    ('Registration / coffee', 
     datetime.datetime(2010, 2, 22, 8, 0),
     datetime.datetime(2010, 2, 22, 9, 0)),
    ('Morning Sessions', 
     datetime.datetime(2010, 2, 22, 9, 0),
     datetime.datetime(2010, 2, 22, 12, 0)),
    ('Lunch (on your own)', 
     datetime.datetime(2010, 2, 22, 12, 0),
     datetime.datetime(2010, 2, 22, 13, 30)),
    ('Afternoon Sessions', 
     datetime.datetime(2010, 2, 22, 13, 30),
     datetime.datetime(2010, 2, 22, 16, 30)),
    ('Registration / Breakfast',
     datetime.datetime(2010, 2, 23, 8, 0),
     datetime.datetime(2010, 2, 23, 9, 0)),
    ('Orientation / Housekeeping',
     datetime.datetime(2010, 2, 23, 9, 0),
     datetime.datetime(2010, 2, 23, 9, 15)),
    ('Keynote #1: Cathy Marshall',
     datetime.datetime(2010, 2, 23, 9, 15),
     datetime.datetime(2010, 2, 23, 10, 0),
     '/conference/2010/marshall'),
    ('Cloud4Lib'
     datetime.datetime(2010, 2, 23, 10, 0),
     datetime.datetime(2010, 2, 23, 10, 20),
     '/conference/2010/frumkin_reese'),
    ('The Linked Library Data Cloud: Stop talking and start doing'
     datetime.datetime(2010, 2, 23, 10, 20),
     datetime.datetime(2010, 2, 23, 10, 40),
     '/conference/2010/singer'),
    ('Break',
     datetime.datetime(2010, 2, 23, 10, 40),
     datetime.datetime(2010, 2, 23, 11, 0),
     '/conference/2010/dekker'),
    ('Do It Yourself Cloud Computing with Apache and R'
     datetime.datetime(2010, 2, 23, 11, 0),
     datetime.datetime(2010, 2, 23, 11, 20),
     '/conference/2010/dekker'),
    ('Public Datasets in the Cloud'
     datetime.datetime(2010, 2, 23, 11, 20),
     datetime.datetime(2010, 2, 23, 11, 40),
     '/conference/2010/klien_metz'),
    ('7 Ways to Enhance Library Interfaces with OCLC Web Services'
     datetime.datetime(2010, 2, 23, 11, 40),
     datetime.datetime(2010, 2, 23, 12, 0),
     '/conference/2010/frumkin_reese'),

]

if __name__ == '__main__':
    parser = etree.HtmlParser()
    tree = etree.parse('data/schedule.html', parser)
    confdays = tree.findall('dl[@class="day"]')
    events = confday.findall('dt[@class="vevent"]')
    for e in events:
        startstring = e.find('abbr[@class="dtstart"]').attrib['title']
        endstring = e.find('abbr[@class="dtend"]').attrib['title']
        summary = e.find('span[@class="summary"]')
        etuple = (
            



    


    
