from . import *
# Contingency Plan — AMELIORATION cout 2 [mental]. ITEM. PREPARATION. Hero Action (thwart) : discard Contingency Plan -> remove up to 2 threat from a
# scheme, ignoring any crisis icons in play. Choose a basic power, Batman gets +2 for his next use of the chosen basic power this round.
# Reference : 34034 Psychic Kicker (`WhenUnitUseBasicPower` temporaire + `TemporaryGain`) ; `ignore_crisis=True` de RemoveThreatFromSchemes.
# ⚠ « Basic power » = ATQ, CTR ou DEF (RR p.10 : cinq pouvoirs de base ; REC et SCH n'existent pas sur la face Batman). Verdict du 26/10/2026 :
# la DEF est proposee (avant, elle etait exclue). Son gain passe par `TemporaryGain(defense=...)` sur le message de defense.
def GetAbilities() -> Sequence['Ability']:
    def plan(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        this.RemoveThreatFromSchemes(effect.targets, 2, effect, ignore_crisis=True)
        identite = joueur.GetIdentity()
        def bonus(pouvoir: str) -> None:
            def action(power_effect: 'Effect', power_message: 'Message.WhenUnitUseBasicPower') -> None:
                gain = {"ATK": {"attack": 2}, "THW": {"thwart": 2}, "DEF": {"defense": 2}}[pouvoir]
                identite.TemporaryGain(effect, power_message.would_message, **gain)
            identite.effect.RegisterTemp(
                AbilityFactory.WhenUnitUseBasicPower(AbilityType.Temp0, identite, action, powers=[pouvoir]),
                unregister_after_exec=True, until_round_end=True,
            )
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Batman gets +2 for his next basic attack this round", lambda t: bonus("ATK")).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility("Batman gets +2 for his next basic thwart this round", lambda t: bonus("THW")).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility("Batman gets +2 for his next basic defense this round", lambda t: bonus("DEF")).SetHasNoTargetEffect(),
        )
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, plan).SetLabel('thwart')
        .SetCostFunc(CostFunc.Discard("This")).SetTarget(Scheme2),
    ]
