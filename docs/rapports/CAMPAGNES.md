# Mode campagne — état des lieux et suite du travail

Document de reprise, écrit le 07/08/2026. Il se suffit à lui-même : tu peux
l'ouvrir dans une session Claude Code neuve, au terminal, sans autre contexte.

La conception et l'historique détaillé sont dans
[`docs/superpowers/specs/2026-08-07-mode-campagne-design.md`](docs/superpowers/specs/2026-08-07-mode-campagne-design.md).
Ce fichier-ci est le mode d'emploi.

---

## 1. En deux mots

> ⚠ Ce paragraphe est resté à l'état du 7 août jusqu'au 12/08/2026, où il annonçait
> encore « six boîtes » et « rien à câbler » pour gmw et aos. Corrigé sur mesure.

Le mode campagne enchaîne les scénarios d'une boîte dans l'ordre du livret. Ce
qu'on gagne dans un scénario (améliorations, alliés, compteurs) est enregistré
dans un **carnet de campagne** et rejoue automatiquement à la mise en place du
scénario suivant.

**LES HUIT BOÎTES QUI ONT UN CARNET OFFICIEL SONT JOUABLES**, chacune avec son
fichier `data/campagnes/*.json`, ses planches de livret et son mode expert :

| Boîte | Code | Ce qu'elle a de particulier |
|---|---|---|
| L'Avènement de Crâne Rouge | `trors` | 3 décisions de joueur (améliorations) |
| Sinistres Motivations | `sm` | la piste de réputation, le score final, le matériel Osborn tiré au sort |
| The Mad Titan's Shadow | `mts` | tout au collecteur moteur |
| La Genèse des Mutants | `mut_gen` | le rôle, choisi en jeu, et le role-building |
| NeXt Evolution | `next_evol` | les manigances de campagne et leurs environnements |
| L'Ère d'Apocalypse | `aoa` | les missions, et la seule victoire qui peut perdre la campagne |
| Galaxy's Most Wanted | `gmw` | **le Marché** : une monnaie qui traverse les scénarios |
| Agents of S.H.I.E.L.D. | `aos` | **l'enquête** : la taupe, la grille des 27, l'accusation |

Seule **Civil War** reste dehors, et ce n'est pas une campagne : c'est un mode
bataille par équipes, qui demande son propre flux de préparation
(`.planning/todos/2026-07-30-mode-bataille-civil-war.md`).

**Le carnet se remplit tout seul** : 92 champs sur 98 sont relevés par le jeu, par le
collecteur du moteur ou par un détecteur qui lit le descripteur de monde. Les 6 qui
restent sont de vraies décisions du livret (« each player chooses »), voir §11.

**Chaque boîte a au moins un scénario joué de bout en bout par un test**, carnet écrit
et relu (§15 pour les trois dernières).

**Une clé fausse ne fait aucun bruit** (§5). `tools/verifier_campagnes.py` compare
chaque clé déclarée aux chaînes du moteur, vérifie que chaque `detection` existe
vraiment dans `detecteurs.ts`, et refuse un `tirage` mal formé. À lancer après toute
écriture de définition.

---

## 2. Lancer et tester

Le jeu tourne sous WSL, en Python 3.10 obligatoire.

Démarrer le serveur (ou double-cliquer `JOUER-SOLO.bat`) :

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src' && ~/marvel-work/python/bin/python3.10 launcher_fast.py"
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
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG' && bash ui-app/deployer.sh"
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
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src' && \
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
carte.

**FAIT le 12/08/2026** : 372 lignes retirées de `public/js/prepare/app.js`
(`CAMPAIGN_SCHEMAS`, `CAMPAIGN_CODES`, `campaignBoxes`, `renderCampaignPath`,
`renderCampaignStory`, `renderCampaignJournal`, les helpers « Story » et
`_extCodeByKey`), plus les quatre méthodes de campagne devenues orphelines dans
`prefs.js`. La campagne a son écran, et son état vit sur le SERVEUR, pas dans le
stockage local d'un navigateur.

**Comment la mort a été prouvée, parce que le commentaire mentait.** Il affirmait
« isCampaignMode() est désormais toujours faux » : c'est FAUX, l'arrivée sur
`/prepare.html?campagne` met bien le mode à `campaign`. Le vrai argument est ailleurs,
et il est mesurable : dans ce mode `STEPS` vaut `["Équipe", "Decks"]`, donc
`case 2: stepScenario()` est inatteignable, et c'est l'étape scénario qui appelait tout
ce bloc. Vérifié en faisant LEVER les quatre fonctions (`throw`) puis en jouant les
suites qui traversent l'écran : création d'équipe, modification des decks et lancement
normal, 9 cas verts avec le code piégé.

Une leçon de méthode : un commentaire qui déclare du code mort n'est pas une preuve,
et celui-ci se trompait de raison tout en ayant raison sur la conclusion.

---

### 6 ter. Les bonus ET les malus passent d'une mission à l'autre (10/8/2026)

Le tableau ci-dessus prouve que le carnet SORT. Reste la question inverse,
posée en jeu : est-ce que ce qu'on a gagné ou perdu **revient** au scénario
suivant ? Mesuré à la sonde, une campagne à la fois, chaque fois en comparant
le monde AVEC et SANS carnet. La différence est la preuve ; sans le témoin
« sans carnet », on prendrait pour une récompense une carte qui était là de
toute façon.

| Boîte | Ce qui a été injecté | Effet constaté | Sans carnet |
|---|---|---|---|
| `trors` | `Player 1 Rescued Allies = 01002`, scénario 4 | l'allié entre dans `player_deck` | absent |
| `trors` | `Experimental Weapons = 04072;04073`, scénario 2 | les deux armes entrent dans `encounter_deck` | absentes |
| `sm` | `Reputation Track = 9` + récompense d'aspect, scénario 2 | un exemplaire de plus dans `player_deck` | 1 seul |
| `mts` | `Campaign Pool: Cosmo = 1`, scénario 3 | Cosmo dans `players/allies` | absent |
| `mut_gen` | rôle + `Frightened Police Defeated`, scénario 2 | amélioration du BON rôle attachée | aucune |
| `mut_gen` | `Campaign Pool: Jubilee` + captif, scénario 3 | Jubilé alliée, captif dans `player_deck` (choisi) | absents |

Les quatre campagnes jouables appliquent donc leurs bonus, et `trors` prouve
qu'un MALUS passe aussi : les armes expérimentales laissées derrière soi
reviennent grossir le deck de rencontre.

**Ce que ça ne prouve pas** : que chaque récompense de chaque boîte est
branchée. Une par campagne a été éprouvée, pas les quarante. Le reste repose
sur la lecture du `campaign.py`, et sur `tools/verifier_campagnes.py` qui
garantit au moins que les clés déclarées existent.

### 6 bis. Ce que les livrets officiels ont appris (10/8/2026)

Les PDF officiels de FFG, livrets et carnets de campagne, sont dans
`regles-officielles/` à la racine de `Marvel LCG` (rangés là le
31/08/2026, ils étaient à la racine). Ils sont **vectoriels**, donc lisibles au
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

### Audit texte-vs-code, boîte par boîte (commencé le 10/8/2026)

L'outil `verifier_campagnes.py` prouve qu'une clé déclarée existe dans le
moteur, et le contrôle inverse prouve qu'aucune clé lue par le moteur n'est
absente des écrans. **Aucun des deux ne dit qu'une clé juste applique la bonne
règle.** D'où cette relecture, encart SETUP du livret contre `campaign.py`,
instruction par instruction. Même méthode que l'audit comportemental d'Hercule,
qui avait sorti deux vrais bugs invisibles aux tests de construction.

**Mutant Genesis : fait. Un écart trouvé et corrigé.** Les quatre autres
instructions de mise en place sont conformes (constitution du deck Futur Passé,
amélioration de rôle tirée au hasard conditionnée à la manigance vaincue,
Jubilé face B et retirée définitivement, manigance de campagne révélée, mode
expert aux scénarios 2 à 5 — vérifié page par page, les lignes *Expert Campaign
Only* des scénarios 3 et 5 existent bien, elles sont juste imprimées après
l'en-tête VICTORY).

L'écart, **fermé le 11/8/2026** : « Each CAPTIVE ally recorded in the campaign
log **may** be shuffled into **any** player's deck » (p.12, 16 et 19). Le code
ne prenait aucune des deux libertés : il mélangeait tout, d'office, dans le deck
du **premier joueur**. En solo l'écart était mince, encore qu'un allié de plus
dilue un deck et que le livret laisse le refuser. À quatre joueurs, tous les
alliés libérés par toute l'équipe s'entassaient chez le joueur 1.

Un correctif par `ChooseAbilities` avait été écrit puis **retiré** le 10/8/2026,
faute de tenir à la mesure : avec lui, plus aucun allié n'entrait dans un deck.
**Repris et remesuré, le blocage ne se reproduit pas**, ni à un joueur ni à
quatre. L'hypothèse la plus probable est que la question était alors résolue par
son option « Cancel » — le pilote de la sonde répond la première option légale,
et une liste où l'annulation vient en tête donne exactement zéro allié. C'est
d'ailleurs très précisément ce que la mesure `CHOIX=-1` produit aujourd'hui.

**Un second défaut, préexistant, est tombé avec.** `Faces.ShuffleAllTo` ne
mélange que s'il a *déplacé* quelque chose (`if moved_faces: deck.Shuffle(...)`).
Les cartes étant générées directement **dans** `player_deck`, rien ne bougeait :
le mélange ne partait jamais et les alliés restaient sur le dessus. Mesuré avant
correction, sur le code d'origine : les **quatre captifs se retrouvaient dans la
main de départ**, à un joueur comme à deux. Le livret dit « shuffled into », pas
« posé sur le dessus ». La carte est désormais générée hors deck, comme le fait
déjà `MelangerLesInterferences` dans aos.

**Comment on mesure un menu à plusieurs branches.** Le pilote de la sonde
répondait toujours la première option légale, ce qui rend une seule branche
observable : un menu à une branche et un menu à quatre se mesuraient pareil.
D'où `CHOIX`, l'index de l'option retenue (négatif = depuis la fin). Piège
associé : `CHOIX` change **aussi** les mulligans, donc la taille d'un deck ne
veut plus rien dire d'une mesure à l'autre — on compte les cartes elles-mêmes,
où qu'elles soient. La sonde accepte aussi plusieurs héros séparés par des
virgules : une règle qui parle de « any player's deck » ne se mesure pas en solo.

11 vérifications dans `tools/test_captifs_mut_gen.py` : les trois branches
(premier joueur, second joueur, refus), le témoin sans carnet, l'absence de
captif dans la main de départ, et un identifiant inconnu qui ne casse rien.

**La leçon de méthode compte plus que l'écart.** La première mesure de ce
correctif avait l'air bonne (33 → 35) parce qu'elle tournait sur du bytecode
PÉRIMÉ : la sonde exécute `.game`, pas `src/`. Copier un `.py` ne suffit pas,
il faut `launcher_fast.py --build-only` avant de sonder. Sans ce rappel, on
mesure l'ancien code et on croit avoir prouvé le nouveau.

**NeXt Evolution : fait. Aucun écart.** Les cinq mises en place sont
conformes, y compris les détails qu'on rate à une lecture rapide : les
Maraudeurs retirés AVANT le texte « Setup » de Gotta Get Away, le tough donné
aux ennemis au seul scénario 2, un compteur de momentum sur Juggernaut par
environnement en jeu, Black Tom et un Saule Rampant distribués face cachée puis
le reste remélangé, la défausse qui s'arrête sur un sbire OU un attachement
PSIONIC suivie du remélange de la défausse rencontre. Et surtout le soin
expert, qui **change de prix selon le scénario** : un pion accélération aux
scénarios 2 et 4 (p.11 et p.16), une carte rencontre face cachée aux scénarios
3 et 5 (p.14 et p.18). Le code fait exactement cette distinction.

**Age of Apocalypse : fait. Aucun écart, dont un faux positif instructif.**
Le carnet officiel donne trois colonnes par mission (Setup, Defeated, Not
Defeated) et l'ordre des en-têtes dans le PDF ne suit pas celui des colonnes :
il faut lire les positions pour ne pas inverser récompense et pénalité. Une
fois remises dans l'ordre, les quatre missions correspondent.

Deux directives « Setup » semblent manquer au code : « Set each campaign ally
aside » (Find Lost Mutants) et « Set each copy of Desperate Measures upgrade
aside » (Liberate the Seattle Core). Elles sont en réalité **inatteignables** :
une mission n'est jamais proposée deux fois (`Mission Done` la retire du
tirage), et le bonus qu'elle met de côté n'est écrit au carnet qu'à la FIN de
la partie où elle est jouée. Pendant sa propre mission, il n'y a donc rien à
mettre de côté. Propriété non évidente, écrite ici pour qu'on ne « corrige »
pas ce qui n'est pas cassé.

Une approximation assumée : « Professor X cannot enter play during this game »
au scénario 5. Professor X est une carte JOUEUR de Mutant Genesis (32019), pas
une carte du set AoA ; l'interdiction porte sur le deck du joueur et n'est pas
contrôlée. À respecter à la main si on l'a mis dans son deck.

**The Mad Titan's Shadow : fait. Aucun écart.** Les cinq mises en place
correspondent, jusqu'aux faces : Cosmo est le verso de « Secure the Landing
Pad » (21180b), Black Swan celui de « Save the Shawarma Place » (21182b), et
Odin entre en jeu sur sa face King (`21139b,21139a`, face B en premier). Le
soin expert est un pion accélération aux scénarios 2 à 5 (p.13, 17, 21, 25),
ce que fait le code.

