from . import *

# * Lyla — SOUTIEN, cout 2 [energy]. PERSONA. TECH.
# Action: Exhaust Lyla -> choose an event in your hand (in your hand or
#   discard pile instead if you are in alter-ego form) and swap it with the
#   top card of your deck.
#
# CARTES DE REFERENCE
#  - `ab007` * Donald Pierce, `ma005` : un SOUTIEN dont l'action se paie par
#    `SetCostFunc(CostFunc.Exhaust("This"))`.
#  - `ag001b`, `bt011` : `Faces.MoveAllToDeck([face], deck, "Top", effect)` —
#    la position est un argument POSITIONNEL (RECETTES §2).
#  - `01034`, `ho013` : recuperer une carte depuis la defausse et la remettre
#    en main (`Faces.AddToHand`).
#  - `22005` Evasive Maneuvering : le ciblage construit DANS l'operation par
#    `ChooseAbilities` + `ForChoiceAbility(...).SetTarget(...)`, ce qui permet
#    ici de faire dependre les zones fouillees de la FORME du joueur.
#
# TEXTE CONTRE CODE
#  ⚠ « in your hand OR DISCARD PILE INSTEAD IF YOU ARE IN ALTER-EGO FORM » :
#    la zone depend de la forme, et un `SetTarget(from_where=...)` est FIGE a
#    la construction de l'ability. C'est pourquoi le selecteur est construit
#    dans l'operation, au moment ou la forme est connue. Litteraux verifies
#    dans `selector_where.py:12` : `"YourHandCards"`, `"YourDiscardPile"`.
#  ⚠ « SWAP it with the top card of your deck » : un ECHANGE, deux
#    deplacements. L'evenement choisi monte sur le dessus du deck, et la carte
#    qui s'y trouvait prend LA PLACE DE L'EVENEMENT — donc la main si
#    l'evenement venait de la main, la defausse s'il venait de la defausse.
#    Un « swap » qui ne rendrait pas la carte du dessus serait une pioche
#    deguisee.
#  ⚠ « Action », pas « Hero Action » : la capacite vaut dans LES DEUX formes.
#    C'est d'ailleurs necessaire, puisque la branche « discard pile » ne peut
#    servir qu'en alter-ego.
#  ⚠ Deck vide : il n'y a pas de « top card » a echanger. La condition
#    l'ecarte plutot que de laisser l'action s'offrir pour rien.
#  ⚠⚠ LA CARTE N'EST PAS « RESTRICTED », ET LE PIEGE EST VISUEL. Le mot
#    « RESTRICTED » figure bien sur le scan, en grand — mais DANS
#    L'ILLUSTRATION, sur le dossier affiche a l'ecran derriere Lyla. La boite
#    de texte, elle, ne porte que « PERSONA. TECH. » puis l'Action. Une
#    premiere lecture l'avait pris pour un mot-cle, et `desc.Restricted` sur un
#    SOUTIEN fait tomber la mise en place sur `KeyError: 'Restricted'` (le
#    mot-cle n'existe que sur les AMELIORATIONS : `03009`, `04002`, `06009` sont
#    toutes des Upgrades). Attrape par `verifier_tous_les_decks.py` le
#    08/09/2026 — aucune autre gate ne le voyait. Meme famille que la lecon
#    Lockjaw : ce qui est imprime sur l'image n'est pas ce qui est imprime sur
#    la carte.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def deck_non_vide(effect: 'Effect', message: Any) -> bool:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return False
        deck = getattr(joueur, "player_deck", None)
        return deck is not None and deck.GetSize() > 0

    def echanger(effect: 'Effect', cibles: Sequence['CardFace']) -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        deck = getattr(joueur, "player_deck", None)
        if deck is None:
            return

        choisi = next((c for c in cibles if c is not None), None)
        if choisi is None:
            return

        # La zone d'ou vient l'evenement, LUE AVANT tout deplacement : c'est
        # elle qui recevra la carte du dessus du deck.
        venait_de_la_defausse = choisi.card.area is getattr(joueur, "discard_pile", None)

        dessus = deck.GetTop()
        Faces.MoveAllToDeck([choisi], deck, "Top", effect)

        if dessus is not None and dessus is not choisi:
            if venait_de_la_defausse:
                Faces.DiscardAll([dessus], effect)
            else:
                Faces.AddToHand([dessus], joueur, effect)

    def lyla(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        zones: List[Any] = ["YourHandCards"]
        if joueur.IsAlterEgo():
            zones.append("YourDiscardPile")

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Swap an event with the top card of your deck",
                lambda cibles: echanger(effect, cibles),
            ).SetTarget(Event, from_where=zones),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            lyla,
            conditions=[deck_non_vide],
        ).SetName("Lyla")
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
