from . import *

# * Quasar — face HEROS (identite 1A, pied « HAND SIZE 5 / HIT POINTS 11 »).
# GUARDIAN. CTR 2, ATQ 2, DEF 2, MNG 5, 11 PV.
# Channel the Bands — Action: Exhaust Quasar → ready Quantum Bands.
#
# Cartes de reference :
#  - **`sk002a`** Skrull Origin / `sk013` Excelsior : `WhenInYourPlayTurn(
#    AbilityType.Action, op, conditions=[...]).SetCostFunc(CostFunc.Exhaust(
#    "This"))` — inclinaison en COUT (la fleche), Action « pure ».
#  - `31009` / `an001a` pour `Faces.ReadyAll([...], effect)` (RECETTES §2).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Action** » (pas Hero Action) : imprimee sur la face heros, elle
#    n'existe donc qu'en forme heros ; en alter ego, Wendell Vaughn ne l'a pas.
#  - « Exhaust **Quasar** → » : COUT, l'identite elle-meme ; un Quasar deja
#    incline ne peut pas l'utiliser.
#  - « ready Quantum Bands » : SES Bandes (la carte est unique), en jeu.
#    Condition : les Bandes sont en jeu ET inclinees (une capacite ne
#    s'initie pas si son effet ne peut rien changer, Rules Reference).
#  - Pas de limite imprimee : l'inclinaison de Quasar en tient lieu.


def GetAbilities() -> Sequence['Ability']:

    def canaliser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)
        RedresserLesBandes(effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            canaliser,
            conditions=[lambda effect, message: BandesInclinees(effect)],
        ).SetName("Channel the Bands").SetCostFunc(CostFunc.Exhaust("This")),
    ]
