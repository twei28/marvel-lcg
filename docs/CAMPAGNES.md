# Mode campagne — état des lieux et suite du travail

Document de reprise, écrit le 07/08/2026. Il se suffit à lui-même : tu peux
l'ouvrir dans une session Claude Code neuve, au terminal, sans autre contexte.

La conception et l'historique détaillé sont dans
[`docs/superpowers/specs/2026-08-07-mode-campagne-design.md`](docs/superpowers/specs/2026-08-07-mode-campagne-design.md).
Ce fichier-ci est le mode d'emploi.

---

## 1. En deux mots

Le mode campagne enchaîne les scénarios d'une boîte dans l'ordre du livret. Ce
qu'on gagne dans un scénario (améliorations, alliés, compteurs) est enregistré
dans un **carnet de campagne** et rejoue automatiquement à la mise en place du
scénario suivant.

**Le moteur est câblé pour les six boîtes à récompenses**, mesuré par sonde
scénario par scénario (détail au §6). **Quatre ont en plus leur fichier
`data/campagnes/*.json` et sont jouables depuis l'écran** :

- L'Avènement de Crâne Rouge (`trors`)
- Intentions Sinistres (`sm`)
- The Mad Titan's Shadow (`mts`)
- La Genèse des Mutants (`mut_gen`), depuis le 10/8/2026

**Deux autres sont câblées côté moteur mais n'ont pas encore de fichier de
définition**, donc invisibles sur `/campagne.html` : NeXt Evolution
(`next_evol`) et Age of Apocalypse (`aoa`). C'est le travail décrit au §9, sur
le modèle de `mts.json` ou de `mut_gen.json`.

**Une clé fausse ne fait aucun bruit** (§5). Depuis le 10/8/2026,
`tools/verifier_campagnes.py` compare chaque clé déclarée aux chaînes du
moteur et refuse de se taire dessus. À lancer après toute écriture de
définition.

La septième boîte, Galaxy's Most Wanted (`gmw`), n'a aucune récompense codée
côté moteur : elle se joue en séquence pure, sans carnet. Rien à câbler pour
elle.

---

## 2. Lancer et tester

Le jeu tourne sous WSL, en Python 3.10 obligatoire.

Démarrer le serveur (ou double-cliquer `JOUER-SOLO.bat`) :

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && ~/marvel-work/python/bin/python3.10 launcher_fast.py"
```

Le jeu répond sur `http://127.0.0.1:2345`. L'écran des campagnes est sur
`/campagne.html`, et la tuile « Campagne » de `/prepare.html` y redirige.

Arrêter le serveur — noter les crochets, sans eux le motif tue le shell qui
lance la commande :

```bash
wsl.exe -e bash -lc "pkill -f 'launcher_[f]ast'"
```

Tests et vérification de types de l'interface du plateau :

```bash
cd ui-app && npx vitest run && npx tsc --noEmit
```

