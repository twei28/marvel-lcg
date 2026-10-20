---

## 13. Les modèles : deux campagnes complètes, fichier par fichier

Le zip contient, dans `modeles/`, **deux campagnes réelles déjà intégrées et jouées**, reconstituées **dans le
format exact d'une livraison** (§12) : tu y trouves ce que tu dois produire, au même endroit, avec les mêmes noms.
Ouvre-les **avant** d'écrire ta première carte.

| Dossier du zip | Campagne | Pourquoi ce modèle |
|---|---|---|
| `modeles/A-officielle-the-mad-titans-shadow/` | **The Mad Titan's Shadow** (officielle, 5 scénarios) | une campagne **officielle** avec **collecteur** : tout est relevé par le moteur ; le plus simple à imiter |
| `modeles/B-maison-web-of-deceit/` | **La Toile du Mensonge / Web of Deceit** (fan-made, 5 scénarios) | une campagne **maison** : préfixe `wd`, auteur (`custom`), sets modulaires fan-made, récompenses **choisies par le joueur** (arbres de talents) |
| `modeles/C-livraison-exemple-hunting-season/` | **Hunting Season** (fan-made, 5 scénarios) | la **vraie livraison d'une autre IA** (ce que Claude a reçu, avec ses brouillons et ses points ouverts) |
| `modeles/D-patrons-de-campaign-py/` | les **douze** `campaign.py` du jeu | un motif pour chaque mécanique (§7.8) |

Chaque `modeles/A-…` et `modeles/B-…` contient : `livraison/` (l'arborescence à produire), `images-exemples/` (quelques
vraies images et pages de livret, pour fixer les formats) et `README.md`.

### 13.1 Modèle A — The Mad Titan's Shadow (officielle)

{{INVENTAIRE:mts|mts|officiel}}

**Ce qu'il faut y voir :**

* **`data/campagnes/mts.json`** — chaque scénario déclare des champs `auto` **sans `detection`** (`Campaign Pool:
  Cosmo`…) : ils sont relevés par `CollectMTS`. Les **PV restants** sont déclarés en `victoire_commune_expert`
  avec le détecteur `pv_restants`. Le dernier scénario porte `final: true` et une `defaite` (`partie_perdue`,
  `expert_seulement`).
* **`src/cards/pack/mts/campaign.py`** — `InPool` / `LogSet` (lecture d'une clé), les briques `PutIntoPlayIfPool`,
  `ShuffleIntoEncounterIfPool`, `EachPlayerShufflesCopyIfPool` (application), `CollectMTS` (relevé),
  `CampaignSetup(level)` (assemblage par niveau). **Les clés écrites par `CollectMTS` sont celles que lit
  `CampaignSetup`** : vérifie-le à la main sur la table `CARNET-CLES.md` de ce modèle.
* **Les faces 1A** (`ebony_maw/21074a.py`, `the_tower_defense/21098a.py`, `thanos/…`, `hela/…`, `loki/…`) appellent
  `*CampaignSetup(n)` avec **n = numéro du scénario**.
* **Les cartes de campagne** (`set_name` « The Mad Titan's Shadow Campaign », classe `Campaign;Basic`) : Shawarma,
  System Shock (une obligation), Norn Stone, Odin… sont **générées au carnet**, pas dans un deck enregistré.
* **Les épreuves** (`tools/epreuves.mts.fragment.py`) : une par récompense, avec son **témoin** (sans carnet).

### 13.2 Modèle B — Web of Deceit (maison)

{{INVENTAIRE:web_of_deceit|web_of_deceit}}

**Ce qu'il faut y voir :**

* **Un pack complet avec un préfixe** : `wd001a`… `wd165`, `custom: "Ripper3"` sur chaque carte, entrée
  `120. Custom (Web of Deceit)` dans `sets_info`, entrée `wd` dans `prefixes_fanmade.json`.
* **Les sets réutilisés plutôt que recopiés** : *Power Drain II* est le set officiel *Power Drain* plus une carte :
  six **`ability_link`** à la place de six scripts (même fidélité que le moteur officiel). *Standard III* est une
  réimpression : **rien à créer**. **Avant d'écrire un script, cherche si la carte existe déjà dans le jeu.**
* **Une mécanique de livret que le moteur ne connaissait pas** — les **arbres de talents** (chaque joueur, après
  chaque scénario gagné, ajoute une carte de son arbre à son deck) — **résolue sans toucher au moteur** :
  des champs `type: "choix"`, `obligatoire: true`, `parJoueur: true`, dont les `options` sont les cartes du palier,
  et **un seul** `campaign.py` de 45 lignes qui **génère dans le deck de chaque joueur** les cartes notées au
  carnet (`ChaqueJoueurRetrouveSesTalents`, appelée par **chaque** face 1A). **Écart assumé et écrit** : l'arbre ne
  s'affiche pas comme un arbre (le joueur voit la liste de son palier). **C'est le bon réflexe quand une
  mécanique inédite peut se ramener à un mécanisme existant : on l'écrit, on n'invente pas.**
* **Un vilain qui se retourne au lieu d'être vaincu** (Shocker), des
  environnements mis de côté qui entrent en jeu par un effet (`set_aside` : « Vote for Fisk », « The Great Web »).
* **Ce que ce modèle n'a PAS (et qu'il faut avoir)** : **aucun texte français** (`textes-fr-fanmade.ts` ne contient
  aucune entrée `wd…`) ; **pas de collecteur** (donc pas d'estampille à tester) ; la `custom` y est bien.

Le **journal de portage** complet (`annexes/G-journal-portage-web-of-deceit.md`, 1 500 lignes) est le meilleur
récit de ce qu'une campagne maison demande : inventaire du Drive, croisement avec l'existant, scénario par
scénario, **trois écarts assumés** par lot, mesures. Lis au moins les §7 à §12 et §14.

### 13.3 Modèle C — Hunting Season : la vraie livraison d'une IA

{{INVENTAIRE:hunting_season|hunting_season}}

Le dossier `modeles/C-livraison-exemple-hunting-season/` contient ce que Claude a **reçu** de l'IA de Nugget :

* `LIRE_D_ABORD.md` — **l'état réel du dossier** (« les 226 cartes physiques sont représentées par 239 entrées JSON :
  les dix complots principaux ont deux faces et les trois cartes de vilain Lizard aussi »), la liste des fichiers,
  et la phrase clé : « *Ce pack ne doit pas être déclaré jouable tant que ces points sont ouverts.* »
* `PROMPT_POUR_CLAUDE.md` — l'instruction de reprise (ne pas réutiliser aveuglément d'anciens identifiants ; ne pas
  coder à la place des mots-clés lus dans `desc` ; **ne pas corriger en silence une carte dont le texte se contredit**).