**The Rise of Red Skull : fait. Aucun écart.** Les instructions communes aux
scénarios 2 à 5 y sont, et les trois particularités du scénario 5 sont dans le
module de sa manigance (`red_skull/04128a.py`), correctement réparties entre
`campaigns=` et `campaigns_expert=` : la menace égale aux pions retard, avec
multiplication par le nombre de héros en expert, va dans la liste normale ; la
carte rencontre aux joueurs qui étaient engagés va bien dans la liste experte.
Une nuance de forme : le livret dit « search their deck for all cards with the
setup keyword », le code repose les améliorations Tech et Basic enregistrées au
carnet. C'est l'intention réelle, ces cartes vivant au carnet et non dans le
deck sauvegardé.

**Sinister Motives : fait. Aucun écart, et un faux positif de ma part qui vaut
leçon.** J'ai cru trouver un bug d'origine : `CampaignSetup` pose Public Outcry
avec `27174a,27174b`, donc toujours la face A, alors que la face A porte
« Standard Mode Only » (2 pions notoriété par héros) et la face B « Expert Mode
Only » (3). J'ai corrigé, puis mesuré à la sonde **avec témoin sur l'ancien
code** : les deux versions posent la face B en expert. Correctif annulé.

La raison est un mécanisme du moteur qu'il faut connaître :
`AbilityFactoryExpert.StandardModeOnly()` et `ExpertModeOnly()` sont des
capacités portées par la CARTE, qui la retournent à son entrée en jeu si le
mode ne correspond pas. C'est `sm/bad_publicity/27174a.py` et `27174b.py` qui
les portent. **Ne jamais réimplémenter le choix de face selon le mode à la mise
en place** : la carte s'en charge. Corollaire de méthode : mon premier `grep`
avait conclu « aucun module pour 27174 » parce qu'il ne regardait pas les
sous-dossiers du pack.

Le reste de `sm` est conforme, y compris les deux crochets du module de
scénario : la menace sur « Light at the End » égale au Cauchemar Éveillé
(`sinister_six/27100a.py`) et les sbires de l'Assaut Sinistre selon les
Derniers Debout (`venom_goblin/27116a.py`).

### Bilan de l'audit texte-vs-code

Six boîtes relues, **un seul vrai écart** : les alliés captifs de Mutant
Genesis — **fermé le 11/8/2026**, voir plus haut. Deux approximations assumées
et documentées (Professor X au scénario 5 d'AoA, la forme du « setup keyword »
de trors), et deux faux positifs qui venaient de ma lecture du PDF et non du
code. Le câblage des campagnes est plus sain que la couverture des tests ne le
laissait espérer.

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

`trors`, `sm` et `mut_gen` ont leurs scans. Sans scans, l'écran affiche le
résumé français seul — c'est prévu, rien ne casse.

`tools/pages_livret.py` fait le découpage à partir des PDF officiels, qui sont
dans `regles-officielles/` à la racine de `Marvel LCG`. Les livrets sont carrés et
vectoriels : on REND les pages, on n'extrait pas leurs images, ce qui donne un
traitement uniforme et la taille des scans déjà en place, 975 px. La seule
chose à fournir pour une nouvelle boîte est la CARTE des pages, en tête de
l'outil : quelle page joue quel rôle. C'est le vrai travail, le reste est
mécanique.

**`pages_regles` s'affiche depuis le 10/8/2026.** La clé était documentée ici
et lue par AUCUN code : les pages de règles valables pour toute la boîte, mode
expert compris, dormaient sur le disque. Quatre fichiers étaient concernés,
trois pour `trors` et un pour `sm`. L'écran des campagnes les montre maintenant
dans un bloc « Règles de la campagne ».

---

## 8. Pièges

**Le déploiement écrase `public/`.** RÉSOLU en deux temps : le 30/08
(`deployer.sh` inverse le sens, le jeu Windows devient la référence), puis le
31/08/2026, où la copie WSL `~/marvel-work/fusion/marvel-lcg-src` a été
**supprimée** lors du grand rangement. `deployer.sh` n'a plus qu'une cible,
l'installation vivante. Plus aucun `rsync` de compensation n'est nécessaire.

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

**La copie WSL peut écraser `src/`, pas seulement `public/`.** RÉSOLU le
31/08/2026 : la copie `~/marvel-work/fusion/marvel-lcg-src` a été supprimée,
il n'existe plus qu'une installation du jeu. Ce piège est conservé ici comme
témoignage : ce mécanisme a effacé deux fois du travail dans
`src/cards/pack/` sans toucher `public/`. Si une deuxième copie du jeu
réapparaît un jour, relire ce paragraphe avant de la brancher à quoi que ce
soit.

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
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src' && ~/marvel-work/python/bin/python3.10 launcher_fast.py --build-only"
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

~~**L'écriture de `campaign_log_last.json` n'est pas atomique.**~~ **CORRIGÉ
le 10/8/2026**, et pas seulement pour le carnet : les trois écritures qui
comptent passent par `src/engine/ecriture_atomique.py` (fichier temporaire dans
le dossier de destination, `fsync`, puis `os.replace`). Le carnet sortant, les
campagnes du joueur (`/save_campagne`) et les hauts faits, ce dernier parce
qu'il garde des déblocages pour toujours.

Ce n'était pas théorique : le 10/8/2026, l'extinction du poste en pleine partie
a laissé `campagnes/Essai_RoleBuild.json` à 0 octet, et `list_campagnes`, qui
saute les fichiers illisibles, faisait disparaître la campagne de l'écran sans
un mot. `tools/test_ecriture_atomique.py` charge le module par son chemin (il
n'a que des imports standard, donc pas besoin d'amorcer le moteur) et casse la
sérialisation en plein milieu : l'ancien contenu doit rester intact et aucun
temporaire ne doit survivre. Le témoin négatif a été joué sur l'ancien code :
53 octets avant, 29 après, JSON illisible.

~~**La sonde efface `campaign_log_last.json` par son nom en dur.**~~
**CORRIGÉ le 10/8/2026.** `tools/sonde_campagne.py` lit désormais la même
source que le moteur, la clé `campaign_log_last_file` du `launch.json` du
dossier de jeu, que `launcher_fast.py` y recopie à chaque lancement. Éprouvé
sur une configuration de place simulée (`./carnet_place2.json`), avec témoin :
la sonde d'avant ne capture aucun carnet, la corrigée le capture et y relit
`Professor Saved`.

---

## 8 bis. Agents of S.H.I.E.L.D., et ce qui lui manque encore

La huitième et dernière boîte à carnet officiel est câblée depuis le 11/8/2026.
Son fil est le **Conseil exécutif** : ses trois membres entrent en jeu à chaque
scénario avec les compteurs secrets qu'ils avaient à la fin du précédent. C'est
la seule campagne du jeu où l'état d'une carte se reporte tel quel, chiffre par
chiffre. Le reste suit : le Niveau d'Alerte du scénario 2 monte de ce qu'on a
laissé debout au 1, les verrous de la Cellule du 3 s'ouvrent à proportion des
captifs libérés au 2, les Adaptoïdes du 3 et les Thunderbolts du 4 reviennent
pour Zemo.

Deux choses ont dû être corrigées dans le pack d'origine :

- `baron_zemo/50167a.py` portait `assert Worlds.IsCampaign(effect) == False`,
  qui **interdisait purement et simplement** le mode campagne. Le commentaire
  au-dessus disait déjà quoi faire à la place ; c'est ce qui a été fait.
  Divergence volontaire, commentée dans le fichier.
- Le scénario de Zemo apporte **déjà** le Conseil avec son set. Poser un second
  exemplaire donnait six membres sur la table. La mise en place ne crée
  désormais un membre que s'il n'est pas là, et lui rend ses compteurs dans
  tous les cas.

Mesuré à la sonde, bytecode recompilé, avec témoin : trois membres exactement
aux scénarios 1 et 5, deux secrets chacun au scénario 1 comme le veut le livret,
et au scénario 5 les valeurs 1 / 0 / 2 du carnet entrant ressortent à
l'identique.

### Le secret de la taupe, et où il dort

Neuf cartes preuve, trois tirées au hasard dans l'enveloppe A.I.M. au début de
la campagne : c'est la combinaison de la taupe, et elle doit rester **cachée du
joueur**. Les six autres forment l'enveloppe S.H.I.E.L.D., où les joueurs
puisent.

**Le secret a trouvé sa place le 11/8/2026.** Le carnet est un fichier que le
joueur LIT et que l'écran affiche en entier : y ranger la combinaison
reviendrait à ouvrir l'enveloppe devant lui. Trois options ont été pesées (le
serveur le garde, pas de secret du tout, l'enveloppe reste en carton) et c'est
la première qui est en place :

- **Tirage** côté serveur à la première écriture d'une campagne `aos`, une
  preuve par série, jamais depuis le client — un client qui en enverrait une se
  la ferait remplacer.
- **Filtrage** : `_sans_secret()` passe sur les trois sorties (`list_campagnes`,
  `get_campagne`, la réponse de `save_campagne`). Le navigateur ne le reçoit
  jamais, donc ne peut pas l'afficher.
- **Injection** : `new_game` remet la part secrète dans `campaign_log` juste
  avant `NewGame`. Le moteur reçoit un carnet complet.

> **Correctif du 07/10/2026.** L'injection n'a lieu que si `new_game.rules`
> contient `mode_campaign` : une campagne dont un scénario est resté « en cours »
> ne dépose plus son secret dans une partie ordinaire.

La difficulté était d'identifier la campagne concernée : le descripteur de
`/new` est **gelé** et ne porte pas d'identifiant. Plutôt que de toucher au
contrat, on se sert de ce qui existe déjà : l'écran écrit `partieEnCours` AVANT
de lancer, donc la campagne visée est celle dont la partie en cours est la plus
récente.

Mesuré : le secret est écrit au fichier (`50187;50189;50191`, une preuve par
série) et **absent des trois routes**. L'injection, longtemps câblée sans
témoin, est prouvée depuis que les preuves se gagnent : voir juste en dessous.

### Les preuves : gagner une carte de l'enveloppe S.H.I.E.L.D.

Câblé le 11/8/2026. Le livret p.6, repris mot pour mot dans les encarts
VICTORY des pages 9, 11, 13 et 15 : « If at least one Board Member environment
in play has no secret counters on it, gain one evidence card from the
S.H.I.E.L.D. envelope ».

Trois lectures comptent, et `_preuve_gagnee` les tient toutes les trois :

- **« environment »**. Un membre passé face attachement n'est plus un
  environnement. Le filtre `card_type=Environment` suffit à l'écarter, et de
  toute façon il a au moins quatre secrets.
- **« from the S.H.I.E.L.D. envelope »**. Jamais une des trois preuves de
  l'enveloppe A.I.M., jamais deux fois la même. Le tirage se fait dans les neuf
  moins la taupe moins ce qui est déjà gagné, avec `Rand.RandomChoice`, donc
  dans le flux d'aléa du moteur et rejouable.
- **la carte ne rejoint aucun deck**. Elle ne sert qu'à rayer des combinaisons
  et à poser sa capacité « Setup » au scénario suivant.

La clé du carnet est `Evidence Gained`, une liste cumulative d'identifiants,
déclarée dans `victoire_commune` de `aos.json`. Le moteur écrit la liste
COMPLÈTE, pas l'ajout : le carnet reste vrai même si le joueur corrige.

**Une fuite a dû être fermée en même temps.** `WriteCampaignLogAtGameOver`
recopiait tout le store dans le carnet sortant, puis le rendait au journal de
partie. La combinaison de la taupe, que le serveur venait d'injecter, ressortait
donc deux fois sous les yeux du joueur. `CLES_SECRETES` l'arrête, dans
`src/cards/pack/mts/campaign.py`, avant les deux sorties.

**L'injection est enfin prouvée**, et c'est ce câblage qui la prouve : à table
identique, un membre vidé de ses secrets rapporte une preuve AVEC
`A.I.M. Envelope` dans le carnet entrant, et rien sans lui. Sans l'enveloppe, on
ignore quelles preuves sont dans celle du S.H.I.E.L.D. : en tirer une au hasard
risquerait de rendre au joueur une carte de la taupe et de fausser la grille, on
préfère donc ne rien donner.

Treize vérifications dans `tools/test_preuves_aos.py`, mesurées à la sonde sur
de vraies parties, bytecode recompilé : cas nominal, deux témoins négatifs
(aucun membre vidé, aucun secret injecté), cumul, enveloppe épuisée, et la paire
qui prouve le filtre — une clé bidon injectée par la même voie ressort, le
secret non.

### Poser les preuves gagnées au scénario suivant

Câblé le 11/8/2026. Encarts SETUP des scénarios 2 à 5 : « After resolving
mulligans, resolve the "Setup" ability of each evidence card the players have
earned. » Les neuf cartes existaient déjà et portaient leur capacité
(`aos/executive_board_evidence/`) ; rien ne les mettait en place.

**Le livret dit « après les mulligans », et il a une bonne raison.** Chaque
preuve propose deux choses : poser un compteur secret sur un membre du Conseil
pour chercher une carte dans sa collection, et poser une menace sur la
manigance principale pour chercher une carte dans son deck et **l'ajouter à la
main**. Résoudre cela avant l'étape 14 coûterait une carte au joueur —
`DrawUp("Max")` compte ce qui est déjà en main — et le mulligan pourrait
ensuite jeter la carte cherchée.

