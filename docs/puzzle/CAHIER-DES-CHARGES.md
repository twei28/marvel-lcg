# Puzzles : cahier des charges (21/10/2026)

Issu de 50 questions/réponses. Aucun code écrit à ce stade.
Existant : le moteur a déjà un format de puzzle (`src/game/puzzle/puzzle_data.py` :
héros, main, decks, défausses, `puzzle_command` avec Damage/Stun/Exhaust…).
À examiner avant de coder : je conserve ce qui sert, je remplace le reste.

## 1. Principe
Un joueur crée une mise en situation ; d'autres cherchent comment la
résoudre, pour apprendre ou pour se lancer un défi. Aucun score.
Mise en place classique (héros, deck, méchant,
sets), puis le vrai plateau s'ouvre en **mode édition**.

## 2. Création (PC seulement)
**Priorité : hyper simple et intuitif.** Un assistant guidé à ordre fixe (9 étapes
facultatives : qui joue, ennemi, menace, mains, decks, en jeu, états, objectif,
présentation), puis « Affiner sur le plateau » pour la liberté totale. Les
fonctions ci-dessous sont les réglages offerts dans ces étapes.
- **Joueurs** : 1 à 4 héros ; un seul résolveur les joue tous.
- **Cartes** : toutes (officielles + maison), avertissement visible si deck illégal.
- **Ajout de carte** : catalogue avec recherche/filtres (glisser) ET clic droit sur
  chaque zone (main, decks, défausses, en jeu).
- **Méchant** : stade, PV actuels, statuts, mode expert/standard.
- **Complot principal** : tout (étape, menace, accélération, complots annexes).
- **Rencontre** : serviteurs, complots annexes, attachements, cartes mises de côté,
  avec dégâts, statuts, attachements. Sets choisis à la mise en place + ajouts libres.
- **Chaque héros** : PV, forme (alter-ego/héros), statuts, prêt/épuisé, cartes en jeu
  (alliés, soutiens, améliorations) avec dégâts/compteurs/état, premier joueur,
  ressources en réserve, main, deck, défausse.
- **Ordre des decks** : liste réordonnable (héros et rencontre) + bouton mélanger.
  Révélation en cours : couverte par l'ordre du deck rencontre.
- **Phase de départ** : n'importe quelle phase/étape du tour.
- **Compteurs/PV/statuts** : panneau chiffré (+/−, saisie, cases) ET clic sur jetons.
- **Édition** : annuler/refaire illimité (Ctrl+Z/Y) ; bouton Tester/Éditer (retour
  à l'état de départ intact) ; brouillons enregistrés dans le navigateur.
- **Présentation** : titre, description/histoire, difficulté (1-5 étoiles), indices.
- **Objectifs** (combinables ET/OU) : vaincre le méchant ce tour, survivre jusqu'à la
  fin du tour, terminer le complot, objectif libre en texte. Pas de contraintes
  supplémentaires de résolution.
- **Validation** : recommandée, non obligatoire (mention « non vérifié » sans
  solution de référence enregistrée).
- **Replays visibles avant résolution** : choix du créateur par puzzle.

## 3. Résolution
- Écran d'intro (titre, histoire, difficulté, objectif) puis plateau.
- Bandeau d'objectif discret et repliable.
- Mode **automatique imposé** (règles appliquées par le moteur, pas de triche involontaire).
- Decks cachés mais **ordre fixe**, identique à chaque essai (déterministe).
- Annuler et recommencer illimités.
- Indices gratuits, un par un, sans aucune trace.
- Détection auto de la réussite pour les objectifs standards ; bouton manuel pour
  l'objectif libre.
- Mobile/tablette : résolution oui, création non.
- Un seul résolveur (pas de coopération en ligne).

## 4. Pas de score, pas de classement
Le but est d'apprendre et de se challenger : ni score, ni classement, ni anti-triche.
Le puzzle est simplement « réussi » (détection auto) ou non.
- **Solution de référence** (optionnelle) : le créateur peut enregistrer sa solution
  (replay). Visibilité avant résolution : choix du créateur (voir section 2).
- Pas de commentaires ni de notes.

## 5. Partage et stockage
- Serveur, code court (type PZ-A4F9) ; lien cliquable envisageable (pas de galerie
  publique, pas de tags).
- Pseudo simple sans compte (mémorisé dans le navigateur).
- Clé d'édition secrète à la publication : suppression ou modification
  (modification libre).
- Hors ligne : création et résolution locales ; publication (codes) en ligne.
- Conservation : 28 jours après le dernier jeu ; chaque partie remet le compteur à zéro.
- Les anciens puzzles du moteur sont supprimés.
- Carte modifiée plus tard : puzzle conservé ; la solution de référence est rejouée et signalée obsolète si elle ne passe plus.

## 6. Interface
- Bouton Puzzle de l'accueil : menu à 3 choix (Résoudre par code, Créer un puzzle,
  Mes puzzles).
- Mes puzzles : créés (brouillons + publiés, avec code et clé), résolus, en cours,
  sauvegardés par code.
- Style Épuré (thème sombre) + panneaux d'édition d'une teinte distincte.

## 7. Livraison
Une seule livraison complète (éditeur, résolution, serveur pour les codes, solution de référence).

## 8. Points tranchés à la conception
- **Objectif « terminer le complot »** : le créateur désigne la cible (principal ou
  annexe précis) dans l'éditeur.
- **Format serveur** : on étend `PuzzleData` du moteur (objectifs, indices,
  métadonnées, états détaillés).
- **Clé d'édition** : montrée à la publication et conservée dans le navigateur,
  retrouvable dans « Mes puzzles ».
- **Scoring** : retiré (décision du 21/10). Plus de définition d'« action jouée » nécessaire.
