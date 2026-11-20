from . import *
def GetAbilities() -> Sequence['Ability']:
    def contre_un_personnage_abime(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        cibles = getattr(message, "targets", None) or []
        return any(getattr(c, "sustained", 0) >= SEUIL_DEGATS for c in cibles)
    def villainous_pour_cette_activation(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        # Villainous = une carte de boost a chaque activation (fiche mots-cles/villainous.md) : une carte de plus pour CETTE attaque.
        message.GiveAdditionalBoostCardForThisActivation(1, effect)
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GainBoostIcon(Worlds.GetVillainStage(effect), effect)
    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            villainous_pour_cette_activation,
            conditions=[contre_un_personnage_abime],
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
