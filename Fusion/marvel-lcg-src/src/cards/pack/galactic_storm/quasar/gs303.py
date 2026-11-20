from . import *

# Flight of Light — evenement signature (QUASAR 3/16 et 4/16, x2). THWART.
# Cout 2, [physical].
# Hero Action (thwart): Remove 3 threat from a scheme. If this removes the last
#   threat from that scheme, remove 2 threat from a scheme.
#
# Cartes de reference :
#  - **`sh019`** Sideswipe : `RemoveThreatFromSchemes(cibles, n, effect,
#    if_this_remove_last_threat=fn)` (RECETTES §13), le rappel note que la
#    premiere menee a vide la manigance ; ne PAS copier `04049` (teste
#    `threat == 0` apres coup : une manigance annexe videe QUITTE le jeu).
#  - **`08013`** / `16155` : seconde cible choisie DANS l'operation par
#    `ChooseAbilities(ForChoiceAbility(...).SetTarget(Scheme2))` (RECETTES §2).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « If this removes the LAST threat from THAT scheme » : la premiere
#    manigance, apres le retrait de 3 (pas « si elle avait 3 ou moins » : une
#    manigance a 0 au depart ne declenche rien, aucune menace retiree).
#  - « remove 2 threat from A scheme » : une SECONDE cible, choisie apres coup,
#    n'importe quelle manigance (la meme est possible si c'est le complot
#    principal, qui reste en jeu a 0 ; une annexe videe a quitte le jeu).
#    Le second retrait est un contre du meme evenement (libelle thwart).
#  - « Hero Action (thwart) » : `SetLabel('thwart')`.


def GetAbilities() -> Sequence['Ability']:

    def envol(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        derniere = [False]

        def noter(*args):
            Unused(args)
            derniere[0] = True

        this.RemoveThreatFromSchemes(effect.targets, 3, effect, if_this_remove_last_threat=noter)
        if not derniere[0]:
            return
        joueur = effect.GetInitiator()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 2 threat from a scheme",
                lambda cibles: this.RemoveThreatFromSchemes(cibles, 2, effect),
            ).SetLabel('thwart').SetTarget(Scheme2),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            envol,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
