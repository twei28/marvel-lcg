from . import *

# Crooked Cop (CRIMINAL, POLICE) — Quickstrike, Vulnerable : bases automatiques.
# When Defeated: The defeating player deals themself 1 facedown encounter card.
# [star] Boost: Take 2 indirect damage.
#
# Modeles : 27080 Lashing Out (TakeIndirectDamage en boost), message
# WhenUnitBeDefeated.GetDefeatingPlayer().

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        joueur = message.GetDefeatingPlayer()
        if joueur:
            joueur.DealEncounterCards(1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        message.GetToPlayer().GetIdentity().TakeIndirectDamage(this, 2, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            vaincu,
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
