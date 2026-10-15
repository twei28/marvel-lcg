from . import *

# * The Thing (Ben Grimm) — ALLIE FANTASTIC FOUR, AGRESSION. Cout 4, THW 0★, ATK 2★, 3 PV.
# Toughness.
# Action: Discard a tough status card from The Thing and choose up to 2 enemies →
#   deal 2 damage to each of them.
#
# Cartes de reference :
#  - **`38007`** Energy Transfer : `CostFunc.Custom(CardFinder(...), fn)` = un cout
#    PERSONNALISE dont la cible est filtree (ici : The Thing, SEULEMENT s'il porte un
#    statut Tenace, `with_tough=True`, checker.py:198) ; **`th007`** : `DiscardTough(
#    effect, rule=1)`.
#  - **`32045`** Team Strike : `SetTarget(Enemy, range=...)` + degats par `DealDamage`.
#  - **fiche `toughness.md`** : « Toughness » est lu directement dans `desc` (aucun script).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Discard a tough status card FROM THE THING » : cout (devant la fleche), retire sur
#    LUI ; sans statut Tenace l'action n'est pas offerte.
#  - « UP TO 2 enemies » : de 0 a 2 cibles ; « 2 damage to EACH » : 2 chacun, pas 2 au total.
#  - « enemies » : ennemis (vilain et sbires), pas seulement des sbires.
#  - THW 0★ : desc « 0* » (degats consequentiels), ATK 2★ (« 2* »).


def GetAbilities() -> Sequence['Ability']:

    def defausser_tenace(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        return bool(cibles) and cibles[0].DiscardTough(effect, rule=1) > 0

    def clobberin_time(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        if effect.targets:
            this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            clobberin_time,
        ).SetCostFunc(CostFunc.Custom(CardFinder(card_ids=["sk049"], with_tough=True), defausser_tenace))
        .SetTarget(Enemy, range=(0, 2)),
    ]
