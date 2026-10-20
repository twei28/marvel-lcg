---

## 3. La liste maîtresse des fichiers d'une campagne

Tous les chemins sont **relatifs à la racine du moteur** (`Fusion/marvel-lcg-src/` dans le dépôt) sauf mention
contraire (`ui-app/`, `docs/`, `outils/` sont à la racine du projet, à côté de `Fusion/`).

Légende de la colonne **Livraison** :

* **NEUF** : un fichier nouveau, que tu livres tel quel à son chemin ;
* **FRAGMENT** : un fichier partagé par tout le monde : tu livres **seulement ta part**, Claude la fusionne ;
* **CLAUDE** : fichier que tu ne produis pas (générique, généré, ou touchant le moteur) ; je le liste pour que tu
  saches qu'il existe et ce qui s'y branche ;
* **OPTION** : utile, pas bloquant.

### 3.1 Données (`data/`)

| # | Chemin | Rôle | Livraison | Obligatoire | Modèle (zip) | Détail |
|---|---|---|---|---|---|---|
| D1 | `data/cards.json` | Toutes les cartes du jeu, rangées par pack : `{"<pack>": [carte, ...]}` | **FRAGMENT** `integration/data/cards.<pack>.fragment.json` = `{"<pack>": [...]}` | oui | `modeles/*/data/cards.*.fragment.json` | §4 |
| D2 | `data/sets_info.json` | L'index des packs : clé `N. Custom (Nom)` → scénarios, héros, sets modulaires, plus grand id | **FRAGMENT** `integration/data/sets_info.<pack>.fragment.json` | oui | `modeles/*/data/sets_info.*.fragment.json` | §5.4 |
| D3 | `data/scenarios/<id>.json` | Un scénario : vilain(s), complot(s) principal(aux), sets de rencontre | **NEUF** | oui, un par scénario | `modeles/*/data/scenarios/` | §5.1 |
| D4 | `data/scenarios/<id>_expert.json` | La variante experte du scénario | **NEUF** | oui si la campagne a un mode expert (toutes les officielles en ont un) | idem | §5.1 |
| D5 | `data/encounter_sets/<set>.json` | Un set de rencontre (modulaire ou propre à un scénario) | **NEUF** | un par set | `modeles/*/data/encounter_sets/` | §5.2 |
| D6 | `data/campagnes/<code>.json` | **La description de la campagne** (écran + panneau de récompenses) | **NEUF** | **oui** | `modeles/*/data/campagnes/` | §8 |
| D7 | `data/nemesis/<héros>_nemesis.json` | Set némésis d'un héros nommable | **NEUF** | option (héros seulement) | `modeles/A-*/` | §5.3 |
| D8 | `deck/starter/<héros>.json` | Deck de départ d'un héros (fait apparaître le héros dans le jeu) | **NEUF** | seulement si la campagne apporte des héros | `commun/` + §5.5 | §5.5 |
| D9 | `data/cards_custom.json` | Second catalogue (anciennes cartes d'auteurs) | **CLAUDE** | ne pas utiliser pour un pack neuf | — | — |
| D10 | `data/arts_alternatifs.json`, `data/images_cartes.json`, `data/identites.json`, `data/palettes-heros.json` | Cosmétique (arts alternatifs, relevé des illustrations, couleurs de héros) | **CLAUDE** | non | — | — |

### 3.2 Moteur : scripts Python (`src/cards/pack/<pack>/`)

`<pack>` est la clé du pack dans `cards.json` : un nom court en minuscules et soulignés (`web_of_deceit`, `mts`,
`skrull_menace`). C'est aussi le nom du dossier.

| # | Chemin | Rôle | Livraison | Obligatoire | Détail |
|---|---|---|---|---|---|
| M1 | `src/cards/pack/<pack>/__init__.py` | Fonctions partagées par plusieurs sets du pack (`from cards.pack import *` en tête) | **NEUF** | option | §6.1 |
| M2 | `src/cards/pack/<pack>/<set_nettoyé>/__init__.py` | **Obligatoire dans chaque dossier de set** : sans lui, les cartes du set n'ont aucune capacité, sans erreur | **NEUF** | **oui** | §6.1 |
| M3 | `src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py` | Le script d'**une face** qui a une capacité imprimée | **NEUF** | une par face à capacité | §6 |
| M4 | `src/cards/pack/<pack>/campaign.py` | **La logique de carnet** : `CampaignSetup(niveau)` (mise en place) + `Collect...` (carnet sortant) | **NEUF** | **oui** | §7 |
| M5 | `src/cards/pack/<pack>/<scénario>/<id_1A>.py` | La face **1A du complot principal** de chaque scénario *appelle* `*CampaignSetup(niveau)` : c'est ce qui branche le carnet | **NEUF** | **oui**, un par scénario (sauf le 1er si rien à appliquer) | §7.3 |
| M6 | `src/game/card/face/card_face.py` | Listes blanches de traits et de compteurs | **CLAUDE** → tu écris tes besoins dans `BESOINS-MOTEUR.md` | — | §4.5 |
| M7 | `src/game/**`, `src/engine/**` | Le moteur lui-même | **CLAUDE** | jamais toi | — |

### 3.3 Registre, textes, interface

| # | Chemin | Rôle | Livraison | Obligatoire | Détail |
|---|---|---|---|---|---|
| R1 | `tools/prefixes_fanmade.json` | Registre des préfixes de `card_id` fan-made (2 lettres) | **FRAGMENT** `integration/tools/prefixes.<pack>.fragment.json` | oui si fan-made | §4.4 |
| T1 | `ui-app/src/board/textes-fr-fanmade.ts` | **Le texte français de chaque carte fan-made** (seul français que le joueur verra dessus) | **FRAGMENT** `integration/textes-fr/<pack>.fragment.txt` (lignes `'id': "texte",`) | oui si fan-made | §10.3 |
| T2 | `public/js/traduction/textes-fr-fanmade.js` | Copie générée du précédent | **CLAUDE** (généré) | — | §10.3 |
| T3 | `public/js/prepare/mechants-info.js` | Mini-biographie du vilain (survol dans le choix du méchant) | **FRAGMENT** `integration/public/js/prepare/mechants-info.fragment.js` | option | §10.5 |
| T4 | `public/js/prepare/heros-info.js` | Biographie d'un héros | **FRAGMENT** | seulement pour un héros | §10.5 |
| T5 | `ui-app/src/board/dico-en.ts`, `public/js/prepare/dico-en.js` | Dictionnaire français → anglais des chaînes de l'interface | **CLAUDE** | — | §10.4 |
| T6 | `public/js/deckbuilder/regles.js` (`SETS_RESERVES_A_LA_CAMPAGNE`) | Cartes qui ne peuvent entrer dans un deck que par la campagne (cartes de campagne) | **CLAUDE** → signale-le dans `BESOINS-MOTEUR.md` | si la campagne a des cartes « réservées » | §14 |
| T7 | `public/campagne.html`, `public/js/campagne/*.js`, `ui-app/src/board/campagne/*` | Écran des campagnes et panneau de récompenses | **CLAUDE** | non | §9 |
| T8 | `src/engine/device/web/server/server_campagne.py` | Routes de campagne | **CLAUDE** | non | §9 |

### 3.4 Images

Toutes ces images sont **fournies par l'utilisateur** (scans, PDF de l'auteur). Tu ne les produis pas : tu
livres **`integration/images.md`**, un tableau `card_id → fichier source → orientation → remarque`, et la liste
des pages de livret attendues.

