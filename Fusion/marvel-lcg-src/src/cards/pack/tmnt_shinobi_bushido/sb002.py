from . import *

# Rectitude — AMELIORATION OATH, classe Bushido (Inkwire, TMNT Shinobi). Cout 1, [energy].
# Uses (3 samurai counters).
# Your hero gets +1 THW.
# Forced Response: After your hero makes a basic thwart, remove 1 samurai counter from this card.
#
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md) ; samurai counter / OATH (samurai-counter.md).
#
# Cartes de reference : `tmnt_shinobi_bushido/sb001` Loyalty (meme montage, pouvoir THW au lieu de DEF) ;
# `totally_awesome_hulk/ah005` (bonus de stat sur l'identite) ; `trors/spider_woman/04032` (AfterUnitUseBasicPower).
#
# TEXTE CONTRE CODE
#  ⚠ « Forced RESPONSE » : apres le pouvoir, forcee, aucun choix.
#  ⚠ « basic THWART » : `powers=["THW"]` seulement (une attaque ou une defense ne retire pas de compteur).
#  ⚠ « from THIS card » ; Uses defausse la carte au dernier compteur.


def GetAbilities() -> Sequence['Ability']:

    def rectitude(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        Faces.RemoveCountersOn([this], 1, 'samurai', effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("YourHero", thwart=1),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.ForcedResponse,
            "You",
            rectitude,
            powers=["THW"],
        ),
    ]
