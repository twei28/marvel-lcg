from . import *

# * Lady Deathstrike (I) — VILAIN, stade 1. REAVER. PV 16 par joueur, ATK 2, SCH 1.
# Forced Response: After Lady Deathstrike attacks and damages you, resolve the "Special" ability on the copy of Bleeding Out
#   attached to your identity.
#
# Cartes de reference :
#  - `41013` Cypher : `AfterUnitAttackAndDamageUnit` (« attacks AND DAMAGES » : pas `AfterUnitAttackUnit`, qui part sans degat).
#  - `45113` Barrage : `message.GetToPlayer()` = le joueur attaque ; `01100`/`40090` pour « the copy ... attached to your identity ».
#  - helper du set `ResoudreSaignement` (ld005 Bleeding Out) : fiche mots-cles/special.md.
#
# ⚠ Mots-pieges :
#  - « attacks and DAMAGES you » : aucune reponse si l'attaque est entierement absorbee (defense, Tenace) ;
#  - « YOUR identity » : la copie de CE joueur (jeu a plusieurs), pas celle du premier joueur ;
#  - Forced Response : obligatoire, APRES l'attaque ; HP « 16* » = 16 par joueur (`desc.HP = "16*"`) ;
#  - nom `* Lady Deathstrike` partage avec deux SBIRES du depot : ne jamais chercher par nom (`IDS_VILAIN`).


def GetAbilities() -> Sequence['Ability']:

    def saigner(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)

        ResoudreSaignement(effect, message.GetToPlayer())

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            "You",
            saigner,
        ),
    ]
