from . import *

# Tony's Arc Reactor : AMELIORATION (ITEM. TECH.), cout 3, [energy].
# Reduce the cost of this card by 1 if you control an upgrade with the TECH trait. Your hand size is +1 while you are in hero form.
#
# CARTES DE REFERENCE
#  - `04159a` : `*GiveKeywordToAttached(Hero, ..)` ; `GiveKeywordToAttached(.., hand_size=N)` (fabrique `asset.py`). `nt005` : `ReduceCostToPlayThis`.
#
# TEXTE CONTRE CODE
#  « +1 hand size WHILE YOU ARE IN HERO FORM » : le bonus vit sur la face heros (`Hero`) : il disparait en alter-ego (contre-cas dans l'AUTRE forme, lecon an002).
#  Chiffres : cout 3, main +1.


def GetAbilities() -> Sequence['Ability']:

    def controle_une_amelioration_tech(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        return joueur is not None and bool(AmeliorationsTech(joueur))

    return [
        AbilityFactory.ReduceCostToPlayThis(1, conditions=[controle_une_amelioration_tech]),
        *AbilityFactory.GiveKeywordToAttached(Hero, hand_size=1),
    ]
