from . import *

# King's Gambit

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Put the top card of your deck into play facedown as a
        # CORRUPT side scheme. Kingpin schemes. »
        joueur = message.GetToPlayer()
        PoserUneManiganceCorrompue(joueur, effect)
        villain = Worlds.FindVillain(effect)
        if villain:
            villain.DoSchemes(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: Discard 1 card from the top of the encounter deck for
        # each pursuit counter on Pursued by the Past. »
        combien = NombreDeCompteursDePoursuite(effect)
        if combien > 0:
            Worlds.DiscardEncounterCards(combien, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
