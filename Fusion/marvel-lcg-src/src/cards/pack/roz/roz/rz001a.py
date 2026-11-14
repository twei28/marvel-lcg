from . import *

# * Roz (face HEROS) — PV 9, ATK 1, THW 2, DEF 1, main 5. S.H.I.E.L.D. SPY. WAKANDA.
# Driven — Response: After you use a basic power, resolve the "Special" ability on another [[WAKANDA]]
#   card you control.
# Special: Ready another friendly character (limit once per round).
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - Driven : `51001a` Black Panther (bp) : `AfterUnitUseBasicPower(Response, "This", op)` puis
#    `initiator.ResolveSpecialAbility(effect.targets, effect)`, cible = les cartes qui imprimaient un Special.
#  - Special : `51010` Kimoyo Beads / `22007` : `AbilityFactory.WhenResolveSpecialAbility("This", op)` +
#    `SetTarget(...)`. « ready » : `01024` One-Two Punch (`Faces.ReadyAll(effect.targets, effect)` +
#    `SetTarget(..., canbe_ready=True)`).
#  - limite : `27065` (`LimitOncePerRoundPerPlayer`) ; `LimitOncePerRound` (ability.py:1104).
#
# MOTS-PIEGES
#  - « ANOTHER WAKANDA card you control » : `exclude="This"` (Roz ne se resout pas elle-meme), seules les
#    cartes qui IMPRIMENT un Special sont proposees (`ADesSpecial`) ; les allies Okoye/Aneka/Ayo en portent un.
#  - « After you use a BASIC POWER » : `AfterUnitUseBasicPower` couvre attaque, contre et defense du heros
#    (modele officiel 51001a).
#  - « ANOTHER friendly character » : un heros ou un allie, jamais Roz elle-meme, et il doit pouvoir etre
#    redresse (`canbe_ready`).
#  - « limit once per ROUND » : par carte, `LimitOncePerRound`. Le limite vaut pour CE Special, qu'il soit
#    resolu par Driven ou par une autre carte (Hand-to-Hand, Nimble...).
def GetAbilities() -> Sequence['Ability']:

    def driven(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.ResolveSpecialAbility(effect.targets, effect)

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        Faces.ReadyAll(effect.targets, effect)

    return [
        CarteWakandaSousControle(
            AbilityFactory.AfterUnitUseBasicPower(
                AbilityType.Response,
                "This",
                driven,
            ).SetName("Driven"),
            autre=True,
        ),
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            special,
        ).SetTarget("Hero|Ally", exclude="This", canbe_ready=True)
        .LimitOncePerRound(),
    ]
