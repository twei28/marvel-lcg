# Vérification carte par carte des cartes hors irefrixs

> **Mise à jour du 20/10/2026 (backlog 12, branche `backlog-12-dazzler`)** :
> pack Dazzler vérifié de dz004 à dz038 (36 cartes) ; `im001b` et `wc014`
> passés en portée « Round ». Gabarits et preuves :
> `.planning/todos/2026-10-20-backlog-12-gabarits-processus-carte.md`.
> Cinq cartes attendent une réponse (dz012, dz016, dz021, dz031, dz035) :
> `.planning/todos/2026-10-20-backlog-12-questions.md`. ⚠ La méthode de la
> fiche (une carte montrée à l'utilisateur, « OK / à corriger ») n'a PAS été
> suivie pour ce lot : vérification faite par un agent, sans dialogue ; les
> points de lecture sont tous dans le fichier de questions. RESTE : les autres
> packs hors irefrixs (fne, web_of_deceit, determination, synthezoid, jj,
> iron_patriot, hercules, luke_cage...).

> **Mise à jour du 07/10/2026 (audit du backlog)** : « dz003 non commité » est PÉRIMÉ : corrigée et commitée (`f7b4e6a0`). RESTE : dz004 à dz038, autoplay Dazzler, puis les cartes hors irefrixs ; même écart « this round » encore en « Phase » dans im001b et wc014.

Ouvert le 06/10/2026. **STATUT : EN PAUSE** (arrêté à la carte 4/40 du pack
Dazzler, à la demande de l'utilisateur, « on verra cela plus tard »).

## Le chantier

L'utilisateur veut relire, une par une, les cartes qui ne viennent pas du dépôt
officiel `irefrixs/marvel-lcg` : lui montrer la carte, ses stats et ce que le
code en fait en langage simple, puis il dit « OK » ou « à corriger ».

- Cartes hors irefrixs : **2410 sur 6409** (comparaison de `data/cards.json`
  avec le clone de référence `C:\tmp\irefrixs-marvel-lcg-check`, commit
  `a77154a`, 3999 cartes). 29 cartes d'irefrixs sont aussi modifiées chez nous.
- Plus gros packs concernés : fne 239, web_of_deceit 176, determination 142,
  synthezoid 88, jj 43, dazzler 40, iron_patriot 40, hercules 39, luke_cage 38.
- Ordre choisi : **un pack à la fois**, en commençant par Dazzler (40 cartes).

## La méthode convenue (à reprendre telle quelle)

1. **Une carte à la fois**, jamais un lot.
2. **L'image du scan envoyée dans la conversation** (`SendUserFile` sur
   `Fusion/marvel-lcg-src/assets/pics/<id>.png`), pas seulement un chemin.
3. Sous l'image : **toutes les stats imprimées** (coût compris, type, classe,
   ressource, PV, ATQ, MNG/REC, DEF, traits, unique), le **texte imprimé**, puis
   **mon interprétation du texte morceau par morceau**, puis **ce que fait le
   code en français simple** et **les cas limites gérés**.
4. Dire ce que le texte ne tranche pas et que le code a tranché.
5. Une question multichoix (`AskUserQuestion`), « OK / interprétation fausse /
   stat fausse / Autre (précise) ».
6. **Si « à corriger » : corriger tout de suite**, avec le processus complet de
   `docs/reference/PROCESSUS-CARTE.md` (preuve par substitution), puis reprendre.
7. Ne présenter que ce que le code fait vraiment : vérifier avant d'écrire une
   phrase (j'ai avancé deux détails non vérifiés sur Longshot, acceptés à tort).

Le lien `G` de `desc.RES` = ressource universelle (wild), `R` physique, `B`
mental, `Y` énergie, `L` éclair.

## Où on en était (pack Dazzler)

| # | Carte | Résultat |
|---|---|---|
| 1 | dz001a Dazzler (héroïne) | OK |
| 2 | dz001b Alison Blaire (alter-ego) | OK |
| 3 | dz002 Longshot | OK |
| 4 | dz003 « A Little Girl's Dream » | **CORRIGÉE** (voir ci-dessous) |
| 5 | dz004 « Beautiful Dreamer » | à faire, prochaine carte |

Restent dz004 à dz038 (35 cartes). Liste complète : filtrer `data/cards.json`,
clé `dazzler`, sur les `card_id` absents du clone irefrixs.

## Ce qui a été corrigé (dz003), NON COMMITÉ

« Reduce the resource cost of the next ally or event you play **this round** »
tombait à la fin de la phase des joueurs (`in_this="Phase"`).
- `src/game/operate/worlds.py` : `UpdateNextCardPlayCost` accepte `in_this="Round"`
  (additif, les 38 autres appels ne bougent pas).
- `src/cards/pack/dazzler/dazzler/dz003.py` : passe en `"Round"`.
- `src/game/puzzle/puzzle.py` : nouveau `Puzzle.EndPlayerPhase()` (ferme la phase
  des joueurs, que `BeginVillainPhase` ne fermait jamais).
- `tools/test_capacites.py` : clé `jouer_apres` et deux cas dz003 (témoin même
  phase, « tout le round »). **Preuve par substitution faite** : vert avec
  `"Round"`, rouge avec `"Phase"` (menace 6 au lieu de 3).
- Vérifiés sans régression : `wc014`, `il001b`, `im001b`, compilation de `src`.
- `docs/reference/RECETTES-MOTEUR.md` : recette ajoutée.

## Reste à faire sur ce chantier

- **Autoplay ciblé non lancé** (étape 8 de PROCESSUS-CARTE : 8 parties Dazzler
  contre Rhino + héros témoin, grep des erreurs). À faire une fois pour tout le
  pack, pas 40 fois.
- **Aucune vraie partie jouée à la main** sur dz003.
- **Même écart ailleurs** : `im001b` (Inventor) et `wc014` (Warping Reality)
  disent « this round » mais restent en `"Phase"`. À traiter carte par carte avec
  le processus complet, par la même option `"Round"`.
- Rien de tout ça n'est déployé ni commité.

## À part : rapport de bug Nick Fury du 05/10/2026

Pas un bug : Nick Fury (01084) est défaussé « à la fin du round », donc après la
phase du méchant, ce que montre le journal du joueur. Réponse envoyée au joueur
sur Discord.
