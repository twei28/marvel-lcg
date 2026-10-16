from . import *

# Rapid Replication — TRAITRISE (Baxter's Lab 15/22, x3). 2 boosts.
# When Revealed: Discard cards from the top of the encounter deck until a minion is discarded. Reveal
#   that minion. Then, resolve the "Special" ability on Baxter's Laboratory.
#
# Cartes de reference : `sk145b` / helper `RevelerPouvoirDuDeck` (`Worlds.DiscardEncounterCardsUntil`
# puis `face.Reveal`) ; `tx004b` pour le Special.
#
# Mots-pieges : « until a MINION is discarded » (type Minion) ; « Reveal THAT minion » (celui qui vient
# d'etre defausse, de la defausse) ; « THEN » : le Special se resout APRES la revelation, par le joueur
# a qui la carte est revelee, et meme si aucun sbire n'a pu etre defausse.


def GetAbilities() -> Sequence['Ability']:

    def repliquer(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        sbire = DefausserJusquAuSbire(effect)
        if sbire is not None:
            sbire.Reveal(joueur, effect)
        ResoudreLeSpecial(effect, joueur)

    return [AbilityFactory.WhenThisRevealed(None, repliquer)]
