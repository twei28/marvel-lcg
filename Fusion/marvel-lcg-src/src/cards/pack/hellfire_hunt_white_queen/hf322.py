from . import *

# Incite Fear (x2). Attachement ILLUSION PSIONIC. « Attach to your identity. You cannot resolve triggered abilities in your identity's printed text box
# (except for Forced abilities). Action : Discard 2 cards at random from your hand -> discard this card. »
# Cartes de reference : 27153 Induced Panic (`PlayersCannotTriggerAbility("You", "TriggeredAbility", on_which_card=...)` : les capacites FORCEES sont deja
# exclues par la fabrique, ce que dit la parenthese imprimee), `player.DiscardRandomHandCards` (04089).


def GetAbilities() -> Sequence['Ability']:
    def action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        joueur.DiscardRandomHandCards(2, effect)
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.PlayersCannotTriggerAbility("You", "TriggeredAbility", on_which_card="YourIdentity"),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, action),
    ]
