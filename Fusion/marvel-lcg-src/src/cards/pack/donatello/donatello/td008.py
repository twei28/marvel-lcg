from . import *

# * Donnie's Lab — SOUTIEN, cout 1, [physical]. LOCATION. NYC. SEWERS.
# Alter-Ego Action: Exhaust Donnie's Lab -> add an ANDROID, ITEM, or TECH card
#   in your discard pile to your hand.
#
# CARTES DE REFERENCE
#  - `01034` Stark Tower : soutien `AlterEgoAction` + `CostFunc.Exhaust("This")`
#    qui rend une carte de la defausse a la main (`Faces.ReturnToHand`).
#  - `22034` Defensive Training / `27001b` : cible dans la DEFAUSSE du joueur =
#    `SetTarget(..., from_where=["YourDiscardPile"])`.
#  - `CardFinder(traits=[...])` : liste de traits en OU (finder.py:133).
#
# TEXTE CONTRE CODE
#  « ANDROID, ITEM, OR TECH card » -> N'IMPORTE LEQUEL des trois traits (OU),
#    sur n'importe quel type de carte (allie, amelioration, evenement...).
#  « in YOUR discard pile » -> `YourDiscardPile`. « add ... to your hand » ->
#    `ReturnToHand` (le choix de la carte est la selection de la cible).
#  « Alter-Ego Action » : injouable en forme heros.


def GetAbilities() -> Sequence['Ability']:

    def laboratoire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        Faces.ReturnToHand(effect.targets, joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            laboratoire,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(
            finder=CardFinder(traits=["ANDROID", "ITEM", "TECH"]),
            from_where=["YourDiscardPile"],
        ),
    ]
