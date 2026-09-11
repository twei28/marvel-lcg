from . import *
# * Patsy Walker — ALTER EGO. PSIONIC. REC 3, MNG 6, 11 PV.
# Mental Potential — Interrupt: When the villain schemes against you, draw 1
#   card → if that card has a printed [mental] resource, reduce the amount of
#   threat placed by 1.
#
# Modele : 45156 Celestial Armor (`WhenUnitSchemeAgainst(..., Villain, "You")`,
# lecture de la ressource imprimee d'une carte). La fleche fait de la pioche le
# COUT : on pioche d'abord, on lit ensuite. `GainSCHForThisScheme(-1)` reduit
# la menace de CETTE manigance (sender_enemy.py:201).

def GetAbilities() -> Sequence['Ability']:

    def mental_potential(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        faces = joueur.DrawUp(1, effect)
        if faces and AMentalImprime(faces[0]):
            message.GainSCHForThisScheme(-1, effect)

    return [
        AbilityFactory.WhenUnitSchemeAgainst(
            AbilityType.Interrupt,
            Villain,
            "You",
            mental_potential,
        ).SetName(MENTAL_POTENTIAL),
    ]
