# configuration for a given project
from pydantic.dataclasses import dataclass

import yaml

CFG = "src/config.yaml"

@dataclass
class ProjectInfo:
    name: str
    benchmark: str

def project_info():
    config = yaml.safe_load(open(CFG))
    return ProjectInfo(
            name=config.get('data').get('name'),
            benchmark=config.get('benchmark_name'))
