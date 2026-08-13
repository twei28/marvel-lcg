from . import *

# * Oblivion

def GetAbilities() -> Sequence['Ability']:

    # Une carte de joueur qui va se cacher dans le deck de rencontre : le
    # chemin existe (04084, Ball and Chain, s'y melange aussi), mais Oblivion
    # est un Event, donc ce depart EST sa capacite Play.
    def melanger_dans_le_deck(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Faces.ShuffleAllTo([this], Worlds.GetEncounterDeck(effect), effect)

    def oblivion_revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Event)

        # APPROXIMATION ECRITE. La carte dit « le joueur QUI L'A JOUEE » ;
        # une fois melangee au deck de rencontre elle a quitte sa zone, et le
        # moteur ne garde pas trace du joueur d'origine. C'est donc le joueur a
        # qui elle est revelee qui choisit. En solo les deux coincident ; a
        # plusieurs, l'ecart existe et il est ici, pas cache.
        player = message.GetToPlayer()

        def degats(targets: Sequence['CardFace']) -> None:
            cibles = list(player.GetAllies())
            villain = Worlds.FindVillain(effect)
            if villain:
                cibles.append(villain)
            cibles += [x for x in Worlds.FindCardsOnField(effect, card_type=Minion,
                                                          engaged_with=player)
                       if not x.IsDefeated()]
            if cibles:
                this.DealDamage(cibles, 5, effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard a card from your hand",
                lambda targets: player.DiscardHandCards((1, 1), effect)
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Deal 5 damage to each of your allies, the villain, and each minion engaged with you",
                degats
            ).SetHasNoTargetEffect(),
        )
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            melanger_dans_le_deck
        ).SetPlay(),
        AbilityFactory.WhenThisRevealed(
            None,
            oblivion_revelee
        ),
    ]
