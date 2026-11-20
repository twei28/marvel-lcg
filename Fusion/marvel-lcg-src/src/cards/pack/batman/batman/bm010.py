from . import *
# Grapple Gun — AMELIORATION cout 3 [energy]. ITEM. TECH. « Batman ignores the guard keyword and the patrol keyword. » Interrupt : when an enemy
# activates, exhaust Grapple Gun -> change your form.
# Reference : sm004 (`UnitIgnoreKeywordIcons`), 01025 Split Personality (`ChangeToOtherIdentityForm`), activate.py (`WhenEnemyActivateAgainstYou`).
def GetAbilities() -> Sequence['Ability']:
    def changer(effect: 'Effect', message: 'Message2') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.GetIdentity().ChangeToOtherIdentityForm(effect)
    return [
        AbilityFactory.UnitIgnoreKeywordIcons(CardFinder(name="Batman"), guard=True, patrol=True),
        AbilityFactory.WhenEnemyActivateAgainstYou(AbilityType.Interrupt, Enemy, changer).SetCostFunc(CostFunc.Exhaust("This")),
    ]
