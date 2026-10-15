from . import *

# Outnumbered — TRAITRISE x2 (Skrull Society). ★.
# When Revealed: Engage each SKRULL minion in play. Then, search the encounter
#   deck and discard pile for a SKRULL minion and reveal it.
# ★ Boost: This card gets +1 boost icon for each SKRULL enemy in play (to a
#   maximum of +4) for this activation.
#
# Cartes de reference : `Minion.EngagePlayer` ; **`27141`** (`Search.EncounterCard(
# include_discard_pile=True, ...)` + `Reveal`) ; **`46028`** (`GainBoostIcon`).
# ⚠ « EACH Skrull minion IN PLAY » (meme ceux engages avec un autre joueur) ;
# « Then » : la recherche se fait meme si aucun sbire n'etait en jeu ;
# « ENEMY » pour le boost (mechant compris) ; plafond +4.


def GetAbilities() -> Sequence['Ability']:

    def encercle(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        for sbire in Worlds.GetOnFieldMinions(effect, CardFinder2("SKRULL")):
            sbire.EngagePlayer(joueur, effect)
        face = Search.EncounterCard(effect, joueur, include_discard_pile=True, trait="SKRULL", card_type=Minion)
        if face:
            face.Reveal(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        n = min(4, len(EnnemisSkrullEnJeu(effect)))
        if n:
            message.GainBoostIcon(n, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, encercle),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
