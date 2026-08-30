from . import *

# Murderer's Guilt — OBLIGATION, give to the Kaine Parker player.
# You may flip to alter-ego form. Choose:
# - Exhaust Kaine Parker and take 2 damage -> remove Murderer's Guilt from
#   the game.
# - Take 1 damage for each event in your hand. If less than 3 damage was
#   taken this way, this card gains surge. Discard this obligation.
#
# Modele exact : okoye/okoye/ok019.py (Funeral Rites), meme structure
# `AbilityFactory.WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgo
# Form` + `player.ChooseAbilities` a 2 branches. Deuxieme branche : nombre
# d'evenements en main via `player.hand_cards.Get()` filtre par
# `Event.IsType` (modele wonder_man/58034.py).


def GetAbilities() -> Sequence['Ability']:

    def murderers_guilt(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def exhaust_and_remove(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            alter_ego = player.GetIdentity().GetAlterEgoFace()
            Faces.ExhaustAll([alter_ego], effect)
            this.DealDamage([alter_ego], 2, effect)
            Faces.RemoveAllFromGame([this], effect)

        def damage_per_event(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            events = [c for c in player.hand_cards.Get() if Event.IsType(c)]
            total = len(events)
            if total > 0:
                this.DealDamage([player.GetIdentity()], total, effect)
            if total < 3:
                ThisCardGainSurge(effect, None)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Kaine Parker and take 2 damage → remove Murderer's Guilt from the game",
                exhaust_and_remove,
            ),
            AbilityFactory.ForChoiceAbility(
                "Take 1 damage for each event in your hand. If less than 3 damage was taken this way, this card gains surge. Discard this obligation",
                damage_per_event,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            murderers_guilt,
        ),
    ]
