from . import *

# * Marine Patrol — evenement signature, x2 (5-6/15). THWART. SUPERPOWER.
# Cout 1.
# Hero Action (thwart): Remove 2 threat from a scheme. Flip up to 2 cards in
# your Rising Tide area facedown. For each card flipped this way, choose
# (max 1 each): remove 2 threat from a scheme. draw 1.
#
# ⚠ « max 1 each » : chaque branche n'est offerte qu'UNE fois au total sur
# les deux retournements possibles, pas une fois PAR carte -- avec deux
# cartes et deux branches, retourner les deux force donc a prendre chaque
# branche exactement une fois. Modele du choix repete sans reemploi : boucle
# sur les cartes retournees, `ForChoiceAbility` construit a chaque tour avec
# seulement les branches encore disponibles (retirees de la liste des qu'une
# est choisie). Modele du choix modal lui-meme : aa004 Wake Thy Power.
# « Flip up to 2 cards » (pas « faceup cards ») : seule lecture sensee, vu la
# suite (« ... facedown »), est de retourner des cartes face visible -- une
# carte deja face cachee ne peut pas etre retournee « facedown ».

def GetAbilities() -> Sequence['Ability']:

    def marine_patrol(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        if not isinstance(initiator, Player):
            return

        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

        retournees = RetournerCartesRisingTide(
            effect, initiator, face_visible=True, minimum=0, maximum=2,
            prompt="Flip up to 2 cards in your Rising Tide area facedown",
        )
        if not retournees:
            return

        options_restantes: List[str] = ["threat", "draw"]

        def menace(cibles: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(cibles, 2, effect)
            options_restantes.remove("threat")

        def pioche(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            initiator.DrawUp(1, effect)
            options_restantes.remove("draw")

        for _ in retournees:
            choix: List['Ability'] = []
            if "threat" in options_restantes:
                choix.append(AbilityFactory.ForChoiceAbility(
                    "Remove 2 threat from a scheme", menace,
                ).SetTarget(Scheme2))
            if "draw" in options_restantes:
                choix.append(AbilityFactory.ForChoiceAbility(
                    "Draw 1 card", pioche,
                ))
            if not choix:
                break
            initiator.ChooseAbilities(effect, *choix)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            marine_patrol,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
