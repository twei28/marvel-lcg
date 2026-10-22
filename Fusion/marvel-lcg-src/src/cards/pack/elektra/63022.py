from . import *

# * Stone — ALLIE 3 [physical], aspect Basic (Elektra Natchios 22). MARTIAL ARTIST. PV 3, THW 1*, ATK 2**.
# Response: After Stone exactly defeats an enemy or side scheme, heal 2 damage from Stone.
#
# CARTES DE REFERENCE
#  - `ua019` Flow of Battle / `pu026` : « exactly defeat an enemy » = `AfterUnitDefeatedUnit(..., has_excess_damage=False)` ;
#    « exactly defeat a side scheme » = `AfterUnitDefeatedScheme` + `message.excess_thwart == 0` (champ du moteur, pu026).
#  - `43011` Pain Tolerance / `40197` Safehouse : `this.HealthUnits(cibles, N, effect)` + `.SetTarget(..., canbe_heal=True)`.
#
# TEXTE CONTRE CODE
#  ⚠ « Stone EXACTLY defeats » : c'est STONE le vainqueur (`"This"`), sans exces ; un exces ne declenche rien (deux cas).
#  ⚠ « an enemy OR side scheme » : DEUX declencheurs (un ennemi vaincu par ses coups, une annexe dejouee par sa parade).
#  ⚠ « heal 2 damage FROM STONE » : sur lui-meme, 2 points (pas davantage que ce qu'il porte).


def GetAbilities() -> Sequence['Ability']:

    def stone(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.HealthUnits([this], 2, effect)

    def annexe_pile(effect: 'Effect', message: 'Message.AfterUnitDefeatedScheme') -> bool:
        return message.excess_thwart == 0

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "This",
            Enemy,
            stone,
            has_excess_damage=False,
        ).SetTarget("This", canbe_heal=True),
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.Response,
            "This",
            SchemeSide2,
            stone,
            conditions=[annexe_pile],
        ).SetTarget("This", canbe_heal=True),
    ]
