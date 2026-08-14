from . import *

# Electromagnetic Pulse

def GetAbilities() -> Sequence['Ability']:

    def impulsion(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        entre = False

        # « If an ELECTRO minion was discarded this way, put that minion into
        # play. » Le set en compte DEUX (6 PV et 3 PV) : la carte officielle
        # nommait Electro, celle-ci designe n'importe lequel des deux, d'ou le
        # filtre par nom plutot que par identifiant.
        for face in Worlds.DiscardEncounterCards(7, effect):
            if face.IsName("Electro") and Minion.IsType(face):
                face.PutIntoPlay(joueur, effect)
                entre = True

        if not entre:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Worlds.DiscardEncounterCards(3, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            impulsion
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
