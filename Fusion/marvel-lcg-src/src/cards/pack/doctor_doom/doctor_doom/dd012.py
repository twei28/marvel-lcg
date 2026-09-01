from . import *

# Rescue Cynthia von Doom — obligation. Boost 2. GiveTo: Victor von Doom.
# Give to the Victor von Doom player.
# Flip to alter-ego form. You may not change form.
#  • Alter-Ego Action: Exhaust your identity and discard a TECH card you
#    control -> remove this card from the game.
#  • Alter-Ego Action: Exhaust your identity -> discard this card.
#
# Cartes de reference : aa014 Chaotic Forces et bt019 Unfinished Projects —
# meme squelette `WhenThisObligationGiveToYou`, meme asymetrie des deux
# branches (l'une RETIRE DE LA PARTIE, l'autre DEFAUSSE, donc la carte
# reviendra).
#
# ⚠ « FLIP to alter-ego form », pas « you MAY flip » : le changement de forme
# est FORCE. On n'utilise donc PAS le helper `YouMayFlipToYourAlterEgoForm`
# (aa014, bt019) mais `ChangeToForm(AlterEgo, effect)` directement — meme
# lecture que vp011, dont le journal venompool note « You MUST flip ».
#
# ⚠ « You may not change form » : tant que l'obligation est en jeu, le joueur
# est bloque en alter-ego. C'est ce qui donne son prix aux deux branches.
# Rendu par `PlayersCannotChangeForms(NonKeyword, "You")`, modele iw015
# (pack invisible_woman) qui bloque de la meme facon toute la table.
#
# ⚠ Les deux branches sont des ACTIONS d'alter-ego, pas des puces d'un
# `ChooseAbilities` : elles restent disponibles tant que la carte est en jeu,
# et le joueur choisit quand les payer. C'est la difference de fond avec
# aa014/bt019, dont le choix est unique et immediat.

def GetAbilities() -> Sequence['Ability']:

    def rescue_cynthia(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)

        player = message.GetGaveToPlayer()
        if player is None:
            return
        identite = player.GetIdentity()
        if identite is not None and player.IsHero():
            identite.ChangeToForm(AlterEgo, effect)

    def retirer_de_la_partie(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        Faces.RemoveAllFromGame([this], effect)

    def defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            rescue_cynthia,
        ),
        AbilityFactory.PlayersCannotChangeForms(AbilityType.NonKeyword, "You"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            retirer_de_la_partie,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.Discard(trait="TECH", from_where=["YouControlCards"])),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            defausser,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
