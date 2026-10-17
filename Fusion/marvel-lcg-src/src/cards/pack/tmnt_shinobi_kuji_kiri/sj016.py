from . import *

# QNA Restoration (sj016), Kuji-Kiri, evenement SPELL (Inkwire, TMNT Shinobi).
# Hero Action: Choose a player. Heal 2 damage from that player's identity. That player may choose 1 card in
# their discard pile and shuffle it into their deck.
#
# Cartes de reference : `gmw/the_market/16176` Tried and True (« Choose a player. That player may ... from their
# discard pile » : `SetTarget("Players")`, `player.MayChooseOneAbility(... SetTarget(from_where=["YourDiscardPile"]))`) ;
# `sm/ghost_spider/27008` (`Faces.ShuffleAllTo(cartes, player.player_deck, effect)`) ; `HealthUnits` (cd004).
#
# TEXTE CONTRE CODE
#  ⚠ « Choose A PLAYER » : n'importe quel joueur, vous compris ; « THAT PLAYER'S identity » : l'identite du
#    joueur choisi (pas la votre) ; « Heal 2 » : jusqu'a 2.
#  ⚠ « THAT player MAY choose 1 card in THEIR discard pile » : facultatif, c'est le joueur choisi qui decide,
#    dans SA defausse, et la carte est MELANGEE dans SON deck (pas posee dessus).


def GetAbilities() -> Sequence['Ability']:

    def qna_restoration(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        for cible in effect.targets:
            joueur = cible.GetControlByPlayer()
            this.HealthUnits([joueur.GetIdentity()], 2, effect)

            def melanger(cartes: Sequence['CardFace'], joueur: 'Player' = joueur) -> None:
                Faces.ShuffleAllTo(cartes, joueur.player_deck, effect)

            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Shuffle a card from your discard pile into your deck",
                    melanger,
                ).SetTarget(from_where=["YourDiscardPile"]),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            qna_restoration,
        ).SetPlay()
        .SetTarget("Players")
        .SetHasNoTargetEffect(),
    ]
