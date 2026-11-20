# Limit X per [période] / Max X

**Texte imprimé / définition** : « (Limit once per round.) », « (limit once per turn) », « Max 1 per round », « Max 1 per deck ». RR « Limit » :
une capacité marquée « Limit X per [période] » ne peut servir que X fois par période. RR « Max » : « The words "max" and "maximum" impose a maximum
across all copies of a card (by title) for all players. » « Turn » (le tour d'UN joueur) n'est PAS « round » (tous les joueurs).

**Mécanisme moteur** :
- `Ability.LimitOncePerRound()` / `MaxOnePerRound()` (`ability.py`) ; `LimitOncePerPhase()` ; `LimitOncePerRoundPerPlayer()`. Le test porte sur l'OBJET `Ability`
  (`world.stat.IsOncePerRound(ability)`, `condition/once_per.py`), enregistré quand la capacité part. Conséquences MESURÉES (26/10/2026, pack `rm`, `rm007`
  Temporal Reversal « Max 1 per round ») : l'`Ability` d'une carte est PARTAGÉE par toutes ses copies ET par tous les joueurs : « Max 1 per round » vaut donc déjà
  pour toute la table, aucun code à ajouter. Cas `rm007 ... vaut pour TOUS les joueurs` (clé `rm_limite_round`, lecture de `IsOncePerRound`) + son témoin « libre ».
- **Pas de « once per TURN » natif.** `WorldStat.turn_serial` (CORRECTIF du 26/10/2026) change à chaque début ET fin de tour de joueur : noter ce numéro SUR la carte au
  moment où l'effet se résout (`effect.this.<cle> = effect.world.stat.turn_serial`) et le lire dans une `conditions=[...]`. Modèle : `rz003` (`ReponseDonneeParOdinson`).
  Banc de test : `Puzzle.NewPlayerTurn()`.
- **Une limite posée sur une capacité DONNÉE à plusieurs cartes** (`GiveKeywordToInPlayWhenApplyThis(..., given_abilities=[ab])`) : l'objet `ab` est le MÊME pour toutes les cartes qui
  la reçoivent, donc `LimitOncePerRound()` donne UNE limite pour tout le groupe, pas une par carte (cas `rz003`, avant le 26/10/2026).
- **Limite d'un effet CHOISI parmi deux** (rz006) : `LimitOncePerRound()` se consommerait même quand l'AUTRE effet est choisi ; marqueur de round sur la carte, posé à l'effet.
- « Max 1 per deck » : jugé par le constructeur de deck, par TITRE (`validerDeck`, `cleCopie`), jamais par le moteur.

**Carte exemple** : `27032` Double Life (`MaxOnePerRound` sur un événement) ; `rm007` ; `rz003` (once per turn) ; `rz006` (limites séparées).

**Pièges connus** : toute limite imprimée exige un TÉMOIN D'ÉPUISEMENT (PROCESSUS-CARTE étape 7.8), mesuré en CHIFFRE au second déclenchement.
