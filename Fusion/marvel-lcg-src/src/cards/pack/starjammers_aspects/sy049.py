from . import *
# Armored Space Suit (Protection, amelioration 1 [physical]). ARMOR. TECH.
# Attach to a STARJAMMER ally. Max 1 per ally.
# Attached ally gains the AERIAL trait.
# Response: After this card enters play, give the attached ally a tough status card.
#
# Cartes de reference : 01074 Inspired (`CanPlayThisUpgradeCard(..)` + `*GiveKeywordToAttached(Ally, trait="AERIAL")`) ; sy041 Jet Bike
# (`AfterCardAttachTo(Response, "This", Unit2, op)` : `message.to_face` = le porteur, RECETTES §3 : un compteur/statut pose AVANT l'attache est
# perdu) ; `Faces.GiveStatus([porteur], "Tough", effect)`.
def GetAbilities() -> Sequence['Ability']:
    def combinaison(effect: 'Effect', message: 'Message.AfterCardAttachTo') -> None:
        Faces.GiveStatus([message.to_face], "Tough", effect)
    return [
        AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Ally, trait="STARJAMMER")),
        *AbilityFactory.GiveKeywordToAttached(Ally, trait="AERIAL"),
        AbilityFactory.AfterCardAttachTo(
            AbilityType.Response,
            "This",
            Unit2,
            combinaison,
        ),
    ]
