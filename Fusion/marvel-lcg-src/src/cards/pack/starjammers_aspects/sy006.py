from . import *
# * Raza Longknife (Basic, allie 3 [physical], 1*/2*, PV 3). CYBORG. STARJAMMER.
# Raza Longknife gets +1 hit point for each upgrade attached to him.
#
# Cartes de reference : 12011 Ant-Man (`ThisGainKeyword(fn, health=1, change_on_event=...)` ; la valeur se relit a chaque
# changement) ; rl001a (`change_on_event=OnEvent.AttachedMove(Upgrade)`). `GetAttachedUpgrades()` : les ameliorations ATTACHEES a la
# carte (pas celles posees pres de l'identite).
def GetAbilities() -> Sequence['Ability']:
    def raza(effect: 'Effect', ui: List['CardFace']) -> int:
        ameliorations = [u for u in effect.this.GetAttachedUpgrades() if u is not None]
        ui.extend(ameliorations)
        return len(ameliorations)
    return [
        AbilityFactory.ThisGainKeyword(
            raza,
            health=1,
            change_on_event=OnEvent.AttachedMove(Upgrade),
        ),
    ]
