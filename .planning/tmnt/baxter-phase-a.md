# Baxter Stockman v3 (TMNT Villains / Modulars, Inkwire) : compte rendu du scénario

Branche `tmnt-baxter`, 16/10/2026. Préfixe de card_id `tx`, pack `baxter_stockman`, set n°195 (PROVISOIRE : à
renuméroter à la fusion si collision avec les sets des six autres agents). Source : zip « TMNT Enemies / Baxter
Stockman v3 » (42 PNG lus carte par carte ; les exemplaires multiples ne diffèrent que par leur numéro de bandeau,
comparaison pixel à pixel). Tout est en français sauf les noms propres et les traits (conventions du dépôt).

## Ce qui a été livré

| Quoi | Où |
|---|---|
| 19 cartes `tx001`-`tx018` (+ `tx004a/b`) | `data/cards.json` (pack `baxter_stockman`), checksum recalculé |
| Carte d'état **Dazed** (6e état du moteur) | `data/cards.json` (pack `status`, card_id `dazed`), `src/cards/pack/status/dazed.py`, texture `assets/textures/dazed.webp` |
| 20 modules de cartes | `src/cards/pack/baxter_stockman/` (flat, comme `spot`) |
| Scénario normal et expert | `data/scenarios/baxter_stockman.json`, `baxter_stockman_expert.json` |
| 4 sets de rencontre | `data/encounter_sets/baxters_lab.json` (18), `cyber_swarm.json` (6), `high_speed.json` (5), `security_protocol.json` (7) |
| Index des packs | `data/sets_info.json` (`195. Custom (Baxter Stockman)`), `tools/prefixes_fanmade.json` (`tx`) |
| Images (JPEG 615 px) | `assets/pics/` (gitignoré) + copie versionnée `.planning/tmnt/pics-baxter/` ; recette `tools/importer_images_baxter_stockman.py` |
| Texte français | `ui-app/src/board/textes-fr-fanmade.ts` (19 entrées) + copie publique régénérée (`node ui-app/outils/generer-traduction-public.mjs`), `compteurs-fr.ts` (câble, bouclier, mutagène), trait `FLY` → MOUCHE (`traits_fr_maison.json`, `generer_traits_fr.py`) |
| Bios | `public/js/prepare/mechants-info.js` (`tx001`) et `vilains-bios.md` |
| Fiches mots-clés | `docs/reference/mots-cles/` : `dazed.md`, `replicate.md`, `all-purpose-counter.md` ; mises à jour de `swarm.md`, `cloaked.md`, `special.md`, `README.md` |
| Recettes | `docs/reference/RECETTES-MOTEUR.md` §7novodecies |
| Cas | `tools/cas/tmnt_baxter.py` : 112 cas `[baxter]` + 23 cas `[dazed]` |
| Plateau | `ui-app/src/board/tmnt-baxter-plateau.test.ts` (11 cas), cas ajoutés à `effets-statuts.test.ts`, `mobile/etats.test.ts`, `compteurs-fr.test.ts` |
| Gabarits PROCESSUS-CARTE | `.planning/tmnt/baxter-gabarits-processus-carte.md` |
| Questions en attente | `.planning/tmnt/baxter-questions.md` (Q1 à Q5) |

## Lecture des scans, décisions

- **Le « Special » de la manigance 1B est une capacité NOMMÉE** (« *Replicate* — Special : ... »), résolue par le joueur : fiche
  `replicate.md`. « all-purpose counter » : FAQ officielle MC4DB (le type est celui de la carte porteuse) → swarm / ooze / cable /
  shield par sbire (`COMPTEUR_DU_SBIRE`).
- **Dazed** : toutes les règles viennent de l'encart `Dazed Rules Insert.png` ; fiche `dazed.md`. Cloaked et Dazed résolvent
  **simultanément** : `cloaked.py` s'efface devant un Dazed du même porteur, `dazed.py` résout le lot (preuve par mutation).
- **Étoiles imprimées** : PV / ATQ / MNG ★ des essaims (tx007, tx012, tx013) = `desc` « 0 » + valeurs dynamiques (fiche `swarm.md`) ;
  le disque orange du coin = PV (vérifié contre `01167`, déjà noté) ; les icônes rouges du coin = boost.
