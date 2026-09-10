from . import *

# Swinging Rescue — EVENEMENT, cout 2, RES [energy], x2. AERIAL. TACTIC.
# Hero Action: Choose an ally in any player's discard pile -> add that ally to
#   its owner's hand and draw 2 cards. Place 2 psionic web counters on
#   Spider-Woman for each [mental] resource you used to pay for this card (to a
#   maximum of 10).
#
# CARTES DE REFERENCE
#  - `sw005` Swing and Kick : la brique « provenance du paiement », partagee
#    par `ToilesParRessourceMentale`. Ici DEUX compteurs par [mental], pas un.
#  - `Faces.AddToHand(faces, joueur, effect)` (faces.py:336).
#
# TEXTE CONTRE CODE
#  ⚠⚠ « in ANY PLAYER'S discard pile » et « to ITS OWNER'S hand » : en
#    multijoueur, on repeche l'allie d'un VOISIN, et il rentre chez LUI. Les
#    deux moities se lisent ensemble — ce n'est pas un vol, c'est un secours.
#    En solo la distinction ne se voit pas ; elle est pourtant tout le texte.
#  ⚠ « DRAW 2 CARDS » : c'est VOUS qui piochez, pas le proprietaire de l'allie.
#  ⚠ Aucune defausse ne contient d'allie : la carte ne fait rien, ni pioche ni
#    compteurs. La fleche en fait une condition, pas un cout.


def GetAbilities() -> Sequence['Ability']:

    def sauvetage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        allies: List['CardFace'] = []
        for autre in Worlds.GetPlayers(effect):
            allies += [f for f in autre.discard_pile.GetAll()
                       if f is not None and Ally.IsType(f)]
        if not allies:
            return

        choisi = joueur.AskChooseFaces(
            allies, (1, 1), effect,
            prompt="Choose an ally in any player's discard pile")
        for allie in choisi:
            proprietaire = allie.card.GetOwner()
            if Player.IsType(proprietaire):
                Faces.AddToHand([allie], proprietaire, effect)
        if choisi:
            joueur.DrawUp(2, effect)
            PoserDesToiles(joueur, ToilesParRessourceMentale(effect, 2), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sauvetage,
        ).SetPlay(),
    ]
