from uuid import UUID
from pydantic.dataclasses import dataclass
from pydantic import HttpUrl

@dataclass
class Resource:
    identifier: UUID
    link: HttpUrl
    keywords: list
    title: str = None
    description: str = None

    def isData(self):
        if len(self.keywords) == 0:
            return False
        k = self.keywords[0]
        return k.endswith('_data')

    def benchmark(self):
        if len(self.keywords) == 0:
            return False
        k = self.keywords[0]
        if k.endswith('_data'):
            return k.split('_data')[0]

