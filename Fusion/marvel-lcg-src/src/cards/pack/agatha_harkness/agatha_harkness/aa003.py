from . import *

# * Ebony — soutien signature. CREATURE. Cout 1.
# While in alter-ego form, Agatha Harkness gets +1 REC.
# Alter-Ego Action: Exhaust Ebony -> look at the top 2 cards of your deck.
#   Add 1 of those cards to your hand.
#
# Cartes de reference (RECETTES-MOTEUR §3) :
#  - +1 REC : ho005 Gwen Stacy Osborn, `GiveKeywordToInPlayWhenApplyThis(
#    Identity, control_by="You", recover=1)` — « while in alter-ego form »
#    est porte par le REC lui-meme, qui n'existe qu'en alter-ego ;
#  - le coup d'oeil : 51016 (pack bp), `player.LookAtDeck(...)` +
#    `AskChooseFaces` + `GainCard`, la carte non prise RESTE sur le deck
#    (regarder n'est pas defausser, lecon ag004).

def GetAbilities() -> Sequence['Ability']:

    def ebony(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        faces = initiator.LookAtDeck(initiator.player_deck, 2, effect)
        if not faces:
            return
        choisies = initiator.AskChooseFaces(faces, (1, 1), effect)
        if choisies:
            initiator.GainCard(list(choisies), effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity,
            control_by="You",
            recover=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            ebony
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
