from . import *

# Star Portal (2/2) - exemplaire physique 2/2, contenu identique a ma013
# (voir ce fichier pour le detail des modeles et de l'ecart de
# construction sur la fleche-cout).


def GetAbilities() -> Sequence['Ability']:

    def allies_des_defausses(effect: 'Effect') -> List['CardFace']:
        faces: List['CardFace'] = []
        for joueur in Worlds.GetPlayers(effect):
            faces.extend(joueur.discard_pile.FindCards(card_type=Ally))
        return faces

    def star_portal(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        candidats = allies_des_defausses(effect)
        if not candidats:
            return

        # « any player's play area » : le joueur de destination est la cible
        # de la capacite. En solo c'est toujours le joueur actif.
        destination = initiator
        if effect.targets:
            joueur = effect.targets[0].GetControlByPlayer()
            if joueur is not None:
                destination = joueur

        allie = initiator.MayChooseOneText(candidats)
        if allie is None:
            return

        allie.PutIntoPlay(destination, effect, under_control=True, exhaust=True)

        menace = max(0, getattr(allie, 'thwart', 0))
        degats = max(0, getattr(allie, 'attack', 0))

        if menace > 0:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Star Portal: remove threat from a scheme",
                    lambda targets:
                        this.RemoveThreatFromSchemes(list(targets), menace, effect),
                ).SetTarget(Scheme2),
            )

        if degats > 0:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Star Portal: deal damage to an enemy",
                    lambda targets:
                        this.DealDamage(list(targets), degats, effect),
                ).SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            star_portal,
            conditions=[
                lambda effect, message: allies_des_defausses(effect) != [],
            ],
        ).SetPlay()
        .SetTarget("Players", range=(1, 1)),
    ]