Construire et déployer le plateau après toute modification de `ui-app/` :

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions' && bash ui-app/deployer.sh"
```

Les fichiers de `public/` (HTML, JS, CSS non compilés) sont servis par lien
symbolique : un rechargement de page suffit, pas besoin de relancer le serveur.
Les fichiers Python du moteur, eux, exigent un redémarrage.

---

## 3. Où vit quoi

### Côté serveur (Python)

| Chemin | Rôle |
|---|---|
| `Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py` | Les sept routes HTTP de campagne |
| `Fusion/marvel-lcg-src/src/engine/device/web/server/server.py` | Y déclare `GameServerCampagne` dans la chaîne d'héritage |
| `Fusion/marvel-lcg-src/data/campagnes/*.json` | Une boîte-campagne décrite en données |
| `Fusion/marvel-lcg-src/campagnes/*.json` | Les campagnes du joueur (créé à la volée) |
| `Fusion/marvel-lcg-src/src/cards/pack/<code>/campaign.py` | Les récompenses, côté moteur |
| `Fusion/marvel-lcg-src/src/game/operate/campaign_logs.py` | Comment le moteur relit le carnet |
| `Fusion/marvel-lcg-src/.game/campaign_log_last.json` | Carnet SORTANT calculé par le moteur, écrasé à chaque fin de partie de campagne (clé de config `campaign_log_last_file`, voir §8) |

Routes : `/list_campagnes_definies`, `/get_campagne_definition?<code>`,
`/get_carnet_suggere`, `/list_campagnes`, `/get_campagne?<id>`,
`/save_campagne` (POST), `/delete_campagne` (POST).

`/get_carnet_suggere` rend le contenu de `campaign_log_last.json` : ce que le
moteur a lui-même relevé à la toute dernière fin de partie de campagne sur
cette place (le fichier est cloisonné par place, voir §8), plus `scenario`,
l'estampille du scénario qui a produit ces suggestions (dérivée du `set_name`
de la manigance principale active, voir `WriteCampaignLogAtGameOver` dans
`campaign.py`). Rien n'efface jamais ce fichier : si deux parties de
campagne, de deux boîtes différentes, s'enchaînent sur la même place, c'est
toujours la plus récente qui répond. `scenario` sert précisément à ça :
`preRemplir` (`ui-app/src/board/campagne/preremplissage.ts`) compare cette
estampille au scénario du contexte de campagne en cours et ignore les
suggestions EN BLOC si elles ne correspondent pas, plutôt que de les
présenter comme relevées par le jeu pour la mauvaise partie. Fichier absent
ou illisible : réponse 200 avec un carnet vide et `scenario: null`, jamais
une erreur.

### Écran des campagnes (JS non compilé)

| Chemin | Rôle |
|---|---|
| `Fusion/marvel-lcg-src/public/campagne.html` | La page |
| `Fusion/marvel-lcg-src/public/js/campagne/app.js` | Les trois vues : liste, création, scénario courant |
| `Fusion/marvel-lcg-src/public/js/campagne/api-campagne.js` | Client des routes |
| `Fusion/marvel-lcg-src/public/js/campagne/brouillon.js` | Passe-plat vers l'écran de préparation pour choisir l'équipe |
| `Fusion/marvel-lcg-src/public/css/campagne/campagne.css` | Style |
| `Fusion/marvel-lcg-src/public/stories/<code>/*.jpg` | Scans du livret, nommés par rôle |

### Panneau de récompenses (React, dans le plateau)

| Chemin | Rôle |
|---|---|
| `ui-app/src/board/campagne/detecteurs.ts` | Ce que le moteur sait déduire tout seul |
| `ui-app/src/board/campagne/detecteurs.test.ts` | 40 tests, bâtis sur des descripteurs capturés |
| `ui-app/src/board/campagne/contexte.ts` | Le plateau apprend qu'il joue une campagne |
| `ui-app/src/board/campagne/preremplissage.ts` | D'où vient chaque valeur pré-remplie |
| `ui-app/src/board/campagne/PanneauRecompenses.tsx` | Le panneau de fin de scénario |
| `ui-app/src/board/board.css` | Style du panneau, en fin de fichier |

---

## 4. Comment ça s'enchaîne

1. `/campagne.html` — le joueur crée une campagne (boîte, nom, difficulté,
   nombre de héros), puis part choisir son équipe sur `/prepare.html?campagne`.
   L'écran de préparation se réduit alors à deux étapes et rend l'équipe par un
   brouillon en `localStorage`.
2. La campagne est écrite sur le serveur : équipe figée, `termines: []`,
   `carnet: {}`.
3. Lancer un scénario pose `localStorage['mc-campagne-partie'] = {id, scenario}`
   puis appelle le `launch()` habituel avec `rules: ["mode_campaign", …]`, les
   sets modulaires du fichier de scénario, et `campaign_log = carnet`.
4. Le moteur applique le carnet à la mise en place (`Message.WhenCampaignSetup`).
5. À la victoire, `PanneauRecompenses` lit la clé, charge la campagne et sa
   définition, puis pré-remplit chaque champ dans l'ordre du §5 : d'abord ce
   que le moteur a lui-même relevé sur `/get_carnet_suggere`, puis ce que les
   détecteurs déduisent du descripteur de monde, puis la valeur déjà présente
   au carnet. Le joueur choisit le reste, et l'écran écrit `carnet` et
   `termines` puis efface la clé.
6. Retour à `/campagne.html`, qui affiche le scénario suivant.

Une **défaite** n'écrit rien : le livret dit qu'on rejoue sans pénalité.

---

## 5. Le format d'un fichier de campagne

`data/campagnes/<code>.json`. Prendre `trors.json` (simple) ou `sm.json`
(complet, avec `victoire_commune`) comme modèle.

```jsonc
{
  "code": "trors",
  "cle_extension": "4. The Rise of Red Skull",   // doit matcher data/sets_info.json
  "nom": "L'Avènement de Crâne Rouge",
  "resume": "…",
  "pages_regles": ["00-campagne-regles-1.jpg"],
  "scenarios": [
    {
      "id": "crossbones",          // = nom du fichier data/scenarios/<id>.json
      "numero": 1,
      "nom": "Crossbones",
      "nom_fr": "Crossbones",
      "resume": "…",               // récit, écrit pour le jeu, en français
      "enjeu": "…",                // ce que la victoire rapportera
      "final": true,               // sur le dernier seulement
      "pages": { "intro": [...], "regles": [...], "epilogue": [...] },
      "victoire": [ /* champs */ ]
    }
  ],
  "victoire_commune": [ /* présentés à chaque victoire sauf la dernière */ ],
  "victoire_commune_expert": [ /* idem, en campagne experte seulement */ ]
}
```

Un **champ de victoire** :

```jsonc
{
  "cle": "Tech Upgrade",       // LA CLÉ QUE LE MOTEUR RELIT — à copier telle quelle
  "parJoueur": true,           // devient « Player N <cle> »
  "type": "auto",              // "auto" = relevé par le jeu | "choix" = décision du joueur
  "format": "liste",           // "liste" (ids joints par « ; ») | "int"
  "obligatoire": true,         // choix : bloque la validation tant qu'il manque
  "detection": "cartes_en_jeu",  // facultatif, voir plus bas
  "parametres": { "compteur": "delay" },
  "condition": "complot_absent",
  "libelle": "Amélioration technologique",
  "aide": "…",
  "options": ["04155", "04156"] // affichées en cartes cliquables
}
```

Les clés **doivent** être copiées depuis `src/game/operate/campaign_logs.py` et
depuis le `campaign.py` du pack. Une clé approximative ne lève aucune erreur :
le moteur lit simplement une valeur vide, et la récompense disparaît en silence.

`detection` est **facultatif pour les boîtes dotées d'un collecteur côté
moteur** (`mts`, `mut_gen`, `next_evol`, `aoa` : voir `WriteCampaignLogAtGameOver`
au §6). Ces boîtes relèvent elles-mêmes leur carnet sortant à la fin de partie
et l'exposent sur `/get_carnet_suggere` ; le panneau le prend en source
prioritaire (§3, §4) et n'a besoin d'un détecteur que pour les clés que le
moteur ne fournit pas. `trors` et `sm`, qui n'ont pas ce collecteur, restent
entièrement dépendantes de `detection`.

### Les détecteurs disponibles

Tous génériques, aucun n'a de boîte en dur. Définis dans
`ui-app/src/board/campagne/detecteurs.ts`.

| `detection` | Rend | Paramètres |
|---|---|---|
| `cartes_en_jeu` | Parmi `options`, celles entrées en jeu | — |
| `compteur_manigance` | Compteur sur la manigance principale | `compteur` |
| `cartes_du_joueur` | Parmi `options`, celles que ce joueur possède | — |
| `joueurs_engages` | Indices des joueurs encore engagés | — |
| `cartes_sous_complot` | Cartes posées sous un complot en jeu | `complot`, `type` |
| `pv_restants` | PV plafonnés aux PV imprimés | — |
| `cartes_en_pile_victoire` | Parmi `options`, celles dans la pile de victoire | — |
| `cartes_dans_zone` | Parmi `options`, celles dans une zone du monde | `zone` |
| `compter_trait` | Nombre de cartes portant un trait, dans les decks | `trait` |

Condition disponible : `complot_absent` (paramètre `complot`). Une condition
inconnue **masque** le champ — on n'accorde pas une récompense dont on ne sait
pas évaluer la règle.

Faits mesurés, à ne pas re-deviner :

- les COMPTEURS sortent en `info.c_<nom>` (`c_delay`), les JETONS en
  `info.k_<nom>` (`k_threat`) ;
- les TRAITS sortent en `traits.t_<NOM>` (`t_SYMBIOTE`) ;
- une carte posée sous un complot est dans **la même zone** que lui, avec
  `bind_object_id` égal à l'`id` du complot ;
- les PV de l'identité sont `info.health` / `info.max_health` sur
  `players[i].area_hero[0]` ;
- le deck des Armes Expérimentales est un **deck additionnel**
  (`additional_decks`), pas une zone mise de côté.

---

## 6. Le câblage moteur, fait et mesuré

### Le mécanisme

Les récompenses de campagne d'un pack ne se déclenchent que si la **carte de
manigance principale 1A** du scénario appelle `CampaignSetup(niveau)` dans son
`GetAbilities()`. Sans cet appel, `Message.WhenCampaignSetup` n'a aucun
auditeur et le carnet est ignoré, en silence. Le module à importer est
`cards.pack.<code>.campaign` pour `mts`, `mut_gen` et `next_evol`, sauf `aoa`,
où c'est `cards.pack.aoa.campaign_setup`.

Voici un fichier câblé, `src/cards/pack/mts/ebony_maw/21074a.py` :

```python
from . import *
from cards.pack.mts.campaign import CampaignSetup

