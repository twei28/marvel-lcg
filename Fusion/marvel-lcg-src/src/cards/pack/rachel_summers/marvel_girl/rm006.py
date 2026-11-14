from . import *

# Telekinetic Counterblast (x2) — EVENEMENT, cout 1 (physique), ATTACK. DEFENSE. PSIONIC.
# Hero Response (attack): After an enemy attacks you, make a basic attack against that enemy without exhausting. Your hero
# gets +3 ATK for this attack.
#
# CARTES DE REFERENCE : `al014` Lurking (`heros.BasicAttack([cible], effect, property=AttackProperty(additional_value=N))` :
# attaque de base SANS inclinaison et avec un bonus d'ATQ pour cette attaque), `36012` (`AfterUnitAttackYou`).
#
# MOTS-PIEGES : « that enemy » = l'attaquant (`message.attacker`), encore en jeu ; « without exhausting » = `BasicAttack`.
def GetAbilities() -> Sequence['Ability']:
    def telekinetic_counterblast(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        heros = initiator.GetIdentity()
        attaquant = message.attacker
        if heros is None or attaquant is None or not attaquant.IsInPlay():
            return
        heros.BasicAttack([attaquant], effect, property=AttackProperty(additional_value=3))

    return [
        AbilityFactory.AfterUnitAttackYou(
            AbilityType.HeroResponse,
            Enemy,
            telekinetic_counterblast,
        ).SetPlay().SetLabel('attack'),
    ]
