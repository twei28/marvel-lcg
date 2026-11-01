from . import *

# Get the Power (2B). « When Completed : Give Selene a tough status card. Find Darkhold and attach it to Selene. »
# Cartes de reference : hf105b (When Completed du stade), 04119 / `SetupCards.AttachTo` (chercher puis attacher), 01190 (`find`).
# « Find » = deck de rencontre, defausse, zone mise de cote ET jeu (le Darkhold peut deja etre attache a Selene par un sort revele pendant
# le stade 2 : dans ce cas il n'y a rien a faire, il est deja sur elle).


def GetAbilities() -> Sequence['Ability']:
    def terminee(effect: 'Effect', message: 'Message.WhenMainSchemeStageCompleted') -> None:
        selene = Selene(effect)
        if selene is None:
            return
        Faces.GiveStatus([selene], "Tough", effect)
        livre = Darkhold(effect)
        if livre is not None:
            if livre.bind_face is not selene:
                livre.AttachTo2(selene, effect)
            return
        face = Search.EncounterCard(effect, "FirstPlayer", include_discard_pile=True, include_set_aside=True, name=NOM_DARKHOLD)
        if face is not None:
            face.CastTo(Attachment).AttachTo2(selene, effect)

    return [AbilityFactory.WhenMainSchemeStageCompleted(AbilityType.ForcedInterrupt, "This", terminee)]
