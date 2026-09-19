from . import *

# Stop the Presses! (COMPLETED) — Setup: Each player puts 1 DAILY BUGLE
#   support (that has not been removed from the campaign) into play from the
#   Stop the Presses! encounter set.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        retirees = set(Retirees(effect))
        en_jeu = {f.paper.card_id for f in Worlds.FindCardsOnField(effect, trait="DAILY BUGLE", card_type=Support)}
        candidats = []
        for cid in SOUTIENS_DAILY_BUGLE:
            if cid in en_jeu:
                continue
            face = CardFactory.GenerateCard(cid, None, effect.world).face
            if face.paper.name.lstrip('* ') in retirees:
                Faces.RemoveAllFromGame([face], effect)
                continue
            candidats.append(face)

        def chacun(player: 'Player') -> None:
            if not candidats:
                return
            choix = candidats[0] if len(candidats) == 1 else player.AskChooseFace(list(candidats), effect, prompt="Choose a Daily Bugle support")
            if choix is None:
                choix = candidats[0]
            candidats.remove(choix)
            choix.PutIntoPlay(player, effect, under_control=True)

        Players.ForEachPlayer(effect, chacun)
        if candidats:
            Faces.RemoveAllFromGame(list(candidats), effect)

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
