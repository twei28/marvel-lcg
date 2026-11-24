from . import *


def GetAbilities() -> Sequence['Ability']:
    def depuis_un_web_shooter(effect: 'Effect', message: 'Message.CheckIfAttackMessageHasKeyword') -> bool:
        return EstWebShooter(SourceDeLAttaque(message))

    def redressees_en_fin_de_phase(effect: 'Effect', message: 'Message.AfterCardReady') -> bool:
        # La fin de phase joueur (`EndPhase`) redresse tout d'un coup : une amelioration redressee AILLEURS
        # (Swing and Reload, Neighborhood Watch...) ne compte pas pour Web-Sling.
        return type(message.by_effect).__name__ == "EndPhase" and Upgrade.IsType(message.trigger)

    def web_sling(effect: 'Effect', message: 'Message.AfterCardReady') -> None:
        this = effect.this.CastTo(Hero)
        fin = message.by_effect
        n = getattr(fin, "sq_redressees", 0) + 1
        fin.sq_redressees = n
        if n % 2 == 1:
            return                      # « for each 2 upgrades you readied this way »
        joueur = effect.GetInitiator()
        stat = effect.world.stat
        if joueur is None or stat.GetRoundCounter(joueur, "sq_web_sling") >= 3:
            return                      # « Limit 3 times per round »

        def frapper(cibles: Sequence['CardFace']) -> None:
            stat.AddRoundCounter(joueur, "sq_web_sling")
            this.DealDamage(cibles, 1, effect)

        def retirer(cibles: Sequence['CardFace']) -> None:
            stat.AddRoundCounter(joueur, "sq_web_sling")
            this.RemoveThreatFromSchemes(cibles, 1, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility("Deal 1 damage to an enemy", frapper).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility("Remove 1 threat from a scheme", retirer).SetTarget(Scheme2),
        )

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            ranged=True,
            conditions=[depuis_un_web_shooter],
        ),
        AbilityFactory.AfterCardReady(
            AbilityType.ForcedResponse,
            CardFinder(card_type=Upgrade),
            web_sling,
            conditions=[redressees_en_fin_de_phase],
            by_player="You",
        ).SetName("Web-Sling"),
        RessourceEnhancedCombatSense(CostFunc.Exhaust(Select.From(
            None,
            finder=CardFinder(traits=["WEAPON", "TECH"], card_type=Upgrade),
            from_where=["YouControlCards"],
            range=(1, 1),
        ))),
    ]