def GetAbilities() -> Sequence['Ability']:
    return [*CampaignSetup(1)]
```

Pour un scénario qui a déjà des capacités, on ajoute l'import et on **préfixe**
la liste retournée :

```python
from cards.pack.mts.campaign import CampaignSetup
# …
    return [
        *CampaignSetup(2),          # <- ajouté
        AbilityFactory.WhenGameBeginSetup(under_siege_game_start),
        AbilityFactory.WhenCardSetup("This", under_siege),
    ]
```

Le `niveau` est le **numéro du scénario dans la campagne**, de 1 à 5. Les
dix-huit scénarios qui manquaient cet appel (3 de `mts`, 5 de `mut_gen`, 5 de
`next_evol`, 5 de `aoa`) sont maintenant tous câblés, en plus des onze qui
l'étaient déjà (`sm` en entier, `trors` aux niveaux 2 à 5, `ebony_maw` et
`thanos` pour `mts`). `crossbones`, le scénario 1 de `trors`, n'appelle pas
`CampaignSetup` : voir plus bas pourquoi c'est volontaire, pas un oubli.
`gmw` reste hors de ce mécanisme : elle n'a pas de `campaign.py` à appeler.

### Le défaut trouvé en route : le carnet sortant ne s'écrivait jamais

`WriteCampaignLogAtGameOver`, la fonction commune aux quatre boîtes, appelait
`player.GetHero()` pour lire le nom du héros à consigner dans le carnet. Cette
méthode lève une `AssertionError` (au lieu de rendre `None`) dès que le joueur
est en forme Alter Ego, ce qui est l'état normal d'un joueur en fin de partie, puisque
la victoire ou la défaite ne force pas la forme Héros. L'assertion coupait
alors l'écriture du carnet en entier, silencieusement : en jeu réel comme sous
la sonde, `RELEASE=1` avale l'exception (`launcher_fast.py`), et rien ne
signalait que le carnet sortant restait vide. Les quatre boîtes câblées ce
jour-là étaient concernées.

Le correctif (commit `1cdcbba`) lit `identity.GetHeroFace()` à la place, qui
retrouve la face héros quelle que soit la forme active du joueur, avec son
propre garde puisqu'elle lève aussi si la carte n'a vraiment aucune face
héros. Une identité illisible ne coûte plus que sa propre clé, jamais le
fichier entier.

### Les mesures

Table complète, sonde `FIN_DE_PARTIE=1` (voir plus bas), un scénario par
niveau et par boîte :

| Boîte | Niv. | Scénario | Carnet entrant appliqué | Carnet sortant écrit |
|---|---|---|---|---|
| mts | 2 | the_tower_defense | oui (21181) | oui |
| mts | 4 | hela | oui (21188, 21185) | oui |
| mts | 5 | loki | oui (21139) | oui |
| mut_gen | 1 | sabretooth | minimal (Player 1 Role, pas d'erreur) | oui |
| mut_gen | 2 | project_wideawake | minimal (Player 1 Role, pas d'erreur) | oui |
| mut_gen | 3 | master_mold | oui (32089) | oui |
| mut_gen | 4 | mansion_attack | minimal (Player 1 Role, pas d'erreur) | oui |
| mut_gen | 5 | magneto | minimal (Player 1 Role, pas d'erreur) | oui |
| next_evol | 1 | morlock_siege | minimal (pas d'erreur) | oui |
| next_evol | 2 | on_the_run | oui (Campaign Pool: Team Assembled) | oui |
| next_evol | 3 | juggernaut | oui (Team Assembled, Geared Up) | oui |
| next_evol | 4 | mister_sinister | oui (Team Assembled) | oui |
| next_evol | 5 | stryfe | oui (Team Assembled) | oui |
| aoa | 1 | unus | minimal (pas d'erreur) | oui |
| aoa | 2 | four_horsemen | oui (Panicked Refugees) | oui |
| aoa | 3 | apocalypse | minimal (pas d'erreur) | oui |
| aoa | 4 | dark_beast | minimal (pas d'erreur) | oui |
| aoa | 5 | en_sabah_nur | minimal (pas d'erreur) | oui |

Le critère minimal (pas d'erreur, carnet sortant présent) distingue câblé de
non câblé, mais pas bon niveau de mauvais niveau : `WriteCampaignLogAtGameOver`
tourne à tous les niveaux d'une même boîte. Pour `mts` et `mut_gen`, la lecture
directe de `campaign.py` confirme que le bon bloc `if (level == N)` s'exécute
à chaque niveau. Pour `next_evol` et `aoa`, la sonde a en plus prouvé un effet
**propre** au niveau, visible dans le descripteur de monde :

- `next_evol` niveau 2 (`on_the_run`) : le statut Tough apparaît sur le vilain
  seulement avec un environnement au carnet (`GiveEnemiesToughIfEnvEarned`).
- `next_evol` niveau 3 (`juggernaut`) : `c_momentum` sur Juggernaut passe de 1
  (base carte) à 3 avec deux environnements en carnet, delta exact
  (`JuggernautMomentumCounters`).
- `next_evol` niveaux 4 et 5 : le seuil de menace de la manigance côté joueur
  augmente de 1 par environnement × joueur, conforme à
  `TeleportedAwaySetup` / `StryfesGraspThreat`.
- `next_evol` niveau 1 est câblé, mais **sa partie commune ne contient pas de
  bloc `if (level == 1)`** : `CampaignSetup(1)` exécute seulement
  `PutEarnedEnvironmentsIntoPlay`, `ChooseCampaignPlayerSideScheme` et
  l'écriture du carnet sortant, qui tournent à tous les niveaux. C'est
  l'inverse de ce que ce document affirmait avant ce chantier : le niveau 1
  n'était pas dispensé de câblage, il devait l'être comme les autres, il n'a
  simplement aucun effet qui lui soit propre à mesurer.
- `aoa` niveau 5 (`en_sabah_nur`) : la mission est forcée sur « Protect the
  Professor » (carte 45170a en jeu), au lieu d'un tirage aléatoire.
- `aoa` a aussi une branche `if (level >= 2)`, gardée par `Worlds.IsExpert`,
  qui n'est active qu'en campagne experte. Elle a été mesurée sur la variante
  `four_horsemen_expert` : avec `Player 1 Remaining hit points` au carnet, les
  PV de fin de mise en place remontent de 5 à 11 (delta +6), un écart absent
  des deux témoins (même scénario sans carnet, et variante standard avec
  carnet). La preuve directe est brouillée par une capacité compagnon de la
  même branche, qui offre un soin optionnel que le pilote automatique de la
  sonde accepte toujours ; l'écart entre témoins reste la preuve que le carnet
  est bien lu et appliqué. Les niveaux `apocalypse`, `dark_beast` et
  `en_sabah_nur` partagent le même code que `four_horsemen_expert` pour cette
  branche, par lecture directe, sans mesure indépendante par scénario.

**Pourquoi `next_evol` niveau 1 est câblé et `trors` niveau 1 ne l'est pas.**
Les deux cas se ressemblent : dans les deux boîtes, le premier scénario d'une
campagne ne peut par nature avoir aucun carnet entrant à appliquer, puisque
rien n'a encore été gagné. La différence tient à ce que fait la partie commune
de `CampaignSetup` en dehors de la lecture du carnet entrant. Chez `next_evol`,
elle écrit aussi le carnet **sortant** (`WriteCampaignLogAtGameOver`, voir plus
haut), et ce carnet doit exister dès la fin du scénario 1 pour que le scénario
2 ait quelque chose à lire : câbler le niveau 1 est donc nécessaire, même sans
rien à appliquer en entrée. Chez `trors`, `CampaignSetup` (`src/cards/pack/trors/campaign.py`) n'a pas de
collecteur de ce genre (c'est une boîte à détecteurs, pas à collecteur, comme
le rappelle le §5), et toutes ses branches sont gardées par `if level >= 2`
ou `if level >= 4` : au niveau 1, l'appel ne produirait strictement aucune
capacité. `crossbones` n'appelle donc pas `CampaignSetup`,
et c'est correct, pas un oubli.

### Vérifier — sans quoi ça ne compte pas

`tools/sonde_campagne.py` monte une partie complète sans navigateur, applique
un carnet, et rend le descripteur de monde. C'est l'outil qui a servi à établir
le tableau ci-dessus.

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  RAPPORT=/tmp/sonde.json \
  CAMPAIGN_LOG='{\"Player 1 Role\":\"Brawler\",\"Captive Allies\":\"32089\"}' \
  ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . master_mold captain_america 4801"
```

