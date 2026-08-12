from . import *

# * Roz Solomon — custom "Rainy"
# Interrupt: When Roz Solomon thwarts, exhaust Congress of Worlds or a
# S.H.I.E.L.D. card you control -> she gets +2 THW for that use.
# (Congress of Worlds fait partie des cartes 8-13 non publiées ; le coût
# accepte toute carte S.H.I.E.L.D contrôlée, ce qui couvre les deux cas.)

def GetAbilities() -> Sequence['Ability']:

    def roz(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Ally)
        this.GainForThisActive(effect, message, thwart=2)

    return [
        AbilityFactory.WhenUnitWouldThwart(
            AbilityType.Interrupt,
            "This",
            roz,
        ).SetCostFunc(CostFunc.Exhaust(
            trait="S.H.I.E.L.D",
            from_where=["YouControlCards"]))
    ]
