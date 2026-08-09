from . import *

# * Mysterio — custom « Rainy » (nemesis de Peter Parker)
# Enters play with 2 illusion counters.
# Forced Interrupt: When Mysterio would take damage, remove an illusion
#   counter from here instead.
# [star] Forced Response: After Mysterio activates against you and deals
#   damage or places threat, deal yourself a facedown encounter card.

def GetAbilities() -> Sequence['Ability']:

    def illusion_au_lieu_des_degats(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Minion)
        message.PreventDamage("All", effect)
        Faces.RemoveCountersOn([this], 1, 'illusion', effect)

    def a_une_illusion(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return effect.this.GetCounters('illusion') > 0

    def carte_rencontre_apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        player = message.GetToPlayer()
        if player:
            player.DealEncounterCards(1, effect)

    def carte_rencontre_apres_intrigue(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Minion)
        player = this.GetEngagedPlayer()
        if player:
            player.DealEncounterCards(1, effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, 'illusion'),

        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "This",
            illusion_au_lieu_des_degats,
            conditions=[a_une_illusion],
        ),

        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "This",
            "You",
            carte_rencontre_apres_attaque,
            dealt_damage=True,
        ),

        AbilityFactory.AfterEnemySchemeAndPlaceThreat(
            AbilityType.ForcedResponse,
            "This",
            Scheme2,
            carte_rencontre_apres_intrigue,
        ),
    ]
