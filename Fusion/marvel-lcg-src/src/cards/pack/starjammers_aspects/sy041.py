from . import *
# Jet Bike (Leadership, amelioration 1 [energy]). VEHICLE.
# Attach to a STARJAMMER ally. Max 1 per ally.
# Attached ally gets +1 THW and +1 ATK.
# Response: After you attach Jet Bike to an ally, ready that ally.
#
# Cartes de reference : 01074 Inspired (`CanPlayThisUpgradeCard(Ally)` + `*GiveKeywordToAttached(Ally, thwart=1)`) ; 03xxx / `AfterCardAttachTo(
# Response, "This", Unit2, op)` (RECETTES §3 : `message.to_face` = le porteur ; part aussi pour l'attache initiale).
# « After YOU attach Jet Bike » : l'attache faite en JOUANT la carte ; l'allie se redresse meme s'il etait pret (sans effet).
def GetAbilities() -> Sequence['Ability']:
    def jet_bike(effect: 'Effect', message: 'Message.AfterCardAttachTo') -> None:
        Faces.ReadyAll([message.to_face], effect)
    return [
        AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Ally, trait="STARJAMMER")),
        *AbilityFactory.GiveKeywordToAttached(Ally, thwart=1, attack=1),
        AbilityFactory.AfterCardAttachTo(
            AbilityType.Response,
            "This",
            Unit2,
            jet_bike,
        ),
    ]
