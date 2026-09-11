from . import *

# * Nyx (sbire, 6 PV, MNG 2, ATQ 1, boost 3, ELITE OLYMPUS)
# Steady. Villainous.
# [star] Forced Interrupt: When Nyx activates against you, discard the top
# card of your deck. If that card has a printed [energy] icon, give Nyx
# 1 additional boost card.
# (Zeus's nemesis minion.)
#
# `Steady` et `Villainous` sont des bases automatiques lues dans `desc`.
# Modeles : 21027 Radioactive Man (activation contre vous ; ici AVANT
# l'activation, donc `WhenEnemyWouldActivate`, dont le message porte
# `GiveBoostCardForThisActivation`, activate.py:6 + sender_enemy.py:94),
# 06030 Trickster (`DiscardDeckTopCards`). « printed [energy] icon » :
# `printed_resource.HasColorPrinted("Y")`, un joker ne compte pas.
#
# ⚠ C'est l'ENERGIE officielle qui est visee, pas l'eclair (relu avec
# l'utilisateur le 11/09/2026).

def GetAbilities() -> Sequence['Ability']:

    def nyx(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        faces = joueur.DiscardDeckTopCards(1, effect)
        for face in faces:
            if ClassCard.IsType(face) and face.printed_resource.HasColorPrinted("Y"):
                message.GiveBoostCardForThisActivation(1, effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.ForcedInterrupt,
            "This",
            nyx,
            conditions=[
                lambda effect, message:
                    message.GetToPlayer() is not None
            ],
        ),
    ]
