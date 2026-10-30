# Index de la documentation

## Je veux créer ou modifier du contenu

- Une carte : `reference/PROCESSUS-CARTE.md`
- Un héros complet : `reference/PROCESSUS-HEROS.md`
- Un scénario : `reference/GUIDE-CREATION-CONTENU.md` §6
- **Une campagne complète à faire produire par une autre IA** (cartes, scénarios, scripts, carnet, textes,
  preuves) : `kit-campagne-ia/` (manuel, liste des fichiers, architecture ; le zip se reconstruit avec
  `python3 outils/construire-kit-campagne.py`)
- **Un héros complet à faire produire par une autre IA** (cartes, deck de départ, scripts, textes, biographie,
  preuves) : `kit-heros-ia/` (manuel, liste des fichiers ; le zip se reconstruit avec
  `python3 outils/construire-kit-heros.py`)
- **Un puzzle** (créer, publier, résoudre) : `puzzle/GUIDE-CREATEUR.md` ; comment ça marche, où est quoi, les pièges et les
  tests : `puzzle/GUIDE-TECHNIQUE.md` ; le plan et l'avancement : `puzzle/PLAN.md`
- Comprendre un mot-clé (officiel ou maison) : `reference/mots-cles/`
- Comprendre ou modifier « Annuler » (instantané du tour, pourquoi pas `deepcopy`, les pièges) :
  `reference/ANNULER-INSTANTANE.md`
- Où vit chaque type de fichier, les deux copies du moteur, le format de
  `cards.json`, l'API de scripting : `reference/GUIDE-CREATION-CONTENU.md`

## Je veux jouer ou faire tourner le jeu

- Lancer une partie en ligne à plusieurs : `reference/MULTIJOUEUR.md`
- Jouer depuis un salon vocal Discord : `reference/DISCORD.md`
- Administrer le serveur, lire les rapports de bug reçus, ajouter un livret
  de règles au panneau « Documents » : `../deploiement/MODE-EMPLOI.md`
- Jouer en mode manuel comme sur OCTGN (guide des gestes, état actuel,
  ce qui manque) : `superpowers/specs/2026-10-06-mode-manuel-comme-octgn-design.md` §A,
  plan dans `superpowers/plans/2026-10-06-mode-manuel-comme-octgn.md`
- Le cadre de décision tour par tour (aussi la spec du bot autoplay) :
  `reference/GUIDE-STRATEGIE-JEU.md`

## Je veux voir ce qui reste à faire

- `BACKLOG.md` : les chantiers décidés ou envisagés, pas encore faits (par exemple le jeu installable sans
  télécharger toutes les cartes)

## Je veux comprendre l'historique du projet

- `rapports/RANGEMENT.md` : pourquoi le dossier est organisé ainsi
- `rapports/RAPPORT-AUDIT-CARTES.md`, `rapports/RAPPORT-SCANS-FR.md` :
  audits ponctuels, figés à leur date
- `rapports/BRIEF-REFONTE-PLATEAU.md` : passation de la refonte du plateau
- `rapports/CAMPAGNES.md` : état des lieux du mode campagne, figé au
  07/08/2026 (comprendre comment ça marchait à cette date, pas une
  référence tenue à jour)

## Packs custom avec leur propre dossier de conception

- `packs/squirrel_girl/`
