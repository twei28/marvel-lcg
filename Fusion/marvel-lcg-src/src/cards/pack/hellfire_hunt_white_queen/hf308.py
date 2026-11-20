from . import *

# Illusion Loop. Traitrise SKILL. « When Revealed : For each ILLUSION attachment in play, if it has any illusion counters on it, place 1 illusion counter
# on it. The villain schemes. [star] Boost : If there is at least one ILLUSION attachment attached to your identity, you are confused. »
# Cartes de reference : 06027 (`Worlds.GetOnFieldCards`), 41029 (`GiveStatus`), `villain.DoScheme`.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        for face in Worlds.GetOnFieldCards(effect):
            if Attachment.IsType(face) and face.HasTrait(ILLUSION) and face.GetCounters(COMPTEUR_ILLUSION) > 0:
                Faces.PlaceCountersOn([face], 1, COMPTEUR_ILLUSION, effect)
        villain = Worlds.FindVillain(effect)
        if villain is not None:
            villain.DoSchemes(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        if any(Attachment.IsType(f) and f.HasTrait(ILLUSION) for f in identite.GetAttachedAttachments()):
            Faces.GiveStatus([identite], "Confused", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
