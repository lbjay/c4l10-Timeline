
from rdflib import ConjunctiveGraph, Literal, Namespace, URIRef

g = ConjunctiveGraph()

foaf = Namespace('http://xmlns.com/foaf/0.1/')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns/')
xsd = Namespace('http://www.w3.org/2001/XMLSchema#')

user1 = URIRef('http://example.com/user/don')
user2 = URIRef('http://example.com/user/betty')

g.add((user1, rdf.type, foaf.Person))
g.add((user1, foaf.age, Literal('44', datatype=xsd.int)))
g.add((user2, rdf.type, foaf.Person))
g.add((user2, foaf.age, Literal('34', datatype=xsd.int)))
g.add((user1, foaf.knows, user2))

ns = {'foaf': foaf, 'rdf': rdf , 'xsd': xsd }
person_query = 'select ?p WHERE { ?p rdf:type foaf:Person }'
knows_query = 'select ?a ?b WHERE { ?a foaf:knows ?b }'
age_query = 'select ?p WHERE { ?p rdf:type foaf:Person . FILTER(foaf:age == ?age) }'

persons = g.query(person_query, initNs=ns)
knows = g.query(knows_query, initNs=ns)
age = g.query(age_query, initNs=ns, initBindings={'?age': Literal('44', datatype=xsd.int)})

try:
    assert len(persons) == 2
    print "persons OK"
except AssertionError:
    print len(persons)

try:
    assert len(knows) == 1
    print "knows OK"
except AssertionError:
    print len(knows)

try:
    assert len(age) == 1
    print "age OK"
except AssertionError:
    print len(age)


