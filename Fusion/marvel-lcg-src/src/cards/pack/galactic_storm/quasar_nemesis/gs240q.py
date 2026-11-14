from . import *

# Distant Manipulation — TRAITRISE NEMESIS de Quasar (QUASAR NEMESIS 4/5 et 5/5,
# x2, numero imprime 240, en collision avec Energy Transfer de Binary :
# suffixe q). 1 icone de boost.
# When Revealed: Choose to either exhaust each card with a "Resource" ability
#   you control or discard each resource card from your hand. If you cannot,
#   this card gains surge.
#
# Cartes de reference :
#  - **`hs052`** Restraining Pincers : « Choose to either A or B. If you
#    cannot, this card gains surge » = options construites seulement si
#    elles sont realisables, `joueur.ChooseAbilities(effect, *options)` faux
#    -> `ThisCardGainSurge(effect)`.
#  - `bt004` pour `Faces.ExhaustAll(...)` ; `Faces.DiscardAll(...)` pour la
#    main.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « each card with a "Resource" ABILITY you CONTROL » : les cartes EN JEU
#    du joueur (identite comprise) qui portent une capacite de type Resource ;
#    « Hero Resource » / « Alter-Ego Resource » sont des capacites Resource
#    restreintes a une forme (AbilityTypeFlags : `HeroResource(Resource)`,
#    ability_type.py) : Quantum Bands en fait partie. Seules les cartes
#    PRETES s'inclinent.
#  - « discard EACH RESOURCE CARD from your hand » : les cartes de TYPE
#    ressource (Energy, Quantum Energy...), pas toute carte portant une icone.
#  - « If you CANNOT » : ni carte prete a capacite Resource, ni carte
#    ressource en main -> Renfort. Une option impossible n'est pas offerte.
#  - « Choose » : le joueur qui revele choisit.


def GetAbilities() -> Sequence['Ability']:

    def a_capacite_ressource(face: 'CardFace') -> bool:
        return any(e.ability.flags.is_resource for e in face.effects)

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return

        a_incliner = [f for f in joueur.GetControlCards()
                      if f is not None and f.IsInPlay() and f.CanExhaust() and a_capacite_ressource(f)]
        a_defausser = [f for f in joueur.hand_cards.Get() if Resource.IsType(f)]

        options = []
        if a_incliner:
            options.append(AbilityFactory.ForChoiceAbility(
                "Exhaust each card with a Resource ability you control",
                lambda cibles: Faces.ExhaustAll(a_incliner, effect),
            ))
        if a_defausser:
            options.append(AbilityFactory.ForChoiceAbility(
                "Discard each resource card from your hand",
                lambda cibles: Faces.DiscardAll(a_defausser, effect),
            ))
        if not options or not joueur.ChooseAbilities(effect, *options):
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
