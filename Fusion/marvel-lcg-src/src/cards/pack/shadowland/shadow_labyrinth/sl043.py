from . import *

# Hall of Hidden Doors — COMPLOT ANNEXE. Menace de depart 3 (fixe), Acceleration 1, boost ★ seul.
# When Defeated : The defeating player removes 5 threat from the main scheme. They discard cards from the encounter deck until a minion or side scheme is discarded, then reveal it.
# ★ Boost : Place 3 threat on the main scheme.
#
# Cartes de reference : punisher_mcdc_2026/locations_the_big_apple/pu032 (`Worlds.DiscardEncounterCardsUntil` puis `Reveal`), shadows_in_the_night/sl007 (`WhenSchemeBeDefeated(
# WhenDefeated, "This", ...)`), mut_gen/sabretooth/32069 (`PlaceThreatOnSchemes("MainScheme", n, effect)`), mister_fantastic/mf009 (`RemoveThreatFromSchemes`).
# ⚠ Mots-pieges : « the DEFEATING player » : celui dont le personnage a vaincu la manigance (a defaut le premier joueur) ; « 5 threat from the MAIN scheme » : jusqu'a 5 ;
#  « a minion OR side scheme » : le premier des deux types (une manigance annexe de rencontre, pas la principale) ; « reveal it » : revelee a CE joueur ; deck epuise
#  sans trouver : rien n'est revele ; « 3 threat on the main scheme » en Boost (pas ici).


def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this
        joueur = getattr(message, 'defeating_player', None)
        if joueur is None or not Player.IsType(joueur):
            joueur = Worlds.GetFirstPlayer(effect)
        this.RemoveThreatFromSchemes("MainScheme", 5, effect)
        trouvee = Worlds.DiscardEncounterCardsUntil(effect, check_face_fn=lambda f: Minion.IsType(f) or EncounterSideScheme.IsType(f))
        if trouvee is not None:
            trouvee.Reveal(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        effect.this.PlaceThreatOnSchemes("MainScheme", 3, effect)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
