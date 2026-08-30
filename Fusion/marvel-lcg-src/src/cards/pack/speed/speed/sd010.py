from . import *

# Swift Strikes (3/3) — exemplaire physique 3 de 3, contenu identique a
# sd008 (voir ce fichier pour le detail des modeles et le rappel « miroir de
# Blasting Velocity, pas sa jumelle »).


def GetAbilities() -> Sequence['Ability']:

    def swift_strikes(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 3, effect)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        heros = joueur.GetHero()
        if heros is None:
            return

        cibles = [face for face in FacesAvecUnCompteurExplosif(effect)
                  if Scheme2.IsType(face)]
        if not cibles:
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Make a basic thwart against a scheme with an explosive counter on it, without exhausting",
                lambda targets:
                    heros.BasicThwart(list(targets), effect),
            ).SetTarget(Scheme2, has_counter=COMPTEUR_EXPLOSIF, range=(1, 1)),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            swift_strikes,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
