import os
from pydantic.dataclasses import dataclass

import yaml

PLAN_FILENAME = "benchmark-plan.yml"

@dataclass
class BenchmarkPlan:
    name: str
    base: str
    stages: list
    stage_dict: dict

    def stage(self, name):
        return self.stage_dict.get(name)

def describe_benchmark(path):
    fname = os.path.join(path, PLAN_FILENAME)
    plan = load_benchmark_plan(fname)
    print()
    print(f"benchmark: {plan.name}")
    print(f"base: {plan.base}")
    print()
    print("stages:")
    print()
    for idx, st in enumerate(plan.stages):
        print(f"({idx + 1}) {st}")
        stage = plan.stage(st)
        if stage is not None:
            for repo in stage.get('repos'):
                print(f"    {repo}")

flatten = lambda data: {k: v for x in data for (k,v) in x.items()}

def load_benchmark_plan(path):
    if not os.path.isfile(path):
        print("error: file not found")
        return

    with open(path, "r") as stream:
        try:
            cfg = yaml.safe_load(stream)
            stages = cfg.get('stages')
            stage_dict = {}
            for st in stages:
                stage_dict[st] = cfg.get(st) 
            plan = BenchmarkPlan(
                    stages=stages,
                    stage_dict=stage_dict,
                    **flatten(cfg.get('benchmark')))
            return plan
        except yaml.YAMLError as exc:
            print(exc)
            return
