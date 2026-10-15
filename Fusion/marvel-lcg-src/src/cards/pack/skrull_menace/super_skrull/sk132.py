from . import *

# Skrull Warlords — COMPLOT ANNEXE (Super-Skrull). Menace 2[per_hero], 3 icones Y.
# Forced Response: After a card enters play under any player's control, give the
#   villain a facedown boost card.
#
# Cartes de reference :
#  - **`27189a`** (pack sm) : `AfterCardEnterPlay(ForcedResponse, CardFinder(...), op)` ;
#    **`fne/bullseye 60072`** / `dazzler 60dz023` : une carte boost face cachee pour le
#    mechant = `Faces.GiveFacedownBoostCards([mechant], 1, effect)`.
#  - **`04079b`** : `Condition` sur le controleur (`Player.IsType(trigger.GetControlBy())`).
#
# ⚠ Mots-pieges : « ANY player's control » (n'importe quel joueur ; une carte de
# rencontre, de campagne ou d'un autre ennemi n'est pas concernee) ; « a CARD »
# (tous les types : allie, soutien, amelioration, evenement joue puis laissant une
# carte en jeu...) ; « the VILLAIN » (le mechant courant) ; « FACEDOWN boost card »
# (elle servira a sa prochaine activation).


def GetAbilities() -> Sequence['Ability']:

    def sous_controle_joueur(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> bool:
        return Player.IsType(message.trigger.GetControlBy())

    def guerriers(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        mechant = Worlds.FindVillain(effect)
        if mechant is not None:
            Faces.GiveFacedownBoostCards([mechant], 1, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            CardFinder(),
            guerriers,
            conditions=[sous_controle_joueur],
        ),
    ]
