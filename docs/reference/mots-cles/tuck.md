# Tuck (glisser sous une carte)

**Texte imprimé / définition** : « tuck it here » / « cards tucked here ».
Terme OFFICIEL récent (zone de cartes posées sous une autre carte, face
cachée ou non). Sur `td012` Donatello's Shell : « You may play, spend, or
discard cards tucked here as if they were in your hand. (Max 1 tucked card.)
Hero Action: Exhaust Donatello's Shell → choose a card in your hand and tuck
it here. »

**Mécanisme moteur** : `CardFace.TuckCardUnderHere(faces, effect)`
(`card_face.py`, enveloppe de `PlaceCardHere`) range la carte dans la zone
`PlaceCardArea` de la carte porteuse (`is_place_card_area`, hors jeu) ;
`GetPlacedCardArea().GetSize()` compte les cartes rangées.
`AbilityFactory.AttachedCardCanPlayLikeInHand(also_discard=, also_spend=)` rend
les cartes rangées utilisables « comme en main ». Trois permissions DISTINCTES,
chacune répondue à sa propre question (`Message.CheckIfFaceIsLikeInHand`, champs
`for_discard` / `for_spend`) :
- **jouer** : `Card.IsLikeInHand` (défaut, toute aptitude déclarée) ;
- **dépenser** (`also_spend=True`) : `Card.IsLikeInHandForSpend`, lue par
  `CheckThisCanDropPay` (`factory/resources.py`) : la carte glissée compte comme une
  carte de la main pour le cloisonnement des paiements ;
- **défausser** (`also_discard=True`) : `Card.IsLikeInHandForDiscard`, lue par
  `Player.GetHandCardsAndTuckedDiscardable`, qui sert aux coûts
  `CostFunc.Discard("YourHandCards")` (cible `YourHandCardsDiscardable`) et à
  `Player.DiscardHandCards` (effets où le joueur choisit).
Sans `also_*`, les cartes glissées sous Echo (`60037a`) gardent leur comportement
d'avant (jouer seulement). Une défausse AU HASARD (`DiscardRandomHandCards`) ne
voit pas la carte glissée : « you MAY discard » est une permission du joueur.

**Carte exemple** : `td012` Donatello's Shell (les trois permissions) ; `60030`
Contingency Planning (jouer seulement) ; `dd008` Doomstadt (plafond à 3).

**Pièges connus** :
- jusqu'au 16/10/2026 « spend » et « discard » n'étaient PAS rendus (seul « play »
  l'était) : le cloisonnement des paiements refusait toute carte hors main/réserve ;
- le plafond « Max N » se met en CONDITION de l'action qui range, pas dans le
  corps ;
- `PlaceCardHere` refuse si la carte porteuse n'est pas sur le terrain ;
- `Puzzle.Gain('<id>')` d'une carte déjà en jeu la RAMÈNE en main (même objet) :
  pour une 2e copie, `Puzzle.CreateHandCards`.

**Casey's Bag (`tc013`, pack `casey_jones`)** : « You may play cards tucked here as if they were
in your hand » = `*AbilityFactory.AttachedCardCanPlayLikeInHand()` SANS `also_spend` ni
`also_discard` (le texte ne dit que « play ») et SANS plafond de cartes rangées (contrairement à
la Carapace). Le Sac range lui-même la plus basse arme de la défausse (`discard_pile.Get()` rend la
défausse du FOND vers le dessus : le premier élément filtré est le bon, modèle `hd013`) et
`tc006` Anything Goes ÉCHANGE une arme en jeu avec une arme rangée : on RANGE d'abord (libère la
place Restricted) puis on met en jeu (`PutIntoPlay`). ⚠ Le Sac est PERMANENT : seul un effet du même
set (`paper.set_name`) peut le faire quitter le jeu (`has_permanent.py`) ; pour le déplacer dans un
cas de test, emprunter l'identité de Casey comme `DebugRule` (`casey_resetup`).

**Variantes maison** : aucune.
