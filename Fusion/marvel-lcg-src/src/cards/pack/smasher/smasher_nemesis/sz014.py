from . import *
# Corrupting Revelation, traitrise nemesis. Boost 2.
#
# When Revealed: You are confused. Find Entropic Subversion and reveal it. If Entropic Subversion is already in play, place 3 threat on it.
#
# Carte de reference : 45028 Bantam (« If X is in play, place threat on it. Otherwise, find X and reveal it » : `Worlds.FindCardOnField` +
# `Find.FindAndReveal`). L'ordre imprime est respecte : desorienter d'abord, puis chercher.
def GetAbilities() -> Sequence['Ability']:
    def revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)
        face = Worlds.FindCardOnField(effect, name=NOM_ENTROPIC_SUBVERSION, card_type=SchemeSide2)
        if face:
            this.PlaceThreatOnSchemes([face], 3, effect)
        else:
            Find.FindAndReveal(effect, joueur, name=NOM_ENTROPIC_SUBVERSION, card_type=SchemeSide2)
    return [
        AbilityFactory.WhenThisRevealed(None, revealed),
    ]
