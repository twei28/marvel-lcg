from . import *

# * Casey Jones — ALLIE 3 [physical], 1*/2*, 2 PV, aspect Basic (MC Custom Content, Inkwire). VIGILANTE.
# Response: After Casey Jones enters play, search your deck and discard pile for a [[WEAPON]] upgrade and add
#   it to your hand. (Shuffle.)
#
# NOUVELLE. Carte de reference : 23002 Iron Man (allie) — « After Iron Man enters play, search your deck and
# discard pile for a TECH upgrade and add it to your hand » : meme declencheur `AfterCardEnterPlay("This")`,
# meme fouille `Search.PlayerCard(include_player_deck, include_discard_pile, card_type=Upgrade, trait=...)`.
# TEXTE CONTRE CODE : « deck AND discard pile » (les deux) ; « a WEAPON UPGRADE » (type + trait) ; « Response »
# (facultative) ; « (Shuffle.) » : la fouille du deck le remelange (Search.PlayerCard).


def GetAbilities() -> Sequence['Ability']:

    def casey_jones(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            card_type=Upgrade,
            trait="WEAPON",
        )
        if face:
            Faces.AddToHand([face], initiator, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            casey_jones
        ),
    ]
