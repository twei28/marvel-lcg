# Puzzles : plan d'implémentation (22/10/2026)

Complète `CAHIER-DES-CHARGES.md`. Aucun code écrit. Une seule livraison, mais
construite dans cet ordre (chaque étape testable seule).

## Ce qui existe déjà (à réutiliser)
- **Moteur** : `src/game/puzzle/` (`PuzzleData`, `RunPuzzle` avec ~80 commandes
  `Puzzle.*` : Damage, Stun, Exhaust, MoveTo, Attach, PutIntoPlay, Win, Lose, End…).
  7 puzzles officiels dans `Fusion/marvel-lcg-src/puzzle/*.json`, avec checksum.
- **Routes serveur** : `/list_puzzle_files`, `/get_puzzle_json`, `/load_puzzle`,
  `/new_puzzle`, `/new_puzzle_replay` (`server_new_game.py`, `server_get.py`).
- **Interface** : `navigateur/dist/js/prepare/puzzles.js` (liste + chargement),
  `puzzle_editor.html` (ancien éditeur texte), et surtout le **bac à sable**
  (`js/sandbox/app.js`) : un panneau avec catalogue de cartes qui pilote la partie en
  cours via `POST /sandbox_command` (commandes `Puzzle.*`, seules autorisées).
- **Replays** : le moteur sait déjà rejouer une partie (`is_puzzle`).

## Constats qui pèsent sur le plan
1. `play_puzzle` ne met en place que `players[0]` (main, deck, défausse) : le
   **multi-héros (1 à 4)** demande d'étendre moteur et format.
2. Il n'existe pas de commande pour : premier joueur, ressources en réserve, phase
   de départ, stade du méchant, objectifs. À ajouter.
3. Il manque l'inverse de tout ça : **capturer l'état du plateau** et le convertir
   en puzzle. C'est la plus grosse pièce.
4. Un puzzle publié exécute des commandes sur la machine d'autres joueurs :
   il faut une **liste blanche stricte** (déjà `Puzzle.<méthode>` seulement).
5. Deux déploiements : serveur (Python) et navigateur (Pyodide, `navigateur/`).
   Toute nouveauté moteur doit passer le contrôle d'équivalence.
6. Le moteur existe en plusieurs copies : lire `GUIDE-CREATION-CONTENU.md` §1 avant
   de toucher quoi que ce soit dans `Fusion/`.

## Étapes

### E0. Cadrage — FAIT (22/10)
- Lire GUIDE §1, étudier `puzzle.py`, `puzzle_data.py`, le bac à sable et ses tests.
- Décider définitivement : étendre `PuzzleData` (version 2, compatible avec les 7
  puzzles existants, checksum conservé ou assoupli).

### E1. Format de puzzle v2 — FAIT (22/10), voir FORMAT-V2.md
Ajouter : titre, description, difficulté, indices, objectifs (ET/OU, cible du
complot), visibilité de la solution, solution de référence (replay), état détaillé
par héros (PV, forme, statuts, premier joueur, ressources), phase de départ,
auteur/pseudo. Migration des anciens fichiers. Validation de taille et de schéma.

### E2. Moteur : mise en place complète
- `play_puzzle` pour 1 à 4 héros.
- Nouvelles commandes `Puzzle.*` : premier joueur, ressources, phase/étape de départ,
  stade et PV du méchant, complot (étape, menace, accélération), mise en jeu avec
  dégâts/compteurs/statuts/attachements.
- Garder la liste blanche ; tests unitaires de chaque commande.

### E3. Moteur : objectifs et fin de puzzle
- Détection automatique : vaincre le méchant ce tour, survivre jusqu'à la fin du
  tour, terminer le complot ciblé, combinaisons ET/OU. Objectif libre : bouton manuel.
- Écran de réussite / d'échec (réutiliser les bannières Victoire/Défaite).
- Mode automatique forcé en puzzle.

### E4. Capture de l'état (cœur de l'éditeur)
- Convertir le plateau courant en `PuzzleData` v2 (zones, ordre des decks, cartes en
  jeu avec états, méchant, complot, rencontre).
- Test d'aller-retour : état → puzzle → rechargement → état identique.

### E5. Création : assistant guidé, puis plateau libre
Principe (décision du 22/10) : **hyper simple et intuitif**. Un assistant à ordre
fixe, une étape par écran, barre de progression, bouton Retour, bouton Passer :
toute étape est facultative et se règle avec des valeurs par défaut raisonnables.
Chaque étape montre un aperçu en direct de la situation.

Étapes (ordre logique, du général au détail) :
1. **Qui joue** : nombre de héros, héros, deck de chacun (decks de départ proposés).
2. **L'ennemi** : méchant, stade, mode expert/standard, sets de rencontre.
3. **L'état de la menace** : PV du méchant, complot principal (étape, menace).
4. **Les mains** : cartes en main de chaque héros (recherche + glisser).
5. **Les decks** : ordre des decks héros et rencontre (liste glissable, mélanger).
6. **Ce qui est en jeu** : alliés, soutiens, améliorations, serviteurs, complots
   annexes, attachements (ajout par recherche, glisser sur le plateau).
7. **Les états** : PV des héros, dégâts, statuts, compteurs, prêt/épuisé, ressources,
   premier joueur, phase de départ. Clic sur une carte = petit panneau à gros boutons.
8. **L'objectif** : cases à cocher (vaincre, survivre, terminer le complot…), texte
   libre, indices.
9. **Présentation et test** : titre, histoire, difficulté ; bouton Tester ; solution
   de référence facultative ; Publier.

