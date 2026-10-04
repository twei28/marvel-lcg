from . import *

# A Warrior's Burden — OBLIGATION, RED SONJA NEMESIS.
# Give to the Sonja of Hyrkania player. Choose:
# * Exhaust your identity and discard Hyrkanium Blade -> remove A Warrior's
#   Burden from the game.
# * Search the encounter deck and discard pile for 2 minions and reveal
#   them -> discard this card.
#
# ⚠ Coquille du scan corrigee : « Sonia of Hyrkania » -> « Sonja of
# Hyrkania », nom exact de rs001b (verifie contre `data/cards.json`).
#
# CARTES DE REFERENCE
#  - `si014` Alone (pack superior_iron_man) : montage exact « Give to X »
#    a deux branches, `player.ChooseAbilities(effect,
#    AbilityFactory.ForChoiceAbility(...).SetCostFunc(...), ...)`.
#  - `CostFunc.Discard(name="Hyrkanium Blade", from_where=["YourHandCards"])`
#    pour « discard Hyrkanium Blade » nomme.
#  - `Search.EncounterCards(effect, joueur, include_discard_pile=True,
#    card_type=Minion, total=2)` pour « search the encounter deck and
#    discard pile for 2 minions » -- la recherche montre deja les cartes
#    trouvees a tous les joueurs (« reveal them » est deja couvert par la
#    resolution d'une recherche, aucune action separee a coder).
#
# ⚠⚠ `from_where` EXPLICITE OBLIGATOIRE SUR CostFunc.Discard (23/09/2026, bug
# trouve par le cas de test de cette carte). Sans lui, `from_where=["Default"]`
# (la valeur par defaut de `Select.From`) resout en `get_InPlay`
# (`selector_where.py:197`) : un cout de defausse SANS `from_where` cherche
# la carte nommee EN JEU, jamais en main. Hyrkanium Blade n'a aucune raison
# d'etre en jeu au moment ou cette obligation se resout (elle est en MAIN,
# ramenee par `rs001b` Day of the Sword ou piochee normalement) -- le cout
# etait donc TOUJOURS impayable, la branche 1 systematiquement ecartee sans
# le moindre message d'erreur, et le joueur tombait chaque fois sur la
# branche 2 par defaut.

def GetAbilities() -> Sequence['Ability']:

    def a_warriors_burden(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()

        def rendre_la_lame(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Faces.RemoveAllFromGame([this], effect)

        def chercher_des_sbires(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Search.EncounterCards(
                effect, joueur,
                include_discard_pile=True,
                card_type=Minion,
                total=2,
            )
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust your identity and discard Hyrkanium Blade "
                "-> remove A Warrior's Burden from the game",
                rendre_la_lame,
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
            .SetCostFunc(CostFunc.Discard(name="Hyrkanium Blade", from_where=["YourHandCards"])),
            AbilityFactory.ForChoiceAbility(
                "Search the encounter deck and discard pile for 2 minions "
                "and reveal them -> discard this card",
                chercher_des_sbires,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            a_warriors_burden,
        ),
    ]
