from . import *

# Gear Up — EVENEMENT, cout 1, [wild]. x2.
# Reduce the cost to play this card by 1 if you are in alter-ego form.
# Action: Search your deck and discard pile for an ATTACK, ITEM, TACTIC, or
#   WEAPON card and add it to your hand.
#
# CARTES DE REFERENCE
#  - `ReduceCostToPlayThis(1, conditions=[...])` (resources.py:586) : la
#    reduction conditionnelle du cout de CETTE carte.
#  - `an001b` / `ar003` : `Search.PlayerCard(include_player_deck=True,
#    include_discard_pile=True, finder=CardFinder(traits=[...]))` + `GainCard`.
#
# TEXTE CONTRE CODE
#  ⚠ « Action » (ni Hero ni Alter-Ego) -> jouable dans les DEUX formes ; c'est
#    en civil qu'elle coute 0.
#  ⚠ « ATTACK, ITEM, TACTIC, OR WEAPON card » -> `traits=[...]` est un OU ;
#    « card », pas « upgrade » : Go for the Heart (ATTACK) ou Vampire Bite
#    (ATTACK) sont des cibles legitimes, comme le Bandolier (ITEM WEAPON).
#  ⚠ Le moteur, quand RIEN ne correspond, offre TOUTES les cartes
#    (search_internal.py:44-46, observation du 07/09, pack ares) : pas de
#    contre-cas « deck sans cible » possible.


def GetAbilities() -> Sequence['Ability']:

    def en_forme_civile(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        return joueur is not None and not joueur.IsInHeroForm()

    def gear_up(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            finder=CardFinder(traits=["ATTACK", "ITEM", "TACTIC", "WEAPON"]),
        )
        if face:
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.ReduceCostToPlayThis(
            1,
            conditions=[en_forme_civile],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            gear_up,
        ).SetPlay(),
    ]
