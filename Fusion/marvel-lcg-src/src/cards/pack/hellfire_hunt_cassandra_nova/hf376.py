from . import *

# Mind Shatter (TREACHERY ILLUSION PSIONIC). Peril. Boost 1. « When Revealed : You are confused. You may discard any number of cards from your hand.
# Then, deal X damage to each identity in play, where X is equal to half of the number of cards from your hand. »
# Cartes de reference : `Player.DiscardHandCards((0, "All"), effect)` (player_ask.py), `Faces.GiveStatus`, `TakeDamage` ; Peril : mot-cle natif
# (`desc.Peril`, fiche mots-cles/peril.md).
# ⚠ LECTURE (QUESTIONS.md n°2) : « the number of cards from your hand » = la main APRES la defausse facultative (c'est ce qui donne un sens a
# « you may discard ») ; moitie ARRONDIE AU SUPERIEUR (regle du jeu) ; les degats sont DIRECTS, un a chaque identite en jeu (heros ou alter-ego).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)
        joueur.DiscardHandCards((0, "All"), effect)
        x = (joueur.hand_cards.GetSize() + 1) // 2
        if x > 0:
            for identite in Worlds.GetPlayersIdentities(effect):
                identite.TakeDamage(this, x, effect)

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
