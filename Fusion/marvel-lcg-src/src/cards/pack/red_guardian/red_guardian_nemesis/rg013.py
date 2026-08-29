from . import *

# * Captain America — sbire nemesis de Red Guardian
# Quickstrike.
# [star] Forced Response: After Captain America attacks and damages you,
#   discard 1 random card from your hand.
#
# « Quickstrike » et l'ATK variable « 2* » sont dans les DONNEES (cles desc
# `Quickstrike` et `ATK: "2*"`), pas ici : le moteur lit le mot-cle depuis le
# `desc`, pas depuis le texte ni depuis une capacite.
#
# Gabarit : Pirate Commander (gmw/space_pirates/16138) — meme declencheur
# « after [ce sbire] attacks and damages you » suivi d'une perte de carte en
# main au hasard, et meme `AbilityType.ForcedResponse`.
# `AfterUnitAttackAndDamageUnit` avec `who_be_attacked="You"` : le moteur pose
# lui-meme la regle officielle (« you » = le joueur attaque, meme s'il a
# defendu avec un allie) dans `check_who_be_attacked` (do_attack.py:394).


def GetAbilities() -> Sequence['Ability']:

    def captain_america(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        joueur = message.GetToPlayer()
        joueur.DiscardRandomHandCards(1, effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            "You",
            captain_america,
        ),
    ]
