from . import *

# hs225 Aerial Excellence (environnement du mode Hunter, scenario 4)
# Forced Response : apres l'etape 1 de la phase du vilain, 1 menace sur le complot
# principal par identite sans AERIAL ; chaque identite AERIAL subit 2 degats indirects.

def GetAbilities() -> Sequence['Ability']:

    def survoler(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        this = effect.this
        au_sol = 0
        for joueur in Worlds.GetPlayers(effect):
            identite = joueur.GetIdentity()
            if identite is None:
                continue
            if identite.HasTrait("AERIAL"):
                identite.TakeIndirectDamage(this, 2, effect)
            else:
                au_sol += 1
        if au_sol:
            this.PlaceThreatOnSchemes("MainScheme", au_sol, effect)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, survoler),
    ]
