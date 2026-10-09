from . import *

# hs111 Poisoned Dagger
# Attache a Kraven. Boost 2.
# Forced Response (etoile) : apres que Kraven attaque et blesse un personnage, ce personnage est confus.
# Interrupt : quand vous attaquez Kraven, defaussez une carte au hasard de votre main → defaussez cet attachement.

def GetAbilities() -> Sequence['Ability']:

    def cout(targets, effect) -> bool:
        joueur = effect.GetInitiator()
        return len(joueur.DiscardRandomHandCards(1, effect)) > 0

    def confondre(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        Faces.GiveStatus(list(message.damaged_targets), "Confused", effect)

    def blesse(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        return PorteurAttaque(effect, message) and len(message.damaged_targets) > 0

    return [
        AttacherALaRevelation(),
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, Villain, confondre, conditions=[blesse]),
        InterruptContrePorteur(None, CostFunc.Custom(None, cout)),
    ]
