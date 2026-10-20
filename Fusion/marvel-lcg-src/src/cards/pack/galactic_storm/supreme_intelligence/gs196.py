from . import *

# * Supreme Intelligence (II) — MECHANT (Supreme Intelligence). KREE. SCH 2, ATK 2, 14[per_hero] PV.
# Toughness.
# Forced Response: After a KREE minion is defeated, heal 1 damage from the villain. If that minion has the
#   ELITE trait, give the villain a facedown boost card.
#
# Cartes de reference : **`gs195`** (meme Reponse forcee, helper `ReponseSbireKreeVaincu`) ; Toughness =
# base automatique (`desc.Toughness`, fiche mots-cles/toughness.md), aucun module.
#
# ⚠ Mots-pieges : identiques a gs195.


def GetAbilities() -> Sequence['Ability']:
    return [ReponseSbireKreeVaincu(boost_si_elite_seulement=True)]
