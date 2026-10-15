from . import *

# Enemy Adaptation — ATTACHEMENT (Skrull Elite - Crusader). CONDITION. +1 MNG, +1 ATQ, 2 icones de boost.
# Attach to a SKRULL minion. If you cannot, attach to the villain.
# You cannot defend against attached enemy's attacks.
# Hero Action: Give the villain 1 facedown boost card → discard Enemy Adaptation.
#
# Cartes de reference :
#  - Attache : helper `AttacherAUnSbireSkrull` (modele 01100 / sk146 : `AttachToFaceWhenPutIntoPlay` +
#    `otherwise_attach_to`).
#  - « You cannot defend against X's attacks » : **`ip034`** Molecule Man / **`27152`**
#    (`UnitCannotDefend(Unit2, <attaquant>, cannot_trigger_defense_ability=True)`) avec l'attaquant
#    `"AttachedEnemy"`.
#  - « Hero Action: <effet> → discard this card » : **`sk146`** Captain Paibok (`PlayerActionToDiscardThis` +
#    `SetCostFunc(CostFunc.Custom(None, cout))`) ; le COUT est ici de donner la carte de boost.
#  - +1 MNG / +1 ATQ : natifs (`SCH+` / `ATK+` du desc, comme sk148 / sk150).
#
# ⚠ Mots-pieges : « SKRULL minion » (pas le mechant d'abord, meme SKRULL) puis « the villain » ; « You
# cannot defend AGAINST ATTACHED ENEMY'S attacks » : seules les attaques de l'ennemi porteur, aucun
# personnage (identite ou allie) ne peut defendre ; le « → » separe COUT (la carte de boost) et EFFET
# (la defausse).


def GetAbilities() -> Sequence['Ability']:

    def cout(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        return DonnerBoostAuMechant(effect, 1) > 0

    return [
        AttacherAUnSbireSkrull(),
        *AbilityFactory.UnitCannotDefend(Unit2, "AttachedEnemy", cannot_trigger_defense_ability=True),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCostFunc(CostFunc.Custom(None, cout)),
    ]
