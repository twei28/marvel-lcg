# Tuck (glisser sous une carte)

**Texte imprimé / définition** : « tuck it here » / « cards tucked here ».
Terme OFFICIEL récent (zone de cartes posées sous une autre carte, face
cachée ou non). Sur `td012` Donatello's Shell : « You may play, spend, or
discard cards tucked here as if they were in your hand. (Max 1 tucked card.)
Hero Action: Exhaust Donatello's Shell → choose a card in your hand and tuck
it here. »

**Mécanisme moteur** : `CardFace.TuckCardUnderHere(faces, effect)`
(`card_face.py:1022`, enveloppe de `PlaceCardHere`) range la carte dans la zone
`PlaceCardArea` de la carte porteuse (`is_place_card_area`, hors jeu) ;
`GetPlacedCardArea().GetSize()` compte les cartes rangées ;
`AbilityFactory.AttachedCardCanPlayLikeInHand(finder)` /
`YouMayPlayCardLikeInHand(..., from_where="ThisPlacedCard")` rend les cartes
rangées jouables comme en main (`Card.IsLikeInHand`).

**Carte exemple** : `60030` Contingency Planning (une amélioration, une seule
carte rangée, jouable comme en main) ; `dd008` Doomstadt (plafond à 3).

**Pièges connus** :
- « play, spend, OR DISCARD as if in your hand » : seul « play » (et, par la
  zone, « spend ») est rendu par le moteur. Les coûts « discard 1 card from
  your hand » ne regardent que `YourHandCards` et ne voient pas la carte
  rangée (question Q-TD-12) ;
- le plafond « Max N » se met en CONDITION de l'action qui range, pas dans le
  corps ;
- `PlaceCardHere` refuse si la carte porteuse n'est pas sur le terrain.

**Variantes maison** : aucune.
