from . import *

# Galactic Council Membership — COMPLOT ANNEXE (Super-Skrull). Menace 3[per_hero],
# aucune icone.
# Forced Response: After a player attacks Super-Skrull, place 1 threat on the
#   main scheme.
#
# Cartes de reference :
#  - **`27176`** Back Alley Burglary / `AbilityFactory.AfterUnitAttackEnd` (`against_who=`) :
#    reponse a la FIN d'une attaque contre une cible nommee ; `sk104`-`sk073`
#    (scenario 1) pour `PlaceThreatOnSchemes("MainScheme", n, effect)`.
#  - **`ho015`** : `PlaceThreatOnSchemes` (carte du complot annexe, source de la menace).
#
# ⚠ Mots-pieges : « a PLAYER attacks » (un heros ou un allie d'un joueur ; pas un
# sbire, pas la Riposte) ; « attacks SUPER-SKRULL » (pas un autre ennemi) ; « AFTER »
# l'attaque, qu'elle blesse ou non ; « the MAIN scheme » (pas les annexes) ; UNE
# menace par attaque, pas par degat.


def GetAbilities() -> Sequence['Ability']:

    def conseil(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        Unused(message)
        effect.this.CastTo(EncounterSideScheme).PlaceThreatOnSchemes("MainScheme", 1, effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            CardFinder(card_type=Hero | Ally),
            conseil,
            against_who=CardFinder(name=NOM_MECHANT),
        ),
    ]
