from . import *

# Muir Island Crisis (POTENTIAL ALLY, Wolfsbane). Victory 1.
# Forced Response: After the villain phase ends, deal 1 damage to each hero in player order.
# When Defeated : Wolfsbane.
#
# Cartes de reference : `AbilityFactory.AfterPhaseEnd(Forced.., "Villain", ...)` (turn_phase.py), `this.DealDamage([heros], 1, effect)`.
# ⚠ « each HERO » : l'identite en FORME HEROS seulement (un joueur en alter ego ne prend rien) ; « in player order » : ordre des joueurs.
def GetAbilities() -> Sequence['Ability']:
    def muir(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        for joueur in Worlds.GetPlayers(effect):
            identite = joueur.GetIdentity()
            if Hero.IsType(identite):
                this.DealDamage([identite], 1, effect)

    return [
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Villain", muir),
        AbilitePotentialAlly("Wolfsbane"),
    ]
