from . import *

# Encore
# SONG.
# Max 2 per deck.
# Hero Action: Search your discard pile for a SONG card and add it to your hand.
#
# Elle-meme est un [[SONG]], mais elle n'est pas encore a la defausse quand son
# effet se resout : elle ne peut donc pas se rechercher elle-meme.


def GetAbilities() -> Sequence['Ability']:

    def encore(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        # CORRECTIF (partie reelle) : `include_player_deck` est un argument
        # OBLIGATOIRE de `Search.PlayerCard` (search.py:133). Sans lui, jouer
        # Encore levait `TypeError: Search.PlayerCard() missing 1 required
        # keyword-only argument`. La carte ne cherche QUE dans la defausse :
        # `include_player_deck=False`.
        face = Search.PlayerCard(
            effect, joueur,
            include_player_deck=False, include_discard_pile=True,
            trait=TRAIT_SONG)
        if face:
            Faces.AddToHand([face], joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            encore,
        ).SetPlay().SetLabel(),
    ]
