from . import *

# * Donnie (face alter-ego) — GENIUS. TEENAGER. MUTANT. TURTLE. PV 11, REC 3,
#   main 6.
# Action: Discard 1 card from your hand -> search your deck and discard pile
#   for Donatello's Bo or Donatello's Shell and put it into play, exhausted.
#   (Shuffle.)
#
# CARTES DE REFERENCE
#  - `vp001b` Wade Wilson / `04001b` Clint Barton : `Search.PlayerCard(
#    include_player_deck=True, include_discard_pile=True, ...)` — fouille du
#    deck ET de la defausse, melange par defaut.
#  - `br005` Stellar Leap : `finder=CardFinder(...)` passe tel quel a la
#    recherche ; `62001b` pour l'`AlterEgo` + `Action`.
#  - `face_on_event.py:170` `PutIntoPlay(player, effect, exhaust=True)` :
#    « put it into play, exhausted » (modeles cites dans le moteur : 38028,
#    40171). Une AMELIORATION mise en jeu s'attache d'elle-meme (upgrade.py,
#    `AttachToFaceWhenPutIntoPlayInternal`).
#  - `sf010` / `captain_america 03001a` : `CostFunc.Discard("YourHandCards")`.
#
# TEXTE CONTRE CODE
#  « Donatello's Bo OR Donatello's Shell » -> UNE seule carte (insert : « it
#    only grabs 1 at a time »), au choix du joueur parmi les deux ids.
#  « EXHAUSTED » -> `exhaust=True` (insert : « they enter play exhausted »).
#  « Discard 1 card from your hand » est DEVANT la fleche : c'est un COUT.
#  Le « Bo » imprime sur cette face est sans macron, alors que le titre de
#  td011 est « Donatello's Bō » : on cherche par `card_ids`, pas par nom.


def GetAbilities() -> Sequence['Ability']:

    def atelier(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            finder=CardFinder(card_ids=[ID_BO, ID_CARAPACE], card_type=Upgrade),
        )
        if face is not None:
            face.PutIntoPlay(joueur, effect, exhaust=True)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            atelier,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