- **Icônes vérifiées par découpe contre des cartes officielles** (IoU des silhouettes après redimensionnement 48 x 48, un bruit
  aléatoire donne ~0,18) : Crise `01108` / `tx010` 0,93 et `tx018` 0,92 ; Accélération `01109` / `tx010` 0,86 ; icône de boost
  `01108` / `tx010` 0,72 et coin droit des fan-made (tournée de 90°) 0,69. Aucune icône de ressource sur ces cartes.
- **Homonyme** : `td015` « * Baxter Stockman » est le SBIRE némésis de Donatello ; `tx005` et `tx002` cherchent par card_id / type
  (cas dédié : Blaster attaché au vilain malgré `td015` en jeu).
- **Questions** : voir `baxter-questions.md` ; lectures provisoires marquées `TODO-QUESTION` : tx005 (étoile ATQ, aucun bonus),
  tx017 (plus de bouclier : vaincu normalement), tx016 (qui choisit : le joueur qui révèle), FLYBORG au singulier.

## Moteur partagé touché (minimal, additif)

`card_face.py` (traits `FLYBORG`/`FLY`, compteurs `cable`/`shield`/`ooze`, statut `Dazed`) ; **statut Dazed** :
`component/status.py`, `attribute/can_status.py` (`dazed`, `IsDazed`, `CanbeDazed`, `DiscardDazed`, `GainStatus` refuse un second,
`HasStatus`, `DiscardEachStatus`), `card_type/card_status.py`, `render/symbol.py`, `card_finder/checker.py` (`has_status`,
`canbe_status`), `ability/ability.py` (`ETATS`), `puzzle/puzzle.py` + `puzzle_.py` (`Puzzle.Daze`) ; **`cards/pack/status/cloaked.py`**
(3 garde-fous `pas_de_dazed`, comportement de Cloaked seul inchangé) ; **`tools/autoplay.py`** (`--deck a+b` pour deux joueurs,
joueur interrogé lu via `player_id`, option « Ask » retirée en multi, sans effet en solo) ; UI : `effets-statuts.ts` (+ `compter()`
qui oubliait le nouveau statut : NaN), `mobile/etats.ts`, `ScanCard.tsx`, `compteurs-fr.ts`, `textes-fr-fanmade.ts`,
`traits-fr.ts` + copies publiques régénérées.

## Preuves

- `tools/test_cards.py` : **6435 ok / 0 erreur** (avec toutes les cartes du dépôt chargées, moteur modifié compris).
- `tools/test_capacites.py` : **[baxter] 112 cas, [dazed] 23 cas, tous verts** (passe finale du 16/10/2026) ; **cas Cloaked existants**
  (`[cloaked]`, `tl015`, `tl016`, `td005`...) : 23/23 verts après la modification de `cloaked.py`.
- **Substitution** (`tools/substituer_pack.py .game-src 48000 tx`, empreinte du pack identique avant/après) : 18 cartes sur 19 avec au
  moins un cas rouge sans leur module ; `tx010` : module vide par construction (Hinder, Accélération, Crise, Boost sont des bases `desc`),
  prouvé par les cas `icones`, `Crisis` + témoin et menaces de départ. Les cas restés verts sont des témoins, des cas
  `nombres imprimes` (desc) ou des bases natives, listés carte par carte dans les gabarits. **Dazed** : module remplacé par un
  stub → 10 cas nominaux rouges sur 21 (les verts sont les témoins, la pose, la limite « un seul » portée par `can_status.py`) ;
  **mutations** : sans la priorité de Tough, le cas « Dazed posé avant Tough » tombe au rouge ; `cloaked.py` ramené à sa version
  d'origine → le cas de simultanéité sur les dégâts tombe au rouge (celui de l'attaque de base reste vert : l'ordre des deux
  cartes le fait passer par chance, assumé). Le cas « zéro dégât » reste vert sous mutation : le moteur n'envoie pas le message pour
  0 dégât, la condition `> 0` est redondante (gardée par sécurité).
