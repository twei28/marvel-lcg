from . import *

# * Willow (Willow Rosenberg) — ALLIE (MYSTIC), cout 3, [wild]. THW 1*, ATQ 1*, PV 3. Classe Basic.
# [star] Response: After Willow uses a basic power, spend a: [mental] resource → remove 2 threat from a scheme.
#   [physical] resource → deal 2 damage to an enemy. [energy] resource → heal 2 damage from Willow.
#
# CARTES DE REFERENCE
#  - `49013` Kid Omega : `ChooseAbilities(.., ForChoiceAbilityWithCost(Cost("Y"), libelle, op).SetTarget(..), ..)` pour « spend a [x] resource → ... ».
#  - `AfterUnitUseBasicPower(Response, "This", op, powers=[..])` (14001a, 04032) pour « after X uses a basic power » ; le [star] imprime est une
#    convention d'impression, pas un `NonKeywordStar` (RECETTES-MOTEUR §1).
#
# TEXTE CONTRE CODE
#  « uses a basic power » -> ATQ ET CTR (Willow n'a pas de DEF d'allie). « spend a » + trois branches -> UNE seule, payee par UNE ressource du type
#    de la branche. « heal 2 damage from Willow » -> elle-meme, pas de cible.


def GetAbilities() -> Sequence['Ability']:

    def willow(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        joueur = effect.GetInitiator()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("B"),
                "Spend a [mental] resource → remove 2 threat from a scheme",
                lambda targets, res: this.RemoveThreatFromSchemes(targets, 2, effect),
            ).SetTarget(Scheme2),
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("R"),
                "Spend a [physical] resource → deal 2 damage to an enemy",
                lambda targets, res: this.DealDamage(targets, 2, effect),
            ).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("Y"),
                "Spend a [energy] resource → heal 2 damage from Willow",
                lambda targets, res: this.HealthUnits([this], 2, effect),
            ),
        )

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            willow,
            powers=["ATK", "THW"],
        ),
    ]
