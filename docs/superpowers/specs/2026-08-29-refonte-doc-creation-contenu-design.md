# Refonte de la documentation de création de contenu — design

Écrit le 29/08/2026, à la suite d'une session de brainstorming. Décisions
validées par l'utilisateur, question par question.

## 1. Constat de départ

Trois symptômes remontés par l'utilisateur, pour un même mal :

1. **Mots-clés non référencés.** Rien ne dit « ce mot-clé se code comme ça,
   voici une carte officielle qui le fait » — l'info existe mais éclatée en
   pavés narratifs par pack (`GUIDE-CREATION-CONTENU.md` §9), jamais indexée
   par mot-clé.
2. **Processus pas suivi de bout en bout.** Des étapes déjà documentées
   (biographie du héros, tests par capacité avec preuve, comparaison avec une
   carte existante, revue texte-contre-code) ont été oubliées ou bâclées sur
   des créations passées, alors qu'elles figurent dans
   `GUIDE-CREATION-CONTENU.md` §4/§5 et `CHECKLIST-VALIDATION-CARTE.md`.
3. **Rien ne force à lire ces fichiers.** Il n'existe aucun `CLAUDE.md` dans
   le projet (racine, ni `Jeu Marvel Champions/`) : la documentation n'est
   consultée que si une session pense elle-même à aller la chercher.

**Défaut annexe découvert pendant l'exploration**, à corriger dans la foulée
puisqu'on réécrit ces sections : les callouts « Où créer tout ça » en tête
des §4, §5 et §6 actuels du guide pointent encore vers
`~/marvel-work/fusion/marvel-lcg-src/` comme copie vivante et renvoient vers
le `rsync` de §1.3 — exactement l'inverse de ce que le correctif du
29/08/2026 en §1.1 vient d'établir (la copie vivante est désormais la copie
Windows, le `rsync` est destructeur et supprimé). Ces trois callouts seront
retirés ou corrigés en même temps que la réécriture.

## 2. Objectif

Remplacer un ensemble de fichiers descriptifs, consultés sur la bonne
volonté de chaque session, par : un point d'entrée qui se charge tout seul
(`CLAUDE.md`), un processus linéaire non sautable par carte/héros avec preuve
à chaque étape, et un catalogue de mots-clés consultable directement.

Non-objectif : ce chantier ne touche pas au contenu de `GUIDE-STRATEGIE-JEU.md`
(spec du bot autoplay), `MULTIJOUEUR.md`, ni aux §6 (nouveau scénario) et §7
(éditeur web) du guide actuel, qui sont déplacés tels quels sans réécriture.

## 3. Arborescence cible

```
Jeu Marvel Champions/
├── CLAUDE.md                              ← nouveau, auto-chargé chaque session
└── docs/
    ├── README.md                          ← nouveau, index
    ├── reference/
    │   ├── GUIDE-CREATION-CONTENU.md      (déplacé, §4/§5 retirés → voir PROCESSUS-*, §9 allégé)
    │   ├── PROCESSUS-CARTE.md             ← nouveau, fusion §4 + CHECKLIST-VALIDATION-CARTE.md
    │   ├── PROCESSUS-HEROS.md             ← nouveau, ex-§5 réécrit
    │   ├── GUIDE-STRATEGIE-JEU.md         (déplacé, inchangé)
    │   ├── MULTIJOUEUR.md                 (déplacé, inchangé)
    │   ├── CAMPAGNES.md                   (déplacé, inchangé — voir §7 ci-dessous)
    │   └── mots-cles/
    │       ├── <slug-officiel>.md         (~20 fiches, ex. toughness.md, guard.md, retaliate.md...)
    │       └── <slug-maison>.md           (ex. drain-x.md, traitor.md, companion.md, squirrel.md, investigate-x.md, et tout ce que révèle l'inventaire d'exécution)
    ├── rapports/
    │   ├── RANGEMENT.md
    │   ├── RAPPORT-AUDIT-CARTES.md
    │   ├── RAPPORT-SCANS-FR.md
    │   └── BRIEF-REFONTE-PLATEAU.md
    └── packs/
        └── squirrel_girl/
            ├── squirrel_girl_cartes.md
            └── squirrel_girl_complete_custom_hero_pack_and_starter_deck.md
```

`CHECKLIST-VALIDATION-CARTE.md` disparaît en tant que fichier séparé : son
contenu (les 4 blocs) est absorbé dans `PROCESSUS-CARTE.md`.

## 4. `CLAUDE.md` du projet

Fichier court. Contenu attendu :

- Une phrase de contexte : projet Marvel Champions LCG, moteur
  `irefrixs/marvel-lcg`, copie vivante = `Fusion/marvel-lcg-src/` (renvoi vers
  `docs/reference/GUIDE-CREATION-CONTENU.md` §1 pour le détail, pas de
  duplication ici).
- Règle impérative : avant toute création ou modification de carte, lire et
  suivre `docs/reference/PROCESSUS-CARTE.md` ; avant tout nouveau héros,
  `docs/reference/PROCESSUS-HEROS.md`. Rien n'est considéré terminé sans le
  gabarit rempli avec preuve.
- Renvoi vers `docs/README.md` pour le reste (« pour X, ouvre Y »).

## 5. `docs/reference/PROCESSUS-CARTE.md`

Fusion de l'actuel §4 du guide et des 4 blocs de
`CHECKLIST-VALIDATION-CARTE.md`, réordonnée dans l'ordre réel d'exécution.
Un seul gabarit à copier par carte, chaque étape avec sa preuve :

1. **Entrée `data/cards.json`** — pack, tri par `card_id`, `type`, `name`,
   `desc`, `traits`, `set_name`, `text`.
