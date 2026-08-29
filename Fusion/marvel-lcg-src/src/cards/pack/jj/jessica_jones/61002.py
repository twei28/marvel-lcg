from . import *
def GetAbilities() -> Sequence['Ability']:
    def alias_investigations(effect: 'Effect', message: 'Message.AfterSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Support)
        this.PlaceCountersInternal(2, 'evidence', effect)
        # « Then, you MAY remove evidence counters ... to defeat the villain's
        # current stage. » Le retrait est optionnel : le joueur doit pouvoir
        # garder ses jetons. L'ancienne version le faisait d'office.
        villain = Worlds.FindVillain(effect)
        if not villain:
            return
        hp = villain.health
        if this.GetCounters('evidence') < hp:
            return
        player = effect.GetInitiator()

        def defaire(_cibles: Sequence['CardFace']):
            removed = this.RemoveCountersInternal(hp, 'evidence', effect, forced=False)
            # Le message expose `removed_counters`, pas `diff`.
            if removed and removed.removed_counters > 0:
                # On defait le vilain tel qu'il est en jeu ; le moteur enchaine
                # lui-meme sur le stade suivant ou sur la victoire.
                Faces.DefeatUnits([villain], this, effect)

        def refuser(_cibles: Sequence['CardFace']):
            pass

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                f"Retirer {hp} jeton(s) evidence pour defaire le stade actuel du vilain", defaire),
            AbilityFactory.ForChoiceAbility('Conserver les jetons', refuser),
        )
    return [
        AbilityFactory.AfterSchemeBeDefeated(
            AbilityType.Response, None, alias_investigations
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
