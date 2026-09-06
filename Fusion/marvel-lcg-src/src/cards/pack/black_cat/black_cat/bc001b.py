from . import *

# * Felicia Hardy (face alter-ego) — THIEF. PV 9, REC 3, main 6.
# If there are more than 3 tucked cards here, discard all but 3 of those cards.
# Cat Burglary — Action: Look at the top 2 cards of the encounter deck and
#   tuck 1 of them under your identity. (Limit once per round.)
#
# ⚠ HOMONYME INTERNE AU PACK : « Cat Burglary » est AUSSI le nom de la carte
# `bc005`, un evenement. Ici c'est le LIBELLE d'une capacite, la` : un nom de
# carte. Les deux coexistent sur la table, et le texte francais s'ecrit sur le
# `card_id`, jamais sur le nom.
#
# ⚠ ET LE ZIP NUMEROTE LES DEUX FACES A L'ENVERS, comme tous les packs de
# Rainy : « 0.1 » est l'ALTER-EGO (Felicia Hardy), « 0.2 » le HEROS. Verifie
# sur les libelles imprimes ALTER-EGO / HERO, pas sur le nom de fichier.
#
# CARTES DE REFERENCE
#  - `48021` * Gambit : `LookAtDeck("EncounterDeck", n, effect)` puis
#    `AskChooseFace` puis `TuckCardUnderHere`. Meme geste, a une carte pres.
#  - `bc001a` : la face heros, qui LIT cette pile.
#
# TEXTE CONTRE CODE
#  ⚠ « LOOK AT the top 2 cards » et non « discard » : les cartes sont
#    REGARDEES. Celle qu'on ne glisse pas reste sur le deck de rencontre —
#    c'est ce que fait `LookAtDeck`, qui ne deplace rien de lui-meme.
#  « tuck 1 OF THEM » -> une des deux vues, pas une carte au choix ailleurs.
#  « under YOUR IDENTITY » -> la meme pile que « here » de la face heros :
#    elle est portee par la CARTE (card_face.py:1017).
#  ⚠ AUCUN PLAFOND ICI. La carte ne dit pas « (to a maximum of 3) » : la carte
#    entre toujours, et c'est la regle continue des deux faces qui ramene la
#    pile a 3 ensuite. Difference de fond avec le pack `spider_man_noir`.
#  « (Limit once per ROUND.) » -> `.LimitOncePerRound()`.


def GetAbilities() -> Sequence['Ability']:

    def cambriolage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        vues = joueur.LookAtDeck("EncounterDeck", 2, effect)
        if not vues:
            return
        choisie = joueur.AskChooseFace(list(vues), effect)
        if choisie is None:
            return
        GlisserSousIdentite(effect, [choisie], joueur)

    return [
        RegleDesTroisCartes(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            cambriolage,
        ).LimitOncePerRound()
        .SetName("Cat Burglary"),
    ]
