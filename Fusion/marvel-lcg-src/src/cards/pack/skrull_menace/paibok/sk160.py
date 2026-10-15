from . import *

# Power Demonstration — TRAITRISE x4 (Paibok). 2 boosts.
# When Revealed: Resolve the "Boost" ability on each attachment in play, that belongs to the Paibok
#   encounter set.
#
# Cartes de reference : **`24017`** Double Trouble (`ResolveAbility` d'une capacite nommee de cartes en
# jeu) ; helper `ResoudreLesBoosts` (paibok/__init__.py), identique a sk159 (alter ego), sk155, sk146.
#
# ⚠ Mots-pieges : « each attachment IN PLAY that belongs to the Paibok SET » (Distracted, Hypnotized,
# Trapped in Ice sur les identites ; Captain Paibok et les POWER SKRULL sur Paibok) ; le Boost se resout
# pour le joueur qui REVELE (« a character you control », « your hand ») ; aucun attachement en jeu :
# rien (pas de surge, la carte ne dit pas).


def GetAbilities() -> Sequence['Ability']:

    def demonstration(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        ResoudreLesBoosts(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, demonstration),
    ]