Puis chercher la carte attendue dans le rapport :

```bash
wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json
d=json.load(open('/tmp/sonde.json')); m=d.get('monde') or {}
print('erreurs:', d['erreurs'][:2])
for i,p in enumerate(m.get('players',[])):
    for z,v in p.items():
        if isinstance(v,list):
            for c in v:
                if isinstance(c,dict) and c.get('card_id')=='32089':
                    print('TROUVE en J%d.%s'%(i,z))
\""
```

Variables acceptées : `CAMPAIGN_LOG`, `RULES` (défaut `["mode_campaign"]`),
`PUZZLE` (liste de commandes `Puzzle.*` exécutées après la mise en place),
`RAPPORT`, et `FIN_DE_PARTIE` (si mise à `1`, la sonde force la fin de partie
après la mise en place via `SetGameOverByRule`, ce qui déclenche
`WriteCampaignLogAtGameOver`, et range le carnet sortant lu depuis
`campaign_log_last.json` sous la clé `carnet_sortant` du rapport). Sans cette
variable, comportement identique à avant : la sonde s'arrête à la mise en
place et ne mesure que le carnet entrant.

Le critère : la carte du carnet doit apparaître dans une zone du joueur ou du
monde, et, depuis `FIN_DE_PARTIE=1`, la clé attendue doit apparaître dans
`carnet_sortant`. Tant que ce n'est pas le cas, le scénario n'est pas câblé,
quoi que dise le code.

