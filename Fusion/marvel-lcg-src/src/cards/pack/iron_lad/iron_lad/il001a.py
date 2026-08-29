from . import *

# * Iron Lad (face heros)
# Destiny — Action: Name a resource type and look at the top 4 cards of
#   your deck. Add up to 2 cards with the chosen resource type to your hand
#   and discard the others. (Limit once per round.)
#
# Modele : Tony Stark (core/iron_man/01029b.py), meme couple
# `initiator.LookAtDeck(deck, N, effect)` + `AskChooseFace(s)`, etendu a
# "jusqu'a 2 cartes" via `AskChooseFaces(faces, (0, 2), effect, forced=False)`
# et filtre au type de ressource nomme via `CardFinder(has_printed_res=lettre)
# .Checks(faces)` (idiome vu sur `CostFunc.Discard("YourHandCards",
# has_printed_res="B")`, toafk/kang/11019.py). Le type de ressource se nomme
# via `initiator.DeclareResourceType()` (player_ask.py), qui rend directement
# une lettre R/B/Y/G.

def GetAbilities() -> Sequence['Ability']:

    def destiny(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        initiator = effect.GetInitiator()
        lettre = initiator.DeclareResourceType()

        faces = initiator.LookAtDeck(initiator.player_deck, 4, effect)
        correspondantes = CardFinder(has_printed_res=lettre).Checks(faces)
        gardees = initiator.AskChooseFaces(correspondantes, (0, 2), effect, forced=False)

        for face in gardees:
            faces.remove(face)
        if gardees:
            Faces.AddToHand(gardees, initiator, effect)
        Faces.DiscardAll(faces, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            destiny
        ).SetName("Destiny")
        .LimitOncePerRound(),
    ]
