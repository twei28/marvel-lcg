from . import *

# Inescapable Horror (2/2) — exemplaire physique 2 de 2, contenu identique a
# wc021 (voir ce fichier pour le detail des modeles et des deux portees).


def GetAbilities() -> Sequence['Ability']:

    def inescapable_horror(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        personnages = Worlds.GetOnFieldFriendlyCharacters(effect)
        if personnages:
            this.DealDamage(personnages, 1, effect)

        if not MoridunEnJeu(effect):
            return

        player = message.GetToPlayer()
        if player is None:
            return
        identite = player.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Stunned", effect)

    def inescapable_horror_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)

        player = message.GetToPlayer()
        if player is None:
            return

        personnages: List['CardFace'] = []
        identite = player.GetIdentity()
        if identite is not None:
            personnages.append(identite)
        personnages += list(player.allies.Get())

        if personnages:
            this.DealDamage(personnages, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            inescapable_horror,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            inescapable_horror_boost,
        ),
    ]
