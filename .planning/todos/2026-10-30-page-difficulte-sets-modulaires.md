# Plan : page « Difficulté et sets modulaires » (préparation de partie)

Statut : **réalisé le 30/10/2026** (voir « Réalisation » en fin de fichier). Maquette vue et validée (affichage « Normal »,
capture du 30/10/2026 : `.planning/…/apercu-page-difficulte-normal.png`, à ranger si besoin).

## Ce qui est décidé

- **Nouvelle étape** après « Méchant » : Équipe, Decks, Méchant, **Difficulté**, Final (5 étapes).
- **Colonne gauche** : sets de la partie (obligatoires, recommandés, ajoutés par le joueur), chacun avec sa
  boîte d'origine ; difficulté estimée ; bouton « Sets proposés par VillainTheory ».
- **Colonne droite** : niveau (Standard I/II/III, Expert, Skirmish, Héroïque) et liste permanente de **tous les
  sets modulaires**, groupés par boîte, repliables, avec recherche et cases à cocher.
- **Bandeau du bas** : propositions VillainTheory du méchant choisi (nom, difficulté, sets, boîte, pourquoi).
  Une proposition dont un set manque dans le jeu est **grisée avec la raison**.
- Choisir Standard I/II/III change tout seul le set obligatoire (comportement déjà existant, `niveau-standard.js`).
- Liste limitée aux sets **modulaires** (pas de nemesis, ni Standard/Expert/scénario).
- Noms **français** : déduits des cartes FR du jeu ; anglais quand rien n'est trouvé.
- Source des propositions : `Every_Villains_Best_Modular_Sets_by_VillainTheory` (≈600 combinaisons).

## ⚠ À savoir avant de commencer

1. `app.js` (STEPS, l. ~209) dit que niveau et sets se choisissent « sur l'écran de la cible, en voyant le méchant ».
   Cette décision est **inversée** ici. Le bloc « Menace / Sets modulaires » de l'écran Méchant disparaît (ou se
   réduit à un résumé + lien vers la page). À confirmer avec le joueur au moment de coder.
2. Le catalogue (`catalog.js`) ne connaît **pas la boîte d'un set de rencontre**. Il faut une table set → boîte.
3. Le jeu n'a **aucune table de noms FR des sets** (seulement des cartes : `noms-fr.js`).
4. Le document VillainTheory est en anglais et nomme les sets en anglais ; il faut un **rapprochement** avec
   les identifiants de sets du moteur (`bomb_scare`, `hydra_patrol`…).
5. Le moteur sait déjà lancer une partie avec `selectedModularSets` et `modularConfig` (`launcher.js`) : la
   page n'a pas à toucher au moteur Python.
6. Campagne : l'écran de campagne impose ses propres sets ; la page ne doit pas s'y afficher
   (`creationCampagne()` garde déjà « Équipe, Decks » seulement).

## Étapes

### 1. Données (aucune interface)
- 1a. Extraire le tableau du `.mht` en JSON propre : méchant, nom de combinaison, sets, difficulté (+4…−2),
  note, pack, coche « ✔ recommandé ».
- 1b. Table **set → boîte** (nom de la boîte en français) pour tous les sets modulaires du jeu. Source :
  noms des packs dans les données existantes ; compléter à la main ce qui manque.