| # | Chemin | Rôle | Format | Obligatoire | Détail |
|---|---|---|---|---|---|
| I1 | `assets/pics/<card_id>.<jpg\|png\|webp>` | L'image de chaque face de carte. L'extension est **obligatoire**. | portrait ≈ 600×840 ; complots en **paysage** ≈ 840×600 | oui, une par `card_id` | §10.1 |
| I2 | `assets/vignettes/` | Miniatures de la table | généré par `tools/generer_vignettes.py` | **CLAUDE** | §10.1 |
| I3 | `assets/pics-fr/<card_id>.jpg` | Scans français officiels | seulement le contenu officiel | **CLAUDE** | — |
| I4 | `assets/textures/sets/<cle_extension>.webp` | L'image de la boîte (écran des campagnes, choix du méchant) | pochette | oui | §10.2 |
| I5 | `public/img/prepare/boites/<n>.webp` | Pochette recadrée de la boîte | générée par `outils/pochettes-boites.py` | **CLAUDE** | §10.2 |
| I6 | `public/stories/<code>/00-couverture.jpg` | Couverture du livret | carré 975×975 | option (repli : l'image de la boîte) | §10.6 |
| I7 | `public/stories/<code>/<NN>-<scénario>-<intro\|regles\|epilogue>-<n>.jpg` | Planches du livret, par scénario | carré 975×975 | option, mais l'écran les affiche | §10.6 |
| I8 | `public/stories/<code>/fr/<même nom>.jpg` | Pages du livret refaites en français | idem | option ; active seulement si `livret_fr: true` | §10.6 |

### 3.5 Preuves et documentation

| # | Chemin | Rôle | Livraison | Obligatoire | Détail |
|---|---|---|---|---|---|
| P1 | `tools/cas/<bloc>.py` | Les **cas de test de capacité** des cartes (un cas par capacité, avec preuve par substitution) | **NEUF** | **oui** pour chaque carte à capacité | §11.2 |
| P2 | `tools/epreuves_campagnes.py` | Les **épreuves de boucle de campagne** (partie 1 gagnée → carnet → partie 2) | **FRAGMENT** `integration/tools/epreuves.<code>.fragment.py` (`EPREUVES += [...]`) | **oui** | §11.3 |
| P3 | `tools/test_capacites.py` | Le harnais (il découvre `tools/cas/*.py` tout seul) | **CLAUDE** | — | §11.2 |
| P4 | `ui-check/tests/campagne-<code>.spec.ts` | Test d'écran Playwright | **CLAUDE** | non | — |
| P5 | `docs/packs/<code>/` | Dossier de conception : relevé des cartes, livret FR, décisions | **NEUF** | option | §12 |
| P6 | `docs/packs/<code>/GABARITS.md` | Un gabarit `PROCESSUS-CARTE` par carte, preuves réelles | **NEUF** | **oui** | §11.1 |

### 3.6 Le strict minimum pour qu'une campagne apparaisse et se joue

Dans l'ordre : D1 (cartes) → D3/D4/D5 (scénarios, sets) → D2 (index) → D6 (campagne) → I1 (images) → M2/M3
(scripts) → M4+M5 (carnet) → T1 (français) → P1/P2 (preuves). Sans D2, la campagne n'apparaît nulle part ; sans
D6, elle n'est pas une campagne (juste des scénarios isolés) ; sans M4/M5, le carnet est ignoré **en silence**.

### 3.7 Comment une campagne apparaît dans le jeu : ce qui est lu automatiquement

* `/list_campagnes_definies` lit **tous** les `data/campagnes/*.json` et les trie par le numéro de
  `cle_extension` (« 21. The Mad Titan's Shadow » → 21). Ajouter un fichier suffit : rien à enregistrer ailleurs.
* L'écran charge ensuite `catalog.scenariosForExtension(cle_extension)` : il cherche **dans `sets_info.json` la
  clé exactement égale** à `cle_extension` et en lit la liste `scenarios`. Une clé qui diffère d'un seul
  caractère → « scénario introuvable dans le catalogue ».
* Le scénario réel lancé est `data/scenarios/<id>.json`, ou `<id>_expert.json` si la campagne est experte **et**
  que ce fichier existe.
* `tools/cas/*.py` est découvert par un `glob` : déposer le fichier suffit.
* L'image de la boîte est `/sets/<cle_extension>` → `assets/textures/sets/<cle_extension>.webp`.
