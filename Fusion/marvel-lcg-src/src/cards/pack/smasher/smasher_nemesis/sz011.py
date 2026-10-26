from . import *
# * Scientist Supreme (Andrew Forson), sbire nemesis. PV 4, ATQ 1*, SCH 2, boost 3. A.I.M. ELITE. GENIUS.
#
# Villainous.                                  -> desc.Villainous = "1" (base automatique, fiche mots-cles/villainous.md)
# [star] Scientist Supreme's attacks gain piercing and ranged.
# When Revealed: You are stunned and confused.
# (Smasher's nemesis minion.)                  -> desc.Nemesis
#
# Cartes de reference : ho016 Bullseye (`UnitAttackGainKeyword("This", piercing=True, ..)`, capacite etoilee permanente) ;
# 56176 Pheromones (« You are stunned and confused » : `WhenThisRevealed(None, op)` + `Faces.GiveStatus([identite], ..)` x2).
def GetAbilities() -> Sequence['Ability']:
    def revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        identite = message.GetToPlayer().GetIdentity()
        Faces.GiveStatus([identite], "Stunned", effect)
        Faces.GiveStatus([identite], "Confused", effect)
    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True, ranged=True),
        AbilityFactory.WhenThisRevealed(None, revealed),
    ]
