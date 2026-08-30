from . import *

# Impenetrable Barrier (2/2) — exemplaire physique 2 de 2, contenu identique
# a wc003 (voir ce fichier pour le detail des modeles et des arbitrages).


def GetAbilities() -> Sequence['Ability']:

    def impenetrable_barrier(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        identite = initiator.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Tough", effect)

        icones = IconesBoostDuDessus(effect, initiator)
        if icones <= 0:
            return

        candidats = Worlds.GetOnFieldFriendlyCharacters(
            effect,
            CardFinder(canbe_status="Tough"),
        )
        if not candidats:
            return

        choisies = initiator.AskChooseFaces(
            candidats,
            (0, icones),
            effect,
            prompt="Give a Tough status card",
            not_move=True,
        )
        if choisies:
            Faces.GiveStatus(choisies, "Tough", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            impenetrable_barrier,
        ).SetPlay(),
    ]
