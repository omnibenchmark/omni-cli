import datetime
from string import Template

import humanize
import rdflib
from tabulate import tabulate

from SPARQLWrapper import SPARQLWrapper, JSON

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

# TODO: checksum and atLocation do not return literal in rdflib query result

#?files prov:atLocation ?loc .
#?entity prov:atLocation ?entityLoc .

def fmt_date(ts):
    return ts.strftime("%a, %d %b %Y at %H:%M:%S")

def doQuery(query):
    return rdflib.Graph().query(query)

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

def query_last_generation():
    # TODO: we could derive the last-gen as a nested query, instead
    # of issuing two different queries.
    r = doQuery(lastGenQuery)
    generation = tuple(r)[0].gen

    sparql = SPARQLWrapper(LOCAL_ENDPOINT)
    sparql.setReturnFormat(JSON)

    q = Template(filesForGenerationQuery)
    query = q.substitute(generation=generation)
    sparql.setQuery(query)

    data = []

    try:
        ret = sparql.queryAndConvert()
        for r in ret["results"]["bindings"]:
            date_str = r['modified']['value']
            data.append({
                'file': r['source']['value'],
                'last_modified': fmt_date(datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")),
                'md5sum': r['checksum']['value'][:8],
                'keywords': r['keywords']['value'],
            })
    except Exception as e:
        print("error:", e)

    print(tabulate(
        data, showindex=True,
        headers={"file": "file", "last_modified": "modified", "md5sum": "md5", "keywords": "keywords"}))
