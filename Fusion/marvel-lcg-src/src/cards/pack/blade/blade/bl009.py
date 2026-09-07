from . import *

# Daywalker — AMELIORATION, cout 2, [energy]. SUPERPOWER. TITLE.
# You get +3 hit points and your Vampire Bite attacks gain piercing.
# Hero Interrupt: When you would trigger Blade's Blood Rush ability, take 2
#   damage -> resolve that ability without paying its cost instead.
#
# CARTES DE REFERENCE
#  - `aa008` (Agatha) / `dd010` : `GiveKeywordToInPlayWhenApplyThis(..., health=3)`,
#    ici sur `"You"`.
#  - `bl001a` Blood Rush : le MEME declencheur (`AfterUnitUseBasicPower(...,
#    "You")`), le MEME nom, la MEME limite partagee.
#  - `CostFunc.TakeDamage(2, "YourIdentity")` (cost_func.py:408) : « take 2
#    damage -> ».
#
# TEXTE CONTRE CODE
#  ⚠ « your Vampire Bite attacks gain piercing » est code DANS bl005 (la
#    propriete d'une attaque se declare a sa source) : `ControleDaywalker`.
#  ⚠ « When you would trigger Blood Rush, take 2 damage -> resolve that ability
#    without paying its cost instead » -> ecrit comme une SECONDE Response au
#    meme moment (apres un pouvoir de base), a cout « 2 degats », qui redresse
#    Blade. Effet identique ; le moteur n'a pas de message « would trigger an
#    ability ». Avec zero pion de sang, seule cette version est offerte ; avec
#    des pions, le joueur voit les deux et choisit son cout.
#  ⚠ La limite « once per phase » de Blood Rush est PARTAGEE : condition
#    `BloodRushPasEncoreResolue` + `SetName(NOM_BLOOD_RUSH)` + `LimitOncePerPhase`.
#  ⚠ « take 2 damage » est un COUT : un Blade a 2 PV ou moins ne peut pas le
#    payer sans mourir ; le moteur (TakeDamageOnCall) tranche.


def GetAbilities() -> Sequence['Ability']:

    def blood_rush_sans_sang(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        heros = HerosDuJoueur(effect)
        if heros is None:
            return
        Faces.ReadyAll([heros], effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            health=3,
        ),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "You",
            blood_rush_sans_sang,
            conditions=[BloodRushPasEncoreResolue],
        ).SetName(NOM_BLOOD_RUSH)
        .SetCostFunc(CostFunc.TakeDamage(2, "YourIdentity"))
        .LimitOncePerPhase(),
    ]
