from . import *

# * Damaged Spine (TECH) — Permanent.
# [star] Forced Response: After Bullseye schemes, remove 3 damage from here.
#   Then, if there is no damage here, flip this card.

def GetAbilities() -> Sequence['Ability']:

    def repare(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.RemoveCountersOn([this], 3, 'damage', effect)
        if this.GetCounters('damage') <= 0:
            RetournerLaColonne(this, effect)

    return [
        # Le retournement DETACHE la carte (« Bullseye perd l'amelioration »,
        # constate au harnais) : comme 55007b, la face B porte son propre
        # AttachToFaceWhenPutIntoPlay pour se raccrocher.
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Bullseye")),
        AbilityFactory.AfterUnitSchemeEnd(
            AbilityType.ForcedResponse,
            CardFinder(name="Bullseye"),
            repare,
        ),
    ]
