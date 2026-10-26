from . import *

# * U.S. Agent's Shield — amelioration unique, cout 1, ressource [physical]. ITEM. WEAPON.
# Restricted.
# Hero Interrupt: When you are attacked by an enemy, exhaust U.S. Agent's Shield → deal 2 damage to the attacker or
# prevent 1 damage from this attack.
#
# Cartes de reference :
#  - `05012` Nova : « When an enemy initiates an attack against you » = `WhenUnitInitiatesAttackAgainst(Interrupt, Enemy,
#    "You", op)` + cible `"Attacker"` ; la meme fenetre permet de VAINCRE l'attaquant avant qu'il ne frappe.
#  - `45040` Magic Barrier : `message.PreventDamage(N, effect)` sur ce meme message (« prevent N damage from this attack »).
#  - RECETTES §2 « Choix secondaire » : `joueur.ChooseAbilities(effect, ForChoiceAbility(...), ForChoiceAbility(...))`.
#
# ⚠ Mots-pieges :
#  - « deal 2 damage to the attacker OR prevent 1 damage » : UN SEUL des deux, au choix du joueur (jamais les deux).
#  - « When YOU are attacked » : attaque dirigee contre ce joueur (son heros ou son identite), pas contre un allie.
#  - « by AN ENEMY » : villain ou sbire.
#  - Restricted : natif (`desc.Restricted`).


def GetAbilities() -> Sequence['Ability']:

    def us_agents_shield(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        attaquant = message.attacker

        def blesser_l_attaquant(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            if attaquant is not None:
                this.DealDamage([attaquant], 2, effect)

        def prevenir_un_degat(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            message.PreventDamage(1, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Deal 2 damage to the attacker", blesser_l_attaquant),
            AbilityFactory.ForChoiceAbility("Prevent 1 damage from this attack", prevenir_un_degat),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitInitiatesAttackAgainst(
            AbilityType.HeroInterrupt,
            Enemy,
            "You",
            us_agents_shield,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
