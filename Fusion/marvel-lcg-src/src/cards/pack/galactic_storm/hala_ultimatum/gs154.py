from . import *

# Battle Cry — TRAITRISE (Hala Ultimatum). 1 etoile + 1 icone de boost. 2 exemplaires.
# When Revealed: Give the villain a tough status card. If the villain already has a tough status card,
#   give it a facedown boost card.
# [star] Boost: If the activating enemy has a tough status card, this card gets +2 boost icons for this
#   activation.
#
# Cartes de reference :
#  - « Give the villain a tough status card. If ... already ... » : `DonnerTenaceAuVillainOuSinon`
#    (hala_ultimatum/__init__.py).
#  - « give it a facedown boost card » : `Faces.GiveFacedownBoostCards`, modele
#    `skrull_menace/communs_modulaires.py` (`DonnerBoostAuMechant`).
#  - « this card gets +2 boost icons for this activation » : `HasBoostIcon.GainBoostIcons(2, effect)`
#    (`game/card/face/attribute/has_boost_icon.py`), appele sur `effect.this` au moment ou la carte EST le
#    boost resolu (`WhenCardBecomeBoost`).
#
# ⚠ Mots-pieges : « this card gets +2 boost icons », pas « the activation gains +2 ATK/SCH » : la bonification
# porte sur le DECOMPTE d'icones avant conversion en stat, pas directement sur l'attaque ou la manigance.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)

        def sinon(villain: 'Villain') -> None:
            Faces.GiveFacedownBoostCards([villain], 1, effect)

        DonnerTenaceAuVillainOuSinon(effect, sinon)

    def booster(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        from game.card.face.attribute.has_boost_icon import HasBoostIcon
        if Faces.HasStatus([message.activating_enemy], "Tough") > 0:
            effect.this.CastTo(HasBoostIcon).GainBoostIcons(2, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", booster),
    ]
