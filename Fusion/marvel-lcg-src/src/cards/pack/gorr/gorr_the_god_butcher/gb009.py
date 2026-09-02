from . import *

# Black Berserker — SBIRE NECROVERSE (×3 dans le set modulaire).
# MNG 1 / ATQ 2 — 4 PV, 1 icone de boost.
#
# Patrol.
# [star] Black Berserker gets +X hit points, where X is the number of
#   NECROVERSE attachments in play (to a maximum of 4).
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Patrol` (mots-cles/patrol.md) : BASE AUTOMATIQUE, `desc.Patrol = "1"`.
# - `Boost` (mots-cles/boost.md) : `desc.Boost = "1"`, base automatique.
# - Le `[star]` en tete de ligne est une capacite PERMANENTE
#   (mots-cles/special.md) : `AbilityType.NonKeywordStar`. Ici elle passe par
#   une fabrique de bonus continu, qui porte deja le bon type.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Bonus de PV calcule sur l'etat du plateau : `ThisGainKeyword` avec
#   `get_new_value` (enhance_self.py), la forme employee par 57005b pour un
#   Hinder calcule. Le recalcul quand la quantite bouge passe par
#   `change_on_event`, comme sur al001a (le malus qui ne suivait pas
#   l'accrochage) — ici l'evenement est l'entree ou la sortie de jeu d'un
#   attachement.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « +X HIT POINTS » -> des PV supplementaires, pas des PV de base : un sbire
#   deja blesse ne se soigne pas quand X monte.
# « NECROVERSE ATTACHMENTS » -> les attachements qui portent le trait, pas
#   n'importe quel attachement (le pack en compte quatre : gb011 a gb014).
# « IN PLAY » -> partout sur la table, y compris ceux poses sur l'identite
#   d'un joueur (Blighted Chains s'attache au heros), pas seulement ceux poses
#   sur le vilain.
# « TO A MAXIMUM OF 4 » -> plafond sur X, pas sur les PV totaux.


def GetAbilities() -> Sequence['Ability']:

    def attachements_necroverse(effect: 'Effect', ui: List['CardFace']) -> int:
        # Signature imposee par la fabrique : (effect, ui) -> int
        # (enhance_self.py:371). `health=1` n'est pas la valeur du bonus mais
        # l'activation du mot-cle ; la valeur, c'est ce que rend cette
        # fonction — meme montage que 57005b pour un Hinder calcule.
        Unused(ui)
        trouves = Worlds.FindCardsOnField(
            effect,
            CardFinder(trait="NECROVERSE", card_type=Attachment),
        )
        return min(len(trouves), 4)

    return [
        AbilityFactory.ThisGainKeyword(
            attachements_necroverse,
            health=1,
            change_on_event=OnEvent.CardInPlay(Attachment),
        ),
    ]
