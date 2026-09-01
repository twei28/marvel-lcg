from . import *

# * Wonder Man — Simon Williams. Allie signature. AVENGER. Cout 3, 4 PV.
# When Defeated: Deal 2 damage to an enemy.
#
# Carte de reference :
#  - « When Defeated » sur un ALLIE qui inflige des degats : 44013 Dogpool
#    (« When Defeated: Deal 1 damage to an enemy »), meme structure exacte,
#    `WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", op).SetTarget(Enemy)`.
#    Comparable parce que le declencheur (l'allie lui-meme est vaincu) et
#    l'effet (degats a un ennemi au choix) sont les memes ; seule la valeur
#    change, 2 au lieu de 1.
#
# ⚠ `WhenDefeated` (le type de capacite) n'est PAS `AfterUnitDefeatedUnit`
# (l'allie a vaincu quelqu'un) : ici c'est l'allie qui TOMBE. Le mot imprime
# est « When Defeated », la carte parle bien de sa propre mort.

def GetAbilities() -> Sequence['Ability']:

    def wonder_man(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            wonder_man
        ).SetTarget(Enemy),
    ]
