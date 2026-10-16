from . import *

# Wrapped Up — TRAITRISE (High Speed 4/5, x2). 1 boost.
# When Revealed: Daze a friendly character. If you cannot, this card gains surge.
#
# Cartes de reference : `td005` Improvised Tactics (« friendly characters » = `Worlds.
# GetOnFieldFriendlyCharacters`, choix par `AskChooseFaces`) ; RECETTES §2 « If you cannot » : on lit le
# RETOUR de `Faces.GiveStatus` (nombre de personnages reellement servis) ; `ThisCardGainSurge`.
#
# Mots-pieges : « a FRIENDLY character » (identites et allies de TOUS les joueurs) ; « If you CANNOT »
# (tous les personnages amis portent deja une carte Dazed, ou aucun n'existe : surge). Le repli n'est PAS
# declare en cible legale (sinon l'abilite ne partirait pas et le surge serait mort).


def GetAbilities() -> Sequence['Ability']:

    def hebeter(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        amis = [ami for ami in Worlds.GetOnFieldFriendlyCharacters(effect) if ami.CanbeDazed()]
        servis = 0
        if amis:
            choisi = joueur.AskChooseFace(amis, effect, prompt="Daze a friendly character")
            if choisi is not None:
                servis = Faces.GiveStatus([choisi], "Dazed", effect)
        if servis == 0:
            ThisCardGainSurge(effect)

    return [AbilityFactory.WhenThisRevealed(None, hebeter)]
