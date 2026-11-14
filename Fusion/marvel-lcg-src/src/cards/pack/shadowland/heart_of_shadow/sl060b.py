from . import *

# Dark Invitation (1B) — MANIGANCE PRINCIPALE, stade 1. Menace 6 par joueur, depart 2 par joueur, escalade +1 par joueur.
# Forced Interrupt : When this stage would be completed, instead remove all threat from here and each player chooses:
#   • Place 2 corruption counters on their Creeping Corruption.
#   • Take 3 damage and deal themself 1 facedown encounter card.
# Forced Response : After Krahllak is defeated, advance this scheme to stage 2A.
#
# Cartes de reference : 21099b The Armies of Thanos (`WhenMainSchemeStageWouldBeCompleted` + `SetBeInstead` + `RemoveThreatFromSchemes(.., "All", ..)` + une carte rencontre par joueur),
# punisher_mcdc_2026/commun.py `ComplotEn2A` (« when the villain stage advances, advance the main scheme to 2A » : `Ability(.., Message.AfterVillainAdvanced, ..)` + `Advance("2A")`),
# sl001b (le complot de ce pack). Choix par joueur : `player.ChooseAbilities` + `ForChoiceAbility`.
# ⚠ Mots-pieges : « INSTEAD » : le stade n'est jamais accompli, la menace repart a 0 ; « EACH player chooses » : chaque joueur, dans l'ordre, decide POUR LUI ; « place 2 corruption counters »
#  exige une Creeping Corruption (sinon seule la 2e branche est offerte) ; « take 3 damage AND deal themself 1 facedown encounter card » : LES DEUX, dans cet ordre ; « THEMSELF » : le joueur qui
#  choisit, pas le premier joueur ; « AFTER Krahllak is DEFEATED » : apres que le stade du vilain est tombe (on se branche sur l'avancee du vilain, donc apres sa defaite) ; seulement pendant CE stade
#  de la manigance (la face 2B n'a pas ce texte).


def GetAbilities() -> Sequence['Ability']:

    def accompli(effect: 'Effect', message: 'Message.WhenMainSchemeStageWouldBeCompleted') -> None:
        this = effect.this.CastTo(MainScheme)
        message.SetBeInstead(effect)
        this.RemoveThreatFromSchemes([this], "All", effect)

        def choisit(joueur: 'Player') -> None:
            def corruption(cibles: Sequence['CardFace']) -> None:
                Unused(cibles)
                PlacerCorruption(effect, joueur, 2)

            def degats_et_carte(cibles: Sequence['CardFace']) -> None:
                Unused(cibles)
                joueur.GetIdentity().TakeDamage(this, 3, effect)
                joueur.DealEncounterCards(1, effect)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Place 2 corruption counters on your Creeping Corruption", corruption, condition=PeutPlacerCorruption(joueur)),
                AbilityFactory.ForChoiceAbility("Take 3 damage and deal yourself 1 facedown encounter card", degats_et_carte),
            )

        Players.ForEachPlayer(effect, choisit)

    def vilain_avance(effect: 'Effect', message: 'Message.AfterVillainAdvanced') -> None:
        Unused(message)
        # Seulement si un stade 2 attend encore dans la pile des complots (un complot deja au stade 2 ne bouge plus : le moteur l'exige).
        if effect.world.main_schemes_deck.FindCard(CardFinder(stage=2), card_type=MainScheme) is None:
            return
        effect.this.CastTo(MainScheme).Advance("2A", effect)

    return [
        AbilityFactory.WhenMainSchemeStageWouldBeCompleted(AbilityType.ForcedInterrupt, "This", accompli),
        Ability(AbilityType.ForcedResponse, Message.AfterVillainAdvanced, [], vilain_avance),
    ]
