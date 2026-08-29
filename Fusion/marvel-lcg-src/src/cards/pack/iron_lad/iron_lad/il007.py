from . import *

# Seeking Solutions (1/2)
# Alter-Ego Action: Shuffle 2 cards from your discard pile back into your
#   deck. Draw 1 card for each TECH card shuffled into your deck this way.
#
# `initiator.AskChooseFaces(..., (0, 2), effect, forced=False)` sur la
# defausse, puis `Faces.ShuffleAllTo(...)` (modele : magneto/49002.py
# Asteroid M). `initiator.DrawUp(N, effect)` pour la pioche (modele :
# albert/ab001a.py).

def GetAbilities() -> Sequence['Ability']:

    def seeking_solutions(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        choisies = initiator.AskChooseFaces(initiator.discard_pile.Get(), (0, 2), effect, forced=False)
        if not choisies:
            return

        nb_tech = len([f for f in choisies if f.HasTrait("TECH")])
        Faces.ShuffleAllTo(choisies, initiator.player_deck, effect)
        if nb_tech:
            initiator.DrawUp(nb_tech, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            seeking_solutions
        ).SetPlay(),
    ]
