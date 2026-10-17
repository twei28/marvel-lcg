from . import *

# Pizza Time — EVENEMENT 0 [energy], aspect Basic (TMNT Reskins).
# Play only if your identity has the [[MUTANT]] trait.
# Alter-Ego Action: Choose up to 2 identity-specific cards in your discard pile and shuffle them into your
#   deck. If Rupert's Pizzeria is in play, draw 1 card.
#
# MODIFIEE de 37021 Mutant Education : « X-Mansion » -> « Rupert's Pizzeria » (ub043). Script copie de
# 37021, y compris la borne basse des cibles (1 sans Pizzeria : la carte ne se joue pas pour rien ;
# 0 avec, car elle pioche quand meme).


def RupertsPizzeriaEnJeu(effect: 'Effect') -> bool:
    return Worlds.FindCardOnField(effect, name="Rupert's Pizzeria") != None


def GetAbilities() -> Sequence['Ability']:

    def pizza_time(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        Faces.ShuffleAllTo(effect.targets, initiator.player_deck, effect)

        if RupertsPizzeriaEnJeu(effect):
            initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            pizza_time,
        ).SetPlay(only_if_your_identity_has_trait="MUTANT").SetLabel()
        .SetTarget(card_class="IdentitySpecific",
            range=(lambda effect: 0 if RupertsPizzeriaEnJeu(effect) else 1, 2),
            from_where=["YourDiscardPile"]
        ),
    ]
