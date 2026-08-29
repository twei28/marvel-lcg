from . import *

# "Rich Angel"
# DEFENSE. SONG.
# Hero Interrupt (defense): When you would take any amount of damage from an
#   attack, prevent all of that damage.
# Showtime!: Heal 2 damage from an identity.
#
# Squelette de Shield Block (rg004 / 03005), a une nuance pres qui compte :
# ici le texte dit « from an ATTACK », donc `is_from_attack=True`, alors que
# Shield Block prend n'importe quels degats.


def GetAbilities() -> Sequence['Ability']:

    def ange(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.PreventDamage("All", effect)

    def showtime(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Event)
        # Le joueur CHOISIT la cible : `ResolveAbility` prendrait sinon la
        # premiere cible legale sans rien demander (cf. CiblesShowtime).
        this.HealthUnits(CiblesShowtime(effect), 2, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            ange,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense'),
        Showtime(showtime).SetTarget(Identity, canbe_heal=True, range=(0, 1)),
    ]
