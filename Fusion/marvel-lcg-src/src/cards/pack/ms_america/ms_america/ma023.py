from . import *

# * Marvel Boy (Noh-Varr) — ALLIE BASIC, custom « jakxin »
# Cout 3, PV 3, ATQ 2*, CTR 1*, [energy], traits KREE + YOUNG AVENGER.
#
# Interrupt: When Marvel Boy is defeated by consequential damage, ready an
#   upgrade you control.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# Le declencheur : `kb002` Hawkeye (pack kate_bishop) et `40024` Deadpool,
# tous deux `WhenUnitWouldBeDefeated(AbilityType.Interrupt, "This", ...,
# by_consequential_damage=True)`.
#
# L'effet : `31022` Spider-Man (Otto), dont le texte imprime dit « ready an
# upgrade you control » et qui s'ecrit `Faces.ReadyAll(effect.targets,
# effect)` avec `.SetTarget(Upgrade, canbe_ready=True,
# from_where=["YouControlCards"])`. C'est la ligne exacte.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE — LE MOT « IS », PAS « WOULD BE »
#
# ⚠ Le texte imprime dit « When Marvel Boy IS DEFEATED », pas « would be
# defeated » (comparer avec ma003 Hawkeye, qui dit bien « would be
# defeated » parce qu'elle REMPLACE la defaite). Ici rien n'est remplace :
# Marvel Boy meurt, et on redresse une amelioration. On emploie donc
# `WhenUnitBeDefeated` (defeated.py:110-122) avec `by_consequential=True`,
# la fabrique du « il EST vaincu », et surtout PAS de `SetBeInstead`.
# Modele du couple : `30021` SP//dr, meme fabrique, meme `by_consequential`.
#
# « Interrupt » nu -> `AbilityType.Interrupt`, sans libelle : la carte
# n'imprime ni (defense) ni (thwart), et `Ability.Initialize`
# (ability.py:196) n'accepte de toute facon rien d'autre sur une
# interruption (piege paye sur `pt015`).
#
# « an upgrade YOU CONTROL » -> `from_where=["YouControlCards"]`, la zone de
# jeu du controleur de Marvel Boy. `canbe_ready=True` ecarte les
# ameliorations deja pretes : sans amelioration inclinee, la capacite n'a
# aucune cible legale et ne se declenche pas.
# « CONSEQUENTIAL damage » -> `by_consequential=True` ; sans lui la capacite
# partirait sur n'importe quelle defaite.
#
# ATQ 2* / CTR 1* : l'etoile vaut « degats consecutifs », lue nativement.


def GetAbilities() -> Sequence['Ability']:

    def marvel_boy(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Interrupt,
            "This",
            marvel_boy,
            by_consequential=True,
        ).SetTarget(Upgrade, canbe_ready=True, from_where=["YouControlCards"]),
    ]
