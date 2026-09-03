from . import *

# Rocket Boots — amelioration signature, x1 (n/15 = 13).
# ARMOR. TECH. Cout 1, ressource [physical].
# Iron Man gains the AERIAL trait.
# Hero Interrupt: When you use one of Iron Man's basic powers, exhaust Rocket
#   Boots -> Iron Man gets +1 to that power for this use.
#
# Cartes de reference :
#  - `vv009` Insubstantial Flight / `ho011` pour
#    `GiveKeywordToAttached(..., trait="AERIAL")` ;
#  - **`32177` Swagger** pour la fenetre et le bonus de pouvoir :
#    `WhenUnitUseBasicPower(HeroInterrupt, 'YourHero', op)`, le message porte
#    `message.power` ('ATK' | 'THW' | 'DEF' | 'REC') et
#    `message.would_message` sur lequel se pose le bonus.
#
# ⚠ LA CARTE QUI DEBLOQUE LE PACK. Elle donne AERIAL en PERMANENCE, ce qui
# rend im002 et im003 repartissables ET fait de im004 Take Flight une source
# de compteur a 1 [energy]. C'est la piece que im001b Inventor va chercher au
# Setup (elle est TECH).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « IRON MAN gains the AERIAL trait » : un nom PROPRE, la face HEROS seule.
#    L'alter-ego s'appelle Tony Stark et ne vole pas. D'ou `Hero`, pas
#    `"You"`.
#  - « **one of** Iron Man's basic powers » : les trois, sans filtre. On ne
#    pose donc AUCUNE condition sur `message.power`, contrairement a Swagger
#    qui, lui, filtre sur 'DEF'.
#  - « +1 to **that** power » : au pouvoir employe, pas a tous. Le bonus se
#    pose sur le message du pouvoir en cours, jamais par
#    `GainUntilRoundEnd`, qui durerait tout le round.
#  - « exhaust Rocket Boots **->** » : cout, donc un seul bonus par round.
#  - Le trait AERIAL, lui, est CONTINU et ne coute rien : il survit a
#    l'inclinaison.


def GetAbilities() -> Sequence['Ability']:

    def rocket_boots(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        # « +1 to THAT power » : on ne sait pas lequel a l'avance, c'est le
        # message qui le dit.
        message.GainValue(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            trait="AERIAL",
        ),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            "You",
            rocket_boots,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
