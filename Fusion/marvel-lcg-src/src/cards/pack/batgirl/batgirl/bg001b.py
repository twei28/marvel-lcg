from . import *

# * Barbara Gordon — alter ego. « Eidetic Memory — Action: Choose a resource type. Put the bottommost card with a printed
# resource of that type from your discard pile on top of your deck. If you defeated an enemy or removed the last threat from a
# scheme this round, draw 1 card. (Limit once per round.) »
# Cartes de reference : `40044` Pip the Pug (Faces.MoveAllTo(.., joueur.player_deck) = « on top of your deck »), `01027` Focused Rage
# (`DrawUp(1)` = piocher 1 carte), `world.stat.AddRoundCounter` (CORRECTIF pack sq) pour le registre « ce round ».


def GetAbilities() -> Sequence['Ability']:

    def eidetic_memory(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def choisir(couleur: str):
            def appliquer(targets) -> None:
                cartes = [f for f in joueur.discard_pile.GetAll()
                          if ClassCard.IsType(f) and f.printed_resource.HasColorPrinted(couleur)]
                if cartes:
                    # « bottommost » : la plus ANCIENNE de la defausse (le dessus de la pile est la derniere defaussee).
                    Faces.MoveAllTo([cartes[0]], joueur.player_deck, effect)
                if ExploitCeRound(joueur, effect):
                    joueur.DrawUp(1, effect)
            return appliquer

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("[physical]", choisir("R")).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility("[mental]", choisir("B")).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility("[energy]", choisir("Y")).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            eidetic_memory,
        ).SetName("Eidetic Memory").LimitOncePerRound(),
        *SuivisDeLaManche(),
    ]
