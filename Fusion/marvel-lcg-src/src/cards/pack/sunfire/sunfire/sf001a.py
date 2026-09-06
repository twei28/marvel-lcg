from . import *

# * Sunfire (face heros) — AERIAL. FIRE. X-MEN.
#   PV 11, CTR 2, ATQ 1*, DEF 2*, main 5.
# [star] Burning Aura — Interrupt: When Sunfire makes a basic attack or basic
#   defense against an enemy, attach a set-aside copy of Burning to that enemy.
#
# ⚠ LES ETOILES SUR ATQ ET DEF NE SONT PAS DES DEGATS CONSECUTIFS. Sur un
# HEROS elles marquent la capacite Special, et le depot les ecrit quand meme
# dans les donnees : precedents `58001a` * Wonder Man (`ATK: "1*"`) et
# `61001a` * Jessica Jones (trois etoiles). Verifie au scan, pas suppose.
#
# MOT-CLE : SPECIAL — fiche `docs/reference/mots-cles/special.md`. Le `[star]`
# n'a AUCUNE mention « in expert mode » : la capacite est TOUJOURS active. Elle
# porte un type imprime (`Interrupt`), c'est donc celui-la qu'on ecrit.
#
# CARTES DE REFERENCE
#  - `yondu/yd001a` « D'ast Whistlin' » : le heros dont la capacite se
#    declenche sur les mouvements d'une amelioration attachee a un ennemi.
#    C'est le pack jumeau de celui-ci pour la brique 6.
#  - `WhenUnitWouldAttack` / `WhenUnitDefendAgainstAttack` : les deux fenetres
#    d'un pouvoir de base, cote attaque et cote defense.
#
# TEXTE CONTRE CODE
#  ⚠ « makes a BASIC attack or BASIC defense » -> `is_basic_attack=True` cote
#    attaque (do_attack.py:38) et `is_basic_defense=True` cote defense. ⚠ Les
#    deux fabriques ne nomment PAS le parametre pareil : `is_basic_power`
#    n'existe pas sur `WhenUnitWouldAttack`, et le passer leve un TypeError
#    attrape par `test_cards`, pas par la lecture. Une attaque d'EVENEMENT (`sf005` Solar Blast) ne
#    declenche PAS cette capacite : elle pose sa propre brulure, et confondre
#    les deux doublerait la mise.
#  ⚠ « AGAINST AN ENEMY » -> la cible de l'attaque, ou l'ATTAQUANT dans le cas
#    de la defense. Les deux fenetres ne nomment pas la meme carte, d'ou deux
#    operations et non une.
#  ⚠ INTERRUPT, donc AVANT que le pouvoir ne se resolve : la brulure est deja
#    posee quand les degats tombent. C'est ce qui permet a `sf002` Atomic Fire,
#    jouee ensuite, de compter cet ennemi-la.
#  « a SET-ASIDE copy » -> la reserve. Six exemplaires en circulation ; quand
#    elle est vide, la capacite ne fait rien, et c'est le plafond du pack.
#  ⚠ Le nom « Sunfire » n'est employe NULLE PART pour retrouver le heros :
#    `35014` * Sunfire est un ALLIE du pack wolverine.


def GetAbilities() -> Sequence['Ability']:

    def bruler_la_cible(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
        for cible in list(getattr(message, "targets", []) or []):
            if Enemy.IsType(cible):
                AttacherUneBrulure(effect, cible)

    def bruler_lattaquant(effect: 'Effect', message: 'Message.WhenUnitDefendAgainstAttack') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
        attaquant = getattr(message, "attacker", None)
        if attaquant is not None and Enemy.IsType(attaquant):
            AttacherUneBrulure(effect, attaquant)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            "This",
            bruler_la_cible,
            is_basic_attack=True,
        ),
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.Interrupt,
            "This",
            bruler_lattaquant,
            is_basic_defense=True,
        ),
    ]
