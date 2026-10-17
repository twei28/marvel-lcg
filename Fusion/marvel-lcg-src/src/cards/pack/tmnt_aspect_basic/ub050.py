from . import *

# "Special Delivery!" — EVENEMENT 0 [energy], aspect Basic (TMNT Reskins).
# Play only if your identity has the [[MUTANT]] trait.
# Alter-Ego Action: Choose up to 2 allies in your discard pile with the [[DIMENSION X]], [[MUTANIMAL]], or
#   [[NINJA]] trait and shuffle them into your deck. If Rupert's Pizzeria is in play, draw 1 card.
#
# MODIFIEE de 37031 X-Men Instruction : X-MEN -> DIMENSION X / MUTANIMAL / NINJA ; « X-Mansion » ->
# « Rupert's Pizzeria ». Script copie de 37031.


def RupertsPizzeriaEnJeu(effect: 'Effect') -> bool:
    return Worlds.FindCardOnField(effect, name="Rupert's Pizzeria") != None


def GetAbilities() -> Sequence['Ability']:

    def special_delivery(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        Faces.ShuffleAllTo(effect.targets, initiator.player_deck, effect)

        if RupertsPizzeriaEnJeu(effect):
            initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            special_delivery,
        ).SetPlay(only_if_your_identity_has_trait="MUTANT").SetLabel()
        .SetTarget(Ally, traits=["DIMENSION X", "MUTANIMAL", "NINJA"],
                   range=(lambda effect: 0 if RupertsPizzeriaEnJeu(effect) else 1, 2),
                   from_where=["YourDiscardPile"]),
    ]
