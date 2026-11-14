from . import *

# Roots of a Black Flower — COMPLOT ANNEXE. Menace de depart 1 (fixe), 2 icones Acceleration, Boost ★.
# When Defeated : The defeating player places 2 corruption counters on their Creeping Corruption.
# [star] Boost : Choose: Either place 1 corruption counter on your Creeping Corruption, or place 4 threat on the main scheme.
#
# Cartes de reference : cw/cape_killer/56108 (`WhenSchemeBeDefeated(WhenDefeated, "This", op)` + `message.GetDefeatingPlayer()`), aoa/clan_akkaba/45162 (boost a deux branches dont une menace),
#  shadows_in_the_night/sl004a (`PlaceThreatOnSchemes("MainScheme", n, effect)`).
# ⚠ Mots-pieges : complot = `WhenSchemeBeDefeated` (pas `WhenUnitBeDefeated`) ; « the defeating player » = qui a contre la manigance (a defaut, le premier joueur) ; 2 compteurs d'un coup (4 -> 6) :
#  la Creeping Corruption retire tout ; la menace va sur le complot PRINCIPAL, pas sur cette manigance ; 2 icones Acceleration et menace de depart 1 sont lues dans `desc`.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = message.GetDefeatingPlayer() or effect.GetInitiator()
        PoserCorruption(effect, joueur, 2)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        joueur.ChooseAbilities(
            effect,
            BrancheCorruption(effect, joueur, 1),
            AbilityFactory.ForChoiceAbility("Place 4 threat on the main scheme", lambda cibles: this.PlaceThreatOnSchemes("MainScheme", 4, effect)),
        )

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
