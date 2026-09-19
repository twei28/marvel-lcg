from . import *

# * Stilt-Man (CRIMINAL UNDERLING) — SCH 1 / ATK 1 / 4 PV, boost 3.
# Enters play with 2 stilt counters on him.
# [star] Stilt-Man gets +1 SCH and +1 ATK for each stilt counter on him.
# Forced Interrupt: When Stilt-Man would take any amount of damage, remove 1
#   stilt counter from him instead.
# Modeles : sr015 Mysterio (compteurs a l'entree, degats remplaces tant qu'il
# reste un pion), dt133 (ThisGainKeyword dynamique, rafraichi par
# OnEvent.Counter("This", 'stilt')).

def GetAbilities() -> Sequence['Ability']:

    def pions(effect: 'Effect', ui: List['CardFace']) -> int:
        return effect.this.GetCounters('stilt')

    def a_un_pion(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return effect.this.GetCounters('stilt') > 0

    def un_pion_au_lieu(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage("All", effect)
        Faces.RemoveCountersOn([effect.this], 1, 'stilt', effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, 'stilt'),
        AbilityFactory.ThisGainKeyword(pions, attack=1, scheme=1, change_on_event=OnEvent.Counter("This", 'stilt')),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "This", un_pion_au_lieu, conditions=[a_un_pion]),
    ]
