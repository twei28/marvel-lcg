from core import *
from dataclasses import field

@dataclass
class EncounterSetDescriptor:
    version: str
    name: str
    encounters: List[str]
    # AJOUT (20/10/2026, Galactic Storm Imperial Guard) : voir `CardFactory.RandomPick`.
    random_pick: List[Dict[str, Any]] = field(default_factory=list)
