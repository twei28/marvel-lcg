from . import *

# * Scarlet Spider (face heros)
# Extreme Interrogation — Response: After you deal excess damage to a
#   minion, shuffle it back into the encounter deck. Then, remove threat
#   from a scheme equal to the amount of excess damage dealt. (Max 3 threat
#   per minion.)
#
# Modele : aoa/genosha/45136.py (Genoshan Mech) et mut_gen/zero_tolerance/
# 32104.py (Operation Zero Tolerance), meme couple `AfterUnitAttackAndDefeatUnit
# "This" -> Minion, has_excess_damage=True` + `message.target` = la carte
# vaincue, ENCORE deplacable a ce stade (le nettoyage generique n'a pas
# encore eu lieu). Rebarrassage dans le deck de rencontre : modele Spot
# (spdr/iron_spiders_sinister_six/31036.py, `Faces.ShuffleAllTo([this],
# "EncounterDeck", effect)`). Retrait de menace : modele falcon/53035.py
# (Winter Soldier, `.SetTarget(Scheme2)` + `RemoveThreatFromSchemes`), avec
# un montant DYNAMIQUE plafonne a 3 au lieu du 2 fixe de Winter Soldier.


def GetAbilities() -> Sequence['Ability']:

    def extreme_interrogation(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        minion = message.target
        Faces.ShuffleAllTo([minion], "EncounterDeck", effect)

        amount = min(message.excess_damage, 3)
        this.RemoveThreatFromSchemes(effect.targets, amount, effect)

    return [
        AbilityFactory.AfterUnitAttackAndDefeatUnit(
            AbilityType.Response,
            "This",
            Minion,
            extreme_interrogation,
            has_excess_damage=True,
        ).SetTarget(Scheme2)
        .SetName("Extreme Interrogation"),
    ]
