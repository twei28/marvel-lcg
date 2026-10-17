from . import *

# * Katsuichi — ALLIE 3 [mental], 1*/2*, 3 PV, aspect Basic (TMNT Reskins, Inkwire). LION. RONIN.
# Response: After Katsuichi enters play, search your deck for an identity-specific card and add it to your
#   hand. (Shuffle).
#
# NOUVELLE (aucun allie Basic officiel ne porte ce texte). Cartes de reference : 01041 Shuri (« After Shuri
# enters play, search your deck for an upgrade and add it to your hand » : `AfterCardEnterPlay(Response,
# "This")` + `Search.PlayerCard(include_player_deck=True, ...)` + `GainCard`) ; 27048 Ghost-Spider
# (`card_class="IdentitySpecific"` pour « identity-specific »).
# TEXTE CONTRE CODE : « your DECK » seulement (pas la defausse) ; « an identity-specific CARD » (tout type).


def GetAbilities() -> Sequence['Ability']:

    def katsuichi(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            card_class="IdentitySpecific",
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            katsuichi
        ),
    ]
