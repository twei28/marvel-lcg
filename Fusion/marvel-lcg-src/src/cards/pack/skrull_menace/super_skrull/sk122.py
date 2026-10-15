from . import *

# Flexibility — ATTACHEMENT (paquet SUPERPOWER). SUPERPOWER. +1 SCH.
# Attach to Super-Skrull.
# Super-Skrull gains stalwart and his attacks gain ranged.
#
# Cartes de reference :
#  - **`gb014`** Vicious Tendrils (pack gorr) : « Attach to <vilain> » +
#    `GiveKeywordToAttached` + `UnitAttackGainKeyword(CardFinder(name=...), ranged=True)`
#    (fiche mots-cles/ranged.md : Ranged se donne a l'ATTAQUE, jamais au personnage).
#  - **`01099`** Charge / `HasModify` : le « +1 SCH » est la cle desc `SCH+`
#    (base automatique, aucun script).
#  - **`16133`** Kree Lieutenant : Stalwart est un mot-cle natif (fiche stalwart.md) ;
#    ici DONNE a l'ennemi attache : `GiveKeywordToAttached(stalwart=1)`.
#
# ⚠ Mots-pieges : « Super-Skrull GAINS stalwart » (le mechant, pas l'attachement) ;
# « HIS ATTACKS gain ranged » (toutes ses attaques) ; pas de ★ imprime sur ces
# lignes (lues sur l'image). Une seule carte porte le nom, le mechant s'appelle
# « Super-Skrull » a tous les stades.


def GetAbilities() -> Sequence['Ability']:
    mechant = CardFinder(name=NOM_MECHANT, card_type=Villain)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(mechant),
        *AbilityFactory.GiveKeywordToAttached(stalwart=1),
        AbilityFactory.UnitAttackGainKeyword(mechant, ranged=True),
    ]
