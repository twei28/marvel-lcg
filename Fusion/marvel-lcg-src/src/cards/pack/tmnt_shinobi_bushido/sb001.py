from . import *

# Loyalty — AMELIORATION OATH, classe Bushido (Inkwire, TMNT Shinobi). Cout 0, [physical].
# Uses (3 samurai counters).
# Your hero gets +1 DEF.
# Forced Response: After your hero makes a basic defense, remove 1 samurai counter from this card.
#
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md, NATIF : `desc.Uses = "3,samurai"`, le moteur pose les 3 compteurs a
# l'entree en jeu et defausse la carte au dernier retire) ; samurai counter / OATH (samurai-counter.md).
#
# Cartes de reference :
#  - « Your hero gets +1 DEF » : `totally_awesome_hulk/ah005` Motivation (`GiveKeywordToAttached("You", defense=1)`,
#    le type `Hero` ne marche que pour une carte explicitement attachee) ;
#  - « After you make a basic X » : `trors/spider_woman/04032` / `throg/tg001a` (`AfterUnitUseBasicPower`, `powers=[...]`) ;
#  - retirer un compteur de CETTE carte : `se003` / `jennika/tj006` (`Faces.RemoveCountersOn([this], 1, 'samurai', effect)`).
#
# TEXTE CONTRE CODE
#  ⚠ « Forced RESPONSE » (pas Interrupt) : `AbilityType.ForcedResponse`, APRES la defense.
#  ⚠ « your HERO makes a basic DEFENSE » : le pouvoir de base DEF seulement (`powers=["DEF"]`), ni ATK ni THW ; seule la forme
#    heros defend. Un ALLIE qui defend ne declenche pas (`"You"` = l'identite).
#  ⚠ « remove 1 samurai counter FROM THIS CARD » : cette carte-ci, pas une autre OATH ; au dernier compteur, `Uses` la defausse.
#  ⚠ Forcee : aucun choix, aucun cout.


def GetAbilities() -> Sequence['Ability']:

    def loyalty(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        Faces.RemoveCountersOn([this], 1, 'samurai', effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("YourHero", defense=1),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.ForcedResponse,
            "You",
            loyalty,
            powers=["DEF"],
        ),
    ]
