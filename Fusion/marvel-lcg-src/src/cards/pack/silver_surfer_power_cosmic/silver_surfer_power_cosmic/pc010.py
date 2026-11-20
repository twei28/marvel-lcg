from . import *

# Surfin' — EVENEMENT. ATTACK. POWER COSMIC. Cout 1, ressource [physical].
# x2 (pc010, 2 exemplaires).
#
# Texte imprime : « Hero Action (attack): Exhaust Cosmic Surfboard → deal 9
# damage to an enemy. You may spend a [physical] resource to give this
# attack overkill. »
#
# CARTES DE REFERENCE
#  - `CostFunc.Exhaust(name="Cosmic Surfboard")` (pc001b) : incliner la carte
#    NOMMEE, pas « This ».
#  - `ls005` To Arms! : `MayChooseOneAbility(ForChoiceAbilityWithCost(...))`
#    pour un cout FACULTATIF.
#  - `AttackProperty(overkill=...)` (can_attack.py) : doit etre fixe AVANT
#    `DealDamage`, donc le choix facultatif se resout D'ABORD.


def GetAbilities() -> Sequence['Ability']:

    def surfin(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        if not effect.targets:
            return
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        perforant = [False]

        def activer(cibles: Sequence['CardFace'], res: Any) -> None:
            Unused(cibles, res)
            perforant[0] = True

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("R"),
                "Give this attack overkill",
                activer,
            ),
        )
        this.DealDamage(effect.targets, 9, effect, property=AttackProperty(overkill=perforant[0]))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            surfin,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust(name="Cosmic Surfboard"))
        .SetTarget(Enemy),
    ]
