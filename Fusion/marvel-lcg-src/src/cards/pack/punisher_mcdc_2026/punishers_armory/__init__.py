from ..commun import *

# Set Punisher's Armory (pack MC×DC 2026) : trois armes a munitions + une grenade + le complot qui les sort du paquet.
#
# Les trois armes (pu115-117) partagent : « Armament. Weapon. Attach to Punisher. Otherwise, attach to the villain. »
# et « When Revealed : Discard each other ARMAMENT card in play ».
# Cartes de reference : galactic_storm/kree_sentry/gs083.py (attache + mots-cles de l'attache), `AttachToFaceWhenPutIntoPlay
# (..., otherwise_attach_to=Villain)` (game/ability/factory/attachment.py).
#
# ⚠ « attach to PUNISHER. Otherwise, attach to the VILLAIN » : le vilain du scenario 3 s'appelle Punisher (PU-4) ; tant
# qu'il n'est pas en jeu (essais avec un autre vilain) l'arme va au vilain en jeu.

def AttacherPunisherSinonVilain() -> 'Ability':
    return AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Punisher", card_type=Villain), otherwise_attach_to=Villain)


def DefausserLesAutresArmements(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
    this = effect.this
    autres = [c for c in Worlds.FindCardsOnField(effect, trait="ARMAMENT") if c is not this]
    if autres:
        Faces.DiscardAll(autres, effect)
