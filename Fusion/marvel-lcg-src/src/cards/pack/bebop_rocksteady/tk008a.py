from . import *

# Rhino Rage (Temper de Rocksteady, face ROWDY)

def GetAbilities() -> Sequence['Ability']:

    def par_compteur(effect: 'Effect', face: 'CardFace', ui: List['CardFace']) -> int:
        return Compteurs(effect.this)

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.PlaceCountersOn([this], 1, COMPTEUR, effect)
        if Compteurs(this) >= 3:
            this.card.Flip(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(SurLeVilain("Rocksteady")),
        *AbilityFactory.GiveKeywordToAttached(
            Villain, get_new_value=par_compteur, attack=1,
            ex_change_on_event=OnEvent.Counter("This", COMPTEUR)),
        AbilityFactory.WhenResolveSpecialAbility("This", special),
    ]
