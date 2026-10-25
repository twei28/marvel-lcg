from . import *

# * She-Hulk (variante Why Not, Merlin)
# "Do You Even Lift?" — Response: After you change to this form, deal 1 damage
# to an enemy for each [acceleration] icon in play.
#
# Modele 01019a (meme declencheur). L'icone est l'ACCELERATION (decision de
# l'utilisateur du 25/10/2026, d'apres la note « Did you look at my
# obligation? » : Legal Work 01160 pose un pion Acceleration). On compte les
# icones imprimees en jeu (`Worlds.GetIconsNum`, modele 44017 Barely a Scratch)
# ET les pions Acceleration poses sur les cartes en jeu (modele bw020).
# Aucune icone : pas de capacite proposee (rien a infliger).


def icones_acceleration(effect: 'Effect') -> int:
    jetons = sum(face.acceleration_token for face in Worlds.GetAccelerationTokenFaces(effect))
    return Worlds.GetIconsNum(effect, ["Acceleration"]) + jetons


def GetAbilities() -> Sequence['Ability']:

    def she_hulk(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Hero)
        this.DealDamage(effect.targets, icones_acceleration(effect), effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            she_hulk,
            to_this_form=True,
            conditions=[lambda effect, message: icones_acceleration(effect) > 0],
        ).SetName('"Do You Even Lift?"')
        .SetTarget(Enemy),
    ]
