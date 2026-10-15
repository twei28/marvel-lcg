from . import *

# Skrull Regeneration — evenement signature (10/16). SKRULL. SUPERPOWER.
# Cout 1 [energy].
# Hero Action: Ready Hulkling. Heal 2 damage from Hulkling for each resource
#   you overpaid for this card.
#
# Cartes de reference :
#  - **`yd006`** Twirlin' and Whirlin' / `14006` Speed Cyclone : le surpaiement
#    se lit par `effect.GetCostX()` (= paye - cout, effect.py:519).
#  - `47012` pour `HealthUnits([identite], n, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **for each** resource you **overpaid** » : le cout imprime (1) ne
#    soigne rien ; seules les ressources AU-DELA comptent, 2 PV chacune.
#  - « Ready Hulkling » : sans condition, meme sans surpaiement.
#  - « **Hero** Action » : forme heros seulement.
#  - ⚠ Harnais : `surpayer: True` obligatoire, sinon X = 0 (RECETTES §2).


def GetAbilities() -> Sequence['Ability']:

    def regeneration(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        identite = effect.GetInitiator().GetIdentity()
        Faces.ReadyAll([identite], effect)
        surpaye = max(0, effect.GetCostX())
        if surpaye:
            this.HealthUnits([identite], 2 * surpaye, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            regeneration,
        ).SetPlay(),
    ]
