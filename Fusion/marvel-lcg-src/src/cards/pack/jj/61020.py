from . import *

# * Run Them to Ground
#
# « Skip the next villain phase » n'a AUCUN precedent dans le moteur : la boucle
# de round (world.py `game_round`) appelle `VillainPhase` sans condition, et il
# n'existe ni drapeau ni message annulable au niveau de la phase entiere. On la
# neutralise donc etape par etape, sur la seule phase vilain qui suit :
#   etape 1 : la manigance principale ne recoit pas sa menace de phase ;
#   etape 2 : aucun ennemi ne s'active ;
#   etape 3 : aucune carte rencontre n'est distribuee (etape 4 n'a donc rien a
#             reveler).
# Ces trois effets meurent a la fin du round, c'est-a-dire juste apres la phase
# vilain sautee.
#
# « until the start of the next (unskipped) villain phase » deborde du round :
# l'immunite du vilain doit survivre a la phase sautee ET a la phase heros
# suivante. Elle est donc posee sans limite de duree et retiree a la main au
# debut de la SECONDE phase vilain vue, la premiere etant celle qu'on saute.

def GetAbilities() -> Sequence['Ability']:

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)

        # • Deal each player 1 facedown encounter card (immediately).
        # Distribue AVANT de poser le blocage de l'etape 3, sans quoi la carte
        # se bloquerait elle-meme.
        for player in Worlds.GetPlayers(effect):
            player.DealEncounterCards(1, effect)

        # • Skip the next villain phase.
        def no_phase_threat(inner_effect: 'Effect', threat_message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
            threat_message.SetBeInstead(effect)

        def check_is_phase_threat(inner_effect: 'Effect', threat_message: 'Message.WhenSchemeWouldPlaceThreat') -> bool:
            from game.effect.rule import MainSchemePhasePlaceThreat
            by_effect = threat_message.by_effect
            return by_effect is not None and isinstance(by_effect, MainSchemePhasePlaceThreat)

        def no_deal(inner_effect: 'Effect', deal_message: 'Message.WhenPlayerWouldBeDealtEncounterCard') -> None:
            deal_message.SetBeInstead(effect)

        def is_villain_phase(inner_effect: 'Effect', deal_message: 'Message.WhenPlayerWouldBeDealtEncounterCard') -> bool:
            return inner_effect.world.phase.IsVillainPhase()

        this.effect.RegisterTemp(
            AbilityFactory.WhenSchemeWouldPlaceThreat(
                AbilityType.Temp0,
                MainScheme,
                no_phase_threat,
                conditions=[check_is_phase_threat],
            ),
            AbilityFactory.EnemyCannotActivate(
                AbilityType.Temp0,
                Enemy,
            ),
            Ability(
                AbilityType.Temp0,
                Message.WhenPlayerWouldBeDealtEncounterCard,
                [is_villain_phase],
                no_deal,
            ),
            unregister_after_exec=False,
            until_round_end=True,
        )

        # • The villain cannot take damage until the start of the next
        #   (unskipped) villain phase.
        villain = Worlds.FindVillain(effect)
        if not villain:
            return

        def cannot_take_damage(inner_effect: 'Effect', damage_message: 'Message.WhenUnitWouldTakeDamage') -> None:
            damage_message.PreventDamage("All", effect)

        immunite = villain.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.Temp0, "This", cannot_take_damage),
            unregister_after_exec=False,
        )

        # La phase vilain sautee est la premiere vue ; l'immunite tombe au debut
        # de la suivante.
        phases_vues = [0]

        def leve_immunite(inner_effect: 'Effect', phase_message: 'Message.WhenPhaseBegin') -> None:
            from game.operate.effects import Effects
            phases_vues[0] += 1
            if phases_vues[0] < 2:
                return
            Effects.UnRegister(immunite)
            Effects.UnRegister(compteur)

        compteur = this.effect.RegisterTemp(
            AbilityFactory.WhenVillainPhaseBegin(AbilityType.Temp0, leve_immunite),
            unregister_after_exec=False,
        )

    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated)]