Le moteur n'avait pas ce point d'accroche. Il en a un maintenant : **étape
15 bis**, `Message.WhenCampaignSetupAfterMulligans`, envoyée dans
`world.GameSetup` juste après les mulligans et avant les capacités de mise en
place des identités, avec sa fabrique
`AbilityFactoryCampaign.WhenCampaignSetupAfterMulligans`. Ajout purement
additif : aucune autre boîte n'y écoute. Mesuré à la sonde, la main passe de 6
à 8 avec deux preuves, ce qui ne peut arriver qu'après la pioche.

Deux pièges relevés en chemin :

- **`aside_deck` n'est pas un deck.** `Evidence.OnWhenCardSetup` sait entrer en
  jeu tout seul, mais seulement `if self.IsInDeck()`, et
  `DeckTypeFlags.AsideDeck.is_deck` est faux. Une preuve générée là restait
  invisible, capacité jamais partie. On la pose donc soi-même avec
  `PutIntoPlay`, puis `Setup`.
- **Le scénario 5 apportait les neuf preuves.** `baron_zemo.json` charge le set
  `executive_board_evidence` complet, et le moteur résout la capacité « Setup »
  de toute carte Evidence trouvée dans un deck (étape 12). En mode campagne,
  `area_evidence` contenait donc 50185 à 50193 — **dont les trois de
  l'enveloppe A.I.M.**, ce qui donnait la taupe au joueur sans qu'il ait à
  enquêter. Mesuré avant correction. `EcarterLesPreuvesDuScenario` retire le
  set à la création du deck de rencontre, en mode campagne seulement ; hors
  campagne le comportement est inchangé, vérifié en remettant le fichier
  d'avant et en remesurant.

Onze vérifications de plus dans `tools/test_preuves_aos.py` (24 au total), et
la suite complète des cartes repassée après le changement de
`world.GameSetup` : 4189 OK, 0 erreur.

### La grille de déduction

Câblée le 11/8/2026, côté écran. Livret p.5 : « The campaign log contains a
list of all possible combinations of means, motive, and opportunity, with each
combination implicating one of the board members. »

**Vingt-sept combinaisons, neuf par membre.** Ce sont des données imprimées, pas
une règle à déduire : relevées une à une sur
`mc50_agents_of_shield_campaign_log.pdf` et rangées dans le bloc `enquete` de
`data/campagnes/aos.json`, sur le modèle du `marche` de `gmw.json`. La
transcription a été contrôlée par construction : les 27 combinaisons possibles
(3 moyens × 3 mobiles × 3 occasions) doivent apparaître chacune exactement une
fois, et c'est le cas. Une ligne mal recopiée aurait désigné le mauvais membre
sans rien casser d'autre.

**Le raisonnement est à l'envers de l'intuition.** Une preuve qu'on TIENT est
une preuve qui n'est PAS dans l'enveloppe A.I.M. : toute combinaison qui la
contient est donc morte. Se tromper de sens rayerait exactement le complément
et accuserait le mauvais membre. C'est le premier cas du test.

Le rayage n'est pas coché à la main comme sur le carnet papier : il est
**déduit** de `Evidence Gained`. Le joueur ne peut pas se tromper, et il n'y a
rien à enregistrer. L'écran compte les combinaisons restantes par membre, marque
« mis hors de cause » celui qui n'en a plus, et dit quand une seule tient
encore.

Vue `vueEnquete` dans `public/js/campagne/app.js`, atteinte par un bouton de la
vue campagne — accessible même partie en cours, puisqu'on ne touche à rien en la
lisant. Les neuf cartes preuve sont montrées en légende, celles qu'on tient
mises en avant : elles existent toutes et le joueur les connaît, ce que l'écran
ignore c'est lesquelles dorment dans l'enveloppe A.I.M.

**Un piège d'`el()`** : ses styles sont appliqués par `Object.assign`, qui ignore
silencieusement les clés `--*` (il faut `setProperty`). Une teinte passée en
`--teinte` laissait le fond transparent et le texte sombre du CSS devenait
illisible sur le fond noir. La couleur est posée sur `background`.

Cinq cas dans `ui-check/tests/campagne-enquete.spec.ts`, dont le dernier vérifie
qu'aucune route ne rend `secret_aim` ni `A.I.M. Envelope` à cette page.

### L'accusation du scénario 5

Câblée le 11/8/2026. Surprise en ouvrant le pack : **tout était déjà écrit** —
les étapes 1B → 2A → 2B → 3A → 3B, les deux sanctions, et même la table des 27
combinaisons dans `CalcMole`. Elle correspond exactement à ma transcription du
carnet imprimé, faite indépendamment : deux lectures séparées de la même page,
même résultat.

Mais tout cela était **inerte en campagne**. `50167a` renonce à préparer les
preuves en mode campagne (à raison : les membres du Conseil viennent du
scénario précédent), donc les deux enveloppes n'étaient jamais créées et
`CalcMole` tombait sur son `assert False`.

**Les enveloppes ne sont pas des paquets de cartes en campagne.** Le pack les
monte en vraies piles avec `SetAsideDeck`, ce qui convient hors campagne. Mais
`SetAsideDeck.Create` inscrit la pile dans `world.additional_decks`, et
`to_descriptor` rend TOUTES ces piles au navigateur avec le `card_id` réel de
chaque carte, face cachée ou non — mesuré hors campagne : les neuf preuves
arrivent au client, identifiants en clair. Monter l'enveloppe A.I.M. en pile
aurait rendu la taupe lisible depuis la console, après deux fuites déjà fermées
pour la même raison.

En campagne, les deux enveloppes sont donc **deux lectures du carnet** :

- A.I.M. = les trois identifiants de `A.I.M. Envelope` ;
- S.H.I.E.L.D. = les neuf moins celles-là moins `Evidence Gained`.

Aucune carte n'existe tant que le joueur n'a pas le droit de la voir. Une preuve
puisée est fabriquée au moment du gain, et les trois de la taupe seulement à
l'étape 2B, quand le livret dit « the players take the evidence cards from the
A.I.M. envelope ». `ShieldEnvelopeHasCards`, `GainCardsFromShieldEnvelope` et
`CalcMole` se branchent là-dessus ; hors campagne, rien ne change.

**Deux correctifs de règle**, tous deux dans `50168a.py` :

- L'accusé était **demandé** au joueur parmi les environnements sur la table.
  Le livret p.19 dit qu'il **découle** de la combinaison : « Each combination is
  listed underneath a board member. This board member is the accused. » On
  pouvait donc accuser un membre que sa propre combinaison n'accusait pas.
- Pire en campagne : un membre passé côté attachement n'est plus un
  environnement de ce nom, donc n'était plus proposable. Or les secrets se
  reportent, un membre à quatre secrets arrive **déjà retourné** et le reste
  jusqu'à la fin (p.6). Mesuré : avec le Médecin en chef retourné à l'arrivée,
  il était impossible de l'accuser alors qu'il était la taupe — l'accusation
  était fausse d'office. `MembreDeLaCombinaison` rend le membre quelle que soit
  sa face.

Corrigé aussi : `CollectAOS` accordait une preuve à la victoire du scénario 5.
Les encarts VICTORY des scénarios 1 à 4 portent cette clause, celui du 5 non
(p.19) — au 5, les preuves se gagnent en partie, par la Réponse de l'étape 1B.

29 vérifications dans `tools/test_accusation_aos.py` : puiser dans l'enveloppe,
les trois sanctions de la page 19 (tout juste, une hypothèse ratée, tout faux),
la taupe déjà retournée, et le non-passage du secret au descripteur. Plus deux
cas de non-régression hors campagne. Suite complète des cartes repassée : 4189
OK, 0 erreur.

### Rejouer le scénario 5 après une défaite

Câblé le 11/8/2026. Livret p.19, encart DEFEAT, campagne **standard**
uniquement : « Prepare the evidence as if you are starting a new campaign. Gain
one evidence card from the S.H.I.E.L.D. envelope for each scenario in which you
had at least one Board Member environment with no secret counters on it. »

**La taupe change.** Ce n'est pas une remise à zéro anodine : la grille de
déduction construite pendant quatre scénarios est invalidée d'un coup. Le joueur
doit le lire avant de cliquer, d'où un encadré ambre et un bouton qui dit ce
qu'il fait (« Re-préparer les preuves ») plutôt qu'un simple « Valider ».

**Le compte manquait.** « For each scenario in which you had at least one Board
Member environment with no secret counters » — le carnet imprimé permet de le
recalculer après coup, puisqu'il garde une colonne de compteurs secrets par
scénario (#1 à #4). Le moteur, lui, n'écrase qu'une valeur par membre. On tient
donc le compte au fil de l'eau, clé `Scenarios With A Cleared Board Member`,
incrémentée à chaque victoire des scénarios 1 à 4.

Point de détail qui compte : la condition est mesurée **à part de la
récompense** (`_un_membre_sans_secret`). L'enveloppe S.H.I.E.L.D. peut être vide
alors que la condition tient — le scénario ne rapporte alors aucune preuve, mais
il compte quand même pour la reprise. Les mélanger aurait sous-compté.

**Tout se décide côté serveur**, route `/reinitialiser_enquete` : nouveau tirage
de `secret_aim`, puis N preuves tirées de la NOUVELLE enveloppe S.H.I.E.L.D. Le
client n'envoie qu'un identifiant et ne reçoit qu'un compte. Lui laisser choisir
les preuves rendues reviendrait à écrire la réponse de l'enquête dans le
navigateur, puisque les six rendues sont exactement le complément de la taupe.

La route **refuse en expert** : le même encart y dit l'inverse, la campagne est
perdue, et c'est déjà la règle `defaite` de `aos.json`. Les deux ne peuvent
jamais s'appliquer ensemble, ce que `repriseDeCampagne` traduit par
`standard_seulement` comme `verdictDeCampagne` le fait avec `expert_seulement`.

Mesuré : sur six reprises d'affilée, la combinaison est bien re-tirée à chaque
fois, et **aucune preuve rendue n'appartient jamais à la nouvelle taupe** —
l'invariant sans lequel la déduction repartirait fausse.

6 cas vitest sur `reprise-campagne.ts` (module pur, comme `defaite-campagne.ts`)
et 5 cas Playwright sur la route, dont le compte borné à six et le refus en
expert. Le câblage du panneau — s'ouvrir à la défaite du scénario 5 et appeler
la route — est couvert par `campagne-panneau.spec.ts`, sur une vraie partie
perdue (voir §10).

### Le soin de campagne experte

Câblé le 11/8/2026. Encarts SETUP des scénarios 2 à 5, sous « Expert Campaign
Only » : « Each player may place one secret counter on a Board Member
environment to heal damage from their identity equal to their REC. »

Les huit boîtes font toutes payer le retour à la santé, et jamais deux fois de
la même façon : une carte rencontre face cachée pour sm et next_evol, une
obligation ajoutée au deck pour trors. Ici le prix se paie sur le **décor** : un
secret de plus sur le Conseil, donc un pas de plus vers le basculement d'un
membre du côté de Zemo. Le soin se paie en terrain perdu sur le fil de la
campagne, pas en cartes.

Deux écarts avec les sept autres, tous deux voulus par le livret : on soigne de
sa **RÉC** et non jusqu'aux PV imprimés, et le coût ne touche pas le deck du
joueur.

L'ordre compte, et il est celui du livret : `PoserLeConseil` (sinon rien à
viser), puis `ExpertCampaignSetPlayersHPToTheirRemainingHP` (sinon on soignerait
des PV écrasés juste après), puis le soin.

Une conséquence qui n'est pas un défaut : quand **tout le Conseil a basculé**,
il n'y a plus un seul *environnement* Board Member sur la table, donc plus rien
à viser et plus de soin. Laisser le Conseil tomber coûte donc aussi la santé des
héros. Mesuré au scénario 5 expert avec trois membres à trois secrets.

13 vérifications dans `tools/test_soin_expert_aos.py`, sur Maria Hill (9 PV
imprimés, RÉC 3) pour que les comptes soient lisibles à la main : cas nominal
3 → 6, plafond 8 → 9, témoin standard, témoin scénario 1, et le Conseil basculé.

### Les Thunderbolts survivants, et la grille tenue en double

Deux points fermés le 11/8/2026.

**Les Thunderbolts survivants reviennent au scénario 5.** Livret p.19 : « If you
recorded any "Surviving Thunderbolts" in the campaign log, shuffle those minions
**and their encounter sets**, except for Jolt's, into the encounter deck. » La
clé `Surviving Thunderbolts` était **écrite** au scénario 4 et **relue nulle
part** : rien ne revenait, ni les sbires ni leurs sets.

Le set porte le sbire : l'ajouter au deck de rencontre ramène les deux d'un
coup, et c'est le moteur qui mélange. On passe donc par `encounter_set_names` à
la création du deck, comme `EcarterLesPreuvesDuScenario` — la seule étape où le
contenu du deck se décide encore.

Le « except for Jolt's » n'est pas une exception arbitraire : **Jolt appartient
au set du scénario 4 lui-même** (`data/scenarios/thunderbolts.json`, clé
`encounters`) et aucun fichier de `data/encounter_sets/` ne la contient. Il n'y
a rien à rapporter avec elle, on ne remet que la carte. Mesuré : avec Moonstone
et Jolt au carnet, le deck de rencontre grossit de sept cartes — les six de
`gravitational_pull`, plus Jolt seule.

11 vérifications dans `tools/test_thunderbolts_aos.py`, dont le témoin sans
carnet et le témoin hors campagne.