- 1c. Table **set → nom français** déduite des textes FR des cartes de scénario (« Les sets de rencontre … /
  recommandé : … »). Produire un **rapport de couverture** : sets avec nom FR, sets sans (à valider un par un
  avec le joueur, règle « questions : règles d'abord »).
- 1d. Rapprochement VillainTheory ↔ identifiants du moteur ; liste des **combinaisons écartées** (set
  absent du jeu, méchant absent, sets nemesis hors périmètre) avec la raison.
- Livrable : un fichier de données versionné + un test qui échoue si un identifiant de set n'existe pas.

### 2. Page « Difficulté » (PC, affichage Normal)
- 2a. Nouvelle étape dans `STEPS` et dans le fil d'étapes (PC et téléphone) ; Final passe en 5.
- 2b. Colonne gauche : état = `state.difficulty` existant (`standard`, `base`, `heroic`, `skirmish`,
  `modularConfig`, `selectedModularSets`). Pas de nouvel état, pour que `launcher.js` ne change pas.
- 2c. Colonne droite : niveau + liste des sets par boîte, recherche, cases ; bascule automatiquement
  `modularConfig` en « custom » dès qu'on coche/décoche.
- 2d. Bandeau VillainTheory : cartes de combinaisons ; « Utiliser » remplit `selectedModularSets` ;
  grisées avec raison si un set manque.
- 2e. **Difficulté estimée** : la note VillainTheory de la combinaison, décalée par le niveau (Standard II/III,
  Expert) seulement si une règle claire existe ; sinon afficher la note seule, sans inventer de calcul.
- 2f. Retirer/adapter le bloc de l'écran Méchant ; garder « Aléatoire » et « Recommandés » accessibles.

### 3. Autres affichages et appareils
- Coloré et Sobre (mêmes composants, classes du site, pas de couleur en dur) ; téléphone : colonnes empilées,
  bandeau VillainTheory en feuille. Maquette téléphone à valider avant de coder cette partie.
- Noms/FR via `t()` et `dico-en.js` (règle i18n du projet).

### 4. Vérifications
- Tests unitaires purs : table des données (identifiants valides), filtre « grisé », estimation de difficulté.
- Test Playwright (`ui-check`) sur moteur d'essai **hors 2345** : parcours Équipe → … → Difficulté → Final,
  choix d'une combinaison, la partie démarre avec les bons sets (vérifier `encounter_set_names` envoyé à `/new`).
- Captures dans les trois affichages, PC + téléphone, à regarder avant de dire « terminé »
  (mémoire : vérifier dans un navigateur).
- Annonce dans `nouveautes.js` ; fiche `docs/reference/` décrivant les tables et leur mise à jour.

## Ordre conseillé et points d'arrêt

1. Étape 1 entière, puis **point d'arrêt** : rapport de couverture FR + combinaisons écartées au joueur.
2. Étape 2 sur PC en affichage Normal, puis **point d'arrêt** : captures réelles.
3. Étape 3, puis étape 4.

## Décisions du 30/10/2026 (questions tranchées)

- Bloc « Menace / Sets modulaires » de l'écran Méchant : **supprimé**. L'écran Méchant ne sert plus qu'à choisir le scénario.
- Noms des combinaisons VillainTheory : **laissés en anglais** (noms d'auteur).
- Téléphone : **trois onglets en haut** (Sets de la partie / Niveau / Propositions), un seul contenu à l'écran à la fois.
- Import : **seulement les combinaisons jouables** (méchants présents dans le jeu) ; le reste va dans le rapport d'écart, pas dans les données.

Plus aucune question ouverte : on peut démarrer par l'étape 1.

## Réalisation (30/10/2026)

Fait : étapes 1 à 4 du plan. Fiche technique : `docs/reference/PAGE-DIFFICULTE.md`.

- Données : 811 combinaisons lues, **773 gardées** (725 jouables, 48 grisées), 38 écartées (méchants absents,
  sets génériques). Rapport : `docs/rapports/VILLAINTHEORY-IMPORT.md`.
- Noms français : **4 seulement** déduits des cartes FR (Alerte à la Bombe, Gadgets du Bouffon, Maîtres du Mal,
  Civils Attaqués) ; les autres sets restent en anglais. Rapport : `docs/rapports/NOMS-SETS-FR.md`. La déduction
  est limitée par le jeu lui-même : les textes FR de scénario ne citent que les sets recommandés.
- Page PC (affichage Normal, Coloré, Sobre, anglais) et téléphone (trois onglets) ; bloc « Menace / Sets » retiré de
  l'écran Méchant (reste la seconde table du mode Bataille, qu'exige l'étape).
- Plafond de sets relevé à 8 (`nombreMaxDeSets`) : les propositions en prennent jusqu'à 7.
- Tests : `difficulte-logique.test.mjs` (12), `ui-check/tests/page-difficulte.spec.ts` (PC, lancement, téléphone) ;
  specs existantes adaptées : `intense-combatants`, `fanmade-createurs`, `ecran-mechant-boutons`,
  `lancement-partie`, `preparation-telephone`, `assistant-telephone` (4 largeurs, zones de 44 px).

Limites connues : voir `docs/reference/PAGE-DIFFICULTE.md` (pièges 4 et 5). Des specs de préparation échouent déjà
sans cette étape (langue du navigateur de test, fenêtre d'options du héros, `coop-decks-sequentiels` cassé par
`__dirname`) : non touchées.
