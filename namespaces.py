from rdflib import Namespace
 
foaf = Namespace('http://xmlns.com/foaf/0.1/')
dce = Namespace('http://purl.org/dc/elements/1.1/')
dct = Namespace('http://purl.org/dc/terms/')
sioc = Namespace('http://rdfs.org/sioc/ns/')
voc = Namespace('http://ns.inria.fr/irc/2008/09/25/voc/')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns/')
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema/')
xsd = Namespace('http://www.w3.org/2001/XMLSchema#')
ov = Namespace('http://open.vocab.org/terms/')
swc = Namespace('http://data.semanticweb.org/ns/swc/ontology#')
ical = Namespace('http://www.w3.org/2002/12/cal/ical#')
time = Namespace('ttp://www.w3.org/2006/time#')

def bind_graph(graph):
    for k,v in vars().items():
        if not isinstance(v, Namespace):
            continue
        graph.bind(k, v)