### Ensuite seulement, les fichiers de campagne

`mts.json` a été écrit sur ce modèle (commit `063172a`) : ses 9 clés viennent
de `CollectMTS`, vérifiées une par une contre `campaign.py`. `mut_gen.json`,
`next_evol.json` et `aoa.json` restent à écrire, voir §9.

Une fois une boîte câblée et vérifiée, écrire son `data/campagnes/<code>.json` :

1. Relever les clés exactes dans `src/cards/pack/<code>/campaign.py`.
2. Récupérer l'ordre des scénarios dans `data/sets_info.json`.
3. Les sets modulaires viennent du fichier de scénario, on ne les recopie pas.
4. Écrire les résumés français et les enjeux.
5. Déposer les scans du livret (§7) — facultatif, l'écran s'en passe.

`public/js/prepare/app.js` contient encore, en code mort mais **conservé
exprès**, un objet `CAMPAIGN_SCHEMAS` qui décrit les carnets des six boîtes.
C'est un point de départ utile, **mais il contient des erreurs avérées** :

- `trors` : il listait 04155-04158 (améliorations TECH) comme « armes
  expérimentales », au lieu de 04072-04075 ;
- `sm` : il libellait « Last Ones Standing » en « Sinistres Six vaincus », alors
  que le livret note les vilains **encore debout**, qui reviennent en sbires.

