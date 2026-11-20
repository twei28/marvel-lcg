from . import *

# * Infiltration (MANIGANCE ANNEXE DE JOUEUR) : cout 0, [mental], menace 6 (fixe), Victory 0.
# Characters other than Mystique cannot remove threat from Infiltration.
# When Defeated: Choose to deal 5 damage to an enemy or remove 3 threat from a scheme.
# While Infiltration is in the victory display, Mystique ignores the guard and patrol keywords.   (FR 1.1.1 ; l'EN beta ajoute « and the crisis icon » : le FR prime)
#
# CARTES DE REFERENCE
#  - `40006` Technovirus Purge (cable) : `ThreatCannotBeRemovedFromWhile("This", by_character=CardFinder(non_name=..))` pour « characters other than X cannot remove threat from this card ».
#  - `42017` Render Medical Aid : `WhenSchemeBeDefeated(WhenDefeated, "This", op)` sur une manigance annexe de joueur.
#  - la capacite « en vitrine de victoire » est posee sur l'IDENTITE (`my001a`, RECETTES §3bis) : le script de cette carte ne la porte pas.
#
# TEXTE CONTRE CODE
#  « Characters OTHER THAN MYSTIQUE cannot remove threat » : seuls les effets dont la source est Mystique retirent de la menace (Unnoticed, Civilian de Mystique...) ; un allie, un autre heros, ne peuvent pas.
#    « Victory 0 » : lu dans `desc`. « CHOOSE to deal 5 damage to an enemy OR remove 3 threat from a scheme » : UNE branche, au choix du joueur qui la vainc. « While in the victory display » : sur my001a.
#  Chiffres : cout 0, menace 6, 5 degats, 3 menaces.


def GetAbilities() -> Sequence['Ability']:

    def une_fois_dejouee(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 5 damage to an enemy",
                lambda cibles: this.DealDamage(cibles, 5, effect),
            ).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                "Remove 3 threat from a scheme",
                lambda cibles: this.RemoveThreatFromSchemes(cibles, 3, effect),
            ).SetTarget(Scheme2),
        )

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            by_character=CardFinder(non_name=NOM_MYSTIQUE),
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            une_fois_dejouee,
        ),
    ]