2. **Carte(s) de référence** *(nouveau champ obligatoire)* — pour chaque
   capacité de la carte : quelle carte déjà scriptée est comparable, et
   pourquoi. Rempli **avant** d'écrire le script, pas après coup.
3. **Script** `src/cards/pack/<pack>/<set>/<card_id>.py` — pour chaque
   mot-clé imprimé, ouvrir sa fiche dans `mots-cles/` ; absente → la créer
   d'abord (voir §6).
4. **Image** `assets/pics/<card_id>.<ext>`.
5. **Bloc texte-contre-code** (ex-Bloc 1) — mots-pièges, tableau conservé
   tel quel.
6. **Bloc nombres texte↔code** (ex-Bloc 2).
7. **Bloc tests par capacité, preuve par substitution** (ex-Bloc 3).
8. **Bloc autoplay ciblé, grep exhaustif** (ex-Bloc 4).
9. **Carte terminée : OUI / NON** — si NON, ce qui manque et pourquoi,
   explicitement (jamais un « à vérifier en partie réelle » vague — règle
   déjà en vigueur, reprise telle quelle).

La règle du §4.1 actuel (une question à la fois, multichoix, une carte à la
fois, en cas de doute sur un mot-clé/une portée/une icône de ressource) est
reprise intégralement dans ce fichier, elle ne bouge pas de sens.

## 6. `docs/reference/mots-cles/<slug>.md`

Un fichier par mot-clé, officiel et maison. Gabarit :

```markdown
# <Mot-clé>

**Texte imprimé / définition** : ...

**Mécanisme moteur** : clé `desc` directe (laquelle) | `AbilityFactory` à
utiliser | montage maison (décrire le montage, ex. `ThisGainKeyword` +
`GiveKeywordToAttached`).

**Carte exemple** : `<card_id>` — <nom>, extrait du `.py` correspondant.

**Pièges connus** : renvoi vers les lignes concernées du tableau
« mots-pièges » de `PROCESSUS-CARTE.md` §5, si applicable.

**Variantes maison** : autres packs portant un mot-clé identique ou proche,
avec le montage qu'ils ont choisi (évite de réinventer une variante déjà
tranchée ailleurs).
```

Population initiale (à l'exécution, pas figée ici) : les ~20 mots-clés
officiels listés au §2 du guide actuel (`Toughness, Guard, Quickstrike,
Retaliate, Surge, Villainous, Hazard, Crisis, Acceleration, Amplify, Steady,
Stalwart, Peril, Incite, Patrol, Hinder, Vulnerable`, plus `Restricted`,
`TeamUp`, `Alliance` et tout autre mot-clé du vocabulaire officiel trouvé en
scriptant), et tous les mots-clés maison déjà inventés — au minimum ceux
déjà identifiés au §9 actuel (`drain X`, `traitor`, `Companion`, `Squirrel`,
`INVESTIGATE X`) plus l'inventaire complet à faire sur les autres packs
custom listés en mémoire de session (Dazzler, Wolverine X-23, Red Guardian,
Human Torch, Jessica Jones, Luke Cage, Lockjaw, Cloak & Dagger, Madame Web,
Totally Awesome Hulk, Agent Anti-Venom). L'inventaire exhaustif est une
tâche d'exécution, pas un livrable de cette spec.

Le §9 du guide (« Divergences volontaires à préserver ») est allégé en
conséquence : il garde l'historique et le pourquoi par pack, mais renvoie
vers la fiche pour le mécanisme au lieu de le réexpliquer.

## 7. `docs/reference/PROCESSUS-HEROS.md`

Réécriture de l'actuel §5 du guide. Étapes propres au héros (cartes,
scripts, deck de départ, némésis, `sets_info.json`, images), plus :

- **Biographie** (`heros-info.js`, §5.1 actuel repris tel quel pour le
  format) — devient une case à cocher avec preuve (confirmation que la fiche
  s'affiche au survol dans le wizard), pas une ligne de liste qu'on oublie.
- **Texte français** (`textes-fr-fanmade.ts`, §11.1 actuel) — inchangé,
  reste obligatoire.
- **Gate finale** : « héros terminé » exige un `PROCESSUS-CARTE.md` rempli
  et « carte terminée : OUI » pour **chaque** carte du pack, plus une partie
  complète jouée. Pas de héros à moitié validé.

Les mises en garde déjà présentes (§5.2 cartes signature d'un autre héros,
§5.3 identité alternative) sont reprises telles quelles.

## 8. `docs/README.md`

Page courte : ce que sont `reference/`, `rapports/`, `packs/` ; quel fichier
ouvrir pour créer une carte (`PROCESSUS-CARTE.md`), un héros
(`PROCESSUS-HEROS.md`), comprendre un mot-clé (`mots-cles/<slug>.md`), ou
consulter l'historique du projet (`rapports/`).

## 9. Points ouverts pour la relecture

- **`CAMPAGNES.md`** : classé dans `reference/` par défaut (fonctionnalité
  permanente du jeu), alors que son en-tête se présente comme un « document
  de reprise » figé au 07/08/2026. Si c'est en réalité un rapport de
  passation périmé plutôt qu'une référence vivante, il ira dans `rapports/`
  à la place — à trancher à la lecture.
- **Références croisées** : tout fichier qui pointe vers un chemin déplacé
  (`GUIDE-CREATION-CONTENU.md` cité depuis `RANGEMENT.md`, depuis lui-même en
  tant que « ce fichier », etc.) doit être mis à jour au moment du
  déplacement, pas laissé avec un chemin mort.
