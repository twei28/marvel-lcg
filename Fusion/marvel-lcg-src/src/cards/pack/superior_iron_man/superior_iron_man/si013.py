from . import *

# Endo-Sym Matter
#
# Modele The Power of Justice (core/01062.py) : `DoubleResourcesThisGenerates`.
#
# CORRECTIF (bug trouve en test) : `card_class="IdentitySpecific"`, PAS
# "Hero". `ClassCard.__init__` (card_player.py:64) traduit `desc.Class:
# "Hero"` en interne vers `"IdentitySpecific"` des la lecture
# (`if card_class == "Hero": card_class = "IdentitySpecific"`) : la carte ne
# porte donc jamais litteralement "Hero" dans `self.card_classes`, seulement
# "IdentitySpecific". Avec `card_class="Hero"`, le doublement ne se
# declenchait JAMAIS -- silencieusement, la carte se comportait comme une
# ressource wild normale (1 au lieu de 2), decouvert en jouant si011 (cout 2)
# avec elle comme seule ressource.

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.DoubleResourcesThisGenerates(
            CardFinder(card_class="IdentitySpecific")
        ),
    ]
