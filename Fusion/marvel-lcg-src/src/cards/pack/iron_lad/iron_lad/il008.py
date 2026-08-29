from . import *

# Seeking Solutions (2/2) — contenu identique a il007, voir ce fichier pour
# le detail du modele repris.

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