Règles de conception :
- Un seul geste par action (clic ou glisser), jamais de menu caché obligatoire.
- Texte clair en français, bulles d'aide, aucun jargon de moteur.
- Contrôle en direct : avertissement doux si deck illégal ou situation incohérente
  (ex. héros à 0 PV), jamais bloquant.
- **« Affiner sur le plateau »** à tout moment : bascule sur le vrai plateau en mode
  édition (catalogue, clic droit, jetons, annuler/refaire Ctrl+Z/Y, bouton
  Tester/Éditer). On peut revenir à l'assistant ; les deux modifient le même état.
- Brouillon sauvegardé automatiquement dans le navigateur à chaque étape.
- Chaque étape = un composant indépendant, testable seul (Playwright).
- Tests d'utilisabilité : faire créer un puzzle à quelqu'un qui n'a pas vu l'outil ;
  le premier puzzle doit prendre moins de 5 minutes.

### E6. Publication (côté client)
- Écran titre/description/difficulté/indices/objectifs/visibilité de la solution.
- Enregistrement optionnel de la solution de référence (replay) ; mention
  « non vérifié » sinon.
- Affichage du code, du lien et de la clé d'édition (une fois, puis dans Mes puzzles).

### E7. Serveur de puzzles
- API : publier, lire par code, modifier/supprimer avec la clé, stockage disque.
- Codes courts uniques (type PZ-A4F9), liens cliquables, limites de taille et de
  débit, validation stricte du contenu (liste blanche des commandes).
- Aucune donnée personnelle : pseudo libre uniquement.
- **Conservation : 28 jours** à partir de la dernière fois où le puzzle a été joué
  (la création compte comme premier jeu). Chaque partie lancée par quelqu'un remet le
  compteur à zéro. Passé 28 jours sans jeu, le puzzle est supprimé automatiquement
  (nettoyage périodique côté serveur). Le créateur peut aussi le supprimer avec sa clé.
- Prévoir l'affichage « expire dans N jours » dans Mes puzzles, et l'avertissement
  au créateur d'un puzzle proche de l'expiration (côté navigateur, à l'ouverture).

### E8. Résolution
- Écran d'intro (titre, histoire, difficulté, objectif) puis plateau.
- Bandeau d'objectif repliable ; indices un par un ; annuler et recommencer
  illimités ; decks cachés mais ordre fixe (même graine à chaque essai).
- Solution de référence : visible ou non selon le choix du créateur.
- Résolution sur mobile/tablette (l'édition reste PC).

### E9. Accueil et « Mes puzzles »
- Le bouton Puzzle ouvre un menu à 3 choix : Résoudre par code, Créer, Mes puzzles.
- Mes puzzles : créés (brouillons + publiés, code, clé), résolus, en cours,
  sauvegardés par code (stockage navigateur).
- Remplacer `puzzles.js` et l'ancien `puzzle_editor.html`. **Les 7 puzzles
  existants sont supprimés** (décision du 22/10) : fichiers `puzzle/*.json`, routes
  et copie dans le paquet navigateur (`construire.py`) à retirer proprement.

### E10. Hors ligne et navigateur
- Création/résolution locales dans la version navigateur (Pyodide) ; publication et
  lecture par code seulement avec le serveur.
- Contrôle d'équivalence moteur serveur / navigateur sur les nouveaux scénarios.

### E11. Robustesse
- Garde de compatibilité : après modification d'une carte, rejouer les solutions de
  référence et marquer les obsolètes.
- Tests UI (Playwright, dossier `ui-check`) : créer, tester, publier, résoudre,
  modifier, supprimer, reprise après rechargement, mobile en résolution.
- Batterie complète en fin de chantier (gros regroupement), filtres ciblés entre
  les étapes.

### E12. Documentation et fin
- `docs/puzzle/` : guide créateur et guide technique ; mise à jour de `docs/README.md`.
- Commit par étape. **Pas de déploiement sans demande** ; avant tout déploiement,
  vérifier les joueurs en ligne. Push GitHub seulement en fin de session.

## Ordre et dépendances
E0 → E1 → E2 → E3 → E4 → E5 → E6 → E7 → E8 → E9 → E10 → E11 → E12.
E7 peut avancer en parallèle de E5/E6 dès que E1 est figé. E4 est le point à plus
haut risque : à attaquer tôt et à valider par l'aller-retour avant l'interface.

## Risques
- Capture d'état exhaustive (cartes avec effets en cours, attachements, jetons
  rares, modes particuliers comme la ville Punisher).
- Déterminisme : le même ordre de decks et la même graine à chaque essai, y
  compris dans le navigateur.
- Scripts de cartes qui changent : puzzles et solutions à revalider.
- Taille de l'assistant et du plateau libre : l'interface est la plus grosse part du travail ; la simplicité demande plusieurs essais de maquette.

## Décisions du 22/10
- Les 7 puzzles existants sont supprimés.
- Création par assistant guidé à ordre fixe, étapes facultatives, plateau libre en option.
- Puzzles publiés conservés 28 jours depuis le dernier jeu ; tout jeu remet le compteur
  à zéro.

## Avancement
- **E0/E1 faits** (22/10) : `puzzle_data.py` v2 (compatible v1), `puzzle_validation.py`,
  `outils/test_puzzle_format.py` (12 fichiers v1 relus, 30+ commandes hostiles refusées).
- Constat : `PuzzleHelper.Exec` laisse passer les commandes sans appel (voir
  FORMAT-V2.md) → corrigé en E3 (v2) et filtré à la publication/lecture en E7.
- Interface : les modales et panneaux d'édition sont **en orange** (consigne du 22/10).
- Prochaine étape : E2 (moteur, mise en place complète, 1 à 4 héros).
