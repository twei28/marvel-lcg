from . import *

# hs113 Hunting Rifle
# Attache a Kraven.
# Forced Response : apres que Kraven vous attaque et que vous ne subissez aucun degat, 1 degat a votre identite.
# Interrupt : quand vous attaquez Kraven, depensez 2 ressources quelconques → defaussez cet attachement.

def GetAbilities() -> Sequence['Ability']:

    def aucun_degat(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        joueur = message.GetAgainstPlayer()
        if joueur is None or not PorteurAttaque(effect, message):
            return False
        identite = joueur.GetIdentity()
        return identite in message.attacked_targets and identite not in message.damaged_targets

    def piquer(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        effect.this.DealDamage([message.GetAgainstPlayer().GetIdentity()], 1, effect)

    return [
        AttacherALaRevelation(),
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, Villain, piquer, conditions=[aucun_degat]),
        InterruptContrePorteur(Cost("2")),
    ]
