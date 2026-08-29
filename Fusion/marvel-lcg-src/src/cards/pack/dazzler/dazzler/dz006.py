from . import *

# "Doll"
# SONG.
# Hero Interrupt: When the villain would activate against you, cancel that
#   activation.
# Showtime!: Give your identity a tough status card.
#
# Modele Web Binding (27006) : `SetBeInstead` EST l'annulation d'activation
# dans ce moteur. Ici on filtre sur le VILAIN — le texte ne parle pas des
# sbires, contrairement a Web Binding qui vise n'importe quel ennemi.


def GetAbilities() -> Sequence['Ability']:

    def poupee(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.SetBeInstead(effect)

    def showtime(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        Faces.GiveStatus(effect.targets, "Tough", effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.HeroInterrupt,
            Villain,
            poupee,
        ).SetPlay().SetLabel(),
        Showtime(showtime).SetTarget("YourIdentity"),
    ]
