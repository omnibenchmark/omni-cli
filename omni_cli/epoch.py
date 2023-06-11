from datetime import datetime
from rdflib import Graph, Namespace, RDF
from rdflib import URIRef, BNode, Literal

from SPARQLWrapper import SPARQLWrapper, JSON, POST

from .sparql import get_last_run_by_name

OMNI = Namespace("http://omnibenchmark.org/ns#")
OMNI_RUN = Namespace("http://omnibenchmark.org/run/")
PROV = Namespace("http://www.w3.org/ns/prov#")
LOCAL_ENDPOINT = "http://localhost:7878/update"

def do_start_epoch(benchmark_name):
    """
    Start a new epoch for this benchmark. This should be called by the
    orchestrator before running a controlled batch, or alternatively at any
    fixed interval (i.e., daily) so that any method can take the reference to
    write its own triples.

    This function first tries to retrieve the last known epoch for a given 
    orchestrator run from our alternative Knowledge Graph; then it will add triples
    for a new orchestrator run that starts now, and with an epoch field set to
    the next consecutive integer.

    This function will fail if the knowledge graph configured is not reachable.
    """
    last_run = get_last_run_by_name(benchmark_name)
    if last_run is None:
        last = 0
    else:
        last = last_run.epoch
    bump_benchmark_epoch(name=benchmark_name, last_epoch=last)

def do_stop_epoch(benchmark_name):
    """
    Stop an existing epoch for this benchmark; i.e., writes the ended timestamp
    as the closing interval, setting it to the current date and time.

    Attempting to overwrite the closing interval of an OrchestratorRun that has already
    ended will raise a ValueError exception.
    """
    last_run = get_last_run_by_name(benchmark_name)
    if last_run is None:
        print("cannot close benchmark run, not started")
        return
    close_benchmark_epoch(last_run)
    print("ok")

def newGraphWithOmniNS():
    g = Graph()
    g.bind("omni", OMNI)
    return g

def insert_triples(queryString):
    sparql = SPARQLWrapper(LOCAL_ENDPOINT)
    sparql.setQuery(queryString)
    sparql.setMethod(POST)
    ret = sparql.queryAndConvert()

def bump_benchmark_epoch(name=None, last_epoch=None):
    if name is None or last_epoch is None:
        raise ValueError("Need non null parameters for name and last_epoch")

    epoch = last_epoch + 1
    now = datetime.now()

    g = newGraphWithOmniNS()
    current = OMNI_RUN.__getattr__(str(BNode()))  # a GUID is generated
    g.add((current, RDF.type, OMNI.Benchmark))
    g.add((current, RDF.type, PROV.Activity))
    g.add((current, OMNI.hasName, Literal(name)))
    g.add((current, OMNI.hasEpoch, Literal(epoch)))
    g.add((current, PROV.startedAtTime, Literal(now)))
    insert(g)

def close_benchmark_epoch(last_run=None):
    if last_run.ended is not None:
        raise ValueError("tried to overwrite end timestamp on OrchestratorRun")
    now = datetime.now()
    g = newGraphWithOmniNS()
    current = URIRef(last_run.run)
    g.add((current, PROV.endedAtTime, Literal(now)))
    insert(g)

def insert(g):
    updatequery = "\n".join([f"PREFIX {prefix}: {ns.n3()}" for prefix, ns in g.namespaces()])
    updatequery += f"\nINSERT DATA {{"
    updatequery += " .\n".join([f"\t\t{s.n3()} {p.n3()} {o.n3()}" for (s, p, o) in g.triples((None, None, None))])
    updatequery += f" . \n\n}}\n"
    insert_triples(updatequery)
