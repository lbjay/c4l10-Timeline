from rdflib import ConjunctiveGraph, Literal, URIRef
from namespaces import *

default_graph_uri = 'http://irc.code4lib.org/'
g = ConjunctiveGraph('Sleepycat', identifier = URIRef(default_graph_uri))
g.open('store', create=True)

[g.add(x) for x in [
    (URIRef('user/zoia'), rdfs.type, ov.IrcBot),
]]
