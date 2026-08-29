# Refonte de la documentation de création de contenu — Plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remplacer la documentation actuelle de création de cartes/héros
(éclatée, pas suivie de bout en bout, sans point d'entrée automatique) par
un `CLAUDE.md` projet auto-chargé, deux processus linéaires non-sautables
(carte, héros) avec preuve à chaque étape, et un catalogue de mots-clés
(officiels + maison) consultable par fiche.

**Architecture:** Aucune ligne de code moteur ne change. Tout le travail est
sur des fichiers Markdown : réorganisation de `docs/` en trois dossiers
(`reference/`, `rapports/`, `packs/`), fusion de deux fichiers existants en
deux nouveaux processus, création d'un catalogue de fiches mots-clés, un
`CLAUDE.md` et un `docs/README.md`.

**Tech Stack:** Markdown, `git mv` pour préserver l'historique, `grep`/`python3 -c`
sur `data/cards.json` et les scripts `.py` du moteur pour retrouver les
exemples de cartes.

**Spec:** `docs/superpowers/specs/2026-08-29-refonte-doc-creation-contenu-design.md`

## Global Constraints

- Dépôt git : `Jeu Marvel Champions/` (racine du repo). Toutes les commandes
  `git` de ce plan s'exécutent depuis ce dossier.
- Racine des docs actuelle : `Jeu Marvel Champions/docs/`. Racine du moteur
  (copie vivante) : `Jeu Marvel Champions/Fusion/marvel-lcg-src/` — on ne
  modifie **rien** dedans dans ce plan, on ne fait QUE le lire pour retrouver
  des exemples de cartes.
- Toute la doc est en français, sans tiret cadratin (—) utilisé comme
  séparateur de pensée.
- Le dépôt contient déjà des fichiers modifiés sans rapport avec ce chantier
  (moteur, Squirrel Girl, `ui-app`). Chaque commit de ce plan doit lister ses
  fichiers explicitement (jamais `git add -A` ni `git add .`).
- Le fichier `CHECKLIST-VALIDATION-CARTE.md` est supprimé (contenu absorbé
  dans `PROCESSUS-CARTE.md`) : utiliser `git rm`, pas `rm`, pour garder
  l'historique.
- Gabarit de fiche mot-clé (repris tel quel dans toutes les tâches du
  catalogue) :

  ```markdown
  # <Mot-clé>

  **Texte imprimé / définition** : ...

  **Mécanisme moteur** : ...

  **Carte exemple** : `<card_id>` — <nom>, extrait du `.py` correspondant
  (ou « lu directement depuis `desc`, aucun script requis » si le moteur
  le gère nativement).

  **Pièges connus** : ...

  **Variantes maison** : ...
  ```

---

## Phase A — Structure

### Task 1: Réorganiser `docs/` en trois dossiers

**Files:**
- Create: `Jeu Marvel Champions/docs/reference/`, `docs/rapports/`,
  `docs/packs/squirrel_girl/`, `docs/reference/mots-cles/` (dossiers, créés
  implicitement par les `git mv`)
- Modify (déplacer): tous les `.md` actuels de `docs/`

**Interfaces:**
- Consumes: rien (première tâche)
- Produces: l'arborescence que toutes les tâches suivantes utilisent comme
  chemins cibles.

- [ ] **Étape 1 : vérifier l'état du dépôt avant de toucher à quoi que ce soit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git status --short -- docs/
```

Attendu : aucun fichier sous `docs/` en cours de modification (les
modifications non liées listées dans les Global Constraints sont ailleurs,
sous `Fusion/`, `ui-app/`). Si un fichier sous `docs/` apparaît modifié,
s'arrêter et demander confirmation avant de continuer.

- [ ] **Étape 2 : créer l'arborescence et déplacer les fichiers avec `git mv`**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
mkdir -p docs/reference/mots-cles docs/rapports docs/packs/squirrel_girl

git mv docs/GUIDE-CREATION-CONTENU.md docs/reference/GUIDE-CREATION-CONTENU.md
git mv docs/GUIDE-STRATEGIE-JEU.md docs/reference/GUIDE-STRATEGIE-JEU.md
git mv docs/MULTIJOUEUR.md docs/reference/MULTIJOUEUR.md
git mv docs/CAMPAGNES.md docs/reference/CAMPAGNES.md

git mv docs/RANGEMENT.md docs/rapports/RANGEMENT.md
git mv docs/RAPPORT-AUDIT-CARTES.md docs/rapports/RAPPORT-AUDIT-CARTES.md
git mv docs/RAPPORT-SCANS-FR.md docs/rapports/RAPPORT-SCANS-FR.md
git mv docs/BRIEF-REFONTE-PLATEAU.md docs/rapports/BRIEF-REFONTE-PLATEAU.md

git mv docs/squirrel_girl_cartes.md docs/packs/squirrel_girl/squirrel_girl_cartes.md
git mv docs/squirrel_girl_complete_custom_hero_pack_and_starter_deck.md docs/packs/squirrel_girl/squirrel_girl_complete_custom_hero_pack_and_starter_deck.md
```

Note sur `CAMPAGNES.md` : la spec (§9, points ouverts) laisse un doute entre
`reference/` (par défaut, retenu ici) et `rapports/`. Avant de lancer le
`git mv` ci-dessus, lire les 30 premières lignes du fichier
(`head -n 30 docs/CAMPAGNES.md`) : si le contenu se présente comme une
référence vivante du mode campagne (comment ça marche aujourd'hui) plutôt
qu'un compte-rendu figé au 07/08/2026 à usage unique, garder `reference/`
comme fait ci-dessus. Sinon, remplacer la ligne par
`git mv docs/CAMPAGNES.md docs/rapports/CAMPAGNES.md` et le signaler dans le
message de commit.

- [ ] **Étape 3 : vérifier que `git mv` a bien fait des renommages, pas des suppressions + ajouts**

```bash
git status --short -- docs/
```

Attendu : chaque ligne commence par `R ` (rename), pas `D ` suivi de `??`.

- [ ] **Étape 4 : commit**

```bash
git add docs/
git commit -m "docs: réorganiser docs/ en reference/, rapports/, packs/"
```

---

### Task 2: Écrire `Jeu Marvel Champions/CLAUDE.md`

**Files:**
- Create: `Jeu Marvel Champions/CLAUDE.md`

**Interfaces:**
- Consumes: chemins produits par Task 1 (`docs/reference/PROCESSUS-CARTE.md`,
  `docs/reference/PROCESSUS-HEROS.md`, `docs/README.md`) — ces deux premiers
  n'existent pas encore au moment de cette tâche (créés en Task 4/5), donc ce
  fichier référence des chemins qui seront valides après Phase B. C'est
  acceptable : ce n'est pas une tâche testée par exécution de code, seulement
  par lecture. La Task 17 (vérification finale) confirme que tous les liens
  sont valides une fois tout créé.
- Produces: le fichier auto-chargé par toute session Claude Code ouverte dans
  ce dossier.

- [ ] **Étape 1 : écrire le fichier**

```markdown
# Marvel Champions LCG — projet custom

Jeu Marvel Champions LCG basé sur le moteur officiel open-source
`irefrixs/marvel-lcg`. Copie vivante du moteur :
`Fusion/marvel-lcg-src/` (détail des deux copies et du piège associé dans
`docs/reference/GUIDE-CREATION-CONTENU.md` §1 — ne jamais y toucher sans
avoir lu cette section en premier).

## Règle impérative — création ou modification de contenu

- **Nouvelle carte ou modification d'une carte existante** : lire et suivre
  `docs/reference/PROCESSUS-CARTE.md` du début à la fin. Rien n'est
  considéré terminé sans le gabarit rempli, preuve à l'appui, à la dernière
  étape (« Carte terminée : OUI »).
- **Nouveau héros** : lire et suivre `docs/reference/PROCESSUS-HEROS.md`, qui
  exige un `PROCESSUS-CARTE.md` complet pour chaque carte du pack.
- **Mot-clé rencontré pendant l'écriture d'un script** (officiel ou maison) :
  ouvrir sa fiche dans `docs/reference/mots-cles/` avant d'écrire une ligne
  de code. Absente → la créer d'abord, sur le gabarit donné en tête de
  `docs/reference/mots-cles/README.md`.

Pour toute autre question (mode campagne, multijoueur, stratégie, rapports
d'audit passés), voir `docs/README.md`.
```

- [ ] **Étape 2 : vérifier que les trois chemins cités existeront (existent déjà ou seront créés dans ce plan)**

```bash
grep -n "docs/reference" "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/CLAUDE.md"
```

Attendu : 4 chemins listés (`GUIDE-CREATION-CONTENU.md`,
`PROCESSUS-CARTE.md`, `PROCESSUS-HEROS.md`, `mots-cles/`), tous couverts par
une tâche de ce plan (Task 1, 4, 5, 6).

- [ ] **Étape 3 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add CLAUDE.md
git commit -m "docs: ajouter CLAUDE.md projet, point d'entrée auto-chargé"
```

---

### Task 3: Écrire `docs/README.md`

**Files:**
- Create: `Jeu Marvel Champions/docs/README.md`

**Interfaces:**
- Consumes: arborescence de Task 1.
- Produces: page d'index citée depuis `CLAUDE.md` (Task 2).

- [ ] **Étape 1 : écrire le fichier**

```markdown
# Index de la documentation

## Je veux créer ou modifier du contenu

- Une carte : `reference/PROCESSUS-CARTE.md`
- Un héros complet : `reference/PROCESSUS-HEROS.md`
- Un scénario : `reference/GUIDE-CREATION-CONTENU.md` §6
- Comprendre un mot-clé (officiel ou maison) : `reference/mots-cles/`
- Où vit chaque type de fichier, les deux copies du moteur, le format de
  `cards.json`, l'API de scripting : `reference/GUIDE-CREATION-CONTENU.md`

## Je veux jouer ou faire tourner le jeu

- Lancer une partie en ligne à plusieurs : `reference/MULTIJOUEUR.md`
- Comprendre le mode campagne : `reference/CAMPAGNES.md`
- Le cadre de décision tour par tour (aussi la spec du bot autoplay) :
  `reference/GUIDE-STRATEGIE-JEU.md`

## Je veux comprendre l'historique du projet

- `rapports/RANGEMENT.md` : pourquoi le dossier est organisé ainsi
- `rapports/RAPPORT-AUDIT-CARTES.md`, `rapports/RAPPORT-SCANS-FR.md` :
  audits ponctuels, figés à leur date
- `rapports/BRIEF-REFONTE-PLATEAU.md` : passation de la refonte du plateau

## Packs custom avec leur propre dossier de conception

- `packs/squirrel_girl/`
```

- [ ] **Étape 2 : vérifier que chaque chemin cité existe (une fois Phase B/C terminées) via un grep de contrôle**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/docs"
for f in reference/PROCESSUS-CARTE.md reference/PROCESSUS-HEROS.md reference/GUIDE-CREATION-CONTENU.md reference/mots-cles reference/MULTIJOUEUR.md reference/CAMPAGNES.md reference/GUIDE-STRATEGIE-JEU.md rapports/RANGEMENT.md rapports/RAPPORT-AUDIT-CARTES.md rapports/RAPPORT-SCANS-FR.md rapports/BRIEF-REFONTE-PLATEAU.md packs/squirrel_girl; do
  [ -e "$f" ] && echo "OK  $f" || echo "MANQUANT $f (normal si Phase B/C pas encore faite)"
done
```

Cette vérification est répétée en Task 17 une fois tout le plan exécuté ;
ici elle sert juste à confirmer que Task 1 a bien produit les chemins déjà
attendus (`rapports/*`, `reference/GUIDE-*`, `reference/MULTIJOUEUR.md`,
`reference/CAMPAGNES.md`, `packs/squirrel_girl`) — `MANQUANT` est normal pour
`PROCESSUS-CARTE.md`, `PROCESSUS-HEROS.md` et `mots-cles` à ce stade.

- [ ] **Étape 3 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add docs/README.md
git commit -m "docs: ajouter l'index docs/README.md"
```

---

## Phase B — Fusion des processus (dépend de Task 1)

### Task 4: Créer `docs/reference/PROCESSUS-CARTE.md`, supprimer `CHECKLIST-VALIDATION-CARTE.md`

**Files:**
- Create: `Jeu Marvel Champions/docs/reference/PROCESSUS-CARTE.md`
- Modify: `Jeu Marvel Champions/docs/reference/GUIDE-CREATION-CONTENU.md`
  (retirer le §4 actuel, corriger les callouts « Où créer tout ça » de
  §4/§5/§6, ajouter un renvoi)
- Delete: `Jeu Marvel Champions/docs/CHECKLIST-VALIDATION-CARTE.md` (déjà
  déplacé nulle part par Task 1 — il n'a **pas** été `git mv`, il est
  supprimé ici avec son contenu absorbé)

**Interfaces:**
- Consumes: le contenu actuel du §4 de `GUIDE-CREATION-CONTENU.md` (étapes 1
  à 7, règle §4.1 « en cas de doute ») et les 4 blocs de
  `CHECKLIST-VALIDATION-CARTE.md` (déjà lus dans cette session : revue
  texte-contre-code avec tableau de mots-pièges, comparaison des nombres,
  tests par capacité avec preuve par substitution, autoplay ciblé) ainsi que
  son gabarit final.
- Produces: `docs/reference/PROCESSUS-CARTE.md`, référencé par
  `CLAUDE.md` (Task 2), `docs/README.md` (Task 3) et
  `PROCESSUS-HEROS.md` (Task 5).

- [ ] **Étape 1 : relire les deux sources avant fusion**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
sed -n '381,454p' docs/reference/GUIDE-CREATION-CONTENU.md   # §4 actuel + §4.1
cat docs/CHECKLIST-VALIDATION-CARTE.md                        # 4 blocs + gabarit
```

- [ ] **Étape 2 : écrire `docs/reference/PROCESSUS-CARTE.md`**

Structure exacte (fusion dans l'ordre d'exécution réel, contenu des deux
fichiers repris sans perte — le tableau des mots-pièges du Bloc 1 et la
règle §4.1 « en cas de doute » se recopient **mot pour mot**, ne pas les
paraphraser) :

```markdown
# Processus — une carte, du début à la fin

Fichier unique : construire ET vérifier une carte, dans l'ordre réel
d'exécution. Fusion de l'ancien §4 de `GUIDE-CREATION-CONTENU.md` et de
l'ancien `CHECKLIST-VALIDATION-CARTE.md` (29/08/2026). Une seule carte à la
fois (jamais un lot validé en bloc).

## Étape 1 — Entrée dans `data/cards.json`

Ajouter l'entrée dans le bon pack (tri par `card_id`). Renseigner `type`,
`name`, `desc`, `traits`, `set_name`, `text`. Format détaillé :
`GUIDE-CREATION-CONTENU.md` §2.

## Étape 2 — Carte(s) de référence *(obligatoire, avant le script)*

Pour CHAQUE capacité distincte de la carte : quelle carte déjà scriptée est
comparable (même déclencheur, même genre d'effet), et pourquoi. Ne pas
écrire une ligne de script avant d'avoir rempli ce champ.

```
Capacité <nom> : carte de référence <card_id> (<nom>) — comparable parce que ...
```

## Étape 3 — Script

`src/cards/pack/<pack>/<set>/<card_id>.py`, `GetAbilities()`. Référence API :
`GUIDE-CREATION-CONTENU.md` §3. **Pour chaque mot-clé imprimé sur la carte**,
ouvrir sa fiche dans `mots-cles/` avant de coder son effet ; absente → la
créer d'abord (gabarit dans `mots-cles/README.md`).

### En cas de doute : DEMANDER, carte par carte

**Règle absolue.** Dès qu'une carte laisse place à plus d'une lecture, on ne
tranche pas tout seul : on pose la question à l'utilisateur.

- **Une question à la fois**, en **multichoix**, avec l'option recommandée en
  premier et « Autre (précise) » toujours disponible en dernier.
- **Une question par carte.** Ne jamais grouper « voici mes 8 arbitrages,
  valide en bloc » : chaque carte a son contexte, et un lot se valide à la
  légère.
- Chaque option doit dire **ce que ça change en jeu**, pas seulement ce que ça
  change dans le code.
- Poser la question **avant** d'écrire le script, pas après.

Ce qui déclenche une question, sans exception :

| Situation | Exemple vécu |
|---|---|
| Mot-clé maison non défini sur les cartes fournies | `drain X` (Agent Anti-Venom) : introuvable sur les scans et en ligne |
| Texte imprimé contradictoire | The Made Men : « Forced **Interrupt** : **After** Maniac schemes or attacks » |
| Valeur imprimée que le moteur ne sait pas encoder | l'ATK « ★ » du Homme-Pourpre |
| Portée d'une phrase ambiguë | « Discard this obligation » : la dernière option seulement, ou les deux ? |
| Mot-clé officiel inapplicable tel quel | `TeamUp` de Power Couple, qui suppose DEUX héros en jeu |
| Contenu absent du matériel fourni | aucune decklist d'aspect livrée par l'auteur |
| Un effet que le moteur ne peut pas rendre fidèlement | « if this attack has ranged or piercing » sur un événement |
| Une icône imprimée qu'on ne reconnaît pas | l'icône « nœuds reliés » de Lockjaw, prise pour un os pendant cinq jours |

**Une icône de ressource ne se nomme jamais à vue.** Elle se vérifie contre
une carte du **même pack** dont la fiche déclare la ressource : `desc.RES`
vaut `R` physique, `B` mental, `Y` énergie, `G` wild.

Ce qui ne déclenche PAS de question : les choix purement techniques sans effet
sur les règles. Ceux-là se documentent au §9 de `GUIDE-CREATION-CONTENU.md`,
ils ne se discutent pas.

## Étape 4 — Image

`assets/pics/<card_id>.<jpg|png|webp>` (extension obligatoire).

## Étape 5 — Bloc texte-contre-code, ligne par ligne

Lire le texte imprimé phrase par phrase, puis le script Python, et vérifier
que chaque mot du texte a sa contrepartie exacte dans le code.

**Liste des mots-pièges à chercher explicitement sur CHAQUE carte** :

| Mot ou tournure | Piège concret déjà rencontré |
|---|---|
| `each`, `for each` | rendu par erreur « chaque joueur » au lieu de « chaque héros » (`wd001b`, `wd014`) |
| `against you`, `your` | portée oubliée ou élargie par erreur |
| `you control` | le coût ou la cible peut viser une carte hors du contrôle du joueur, y compris celle du vilain (`wd165`) |
| `unless`, `otherwise`, `without` | branche alternative non codée |
| `instead` | un déplacement écrit « instead » veut dire que la chose PART d'un endroit et ARRIVE ailleurs, pas qu'elle est dupliquée (leçon The Spot) |
| `once per round per player` | à ne pas coder comme une limite globale (`wd056b`) |
| `if you cannot` | vérifier que le cas testé est réellement atteignable (`wd028`) |
| `that <nom>` | vérifier que la cible visée est bien LA MÊME carte que celle nommée plus haut (`wd022`) |
| `equal number` | vérifier le sens exact du décompte (`wd037`) |
| `attacks` vs `attacks or engages` vs `attacks and damages` | trois déclencheurs différents (`wd006`, `41013` Cypher) |
| `and remove` (coût à plusieurs parties) | vérifier qu'AUCUNE partie n'est oubliée (`wd005`) |
| `defeated` vs `damaged` | ne jamais coder l'un pour l'autre (`45160` Scarab) |
| **Response**/**Interrupt** + `After` | déclencheur = vrai message du moteur avec fenêtre (`wd089`) |
| **Forced Interrupt** vs **Forced Response** | l'un résout AVANT l'événement, l'autre APRÈS (`40187` Reaper, `38031` Bonebreaker) |
| **Hero Response**/**Hero Action** | sous-type dédié, pas le type nu (`27009` Web-Bracelet) |
| un second Interrupt/Response/mot-clé annoncé | vérifier qu'il a vraiment un module (`wd077b`) |
| mot-clé cité mais pas imprimé sur CETTE carte | ne pas coder de capacité fantôme |
| icône de ressource | vérifier contre une carte du MÊME PACK, jamais à vue (leçon Lockjaw) |

**Bases automatiques à ne pas recoder inutilement** : `Toughness` et
`Restricted` sont lus par le moteur directement dans `desc`, aucun module
n'est nécessaire pour eux.

Si un mot ou une tournure ne figure pas dans la liste mais laisse un doute :
appliquer la règle « en cas de doute » ci-dessus.

## Étape 6 — Bloc nombres, texte ↔ code

Relever chaque valeur numérique imprimée (coûts, seuils, PV, compteurs,
« X fois », limites, distances) et vérifier qu'elle est identique dans
`data/cards.json` (`desc`) ET dans le script Python. Ce seul filet a trouvé
`wd077b` tout seul le 20/08/2026 : ne jamais le sauter.

## Étape 7 — Bloc tests par capacité, preuve par substitution

Pour CHAQUE capacité distincte (chaque bloc Action/Response/Interrupt/When
Revealed... séparé sur le texte imprimé) :

1. Écrire un cas dans `tools/test_capacites.py` qui monte une position réelle
   avec l'API Puzzle, déclenche la capacité, et vérifie l'état du monde.
2. Le cas doit être **sujet** : le `card_id` apparaît dans le NOM du cas.
3. **Preuve par substitution, obligatoire** : retirer/commenter le module,
   relancer le cas, constater ROUGE. Remettre le module, constater VERT.
4. Clés déterministes utiles : `main_exclusive`, `cibles`, `surpayer`,
   `payer_avec`, `accepter_choix`, `heros2`.
5. Pour une capacité de tour de jeu : `Puzzle.Attack`, `Puzzle.Scheme`,
   `Puzzle.Action` plutôt que « hors de portée du harnais ».

Aucune carte n'est « terminée » tant qu'il reste une capacité sans cas sujet
et sans preuve par substitution.

## Étape 8 — Bloc autoplay ciblé, grep exhaustif des erreurs

1. `tools/autoplay.py` sur le deck/scénario qui contient la carte, au moins
   8 parties, contre le même vilain qu'un héros TÉMOIN dans la même fournée.
2. Grep **exhaustif** de tous les logs, pas seulement le compteur d'incidents :
   ```bash
   for f in /tmp/autoplay_*.log; do
     grep -c "NameError\|AttributeError\|TypeError\|KeyError\|AssertionError" "$f"
   done
   ```
   Résultat attendu : 0 partout.
3. **Lire le journal ligne à ligne** pour les parties qui touchent
   directement la nouvelle carte, pas seulement grep les mots d'erreur.
4. Comparer le taux de blocage de la nouvelle carte à celui du témoin.

## Ce que ces blocs ne peuvent pas voir

Une vraie partie jouée par un humain dans le navigateur reste le seul juge
de « est-ce que la carte est agréable et fait ce qu'elle promet ». Si ce
point n'a pas été fait, l'écrire noir sur blanc dans le rapport de fin de
travail. Jamais « à vérifier en partie réelle » sans dire PRÉCISÉMENT quel
outil manque.

## Gabarit à copier, une fois par carte

```
### <card_id> — <nom de la carte>

- [ ] Étape 2 — carte(s) de référence : ...
- [ ] Étape 5 — texte-contre-code : mots-pièges vérifiés (lister) : ...
      Résultat : ...
- [ ] Étape 6 — nombres texte ↔ code : ...
      Résultat : ...
- [ ] Étape 7 — cas test_capacites par capacité, preuve par substitution :
      capacité 1 : cas <nom>, rouge sans module / vert avec — capacité 2 : ...
      Résultat : ...
- [ ] Étape 8 — autoplay ciblé : N parties, témoin <héros>, grep tracebacks : 0,
      lecture du journal : ...
      Résultat : ...

Carte terminée : OUI / NON — si NON, ce qui manque et pourquoi.
```
```

- [ ] **Étape 3 : retirer le §4 de `GUIDE-CREATION-CONTENU.md`, corriger les callouts « Où créer tout ça » et ajouter un renvoi**

Dans `docs/reference/GUIDE-CREATION-CONTENU.md` :
- Remplacer tout le contenu actuel du §4 (de `## 4. Checklist — nouvelle carte`
  jusqu'à juste avant `## 5. Checklist — nouveau héros`) par :

  ```markdown
  ## 4. Nouvelle carte

  Voir `PROCESSUS-CARTE.md`, qui couvre construction ET validation dans
  l'ordre d'exécution. Ce fichier-ci reste la référence pour le format des
  données (§2) et l'API de scripting (§3).
  ```
- Dans les callouts « Où créer tout ça » en tête des §4 (déjà remplacé
  ci-dessus, donc rien à faire ici), §5 et §6 : ils citent encore
  `~/marvel-work/fusion/marvel-lcg-src/` comme copie vivante et renvoient au
  `rsync` de §1.3 (supprimé le 29/08/2026, voir le correctif en tête de
  §1.1). Remplacer chaque occurrence de ce callout par :

  ```markdown
  > **Où créer tout ça** : dans la copie vivante `Fusion/marvel-lcg-src/`
  > (voir §1.1). Depuis le 29/08/2026 il n'y a plus de recopie à faire.
  ```

  Utiliser cette commande pour localiser les trois occurrences avant édition :

  ```bash
  grep -n "Où créer tout ça" "docs/reference/GUIDE-CREATION-CONTENU.md"
  ```

- [ ] **Étape 4 : supprimer l'ancien fichier de checklist**

```bash
git rm docs/CHECKLIST-VALIDATION-CARTE.md
```

- [ ] **Étape 5 : vérifier qu'aucune référence morte ne subsiste vers l'ancien fichier**

```bash
grep -rn "CHECKLIST-VALIDATION-CARTE" "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions" --include="*.md"
```

Attendu : aucune occurrence (si une occurrence apparaît hors de
`PROCESSUS-CARTE.md`/`GUIDE-CREATION-CONTENU.md` déjà traités dans cette
tâche, la corriger avant de continuer).

- [ ] **Étape 6 : commit**

```bash
git add docs/reference/PROCESSUS-CARTE.md docs/reference/GUIDE-CREATION-CONTENU.md
git commit -m "docs: fusionner §4 + CHECKLIST-VALIDATION-CARTE en PROCESSUS-CARTE.md"
```

---

### Task 5: Créer `docs/reference/PROCESSUS-HEROS.md`

**Files:**
- Create: `Jeu Marvel Champions/docs/reference/PROCESSUS-HEROS.md`
- Modify: `Jeu Marvel Champions/docs/reference/GUIDE-CREATION-CONTENU.md`
  (retirer le §5 actuel, garder §5.2/§5.3 comme sous-sections référencées
  depuis le nouveau fichier plutôt que dupliquées)

**Interfaces:**
- Consumes: contenu actuel du §5 (étapes 1 à 10), §5.1 (mini-biographie),
  §5.2 (carte signature d'un autre héros), §5.3 (identité alternative).
- Produces: `docs/reference/PROCESSUS-HEROS.md`, référencé par `CLAUDE.md`
  (Task 2) et `docs/README.md` (Task 3).

- [ ] **Étape 1 : relire la source avant réécriture**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
sed -n '455,613p' docs/reference/GUIDE-CREATION-CONTENU.md   # §5 complet, §5.1 à §5.3
```

- [ ] **Étape 2 : écrire `docs/reference/PROCESSUS-HEROS.md`**

```markdown
# Processus — un nouveau héros, du début à la fin

Étapes propres au héros. Chaque carte du pack passe en plus par
`PROCESSUS-CARTE.md` en entier : ce fichier ne duplique pas ses 8 étapes.

## Étape 1 — Cartes dans `data/cards.json`

Pack du produit, `set_name` = nom du héros :
- `XXXXXa` type `Hero` (`HP/ATK/THW/DEF/HS`) et `XXXXXb` type `AlterEgo`
  (`HP/REC/HS`) — même carte, deux faces ;
- les ~15 cartes signature ;
- 1 obligation (`desc.GiveTo` = nom de l'alter-ego) ;
- 5 cartes némésis (`set_name` = `"<Héros> Nemesis"`).

## Étape 2 — Scripts

Pour chaque carte à capacités, y compris les faces a/b du héros (capacités
imprimées ; ATK/THW/DEF/REC de base sont automatiques).

## Étape 3 — Deck de départ

`deck/starter/<hero>.json` :
```json
{ "version": "0.5.8", "name": "Mon Héros", "metadata": {"url": ""},
  "hero": ["XXXXXa,XXXXXb"],
  "hero_deck": ["...15 cartes..."],
  "set_aside": [],
  "obligations": ["..."],
  "nemesis_set": ["...5 cartes..."],
  "player_deck": ["...~25 cartes d'aspect..."] }
```

## Étape 4 — `data/nemesis/<hero>_nemesis.json`

Facultatif, pour l'UI.

## Étape 5 — Référencer dans `data/sets_info.json`

Dans `heroes` du bon pack.

## Étape 6 — Images

`assets/pics/<card_id>.jpg` pour toutes les cartes (extension obligatoire).

## Étape 7 — Biographie *(case à cocher avec preuve, pas une ligne qu'on oublie)*

Ajouter une entrée dans `public/js/prepare/heros-info.js`, **indexée par le
`card_id` de la face héros** et jamais par le nom :

```js
"64001a": {
    bio:   "3 ou 4 phrases : origine, pouvoirs, ce qui définit le personnage.",
    bioEn: "Same, in English.",
    civil: "Johnny Storm",
    base: "New York (Baxter Building)",
    equipes: "Quatre Fantastiques, Vengeurs",
    equipesEn: "Fantastic Four, Avengers",
    ennemis: "Fatalis, l'Homme-Taupe",
    ennemisEn: "Doctor Doom, Mole Man",
    apparition: "Fantastic Four #1 (1961)",
},
```

Règles : tout champ optionnel sauf `bio`/`bioEn` (mieux vaut omettre que
d'inventer) ; les `*En` seulement si la traduction diffère ; viser 3-4
phrases (panneau étroit, 314 px) ; libellés affichés via `t()` dans
`public/js/prepare/dico-en.js`. Un héros sans entrée retombe silencieusement
sur l'ancien affichage : rien ne casse, mais la fiche manque, donc **preuve
obligatoire** = confirmer au survol du héros dans le wizard que le panneau
affiche bien le texte attendu, pas juste le grand visuel seul.

Ne pas ajouter de biographie pour une identité alternative purement
cosmétique (voir Étape 10 ci-dessous) : le panneau s'indexe sur la face du
deck de base, une entrée pour la variante resterait orpheline.

## Étape 8 — Texte français de chaque carte *(obligatoire)*

`ui-app/src/board/textes-fr-fanmade.ts` (voir §11.1 de
`GUIDE-CREATION-CONTENU.md`). Sans lui, les cartes du pack n'ont aucun
tooltip français, et rien ne le signale.

## Étape 9 — Validation, carte par carte

`PROCESSUS-CARTE.md` en entier pour **chaque** carte du pack (pas seulement
les cartes signature), plus une partie complète jouée avec le héros.

## Étape 10 — Points d'attention transverses

**Jamais une carte signature d'un autre héros dans un deck.** Une carte de
classe `Hero` (`desc.Class = "Hero"`) appartient à un seul héros. Le moteur
ne valide PAS les decks de départ au chargement : le contrôle doit être fait
à la main.

```bash
cd "$W" && python3 - <<'EOF'
import json, glob, os
d = json.load(open('data/cards.json'))
cl = {c['card_id']: (c.get('name',''), c.get('desc',{}).get('Class',''), c.get('set_name',''))
      for p, cs in d.items() if p != 'checksum' for c in cs
      if isinstance(c, dict) and c.get('card_id')}
for f in sorted(glob.glob('deck/starter/*.json')):
    dk = json.load(open(f))
    hero_set = cl.get(dk['hero'][0].split(',')[0], ('','',''))[2]
    for cid in dk.get('player_deck', []):
        n, classe, setn = cl.get(cid, ('?','?','?'))
        if classe == 'Hero' and setn != hero_set:
            print(os.path.basename(f), '->', cid, n, '(set', setn + ')')
EOF
```

**Identité alternative (art alternatif)** : ne pas créer un deuxième deck de
départ. Déclarer la variante dans `metadata.hero_alts` du deck existant.
Détail complet : `GUIDE-CREATION-CONTENU.md` §5.3 (inchangé, conservé là-bas
pour ne pas dupliquer le mécanisme `catalog.heroes()` / `blocIdentiteHeros()`).

## Gate finale

**Héros terminé** exige :
- [ ] Étapes 1 à 8 complètes
- [ ] Un `PROCESSUS-CARTE.md` rempli et « Carte terminée : OUI » pour
      **chaque** carte du pack (lister les card_id)
- [ ] Une partie complète jouée avec le héros

Pas de héros à moitié validé : si une seule carte du pack manque son
« Carte terminée : OUI », le héros entier reste NON.
```

- [ ] **Étape 3 : retirer le §5 (hors §5.2/§5.3) de `GUIDE-CREATION-CONTENU.md`**

Remplacer `## 5. Checklist — nouveau héros` jusqu'à juste avant
`### 5.2 Ne jamais mettre une carte signature...` par :

```markdown
## 5. Nouveau héros

Voir `PROCESSUS-HEROS.md`, qui couvre toutes les étapes (cartes, scripts,
deck, biographie, texte français, validation) et exige un
`PROCESSUS-CARTE.md` rempli pour chaque carte du pack. Les deux points
d'attention ci-dessous restent ici car ils décrivent un mécanisme du moteur,
pas une étape du processus.
```

Garder `### 5.2` et `### 5.3` tels quels juste après (déjà cités depuis
`PROCESSUS-HEROS.md` Étape 10).

- [ ] **Étape 4 : commit**

```bash
git add docs/reference/PROCESSUS-HEROS.md docs/reference/GUIDE-CREATION-CONTENU.md
git commit -m "docs: réécrire §5 en PROCESSUS-HEROS.md avec gate finale"
```

---

## Phase C — Catalogue de mots-clés (dépend de Task 1)

### Task 6: Inventaire des mots-clés et index `mots-cles/README.md`

**Files:**
- Create: `Jeu Marvel Champions/docs/reference/mots-cles/README.md`

**Interfaces:**
- Consumes: `data/cards.json` et `src/cards/pack/*/*/__init__.py` du moteur
  (lecture seule), §9 de `GUIDE-CREATION-CONTENU.md`.
- Produces: la liste de slugs que les Tasks 7 à 15 consomment (une ligne par
  fiche à créer, cochée au fur et à mesure).

- [ ] **Étape 1 : confirmer la liste des mots-clés officiels présents dans les données**

```bash
W="/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
grep -noE "\"(Toughness|Guard|Quickstrike|Retaliate|Surge|Villainous|Hazard|Crisis|Acceleration|Amplify|Steady|Stalwart|Peril|Incite|Patrol|Hinder|Vulnerable|Restricted|TeamUp|Alliance|Permanent)\"" "$W/data/cards.json" | sort -t: -k2 -u | awk -F: '{print $2}' | sort -u
```

Résultat attendu (déjà vérifié le 29/08/2026) : les 20 mots-clés listés
ci-dessus sont tous présents dans `cards.json`. Si un nouveau apparaît (le
jeu a évolué depuis), l'ajouter à la liste des Tasks 7-9.

- [ ] **Étape 2 : écrire l'index**

```markdown
# Index des fiches mots-clés

Gabarit à copier pour chaque nouvelle fiche :

\`\`\`markdown
# <Mot-clé>

**Texte imprimé / définition** : ...

**Mécanisme moteur** : ...

**Carte exemple** : \`<card_id>\` — <nom>, extrait du \`.py\` correspondant
(ou « lu directement depuis \`desc\`, aucun script requis »).

**Pièges connus** : ...

**Variantes maison** : ...
\`\`\`

## Officiels

- [ ] toughness.md
- [ ] guard.md
- [ ] quickstrike.md
- [ ] retaliate.md
- [ ] restricted.md
- [ ] permanent.md
- [ ] surge.md
- [ ] villainous.md
- [ ] hazard.md
- [ ] crisis.md
- [ ] acceleration.md
- [ ] amplify.md
- [ ] steady.md
- [ ] stalwart.md
- [ ] peril.md
- [ ] incite.md
- [ ] patrol.md
- [ ] hinder.md
- [ ] vulnerable.md
- [ ] teamup.md
- [ ] alliance.md

## Maison

- [ ] drain-x.md (pack `agent_anti_venom`)
- [ ] traitor.md (pack `agent_anti_venom`)
- [ ] companion.md (pack `lockjaw`)
- [ ] squirrel.md (pack `squirrel_girl`)
- [ ] investigate-x.md (pack `jessica_jones`)
- [ ] setlist.md (pack `dazzler`)
- [ ] showtime.md (pack `dazzler`)

## Packs passés en revue, aucun mot-clé imprimé propre trouvé

(À compléter par Task 15 : liste des packs vérifiés qui n'introduisent pas
de mot-clé maison réutilisable, pour ne pas les revérifier deux fois.)
```

- [ ] **Étape 3 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add docs/reference/mots-cles/README.md
git commit -m "docs: index du catalogue de mots-clés"
```

---

### Task 7: Fiches mots-clés officiels — lot 1 (desc automatiques)

**Files:**
- Create: `docs/reference/mots-cles/toughness.md`, `guard.md`,
  `quickstrike.md`, `retaliate.md`, `restricted.md`, `permanent.md`
- Modify: `docs/reference/mots-cles/README.md` (cocher les 6 cases)

**Interfaces:**
- Consumes: index de Task 6.
- Produces: 6 fiches, consommées par `PROCESSUS-CARTE.md` Étape 3 et le
  Bloc « bases automatiques » de son Étape 5.

- [ ] **Étape 1 : pour chaque mot-clé, retrouver un exemple et vérifier s'il a un script**

```bash
W="/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
python3 -c "
import json
d = json.load(open('$W/data/cards.json'))
cards = [c for p, cs in d.items() if p != 'checksum' for c in cs if isinstance(c, dict)]
for kw in ['Toughness','Guard','Quickstrike','Retaliate','Restricted','Permanent']:
    hit = next((c for c in cards if kw in c.get('desc', {})), None)
    print(kw, '->', hit['card_id'] if hit else 'AUCUNE CARTE TROUVEE', hit.get('name') if hit else '')
"
```

Pour chaque `card_id` trouvé, vérifier s'il existe un script :

```bash
find "$W/src/cards/pack" -name "<card_id>.py"
```

- [ ] **Étape 2 : écrire les 6 fiches sur le gabarit de `mots-cles/README.md`**

Contenu attendu pour chacune, à partir des résultats de l'Étape 1 (le
`card_id` exact dépend du résultat de la commande, à reporter tel quel) :

- **toughness.md** : mécanisme = clé `desc.Toughness`, lue nativement par le
  moteur, **aucun script requis** (rappel exprès du guide : « bases
  automatiques à ne pas recoder inutilement »). Carte exemple = le
  `card_id` trouvé.
- **guard.md**, **quickstrike.md**, **retaliate.md** : mécanisme = clé
  `desc.<Keyword>` sous forme de compteur (`"1"`, `"2"`...), gérée nativement
  par les règles de combat/schemes du moteur, généralement sans script
  dédié sauf si la carte a AUSSI une capacité imprimée distincte du
  mot-clé lui-même (dans ce cas, le script porte cette capacité-là, pas le
  mot-clé). Vérifier avec la recherche `find` de l'Étape 1 si la carte
  trouvée a un script ; si oui, noter dans « Pièges connus » que le script
  ne doit pas recoder le mot-clé, seulement le reste du texte.
- **restricted.md** : identique à `toughness.md` (même rappel exprès du
  guide), clé `desc.Restricted`, aucun script requis pour la restriction
  elle-même.
- **permanent.md** : clé `desc.Permanent`, empêche la défausse/le retrait
  normal d'une carte ; lue nativement.

- [ ] **Étape 3 : cocher les 6 cases dans l'index**

- [ ] **Étape 4 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add docs/reference/mots-cles/toughness.md docs/reference/mots-cles/guard.md docs/reference/mots-cles/quickstrike.md docs/reference/mots-cles/retaliate.md docs/reference/mots-cles/restricted.md docs/reference/mots-cles/permanent.md docs/reference/mots-cles/README.md
git commit -m "docs: fiches mots-clés officiels lot 1 (Toughness, Guard, Quickstrike, Retaliate, Restricted, Permanent)"
```

---

### Task 8: Fiches mots-clés officiels — lot 2

**Files:**
- Create: `docs/reference/mots-cles/surge.md`, `villainous.md`, `hazard.md`,
  `crisis.md`, `acceleration.md`, `amplify.md`
- Modify: `docs/reference/mots-cles/README.md`

**Interfaces:**
- Consumes: index de Task 6.
- Produces: 6 fiches.

- [ ] **Étape 1 : même procédure de recherche que Task 7, Étape 1, avec cette liste de mots-clés**

```bash
W="/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
python3 -c "
import json
d = json.load(open('$W/data/cards.json'))
cards = [c for p, cs in d.items() if p != 'checksum' for c in cs if isinstance(c, dict)]
for kw in ['Surge','Villainous','Hazard','Crisis','Acceleration','Amplify']:
    hit = next((c for c in cards if kw in c.get('desc', {})), None)
    print(kw, '->', hit['card_id'] if hit else 'AUCUNE CARTE TROUVEE', hit.get('name') if hit else '')
"
```

- [ ] **Étape 2 : écrire les 6 fiches**

Mécanisme pour les six : clé `desc.<Keyword>` en compteur, mots-clés de
rencontre/vilain gérés nativement par le moteur (Surge = pioche une carte
Rencontre en plus, Villainous = ignore l'engagement normal, Hazard =
inflige des dégâts au moment de la révélation, Crisis = force une réponse
immédiate, Acceleration/Amplify = accélèrent la menace des complots).
Reprendre le `card_id` trouvé à l'Étape 1 comme carte exemple pour chaque
fiche. Si une carte a un script en plus du mot-clé (vérifier avec `find`
comme en Task 7), le signaler en « Pièges connus » : le script ne recode
jamais le mot-clé lui-même.

- [ ] **Étape 3 : cocher les 6 cases dans l'index**

- [ ] **Étape 4 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add docs/reference/mots-cles/surge.md docs/reference/mots-cles/villainous.md docs/reference/mots-cles/hazard.md docs/reference/mots-cles/crisis.md docs/reference/mots-cles/acceleration.md docs/reference/mots-cles/amplify.md docs/reference/mots-cles/README.md
git commit -m "docs: fiches mots-clés officiels lot 2 (Surge, Villainous, Hazard, Crisis, Acceleration, Amplify)"
```

---

### Task 9: Fiches mots-clés officiels — lot 3

**Files:**
- Create: `docs/reference/mots-cles/steady.md`, `stalwart.md`, `peril.md`,
  `incite.md`, `patrol.md`, `hinder.md`, `vulnerable.md`, `teamup.md`,
  `alliance.md`
- Modify: `docs/reference/mots-cles/README.md`

**Interfaces:**
- Consumes: index de Task 6.
- Produces: 9 fiches.

- [ ] **Étape 1 : recherche des exemples**

```bash
W="/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
python3 -c "
import json
d = json.load(open('$W/data/cards.json'))
cards = [c for p, cs in d.items() if p != 'checksum' for c in cs if isinstance(c, dict)]
for kw in ['Steady','Stalwart','Peril','Incite','Patrol','Hinder','Vulnerable','TeamUp','Alliance']:
    hit = next((c for c in cards if kw in c.get('desc', {})), None)
    print(kw, '->', hit['card_id'] if hit else 'AUCUNE CARTE TROUVEE', hit.get('name') if hit else '')
"
```

- [ ] **Étape 2 : écrire les 9 fiches**

Steady, Stalwart, Peril, Incite, Patrol, Hinder, Vulnerable : mécanisme =
clé `desc.<Keyword>` en compteur, mots-clés de combat/menace gérés
nativement, même traitement que Tasks 7-8.

**TeamUp** : cas particulier, déjà documenté dans le guide (§4 « en cas de
doute », exemple Power Couple 73022) — la clé `desc.TeamUp` suppose deux
identités héros en jeu simultanément. Reprendre l'exemple Power Couple
comme carte exemple, et noter en « Pièges connus » : si le second héros
nommé n'est en réalité qu'un allié signature (pas une vraie identité), le
mot-clé natif ne suffit pas, une condition de script est nécessaire (voir
`docs/reference/GUIDE-CREATION-CONTENU.md` §9, entrée `jessica_jones`).

**Alliance** : mécanisme différent des autres — hook `CheckAnyPlayerMayHelpPay`
(`game/ability/factory/resources.py`), qui autorise un autre joueur à
financer un coût. Carte exemple : Coordinated Effort (`58032`), déjà citée
dans `GUIDE-CREATION-CONTENU.md` §3.1. Variantes maison : l'AUTORISATION de
Forces Combined (pack `cloak_dagger`, `70003`) étend ce même hook — le
mentionner en « Variantes maison ».

- [ ] **Étape 3 : cocher les 9 cases dans l'index**

- [ ] **Étape 4 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add docs/reference/mots-cles/steady.md docs/reference/mots-cles/stalwart.md docs/reference/mots-cles/peril.md docs/reference/mots-cles/incite.md docs/reference/mots-cles/patrol.md docs/reference/mots-cles/hinder.md docs/reference/mots-cles/vulnerable.md docs/reference/mots-cles/teamup.md docs/reference/mots-cles/alliance.md docs/reference/mots-cles/README.md
git commit -m "docs: fiches mots-clés officiels lot 3 (Steady, Stalwart, Peril, Incite, Patrol, Hinder, Vulnerable, TeamUp, Alliance)"
```

---

### Task 10: Fiches mots-clés maison — pack `agent_anti_venom` (drain X, traitor)

**Files:**
- Create: `docs/reference/mots-cles/drain-x.md`, `traitor.md`
- Modify: `docs/reference/mots-cles/README.md`

**Interfaces:**
- Consumes: `docs/reference/GUIDE-CREATION-CONTENU.md` ligne 1109 (déjà lue
  dans cette session), `src/cards/pack/agent_anti_venom/*/__init__.py`.
- Produces: 2 fiches.

- [ ] **Étape 1 : relire la source**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
sed -n '1109p' docs/reference/GUIDE-CREATION-CONTENU.md
grep -n "def Drain\|def " "Fusion/marvel-lcg-src/src/cards/pack/agent_anti_venom"/*/__init__.py
```

- [ ] **Étape 2 : écrire `drain-x.md`**

- Définition : « X dégâts à l'ennemi, puis X soins sur Agent Anti-Venom, et
  sur lui seul » — lecture arrêtée avec l'utilisateur le 4/8/2026 (mot-clé
  introuvable sur les scans fournis et en ligne).
- Mécanisme : centralisé dans `Drain()` du `__init__.py` du set
  `agent_anti_venom`.
- Carte exemple : Bear Arms et Unlikely Allies (relire les `card_id` exacts
  via `grep -n "Bear Arms\|Unlikely Allies" Fusion/marvel-lcg-src/data/cards.json`
  et reporter le script correspondant).
- Pièges connus : mot-clé maison non défini sur les cartes fournies —
  déclenche systématiquement une question à l'utilisateur (voir
  `PROCESSUS-CARTE.md`, tableau « en cas de doute »).
- Variantes maison : aucune connue au 29/08/2026.

- [ ] **Étape 3 : écrire `traitor.md`**

- Définition : défini en toutes lettres sur les cartes qui le posent (pas
  un mot-clé ambigu, contrairement à `drain X`).
- Mécanisme : `TreatAsMinion` (`game/ability/factory/treat.py`) appelé HORS
  attachement (le moteur ne l'exposait que via `AfterCardGainUpgrade`).
  Carte-gabarit `aav_traitor_minion` avec SCH forcé à 1.
- Carte exemple : Infected Scorpion (retrouver le `card_id` via
  `grep -n "Infected Scorpion" Fusion/marvel-lcg-src/data/cards.json`).
- Pièges connus : le déclenchement hors attachement est la partie non
  standard — une implémentation naïve ne se déclenche que via
  `AfterCardGainUpgrade`, ce qui rate le cas `traitor`.
- Variantes maison : `TreatAsAlly` de Totally Awesome Hulk (`tah_hellbender_ally`,
  pack `totally_awesome_hulk`) est le même genre de montage (« traiter une
  carte comme si »), à inspecter si un futur pack a besoin d'un « traiter
  comme » différent.

- [ ] **Étape 4 : cocher les 2 cases dans l'index**

- [ ] **Étape 5 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add docs/reference/mots-cles/drain-x.md docs/reference/mots-cles/traitor.md docs/reference/mots-cles/README.md
git commit -m "docs: fiches mots-clés maison drain X et traitor (agent_anti_venom)"
```

---

### Task 11: Fiche mot-clé maison — pack `lockjaw` (Companion)

**Files:**
- Create: `docs/reference/mots-cles/companion.md`
- Modify: `docs/reference/mots-cles/README.md`

**Interfaces:**
- Consumes: `docs/reference/GUIDE-CREATION-CONTENU.md` ligne 1124.
- Produces: 1 fiche.

- [ ] **Étape 1 : relire la source**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
sed -n '1124p' docs/reference/GUIDE-CREATION-CONTENU.md
```

- [ ] **Étape 2 : écrire `companion.md`**

- Définition : « ne compte pas dans la limite d'alliés et ne peut pas
  défendre ».
- Mécanisme : composé dans le `__init__.py` du set `lockjaw` à partir de
  `ThisNotCountAllyLimit` + `UnitCannotDefend`.
- Carte exemple : retrouver un allié `Companion` du pack via
  `grep -n "Companion" Fusion/marvel-lcg-src/data/cards.json | grep -i lockjaw`
  ou en listant les cartes du set `lockjaw` (`78001a-78030`).
- Pièges connus : aucun signalé au 29/08/2026.
- Variantes maison : **Squirrel** (pack `squirrel_girl`, voir `squirrel.md`)
  reprend exactement ce montage en y ajoutant une capacité de dépense — les
  deux fiches se renvoient l'une à l'autre.

- [ ] **Étape 3 : cocher la case dans l'index**

- [ ] **Étape 4 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add docs/reference/mots-cles/companion.md docs/reference/mots-cles/README.md
git commit -m "docs: fiche mot-clé maison Companion (lockjaw)"
```

---

### Task 12: Fiche mot-clé maison — pack `squirrel_girl` (Squirrel)

**Files:**
- Create: `docs/reference/mots-cles/squirrel.md`
- Modify: `docs/reference/mots-cles/README.md`, `docs/reference/mots-cles/companion.md`
  (ajouter le renvoi croisé si Task 11 est déjà faite, sinon le laisser à
  Task 11 de le faire dans l'autre sens)

**Interfaces:**
- Consumes: `docs/reference/GUIDE-CREATION-CONTENU.md` ligne 1127.
- Produces: 1 fiche.

- [ ] **Étape 1 : relire la source**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
sed -n '1127p' docs/reference/GUIDE-CREATION-CONTENU.md
```

- [ ] **Étape 2 : écrire `squirrel.md`**

- Définition : mot-clé maison = `ThisNotCountAllyLimit` + `UnitCannotDefend`
  + `UnitCannotHaveUpgradeAttached` + la capacité de dépense.
- Mécanisme : composé dans le `__init__.py` du set `squirrel_girl`. Les
  six écureuils sont posés en `additional_deck` (setup via
  `BeginGameWithSetAside` + `Faces.ShuffleAllTo`), « appelés » (révélation,
  mise en jeu épuisée) et « dépensés » via une capacité `Resource` portée
  par les deux faces d'identité (pas par les écureuils eux-mêmes, à cause
  de la limite « 1 seul écureuil par carte jouée »).
- Carte exemple : lister un écureuil via
  `grep -n "\"750" Fusion/marvel-lcg-src/data/cards.json` (pack `squirrel_girl`,
  75001-75022) et son script dans
  `Fusion/marvel-lcg-src/src/cards/pack/squirrel_girl/squirrel_deck/`.
- Pièges connus : les cartes d'un deck hors jeu ne se désignent PAS par
  `SetTarget(Select.From(faces=...))`, il faut `player.MayChooseFace`. Une
  capacité `Resource` par écureuil casserait la limite « 1 par carte
  jouée » (assertion `len(resources_effects) == 1`), d'où le montage par
  identité.
- Variantes maison : renvoi vers `companion.md` (même base
  `ThisNotCountAllyLimit` + `UnitCannotDefend`).

- [ ] **Étape 3 : cocher la case dans l'index, ajouter le renvoi croisé dans `companion.md` s'il n'y est pas déjà**

- [ ] **Étape 4 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add docs/reference/mots-cles/squirrel.md docs/reference/mots-cles/companion.md docs/reference/mots-cles/README.md
git commit -m "docs: fiche mot-clé maison Squirrel (squirrel_girl)"
```

---

### Task 13: Fiche mot-clé maison — pack `jessica_jones` (INVESTIGATE X)

**Files:**
- Create: `docs/reference/mots-cles/investigate-x.md`
- Modify: `docs/reference/mots-cles/README.md`

**Interfaces:**
- Consumes: `docs/reference/GUIDE-CREATION-CONTENU.md` ligne 1107,
  `src/cards/pack/jessica_jones/on_the_job/__init__.py` (fonction
  `Investigate`, déjà repérée dans cette session à la ligne 16).
- Produces: 1 fiche.

- [ ] **Étape 1 : relire la source**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
sed -n '1107p' docs/reference/GUIDE-CREATION-CONTENU.md
sed -n '1,40p' "Fusion/marvel-lcg-src/src/cards/pack/jessica_jones/on_the_job/__init__.py"
```

- [ ] **Étape 2 : écrire `investigate-x.md`**

- Définition : « When revealed, move X threat from the main scheme to
  here ».
- Mécanisme : `Investigate()` dans `on_the_job/__init__.py`, qui retire
  d'abord sur le complot principal et ne pose que ce qui a réellement été
  retiré. Compteur `evidence` ajouté au moteur pour Jessica's Camera (trois
  paliers 1/2/3 → +1 DEF/THW/ATK, trois `GiveKeywordToAttached` distincts
  sur `OnEvent.Counter`). Le set de rencontre « On the Job » lui-même
  (`data/encounter_sets/on_the_job.json`) est ajouté via
  `message.encounter_set_names` dans `Message.WhenGameBeginSetup`,
  enregistré en `RegisterTemp` depuis `WhenPlayerSelectHero` (avant que
  `World.Begin` ait mélangé le deck).
- Carte exemple : lister les cartes 73012-73016 via
  `grep -n "\"7301[2-6]\"" Fusion/marvel-lcg-src/data/cards.json`.
- Pièges connus : aucune fabrique moteur ne porte ce mot-clé nativement, ne
  pas chercher du côté d'`AbilityFactory` standard.
- Variantes maison : aucune connue au 29/08/2026.

- [ ] **Étape 3 : cocher la case dans l'index**

- [ ] **Étape 4 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add docs/reference/mots-cles/investigate-x.md docs/reference/mots-cles/README.md
git commit -m "docs: fiche mot-clé maison INVESTIGATE X (jessica_jones)"
```

---

### Task 14: Fiches mots-clés maison — pack `dazzler` (Setlist, Showtime!)

**Files:**
- Create: `docs/reference/mots-cles/setlist.md`, `showtime.md`
- Modify: `docs/reference/mots-cles/README.md`

**Interfaces:**
- Consumes: `src/cards/pack/dazzler/dazzler/__init__.py` (fonctions
  `Showtime`, `Setlist`, `Concert`, `SongsDansLaDefausse`... déjà repérées
  dans cette session), `data/cards.json` (pack `dazzler`).
- Produces: 2 fiches.

Ce pack n'apparaît pas dans le tableau §9 de `GUIDE-CREATION-CONTENU.md`
(créé après la dernière mise à jour de cette section) : pas de paragraphe à
relire, la source est uniquement le code.

- [ ] **Étape 1 : lire le mécanisme dans le script**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
sed -n '1,270p' "Fusion/marvel-lcg-src/src/cards/pack/dazzler/dazzler/__init__.py"
grep -n "\"Showtime\|\"Setlist\|Song" "Fusion/marvel-lcg-src/data/cards.json" | head -20
```

- [ ] **Étape 2 : écrire `setlist.md` et `showtime.md`**

Remplir le gabarit à partir de la lecture de l'Étape 1 : la définition
exacte (texte imprimé des cartes concernées), le mécanisme (fonctions
`Setlist()`/`Showtime()` et leurs helpers `ResoudreShowtime`,
`CiblesShowtime`, `Concert`, `EstRepete`/`MarquerRepete`/`EffacerRepete`,
`SongsDansLaDefausseBornee`), et au moins une carte exemple avec `card_id`
réel trouvé à l'Étape 1 (pas un `card_id` inventé). Si en lisant le code la
distinction Setlist/Showtime! s'avère être une seule mécanique et pas deux
mots-clés séparés, n'écrire qu'une seule fiche et le signaler dans le
commit.

- [ ] **Étape 3 : cocher les cases dans l'index (ou une seule si fusionné à l'Étape 2)**

- [ ] **Étape 4 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add docs/reference/mots-cles/setlist.md docs/reference/mots-cles/showtime.md docs/reference/mots-cles/README.md
git commit -m "docs: fiches mots-clés maison Setlist et Showtime! (dazzler)"
```

---

### Task 15: Revue des packs restants, mots-clés éventuels manqués

**Files:**
- Create: fiches supplémentaires si un mot-clé imprimé réutilisable est
  trouvé (chemin `docs/reference/mots-cles/<slug>.md`, gabarit identique aux
  tâches précédentes)
- Modify: `docs/reference/mots-cles/README.md` (section « Packs passés en
  revue, aucun mot-clé imprimé propre trouvé »)

**Interfaces:**
- Consumes: le reste du §9 (`rainy`, `albert`, `gwenpool`, `human_torch`,
  `mister_fantastic`, `the_thing`, `totally_awesome_hulk`, `invisible_woman`,
  `madame_web`, `cloak_dagger`, `spider_man_rainy`, `venom_rainy`,
  `moon_knight`, `brawn` — lignes 1084-1130 sauf celles déjà traitées) et les
  packs absents de §9 (`wolverine_x23`, `red_guardian`, `jj`, `luke_cage`).
- Produces: l'index complet, tenu à jour.

**Comment trancher « mot-clé imprimé propre » vs « mécanisme interne » :**
un mot-clé mérite une fiche s'il apparaît **en gras sur le texte imprimé
d'au moins une carte**, comme `Companion` ou `Squirrel` (vérifiable dans
`desc.text` de la carte dans `cards.json`). Une fonction Python nommée
`BouclierEnJeu` ou `EstTonHeros` qui sert UNE seule carte sans mot-clé
imprimé correspondant n'est pas un mot-clé : c'est un helper de script
normal, il n'a pas sa place dans le catalogue.

- [ ] **Étape 1 : lister les packs à vérifier avec leur ligne §9 (ou absence)**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
for l in 1084 1085 1091 1092 1093 1094 1095 1096 1102 1104 1105 1111 1130; do
  sed -n "${l}p" docs/reference/GUIDE-CREATION-CONTENU.md
  echo "---"
done
```

(1097 = `madame_web`, 1124 = `lockjaw`, 1127 = `squirrel_girl`, 1107 =
`jessica_jones`, 1109 = `agent_anti_venom` sont déjà traités par les Tasks
10-13 et exclus de cette liste.)

- [ ] **Étape 2 : pour chaque pack, chercher un texte imprimé en gras suspect de mot-clé**

```bash
W="/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
for pack in rainy albert gwenpool human_torch mister_fantastic the_thing totally_awesome_hulk invisible_woman cloak_dagger spider_man_rainy venom_rainy moon_knight brawn wolverine_x23 red_guardian jj luke_cage; do
  echo "== $pack =="
  python3 -c "
import json
d = json.load(open('$W/data/cards.json'))
cards = d.get('$pack', [])
for c in cards:
    t = c.get('text', '')
    import re
    for m in re.findall(r'<b>([A-Z][a-zA-Z ]{2,20})</b>', t):
        print(' ', c['card_id'], '->', m)
"
done
```

Cette commande fait remonter tout mot en gras qui pourrait être un mot-clé
(officiel déjà catalogué, maison à cataloguer, ou simplement un nom de
capacité propre à une carte comme « Showtime! » vu en Task 14 — utiliser le
même critère qu'en tête de cette tâche pour trancher).

- [ ] **Étape 3 : pour chaque candidat retenu, écrire sa fiche sur le gabarit habituel**

Reprendre la procédure de Task 10-14 : lire le script du set concerné,
identifier le mécanisme réel, choisir un `card_id` exemple réel.

- [ ] **Étape 4 : mettre à jour l'index**

Ajouter les nouvelles fiches créées à la section « Maison » de
`mots-cles/README.md`, et lister dans la nouvelle section « Packs passés en
revue » tous les packs vérifiés à l'Étape 2 qui n'ont produit aucun
candidat retenu.

- [ ] **Étape 5 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add docs/reference/mots-cles/
git commit -m "docs: revue des packs restants pour le catalogue de mots-clés"
```

---

## Phase D — Nettoyage final

### Task 16: Alléger le §9 de `GUIDE-CREATION-CONTENU.md`

**Files:**
- Modify: `docs/reference/GUIDE-CREATION-CONTENU.md` (§9 uniquement)

**Interfaces:**
- Consumes: toutes les fiches créées en Phase C (Tasks 7-15).
- Produces: §9 allégé, sans duplication du mécanisme déjà décrit dans les
  fiches.

- [ ] **Étape 1 : repérer, dans chaque ligne de §9 traitée en Phase C, le passage qui explique le MÉCANISME du mot-clé (par opposition à l'historique/le pourquoi du pack)**

Exemple concret sur la ligne `agent_anti_venom` (1109) : le passage
« rendu par `Drain()` du `__init__.py` du set » est du mécanisme (→
supprimer, remplacer par un renvoi) ; le passage « lecture arrêtée avec
l'utilisateur le 4/8/2026 » est de l'historique (→ garder).

- [ ] **Étape 2 : pour chaque ligne traitée (1107, 1109, 1124, 1127, et toute
  fiche créée en Task 14/15), remplacer le passage mécanisme par un renvoi**

Format du renvoi : `(mécanisme détaillé dans mots-cles/<slug>.md)`, inséré
à l'endroit où le mécanisme était expliqué, phrase gardée courte. Ne pas
toucher aux lignes des packs qui n'ont pas de mot-clé catalogué (le reste de
leur paragraphe narratif reste inchangé).

- [ ] **Étape 3 : vérifier qu'aucun mécanisme n'est resté dupliqué**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
grep -n "mots-cles/" docs/reference/GUIDE-CREATION-CONTENU.md
```

Attendu : un renvoi par mot-clé catalogué référencé dans §9 (au moins 7 :
drain-x, traitor, companion, squirrel, investigate-x, setlist, showtime, plus
tout ajout de Task 15).

- [ ] **Étape 4 : commit**

```bash
git add docs/reference/GUIDE-CREATION-CONTENU.md
git commit -m "docs: alléger §9, renvoyer vers le catalogue de mots-clés au lieu de dupliquer le mécanisme"
```

---

### Task 17: Vérification finale — aucune référence morte

**Files:**
- Aucun fichier créé ; vérification pure, corrections ponctuelles si un
  chemin mort est trouvé.

**Interfaces:**
- Consumes: l'ensemble du travail des Tasks 1 à 16.
- Produces: confirmation que le chantier est cohérent de bout en bout.

- [ ] **Étape 1 : chercher toute référence à un ancien chemin dans tout le projet (pas seulement `docs/`)**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
grep -rln "docs/GUIDE-CREATION-CONTENU\|docs/CHECKLIST-VALIDATION-CARTE\|docs/CAMPAGNES\|docs/RANGEMENT\|docs/RAPPORT-AUDIT-CARTES\|docs/RAPPORT-SCANS-FR\|docs/BRIEF-REFONTE-PLATEAU\|docs/squirrel_girl_cartes\|docs/squirrel_girl_complete_custom_hero_pack_and_starter_deck\|docs/GUIDE-STRATEGIE-JEU\|docs/MULTIJOUEUR" -- . --include="*.md" --include="*.js" --include="*.py" --include="*.sh"
```

Attendu : aucune occurrence hors des fichiers déjà corrigés dans ce plan. Si
une occurrence apparaît (par exemple un ancien lanceur ou un autre document
qui citait un de ces fichiers par son ancien chemin), corriger le chemin sur
place.

- [ ] **Étape 2 : confirmer tous les liens internes de `docs/README.md` et `CLAUDE.md`**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/docs"
for f in reference/PROCESSUS-CARTE.md reference/PROCESSUS-HEROS.md reference/GUIDE-CREATION-CONTENU.md reference/mots-cles/README.md reference/MULTIJOUEUR.md reference/CAMPAGNES.md reference/GUIDE-STRATEGIE-JEU.md rapports/RANGEMENT.md rapports/RAPPORT-AUDIT-CARTES.md rapports/RAPPORT-SCANS-FR.md rapports/BRIEF-REFONTE-PLATEAU.md packs/squirrel_girl; do
  [ -e "$f" ] && echo "OK  $f" || echo "MANQUANT $f"
done
```

Attendu : tout `OK` (contrairement à la vérification identique en Task 3,
`PROCESSUS-CARTE.md`, `PROCESSUS-HEROS.md` et `mots-cles/README.md` doivent
maintenant exister).

- [ ] **Étape 3 : confirmer que toutes les cases de `mots-cles/README.md` sont cochées**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
grep -n "^\- \[ \]" docs/reference/mots-cles/README.md
```

Attendu : aucune ligne (toutes les cases `- [ ]` sont devenues `- [x]` au
fil des Tasks 7-15). Si des cases restent vides, la fiche correspondante
n'a pas été créée : y remédier avant de clore le plan.

- [ ] **Étape 4 : `git status` final propre sur `docs/` et `CLAUDE.md`**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git status --short -- docs/ CLAUDE.md
```

Attendu : rien (tout a été commité au fil des tâches). Si des fichiers
apparaissent encore modifiés, les committer.

- [ ] **Étape 5 : commit final si l'Étape 1 a produit des corrections**

```bash
git add -- docs/ CLAUDE.md
git commit -m "docs: corriger les dernières références mortes après la refonte"
```

(Ne pas committer si l'Étape 1 n'a rien trouvé à corriger — pas de commit
vide.)
