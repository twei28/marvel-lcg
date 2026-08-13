from . import *

# * Red Dagger

def GetAbilities() -> Sequence['Ability']:

    def poser_un_jeton(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Faces.PlaceTokensOn([this], 1, 'acceleration_token', effect)

    def red_dagger(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)

        # « resoudre cette attaque X fois » : le moteur sait ajouter des cibles
        # a une attaque en cours (25013, Thor, resout la sienne contre chaque
        # sbire engage). En repetant LA MEME cible, l'attaque se resout X fois
        # pour de vrai — avec ses fenetres, sa riposte et ses degats consequents,
        # ce qu'une ATK multipliee n'aurait pas donne.
        jetons = sum(f.acceleration_token
                     for f in Worlds.GetAccelerationTokenFaces(effect))
        cibles = list(message.attacked_targets)
        if jetons > 1 and cibles:
            for _ in range(jetons - 1):
                message.AddTarget(*cibles)

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
