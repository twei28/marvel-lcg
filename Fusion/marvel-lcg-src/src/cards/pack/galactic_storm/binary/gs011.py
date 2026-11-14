from . import *

# Light, Radiation, Heat — AMELIORATION, cout 1, [mental]. SUPERPOWER. Binary 15/15.
# While the number of [energy] resources in your hand is at least:
#  • 1 - Your basic attacks gain ranged.
#  • 2 - Your basic attacks also gain piercing.
#  • 3 - Your basic attacks also gain overkill.
#
# Cartes de reference :
#  - **`ho016`** / **`27078`** : « attacks gain overkill/piercing/ranged » =
#    `UnitAttackGainKeyword(attacker, overkill=, piercing=, ranged=)`
#    (`do_attack.py:828`, message `CheckIfAttackMessageHasKeyword`), RECETTES §3.
#  - « basic attacks » : parametre `is_basic_attack=True` de la meme fabrique.
#  - fiches `mots-cles/ranged.md`, `piercing.md`, `overkill.md`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « YOUR basic attacks » : `"You"` = l'identite (seule la forme heros
#    attaque) ; les attaques d'un allie et les evenements d'attaque ne gagnent
#    rien (`is_basic_attack=True`, contre-cas Solar Flare).
#  - « AT LEAST » : paliers CUMULATIFS (« also gain ») : 1 -> distance ;
#    2 -> distance + perforant ; 3 et plus -> les trois.
#  - le compte est lu au moment ou le moteur demande si l'attaque a le mot-cle
#    (pendant l'attaque), donc sur la main du moment. Helper `EnergieEnMain`.


def AuMoins(n: int):
    def condition(effect: 'Effect', message: 'Message.CheckIfAttackMessageHasKeyword') -> bool:
        Unused(message)
        return EnergieDuJoueur(effect) >= n
    return condition


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            is_basic_attack=True,
            conditions=[AuMoins(1)],
            ranged=True,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            is_basic_attack=True,
            conditions=[AuMoins(2)],
            piercing=True,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            is_basic_attack=True,
            conditions=[AuMoins(3)],
            overkill=True,
        ),
    ]
