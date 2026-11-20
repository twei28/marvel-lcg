from . import *

# * Auto-9 : AMELIORATION (TECH. WEAPON.), cout 2, [physical]. Restricted. Unique.
# Hero Action (attack): Exhaust Auto-9 and spend 1 resource of any type → deal 2 damage to an enemy. This attack gains ranged.
#
# CARTES DE REFERENCE
#  - `33001a` Cyclops « Optic Blast » : Action d'attaque nommee, `SetName(..)` + `SetCost(Cost("1"))` (une ressource de n'importe quel type) + `SetTarget(Enemy)` ;
#    le NOM permet a `Internal Reload System` (rc006) de cibler « Auto-9's ability » (`CanGenerateResources(for_ability=..)`, modele `33003` Ruby Quartz Visor).
#  - `01053` Relentless Assault : `hero.DealDamage(.., property=AttackProperty(ranged=True))` pour « this attack gains ranged ».
#  - `Restricted` : lu dans `desc` (base automatique, fiche `mots-cles/restricted.md`).
#
# TEXTE CONTRE CODE
#  « Exhaust Auto-9 AND spend 1 resource of ANY type » : deux couts, tous deux obligatoires. « deal 2 damage to AN enemy » : une cible, vilain ou sbire.
#  « This attack gains ranged » : propriete de CETTE attaque (ignore Riposte). Hero Action : forme heros seulement.
#  Chiffres : cout 2, 2 degats.


def GetAbilities() -> Sequence['Ability']:

    def auto_9(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        hero = effect.GetInitiator().GetHero()
        hero.DealDamage(effect.targets, 2, effect, property=AttackProperty(ranged=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            auto_9,
        ).SetLabel('attack')
        .SetName(NOM_AUTO_9)
        .SetCost(Cost("1"))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
    ]
