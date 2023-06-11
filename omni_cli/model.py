from dataclasses import dataclass
import datetime

#
# Models for data structures
#

@dataclass(init=True)
class OrchestratorRun:
    """A single run of an orchestrator"""
    name: str
    run: str
    epoch: int
    started: datetime.datetime
    ended: datetime.datetime

