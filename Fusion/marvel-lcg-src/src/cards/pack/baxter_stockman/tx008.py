from . import *

# Radical Ingenuity — TRAITRISE (Baxter's Lab 12/22, x3). 2 boosts.
# When Revealed: Choose:
#  • Resolve the "Special" ability on Baxter's Laboratory.
#  • Place 2 threat on the main scheme.
#
# Cartes de reference : `Player.ChooseAbilities(effect, ForChoiceAbility(...), ...)` (RECETTES §2,
# 08013 / 16155) pour « Choose » ; `tx004b` pour le Special ; `this.PlaceThreatOnSchemes("MainScheme", n)`.
#
# Mots-pieges : « Choose » = UNE des deux puces ; « Resolve the Special » : par le joueur a qui la
# carte est revelee (« engaged with YOU »), jamais par tous.


def GetAbilities() -> Sequence['Ability']:

    def choisir(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Resolve the \"Special\" ability on Baxter's Laboratory",
                lambda cibles: ResoudreLeSpecial(effect, joueur),
            ),
            AbilityFactory.ForChoiceAbility(
                "Place 2 threat on the main scheme",
                lambda cibles: this.PlaceThreatOnSchemes("MainScheme", 2, effect),
            ),
        )

    return [AbilityFactory.WhenThisRevealed(None, choisir)]
