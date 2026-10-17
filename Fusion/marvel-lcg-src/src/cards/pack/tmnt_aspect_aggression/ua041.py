from . import *

# * Yagi & Gorogoro — ALLIE 2 [mental], ATK 4 (aucun degat consecutif imprime), THW —, PV 2. ASSASSIN. GOAT.
# [star] Yagi & Gorogoro's attacks gain piercing.
# [star] Forced Response: After Yagi & Gorogoro make a basic attack, choose to either discard 2 cards from your
#   hand, or remove Yagi & Gorogoro from the game.
#
# MOT-CLE (fiche lue AVANT le code) : piercing.md.
# CARTES DE REFERENCE
#  - `tm002` * Slash : « X's attacks gain piercing » = `UnitAttackGainKeyword("This", piercing=True)`.
#  - `21019` * Blade : « After Blade thwarts or attacks, choose to either spend ... or discard Blade » =
#    `AfterUnitAttackEnd(ForcedResponse, "This", ...)` + `ChooseAbilities` de deux branches.
#  - `ts007` / `iw015` : « discard 2 cards from your hand » = deux cartes de la main, exactement.
# TEXTE CONTRE CODE
#  ⚠ « make a BASIC attack » (`is_basic_attack=True`) ; THW « — » : pas de contre de base (pas de cle THW).
#  ⚠ « discard 2 cards » : branche offerte seulement avec 2 cartes en main ; sinon il ne reste que le retrait.
#  ⚠ « REMOVE from the game » (pas defausser).


def GetAbilities() -> Sequence['Ability']:

    def yagi(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        effect.GetInitiator().ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard 2 cards from your hand",
                lambda cartes: Faces.DiscardAll(cartes, effect),
            ).SetTarget(from_where=["YourHandCards"], range=(2, 2), canbe_discard=True),
            AbilityFactory.ForChoiceAbility(
                "Remove Yagi & Gorogoro from the game",
                lambda _c: Faces.RemoveAllFromGame([this], effect),
            ),
        )

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            "This",
            yagi,
            is_basic_attack=True,
        ),
    ]
