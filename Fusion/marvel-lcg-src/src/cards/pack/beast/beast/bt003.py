from . import *

# * Phoenix — Jean Grey. Allie signature. PSIONIC. X-MEN. Cout 3, 4 PV.
# When Defeated: Deal 2 damage to an enemy.
#
# Carte de reference : bt002 * Wonder Man, du meme pack — texte identique au
# mot pres, seuls le nom, les traits et l'illustration changent. La carte
# imprimee la numerote « 1B/15 » quand Wonder Man est « 1/15 » : l'auteur en
# fait deux versions du meme emplacement (voir le journal de portage,
# .planning/todos/2026-08-31-portage-beast.md §3, point 3).
#
# Modele d'origine, remonte via bt002 : 44013 Dogpool.

def GetAbilities() -> Sequence['Ability']:

    def phoenix(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            phoenix
        ).SetTarget(Enemy),
    ]
