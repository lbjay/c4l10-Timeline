
import unittest
from rdflib import ConjunctiveGraph, Literal, Namespace, URIRef

g = ConjunctiveGraph()

foaf = Namespace('http://xmlns.com/foaf/0.1/')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns/')
xsd = Namespace('http://www.w3.org/2001/XMLSchema#')
ns = {'foaf': foaf, 'rdf': rdf , 'xsd': xsd }

user1 = URIRef('http://example.com/user/don')
user2 = URIRef('http://example.com/user/betty')
user3 = URIRef('http://example.com/user/midge')

g.add((user1, rdf.type, foaf.Person))
g.add((user1, foaf.age, Literal('38', datatype=xsd.int)))
g.add((user2, rdf.type, foaf.Person))
g.add((user2, foaf.age, Literal('31', datatype=xsd.int)))
g.add((user3, rdf.type, foaf.Person))
g.add((user3, foaf.age, Literal('30', datatype=xsd.int)))
g.add((user1, foaf.knows, user2))
g.add((user1, foaf.knows, user3))

class SparqlCheck(unittest.TestCase):
    def testPersons(self):
        """query for foaf:Person nodes"""
        person_query = 'select ?p WHERE { ?p rdf:type foaf:Person }'
        persons = g.query(person_query, initNs=ns)
        self.assertEqual(len(persons), 3)

    def testKnows(self):
        """query for who foaf:knows who"""
        knows_query = 'select ?a ?b WHERE { ?a foaf:knows ?b }'
        knows = g.query(knows_query, initNs=ns)
        self.assertEqual(len(knows), 2)

    def testAge(self):
        """query for who is older than X"""
        age_query = """
            select ?p WHERE 
            { ?p rdf:type foaf:Person .
              ?p foaf:age ?a
              FILTER(?a > xsd:int(?age))
            }
        """
        bindings={'?age': '35'}
        ages = g.query(age_query, 
            initNs=ns, 
            initBindings=bindings
        )
        self.assertEqual(len(ages), 1)

if __name__ == '__main__':
    unittest.main()

