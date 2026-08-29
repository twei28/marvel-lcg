from . import *

# Soviet Super-Soldier
# Red Guardian gains steady.
# Resource: Exhaust Soviet Super-Soldier -> generate a [wild] resource.
#
# Montage officiel mot pour mot : Magneto's Helmet (49003), qui imprime les deux
# memes lignes (« Magneto gains steady. » + une ressource [wild] par epuisement).
# Le mot-cle steady n'est pas une capacite mais un attribut donne a la carte
# nommee : `GiveKeywordToAttached(CardFinder(name=...), steady=1)`.
#
# Le nom vise la face HEROS : l'alter-ego du set s'appelle « Alexei Shostakov »,
# et le texte dit bien « Red Guardian ». Le mot-cle ne suit donc pas le
# retournement, ce qui est le comportement imprime.
#
# La ressource est universelle (pas de `for_card`), contrairement au casque de
# Magneto qui restreint aux cartes MAGNETIC.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Red Guardian"),
            steady=1,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