Vérifier chaque champ contre le `campaign.py` du pack et le livret, carte par
carte. Une fois les six boîtes portées, tout ce bloc peut disparaître, avec
`renderCampaignPath`, `renderCampaignStory`, `renderCampaignJournal` et
`campaignBoxes`.

---

### 6 bis. Ce que les livrets officiels ont appris (10/8/2026)

Les PDF officiels de FFG, livrets et carnets de campagne, sont sur le Bureau à
la racine de `Marvel LCG last try`. Ils sont **vectoriels**, donc lisibles au
texte et rendables en image. Les avoir change deux choses sur `mut_gen`, et
aucune n'était devinable depuis le code seul.

**Le carnet officiel a DEUX lignes d'alliés**, pas une : « Allies from
Abduction Protocols » au scénario 2, et « Allies under Rescue Captives or Find
the Prisoners » au scénario 3. Le moteur ne collectait qu'au niveau 2, donc les
alliés libérés au scénario 3 sous Rescue Captives (32173b, qui les rend à
chaque SENTINEL vaincu) étaient **perdus en silence**, alors que la mise en
place des scénarios 4 et 5 dit « each CAPTIVE ally recorded in the campaign log
may be shuffled into any player's deck ». `CollectMG` collecte désormais aux
niveaux 2 ET 3. Divergence assumée avec le moteur d'origine, prouvée à la
sonde avec son témoin : le scénario 3 relève l'allié, le 4 ne le relève pas.

**La colonne Jubilé s'ouvre au scénario 2**, pas au 3 : elle est libérée dans
`project_wideawake`. Le carnet la suit sur les scénarios 2, 3 et 4, avec une
case « retirée de la campagne » à partir du 3. Le fichier de campagne l'expose
maintenant ainsi.

