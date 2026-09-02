from . import *

# Vicious Tendrils — ATTACHEMENT NECROVERSE. WEAPON. +1 ATQ, riposte 1,
# 3 icones de boost.
#
# Attach to Gorr the God Butcher.
# Gorr the God Butcher gains retaliate 1.
# [star] Gorr the God Butcher's attacks gain ranged.
# Hero Action: Discard 1 card at random from your hand and discard the top 4
#   cards of your deck → discard this card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Retaliate` (mots-cles/retaliate.md) : le mot-cle est une BASE
#   AUTOMATIQUE, mais `desc.Retaliate` sur CET attachement le donnerait a
#   l'attachement, pas au vilain. Le texte dit « GORR gains retaliate 1 » :
#   c'est un bonus DONNE, donc `GiveKeywordToAttached(retaliate=1)`.
# - `Ranged` (mots-cles/ranged.md, creee pour ce pack) : aucune cle `desc`,
#   toujours scripte, et il se donne a l'ATTAQUE :
#   `UnitAttackGainKeyword(..., ranged=True)`.
# - Le `[star]` marque une capacite permanente (mots-cles/special.md).
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Attachement qui donne un mot-cle a son porteur : 45107 (Apocalypse),
#   `GiveKeywordToAttached` ; 50107b pour le `UnitAttackGainKeyword` permanent.
# - Action qui se defausse : 07020, comme gb012 et gb013.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Gorr GAINS retaliate 1 » -> le vilain riposte, pas l'attachement.
# « Gorr's ATTACKS gain ranged » -> les attaques du vilain ignorent la riposte
#   des defenseurs. Les deux lignes se contredisent pour l'adversaire : Gorr
#   riposte mais ne subit pas les ripostes. C'est voulu.
# « Discard 1 card AT RANDOM from your hand AND discard the top 4 » -> cout a
#   deux parties, la premiere ALEATOIRE (contrairement a gb013), et 4 cartes
#   de deck, pas 2.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_GORR)
        ),
        *AbilityFactory.GiveKeywordToAttached(
            retaliate=1,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            CardFinder(name=NOM_GORR),
            ranged=True,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.Discard("RandomHandCard"))
        .SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 4)),
    ]
