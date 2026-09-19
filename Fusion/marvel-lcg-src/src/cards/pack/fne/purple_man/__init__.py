from cards.pack import *

# Helpers du set Purple Man (Fear No Evil, 60097-60109).


def TrouverPurpleMan(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindCardOnField(effect, name="Purple Man", card_type=Villain)


def CapacitesDePurpleMan(*, guard: bool, villainous: bool, patrol: bool) -> Sequence['Ability']:
    """Each INFLUENCED minion gains guard (II : and villainous ; III : guard,
    patrol, and villainous) -> GiveKeywordToInPlayWhenApplyThis (liste).
    Each boost card from the Purple Man encounter set gains « [star] Boost :
    After this activation, deal this card to yourself as a facedown encounter
    card » -> une seule capacite sur le vilain, WhenCardBecomeBoost filtre par
    set_name, `message.AfterThisActivation` (07009) puis `DealEncounterCard`
    (27093 Fearmonger). « yourself » = le joueur contre qui l'ennemi s'active.
    """
    mots = {}
    if guard: mots['guard'] = 1
    if villainous: mots['villainous'] = 1
    if patrol: mots['patrol'] = 1

    def du_set(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> bool:
        return message.trigger.paper.set_name == "Purple Man"

    def a_toi(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        carte = message.trigger
        joueur = message.GetToPlayer()

        def donner() -> None:
            if joueur is not None and not carte.IsInPlay():
                joueur.DealEncounterCard(carte, effect)

        message.AfterThisActivation(effect, donner)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="INFLUENCED", card_type=Minion),
            **mots,
        ),
        AbilityFactory.WhenCardBecomeBoost(None, a_toi, conditions=[du_set]),
    ]


def ObligationCommandee(nom: str, action: Callable[['Effect', 'Player', 'Obligation'], None]) -> Sequence['Ability']:
    """« Fight. » / « Protect. » / « Serve. » : Uses (3 command counters) en
    base desc ; Forced Action : Exhaust this card and remove 1 command counter
    from it -> <effet>. Modele ls016 (WhenInYourPlayTurn(ForcedAction) +
    CostFunc.Exhaust("This")), le pion en second cout (CostFunc.Counter)."""
    def executer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        action(effect, effect.GetInitiator(), this)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.ForcedAction, executer)
            .SetName(nom)
            .SetCostFunc(CostFunc.Exhaust("This"))
            .SetCostFunc(CostFunc.Counter("This", 1, 'command')),
    ]
