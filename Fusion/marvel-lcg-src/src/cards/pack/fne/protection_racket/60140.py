from . import *

# * Man-Bull (BRUTE) — SCH 2, ATK 4, 6 PV, boost 2.
# [star] Forced Response: After Man-Bull attacks, place threat on the main
#   scheme equal to the excess damage dealt by this attack.
# [star] Boost: If this activation is an attack, place threat on the main
#   scheme equal to the excess damage dealt by this attack.
#
# ⚠ REECRITE LE 18/09/2026 : LA CARTE ETAIT INERTE, ET SES DEUX CAS PASSAIENT.
# La version precedente lisait `AfterUnitAttackEnd.excess_damage`, qui
# N'EXISTE PAS (sender_damage.py:558 : le message porte `total_dealt_damage`,
# `damaged_targets`, `atk_messages`). `getattr(..., 0)` rendait donc toujours
# 0, aucune menace n'etait posee — et les deux cas restaient verts parce que
# Battle in the Bodega (60134b) pose 1 menace de son cote sur la meme attaque.
# C'est la preuve par SUBSTITUTION qui l'a montre : « SUBST 60140 : rouges
# 0/2 », les deux cas verts sans le module.
#
# L'exces n'existe qu'A LA DEFAITE (`WhenUnitBeDefeated.excess_damage`,
# sender_unit.py:70 = `-health` apres coup), comme pour 60135b Bull in a China
# Shop. On ecoute donc la defaite, filtree sur « vaincu par CETTE carte, au
# cours d'une attaque, avec de l'exces » : `by_attack=True`, `attacker="This"`,
# `took_excess_damage=True`. Un personnage vaincu par autre chose, ou sans
# exces, ne declenche rien.
#
# ⚠ « the main scheme » DANS CE SET : il y en a un PAR JOUEUR. La menace tombe
# sur le complot du joueur qui controlait le personnage vaincu (meme regle que
# la manigance de base du vilain, voir __init__.py), et sur « MainScheme » en
# dernier recours.


def PoserLExces(porteur: 'CardFace', message: 'Message.WhenUnitBeDefeated',
                effect: 'Effect') -> None:
    exces = int(message.excess_damage or 0)
    if exces <= 0:
        return
    vaincu = message.trigger
    complot = None
    proprietaire = vaincu.GetControlByOrOwner() if vaincu is not None else None
    if Player.IsType(proprietaire):
        complot = ComplotDuJoueur(effect, proprietaire)
    porteur.PlaceThreatOnSchemes([complot] if complot is not None else "MainScheme",
                                 exces, effect)


def GetAbilities() -> Sequence['Ability']:

    def poser(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        PoserLExces(effect.this, message, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        being = message.being_message
        ennemi = message.activating_enemy
        if being is None or not being.IsAttack() or ennemi is None:
            return
        # ⚠ `unregister_after_exec` est OBLIGATOIRE (mot-cle sans defaut) :
        # sans lui, TypeError avale a chaque boost (autoplay du 18/09/2026).
        # La capacite est posee sur l'ENNEMI QUI S'ACTIVE (« this activation »),
        # pas sur Man-Bull, qui n'est qu'une carte de boost ici.
        ennemi.effect.RegisterTemp(
            AbilityFactory.WhenUnitBeDefeated(
                AbilityType.Temp0,
                Unit2,
                poser,
                by_attack=True,
                attacker="This",
                took_excess_damage=True,
            ),
            unregister_after_exec=True,
            until_phase_end=True,
        )

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.ForcedResponse,
            Unit2,
            poser,
            by_attack=True,
            attacker="This",
            took_excess_damage=True,
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
