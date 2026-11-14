from . import *

# Position du heros, face b (Atop the Tenshu). HERO POSITION.
# First Player Action : resoudre UN des effets ci-dessous, puis retourner cette carte :
#  • infliger 3 degats a votre identite ;
#  • depenser [energy][energy] ;
#  • defausser un allie ou une amelioration que vous controlez.
# Cartes de reference : voir sl004a (+ fne/art_museum_heist/60127 pour Cost("YY")).
# ⚠ Mots-pieges : « an ally or upgrade you control » = l'un des deux types, a votre controle (pas la main) ; JAMAIS une carte PERMANENTE (`canbe_discard=True`) : la Creeping Corruption (sl072)
#  est une amelioration Permanent et le moteur plante (assert `is_eliminated`) si on la defausse, trouve en autoplay le 22/10/2026 ; mêmes regles de retournement que sl004a.


def GetAbilities() -> Sequence['Ability']:

    def branches(effect: 'Effect', joueur: 'Player', retourner: Callable[[], None]) -> Sequence['Ability']:
        this = effect.this

        def trois_degats(targets: Sequence['CardFace']) -> None:
            this.DealDamage([joueur.GetIdentity()], 3, effect)
            retourner()

        def deux_energies(targets: Sequence['CardFace'], res: 'Resources') -> None:
            retourner()

        def defausser_allie_ou_amelioration(targets: Sequence['CardFace']) -> None:
            Faces.DiscardAll(targets, effect)
            retourner()

        return [
            AbilityFactory.ForChoiceAbility("Deal 3 damage to your identity", trois_degats),
            AbilityFactory.ForChoiceAbilityWithCost(Cost("YY"), "Spend [energy][energy] resources", deux_energies,
                                                    conditions=[lambda e, m: PeutCouvrirLeCout(joueur, e, Cost("YY"))]),
            AbilityFactory.ForChoiceAbility("Discard an ally or upgrade you control", defausser_allie_ou_amelioration)
            .SetTarget(finder=CardFinder(card_type=Ally|Upgrade, canbe_discard=True), from_where=["YouControlCards"], range=(1, 1)),
        ]

    return [ActionPositionHeros(branches)]