**Leçon générale** : le `campaign.py` d'un pack dit ce que le moteur FAIT, le
carnet officiel dit ce que le livret DEMANDE. Les deux ne coïncident pas
toujours, et seul le second est l'autorité. Lire le carnet avant d'écrire une
définition, pas après.

## 7. Les scans du livret

`public/stories/<code>/`, nommés par rôle :

```
00-campagne-regles-1.jpg          règles générales de la campagne
00-campagne-expert-1.jpg          règles de la campagne experte
01-<scenario>-intro-1.jpg         planche de BD d'ouverture
01-<scenario>-regles-1.jpg        page de règles du scénario
01-<scenario>-epilogue-1.jpg      planche de BD de fin
```

Le fichier de campagne dit quelles pages chaque scénario affiche. Une planche
qui sert d'épilogue à un scénario ET d'intro au suivant n'est **pas
dupliquée** : les deux scénarios la référencent.

Seules `trors` et `sm` ont des scans. Sans scans, l'écran affiche le résumé
français seul — c'est prévu, rien ne casse.

---

## 8. Pièges

**Le déploiement écrase `public/`.** `ui-app/deployer.sh` traite
`~/marvel-work/fusion/marvel-lcg-src` comme la SOURCE de `public/js` et
`public/css`, et la `rsync --delete` par-dessus la copie Windows. Éditer
`public/js` côté Windows puis déployer **supprime le travail** — c'est arrivé
une fois sur ce chantier. Toute modification de `public/js` ou `public/css`
doit être poussée vers la copie WSL avant le déploiement suivant :

```bash
wsl.exe -e bash -lc "rsync -a '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src/public/js/' \$HOME/marvel-work/fusion/marvel-lcg-src/public/js/"
```

`outils/rejouer-patches-campagne.py` rejoue, de façon idempotente, les patches
« campagne » de `public/js/prepare/app.js` et `launcher.js` si le cas se
reproduit :

```bash
python outils/rejouer-patches-campagne.py "Fusion/marvel-lcg-src/public/js/prepare"
```

**Une clé de carnet fausse ne lève aucune erreur.** Le moteur lit une valeur
vide et la récompense disparaît sans bruit. D'où l'obligation de vérifier par
la sonde, jamais par la lecture du code seule.

**Le `pkill` du serveur doit utiliser les crochets** (`launcher_[f]ast`), sinon
le motif correspond à la ligne de commande du shell qui l'exécute et tue son
propre terminal.

**Les campagnes du joueur vivent hors de `.game`**, dans
`Fusion/marvel-lcg-src/campagnes/`, à côté de `replays/` — `.game` est
reconstruit à chaque lancement.

**La copie WSL peut écraser `src/`, pas seulement `public/`.** Une autre
session, sur ce même dépôt, entretient un outillage qui repasse la copie
`~/marvel-work/fusion/marvel-lcg-src` par-dessus la copie Windows. Ce chantier
a vu son câblage de `mts` et `mut_gen`, ainsi que la réparation du carnet,
effacés deux fois dans `src/cards/pack/` par ce mécanisme, alors qu'il ne
touchait pas `public/`. `src/cards/` n'est pas suivi par git, ce qui rend la
perte invisible tant qu'on ne compare pas les deux copies. Le remède est le
même que pour `public/js` : pousser toute modification de `src/` vers la
copie WSL après chaque commit, tant qu'une autre session peut tourner en
parallèle sur ce dépôt :

```bash
wsl.exe -e bash -lc "rsync -a '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src/src/' \$HOME/marvel-work/fusion/marvel-lcg-src/src/"
```

