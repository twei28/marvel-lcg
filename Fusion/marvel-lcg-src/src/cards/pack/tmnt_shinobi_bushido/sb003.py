from . import *

# Courage — AMELIORATION OATH, classe Bushido (Inkwire, TMNT Shinobi). Cout 1, [mental].
# Uses (3 samurai counters).
# Your hero gets +1 ATK.
# Forced Response: After your hero makes a basic attack, remove 1 samurai counter from this card.
#
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md) ; samurai counter / OATH (samurai-counter.md).
#
# Cartes de reference : `tmnt_shinobi_bushido/sb001` Loyalty (meme montage, pouvoir ATK au lieu de DEF) ;
# `totally_awesome_hulk/ah005` ; `trors/spider_woman/04032`.
#
# TEXTE CONTRE CODE
#  ⚠ « Forced RESPONSE » : apres l'attaque, forcee. « basic ATTACK » : `powers=["ATK"]` seulement ; un evenement
#    d'attaque (Tsujigiri...) n'est PAS un pouvoir de base : aucun compteur retire.
#  ⚠ « from THIS card » ; Uses defausse la carte au dernier compteur.


def GetAbilities() -> Sequence['Ability']:

    def courage(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        Faces.RemoveCountersOn([this], 1, 'samurai', effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("YourHero", attack=1),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.ForcedResponse,
            "You",
            courage,
            powers=["ATK"],
        ),
    ]
