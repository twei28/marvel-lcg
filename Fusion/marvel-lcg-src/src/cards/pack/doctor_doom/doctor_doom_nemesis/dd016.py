from . import *

# Richards! — traitrise nemesis (3/4), x2. Boost 3.
# When Revealed: Mister Fantastic activates. If Mister Fantastic did not
#   activate this way, find and reveal Mister Fantastic.
#
# Cartes de reference :
#  - squelette : an011 / bt021, `WhenThisRevealed(None, op)` ;
#  - faire ACTIVER un ennemi deja en jeu : 21106 « Proxima's Power » et 11051
#    « Ancient Grudge », meme structure exacte (« X activates. If X is not in
#    play, search... ») : `Worlds.FindCardOnField(...)` puis
#    `enemy.DoActivate(player, effect)` — et non un `Activate(effect)` qui
#    n'existe pas ;
#  - aller chercher une carte dans le deck rencontre et la reveler : bt023,
#    `Search.EncounterCards(effect, player, include_discard_pile=True,
#    include_set_aside=True, card_ids=[...])` puis `face.Reveal(None, effect)`.
#
# ⚠ `include_set_aside=True` est INDISPENSABLE : au debut de partie, les cartes
# du set nemesis ne sont PAS dans le deck de rencontre, elles attendent dans
# `set_aside_nemesis_sets` jusqu'a ce qu'une obligation les y verse. Sans ce
# drapeau la recherche ne trouve rien et la carte ne fait rien — constate au
# premier passage des cas le 01/09/2026, journal a l'appui (le deck rencontre
# listait dd012 et dd013, mais pas dd015).
#
# ⚠ « If Mister Fantastic did NOT activate this way » : la seconde phrase est
# le REPLI de la premiere, pas un ajout. Si le sbire est en jeu, il active et
# on s'arrete la ; s'il n'y est pas, on le fait venir. Les coder toutes les
# deux ferait entrer un second Mister Fantastic.
#
# ⚠ La recherche vise le sbire par son card_id (`dd015`) et non par son nom :
# « Mister Fantastic » designe AUSSI le heros officiel mf001a et l'allie iw002
# (pack invisible_woman). Chercher par nom pourrait attraper la mauvaise carte
# dans une partie ou l'un d'eux est present.

def GetAbilities() -> Sequence['Ability']:

    def richards(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        en_jeu = Worlds.FindCardOnField(effect, card_type=Minion, card_ids=["dd015"])
        if en_jeu:
            en_jeu.DoActivate(joueur, effect)
            return

        trouves = Search.EncounterCards(
            effect,
            joueur,
            include_discard_pile=True,
            include_set_aside=True,
            card_ids=["dd015"],
        )
        if trouves:
            trouves[0].Reveal(None, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            richards,
        ),
    ]
