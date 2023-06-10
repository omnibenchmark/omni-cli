from datetime import datetime
from rdflib import BNode, Graph, Literal, Namespace, RDF
from SPARQLWrapper import SPARQLWrapper, JSON, POST

OMNI = Namespace("http://omnibenchmark.org/ns#")
OMNI_RUN = Namespace("http://omnibenchmark.org/run/")
PROV = Namespace("http://www.w3.org/ns/prov#")
LOCAL_ENDPOINT = "http://localhost:7878/update"

def insert_triples(queryString):
    sparql = SPARQLWrapper(LOCAL_ENDPOINT)
    sparql.setQuery(queryString)
    sparql.setMethod(POST)
    ret = sparql.queryAndConvert()
    print(ret)

def bump_benchmark_epoch(benchmark_name):
    g = Graph()
    g.bind("omni", OMNI)

    current = OMNI_RUN.__getattr__(str(BNode()))  # a GUID is generated
    epoch = 4
    now = datetime.now()

    g.add((current, RDF.type, OMNI.Benchmark))
    g.add((current, RDF.type, PROV.Activity))
    g.add((current, OMNI.hasName, Literal(benchmark_name)))
    g.add((current, OMNI.hasEpoch, Literal(epoch)))
    g.add((current, PROV.startedAtTime, Literal(now)))
    insert(g)

def insert(g):
    updatequery = "\n".join([f"PREFIX {prefix}: {ns.n3()}" for prefix, ns in g.namespaces()])
    updatequery += f"\nINSERT DATA {{"
    updatequery += " .\n".join([f"\t\t{s.n3()} {p.n3()} {o.n3()}" for (s, p, o) in g.triples((None, None, None))])
    updatequery += f" . \n\n}}\n"
    insert_triples(updatequery)

if __name__ == "__main__":
    bump_benchmark_epoch("iris")
