from . import *

# * She-Hulk (variante Why Not, Merlin)
# "Do You Even Lift?" — Response: After you change to this form, deal 2 damage
# to an enemy. Deal 1 damage to an enemy for each [acceleration] icon in play.
#
# Modele 01019a (meme declencheur, memes 2 degats fixes). L'icone est
# l'ACCELERATION (decision de l'utilisateur du 25/10/2026, d'apres la note
# « Did you look at my obligation? » : Legal Work 01160 pose un pion
# Acceleration). On compte les icones imprimees en jeu (`Worlds.GetIconsNum`,
# modele 44017 Barely a Scratch) ET les pions Acceleration poses sur les
# cartes en jeu (modele bw020).
#
# ⚠ DEUX capacites distinctes (decision de l'utilisateur du 27/10/2026,
# relecture du scan wn001a.jpg : l'autocollant REMPLACE « 2 damage to an
# enemy » par « 1 damage to an enemy for each icon in play » dans le texte
# imprime, mais l'utilisateur veut les DEUX effets, avec deux cibles choisies
# INDEPENDAMMENT, pas un seul total sur une cible unique) : les 2 degats fixes
# partent TOUJOURS ; le bonus par icone ne propose la capacite que s'il y a au
# moins une icone (rien a infliger sinon).


def icones_acceleration(effect: 'Effect') -> int:
    jetons = sum(face.acceleration_token for face in Worlds.GetAccelerationTokenFaces(effect))
    return Worlds.GetIconsNum(effect, ["Acceleration"]) + jetons


def GetAbilities() -> Sequence['Ability']:

    def deux_degats_fixes(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        Unused(message)
        this = effect.this.CastTo(Hero)
        this.DealDamage(effect.targets, 2, effect)

    def degats_par_icone(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        Unused(message)
        this = effect.this.CastTo(Hero)
        this.DealDamage(effect.targets, icones_acceleration(effect), effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            deux_degats_fixes,
            to_this_form=True,
        ).SetName('"Do You Even Lift?"')
        .SetTarget(Enemy),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            degats_par_icone,
            to_this_form=True,
            conditions=[lambda effect, message: icones_acceleration(effect) > 0],
        ).SetName('"Do You Even Lift?"')
        .SetTarget(Enemy),
    ]
