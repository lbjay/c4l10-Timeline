from rdflib import plugin, ConjunctiveGraph, URIRef
from rdflib.store import Store, NO_STORE, VALID_STORE

#class PostStore(SQLite):
#    def __init__(self, create=False):
#        SQLite.__init__(self)

default_graph_uri = 'http://irc.code4lib.org'
#store = plugin.get('SQLite', Store)('sqlite.dat')
store = plugin.get('Sleepycat', Store)('sleepycat')
rt = store.open('sleepycat', create=False)

if rt == 0:
    store.open('sleepycat', create=True)
else:
    assert rt == VALID_STORE

g = ConjunctiveGraph(store,
        identifier = URIRef(default_graph_uri))

