from . import *

# Shapeshifting — ATTACHEMENT (Paibok). POWER SKRULL. MNG +1, boost 1 + etoile.
# Attach to Paibok.
# Paibok gains stalwart and the AERIAL trait.
# Hero Action: Spend [energy][physical] resources → discard this card.
# [star] Boost: Confuse a character you control.
#
# Cartes de reference :
#  - **`gmw 16064`** Drang's Spear : `GiveKeywordToAttached(..., stalwart=1)` ; le trait se donne par
#    le meme parametre `trait="AERIAL"` (asset.py:17, modele `40006` Technovirus Purge pour la forme).
#  - Boost : **`24017`** Double Trouble (desorienter SON personnage) ; helper `AuChoixDuJoueur`.
#
# ⚠ Mots-pieges : « gains stalwart AND the AERIAL trait » : DEUX gains dans UN appel ; Stalwart
# (« cannot be stunned or confused ») : mot-cle natif de l'hote ; `canbe_confused` (un Stalwart n'est
# pas ciblable) ; cout `[energy][physical]` = `YR` (eclair + poing).


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        AuChoixDuJoueur(effect, message.GetToPlayer(),
                        lambda cibles: Faces.GiveStatus(cibles, "Confused", effect),
                        canbe_confused=True)

    return [
        AttacherAPaibok(),
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name=NOM_MECHANT, card_type=Villain), stalwart=1, trait="AERIAL"),
        ActionDefausserPouvoir(Cost("YR")),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
