from . import *

# * Vanessa Fisk (PERSONA) — +1 SCH (desc SCH+), boost [star] seule.
# When Revealed: Attach to Kingpin. You are confused.
# Hero Action: Discard an ATTACK event from your hand -> discard Vanessa Fisk.
#   Kingpin attacks you.
# [star] Boost: You are confused. If you were already confused, place 1 threat
#   on the main scheme.
# Voir CapacitesDUnePersona ; « Kingpin attacks you » = DoAttackYou (60118).

def GetAbilities() -> Sequence['Ability']:

    def confus(effect: 'Effect', joueur: 'Player', kingpin: 'Villain') -> None:
        Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)

    def attaque(effect: 'Effect', joueur: 'Player', kingpin: 'Villain') -> None:
        kingpin.DoAttackYou(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        identite = message.GetToPlayer().GetIdentity()
        deja = identite.IsConfused()
        Faces.GiveStatus([identite], "Confused", effect)
        if deja:
            this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    return [
        *CapacitesDUnePersona("ATTACK", "Discard an Attack event: discard Vanessa Fisk, Kingpin attacks you",
                              confus, attaque),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
