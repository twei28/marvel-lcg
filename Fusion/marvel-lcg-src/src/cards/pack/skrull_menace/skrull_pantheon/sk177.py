from . import *

# Blessed by Sl'gur't (x2, 177) — ATTACHEMENT CONDITION. +X ATK. 1 icone Y + etoile de boost.
# Attach to the minion with the lowest ATK. If you cannot, this card gains surge.
# X is equal to the number of faith counters on the villain.
# ★ Boost: If this activation is an attack, this card gets +2 boost icons (Y Y) for this activation.
#
# Cartes de reference : voir `sk176` (meme montage, ATK au lieu de SCH) ; accrochage au plus faible ATK :
# `AttachToFaceWhenPutIntoPlay(..., lowest_atk=True)` ; boost : **`sk113`** Skrull Commander
# (`WhenCardBecomeBoost("This", op, during_attack=True)`).
#
# ⚠ Mots-pieges : « the minion with the LOWEST ATK » (ATK courant, pas imprime) ; « If this activation is an
# ATTACK » (rien pendant une manigance) ; X lu sur le MECHANT.


def GetAbilities() -> Sequence['Ability']:

    def foi(effect: 'Effect', attache: Any, ui: List['CardFace']) -> int:
        Unused(attache, ui)
        return Foi(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GainBoostIcon(2, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Minion, lowest_atk=True, if_cannot_gain_surge=True),
        *AbilityFactory.GiveKeywordToAttached(
            Minion,
            attack=1,
            get_new_value=foi,
            ex_change_on_event=OnEvent.Counter(Villain, COMPTEUR_FOI),
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True),
    ]
