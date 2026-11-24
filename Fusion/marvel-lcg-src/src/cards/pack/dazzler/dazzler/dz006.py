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
#
# « against YOU » : la fabrique `WhenEnemyWouldActivate` n'a PAS de filtre de
# joueur (son `against_you` est commente dans factory/activate.py). Sans la
# condition `ContreToi`, Doll annulait aussi une activation du vilain contre
# un AUTRE joueur (ecart invisible en solo, corrige le 20/10/2026, backlog 12,
# cas a deux joueurs). Le joueur vise est `message.to_player`.


def GetAbilities() -> Sequence['Ability']:

    def poupee(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.SetBeInstead(effect)

    def contre_ce_joueur(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> bool:
        return message.to_player is not None and \
            message.to_player == effect.GetInitiator()

    def showtime(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        Faces.GiveStatus(effect.targets, "Tough", effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.HeroInterrupt,
            Villain,
            poupee,
            conditions=[contre_ce_joueur],
        ).SetPlay().SetLabel(),
        Showtime(showtime).SetTarget("YourIdentity"),
    ]
