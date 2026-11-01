from . import *

# Dead or Alive (x3) : EVENEMENT (ATTACK), cout 2, [physical].
# Hero Response (attack): After a WEAPON upgrade you control deals damage to an enemy, deal 5 damage to that enemy. This attack gains overkill.
#
# CARTES DE REFERENCE
#  - `damage.py` `AfterUnitTookDamage` : `message.by_effect` est l'effet qui a inflige le degat ; `.this` = la carte qui l'a cause (l'arme, pas le heros).
#  - `01053` Relentless Assault : `hero.DealDamage(.., property=AttackProperty(overkill=True))` pour « this attack gains overkill ». `bf013` Stakeout : Reponse jouee
#    depuis la main sur « Trigger » (`.SetTarget("Trigger")`, `SetLabel('attack')`).
#
# TEXTE CONTRE CODE
#  « a WEAPON upgrade YOU control deals damage » -> la cause du degat est une amelioration WEAPON que ce joueur controle (ses propres effets d'arme, jamais ceux de
#    l'evenement lui-meme : pas de boucle). « to an enemy » -> la cible est le sbire ou vilain qui vient d'etre blesse (`Trigger`). « that enemy » : le meme.
#  Hero Response (sous-type dedie, forme heros). Chiffres : cout 2, 5 degats, overkill.


def GetAbilities() -> Sequence['Ability']:

    def dead_or_alive(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        hero = joueur.GetHero()
        hero.DealDamage(effect.targets, 5, effect, property=AttackProperty(overkill=True))

    def cause_par_une_arme(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> bool:
        cause = message.by_effect.this
        return ArmeDuJoueur(cause, effect.GetInitiator())

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.HeroResponse,
            Enemy,
            dead_or_alive,
            conditions=[cause_par_une_arme],
        ).SetPlay().SetLabel('attack')
        .SetTarget("Trigger"),
    ]
