from . import *

# Total Eclipse (traitrise, boost 1 + etoile) — x2
# When Revealed: Discard the top 3 cards of your deck. Take 1 indirect damage
# for each event discarded this way. If an event with a printed "Special"
# ability is discarded this way, you are stunned.
# [star] Boost: Give the activating enemy an additional boost card.
#
# Modeles : 06030 Trickster (`DiscardDeckTopCards`), 02044 Lightning Bolt
# (`TakeIndirectDamage`), an010 (`Faces.GiveStatus(..., "Stunned")`), 01164
# Titania's Fury (boost additionnel). « printed Special » : APrintedSpecial,
# qui lit les capacites declarees et fonctionne sur une carte defaussee.
#
# ⚠ « the activating enemy » : on passe la FACE qui s'active
# (`message.being_message.by_face`), car `GiveBoostCardForThisActivation`
# n'accepte un sbire que par sa face (sender_card.py:751) ; passer `Villain`
# ne donnerait rien quand c'est un sbire qui s'active.

def GetAbilities() -> Sequence['Ability']:

    def total_eclipse_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        faces = joueur.DiscardDeckTopCards(3, effect)
        evenements = [face for face in faces if Event.IsType(face)]
        if evenements:
            identite.TakeIndirectDamage(this, len(evenements), effect)
        if any(APrintedSpecial(face) for face in evenements):
            Faces.GiveStatus([identite], "Stunned", effect)

    def total_eclipse_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        message.GiveBoostCardForThisActivation(message.being_message.by_face, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            total_eclipse_revealed,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            total_eclipse_boost,
        ),
    ]
