import datetime
from string import Template

import humanize
import rdflib
from tabulate import tabulate

from SPARQLWrapper import SPARQLWrapper, JSON

from .model import OrchestratorRun

# TODO read endpoint from config file
LOCAL_ENDPOINT = "http://localhost:7878/query"


genListQuery = """
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?act ?gen ?start ?end WHERE {
  SERVICE <http://localhost:7878/query> {
      ?gen a prov:Generation .
      ?gen prov:activity ?act . 
      ?act prov:startedAtTime ?start.
      ?act prov:endedAtTime ?end;
  }
}
ORDER BY DESC(?start)
LIMIT 100
"""

# TODO: filter by namespace
# TODO: pass the local endpoint

lastGenQuery = """
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?act ?gen ?start ?end WHERE {
  SERVICE <http://localhost:7878/query> {
      ?gen a prov:Generation .
      ?gen prov:activity ?act . 
      ?act prov:startedAtTime ?start.
      ?act prov:endedAtTime ?end;
  }
}
ORDER BY DESC(?start)
LIMIT 1
"""

filesForGenerationQuery = """
PREFIX schema: <http://schema.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX renku: <https://swissdatasciencecenter.github.io/renku-ontology#>
SELECT ?part ?source ?checksum ?modified ?keywords WHERE {
  FILTER (?gen = <$generation>)
        ?dataset schema:hasPart ?files .
        ?dataset schema:dateModified ?modified .
        ?dataset schema:keywords ?keywords .
        ?files prov:entity ?datasetEntity .
        ?datasetEntity prov:qualifiedGeneration ?gen .
        ?dataset schema:hasPart ?part .
        ?part prov:entity ?entity .
        ?part renku:source ?source .
        ?entity renku:checksum ?checksum .
}
"""

epochForOrchestratorQuery = """
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX omni: <http://omnibenchmark.org/ns#>

SELECT ?run ?epoch ?start ?end WHERE {
  ?run omni:hasName "$name" .
  ?run omni:hasEpoch ?epoch.
  ?run prov:startedAtTime ?start.
  OPTIONAL {?run prov:endedAtTime ?end.}
} 
ORDER BY DESC(?start)
LIMIT 10
"""

lastEpochForOrchestratorQuery = """
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX omni: <http://omnibenchmark.org/ns#>

SELECT ?run ?epoch ?start ?end WHERE {
  ?run omni:hasName "$name" .
  ?run omni:hasEpoch ?epoch.
  ?run prov:startedAtTime ?start.
  OPTIONAL {?run prov:endedAtTime ?end.}
} 
ORDER BY DESC(?start)
LIMIT 1
"""

def fmt_date(ts):
    return ts.strftime("%a, %d %b %Y at %H:%M:%S")

def doQuery(query):
    return rdflib.Graph().query(query)

def prepareAndSubmitQueryFromTemplate(template, ctx):
    sparql = SPARQLWrapper(LOCAL_ENDPOINT)
    sparql.setReturnFormat(JSON)
    q = Template(template)
    query = q.substitute(**ctx)
    sparql.setQuery(query)
    try:
        result = sparql.queryAndConvert()
    except Exception as e:
        print("error:", e)
    return result

def query_generations():
    result = doQuery(genListQuery)

    table = []
    for row in result:
        _delta = humanize.naturaldelta(row.end.value - row.start.value)
        table.append((fmt_date(row.start.value), _delta, row.gen.split('/')[-1], row.gen.split('/')[-3]))
    print(tabulate(
        table,
        showindex=True,
        headers=["Start", "Duration", "Generation ID", "Activity ID"]))

# TODO: pass generation hash (activity/generation)
# TODO: pass keywords to limit the query

parse_time_with_ms = lambda s: datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f")
parse_time_with_tz = lambda s: datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")

def query_last_generation():
    # TODO: we could derive the last-gen as a nested query, instead
    # of issuing two different queries.

    r = doQuery(lastGenQuery)
    generation = tuple(r)[0].gen
    ctx = {'generation': generation}
    result = prepareAndSubmitQueryFromTemplate(filesForGenerationQuery, ctx)

    data = []

    for r in result["results"]["bindings"]:
        date_str = maybe(r, 'modified')
        data.append({
            'file': maybe(r, 'source'),
            'last_modified': fmt_date(parse_time_with_tz(date_str)),
            'md5sum': maybe(r, 'checksum')[:8],
            'keywords': maybe(r, 'keywords'),
        })

    print(tabulate(
        data, showindex=True,
        headers={"file": "file", "last_modified": "modified", "md5sum": "md5", "keywords": "keywords"}))



def query_epochs_by_name(name):
    ctx = {'name': name}
    result = prepareAndSubmitQueryFromTemplate(epochForOrchestratorQuery, ctx)

    data = []
    for r in result["results"]["bindings"]:
        started = maybe(r, 'start')
        if started is not None:
            started = fmt_date(parse_time_with_ms(started))
        ended = maybe(r, 'end')
        if ended is not None:
            ended = fmt_date(parse_time_with_ms(ended))
        data.append({
            'name': name,
            'epoch': maybe(r, 'epoch'),
            'started': started,
            'ended': ended,
            'run': maybe(r, 'run')
        })

    print(tabulate(
        data, showindex=True,
        headers={"name": "name", "epoch": "epoch", "started": "started", "ended": "ended", "run": "run"}))

def get_last_run_by_name(name):
    ctx = {'name': name}
    result = prepareAndSubmitQueryFromTemplate(lastEpochForOrchestratorQuery, ctx)
    data = []
    for r in result["results"]["bindings"]:
        data.append({
            'run': maybe(r, 'run'),
            'epoch': maybe(r, 'epoch'),
            'start': maybe(r, 'start'),
            'end': maybe(r, 'end'),
        })
    if len(data) != 1:
        return None
    d = data[0]
    start_ts = parse_time_with_ms(d.get('start'))
    ended_ts = parse_time_with_ms(d.get('end')) if d.get('end') is not None else None
    run = OrchestratorRun(
            name=name,
            run=d.get('run'),
            epoch=int(d.get('epoch')),
            started=start_ts,
            ended=ended_ts)
    return run

def maybe(d, var):
    _d = d.get(var)
    if _d is None:
        return None
    return _d.get('value')


