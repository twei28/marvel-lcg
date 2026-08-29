from . import *

# Performance Anxiety — obligation d'Alison Blaire
# Give to the Alison Blaire player.
# You may flip to alter-ego form.
# You cannot use your Songwriter ability or use the 'Hero Action' on Live
#   Concert.
# Action: Exhaust your identity and discard a support or upgrade you control ->
#   remove this obligation from the game.
#
# Gabarit : Caged Bird (rg012), l'obligation de Red Guardian, qui reste en jeu
# et se retire par une action a cout.
#
# L'INTERDIT n'est PAS code ici. Le moteur ne sait pas eteindre une capacite
# nommee portee par une autre carte ; on le verifie donc a la source, dans
# `dz001b` (Songwriter) et `dz017a` (Hero Action de Live Concert), via le
# helper `AngoisseEnJeu`. C'est le meme choix que pour le ciblage de Wolverine :
# la contrainte vit la ou elle s'applique.
#
# « Action » et non « Alter-Ego Action » : la carte se retire dans les deux
# formes, contrairement a Caged Bird.


def GetAbilities() -> Sequence['Ability']:

    def donnee(effect: 'Effect',
               message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)
        joueur = message.GetGaveToPlayer()
        if joueur is None or not joueur.IsInHeroForm():
            return

        # « YOU MAY flip » : le choix reste offert, jamais force.
        def basculer(targets: Sequence['CardFace']) -> None:
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.ChangeToForm(AlterEgo, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility("Flip to alter-ego form", basculer),
        )

    def se_retirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            donnee,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            se_retirer,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.Discard(
            "YouControlCards", card_type=Support | Upgrade)),
    ]