**Le moteur exécute `.game`, pas `src/`.** `launcher_fast.py` compile
`src/*.py` en `.game/*.pyc`, mais seulement si la source est plus récente que
le binaire compilé. Si la date d'un fichier de `src/` recule (restauration
depuis une sauvegarde, copie qui ne préserve pas les mtimes, horloge d'une
machine différente), la recompilation ne se déclenche plus jamais et le jeu
tourne indéfiniment sur l'ancien bytecode, sans le moindre message d'erreur.
Ce chantier a trouvé douze cartes dans ce cas, restées sur du code périmé
pendant plusieurs jours. Pour le détecter, recompiler chaque source en
mémoire et comparer au bytecode réellement chargé, plutôt que de se fier aux
dates de fichiers :

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && ~/marvel-work/python/bin/python3.10 launcher_fast.py --build-only"
```

Si les compteurs `compilés` restent obstinément bas alors qu'un fichier vient
d'être modifié, c'est le signe que sa date ne suffit plus à déclencher sa
recompilation.

**`updates[cle] = None` efface une entrée du carnet côté moteur, mais le
plateau ne distingue pas « clé absente » de « clé effacée » et ressuscite
l'ancienne valeur.** `WriteCampaignLogAtGameOver` (`campaign.py`) retire bien
la clé de `out` quand `collect_fn` rend `None`, mais `chargerCarnetSuggere`
ne transmet que ce qui reste dans `suggestions` : une clé absente du JSON est
indiscernable, côté plateau, d'une clé jamais écrite, donc `preRemplir`
retombe sur `carnet?.[cle]`, c'est-à-dire l'ancienne valeur. Sans effet
aujourd'hui, `CollectMTS` (`mts`) ne rendant jamais `None`, mais `mut_gen`,
`next_evol` et `aoa` l'utilisent déjà pour lever des pénalités : à régler
avant d'écrire leurs fichiers de campagne (§9), sans quoi une pénalité comme
`Panicked Refugees` (`aoa`), une fois posée, ne pourra plus jamais être levée.

**L'écriture de `campaign_log_last.json` n'est pas atomique.** `open(chemin,
'w')` puis `json.dump` écrit directement dans le fichier final ; une lecture
concurrente (une autre place, une requête `/get_carnet_suggere` qui arrive
pendant l'écriture) peut tomber sur du JSON tronqué. La route avale l'erreur
de parsing et rend un carnet vide, silencieusement. Pour `mts`, dont aucun
champ de `mts.json` n'a de `detection` de secours (§5 : les neuf clés sont
des drapeaux moteur purs), un carnet vide ainsi rendu perd la récompense sans
le moindre message, ni pour le joueur ni dans les journaux.

**La sonde efface `campaign_log_last.json` par son nom en dur.** Le carnet
sortant décrit au §3 est cloisonné par place de serveur via la clé de
configuration `campaign_log_last_file` (commit `89a1193`, comme le sont déjà
`campagne_folder` et `achievements_file`), mais `tools/sonde_campagne.py`
continue de lire et d'effacer le nom de fichier par défaut, sans passer par
cette clé. Avec la configuration par défaut les deux chemins coïncident et
rien ne se voit. Sur une
configuration de place (place 2, 3 ou 4 d'un serveur multi), la sonde
effacerait puis relirait le mauvais fichier, ce qui rendrait un faux positif
ou un faux négatif selon ce que la partie précédente y a laissé. C'est une
dette connue, à corriger avant toute mesure de sonde faite sur une
configuration de place.

---

## 9. Après le câblage

Par ordre d'intérêt :

1. **Écrire `next_evol.json` et `aoa.json`**, sur le modèle de `mts.json` ou
   de `mut_gen.json` (§6) : relever les clés exactes dans le `campaign.py` de
   chaque pack, récupérer l'ordre des scénarios dans `data/sets_info.json`,
   écrire résumés et enjeux en français, puis passer
   `tools/verifier_campagnes.py`. C'est ce qui manque pour que ces deux
   boîtes, déjà câblées côté moteur, deviennent jouables depuis l'écran.
   `mut_gen.json` est fait, et éprouvé à la sonde sur les cinq scénarios :
   mise en place de campagne, rôle conservé d'un scénario à l'autre, porte
   « manigance vaincue » ouvrant l'amélioration suivante (avec son témoin
   négatif), Jubilé ralliée, allié CAPTIVE remélangé, et carnet sortant écrit.
2. **Corriger la sonde pour lire `campaign_log_last_file`** au lieu du nom en
   dur `campaign_log_last.json` (§8), avant toute mesure faite sur une
   configuration de place.
3. **Identité verrouillée, deck modifiable** entre deux scénarios. Aujourd'hui
   le deck est figé tel qu'il a été choisi à la création de la campagne. Le
   livret autorise à changer d'aspect et de cartes entre les scénarios, mais
   jamais de héros, et interdit de retirer les cartes gagnées en campagne.
4. **Haut fait** de fin de campagne, et la défaite finale en campagne experte
   qui perd la campagne (règle codée côté données mais pas côté écran).
5. **Éprouver `cartes_sous_complot` et `pv_restants` en jeu.** Ils sont testés
   unitairement sur des formes mesurées, mais n'ont jamais été vus dans une
   vraie fin de scénario Zola ni en campagne experte. C'est exactement le
   contexte où le bug des armes expérimentales s'était glissé — un détecteur
   plausible qui relevait quatre cartes au lieu d'une.
6. **`gmw`** : jouable en séquence, sans récompense codée. À décider si on
   l'expose comme campagne ou pas.
