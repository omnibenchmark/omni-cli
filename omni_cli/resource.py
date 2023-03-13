from dataclasses import dataclass

#TODO(btrave): maybe use https://docs.pydantic.dev/usage/dataclasses/

@dataclass
class Resource:
    _id: str
    uri: str
    _type: str
    name: str
    description: str
