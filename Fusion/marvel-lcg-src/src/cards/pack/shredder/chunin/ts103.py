from . import *

# * Kira no Ken — ATTACHEMENT UNIQUE (set Chunin). FOOT CLAN. RELIC. WEAPON.
# ATQ +1*, 2 icones de boost.
# Attach to Karai. If Karai is not in play, search the encounter deck and discard
# pile for Karai and reveal her. Then, attach this card to her.
# [star] Attached minion's attacks gain piercing.
#
# Cartes de reference : `01100` (`AttachToFaceWhenPutIntoPlay`) avec son
# `if_cannot_operation` (« if you cannot attach ... ») pour la branche « Karai
# n'est pas en jeu » ; `ts102` (la recherche de Karai) ; `UnitAttackGainKeyword`
# pour « attacks gain piercing ».
#
# Mots-pieges : « Karai » = ts101 OU tl015 (meme personnage, `IDS_KARAI`) ;
# « Then, attach this card to HER » : apres la revelation ; si Karai reste
# introuvable, la carte n'a nulle part ou s'attacher et est defaussee.


def GetAbilities() -> Sequence['Ability']:

    def karai_absente(effect: 'Effect', joueur: 'Player') -> None:
        this = effect.this.CastTo(Attachment)
        face = Search.EncounterCard(
            effect, joueur,
            include_discard_pile=True,
            finder=CardFinder(card_ids=IDS_KARAI),
        )
        if face:
            face.Reveal(joueur, effect)
        karai = Worlds.FindCardOnField(effect, card_ids=IDS_KARAI, card_type=Minion)
        if karai:
            this.AttachTo2(karai, effect)
        else:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_ids=IDS_KARAI, card_type=Minion),
            if_cannot_operation=karai_absente,
        ),
        AbilityFactory.UnitAttackGainKeyword("AttachedMinion", piercing=True),
    ]
