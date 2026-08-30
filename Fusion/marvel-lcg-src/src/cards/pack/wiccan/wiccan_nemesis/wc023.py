from . import *

# Master Magus Returns — trahison nemesis de Wiccan (5/5)
# When Revealed: If The Demiurge environment is not in play, reveal the
#   set-aside Moridun attachment, then remove Master Magus Returns from the
#   game. If Moridun was not revealed this way, you are confused.
# [star] Boost: You are confused.
#
# Structure a DEUX branches enchainees, dans l'ordre imprime :
#   1. « If The Demiurge environment is NOT in play » -> garde negative sur
#      `Worlds.FindCardsOnField(effect, name="The Demiurge")`. Une fois New
#      Vessel accomplie et retournee en environnement permanent, cette
#      trahison ne ramene plus Moridun : Wiccan a deja perdu ce combat-la.
#   2. « reveal the SET-ASIDE Moridun attachment » -> `Worlds.
#      GetSetAsideAreaCards(effect, CardFinder(name="Moridun"))` puis
#      `face.Reveal(player, effect)`. Modele : mw018 (recherche en zone de
#      reserve) et wc020 lui-meme, qui va chercher New Vessel de la meme
#      facon. C'est bien la zone SET-ASIDE, pas la defausse de rencontre :
#      Moridun n'y arrive que par `Faces.SetAside`, pose par wc019a.
#   3. « then remove Master Magus Returns from the game » ->
#      `Faces.RemoveAllFromGame([this], effect)`. La phrase est DANS la
#      branche conditionnelle (elle suit « reveal ... , THEN remove ») :
#      quand The Demiurge est en jeu, la carte n'est PAS retiree du jeu, elle
#      part a la defausse de rencontre normalement.
#   4. « If Moridun was NOT revealed this way, you are confused » -> hors
#      branche : c'est une phrase separee, qui s'applique aussi bien quand
#      The Demiurge bloquait la revelation que quand Moridun n'etait pas de
#      cote. Piege `that <nom>` / `unless` de PROCESSUS-CARTE : « this way »
#      designe la revelation de CETTE carte-ci, pas un Moridun deja en jeu.
#      Un Moridun deja EN JEU n'est pas « de cote » : la revelation echoue
#      donc, et le joueur est bien desoriente — lecture voulue.
#
# « you » = le joueur qui revele (`message.GetToPlayer()`), jamais le premier
# joueur ni tous les joueurs.
#
# [star] Boost « You are confused » -> `AbilityFactory.WhenCardBecomeBoost
# ("This", ...)` + `Faces.GiveStatus([identite], "Confused", effect)`, meme
# idiome que 56177 Venom Blast.

def GetAbilities() -> Sequence['Ability']:

    def master_magus_returns(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        player = message.GetToPlayer()
        if player is None:
            return

        revele = False
        demiurge = Worlds.FindCardsOnField(effect, name=NOM_DEMIURGE)
        if not demiurge:
            faces = Worlds.GetSetAsideAreaCards(effect, CardFinder(name=NOM_MORIDUN))
            if faces:
                faces[0].Reveal(player, effect)
                revele = True
            Faces.RemoveAllFromGame([this], effect)

        if not revele:
            identite = player.GetIdentity()
            if identite is not None:
                Faces.GiveStatus([identite], "Confused", effect)

    def master_magus_returns_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        if player is None:
            return
        identite = player.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Confused", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            master_magus_returns,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            master_magus_returns_boost,
        ),
    ]
