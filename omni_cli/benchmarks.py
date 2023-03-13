import json

import yaml
import requests

from .config import local_bench_data, local_orch_data

def strip_suffix_fn(sep='_'):
    """
    strip the last suffix joined by the separator
    """
    return lambda s: sep.join(s.split(sep)[:-1])

# TODO(btraven): I am not absolutely certain what's the semantics for the comma in these benchmarks, so I'll skip for now.
not_comma = lambda s: ',' not in s
not_example  = lambda s: not s.endswith('_example')

class NoBenchmarkID(Exception):
    pass

def benchmark_list():
    with open(local_orch_data) as f:
        data = json.load(f)
    keys = data.keys()
    return list(filter(lambda s: not_comma(s) and not_example(s), keys))

def fetch_orchestrator_ci_yaml(base):
    url = base + '/-/raw/master/.gitlab-ci.yml?inline=false'
    ci = yaml.safe_load(requests.get(url).text)
    return ci.get('stages')

def stage_list(bench_id):
    # steps:
    # 1. download (or find in local cache) the gitlab-ci yaml for the orchestrator
    # 2. return the stages
    with open(local_orch_data) as f:
        data = json.load(f)
    bench = data.get(bench_id)
    if bench is None:
        raise NoBenchmarkID
    base = bench.get("url")
    return fetch_orchestrator_ci_yaml(bench.get("url"))

def keyword_list():
    #TODO: just exploring kw heuristics
    with open(local_bench_data) as f:
        data = [x for x in json.load(f).values()]
    kw = [i['keywords'][0] if len(i['keywords'])==1 else '' for i in data]
    fn = strip_suffix_fn()
    return set(map(fn, kw))
