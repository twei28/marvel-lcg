from . import *

# Seething Rage — RESSOURCE [physical]. x2.
# Response: After you spend this card, heal 2 damage from Raphael and place 1
#   rage counter on him (to a maximum of 3).
#
# PHASE A : construit, jamais execute.
#
# CARTES DE REFERENCE
#  - `29009` Stroke of Genius (ironheart) : « Response: After you spend this
#    card » -> `AbilityFactory.AfterYouSpendThisCard(AbilityType.Response, op)`,
#    Reponse SIMPLE (pas `HeroResponse`), comme le texte imprime ici.
#  - `42018` Angel's Aerie : `this.HealthUnits(cibles, n, effect)` pour soigner.
#  - `tr001a` : la pose de rage, plafonnee a 3.
#
# TEXTE CONTRE CODE
#  ⚠ « Response » et NON « Hero Response » : la carte se depense (et repond)
#    aussi quand le joueur est en civil. Mais « Raphael » est la face HEROS :
#    en civil il n'y a ni soin ni rage. TODO-QUESTION Q2 (voir __init__).
#  ⚠ « heal 2 damage FROM RAPHAEL » : le heros, pas un autre personnage.
#  ⚠ « (to a maximum of 3) » : imprime ICI, donc `plafonne=True`.
#  ⚠ « After you SPEND this card » : declenche a la depense comme ressource,
#    pas a la pose en main/defausse. Une ressource depensee pour jouer une
#    carte declenche le message `AfterCardsBeSpendAsResource`.
#  Pas de [star], pas de limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def rage_bouillonnante(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        heros = HerosDuJoueur(effect, joueur)
        if heros is None:
            return
        this.HealthUnits([heros], 2, effect)
        PlacerRage(effect, joueur, plafonne=True)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            rage_bouillonnante,
        ),
    ]
