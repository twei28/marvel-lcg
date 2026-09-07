from . import *

# * Blade — HEROS. AVENGER. VAMPIRE. CTR 2 / ATQ 2 / DEF 2 — main 5 / 12 PV.
# [star] Blood Rush — Response: After Blade uses a basic power, remove 1 blood
#   counter from him -> ready Blade. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `ls001a` Valiant Warrior (Lady Sif) : `AfterUnitUseBasicPower(Response,
#    "You", op)`, les TROIS pouvoirs de base (`powers=None`), UNE seule
#    question au joueur (lecon autoplay du 03/09 : pas de ChooseAbilities).
#  - `61033a` Suggestion : le pion en COUT, `CostFunc.Counter("This", 1, ...)`.
#  - `23001a` War Machine : des pions sur l'IDENTITE.
#
# TEXTE CONTRE CODE
#  ⚠ « a basic power » -> contrer, attaquer OU defendre. Un Blade qui defend
#    puis se redresse peut defendre une seconde fois dans la phase du mechant.
#  ⚠ « remove 1 blood counter FROM HIM » -> le pion est sur l'identite (la
#    carte, pas la face : Eric Brooks les pose, Blade les depense).
#  ⚠ « Limit once per PHASE » -> PARTAGEE avec la version Daywalker (bl009) :
#    meme `SetName`, condition `BloodRushPasEncoreResolue`. Redresser Blade par
#    Daywalker interdit Blood Rush dans la meme phase, et inversement.
#  ⚠ Pas de boucle : se redresser n'est pas un pouvoir de base.


def GetAbilities() -> Sequence['Ability']:

    def blood_rush(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)
        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "You",
            blood_rush,
            conditions=[BloodRushPasEncoreResolue],
        ).SetName(NOM_BLOOD_RUSH)
        .SetCostFunc(CostFunc.Counter("This", 1, COMPTEUR_SANG))
        .LimitOncePerPhase(),
    ]
