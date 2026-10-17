from . import *

# Kagemusha — PATH (la Voie du Kagemusha), classe Ninjutsu (Inkwire, TMNT Shinobi). NINJUTSU.
# Permanent. You get -1 hand size.
# Your hero gains the NINJA trait.
# Shadow Stride — Hero Action: Exhaust this card -> cloak your hero.
# « I am the shadows. »
#
# Mots-cles (fiches lues AVANT le code) : Cloak (mots-cles/cloak.md) ; Permanent (permanent.md) ;
# Shinobi / Path (shinobi.md).
#
# Cartes de reference :
#  - « You get -1 hand size » : `sentinel/st005b` Legs (Destroyed) =
#    `GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1)` (modele `04165` Martial Law) ;
#  - « gains the X trait » : `hunting_season/hs092` = `GiveKeywordToInPlayWhenApplyThis(<cible>, trait=...)` ;
#  - « Hero Action: Exhaust this card -> ... » : `jennika/tj011` (Path) / `ua...` = `WhenInYourPlayTurn(HeroAction)`
#    + `CostFunc.Exhaust("This")` ;
#  - « cloak your hero » : `tmnt_aspect_protection/up023` Lookout = `Faces.GiveStatus([hero], "Cloaked", effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « YOU get -1 hand size » : les DEUX formes de l'identite ("You") ; « YOUR HERO gains the NINJA trait » :
#    la face HEROS seulement (« Your hero »), pas l'alter-ego.
#  ⚠ « Hero Action » : forme heros uniquement ; le « -> » est le cout : incliner d'abord (une fois par
#    redressement, aucune limite imprimee ; le livret dit « once per round », ce que l'inclinaison realise).
#  ⚠ Nom de la capacite : le SCAN imprime « Shadow Stride » ; le livret (p.1, p.2) la nomme « Walk in Shadows »
#    (voir .planning/tmnt/shinobi-socle-questions.md, Q-S1).
#  ⚠ « cloak your hero » : une carte Cloaked sur le HEROS (jamais sur l'alter-ego) ; un heros deja camoufle
#    n'en recoit pas une seconde (une seule Cloaked par personnage).


def GetAbilities() -> Sequence['Ability']:

    def shadow_stride(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Path)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        ShinobiCloak(effect, joueur.GetHero())

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("YourHero", trait="NINJA"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            shadow_stride,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