**La grille des 27 ne peut plus diverger en silence.** Elle est recopiée à deux
endroits qui ne se parlent pas : `MembreDeLaCombinaison` (moteur, qui désigne la
taupe et l'accusé) et le bloc `enquete` de `aos.json` (écran, qui raye). Les deux
ont été relevées indépendamment et concordent, mais rien ne les comparait :
modifier l'une sans l'autre ferait afficher au joueur une grille qui n'accuse pas
le même membre que le jeu.

`tools/verifier_grille_aos.py` lit le module Python en AST — sans démarrer le
moteur — et le compare au JSON, membre par membre. Il revérifie au passage que
les 27 combinaisons possibles sont couvertes, chacune une fois. **Mis en défaut
exprès** en changeant une ligne du JSON : il refuse et nomme la combinaison
fautive.

### Le Conseil entièrement retourné perd la partie

Câblé le 11/8/2026. Les trois cartes attachement (50181b, 50182b, 50183b)
portent toutes le même texte : « If there are 3 [[Board Member]] attachments in
play, the players lose the game », et le livret p.18 le redit pour Zemo.

Le pack le câble **en réponse à un retournement**
(`IfThereAre3BoardMemberAttachmentsInPlayPlayersLoseTheGame`, sur
`AfterFlipToThisFace`). Cela suffit tant que le troisième bascule en cours de
partie. En campagne, non : les secrets se reportent, un membre à quatre secrets
(trois en expert) arrive **déjà retourné**, et `Card.Flip` n'envoie
`AfterCardFlip` que si `world.is_game_started` — ce qui est faux pendant la mise
en place.

Mesuré avant correction, scénario 5 expert avec les trois membres à trois
secrets : les trois basculaient au setup, `game_over` restait faux, et comme
**plus aucun retournement ne pouvait survenir ensuite**, la condition ne se
déclenchait jamais. Les joueurs jouaient une partie déjà perdue, avec les trois
attachements sur le dos.

La condition est un **état**, pas un événement : elle est donc relue une fois la
mise en place de campagne faite, à **tous** les scénarios — les trois cartes
portent le texte, et un Conseil peut basculer avant le dernier scénario. Mesuré
au scénario 3 standard avec quatre secrets chacun : perdu aussi.

Un cas de `test_soin_expert_aos.py` **est devenu faux** et a été réécrit : il
observait qu'un Conseil entièrement basculé ne laisse aucun environnement à
viser pour le soin expert. C'est toujours vrai, mais la situation est désormais
inatteignable — la partie s'arrête avant. Une mesure qui décrit un état devenu
impossible est pire qu'absente.

Et une leçon en passant : à deux secrets reportés en expert, **le prix du soin**
(un secret de plus) fait basculer un membre. Ce n'est pas un défaut, c'est
l'économie de la boîte, et c'est maintenant un cas de test.

14 vérifications dans `tools/test_conseil_aos.py`, dont les deux seuils
(quatre en standard, trois en expert) et le scénario 1, qui impose deux secrets
à chacun et ne peut donc jamais commencer perdu.

### Ce qui n'est PAS fait

**Une fuite du mode HORS campagne**, laissée telle quelle : les neuf preuves des
deux enveloppes partent au navigateur avec leurs identifiants, via
`world.additional_decks`. C'est le comportement d'origine du pack, et hors
campagne le secret ne vit qu'une partie. La fermer demanderait de filtrer les
cartes non visibles dans `Card.Render`, ce qui touche le rendu de TOUTES les
cartes du jeu.


## 9. Après le câblage

Par ordre d'intérêt :

1. ~~**Écrire `next_evol.json` et `aoa.json`**~~ **FAIT le 10/8/2026.** Les
   deux sont jouables, leurs clés vérifiées et leurs effets éprouvés à la
   sonde : l'environnement « Équipe Rassemblée » entre en jeu pour
   `next_evol`, et le MALUS des Réfugiés Paniqués atterrit dans le deck pour
   `aoa`, dans les deux cas seulement avec le carnet. Méthode d'origine, sur
   le modèle de `mts.json` ou de `mut_gen.json` (§6) : relever les clés exactes dans le `campaign.py` de
   chaque pack, récupérer l'ordre des scénarios dans `data/sets_info.json`,
   écrire résumés et enjeux en français, puis passer
   `tools/verifier_campagnes.py`. C'est ce qui manque pour que ces deux
   boîtes, déjà câblées côté moteur, deviennent jouables depuis l'écran.
   `mut_gen.json` est fait, et éprouvé à la sonde sur les cinq scénarios :
   mise en place de campagne, rôle conservé d'un scénario à l'autre, porte
   « manigance vaincue » ouvrant l'amélioration suivante (avec son témoin
   négatif), Jubilé ralliée, allié CAPTIVE remélangé, et carnet sortant écrit.
2. ~~**Corriger la sonde pour lire `campaign_log_last_file`**~~ **FAIT le
   10/8/2026** (§8), en même temps que l'écriture atomique des campagnes, du
   carnet sortant et des hauts faits.
