import json

from .config import local_bench_data, local_orch_data

def strip_suffix_fn(sep='_'):
    """
    strip the last suffix joined by the separator
    """
    return lambda s: sep.join(s.split(sep)[:-1])

not_comma = lambda s: ',' not in s
not_example  = lambda s: not s.endswith('_example')

def benchmark_list():
    with open(local_orch_data) as f:
        data = json.load(f)
    keys = data.keys()
    return list(filter(lambda s: not_comma(s) and not_example(s), keys))

def keyword_list():
    #TODO: just exploring kw heuristics
    with open(local_bench_data) as f:
        data = [x for x in json.load(f).values()]
    kw = [i['keywords'][0] if len(i['keywords'])==1 else '' for i in data]
    fn = strip_suffix_fn()
    return set(map(fn, kw))



