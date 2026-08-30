from . import *

# * Noh-Varr's Ship — SOUTIEN BASIC, custom « jakxin »
# Cout 3, [energy], traits KREE + VEHICLE + YOUNG AVENGER.
#
# Play only if your identity has the [[YOUNG AVENGER]] trait.
# Resource: Exhaust Noh-Varr's Ship → generate a [wild] resource.
#
# ---------------------------------------------------------------------------
# UNE VRAIE SYNERGIE INTER-PACKS
#
# Le trait YOUNG AVENGER est porte, dans ce jeu, par SIX identites custom :
# Wiccan (wc001a/b), Speed (sd001a/b), Iron Lad (il001a/b), Patriot
# (pt001a/b), Kate Bishop (kb001a/b) et Ms. America (ma001a). La carte est
# donc reellement jouable ailleurs que dans son propre pack — c'est le seul
# soutien BASIC du catalogue reserve a cette equipe.
#
# ---------------------------------------------------------------------------
# LA CONDITION DE JEU
#
# `AbilityFactory.CanPlayThisSupportCard().SetPlay(
# only_if_your_identity_has_trait=TRAIT_YOUNG_AVENGER)` : kwarg dedie de
# `Ability.SetPlay` (ability.py:596-629). Modeles : `12014`
# (`only_if_your_identity_has_trait="AVENGER"`) et `45042`
# (`"X-MEN"`). `53020` Flight Squadron montre le meme couple
# `CanPlayThisSupportCard().SetPlay(...)` sur un SOUTIEN.
#
# ⚠ « your IDENTITY », pas « your hero » : le kwarg
# `only_if_your_hero_has_trait` existe aussi et serait FAUX ici — il
# exigerait la forme heros. Le texte parle de l'identite, donc des deux
# faces.
#
# ⚠ `.SetPlay(...)` AVANT tout `.SetTarget` : `SetCondition` porte
# `assert self.selectors == []` (ability.py:486).
#
# ---------------------------------------------------------------------------
# LA CAPACITE RESSOURCE
#
# « Resource » NU (ni « Hero Resource », ni « Alter-Ego Resource ») ->
# `AbilityType.Resource` : la carte finance dans LES DEUX formes. Modele
# `kb013` Kate's Quiver, meme phrase imprimee, meme
# `CanGenerateResources(<type>, Resources("G")).SetCostFunc(
# CostFunc.Exhaust("This"))`.
#
# LA FLECHE EST UN COUT : incline, le vaisseau ne finance plus rien.
#
# ⚠ Une carte n'a droit qu'a UNE `CanGenerateResources`
# (assert card_player.py:50) : il n'y en a qu'une ici.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisSupportCard(
        ).SetPlay(only_if_your_identity_has_trait=TRAIT_YOUNG_AVENGER),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
