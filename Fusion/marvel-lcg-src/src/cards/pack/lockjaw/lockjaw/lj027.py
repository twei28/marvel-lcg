from . import *

# Animals Unleashed — custom « Nugget » (carte d'aspect BASIC)
# Max 1 per deck.
# Hero Action: Each player may search their deck, hand and discard pile for a
#   PET AVENGER ally and put it into play. Each PET AVENGER gets +1 ATK until
#   the end of the round.


def GetAbilities() -> Sequence['Ability']:

    def lacher_la_meute(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        for joueur in Worlds.GetPlayers(effect):
            face = Search.PlayerCard(
                effect,
                joueur,
                include_player_deck=True,
                include_discard_pile=True,
                include_player_hand_cards=True,
                may=True,
                trait="PET AVENGER",
                card_type=Ally,
            )
            if face:
                face.PutIntoPlay(joueur, effect)

        for compagnon in Worlds.FindCardsOnField(effect, card_type=Ally):
            if compagnon.HasTrait("PET AVENGER"):
                compagnon.GainUntilPhaseEnd(effect, attack=1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lacher_la_meute,
        ).SetPlay(),
    ]
