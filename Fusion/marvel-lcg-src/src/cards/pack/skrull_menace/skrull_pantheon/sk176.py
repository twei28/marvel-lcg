from . import *

# Blessed by Kly'bn (x2, 176) — ATTACHEMENT CONDITION. +X SCH. 1 icone Y + etoile de boost.
# Attach to the minion with the lowest SCH. If you cannot, this card gains surge.
# X is equal to the number of faith counters on the villain.
# ★ Boost: If this activation is a scheme, this card gets +2 boost icons (Y Y) for this activation.
#
# Cartes de reference :
#  - Accrochage a la cible la plus faible, sinon Renfort : **`gmw/galactic_artifacts/16126`**
#    (`AttachToFaceWhenPutIntoPlay(..., lowest_sch=True)`) + `if_cannot_gain_surge=True` (meme option
#    que **`sm/27181`** Snitches Get Stitches pour « if you cannot, this card gains surge »).
#  - Bonus calcule qui suit un compteur : **`brawn/bw016`** Hulk Out (`GiveKeywordToAttached(...,
#    get_new_value=..., ex_change_on_event=OnEvent.Counter(...))`).
#  - Boost conditionnel a l'activation : **`sk113`** Skrull Commander (`WhenCardBecomeBoost("This", op,
#    during_attack=True)`, ici `during_scheme=True`, + `message.GainBoostIcon(2, effect)`).
#
# ⚠ Mots-pieges : « the MINION with the LOWEST SCH » (un sbire, pas le mechant ; les egalites sont tranchees
# par le joueur) ; « If you CANNOT » (aucun sbire en jeu : Renfort) ; « X = faith counters on the VILLAIN »
# (le compteur du mechant, pas de la carte) ; le bonus se recalcule quand le nombre de jetons change ;
# « If this activation is a SCHEME » (rien pendant une attaque) ; « +2 boost icons FOR THIS ACTIVATION ».


def GetAbilities() -> Sequence['Ability']:

    def foi(effect: 'Effect', attache: Any, ui: List['CardFace']) -> int:
        Unused(attache, ui)
        return Foi(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GainBoostIcon(2, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Minion, lowest_sch=True, if_cannot_gain_surge=True),
        *AbilityFactory.GiveKeywordToAttached(
            Minion,
            scheme=1,
            get_new_value=foi,
            ex_change_on_event=OnEvent.Counter(Villain, COMPTEUR_FOI),
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_scheme=True),
    ]
