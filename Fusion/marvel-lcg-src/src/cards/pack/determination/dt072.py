from . import *

# * Red Dagger

def GetAbilities() -> Sequence['Ability']:

    def poser_un_jeton(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Faces.PlaceTokensOn([this], 1, 'acceleration_token', effect)

    def red_dagger(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)

        # « resoudre cette attaque X fois » : le moteur ne rejoue pas une
        # attaque en cours. APPROXIMATION ECRITE — l'attaque est resolue une
        # fois, avec l'ATK multipliee par X. Le total de degats est le meme ;
        # ce qui differe est le nombre de fenetres d'attaque ouvertes (retaliate,
        # « apres une attaque », defense) et les degats consequents encaisses.
        jetons = sum(f.acceleration_token
                     for f in Worlds.GetAccelerationTokenFaces(effect))
        if jetons > 1:
            this.GainForThisActive(effect, message,
                                   attack=this.attack * (jetons - 1))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            poser_un_jeton
        ).LimitOncePerPhase(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            "This",
            red_dagger
        ),
    ]
