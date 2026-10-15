from . import *

# The Skrull Invasion 2A — complot principal, face A.
# When Revealed: If Mistrust and Paranoia is in play, remove 2[per_hero] suspicion counters from "Who Do You Trust?".
#   Otherwise, find Mistrust and Paranoia and reveal it.
#
# Cartes de reference : **`skrull_menace/paibok/sk145a`** (« if X is in play ... otherwise, search the encounter deck
# and discard pile for X » : `Search.EncounterCard(include_discard_pile=True, name=...)` puis `Reveal`) ; **`01136`**
# Ultron (meme recherche). Retrait de jetons : `Faces.RemoveCountersOn` (helper `RetirerSoupcons`).
#
# ⚠ Mots-pieges : « IF Mistrust and Paranoia IS IN PLAY » : deux branches exclusives (en jeu = on retire les jetons ET
# on ne cherche rien) ; « 2[per_hero] » : 2 par joueur ; « find » = fouiller le deck ET la defausse ; la fouille
# melange le deck rencontre (natif). Un 2A sans TargetThreat avance seul en 2B.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        en_jeu = [f for f in Worlds.GetOnFieldCards(effect) if f.paper.card_id == "sk201" and f.IsInPlay()]
        if en_jeu:
            RetirerSoupcons(effect, SeuilSoupcons(effect))
            return
        face = Search.EncounterCard(effect, include_discard_pile=True, name="Mistrust and Paranoia")
        if face is not None:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
