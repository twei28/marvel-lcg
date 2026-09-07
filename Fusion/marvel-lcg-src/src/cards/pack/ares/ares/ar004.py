from . import *

# * Ares' Axe — AMELIORATION, cout 1, [physical]. OLYMPUS. WEAPON. UNIQUE.
# Restricted.
# Hero Interrupt: When Ares makes a basic attack against an enemy, exhaust
#   Ares' Axe -> you get +1 ATK for this attack for each upgrade attached to
#   that enemy. That attack gains piercing.
#
# CARTES DE REFERENCE
#  - `sf001a` Burning Aura (pack sunfire) : `WhenUnitWouldAttack(type, "This",
#    op, is_basic_attack=True)` pour la fenetre « makes a BASIC attack ».
#    Ici la carte est une amelioration, donc `"You"` (l'identite) et non
#    `"This"`. ⚠ Le parametre s'appelle `is_basic_attack`, PAS
#    `is_basic_power` (do_attack.py:38, lecon sf001a).
#  - `60008` Cross-Examination : `len(target.GetAttachedUpgrades())`, le compte
#    des AMELIORATIONS attachees a la cible.
#  - `19018` Subdue : `message.GainATKForThisAttack(n, effect)`.
#  - `ho016` * Bullseye : `message.GainPiercing(effect)` (fiche piercing.md).
#
# TEXTE CONTRE CODE
#  ⚠ « Restricted » : lu par le moteur dans `desc`, aucun module (RECETTES §3).
#  ⚠ « When ARES makes a basic attack » -> `"You"` + `is_basic_attack=True` :
#    l'identite, en forme heros (Hero Interrupt). Un allie qui attaque ne
#    declenche rien.
#  ⚠ « exhaust Ares' Axe → » -> le COUT est l'inclinaison de CETTE carte,
#    `CostFunc.Exhaust("This")` : une hache inclinee ne se propose plus.
#  ⚠ « for each UPGRADE attached to THAT enemy » -> les ameliorations (type
#    Upgrade) posees sur la CIBLE de l'attaque : Feint, Reeling, Sundered, ou
#    une amelioration d'aspect. ⚠ Un ATTACHEMENT de rencontre (Aegis
#    Breastplate, ar013) n'est PAS une amelioration et ne compte pas :
#    `GetAttachedUpgrades` fait exactement ce tri (helper
#    `AmeliorationsAttacheesA`). Zero amelioration = +0, mais le percant reste.
#  ⚠ « That attack gains PIERCING » -> inconditionnel des que la capacite
#    part, meme a +0.


def GetAbilities() -> Sequence['Ability']:

    def frapper_de_la_hache(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        cibles = [c for c in list(getattr(message, "targets", []) or [])
                  if c is not None and Enemy.IsType(c)]
        bonus = sum(len(AmeliorationsAttacheesA(c)) for c in cibles)
        if bonus > 0:
            message.GainATKForThisAttack(bonus, effect)
        message.GainPiercing(effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            "You",
            frapper_de_la_hache,
            is_basic_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
