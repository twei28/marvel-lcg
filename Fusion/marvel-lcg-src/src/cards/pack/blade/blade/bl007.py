from . import *

# Bandolier of Stakes — AMELIORATION, cout 1, [physical]. ITEM. WEAPON.
# Uses (3 stake counters).
# Hero Interrupt: When a hero attacks, remove 1 stake counter from here -> that
#   attack deals 1 additional damage and gains piercing.
#
# CARTES DE REFERENCE
#  - `39048` Bandolier of Stakes (Mojo, set Horror) : LE modele, meme nom, meme
#    pion `stake`, `WhenUnitMakeAttack(HeroInterrupt, ...)` +
#    `CostFunc.Counter("This", 1, 'stake')` ; Uses lu dans `desc`
#    (fiche uses.md : ne PAS coder la sortie de jeu).
#  - `DealAdditionalDamage` (sender_damage.py:128) plutot que
#    `GainATKForThisAttack`, qui ASSERT une attaque de base : ici « a hero
#    attacks » couvre aussi les attaques d'evenement (Go for the Heart).
#
# TEXTE CONTRE CODE
#  ⚠ « When A HERO attacks » -> n'importe quel heros (multijoueur), toute
#    attaque, de base ou d'evenement : `attacker=Hero`, pas de
#    `is_basic_attack`. Le Bandolier de Mojo (39048) dit « YOUR hero » et
#    « BASIC attack » : ce n'est PAS la meme carte.
#  ⚠ « deals 1 ADDITIONAL damage and gains piercing » -> les deux, toujours.
#  ⚠ C'est une amelioration WEAPON : Go for the Heart et Vampiric Reflexes
#    peuvent l'incliner. Elle n'a pas de capacite a inclinaison, l'incliner
#    ne coute rien d'autre.


def GetAbilities() -> Sequence['Ability']:

    def planter_un_pieu(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.DealAdditionalDamage(1, effect)
        message.GainPiercing(effect)

    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            Hero,
            planter_un_pieu,
        ).SetCostFunc(CostFunc.Counter("This", 1, COMPTEUR_PIEU)),
    ]
