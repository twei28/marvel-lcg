from . import *

# Electricity Projection — ATTACHEMENT (Paibok). POWER SKRULL. ATQ +1, boost 1 + etoile.
# Attach to Paibok.
# Paibok gains retaliate 1.
# Hero Action: Spend [mental][physical] resources → discard this card.
# [star] Boost: Stun a character you control.
#
# Cartes de reference :
#  - **`gmw 16064`** Drang's Spear : `AttachToFaceWhenPutIntoPlay(CardFinder(name=...))` +
#    `GiveKeywordToAttached(..., <mot-cle>=1)` + action de defausse (`PlayerActionToDiscardThis`).
#    Ici `retaliate=1` (fabrique `GiveKeywordToAttached`, asset.py:6). `ATK+ 1` : natif (desc).
#  - Boost : **`24017`** Double Trouble (choisir son personnage a etourdir) ; helper `AuChoixDuJoueur`.
#
# ⚠ Mots-pieges : « Paibok gains retaliate 1 » (le MECHANT, via l'attache) ; « a character YOU CONTROL »
# (le joueur qui subit le Boost, pas un ennemi) ; `canbe_stunned` (un Stalwart n'est pas ciblable) ;
# cout `[mental][physical]` = `BR` (nœuds = mental ; poing = physique) ; la defausse n'est offerte que
# si les pouvoirs ne sont pas verrouilles (`ActionDefausserPouvoir`).


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        AuChoixDuJoueur(effect, message.GetToPlayer(),
                        lambda cibles: Faces.GiveStatus(cibles, "Stunned", effect),
                        canbe_stunned=True)

    return [
        AttacherAPaibok(),
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name=NOM_MECHANT, card_type=Villain), retaliate=1),
        ActionDefausserPouvoir(Cost("BR")),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
