# Marvel LCG — Reconstruction du code source : passation V2

Suite de `HANDOFF.md` (dépôt Claude). Ce document rend l'état vérifié par
exécution au 26 juillet 2026, après fusion des travaux Claude et ChatGPT.

---

## 1. Résultat en une phrase

Le code source du jeu est **fonctionnellement reconstruit à ~99,9 %** : sur
4 295 fichiers Python, **4 289 sont vérifiés par substitution réelle** dans
le jeu (ils remplacent le bytecode d'origine et le jeu fonctionne avec).
Il reste **10 fichiers défectueux** (9 moteur + `cards/database.py`), pour
lesquels le dépôt embarque le bytecode d'origine afin que le jeu tourne
quand même à 100 %.

**Progression étape 4** : 18 fichiers moteur reconstruits et vérifiés cette
session (0 régression sur les 3 444 cartes + création de partie OK). Catalogue
des artefacts du décompilateur rencontrés et corrigés :
- guillemets d'annotations forward perdus (`x: World` → `x: 'World'`) :
  `attachment.py`, `environment_helper.py`
- accolades `{}` parasites (faux `set`) sur des concaténations de chaînes :
  `rbyg.py` (débloque 224 cartes), `scene.py`
- bloc `UNKNOWN(...)` unique = un `return` conditionnel : `form.py`,
  `resolve.py`
- `if/else` aplati avec assertion fausse : `selector_range.py` (débloque 29
  cartes)
- unpacking de boucle perdu (`for i, x in enumerate/items`) : `job/manager.py`,
  `statistics.py`, `config.py`, `finder.py`
- blocs `with` perdus (`SETUP_WITH`) : `condition.py`, `loader.py`
- blocs `try/except` perdus (`SETUP_FINALLY`) : `net_lib.py`, `user_info.py`,
  `file/manager.py`, `image_creator.py`
- comparaison chaînée aplatie (`0 <= x <= n`) : `net_lib.py`
- `return` sans valeur (valeur retournée perdue) : `file/manager.py`
  (`FindJsonPath` renvoyait `None` → aucune partie ne démarrait)
- f-string inversée (`f"{'.2f':x}"` → `f"{x:.2f}"`) : `user_info.py`
- `import numpy.random as numpy` parasite : `random.py`
- corps de fonctions `@deprecated` effacés : `treat.py`

**Attention méthode (leçon coûteuse)** : plusieurs fichiers (`random.py`,
`scene.py`, `file/manager.py`) passaient le test des cartes mais cassaient la
**création de partie**, et `finder.py` passait le boot mais cassait 5 cartes.
Un fichier moteur n'est « vérifié » qu'après `test_cards.py` **et**
`test_newgame.py`, tous deux à 0 régression. Corollaire : corriger le seul
marqueur signalé ne suffit pas — `finder.py` avait 3 bugs voisins non marqués
(deux `return` prématurés, une f-string). Toujours comparer méthode par méthode
au désassemblage du `.pyc` d'origine.

C'est très au-delà de l'estimation du HANDOFF V1 (234 fichiers moteur à
reconstruire, 60-80 sessions).

---

## 2. Chiffres vérifiés par exécution

Méthode : Python 3.10.13, moteur substitué fichier par fichier dans une
copie bootable, puis exécution réelle. Aucun chiffre de décompilation.

| Test | Référence (bytecode original) | Dépôt fusionné | Verdict |
|---|---|---|---|
| `Engine.Initialize()` | True | True | identique |
| `GET /scene` | HTTP 200, 75 211 o | HTTP 200, 75 211 o | **identique à l'octet** |
| Création de partie (Spider-Man vs Rhino) | world, 1 joueur | world, 1 joueur | OK |
| Construction des capacités des cartes | 3 444 OK / 7 échecs | 3 444 OK / 7 échecs | **0 régression** |

Les 7 échecs de cartes sont présents **dans le bytecode d'origine lui-même**
(donc pas des régressions) : `cw.resistance.56200b` (NameError 'Leader'),
`mut_gen.magneto.32150`, `mut_gen.shadowcat.32055`, `nova.armadillo.28030`,
`sm.osborn_tech.27152`, `tt.trickster_magic.55061`, `55062` (AssertionError,
dépendantes du contexte de partie).

---

## 3. La découverte clé de cette session

Le décompilateur (pycdc) a **perdu les guillemets des annotations de type
« forward »** : le source d'origine écrit `def f(x: 'World')`, le décompilé
rend `def f(x: World)`. À l'import, `World` n'existe pas encore → `NameError`
en cascade, et **des centaines de fichiers paraissaient cassés alors qu'ils
étaient sains**.

- L'original n'utilise `from __future__ import annotations` **nulle part**
  (vérifié via les `co_flags` des 4 295 `.pyc`). Le retrait de cet import
  ajouté par ChatGPT était donc correct et nécessaire.
- Réparation automatisée : re-quotage des annotations forward, guidé par la
  traceback (voir `tools/master_loop.py` et `tools/card_fix_loop.py`).
  400+ annotations moteur et 200+ annotations de cartes re-quotées.

Sans cette découverte, on comptait ~93 fichiers moteur « défectueux » ;
après, il n'en reste que 27.

---

## 4. Les 28 fichiers encore défectueux (à reconstruire à la main)

Ils échouent à l'exécution pour cause de troncature pycdc ou de marqueurs
`RECOVER_TODO` / `UNKNOWN` (constructions `with`, `try/except`, décorateurs
perdus). Liste exacte dans `defectueux.json`. Bytecode d'origine fourni dans
`originals_pyc/`.

Moteur (27) — par ordre de dépendance gameplay :

- `game/ability/factory/attachment.py`  *(179 cartes en dépendent)*
- `game/selector/factory.py`, `game/selector/selector_range.py`
- `game/ability/factory/{ability_factory,form,resolve,environment,environment_helper,treat}.py`
- `game/ability/cost_func.py`
- `game/card/card_finder/{finder,checker}.py`
- `game/scene/{loader,scene}.py`, `game/element/rbyg.py`, `game/statistics/statistics.py`
- `engine/{config,job/manager,task/condition,file/manager,user/user_info,log/log}.py`
- `engine/lib/{json,image_creator,random}.py`, `engine/network/{net_lib,web_server}.py`

Cartes (1) : `cards/database.py` (14 `RECOVER_TODO`, 4 `UNKNOWN`).

Note : `game/ability/ability.py` et `game/effect/effect.py`, marqués
« reconstruits à la main » dans le HANDOFF V1, **fonctionnent** en version
ChatGPT re-quotée ; les fichiers reconstruits Claude cités au §11 du V1 sont
absents du dossier reçu (perdus), mais ils ne sont plus nécessaires.

---

## 5. Contenu du dépôt

```
marvel-lcg-src/
├── src/              4299 fichiers .py (moteur + cartes), annotations re-quotées
├── originals_pyc/    28 .pyc d'origine des fichiers défectueux
├── data/ deck/ public/ puzzle/ assets/   données et front d'origine, intacts
├── launch.json
├── launcher.py       compile src → superpose originals_pyc → démarre le jeu
├── defectueux.json   liste des 28 fichiers à réparer
├── QUALITE-V2.csv    provenance + statut vérifié de chaque fichier
├── tools/            master_loop.py, card_fix_loop.py, test_*.py, tools_fix_pycdc.py
└── HANDOFF-V2.md
```

`provenance` dans QUALITE-V2.csv : `chatgpt_corrige` = source ChatGPT +
re-quotage d'annotations, vérifiée par substitution. `bytecode_original` =
défectueux, tourne sur le `.pyc` d'origine en attendant reconstruction.

---

## 6. Lancer

```bash
# Python 3.10 OBLIGATOIRE (le bytecode d'origine des défectueux en dépend)
pip install aiohttp cryptography numpy Pillow requests Jinja2 packaging colorama psutil
python launcher.py
# puis http://127.0.0.1:2345 dans un navigateur
```

Sous Linux/WSL, `launcher.py` injecte un stub `winsound` (module Windows).
Sous Windows, il n'y touche pas.

---

## 7. Prochaine étape : reconstruire les 28 défectueux (étape 4 du plan)

Attaquer dans l'ordre du §4 (gameplay d'abord, `attachment.py` en tête).
Pour chaque fichier, méthode HANDOFF V1 §8, **non négociable** :

