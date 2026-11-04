from . import *

# Tri-Force Vision — EVENEMENT x3 (dm002/dm003/dm004, meme texte). SUPERPOWER.
# Cout 1, [energy].
# Hero Action: Look at the top 3 cards of the encounter deck → put them back
#   in any order. If you put them back in the same order, shuffle 3 cards
#   from your discard pile into your deck.
#
# CARTES DE REFERENCE
#  - « Look at the top N cards of the encounter deck ... put them back in any
#    order » : **`uj016`** Inspector Ishida (meme phrase exacte) : `joueur.
#    LookAtDeck("EncounterDeck", 3, effect)` puis `joueur.
#    PlaceOnTopInAnyOrder(list(faces), effect)` (player_cards.py:41).
#  - « shuffle N cards from your discard pile into your deck », choix du
#    JOUEUR (pas « the top N », pas de filtre de nom) : **`rm008`** Askani
#    pour `Faces.ShuffleAllTo(cartes, joueur.player_deck, effect)`, mais ici
#    le choix se fait via `joueur.AskChooseFaces(defausse, (0, min(3,
#    taille)), effect, not_move=True)` (player_ask.py:261), modele du
#    `AskChooseFaces` deja utilise par `PlaceOnTopInAnyOrder` lui-meme.
#
# TEXTE CONTRE CODE
#  « put them back in the SAME order » : compare l'ordre REELLEMENT choisi
#  (dessus du deck de rencontre apres `PlaceOnTopInAnyOrder`) a l'ordre VU au
#  regard — pas un drapeau pose par le joueur. Avec 0 ou 1 carte regardee, il
#  n'y a rien a reordonner : l'ordre est necessairement « le meme », la
#  recompense s'applique (lecture litterale, rien a reordonner n'est pas
#  rater l'ordre). « shuffle 3 cards from your discard pile » : JUSQU'A 3,
#  choisies par le joueur ; une defausse plus petite en donne moins. « into
#  your deck » : `joueur.player_deck`, remelange natif (`ShuffleAllTo`).


def GetAbilities() -> Sequence['Ability']:

    def tri_force_vision(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        faces = joueur.LookAtDeck("EncounterDeck", 3, effect)
        ordre_avant = list(faces)
        if len(faces) > 1:
            joueur.PlaceOnTopInAnyOrder(list(faces), effect)

        deck = Worlds.GetEncounterDeck(effect)
        ordre_apres = deck.Get(True)[:len(ordre_avant)]
        if ordre_apres != ordre_avant:
            return

        defausse = list(joueur.discard_pile.Get())
        if not defausse:
            return
        choisies = joueur.AskChooseFaces(
            defausse,
            (0, min(3, len(defausse))),
            effect,
            not_move=True,
            prompt="Shuffle into your deck",
        )
        if choisies:
            Faces.ShuffleAllTo(choisies, joueur.player_deck, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tri_force_vision,
        ).SetPlay(),
    ]
