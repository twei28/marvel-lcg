from . import *

# * Sif's Sword — amelioration signature, x1 (n/15 = 15).
# ASGARD. WEAPON. Cout 2, ressource [physical].
# Restricted.
# Lady Sif gets +1 ATK while in hero form. While in hero form, Lady Sif's
#   basic attacks gain piercing.
#
# Cartes de reference :
#  - `03009` / `ls010` du meme pack pour `GiveKeywordToAttached(Hero,
#    attack=1)` ;
#  - **`27078` "Now We're Angry!"** pour le mot-cle d'attaque :
#    `UnitAttackGainKeyword(<qui>, piercing=True)`.
#
# ⚠ `Restricted` est une base automatique (`desc.Restricted`) : aucun module.
# Avec ls010, ce sont les deux seules Restricted du pack — un joueur peut donc
# porter les deux, et pas une de plus.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « BASIC attacks » seulement. `is_basic_attack=True` est indispensable :
#    sans lui, Impale (ls003) et Lead The Charge gagneraient le piercing eux
#    aussi, ce que le texte n'accorde pas. ⚠ Lead The Charge fait faire une
#    attaque de BASE : celle-la, elle, gagne bien le piercing.
#  - « WHILE IN HERO FORM », repete DEUX fois sur la carte : il porte sur le
#    +1 ATQ **et** sur le piercing. D'ou `Hero` des deux cotes, jamais
#    `"You"`.
#  - Le nom « Lady Sif » est porte par les deux faces ET par un allie officiel
#    (`06002`) : on cible par TYPE de face et par controle, pas par nom. Pour
#    l'attaquant, `"You"` (`GetYouRule(..., identity=True)`) borne a NOTRE
#    identite ; « while in hero form » est alors implicite, un alter-ego
#    n'attaquant jamais.
#  - `piercing` ignore les cartes Tenace et les preventions de dégâts : c'est
#    ce qui fait de Skurge (ls015, Toughness) une cible naturelle.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            attack=1,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            piercing=True,
            is_basic_attack=True,
        ),
    ]
