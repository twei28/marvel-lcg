from . import *
def GetAbilities() -> Sequence['Ability']:
    def discard_top_check(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        # « If the discarded card has a "Boost" ability » : le moteur marque ces
        # capacites avec AbilityType.Boost (c'est le test que fait lui-meme
        # boost.py). On l'interroge plutot que de lire le texte de la carte.
        this = effect.this.CastTo(Minion)
        # CORRECTIF (10/10/2026) : « the ATTACKING player » = celui qui controle
        # l'attaquant. `effect.GetInitiator()` est, pour un sbire, le mechant :
        # assertion levee (avalee par le moteur), Sidewinder jamais distribue.
        # Modele : 24046 Speed Demon, meme declencheur, `message.attacker`.
        attaquant = message.attacker
        joueur = attaquant.GetControlByPlayer() if attaquant is not None and Player.IsType(attaquant.GetControlBy()) else None
        faces = Worlds.DiscardEncounterCards(1, effect)
        for face in faces:
            if face.effect.Find(type=AbilityType.Boost) and joueur is not None:
                # Sidewinder lui-meme est distribue au joueur qui l'attaquait.
                joueur.DealEncounterCard(this, effect)
    return [
        AbilityFactory.WhenUnitWouldBeAttacked(AbilityType.ForcedInterrupt, "This", discard_top_check),
    ]