3. ~~**Identité verrouillée, deck modifiable** entre deux scénarios~~
   **FAIT le 10/8/2026.** La fiche de scénario porte un bouton « Modifier les
   decks » (absent tant qu'un scénario est en cours), qui renvoie à l'écran de
   préparation avec le brouillon marqué `modifie`. Au retour, l'écran des
   campagnes REMPLACE l'équipe au lieu d'en créer une : c'est la seule chose
   qui distingue les deux branches, et un `modifie` perdu fabriquerait une
   deuxième campagne sans le moindre message. La règle du livret est tenue au
   retour, jamais avant : si les identités ont bougé, on refuse tout et on
   n'écrit rien. Éprouvé par `npm run campagne-decks` (trois cas : création,
   même identité avec un autre deck, identité changée), et le test a été mis
   au rouge exprès en désarmant la branche de modification — il a bien vu la
   seconde campagne apparaître.

   **L'équipe revient déjà en place**, dans l'ordre des sièges : le brouillon
   emporte l'équipe enregistrée sous la clé `equipeActuelle`, et la préparation
   la repose (héros retrouvé par sa CARTE d'identité, jamais par son nom, qui
   est traduit à l'affichage). Le geste demandé est donc d'ajuster un deck, pas
   de refaire une équipe, et le refus des identités devient un filet plutôt
   qu'un passage obligé. Deux clés distinctes, et non une seule : c'est
   l'arrivée de `equipe` qui signale au retour que la préparation a validé
   quelque chose. Les confondre enregistrerait une modification que personne
   n'aurait faite, au premier passage sur l'écran.

   Le deck déjà joué n'appartient à aucune liste de l'écran (ni base, ni
   sauvegardé, ni package d'aspect) : il reçoit sa propre entrée, « Deck actuel
   de la campagne », en tête et retenue. Elle est tenue par un registre à part
   (`DECKS_CAMPAGNE`, par siège) et non par l'état du joueur, parce que
   re-cliquer son propre héros appelle `assignHero`, qui remet le deck de base.
   Sans ce registre, ce clic de curiosité perdait le deck de la campagne sans
   aucun moyen d'y revenir.

   Ce que ça ne fait toujours pas : l'interdiction de retirer les cartes
   gagnées en campagne n'est pas contrôlée. Et la mesure ne peut pas se faire
   sur `deck.name`, que `validerEquipeCampagne` réécrit avec le nom du héros :
   deux decks différents s'appellent pareil une fois enregistrés.
4. ~~La défaite finale en campagne experte qui perd la campagne~~ **FAIT le
   10/8/2026.** La règle a été relevée dans les six livrets, et AoA s'écarte des
   cinq autres sur les DEUX points : sa condition n'est pas la défaite mais la
   mission (« If the Protect the Professor MISSION side scheme was defeated,
   the players saved Professor X and win the campaign! »), et elle ne porte pas
   la mention *Expert Campaign Only*. D'où deux formes déclarées sur le
   scénario final, dans `defaite` : `partie_perdue` (cinq boîtes, expert
   seulement) et `cle_absente` (aoa, sur `Professor Saved`). La clé morte
   `expert.defaite_finale_perd_la_campagne`, que trors et sm déclaraient et que
   rien ne lisait, a disparu : une seule source de vérité.

   La décision vit dans `ui-app/src/board/campagne/defaite-campagne.ts`, module
   pur, éprouvé par neuf cas dont ceux qui ne doivent PAS perdre la campagne
   (scénario intermédiaire, mode standard, partie gagnée, règle sans clé). Le
   panneau de récompenses s'ouvre désormais aussi à la défaite, mais seulement
   quand elle perd la campagne, et il n'affiche alors ni épilogue ni champ :
   une partie perdue ne rapporte rien. Côté moteur, `CollectAoA` consigne
   `Professor Saved`, prouvé à la sonde avec témoin (sans la clé de mission :
   absent ; avec : `"Professor Saved": "1"`).

   **Le haut fait de fin de campagne est fait, lui aussi** (même date) : trois
   entrées, « Chroniqueur » (terminer une campagne), « Chroniqueur × 3 » (trois
   boîtes différentes) et « Increvable » (une campagne experte menée à son
   terme). Le partage est net : `resume_campagnes()` côté serveur transforme
   les fichiers du disque en `{code, difficulte, gagnee}`, et
   `game/achievements.py` décide à partir de ce résumé sans jamais lire un
   fichier. Une campagne perdue au dernier scénario ne compte pas, et le nombre
   de scénarios vient de la définition livrée, jamais d'un 5 en dur.

   L'évaluation se déclenche dans `/save_campagne` et pas à la fin de la
   partie : le scénario final est gagné AVANT que le panneau de récompenses
   n'écrive `termines`, donc à la fin de partie la campagne n'est jamais encore
   terminée. Éprouvé par `npm run campagne-hauts-faits`, qui traverse les deux
   moitiés par le serveur — un banc sur l'une ne prouverait rien sur l'autre.
5. **Éprouver `cartes_sous_complot` et `pv_restants` en jeu.** Ils sont testés
   unitairement sur des formes mesurées, mais n'ont jamais été vus dans une
   vraie fin de scénario Zola ni en campagne experte. C'est exactement le
   contexte où le bug des armes expérimentales s'était glissé — un détecteur
   plausible qui relevait quatre cartes au lieu d'une.
6. **`gmw`** : **en cours.** Le moteur de campagne est écrit et éprouvé
   (`src/cards/pack/gmw/campaign.py`, les cinq manigances 1A appellent
   `CampaignSetup`), et `data/campagnes/gmw.json` déclare ses 11 clés, toutes
   reconnues par `verifier_campagnes.py`. La boîte apparaît désormais dans
   l'écran des campagnes, qui en compte sept.

   Deux mesures à la sonde, bytecode recompilé, chacune avec témoin : le
   Chasseur de têtes et la manigance de campagne entrent bien en jeu aux cinq
   scénarios, et les cartes du Marché enregistrées au carnet rejoignent le deck
   (33 cartes sans, 35 avec deux cartes achetées).

   **Les planches sont découpées** (16 pages vers `public/stories/gmw/`), et
   `tools/pages_livret.py` a appris au passage qu'une intro peut tenir sur une
   double page : gmw ouvre sur deux planches qui ne se lisent qu'ensemble.

   **Le Marché est fait.** C'est la seule boîte du jeu où une monnaie traverse
   les scénarios. L'écran est déclaré par les données (bloc `marche` de
   `gmw.json` : bornes des cartes, clés du carnet, titre, aide) et non en dur :
   aucune autre boîte n'affiche le bouton. Le prix est lu sur la carte
   elle-même (`Unit Cost X` dans son texte), jamais recopié. Acheter soustrait
   du solde, inscrit la carte au carnet et enregistre ; le moteur la remet au
   deck à chaque mise en place suivante.

   Éprouvé par `npm run campagne-marche`, trois cas avec témoins : avec 3
   unités la carte à 1 est achetable et celle à 4 ne l'est pas, l'achat retire
   bien le prix et écrit au carnet, et une carte déjà achetée reste hors de
   portée même avec 9 unités — pendant que celle à 4, elle, redevient
   achetable.

   **Une carte du Marché ne s'achète qu'une fois par CAMPAGNE, équipe
   confondue.** Ce n'était pas un choix à faire : le livret le dit à la
   dernière phrase de la section, « Only one copy of each card from The Market
   can be used during a campaign **for the players as a group** ». La première
   version limitait par JOUEUR, faute d'avoir lu cette phrase — mon extraction
   du PDF la coupait. À quatre joueurs, l'écart est majeur : les 28 cartes se
   partagent au lieu d'être offertes à chacun.

   L'écran distingue les deux cas, parce que ce n'est pas la même information :
   « Dans le deck » pour la sienne, « Prise » en gris pour celle d'un
   coéquipier. Le quatrième cas de `npm run campagne-marche` le tient, avec
   témoin : remis en limite par joueur, il devient rouge.

## 10. Le panneau de récompenses, de bout en bout

Ajouté le 11/8/2026. C'est le point de passage **obligé** de toutes les
campagnes — rien n'entre dans un carnet sans lui — et aucun test ne le
traversait. Seules ses briques pures étaient éprouvées (`preremplissage`,
`detecteurs`, `defaite-campagne`, `reprise-campagne`). Trois câblages en
dépendaient sans preuve : qu'il s'ouvre au bon moment, qu'il enregistre ce qu'il
affiche, et qu'il appelle `/reinitialiser_enquete` à la défaite du scénario 5.

`ui-check/tests/campagne-panneau.spec.ts` mène de **vraies parties de campagne**
jusqu'à leur fin. Trois cas : victoire au scénario 1 (le panneau s'ouvre,
enregistre, et renvoie à l'écran des campagnes), défaite hors dernier scénario
(le panneau ne s'ouvre pas, rien n'est reporté), défaite au scénario 5 en
standard (le panneau s'ouvre sur la reprise et re-prépare l'enquête).

### Comment une vraie partie est menée dans un test

Deux contraintes qui se contredisent presque :

- **le plateau doit être ouvert** : le moteur attend un client avant de poser sa
  première question, et c'est le plateau qui affiche le panneau ;
- **répondre en cliquant serait intenable** : la mise en place de Black Widow
  demande déjà de choisir un sbire parmi dix, et chaque scénario a ses propres
  questions.

D'où le montage : on ouvre le plateau, mais on répond par `/get_ask` + `/post`,
exactement comme le fait le navigateur, en prenant la **première option légale**.
C'est le pilote de `tools/sonde_campagne.py`, transposé en HTTP. La fin de partie
est ensuite forcée par `/debug`, la console que le joueur a sous la main :
`Damage("Black Widow", 100)` pour une victoire, `Eliminate(0)` pour une défaite.

Trois pièges relevés en montant ce test :

- **Le mode fixture ne convient pas.** `/app/board.html?etat=<fichier>` affiche
  un état enregistré en lecture seule et ne rend **jamais** l'écran de fin de
  partie. C'est volontaire, et il faut que ça le reste : le panneau écrit dans
  les campagnes, ouvrir une fixture ne doit pas pouvoir en modifier une.
- **Sans navigateur, rien ne démarre.** Piloter uniquement par HTTP ne suffit
  pas : `/get_ask` reste vide tant qu'aucun client ne s'est connecté.
- **`addInitScript` repose la clé à chaque navigation.** On ne peut donc pas
  vérifier que le panneau efface `mc-campagne-partie` : valider renvoie à
  `/campagne.html`, et le script de test réécrit la clé au passage. Le signe
  observable retenu est la navigation elle-même.

⚠️ Ce test lance de **vraies parties** sur le serveur visé : toute partie en
cours y est perdue. Même précaution que `lancement-partie.spec.ts`.
`npm run campagne-panneau`.

## 11. Ce que le jeu relève tout seul (11/8/2026)

Le mode campagne promet une chose simple : **le joueur ne recopie rien**. Cette
section dit où en est cette promesse, ce qui a été corrigé pour la tenir, et ce
qui reste — volontairement — une décision de joueur.

### Deux récompenses se perdaient en silence

`Marauders Defeated` et `Morlocks Saved` (NeXt Evolution, scénario 1) étaient
**lues** au scénario 2 (`RemoveMaraudersDefeatedBeforeSetup`,
`MorlocksSavedSearch`) et **écrites par personne**. `CollectNeXt` ne les
produisait pas, et les champs sont déclarés `type: "auto"` : l'écran ne les
demandait donc pas non plus. Résultat, le scénario 2 retirait zéro Maraudeur du
deck du vilain et ne donnait aucune carte — sans un mot, à toutes les parties.

Le livret (p.9) : « Record the title of each villain under Routed […] Record the
number of Morlock allies still in play ». Les deux sont câblées dans
`CollectNeXt`, avec les `card_id` plutôt que les titres (le lecteur du scénario 2
accepte les deux, et un identifiant survit à la traduction).

Éprouvé sur une vraie partie, et mis au rouge exprès en désarmant le collecteur :
`ui-check/tests/campagne-releves.spec.ts`.

### La piste de réputation de Sinister Motives se calcule

Les six conditions imprimées sous la piste (livret sm p.22) sont **six lectures
de la table**, pas des décisions :

    (+X) Victory points in the victory display
    (+1) No minions in play
    (+1) No side schemes in play
    (+1) No threat on the main scheme
    (+1) Fewer than 1 acceleration tokens in play
    (+1) No defeated identities

Le joueur les recopiait à la main dans un champ `choix`. Elles sont désormais
relevées par le détecteur `conditions_reputation`, et le champ est `auto` — donc
pré-rempli, et **toujours corrigeable** (un champ `int` reste éditable dans le
panneau, ce qui laisse la main à qui joue avec la piste papier).

Clés MESURÉES sur une vraie partie de Sandman, jamais déduites : la menace de la
manigance principale est `info.k_threat` (un JETON, pas un compteur `c_`), les
pions accélération `info.k_acceleration_token`, les points de victoire
`info.victory` sur chaque carte de la pile de victoire. Un sbire **engagé** n'est
pas dans `area_villain` : ne lire que cette zone donnerait un point de trop.

**Le cumul ne vit pas dans le détecteur.** La piste s'ajoute aux nœuds déjà
marqués ; le détecteur ne voit pas le carnet et ne rend que ce que la partie vient
de gagner. La somme est faite par `preRemplir`, via l'attribut `cumulatif` du
champ. Ce que le MOTEUR relève n'est jamais additionné une seconde fois : son
collecteur cumule déjà (`Scenarios With A Cleared Board Member` en est l'exemple).

### Ce qui reste au joueur, et pourquoi ce n'est pas un manque

Après cet audit, **aucun champ `auto` n'est sans source**. Les seuls champs qui
attendent encore une saisie sont des DÉCISIONS que le livret confie au joueur :

| Champ | Ce que dit le livret |
|---|---|
| `Tech Upgrade`, `Basic Upgrade` (trors) | « each player chooses » une amélioration |
| `S.H.I.E.L.D. Tech` (sm) | trois tirées au hasard, « that player **may choose** 1 » |
| `Aspect Advantage` (sm) | une carte de SA COLLECTION, hors du jeu |
| `Planning Ahead` (sm) | « chooses one card from their deck » |
| `Osborn Tech` (sm) | « Choose one at random » — un tirage, mais à des paliers de piste que le PDF ne donne pas en texte lisible |

`Osborn Tech` est le seul cas discutable : c'est un pur tirage au hasard, donc
automatisable — mais seulement si l'on sait À QUELS PALIERS il se déclenche. Le
moteur n'en connaît qu'un (`value >= 1`) et mélange toutes les cartes notées ; la
piste imprimée en montre trois, à des hauteurs que l'extraction texte du livret
ne rend pas. Tirer une carte à chaque victoire ajouterait des pénalités que le
livret ne demande pas : on préfère laisser le joueur suivre sa piste. Relever les
trois paliers sur la planche `public/stories/sm/` fermerait cette dernière case.

### Le vérificateur refuse maintenant deux silences de plus

`tools/verifier_campagnes.py` comparait les clés déclarées aux chaînes du moteur.
Il vérifie en outre, depuis le 11/8/2026 :

- qu'une `detection` déclarée **existe** dans `detecteurs.ts` (les `case '<nom>'`
  de `detecter()` sont lus dans le fichier, pas recopiés). Une detection inconnue
  ne lève rien à l'exécution : le champ reste vide, la récompense disparaît.
  Mis en défaut exprès sur `cartes_en_jeux` : il refuse et nomme le champ ;
- que `deck: "requis"` porte bien `parJoueur` (sans quoi la carte imposée ne
  désigne le deck de personne) et que sa valeur est connue.

### Le pilote des vraies parties, et ses trois pièges

`ui-check/pilote-campagne.ts` sort le montage du §10 de `campagne-panneau.spec.ts`
pour le partager. `campagne-panneau` garde sa copie : c'est la référence du
montage, et le lier au module partagé ferait qu'une retouche ici casse la preuve
du panneau sans qu'on y pense.

1. **Une commande de console se vise par OBJECT ID (`c49`), jamais par nom ni par
   card_id.** Le nom imprimé des cartes uniques commence par une étoile
   (« * Blockbuster »), que le descripteur retire : une commande bâtie sur le nom
   affiché ne trouve rien, et la console ne s'en plaint pas. Pire, un card_id
   ABSENT DU JEU fait **fabriquer** la carte (`FindOrCreateFace`) dans la zone mise
   de côté — et `scenario.py` refuse alors la victoire, qui exige
   `aside_deck.FindCard(card_type=Villain) == None`. Mesuré sur Sandman : les deux
   stades vaincus, la zone du vilain vide, et la partie qui ne se terminait
   JAMAIS ; deux doublons de Sandman I dormaient dans la zone mise de côté.
2. **`PutIntoPlay` n'accepte qu'UN argument** côté console (`PutIntoPlay(carte)`).
   L'appeler autrement lève, et l'erreur suivante a abattu le moteur. Un moteur
   mort continue de répondre 200 sur `/get_world` avec l'état FIGÉ de la partie
   précédente : toutes les commandes semblent alors n'avoir aucun effet et on
   accuse la commande. `ouvrirEtMettreEnPlace` refuse désormais de continuer si la
   première lecture ne montre aucune phase de mise en place.
3. **La console n'exécute ses commandes qu'au prochain cycle du moteur.** Il faut
   répondre (`/get_ask` + `/post`) après l'envoi, sinon on mesure l'état d'avant.
   Corollaire : `PlaceThreat` et `SetThreat` n'ont, eux, **aucun effet** quel que
   soit le moment — mesuré sur la manigance principale de Sandman et sur la mission
   45170a d'aoa. Rien de ce qui dépend de la menace ne se pilote depuis un test.

### La sonde ne remplace pas une vraie partie

`tools/sonde_campagne.py` exécute ses commandes Puzzle « en direct, pas dans une
file » : un `Puzzle.Damage(vilain, 100)` retire bien les points de vie, mais la
réponse forcée « After a villain is defeated » ne part jamais. Mesuré sur Morlock
Siege : sept vilains frappés à 100, **zéro vaincu**, rien sous « Routed ». Tout ce
qui dépend d'une réaction en chaîne se mesure en partie, par le pilote.

## 12. Les trois autres chantiers du 11/8/2026

### Une carte inscrite au carnet ne sort pas du deck

Livret trors p.3 : « Added cards must be included in the player's deck for the
rest of the campaign. » Dans ce jeu, **la plupart des cartes gagnées vivent au
carnet et non dans le deck enregistré** : le moteur les repose à chaque mise en
place depuis leur clé (améliorations Tech de trors, matériel S.H.I.E.L.D. de sm,
allié de campagne d'aoa, cartes du Marché de gmw). Personne ne peut donc les
retirer d'un deck où elles n'ont jamais été, et la règle est tenue par
construction — c'est ce qui rendait l'entrée de TODO trompeuse.

**Une** récompense fait l'inverse et cherche la carte DANS le deck du joueur :
« Planning Ahead » (sm, Réputation 17). Mesure à la sonde, avec témoin : carte
notée présente dans le deck, elle arrive EN MAIN à la mise en place ; carte notée
absente, **il ne se passe rien** — pas d'erreur, pas de message, la récompense
disparaît. D'où un refus au retour de « Modifier les decks », le seul moment où
un deck de campagne change. Déclaré par les données (`"deck": "requis"` sur le
champ) et non en dur, comme tout le reste du format.

Trois cas dans `ui-check/tests/campagne-cartes-imposees.spec.ts`, dont le témoin
inverse (la carte est toujours là, la modification passe), et le contrôle a été
désarmé exprès pour vérifier que le cas de refus tombe bien au rouge.

### Le score de réputation final (sm)

Dernière case du carnet officiel que le jeu ne demandait jamais. Livret sm p.5 et
p.17 (encart VICTORY du scénario 5, sous « Optional ») : recalculer une dernière
fois les Conditions, marquer les nœuds, puis noter un score égal au nombre de
nœuds marqués.

Sa place est le **bilan de fin de campagne**, pas le carnet : aucune mise en place
ne le relit, et l'y mettre aurait exigé une clé que le moteur ne connaît pas —
`verifier_campagnes.py` la refuserait, à juste titre. Il vit donc sous
`scoreFinal`, dans la campagne. Le bloc est déclaré par les données (`bilan` dans
`sm.json`) : aucune autre boîte ne l'affiche, et c'est ce que tient le troisième
cas de `ui-check/tests/campagne-bilan.spec.ts`.

### Deux fausses pistes, mesurées et refermées

**Les alliés retirés de la campagne (trors) ne reviennent PAS au scénario 5.**
Le soupçon était net : `EachPlayerAddRescuedAlliesToTheirDeck` remet tous les
`Rescued Allies` au deck aux niveaux ≥ 4, sans regarder
`Allies removed from the campaign`. Mesure avant de corriger quoi que ce soit :
avec `{"Player 1 Rescued Allies": "04097;04098", "Allies removed from the
campaign": "04098"}`, 04097 arrive dans `player_deck` et **04098 part dans
`area_removed`**. C'est `the_rise_of_the_red_skull_remove_allies` (04128a.py) qui
le fait, à la mise en place du scénario 5. Propriété non évidente, écrite ici pour
qu'on ne « corrige » pas ce qui marche.

**Professor X : CÂBLÉ le 12/8/2026**, après deux mesures qui disent où le
mécanisme vit et où il ne vit pas. Voir §16.

### La fuite hors campagne : FERMÉE le 12/8/2026 (voir §17)

Ce qui suit reste vrai du deck de rencontre, mais plus des preuves d'aos.

### La fuite hors campagne est STRUCTURELLE, pas propre à aos (mesurée)

Le défaut assumé disait : « les neuf preuves des deux enveloppes partent au
navigateur avec leurs identifiants ». Mesure faite le 11/8/2026, sur une vraie
partie de Baron Zemo lancée **hors** campagne :

    deck de rencontre     : 33 cartes, 33 face cachée, 33 card_id lisibles
    decks additionnels    : les 9 preuves, is_face_up = false,
                            visible_for_players = [] … et card_id en clair

Autrement dit, les preuves ne sont pas un cas particulier : **tout le deck de
rencontre** part au client avec ses identifiants. `Card.Render` envoie toujours
`card_id`, même quand `visible_for_players` est vide — le client est censé afficher
`down_card_ids` à la place, mais rien ne l'y oblige.

Deux conséquences, et c'est ce qui tranche la question :

- fermer la fuite des seules preuves serait un pansement : qui lit la console
  pour connaître la taupe lit aussi le deck de rencontre entier ;
- le correctif propre a un critère net, déjà transmis : ne pas envoyer `card_id`
  quand `visible_for_players` est vide. Il touche le rendu de TOUTES les cartes
  du jeu, donc il se fait avec sa propre campagne de tests, pas en passant.

En campagne, la fuite est déjà fermée à la racine : aucune carte de preuve n'existe
tant que le joueur n'a pas le droit de la voir (§8 bis). C'est cette approche-là —
ne pas fabriquer plutôt que ne pas rendre — qu'il faudra reprendre si l'on veut
fermer le mode hors campagne.

### Le pilote sait JOUER, et les deux derniers angles morts sont tombés

Ce qui lui manquait tenait en deux caractères : **`{}`**. Le contrat le dit depuis
toujours (`ui-app/src/board/moteur.ts`, `envoyerReponse(null)`) — poster `{}`
signifie « je ne fais rien », et c'est ce qui **termine une phase de joueur**. Sans
lui, le pilote répondait la première option légale en boucle : aucune phase ne se
terminait, la menace ne montait jamais, le vilain ne jouait pas. Tout ce qui pend à
une fin de phase était hors de portée, et on croyait le problème ailleurs (les
commandes de console, la menace, la sonde).

`avancerLaPartie()` suit quatre règles, dans cet ordre :

1. **accepter les Réponses et les Interruptions.** Ce sont les crochets du
   scénario (« Place 2 secret counters… », « Advance to stage 2A ») : les refuser
   fige l'histoire, et c'est précisément ce qu'on veut voir se déclencher ;
2. **retenir « End Phase »** : c'est lui qui fait tourner les phases ;
3. **passer si le moteur l'autorise** (`show_cancel`). On ne joue donc aucune
   carte, et l'on n'a jamais à payer de ressources ;
4. sinon la question est FORCÉE : répondre la première option dont les cibles sont
   tenables.

`avancerJusquALaQuestion()` s'arrête **sur** une question sans y répondre. C'est la
seule façon de la voir à l'écran : une réponse par HTTP la fait disparaître avant
que le DOM n'ait bougé.

Les deux entrées, fermées dans `ui-check/tests/campagne-accusation.spec.ts` :

- **les preuves gagnées EN PARTIE au scénario 5.** Le livret p.19 n'en donne
  aucune à la victoire, contrairement aux scénarios 1 à 4 : elles se gagnent par la
  Réponse de l'étape 1B (`50167b`), un `AfterPhaseEnd`. Mesuré : la preuve `50190`
  entre en jeu, et l'invariant tient — une preuve gagnée n'appartient **jamais** à
  la combinaison de la taupe, puisque l'enveloppe S.H.I.E.L.D. en est exactement le
  complément ;
- **les trois questions de l'accusation, vues dans l'interface.** La chaîne avance
  par ses propres Réponses jusqu'à « The Accusation », qui demande un moyen, un
  mobile, puis une occasion. Les trois choix s'affichent dans la **demande
  centrale** (`DemandeCentrale.tsx`, qui nettoie le préfixe `p_` de
  `AskChoosePaper`), on y répond EN CLIQUANT, et aucune question ne demande ensuite
  un membre du Conseil : l'accusé découle de la combinaison, comme le livret le veut.

Mis au rouge exprès en désarmant le `passer` : les deux cas tombent.

**Ce qui reste hors de portée du pilote** : jouer une carte (il faudrait choisir et
payer des ressources) et donc déjouer une manigance. C'est ce qui manque encore à
la branche « Professeur sauvé » d'aoa, et `PlaceThreat`/`SetThreat` n'y aident pas
(aucun effet depuis la console).

## 13. Le pilote complet : il joue, il ne gagne pas (12/8/2026)

Le pilote savait mener les phases (§11). Il sait maintenant faire les GESTES du
jeu, et le geste qui débloque tous les autres est **payer**.

### Il paie comme le plateau, pas comme une copie du plateau

`ui-check/pilote-campagne.ts` **importe** `ui-app/src/board/ask.ts`, qui n'a pas un
seul import et sert déjà au plateau à décider qu'une action est prête à partir.
`ressourcesPour()` empile les moyens que le moteur propose jusqu'à ce que
`reponsePrete()` dise oui : la même fonction que celle qui débloque le bouton
« Valider ». Un coût exprimé en TYPES (« BY » = une énergie ET une mentale) ne se
satisfait donc pas en comptant, un « UpTo » se paie à zéro, et une carte à double
ressource vaut deux d'un coup — sans une ligne de règle réécrite ici. Dupliquer
aurait produit deux vérités qui dérivent en silence.

### La conduite, et pourquoi chaque défaut est ce qu'il est

`avancerLaPartie(page, request, arret, tours, conduite)` :

| Réglage | Ce qu'il fait |
|---|---|
| `dejouer` | complots à déjouer en priorité, par object_id |
| `attaquer`, `attaquerDAbord` | attaquer, et qui viser d'abord |
| `jouerDesCartes`, `jouerDAbord` | jouer ce qu'on peut payer, en préférant des types (`Ally`…) |
| `actions` | déclencher une action par motif sur son nom |
| `resterEnHeros` | reprendre la forme héros : un alter-ego n'a ni attaque ni déviation |
| `equilibrer` | déjouer la manigance principale à mi-chemin de sa cible, attaquer sinon |
| `seDefendre` | se défendre. **Faux par défaut**, et c'est capital |

**La défense est facultative, et son défaut est NON.** Une défense coûte
l'activation du héros. En se défendant à chaque attaque, il arrive épuisé à son
tour et le moteur ne lui propose plus ni `Attack` ni `Thwart` : mesuré sur Rhino,
le pilote « déjouait » sans qu'aucune option `Thwart` ne soit jamais offerte, et la
menace montait jusqu'à la défaite. Encaisser est d'ailleurs le choix courant d'un
joueur.

**Le seuil d'`equilibrer` est à mi-chemin, pas à deux pions de la fin.** La menace
saute par paliers (une manigance qui s'avance, un pion accélération, un boost) :
avec un seuil à « cible - 2 », Rhino est passé de 2/7 à 7/7 dans le même bloc de
tours, le vilain à 3 points de vie. Exception : un vilain presque mort se termine.

**Tous les sièges sont servis.** Chaque joueur a ses propres questions sur
`/get_ask?p=<siège>`. N'en servir qu'un fait attendre le moteur indéfiniment :
mesuré à deux héros, la mise en place ne se terminait jamais.

### Ce qu'il sait faire, prouvé geste par geste

`ui-check/tests/campagne-pilote.spec.ts` ne vérifie aucune règle de campagne : il
vérifie LE PILOTE, sur des faits mesurés. C'est le filet des autres tests de vraies
parties — si le contrat de `/post` change, ça se voit ici, et pas dans un test de
campagne qui échouerait pour une raison obscure.

- il paie et pose devant lui une carte dont le coût est > 0 (compter les cartes qui
  quittent la main ne prouverait rien : la main se recharge, et une carte gratuite
  s'y voit comme une carte payée) ;
- il attaque, et le vilain perd vraiment des points de vie ;
- il déjoue, et la menace de la manigance baisse ;
- il **vainc un stade de vilain sans aucun `/debug`** : sur Morlock Siege, un
  Maraudeur part sous « Routed » par le seul effet du jeu ;
- il mène une **tentative de mission** à deux héros (aoa) ;
- il sert les deux sièges jusqu'au bout de la mise en place.

### La tentative de mission, le geste le plus complet du jeu

Et le seul chemin vers « Professeur sauvé ». Il enchaîne : jouer un allié (donc
payer) → l'allié rejoint la mission (`AllyToMission` lui pose un compteur
« mission ») → l'action nommée « Make a mission attempt » de Mission Team, qui
exige au moins un allié à la mission → la tentative défausse des cartes du deck,
apparie leurs icônes à celles des alliés, frappe le surveillant posté avec leur ATK
et retire de la menace avec leur THW, puis pose un compteur d'essai.

Rien de cela ne se pilote autrement : `45170a` annule tout retrait de menace dont
la source n'est pas Mission Team, et un surveillant posté est immunisé à ce qui ne
vient pas d'une tentative. Mesures : dix tours d'action `Thwart` laissent la mission
à 5/5, et `Damage` par la console ne l'entame pas.

### Ce que le pilote ne sait pas faire : GAGNER

Il joue les gestes, il ne joue pas une stratégie. Deux mesures :

- **Rhino** : le vilain descend de 14 à 3 points de vie, et la manigance se complète
  quand même. Achever une partie reste donc l'affaire de `/debug` ;
- **« Professeur sauvé » (aoa)** reste hors de portée, et ce n'est plus une limite
  d'outillage. À deux héros la mission compte **10 menaces** (5 par joueur) et son
  surveillant **10 points de vie**, pour **4 tentatives maximum** avant l'échec.
  Le pilote joue la chaîne correctement — deux alliés à la mission, trois essais,
  le surveillant de 10 à 6 points de vie, la menace de 10 à 8 — et le compte
  n'arrive pas au bout avec des decks de départ. Il y faudrait des decks construits
  pour la mission, c'est-à-dire un joueur, ou une IA de jeu : un autre chantier.

C'est la dernière entrée non couverte du mode campagne, et elle est désormais
documentée par une mesure plutôt que par une supposition.

**DÉCISION du 12/8/2026 : on n'écrira pas de bot qui gagne.** Le pilote reste ce
qu'il est, un outil de test qui sait faire les gestes ; la branche « Professeur
sauvé » se vérifie à la main, en jouant. Ne pas relancer ce chantier — ce qui suit
n'est donc pas une piste, c'est la raison de s'arrêter là.

## 14. Le matériel Osborn se tire tout seul (12/8/2026)

Dernière case du carnet de Sinister Motives qui ne se remplissait pas : le champ
`Osborn Tech: Reputation Track Penalty` était un `choix` **sans options**, où le
joueur tapait des identifiants de cartes à la main, séparés par des points-virgules.
Or le livret ne lui demande aucune décision : « Choose one "Osborn Tech" attachment
**at random** ». Un tirage, le jeu sait le faire.

### Où étaient les paliers, et comment ils ont été lus

Le code du moteur connaissait les seuils de la colonne GAUCHE de la piste (1, 5, 9,
13, 17, 21, 25) et quatre de ceux de droite (5, 9, 17, 25), mais pas les trois
encarts « Osborn Tech ». Le texte du PDF ne les donne pas : la piste est un dessin,
les encarts n'y sont pas numérotés.

Ils ont été relevés sur la planche elle-même (page 22 du livret, rendue en image),
en **alignant les encarts de droite sur ceux dont le seuil est déjà connu** — la
graduation vaut environ 33 pixels par nœud à cette échelle :

| Encart | Hauteur | Palier |
|---|---|---|
| `Setup: Place 1 threat` (droite) | y≈284 | **5** — connu du code ✔ |
| `Setup: search a minion` (droite) | y≈415 | **9** — connu du code ✔ |
| `Setup: search a side scheme` (droite) | y≈682 | **17** — connu du code ✔ |
| `Setup: deal 1 encounter card` (droite) | y≈931 | **25** — connu du code ✔ |
| **1er « Choose one Osborn Tech »** | y≈164 | **1** (l'étoile, comme le S.H.I.E.L.D. Tech en face) |
| **2e « Choose one Osborn Tech »** | y≈550 | **13** (à la hauteur d'ENHANCED, connu du code) |
| **3e « Choose one Osborn Tech »** | y≈814 | **21** (à la hauteur du Helicarrier, connu du code) |

Les quatre premières lignes sont le témoin : la méthode retrouve exactement les
paliers que le moteur applique déjà. Les trois autres en découlent.

### Le tirage, et ses deux propriétés qui comptent

Déclaré par les données (`tirage: { cle_piste, paliers }` plus les six `options`),
donc aucune boîte en dur. `cartesDuTirage()` est une fonction pure :

- **cumulatif et irréversible** : ce qui est déjà noté reste noté, on ne complète
  que ce qui manque. Sans cela, un scénario rejoué re-tirerait tout et les pénalités
  du deck de rencontre changeraient entre deux tentatives ;
- **le hasard est tiré DEHORS**, une fois, à l'ouverture du panneau
  (`melangerLesTirages`), et passé comme un ordre figé. `preRemplir` tourne dans un
  `useMemo` qui dépend du monde : un `Math.random()` à l'intérieur ferait changer les
  cartes à chaque trame du moteur, sous les yeux du joueur.

Le champ reste **corrigeable** : les six cartes s'affichent en vignettes cliquables
(elles ont maintenant des `options`, ce qui manquait aussi), et qui préfère tirer
sur sa table peut cocher les siennes.

### Ce que le vérificateur refuse désormais

`tools/verifier_campagnes.py` contrôle la forme d'un `tirage` : des paliers entiers,
positifs et **croissants** ; des `options` non vides ; un `type: "auto"` ; et surtout
une `cle_piste` **déclarée AVANT le champ**. Ce dernier point n'est pas cosmétique :
`preRemplir` parcourt les champs dans l'ordre du fichier et lit la piste qu'il vient
de calculer, relevé du jour compris. Une piste déclarée après ferait tirer sur le
total de la veille. Mis en défaut exprès sur des paliers décroissants : il refuse et
nomme le champ.

Éprouvé en vraie partie (`campagne-releves.spec.ts`) : piste à 12 au carnet, le
relevé de la partie la fait franchir 13, et **deux** cartes Osborn différentes sont
inscrites — celles du palier 1 et du palier 13. Plus dix cas vitest sur la fonction
pure, dont « ne re-tire jamais ce qui est déjà noté » et « ne peut pas tirer plus de
cartes qu'il n'en existe ».

**Le carnet de Sinister Motives se remplit désormais entièrement tout seul**, sauf
les trois vraies décisions du joueur : quelle amélioration S.H.I.E.L.D. garder,
quelle carte d'aspect ajouter, quelle carte de son deck préparer.

## 15. Les huit boîtes ont maintenant toutes été JOUÉES (12/8/2026)

Cinq boîtes avaient traversé une vraie partie. Les trois autres —  The Mad Titan's
Shadow, La Genèse des Mutants, Galaxy's Most Wanted — n'étaient validées que par
l'audit texte-vs-code et par la sonde : leurs mises en place avaient été relues
encart par encart contre le livret, mais aucune partie n'avait été menée jusqu'à ce
que le carnet s'écrive. `ui-check/tests/campagne-boites-restantes.spec.ts` comble ça.

Chaque cas vise le relevé le plus caractéristique de sa boîte, et non le plus facile :

| Boîte | Scénario | Ce qui est mesuré |
|---|---|---|
| mts | 1, Ebony Maw | `Campaign Pool: Cosmo` : l'allié (21180b) en jeu à la fin rejoint le pool |
| mut_gen | 1, Sabretooth | `Role` **et** `Frightened Police Defeated` |
| gmw | 1, Brotherhood of Badoon | `Unspent Units` : la monnaie du Marché, qui s'ACCUMULE |

**Le cas de `Role` est le plus intéressant.** Le rôle de Mutant Genesis est choisi
EN JEU, à la mise en place, et remonte au carnet par le **store** du moteur
(`CampaignLog.SetStr`), pas par le collecteur de fin de partie. C'est un chemin
d'écriture que rien n'éprouvait, et il décide de tout le role-building de la
campagne : sans lui, les améliorations des cinq scénarios seraient tirées au hasard.

**`Unspent Units` porte son propre témoin.** Le carnet part à 4 unités et le test
exige que le total AUGMENTE : un collecteur qui remplacerait au lieu d'ajouter
rendrait 1 à 3 unités, donc moins que 4, et le cas tomberait. Le livret est net :
« add these to units you already have ».

**Cosmo a un témoin séparé**, et il a fallu le faire. Une condition posée à la
console (`PutIntoPlay`) prouve que la clé APPARAÎT, mais pas que le moteur la lie à
quoi que ce soit : un collecteur qui écrirait `Campaign Pool: Cosmo` à toutes les
parties passerait pour bon. Le témoin joue donc la même partie SANS Cosmo et lit le
carnet sortant : le collecteur relève des clés, et pas celle-là.

Ce que le désarmement a appris : retirer le `PutIntoPlay` fait tomber le premier cas
sur sa PRÉ-CONDITION (« Cosmo n'a pas été mis en jeu »), pas sur son assertion. Un
test qui ne vérifie pas sa propre mise en scène mesure ce qu'il croit, pas ce qui est.

**Les huit boîtes ont désormais chacune au moins un scénario joué de bout en bout,
carnet écrit et relu.**

## 16. Professor X ne peut plus être joué au scénario 5 d'AoA (12/8/2026)

Livret p.20, instructions SETUP du scénario 5 : « Professor X cannot enter play
during this game. » Le jeu ne l'empêchait pas, et l'entrée était classée « défaut
assumé ». Elle est fermée, et le chemin pour y arriver vaut d'être écrit : deux
mesures ont été nécessaires, chacune éliminant une hypothèse fausse.

### Mesure 1 : le mécanisme ne se diffuse pas depuis le scénario

`AbilityFactory.PlayersCannotPlayCardWhile("AnyPlayer", CardFinder(card_ids=
['32019']))` posé sur la manigance principale (45147a) n'a **aucun effet** :
Professor X mis en main par la console, l'option « Play » reste proposée sans
`failure_reason`. Vérifié jusqu'au bout, en retirant la condition `IsCampaign` puis
en passant `which_card=None` — donc pour TOUTES les cartes, et rien n'était bloqué.

Les quatre usages du moteur sont tous des cartes JOUEUR (un attachement sur
l'identité, ou l'identité elle-même). Ce n'est pas un hasard : la vérification
consulte ce que porte le joueur, pas ce que porte le scénario.

### Mesure 2 : un effet temporaire est porté par la FACE, pas par la carte

Deuxième tentative, sur l'identité du joueur cette fois
(`identity.effect.RegisterTemp(...)`) : toujours aucun effet. La cause est dans
`RegisterTemp` lui-même — `self.face.card.RegisterEffect(ability, self.face, …)` :
l'effet est attaché à **la face**. Or la mise en place de campagne tourne quand le
joueur est encore côté ALTER-EGO. L'effet était donc bien enregistré, sur la face
alter-ego, et devenait inerte au premier passage en forme héros, c'est-à-dire avant
qu'on puisse jouer quoi que ce soit.

**L'interdiction est donc enregistrée sur les DEUX faces de l'identité**, la
courante et celle du héros (`GetHeroFace()`, avec son garde `AssertionError`). C'est
la seule forme qui tienne, et elle tient : l'option « Play » disparaît en campagne,
et reste offerte hors campagne.

### Ce qui est tenu, et ce qui reste approximatif

Ce qui est bloqué, c'est **jouer** la carte : le seul chemin qu'un joueur emprunte
pour la poser. Une capacité qui la mettrait en jeu depuis le deck ou la défausse
passerait encore. Le moteur n'a aucun crochet « cannot enter play » (`grep -rn
"cannot enter play" src/` ne rend rien), et en fabriquer un toucherait la mise en
jeu de toutes les cartes du jeu. L'approximation est donc conservée, mais elle a
changé de nature : ce n'est plus « rien n'est contrôlé », c'est « le geste du joueur
est contrôlé ».

Deux cas dans `ui-check/tests/campagne-professor-x.spec.ts`, dont **le témoin hors
campagne** : sans lui, une interdiction qui déborderait sur toutes les parties
d'En Sabah Nur passerait pour bonne, alors que l'instruction est une CAMPAIGN
INSTRUCTION. Colossus est le héros du test parce que son deck de départ contient
Professor X.

## 17. La répartition des preuves ne part plus au navigateur (12/8/2026)

Le défaut assumé disait : hors campagne, les neuf preuves d'aos partent au client
avec leurs identifiants. Il est fermé, et ce qui a permis de le fermer sans toucher
au rendu de toutes les cartes du jeu tient en une phrase :

**Le secret n'est pas l'existence des neuf preuves — elle est imprimée dans le
livret — c'est leur RÉPARTITION.** Savoir lesquelles trois dorment dans l'enveloppe
A.I.M., c'est connaître la taupe sans jouer. Neuf preuves toutes au même endroit ne
disent rien du tout.

### Ce qui a changé

`PreparingTheEvidence` montait deux piles avec `SetAsideDeck`, et
`SetAsideDeck.Create` les inscrit dans `world.additional_decks`, que `to_descriptor`
rend au navigateur avec le `card_id` réel de chaque carte, face cachée ou non. La
réponse partait donc au client, **triée par enveloppe**.

Désormais, hors campagne comme en campagne :

- les neuf preuves quittent le jeu **toutes ensemble** (`RemoveAllFromGame`). Elles
  atterrissent dans `area_removed`, que le descripteur rend — mais sans dire laquelle
  est où ;
- la combinaison de la taupe est écrite dans le **store**, sous `A.I.M. Envelope`,
  déjà filtrée du carnet sortant par `CLES_SECRETES` ;
- une preuve n'est **fabriquée** qu'au moment où le joueur a le droit de la voir
  (`PreuveEnJeu`), qu'elle soit puisée dans l'enveloppe S.H.I.E.L.D. ou révélée à
  l'étape 3 de l'accusation.

Conséquence agréable : les trois lecteurs (`CartesDeLEnveloppeAim`,
`ShieldEnvelopeHasCards`, `GainCardsFromShieldEnvelope`) n'ont plus qu'un seul
chemin. La branche « hors campagne » a disparu, et avec elle le risque que les deux
modes divergent.

### Les deux régressions que la suite a attrapées

Le premier jet cassait deux invariants, tous deux dans les cas hors campagne de
`tools/test_accusation_aos.py` (27/29). Ils valaient d'être tenus :

1. **« hors campagne : le carnet n'est pas touché ».** `NoterPreuveGagnee` écrivait
   les preuves gagnées sous `Evidence Gained`, une clé qui SORT au carnet — c'est une
   récompense de campagne. Hors campagne il n'y a pas de scénario suivant, et polluer
   le carnet sortant n'a aucun sens. D'où une clé de TRAVAIL,
   `A.I.M. Envelope Gained`, filtrée elle aussi.
2. **« hors campagne : la chaîne s'arrête sur la dernière étape ».** `50168b` lisait
   encore la pile `A.I.M.Envelope` pour attacher les preuves à la taupe. La pile
   n'existant plus, la chaîne s'arrêtait à l'étape 3 **en silence** : aucune erreur
   remontée, juste une manigance qui n'avance pas. Les preuves y sont maintenant
   fabriquées depuis leurs identifiants, campagne ou pas.

Mesure de fermeture, hors campagne : `additional_decks` est vide, et les neuf preuves
sont dans une seule zone. Un cas de `campagne-accusation.spec.ts` le tient, et il
compte les zones plutôt que les cartes — c'est la dispersion qui trahit, pas le
nombre.

**Ce qui reste ouvert**, et n'a pas changé : le deck de rencontre part toujours au
navigateur avec ses identifiants. Y lire l'ordre des cartes est de la triche
ordinaire, pas une déduction cassée, et le fermer demanderait de filtrer `card_id`
dans `Card.Render` pour toutes les cartes du jeu (§12).

## 18. La branche gagnante d'AoA, et le piège qu'elle a révélé (12/8/2026)

Sauver le Professeur **gagne** la campagne (livret p.20). La branche perdante était
couverte depuis le 11/8 ; la gagnante ne l'était pas, et il n'était pas question
d'écrire un bot pour vaincre la mission (§13).

### Le piège : l'écran ne rejoue pas la règle

La première version du test posait une campagne déjà terminée, avec
`Professor Saved` au carnet, ouvrait l'écran et vérifiait la conclusion. **Elle
passait avec ET sans la clé.** La raison est dans `vueConclusion` : elle lit
`campagne.perdue`, un drapeau **posé par le panneau de récompenses**. L'écran des
campagnes n'évalue rien — il affiche un verdict déjà rendu.

Un test qui ne se met pas au rouge ne prouve rien : c'est cette vérification-là qui a
sauvé le cas, pas la relecture du code.

### Ce que le cas fait maintenant

Une **vraie partie** du scénario 5, pour que le panneau évalue le verdict. La mission
n'est pas vaincue — hors de portée — mais la clé est déjà au carnet, et elle survit :
le collecteur d'aoa ne la fournit pas, le pré-remplissage retombe donc sur la valeur
du carnet. C'est exactement la situation d'une équipe qui a sauvé le Professeur.

Mesuré : le panneau n'annonce pas la campagne perdue, son titre dit la victoire de
campagne, le serveur n'a pas de drapeau `perdue`, la clé est toujours au carnet, et
l'écran conclut avec la planche d'épilogue. Désarmé exprès en retirant la clé : le cas
tombe.

**Ce qui reste hors de portée**, et c'est assumé : vaincre la mission en jouant. La
chaîne mesurée s'arrête donc au relevé de la clé — mais tout ce qui en dépend, du
verdict du panneau à l'épilogue de l'écran, est désormais tenu dans les deux sens.

---

## Les trois points assumés sont traités (12/8/2026)

Récapitulatif de la série, chacun repris un par un :

| Point | Décision | Résultat |
|---|---|---|
| Professor X, sc.5 d'AoA | interdire de le jouer | **Câblé** (§16), porté par les deux faces de l'identité |
| Fuite du descripteur | fermer les preuves d'aos | **Fermé** (§17), la répartition ne sort plus ; le deck de rencontre reste lisible |
| « Professeur sauvé » | vérifier ce qui restait vérifiable | **Couvert dans les deux sens** (§18), sauf vaincre la mission en jeu |

## 19. Une campagne à plusieurs, chacun sur son appareil (12/8/2026)

Jusqu'ici, **seul celui qui avait lancé depuis l'écran des campagnes savait qu'il
jouait une campagne.** Les autres avaient un plateau ordinaire : ni panneau de
récompenses, ni règle de défaite, ni carnet, ni règle de reprise.

### Ce que la fiche disait, et ce que la mesure a démenti

La fiche `.planning/todos/2026-08-12-campagne-en-ligne.md` affirmait que le seul
obstacle était la clé `localStorage` `mc-campagne-partie`, posée par
`public/js/campagne/app.js:869` et lue par `contexte.ts`. **C'était faux, et cette
phrase a envoyé le chantier sur une fausse piste.** Il y avait un second obstacle,
en amont et plus dur :

- **L'écran des campagnes lance la partie tout seul, sans jamais passer par le
  salon.** `campagne/app.js:851` compose `joueurs` depuis `campagne.equipe`, pose
  la clé, appelle `launch()`. Les mots « salon », « multi » et « en ligne »
  n'apparaissent nulle part dans ce fichier.
- **Le salon est réservé au hot-seat.** `prepare/app.js:707` fait
  `if (!state.salon.multi || state.mode.id !== "hotseat") return null`, alors que la
  campagne lance avec `mode: { id: "campaign" }`. L'écran de préparation le dit
  lui-même ligne 474 : « Cet écran ne lance donc jamais de partie de campagne. »

**Conséquence : une campagne était TOUJOURS hot-seat.** Les distants n'avaient pas
un plateau qui ignore la campagne — rien ne les convoquait.

### Les deux routes

| Route | Ce qu'elle fait | Ce qu'elle ne peut PAS faire |
|---|---|---|
| `GET /get_campagne_en_cours` | Rend `{id, scenario, nom, equipe}` de la campagne dont `partieEnCours.depuis` est la plus récente, **si la partie du moteur est de campagne** (sinon `{}`) | Rendre le carnet ou le secret. Vérifié sur la **chaîne** de réponse, pas seulement sur l'objet |
| `POST /save_carnet_partiel` | Fusionne des clés de carnet | Terminer un scénario, gagner une campagne, toucher au secret, créer une campagne |

> **Correctif du 07/10/2026.** La route ne répond plus que si la partie tenue par le moteur porte la règle `mode_campaign` (`_partie_du_moteur_est_de_campagne`, `server_campagne.py`), et se tait tant que l'hôte a déclaré une table ordinaire (`get_liens_sieges` pose `table_ordinaire`, tout `/new` ou chargement l'efface). Sans cela, un `partieEnCours` resté armé faisait passer toute partie ordinaire pour la campagne (panneau de récompenses, salon « équipe fixée par la campagne »). Elle ne dit toujours pas QUELLE campagne : c'est la plus récente avec un `partieEnCours`. Le plateau garde sa propre garde, `monde.mode_campaign === true`, avant tout appel réseau (`PanneauRecompenses.tsx`).

La déduction de la première **existait déjà**, enfouie dans
`secret_pour_le_moteur()` : elle a été extraite dans `_campagne_la_plus_recente()`
et verrouillée par un test AVANT l'extraction. Elle ne dépend d'aucun navigateur,
donc elle vaut pour tous les sièges.

`/save_campagne` **n'a pas été modifié**. Il reste le seul à écrire `termines`,
`perdue` et `partieEnCours`. Un siège distant ne doit pas pouvoir déclarer la
campagne gagnée, et le lui interdire **par la forme de la route** coûte moins cher
que de le vérifier partout ailleurs.

### La règle des droits, en une phrase

**Un champ `parJoueur` appartient au siège qu'il nomme, tout le reste appartient à
l'hôte** (`droits-carnet.ts`). Deux conséquences volontaires : l'hôte ne
s'approprie pas les champs personnels des autres, sinon deux personnes
rempliraient la même case ; et un siège inconnu (page sans `?p=`) ne peut rien
écrire.

Le siège vient de `?p=`, **pas de la vue affichée** : regarder la table d'un autre
ne fait pas de nous ce joueur.

### La répartition des sièges : rien à écrire

Le siège N tient `equipe[N]`. C'est **déjà** ce que fait le moteur, qui reçoit
`players` dans cet ordre. L'équipe d'une campagne étant figée par le livret,
« choisir son héros » n'a aucun sens ici : le salon se contente de dire
« Tu tiens <héros> » (§4.7 de la fiche, jalon absent de la conception initiale).

### Trois choses qui se sont révélées gratuites

1. **`PanneauRecompenses` est monté sans condition de siège** (`board.tsx:1384`).
   Sa seule garde était `lireContexte()`. Dès que le contexte atteint tous les
   sièges, le panneau s'ouvre chez tout le monde, en direct, sans autre travail.
2. **`lireContexte()` n'a que deux consommateurs.** Le passage à l'asynchrone,
   redouté par la fiche, a coûté trois lignes. `lireContexte()` reste d'ailleurs
   en place, purement locale, pour le rapport de bug qui se prend au clic et ne
   doit pas attendre le réseau.
3. **`parJoueur` était déjà pleinement câblé côté UI** : `cleCarnet()` préfixe en
   `Player N <clé>` et le panneau affichait déjà une ligne par joueur. Il ne
   restait qu'à décider qui a le droit d'y écrire.

### Les pièges payés

- **Le poll de l'hôte réécrivait ses propres cases.** Fusionner
  `{...carnet, ...valeurs}` ne suffit pas : une case qu'il vient d'EFFACER est
  retirée de `valeurs` (par `poser`, qui fait `delete`), donc le serveur la
  réinjecte trois secondes plus tard. D'où `cleDUnAutreSiege()`, qui ne reprend que
  les clés `Player N ` d'un autre siège.
- **Le scénario vide entre deux parties.** Entre la validation de l'hôte et son
  prochain lancement, `partieEnCours` vaut `null` et la route rend un scénario
  VIDE. Recharger là renverrait les distants sur un plateau mort
  (`scenarioSuivantLance`).
- **« À choisir avant de continuer » mentait aux distants.** Le panneau leur
  listait des cases appartenant à d'autres joueurs, qu'ils n'ont pas le droit de
  remplir. Relevé par `campagne-multi.spec.ts`, corrigé : le message est réservé à
  qui peut valider.
- **Les fins de ligne, deux fois.** `server_campagne.py` et `prepare/dico-en.js`
  sont en CRLF intégral : un motif en LF ne correspond à rien et l'édition échoue
  sans dire pourquoi. Lire `newline=''`, normaliser en LF, éditer, réécrire en CRLF.

### Ce qui n'est PAS fait

- **Aucune partie n'a été menée à deux navigateurs par un humain.** Le critère
  d'acceptation de la fiche n'est donc pas atteint. En particulier, le salon qui
  dit « Tu tiens <héros> » n'a jamais été vu par des yeux : rien d'automatisé ne
  l'atteint.
- **Le secret d'A.I.M. à quatre sièges** (§4.5 de la fiche) reste à éprouver : que
  la combinaison ne se déduise pas d'un carnet partagé lu par plusieurs. C'est une
  campagne de tests à soi seule.
- **Ce que voyait un invité au salon avant ce chantier** est déduit du code, pas
  mesuré.

## 12. Fear No Evil : la première campagne en ORDRE LIBRE (18/09/2026)

Le livret mc60 (p. 8-9) ne donne pas d'ordre : cinq affaires interchangeables,
chacune contre un vilain UNDERLING au choix, puis Kingpin quand les cinq sont
Completed ou Failed. Avant CHAQUE partie, deux affaires non résolues sont
tirées au hasard et progressent d'une marque (deux marques s'il n'en reste
qu'une) ; à trois marques l'affaire est Failed. Rien de cela n'existait dans le
lanceur, qui joue les campagnes dans l'ordre du fichier (`indexCourant`).

Ce qui a été ajouté, et où :

| Pièce | Fichier | Preuve |
|---|---|---|
| Définition | `data/campagnes/fne.json` : `"ordre_libre": true`, `vilains` (avec `ordre` recommandé), 5 affaires `manigance: true`, Kingpin `final: true` + `catalogue: "kingpin_fne"` | `tools/verifier_campagnes.py` |
| Règles pures | `public/js/campagne/ordre-libre.js` : `tirerLaProgression`, `etatAffaire`, `kingpinDisponible`, `vilainsPossibles`, `inscrireLeVilain`, `scenarioDuCatalogue`, `appliquerLaDefaite` | `node --test tools/tests-lanceur/ordre-libre.test.mjs` (12) |
| Écran | `public/js/campagne/app.js` : `vueCampagneLibre()` (tableau du carnet, tirage, choix de l'affaire et du vilain, partie en cours, défaite déclarée), `lancerScenario(scenario, {catalogue, vilain})`, `estTerminee` | `ui-check/tests/campagne-ordre-libre.spec.ts` (4, `npm run campagne-ordre-libre` avec `UI_CHECK_BASE`) |
| Moteur | `src/cards/pack/fne/campaign.py` (clés du carnet, environnements, marques, Mary, cartes retirées, `CollectFNE`) branché sur la face 1A des six manigances | 27 cas `[fne5]` du harnais |

Les clés du carnet sont partagées entre l'écran et le moteur : « Completed
Scenarios », « Failed Scenarios » (listes `;`), « Progress: <affaire> » (0..3),
« Villain: <affaire> », « Trust Established? », « Mary Defeated? », « Allies
removed from the campaign », et les PV restants par joueur (clé moteur, campagne
experte). L'estampille du carnet sortant est nettoyée (`[^a-z0-9_]`) : « Stop
the Presses! » donnait `stop_the_presses!`, qui ne correspondait à rien.

Deux partis pris, faute de mieux côté plateau :
- le **tirage** est fait par l'écran, une fois par partie, et gardé dans
  `campagne.tirage` tant que la partie n'est pas lancée (un rechargement ne
  retire pas deux fois) ;
- une **défaite** ne fait rien remonter du plateau en standard (le panneau de
  récompenses ne s'ouvre pas) : le joueur la déclare sur l'écran, comme il
  cocherait le carnet papier. En campagne experte l'affaire progresse ; contre
  Kingpin en expert, il choisit l'environnement Completed à retourner, ou la
  campagne est perdue s'il n'en reste aucun.

Piège payé : `WhenCampaignSetup` part APRÈS la mise en place des complots, donc
après leur retournement côté 1B ; avec un complot par joueur (Protection
Racket), la garde « seul le premier complot parle » compare les CARTES, pas les
faces. Et `paper.name` n'a plus l'étoile à l'exécution : `CollectFNE` relit
`paper.is_unique` pour les alliés retirés.

## 13. La BOUCLE de campagne est enfin mesurée, les dix boîtes (19/09/2026)

Tout ce qui précède mesurait une partie. Rien ne mesurait le PASSAGE d'une
partie à la suivante : gagner, écrire le carnet, cocher une récompense, et
retrouver cette récompense à la mise en place du scénario d'après. C'est
pourtant là que vit le mode campagne, et c'est là que huit défauts dormaient.

### L'outil

`tools/test_campagnes.py` est générique et ne connaît aucune boîte. Il monte la
partie 1 en mode campagne avec un carnet entrant, laisse un pilote minimal
jouer jusqu'au tour du joueur, force la fin par `Puzzle.Win()` ou
`Puzzle.Lose()` (ajoutés le 19/09/2026 : rien ne permettait de terminer une
partie à la demande), relit le carnet SORTANT, y fusionne ce que le joueur
cocherait au panneau, monte la partie 2 et mesure son état de départ.

`tools/epreuves_campagnes.py` est la connaissance des boîtes : une liste
d'épreuves, chacune disant le scénario joué, l'état à poser avant la fin, le
carnet attendu, les cases cochées, le scénario suivant et l'état attendu à sa
mise en place. Le vocabulaire de mesure couvre les zones (en jeu, main, deck,
défausse, retirées, victoire, de côté, rencontres reçues) et leurs négations,
`parmi` / `un_parmi` / `aucune_parmi`, les tailles de pile, les compteurs, les
jetons, les statuts, la menace (exacte, minimale, maximale), le deck rencontre,
les dégâts, et `perdue` pour une mise en place qui perd la partie.

    RELEASE=1 PARALLELES=4 CAS_PREFIX=cz \
      ~/marvel-work/python/bin/python3.10 tools/test_campagnes.py \
      "$PWD/.game-src-a" 48000 /tmp/rapport-campagnes.json ["filtre"]

**115 épreuves, 115 vertes, 327 s.** Réparties : fne 6, trors 6, mts 12, gmw 15,
sm 13, mut_gen 13, next_evol 16, aoa 11, aos 19, web_of_deceit 4.

### Les huit défauts trouvés, et ce qu'ils coûtaient

| Boîte | Défaut | Conséquence en partie |
|---|---|---|
| toutes | `CollectFNE` et consorts lisaient `world.game_over` pendant `WhenGameOver`, qui n'est posé qu'APRÈS le message | une victoire Fear No Evil ne cochait jamais l'affaire |
| gmw | le relevé des artefacts filtrait sur un trait « GALACTIC ARTIFACT » qui n'existe sur aucune carte | la case du carnet restait vide, aucun artefact ne revenait chez Nebula, la prime d'unités ne tombait pas |
| gmw | les manigances d'artefact n'étaient pas remélangées au deck rencontre | la punition principale du scénario 4 manquait |
| gmw | « Power Stone Control » cherchait la carte 16110 (Fanaticism) au lieu de 16149, et parmi les améliorations au lieu des attachements | « Vous êtes accusé ! » n'arrivait jamais au scénario 5 |
| gmw | le nom du porteur était relevé sur la face active (« Steve Rogers » en alter-ego) et relu à la mise en place, où tout le monde est en alter-ego | la comparaison ne retombait jamais juste |
| gmw | les unités additionnaient `face.victory`, un BOOLÉEN | deux manigances « Victory 0 » rapportaient 2 unités, un sbire « Victory 2 » n'en rapportait qu'une |
| sm | le matériel S.H.I.E.L.D. était fabriqué sans sa face arrière | la récompense du palier 13 (version améliorée) n'existait pas |
| next_evol | les Maraudeurs vaincus étaient cherchés dans le deck vilain, alors qu'ils attendent dans la réserve de côté | la seule récompense du scénario 1 ne servait à rien |
| aos | les serrures de campagne étaient posées sur la carte suivante du paquet de la cellule, alors que le livret dit « the top card of this deck is in play » | les captifs libérés au scénario 2 n'ouvraient rien au 3 |

Chaque correctif est daté dans le code, avec la citation du livret qui tranche.

### Ce que l'outil ne mesure pas

Le pilote joue le minimum : il répond à la première option jouable et force la
fin dès le tour du joueur. Une épreuve mesure donc une MISE EN PLACE, pas une
partie complète. Les trois boîtes sans `WriteCampaignLogAtGameOver` (trors, sm,
web_of_deceit) n'ont pas de carnet sortant : leurs épreuves ne mesurent que ce
que le carnet CHANGE, la détection restant au panneau du plateau.
