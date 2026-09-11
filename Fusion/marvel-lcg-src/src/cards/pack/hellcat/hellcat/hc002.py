from . import *
# * Iron Man (Tony Stark) — ALLIE signature, cout 3, [mental]. AVENGER.
# CTR 2 (1 conseq.) / ATQ 2 (1 conseq.), 3 PV.
# Response: After Iron Man uses a basic power, spend a [mental] resource and
#   choose 1 (limit once per turn): • Ready your identity. • Draw 2 cards.
#
# Modeles : 04032 Captain Marvel (`AfterUnitUseBasicPower(Response, "This")`),
# 45016 Side-by-Side (`ChooseAbilities` + `ForChoiceAbility`), 60020
# (`CostFunc.Spend(Cost("B"))`).
# ⚠ « once per TURN » n'existe pas dans le vocabulaire officiel : rendu « une
#   fois par round » (arbitrage technique du portage, releve du 11/09/2026).

def GetAbilities() -> Sequence['Ability']:

    def iron_man(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        joueur = effect.GetInitiator()
        identite = joueur.GetIdentity()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Ready your identity",
                lambda targets: Faces.ReadyAll(list(targets), effect),
            ).SetTarget([identite], range="All"),
            AbilityFactory.ForChoiceAbility(
                "Draw 2 cards",
                lambda targets: joueur.DrawUp(2, effect),
            ).SetTarget([identite], range="All"),
        )

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            iron_man,
        ).SetCostFunc(CostFunc.Spend(Cost("B")))
        .LimitOncePerRound(),
    ]
