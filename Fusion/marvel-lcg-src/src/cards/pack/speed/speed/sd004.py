from . import *

# Blasting Velocity (2/2) — exemplaire physique 2 de 2, contenu identique a
# sd003 (voir ce fichier pour le detail des modeles et des arbitrages, dont le
# rappel « ne pas copier Swift Strikes dessus, c'est un miroir »).


def GetAbilities() -> Sequence['Ability']:

    def blasting_velocity(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        heros = joueur.GetHero()
        if heros is None:
            return

        cibles = [face for face in FacesAvecUnCompteurExplosif(effect)
                  if Enemy.IsType(face)]
        if not cibles:
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Make a basic attack against an enemy with an explosive counter on it, without exhausting",
                lambda targets:
                    heros.BasicAttack(list(targets), effect),
            ).SetTarget(Enemy, has_counter=COMPTEUR_EXPLOSIF, range=(1, 1)),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            blasting_velocity,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
