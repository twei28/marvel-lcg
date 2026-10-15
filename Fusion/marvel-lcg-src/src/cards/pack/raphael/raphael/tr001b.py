from . import *

# * Raph (face alter-ego) — MUTANT. TEENAGER. TURTLE. PV 14, REC 4, main 5.
# Action: Discard 1 card from your hand -> search your deck and discard pile
#   for up to 2 [[SAI]] upgrades and put them into play, exhausted. (Shuffle.)
#
# PHASE A : construit, jamais execute.
#
# CARTES DE REFERENCE
#  - `54001b` Bucky Barnes : `Search.PlayerCard(include_player_deck=True,
#    include_discard_pile=True, ...)` puis `face.PutIntoPlay(initiator, effect)`
#    — « search your deck and discard pile ... put it into play ».
#  - `sf010` Shame / `sf001b` : le cout « Discard 1 card from your hand » est
#    `CostFunc.Discard("YourHandCards", range=(1, 1))`.
#  - `PutIntoPlay(..., exhaust=True)` : face_on_event.py:170, deja employe par
#    `ma013`, `ma014`, `50088b` pour « put into play, exhausted ».
#
# TEXTE CONTRE CODE
#  ⚠ « Discard 1 card from your hand -> » : FLECHE, donc la defausse est un
#    COUT (payee avant la recherche), pas la premiere moitie de l'effet.
#  ⚠ « UP TO 2 » -> `range=(0, 2)` sur `SearchForCards` (le pilote du harnais
#    prend le MINIMUM d'un « up to » : il faudra la cle `cibles` / un choix
#    force en phase C). Les deux Sai ont des noms differents : le joueur
#    choisit, il n'y a pas de court-circuit « meme nom, meme zone ».
#  ⚠ « deck AND discard pile » : les deux zones, comme `54001b`.
#  ⚠ « EXHAUSTED » : `exhaust=True` a l'entree en jeu. L'encart de regles le
#    rappelle (« they enter play exhausted »).
#  ⚠ « (Shuffle.) » : le melange est le comportement par defaut de la
#    recherche (RECETTES §2), rien a ajouter.
#  ⚠ « Restricted » (limite de 2 Sai Restricted) : lue par le moteur dans
#    `desc`, voir `tr011`/`tr012`. Les deux Sai entrent donc sans conflit.
#  Pas de nom d'action imprime : aucun `SetName`.


def GetAbilities() -> Sequence['Ability']:

    def chercher_les_sai(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        trouvees = Search.SearchForCards(
            effect, joueur,
            include_player_deck=True,
            include_player_discard_pile=True,
            trait=TRAIT_SAI,
            card_type=Upgrade,
            range=(0, 2),
        )
        for face in list(trouvees or []):
            face.CastTo(Upgrade).PutIntoPlay(joueur, effect, exhaust=True)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            chercher_les_sai,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
