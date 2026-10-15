from . import *

# Changeling — amelioration signature (13/16). SKRULL. SUPERPOWER.
# Cout 2 [physical].
# Hulkling gains the [[AERIAL]] trait.
# Interrupt: When you use a basic power, exhaust Changeling → you get +1 to
#   that power for this use.
#
# Cartes de reference :
#  - **`47018`** * Synch : « Interrupt: When you use a basic power, exhaust
#    Synch → you get +1 to that power for this use. » MEME phrase :
#    `WhenUnitUseBasicPower(Interrupt, "You", op).SetCostFunc(Exhaust("This"))`
#    + `message.GainValue(1, effect)`.
#  - `17008` Jet Boots : « X gains the [[aerial]] trait » =
#    `GiveKeywordToAttached(CardFinder(name=...), trait="AERIAL")`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Hulkling** gains » : la face heros seulement (nom propre).
#  - « a basic power » : ATK, THW, DEF ou REC — n'importe lequel, y compris
#    REC en forme civile (Interrupt nu, pas Hero Interrupt).
#  - « exhaust Changeling → » : cout ; une fois incline, plus de bonus ce round.
#  - AERIAL permet de jouer sk029 Glorious Flight (« Play only if you have an
#    AERIAL trait »).


def GetAbilities() -> Sequence['Ability']:

    def changeforme(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.GainValue(1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Hulkling"),
            trait="AERIAL",
        ),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "You",
            changeforme,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
