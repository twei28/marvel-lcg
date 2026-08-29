from . import *
def GetAbilities() -> Sequence['Ability']:
    def discard_top_check(effect: 'Effect', message: 'Message.WhenUnitWouldBeAttacked') -> None:
        # « If the discarded card has a "Boost" ability » : le moteur marque ces
        # capacites avec AbilityType.Boost (c'est le test que fait lui-meme
        # boost.py). On l'interroge plutot que de lire le texte de la carte.
        this = effect.this.CastTo(Minion)
        player = effect.GetInitiator()
        faces = Worlds.DiscardEncounterCards(1, effect)
        for face in faces:
            if face.effect.Find(type=AbilityType.Boost):
                # Sidewinder lui-meme est distribue au joueur qui l'attaquait.
                player.DealEncounterCard(this, effect)
    return [
        AbilityFactory.WhenUnitWouldBeAttacked(AbilityType.ForcedInterrupt, "This", discard_top_check),
    ]