- **`tools/verifier_appels_modules.py`** : OK pour `baxter_stockman` et `status` ; calibré : un module de test appelant
  `Faces.GainKeywordPermanently` le fait tomber (« n'existe pas »).
- **Autoplay** (`tools/autoplay.py`, pilote équilibré, `spider_man` ; deux joueurs : `spider_man+black_widow`) : 32 parties jouées
  de bout en bout (solo normal, solo expert, 2 joueurs normal, 2 joueurs expert, 8 chacune), **0 traceback**, aucune des erreurs
  `NameError|AttributeError|TypeError|KeyError|AssertionError` dans les 32 journaux. 0 victoire sur 32 : le pilote perd aussi
  contre le témoin Rhino (solo 0/8 en 6,9 rounds ; 2 joueurs 0/8 en 7,5 rounds) ; Baxter est plus rapide (3 à 4 rounds, menace 11 par
  joueur + Replicate + traîtrises à menace). 1 partie `bloquee` sur 32 (2 joueurs normal, graine 7) : Tenacity `01093`, défaut du
  pilote déjà documenté dans `autoplay.py`, sans rapport avec le scénario. Expert joué par `--vilains baxter_stockman_expert`
  (le mode `--difficultes expert` n'enlève que le premier stade).
- **Plateau** : `npx vitest run` (314 fichiers) : tout vert sauf `bulles-arts-alternatifs.test.ts` (2 cas), qui lit des
  arts alternatifs de `assets/pics/` absents de cette copie de travail (gitignorés) : sans rapport. `npx tsc --noEmit` vert. Les cas
  `effets-statuts` et `compteurs-fr` ont été vus ROUGES sans le correctif (le test de `compter()` a attrapé un `NaN` que le typage
  seul ne montrait pas à l'exécution) ; les cas d'attachement (Blaster, Swarm Superiority, Intruder Alert!) passent sans correctif :
  le plateau les dessinait déjà.

## Ce qui n'est PAS prouvé

- **Aucune partie jouée par un humain** : seul le pilote automatique (qui perd toujours) a joué. Équilibre du scénario non mesuré.
- Dazed + attaque **perforante** (encart : « 1 dégât perforant → 3 dégâts ») : aucun cas ; repose sur le comportement existant de Tough
  (défaussé avant les dégâts).
- Dazed sur un allié à **dégâts consécutifs** (encart) : aucun cas dédié.
- Coup Rapide de Roadkill Rodneys à l'entrée en jeu : base native `desc`, non mesurée en cas (`Puzzle.PutIntoPlay` ne déclenche pas
  l'attaque rapide).
- L'ordre exact Tough / Dazed / Cloaked quand plusieurs porteurs ont les trois : seules les combinaisons testées sont prouvées.
- Aucune batterie complète de `test_capacites.py` (règle de portée §6bis, ~34 min en parallèle) : seuls `test_cards.py`, les cas du
  pack, les cas Cloaked et les vérificateurs ci-dessus ont été relancés. À faire à la fusion, un fichier moteur partagé a changé.
- Première apparition de Baxter Stockman dans `mechants-info.js` (« Teenage Mutant Ninja Turtles #19 (1989) ») : écrite de mémoire,
  à vérifier.

## À faire à la fusion

1. Remplacer `standard` par `tmnt_standard` et `expert` par `tmnt_expert` dans `data/scenarios/baxter_stockman.json` et
   `baxter_stockman_expert.json` (ensembles habillés TMNT de l'autre agent, préfixe `te`), puis relancer l'autoplay.
2. Vérifier l'unicité du numéro de set 195 (`tools/verifier_prefixes.py`) et recalculer les checksums après fusion de `cards.json` /
   `sets_info.json` (`tools/recalculer_checksums.py`).
3. Fusionner les ajouts groupés aux fichiers partagés : `card_face.py` (listes TRAITS / COUNTER / STATUS), `textes-fr-fanmade.ts` (+ copie
   publique), `compteurs-fr.ts`, `mechants-info.js`, `vilains-bios.md`, `prefixes_fanmade.json`, `README.md` des mots-clés.
4. Relancer `ui-app/outils/generer-traduction-public.mjs` et la batterie complète de `test_capacites.py`.
