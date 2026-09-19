from . import *

# The Raft Breakout (FAILED) — Setup: Shuffle each minion in The Raft Breakout
#   encounter set into the encounter deck (in expert mode, deal 1 of those
#   minions at random to each player as a facedown encounter card before
#   shuffling in the rest).
# Les six prisonniers sont fabriques s'ils ne sont pas deja dans le deck (le
# scenario The Raft Breakout les y a mis lui-meme).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        deja = {f.paper.card_id for f in Worlds.GetEncounterDeckCards(effect.world)}
        faces = []
        for cid in PRISONNIERS_DU_RAFT:
            if cid in deja:
                continue
            faces.append(CardFactory.GenerateCard(cid, None, effect.world).face)
        if not faces:
            return
        if Worlds.IsExpert(effect):
            def distribuer(player: 'Player') -> None:
                if faces:
                    choisi = Rand.RandomChoice(faces, effect)
                    faces.remove(choisi)
                    player.DealEncounterCard(choisi, effect)
            Players.ForEachPlayer(effect, distribuer)
        if faces:
            Faces.ShuffleAllTo(faces, "EncounterDeck", effect)

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
