from . import *

# Nigh-Invulnerability : EVENEMENT (DEFENSE. SPLIT. SUPERPOWER.), cout 1, [physical]. Classe Hero. (x2)
# Hero Interrupt (defense): When an enemy attacks, declare Sentry the defender without exhausting him. Give him a tough status card (stun the attacker if there are 3+ balance counters in play).
# Special: Give the Void a tough status card. The Void cannot take damage this phase.
#
# CARTES DE REFERENCE
#  - `se011` / `56047` : fabrique `WhenUnitWouldAttack(HeroInterrupt, Enemy, op)` avec `.SetPlay()`, le label « defense », puis la cible « YourHero » (le label vient AVANT la cible) ; declaration : `message.DeclareDefender(heros, effect)`.
#  - Statuts : `Faces.GiveStatus(cibles, "Tough"/"Stunned", effect)`. Special : `RegisterTemp(WhenUnitWouldTakeDamage(Temp0, ..), unregister_after_exec=False, until_phase_end=True)` + `PreventDamage("All")` (RECETTES §26).
#
# TEXTE CONTRE CODE
#  « WITHOUT EXHAUSTING him » : la declaration ne depense pas la defense du heros. « Give HIM a tough status card » : Sentry (le defenseur). « stun THE ATTACKER if 3+ counters IN PLAY » : l'ennemi qui attaque. Special : le Void gagne Tough et ne subit
#  AUCUN degat jusqu'a la fin de la PHASE ; sans Void en jeu, rien. Chiffres : cout 1.


def GetAbilities() -> Sequence['Ability']:

    def defendre(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        cibles = [t for t in effect.targets if t is not None]
        if not cibles:
            return
        heros = cibles[0]
        message.DeclareDefender(heros, effect)
        Faces.GiveStatus([heros], "Tough", effect)
        if EquilibreEnJeu(effect) >= 3:
            Faces.GiveStatus([message.trigger], "Stunned", effect)

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        void = VoidEnJeu(effect)
        if void is None:
            return
        Faces.GiveStatus([void], "Tough", effect)

        def aucun_degat(e: 'Effect', m: 'Message.WhenUnitWouldTakeDamage') -> None:
            m.PreventDamage("All", e)

        effect.this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.Temp0, CardFinder(name=NOM_VOID), aucun_degat),
            unregister_after_exec=False,
            until_phase_end=True,
        )

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.HeroInterrupt, Enemy, defendre).SetPlay().SetLabel('defense').SetTarget("YourHero"),
        AbilityFactory.WhenResolveSpecialAbility("This", special).NoOutOfPlayLimit(),
    ]
