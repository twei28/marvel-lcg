from . import *

# * Inspector Ishida — ALLIE 3 [physical], aspect Justice (TMNT Aspects, Inkwire). CAT. DETECTIVE.
# PV 3, THW 2 (1 degat consecutif), ATK 2 (2 degats consecutifs).
# Response: After you play Inspector Ishida from your hand, choose:
#  • Remove 2 threat from a scheme.
#  • Look at the top 3 cards of the encounter deck and put them back in any order.
#
# CARTES DE REFERENCE
#  - `61017` Squirrel Girl : « After you play <allie> FROM YOUR HAND » =
#    `AfterYouPlayThisFromHand(AbilityType.Response, op)` (pas une simple entree en jeu).
#  - `52021` Madame Web : « look at the top N cards of the encounter deck ... put the rest back in any
#    order » = `joueur.LookAtDeck("EncounterDeck", N, effect)` puis `joueur.PlaceOnTopInAnyOrder(...)`.
#  - « choose: • A • B » : `joueur.ChooseAbilities(effect, ForChoiceAbility(A), ForChoiceAbility(B))`
#    (une option exactement ; modele 60023 pour l'option a cible de manigance).
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « After YOU PLAY ... FROM YOUR HAND » : pas une mise en jeu par un effet.
#  ⚠ « choose: » : UNE seule des deux branches.
#  ⚠ « a scheme » : principale ou annexe.
#  ⚠ « the top 3 cards of the ENCOUNTER deck ... put them back in any order » : ni defausse ni pioche,
#    l'ordre est rendu au choix du joueur (deck de moins de 3 cartes : on regarde ce qu'il y a).
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def ishida(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def retirer(cibles: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(list(cibles), 2, effect)

        def regarder(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            faces = joueur.LookAtDeck("EncounterDeck", 3, effect)
            if len(faces) > 1:
                joueur.PlaceOnTopInAnyOrder(list(faces), effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Remove 2 threat from a scheme", retirer).SetTarget(Scheme2),
            AbilityFactory.ForChoiceAbility(
                "Look at the top 3 cards of the encounter deck and put them back in any order", regarder),
        )

    return [
        AbilityFactory.AfterYouPlayThisFromHand(
            AbilityType.Response,
            ishida,
        ),
    ]
