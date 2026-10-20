from . import *

# Kree Assassin — SBIRE (Hala Ultimatum). KREE. SCH 1, ATK 3, PV 5. 1 etoile + 1 icone de boost. 2 exemplaires.
# Retaliate 1.
# [star] Boost: If the activating enemy has a tough status card, exhaust your identity.
#
# Cartes de reference :
#  - Retaliate : natif (desc.Retaliate, fiche mots-cles/retaliate.md).
#  - « Boost: ... exhaust your identity » : `message.activating_enemy` + `Faces.HasStatus` (modele gs144/
#    gs146, meme pack) ; « your » = le joueur vise par l'activation (`message.against_player`, convention
#    GS4 : le « vous » d'un Boost suit le controleur attaque, pas forcement le porteur de la carte) ;
#    `joueur.GetIdentity().card.Exhaust(effect)` (modele `deadpool/44025.py`/`determination/dt012.py` pour
#    `GetIdentity()`, `card.py` pour `Exhaust`).
#
# ⚠ Mots-pieges : « exhaust YOUR identity » (le joueur vise, pas le controleur de Kree Assassin) ; si aucun
# joueur n'est vise (activation hors attaque de joueur), rien a incliner.


def GetAbilities() -> Sequence['Ability']:

    def booster(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if Faces.HasStatus([message.activating_enemy], "Tough") > 0:
            joueur = message.against_player or effect.GetInitiator()
            if joueur is not None:
                joueur.GetIdentity().card.Exhaust(effect)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", booster),
    ]