* `SPECIFICATIONS.md` — les **règles spéciales** de la campagne (expérience, Lodge, paquet Trap, vilain recto-verso…).
* `POINTS_OUVERTS.md` — les décisions à prendre, chacune avec l'image de la carte concernée.
* `VERIFICATION.json` — les contrôles **statiques** faits, **sans simulation du jeu**, et le disent.
* `integration/` — les fragments de données et les scripts, **partiels et honnêtes** (`A_FAIRE_CLAUDE`).
* `reference/` — `campaign_log_contract.json` (les clés du carnet et les besoins d'interface),
  `campaign_rules.py` (le calcul pur de l'expérience, des achats, des soins : **un modèle de travail, pas une extension
  autorisée du schéma natif**), `card_manifest.json` (chaque carte : id, source, état du script).

**Ce que cette livraison a bien fait** : inventaire exact, fragments sans écrasement, un point ouvert par
décision, calcul des règles **séparé** du moteur. **Ce qu'il fallait faire de plus** (et que ce kit exige) : la table
des clés du carnet **écrite/lue** (§7.10), l'appel `*CampaignSetup(n)` sur chaque 1A, les cas de test et les
épreuves de boucle, le texte français, un `custom` sur **chaque** carte. Constat du 20/10/2026 : **les 239
cartes de Hunting Season n'ont pas de clé `custom`** dans `cards.json` : n'imite pas cet oubli.

### 13.4 Les douze `campaign.py` (`modeles/D-patrons-de-campaign-py/`)

| Campagne | Fichier | Lignes | Style | Ce qu'on y apprend |
|---|---|---|---|---|
| The Rise of Red Skull | `trors/campaign.py` | 100 | niveaux croissants, **sans collecteur** | `CampaignSetup(level, campaigns=…)` ; détecteurs côté JSON |
| Sinister Motives | `sm/campaign.py` | 202 | sans collecteur ; piste de réputation | total **cumulatif**, **tirage** aux paliers, deck **requis** |
| The Mad Titan's Shadow | `mts/campaign.py` | 233 | **collecteur** ; clés « pool » | **le modèle**, et la source de `WriteCampaignLogAtGameOver` |
| Mutant Genesis | `mut_gen/campaign.py` | 234 | collecteur ; **rôle** choisi en jeu | alliés captifs, rôle persistant |
| NeXt Evolution | `next_evol/campaign.py` | 271 | collecteur ; environnements gagnés | effets propres à chaque niveau |
| Age of Apocalypse | `aoa/campaign_setup.py` | 178 | collecteur ; **missions** | une mission jamais deux fois ; défaite par clé absente |
| Galaxy's Most Wanted | `gmw/campaign.py` | 388 | collecteur ; **marché** d'unités | solde, estampille explicite (`scenario_id=`) |
| Agents of S.H.I.E.L.D. | `aos/campaign.py` | 597 | collecteur ; **enquête à secret serveur** | `CampaignLog.SetStr` en cours de partie, `WhenCampaignSetupAfterMulligans` |
| Fear No Evil | `fne/campaign.py` | 247 | collecteur ; **ordre libre** | carnet par affaire, retrait de cartes du deck |
| Hunting Season | `hunting_season/campaign.py` | 377 | collecteur ; **expérience**, Lodge | défaite qui continue la campagne, dépenses de mise en place |
| Skrull Menace | `skrull_menace/campaign.py` | 682 | collecteur ; **zone de coopération** | tableau de progression, tirage d'Élites, ensembles alternatifs |
| Web of Deceit | `web_of_deceit/campaign.py` | 45 | **sans collecteur**, gains **choisis** | le minimum viable d'une campagne maison |

### 13.5 Le brief que Claude donne à ses propres agents (Skrull Menace) — ce que tu dois savoir aussi

`annexes/K-skrull-menace-brief-agents.md` est le brief que Claude a rédigé pour des agents travaillant en parallèle sur
un coffret : les **recettes de rangement des images**, le **vocabulaire français**, les **pièges déjà payés**, le
**format d'un livrable de lot**. `annexes/K-skrull-menace-campagne-mode.md` est le tableau **règle par règle du livret
→ implémentation → cas de test** d'une campagne complète : **le modèle de la preuve** (chaque règle du livret a sa
ligne, son fichier et son cas qui la prouve).
