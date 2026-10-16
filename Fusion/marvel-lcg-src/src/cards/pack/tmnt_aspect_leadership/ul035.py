from . import *

# "Turtle Power!" — EVENEMENT Leadership (TMNT Aspects, Inkwire), cout 1, [energy]. TACTIC.
# Play only if your identity has the [[TURTLE]] trait.
# Hero Action: Search the top 5 cards of your deck for a [[TURTLE]] ally and put it into play. If that ally
#   is still in play at the end of the phase, add it to your hand.
#
# MODIFIEE (reskin de `36020` "To Me, My X-Men!") : [[X-MEN]] -> [[TURTLE]] aux deux endroits. Script
# propre copie de 36020, seul le trait change.
#
# TEXTE CONTRE CODE
#  ⚠ « Play only if YOUR IDENTITY has TURTLE » : condition de jeu (`SetPlay(only_if_your_identity_has_trait)`).
#  ⚠ « the top 5 cards » : seulement les 5 du dessus (`Search.PlayerDeckTop(..., 5, ...)`).
#  ⚠ « still in play at the end of the phase » : verifie a la fin de la phase (`RunAt.TheEndOfThePhase`).


def GetAbilities() -> Sequence['Ability']:

    def turtle_power(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        face = Search.PlayerDeckTop(
            effect,
            initiator,
            5,
            trait="TURTLE",
            card_type=Ally,
        )
        if face:
            face.PutIntoPlay(initiator, effect)

            def add_it_to_hand():
                if face.card.area.flags.is_in_play:
                    initiator.GainCard(face, effect)

            RunAt.TheEndOfThePhase(effect, add_it_to_hand)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            turtle_power
        ).SetPlay(only_if_your_identity_has_trait="TURTLE").SetLabel(),
    ]
