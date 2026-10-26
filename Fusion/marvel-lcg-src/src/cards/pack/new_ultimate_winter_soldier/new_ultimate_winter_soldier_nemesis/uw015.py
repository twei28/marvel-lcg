from . import *

# * Alonya Prostovich — sbire nemesis de Winter Soldier. EARTH-6160. DIRECTORATE X. PV 3, ATK ★, SCH ★, boost ★ seul.
# [star] Forced Interrupt: When Alonya Prostovich activates, place 2 threat on each scheme instead.
# [star] Boost: Reveal this card.
#
# Cartes de reference : `hc014` Battle for a Soul (`WhenEnemyWouldActivate(ForcedInterrupt, ..)`) ; `ap007b`/`pu014`
# (« ... instead » = `message.SetBeInstead(effect)`, `WhenEnemyWouldActivate` porte `CanBeInstead`) ; `PlaceThreatOnSchemes(
# "EachScheme", 2, effect)` (complot principal ET annexes, card_face.py) ; `16140` / `pu114` : « [star] Boost: Reveal this
# card » = `WhenCardBecomeBoost("This", RevealThisCard)`.
#
# Mots-pieges : « activates » (attaque OU manigance : elle ne fait ni l'un ni l'autre, `instead`) ; « EACH scheme » (le
# complot principal et tous les complots annexes, Directorate X compris) ; les valeurs imprimees ATK ★ / SCH ★ n'ont pas de
# chiffre (valeur donnee par le texte) : 0 dans `desc`, sans effet puisque l'activation est remplacee.


def GetAbilities() -> Sequence['Ability']:

    def alonya(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Minion)
        message.SetBeInstead(effect)
        this.PlaceThreatOnSchemes("EachScheme", 2, effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.ForcedInterrupt,
            "This",
            alonya,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RevealThisCard,
        ),
    ]
