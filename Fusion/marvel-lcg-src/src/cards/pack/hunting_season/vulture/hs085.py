from . import *

# hs085 * Armadillo
# Forced Response : apres avoir attaque et blesse un personnage, celui-ci gagne AERIAL jusqu'a la fin de la ronde.
# Boost : si l'attaque vous blesse, vous gagnez AERIAL jusqu'a la fin de la ronde.

def GetAbilities() -> Sequence['Ability']:

    def a_blesse(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        return len(message.damaged_targets) > 0

    def planer(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        for cible in list(message.damaged_targets):
            GagnerAerialJusquaLaRonde(cible, effect)

    def en_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        SiLAttaqueVousBlesse(
            effect, message,
            lambda joueur, degats: GagnerAerialJusquaLaRonde(joueur.GetIdentity(), effect))

    return [
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "This", planer, conditions=[a_blesse]),
        AbilityFactory.WhenCardBecomeBoost("This", en_boost, during_attack=True),
    ]
