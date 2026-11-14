# Damnation (zone hors jeu maison, scénario Mephisto, Neptune)

**Texte imprimé / définition** (encart de règles) : zone hors jeu partagée par tous les joueurs, propre au scénario. Les cartes y sont face cachée et suivent les règles des cartes hors jeu ; seules des cartes de la rencontre peuvent les regarder. Chaque joueur a sa propre pile (cartes issues de SA collection). L'environnement Gateway to Corruption (puis Hell au stade 3) exige **10 cartes par joueur en Damnation pour que les joueurs perdent**, et redirige vers Damnation toute carte « mise de côté » depuis le deck d'un joueur. Seules des cartes de la rencontre en retirent (« look at N cards in Damnation and shuffle each back into its owner's deck »). Sous Hell, un jeton d'accélération est posé en fin de round.

**Mécanisme moteur** : zone `player.damnation` (`DeckType.DamnationArea = 25`, `game/deck/deck_type.py`, `player.py`), créée pour tous les joueurs comme la Réserve et la Rising Tide, publiée dans le descripteur (`damnation` par joueur, `to_descriptor.py`), connue du harnais (`puzzle.py`, `puzzle_capture.py`). Drapeaux : hors jeu, face cachée, ni `is_set_aside` (les recherches « set aside » ne la voient pas) ni `is_like_in_hand`. Décision utilisateur du 09/11/2026 : une pile par joueur + compteur visible de tous.
À faire : l'interruption forcée qui y redirige les cartes mises de côté (`WhenCardWouldMoveToArea`, voir `PLAN-DAMNATION.md`), la défaite à 10 par joueur, la lecture réservée à la rencontre, l'affichage React.

**Carte exemple** : aucune scriptée à ce jour (mp007a Gateway to Corruption et mp007b Hell à écrire).

**Pièges connus** : `Card.SetAside` (`card.py:652`) envoie la carte dans `player.set_aside_deck`, qui est un faux ami (en réalité `additional_discard_pile`). La redirection doit garder sa propre ré-entrée (RecursionError avalée par le moteur) et retourner la carte à la main (`CheckIfCanMove` ne retourne que `ui_group=False`). Précédent le plus proche : Rising Tide (pack wave).

**Variantes maison** : tout le mécanisme est maison.
