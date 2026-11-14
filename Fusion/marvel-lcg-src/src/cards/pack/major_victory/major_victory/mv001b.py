from . import *

# * Vance Astro (face alter-ego) : REC 3, main 6, PV 10. MUTANT. PSIONIC. SOLDIER.
# Tactical Foresight — Action: Choose a player. That player draws 2 cards, then places 1 card from their hand on top of
#   their deck. (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `lj009` Fast Travel : `.SetTarget("Players")` pour « choose a player » (la cible est l'identite, `GetControlByPlayer()`).
#  - `bw001b` : `Faces.MoveAllToDeck([carte], joueur.player_deck, "Top", effect)` pour poser une carte sur le deck.
#
# TEXTE CONTRE CODE
#  « that player draws 2 cards, THEN places 1 card from THEIR hand » -> le joueur choisi pioche, puis choisit LUI-MEME la
#    carte de sa main (pas l'initiateur). Si sa main est vide, rien a replacer.
#  « Limit once per round » -> `LimitOncePerRound`. Chiffres : 2 cartes, 1 carte.


def GetAbilities() -> Sequence['Ability']:

    def tactical_foresight(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        for cible in effect.targets:
            joueur = cible.GetControlByPlayer()
            if joueur is None:
                continue
            joueur.DrawUp(2, effect)
            main = list(joueur.hand_cards.Get())
            if not main:
                continue
            carte = ChoisirUne(joueur, main, effect, "Tactical Foresight : place 1 card from your hand on top of your deck")
            if carte is not None:
                Faces.MoveAllToDeck([carte], joueur.player_deck, "Top", effect)

    return [
        (AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            tactical_foresight,
        )
            .SetName("Tactical Foresight")
            .SetTarget("Players")
            .LimitOncePerRound()),
    ]
