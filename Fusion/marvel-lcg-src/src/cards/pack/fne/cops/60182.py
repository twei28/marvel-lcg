from . import *

# Cop (POLICE) — Quickstrike, Vulnerable : bases automatiques.
# [star] Forced Interrupt: When Cop would scheme, it attacks the villain instead.
# When Defeated: Place 2 threat on the main scheme.
#
# « instead » = message.SetBeInstead sur WhenUnitWouldScheme (RECETTES §2),
# puis une attaque de base contre le vilain (BasicAttack, modele 50096 Leaping
# Kick pour un ennemi qui frappe une unite precise).

def GetAbilities() -> Sequence['Ability']:

    def attaque_le_vilain(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        this = effect.this.CastTo(Minion)
        message.SetBeInstead(effect)
        vilain = Worlds.FindVillain(effect)
        if vilain:
            this.BasicAttack([vilain], effect)

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    return [
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.ForcedInterrupt,
            "This",
            attaque_le_vilain,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            vaincu,
        ),
    ]
