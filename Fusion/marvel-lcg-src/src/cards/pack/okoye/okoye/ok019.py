from . import *

# Funeral Rites — OBLIGATION, give to the Okoye player.
# You may flip to alter-ego form. Choose:
# - Exhaust your alter ego and all DORA MILAJE allies you control -> remove
#   Funeral Rites from the game.
# - Exhaust 3 DORA MILAJE allies you control. If no ally was exhausted this
#   way, this card gains surge. Discard this obligation.
#
# Modele exact : kb014 (Family = Trouble), meme structure
# `AbilityFactory.WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm`
# + `player.ChooseAbilities` avec 2 branches. La deuxieme branche cible les
# allies via `canbe_exhaust=True` (CardFinder.KWArgs, deja utilise par
# CostFunc.Exhaust en interne), plafonne a 3 (`max=3`,
# Worlds.FindCardsOnField).


def GetAbilities() -> Sequence['Ability']:

    def funeral_rites(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def retirer_du_jeu(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            alter_ego = player.GetIdentity().GetAlterEgoFace()
            allies = Worlds.FindCardsOnField(effect, trait="DORA MILAJE", card_type=Ally)
            Faces.ExhaustAll([alter_ego] + allies, effect)
            Faces.RemoveAllFromGame([this], effect)

        def exhaustion_partielle(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            allies = Worlds.FindCardsOnField(
                effect, trait="DORA MILAJE", card_type=Ally, canbe_exhaust=True, max=3,
            )
            if allies:
                Faces.ExhaustAll(allies, effect)
            else:
                ThisCardGainSurge(effect, None)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust your alter ego and all Dora Milaje allies you control → remove Funeral Rites from the game",
                retirer_du_jeu,
            ),
            AbilityFactory.ForChoiceAbility(
                "Exhaust 3 Dora Milaje allies you control. If no ally was exhausted this way, this card gains surge. Discard this obligation",
                exhaustion_partielle,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            funeral_rites,
        ),
    ]
