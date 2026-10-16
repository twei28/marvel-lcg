from . import *

# * Superfly — SBIRE unique (Cyber Swarm 4/6). AERIAL. FLYBORG. SWARM. PV 5, 3 boosts.
# Enters play with 2 Ooze counters on him.
# [star] This minion's SCH and ATK are equal to the number of Ooze counters here.
#
# Cartes de reference : `27067` Sand Clone / `td016` pour SCH et ATQ egales a un compteur
# (`ThisGainKeyword(fn, attack=1, scheme=1, change_on_event=OnEvent.Counter("This", compteur))`) ;
# `ThisEnterPlayWithCounters`. Compteur maison `ooze` (card_face.py).
#
# Mots-pieges : ici SEULEMENT SCH et ATK suivent le compteur (les PV sont imprimes : 5, a la difference des
# essaims) ; le compteur s'appelle « Ooze » (pas swarm) ; « on HIM » : il porte ses propres compteurs.


def GetAbilities() -> Sequence['Ability']:

    def jauge(effect: 'Effect', ui: List['CardFace']) -> int:
        Unused(ui)
        return effect.this.CastTo(Minion).GetCounters("ooze")

    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, "ooze"),
        AbilityFactory.ThisGainKeyword(
            jauge,
            attack=1,
            scheme=1,
            change_on_event=OnEvent.Counter("This", "ooze"),
        ),
    ]