1. base = `src/<fichier>.py` (marqueurs `RECOVER_TODO`/`UNKNOWN` explicites),
   croisée avec `pycdas` du `.pyc` d'origine dans `originals_pyc/`.
2. reconstruire méthode par méthode ; croiser signatures avec les appelants.
3. `ast.parse`, puis **substitution + `tools/test_newgame.py` +
   `tools/test_cards.py`**. Jamais « terminé » sans substitution exécutée.
4. quand un fichier passe, le retirer de `defectueux.json` et supprimer son
   `.pyc` de `originals_pyc/` ; consigner dans QUALITE-V2.csv.

Objectif final : `defectueux.json` vide, `originals_pyc/` vide, le jeu tourne
100 % depuis le source.

### Pièges silencieux à surveiller (HANDOFF V1 §7.2)
`None.methode()` → `self.methode()` ; décorateurs perdus `X = None(X)` ;
`and`/`or` inversés (bug de règle invisible) ; queues de fonctions tronquées
sans avertissement. Une partie qui démarre ne prouve pas l'absence de ces
bugs : distinguer dans QUALITE-V2 « vérifié boot » de « vérifié gameplay ».

### Leçon de fin de session : requoter ne suffit pas
Tentative de réparation rapide des 4 fichiers factory sans marqueur
(`attachment.py`, `form.py`, `environment_helper.py`, `selector_range.py`)
par simple re-quotage d'annotations : ils passaient l'import ET la création
de partie, MAIS **cassaient 46 cartes** (AssertionError sur le nombre
d'abilities attendu, marqueurs `UNKNOWN` révélés à l'exécution). Le
re-quotage corrige l'import, pas la logique tronquée. **Critère de validation
d'un fichier factory : non pas « il importe », mais « toutes les cartes qui
l'utilisent construisent leurs capacités sans régression » (test_cards.py
complet).** Ces 4 fichiers restent donc dans `defectueux.json`.
