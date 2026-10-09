from . import *

# hs151 * Vulture (James Natale)
# Quickstrike. Villainous (natifs).
# Forced Response : apres avoir attaque et blesse l'identite, defaussez autant de cartes du dessus du deck que de degats subis.

def GetAbilities() -> Sequence['Ability']:

    def blesse(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        return message.total_dealt_damage > 0 and effect.this in [w.attacker for w in message.would_atk_messages]

    def defausser(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        joueur = message.GetAgainstPlayer()
        joueur.DiscardDeckTopCards(message.total_dealt_damage, effect)

    return [
        AbilityFactory.UniqueRuleNotApplyTo("This"),
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "This", defausser, conditions=[blesse]),
    ]
