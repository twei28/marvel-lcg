from . import *

# * Gennosuke — ALLIE Leadership (TMNT Reskins, Inkwire), cout 2, [physical]. RHINOCEROS. RONIN.
# THW 2 / ATQ 2 / PV 2 (les « * » du scan sont l'icone ETOILE de rappel, pas des degats consecutifs :
# aucune icone de degat consecutif sous les valeurs, comme `21019` Blade dont il derive).
# Forced Response: After Gennosuke thwarts or attacks, choose to either discard 1 card from your hand,
#   or discard Gennosuke.
#
# MODIFIEE (derivee de `21019` Blade) : le premier choix « spend a [physical] resource from your hand »
# devient « discard 1 card from your hand » ; cout, stats et aspect changent. Script propre.
#
# CARTES DE REFERENCE
#  - `21019` Blade : deux Reponses forcees (`AfterUnitAttackEnd` + `AfterUnitThwartEnd`, "This") et un
#    choix a deux options.
#  - `12025` Care for Cassie : « choose and discard 1 card from your hand » comme OPTION d'un choix =
#    `ForChoiceAbility(...).SetTarget(from_where=["YourHandCards"], canbe_discard=True)`.
#
# TEXTE CONTRE CODE
#  ⚠ « thwarts OR attacks » : les deux declencheurs.
#  ⚠ « choose to EITHER ... OR ... » : un seul des deux ; main vide -> seule l'option « discard
#    Gennosuke » reste possible (l'autre n'a pas de cible).
#  ⚠ « discard 1 card from YOUR hand » : n'importe quelle carte, choisie par le joueur.
#  ⚠ Forced : pas facultative.


def GetAbilities() -> Sequence['Ability']:

    def gennosuke(effect: 'Effect', message: 'Message.AfterUnitAttackEnd|Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        joueur = effect.GetInitiator()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard 1 card from your hand",
                lambda cibles: Faces.DiscardAll(cibles, effect),
            ).SetTarget(from_where=["YourHandCards"], canbe_discard=True),
            AbilityFactory.ForChoiceAbility(
                "Discard Gennosuke",
                lambda cibles: Faces.DiscardAll(cibles, effect),
            ).SetTarget([this], canbe_discard=True),
        )

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            "This",
            gennosuke,
        ),
        AbilityFactory.AfterUnitThwartEnd(
            AbilityType.ForcedResponse,
            "This",
            gennosuke,
        ),
    ]
