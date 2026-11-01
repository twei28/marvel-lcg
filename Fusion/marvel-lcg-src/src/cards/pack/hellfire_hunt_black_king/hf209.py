from . import *

# Mercury (Cessily Kincaid), allie CAPTIVE MUTANT. « Toughness. » (desc, natif). Seule capacite : le trait RECRUITED une fois la campagne notee.
# Carte de reference : hf208 (`CaptifRecrute`).


def GetAbilities() -> Sequence['Ability']:
    return [CaptifRecrute()]
