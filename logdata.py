#!/usr/bin/env python

import sys
import re
import rdflib
import uuid
from rdflib import ConjunctiveGraph, Literal, URIRef
from optparse import OptionParser
import urllib
from datetime import datetime
from time import mktime

from namespaces import *
from graphstore import g

siocurl = 'http://irc.code4lib.org/code4lib'
base_uri = 'http://irc.code4lib.org/'

#g = rdflib.ConjunctiveGraph('Sleepycat')
#g.open('sleepy', create=True)

def parse_entry(line):
    (tstamp, user, type, channel, content) = re.split('\s+', line, 4)
    user = re.split('!~?', user[1:])[0]
    tstamp = tstamp[:-6]
    dt = datetime.strptime(tstamp, "%Y-%m-%dT%H:%M:%S")
    content = content[1:]
    return {
        'tstamp': Literal(dt, datatype=xsd.date),
        'user': user,
        'type': type,
        'postid': URIRef('msg/%s' % uuid.uuid1(), base=base_uri),
        'userid': URIRef('user/%s' % user, base=base_uri),
        'content': rdflib.Literal(content)
    }

if __name__ == '__main__':
    op = OptionParser()
    op.set_usage("usage: logdata.py [options] 'YYYY-mm-dd'")
    op.add_option('--mode', dest='mode', action='store', type='string',
        help='load | enrich | users', default='load')
    op.add_option('--debug', dest='DEBUG', action="store_true",
        help='turn on debug output', default=False)
    opts, args = op.parse_args()

    for filename in args:
        raw = open(filename)
        lines = raw.readlines()
        for line in lines:
            try:
                e = parse_entry(line.decode('utf-8', 'ignore'))
            except:
                print >>sys.stderr, line
                raise
            if e['type'] != 'PRIVMSG': continue
            if opts.mode == 'load':
                g.add((e['postid'], rdf.type, sioc.Post))
                g.add((e['postid'], sioc.has_creator, e['userid']))
                g.add((e['postid'], sioc.content, e['content']))
                g.add((e['postid'], dct.created, e['tstamp']))
                if re.match('@', e['content']):
                    g.add((e['postid'], rdf.type, ov.ZoiaCommand))
                m = re.match('([\w\-\_]+):', e['content'])
                if m: 
                    (username,) = m.groups()
                    addressed_to_user = URIRef('http://irc.code4lib.org/user/%s' % username, base=base_uri)
                    if list(g.subject_predicates(addressed_to_user)):
                        g.add((e['postid'], sioc.addressed_to, addressed_to_user))
            elif opts.mode == 'users':
                if not (list(g.subject_predicates(e['userid']))):
                    g.add((e['userid'], rdf.type, sioc.User))
    g.commit()
            

    


    
