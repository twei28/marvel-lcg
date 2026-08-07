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

**Deux boîtes sur sept fonctionnent aujourd'hui**, vérifiées en jouant :

- L'Avènement de Crâne Rouge (`trors`)
- Intentions Sinistres (`sm`)

**Quatre autres sont bloquées** par un défaut du moteur, pas par des données
manquantes. C'est le travail décrit au §6, et c'est par là qu'il faut commencer.

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
| `Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py` | Les six routes HTTP de campagne |
| `Fusion/marvel-lcg-src/src/engine/device/web/server/server.py` | Y déclare `GameServerCampagne` dans la chaîne d'héritage |
| `Fusion/marvel-lcg-src/data/campagnes/*.json` | Une boîte-campagne décrite en données |
| `Fusion/marvel-lcg-src/campagnes/*.json` | Les campagnes du joueur (créé à la volée) |
| `Fusion/marvel-lcg-src/src/cards/pack/<code>/campaign.py` | Les récompenses, côté moteur |
| `Fusion/marvel-lcg-src/src/game/operate/campaign_logs.py` | Comment le moteur relit le carnet |

Routes : `/list_campagnes_definies`, `/get_campagne_definition?<code>`,
`/list_campagnes`, `/get_campagne?<id>`, `/save_campagne` (POST),
`/delete_campagne` (POST).

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
   définition, pré-remplit ce qu'il détecte, laisse choisir le reste, puis écrit
   `carnet` et `termines` et efface la clé.
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
  "detection": "cartes_en_jeu",
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

## 6. LA TÂCHE : câbler le moteur

### Le problème

Les récompenses de campagne d'un pack ne se déclenchent que si la **carte de
manigance principale 1A** du scénario appelle `CampaignSetup(niveau)` dans son
`GetAbilities()`. Sans cet appel, `Message.WhenCampaignSetup` n'a aucun
auditeur et le carnet est ignoré, en silence.

Pour trois boîtes, le module `campaign.py` est écrit, complet — et **aucune
carte ne l'appelle**. Mesuré par sonde, un scénario par boîte, carnet
pré-rempli :

| Boîte | Scénarios câblés | Constat |
|---|---|---|
| `trors` | 5 / 5 | ✅ récompenses appliquées |
| `sm` | 5 / 5 | ✅ récompenses appliquées |
| `mts` | 2 / 5 | ⚠️ Hela et Loki n'appliquent rien |
| `mut_gen` | 0 / 5 | ❌ rien |
| `next_evol` | 0 / 5 | ❌ rien |
| `aoa` | 0 / 5 | ❌ rien |
| `gmw` | — | aucune récompense codée, séquence pure |

### Le geste

Voici un fichier **déjà câblé**, `src/cards/pack/mts/ebony_maw/21074a.py` :

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

Le `niveau` est le **numéro du scénario dans la campagne**, de 1 à 5.

### Les dix-huit fichiers

Tous existent. Le module à importer est
`cards.pack.<code>.campaign` — sauf `aoa`, où c'est
`cards.pack.aoa.campaign_setup`.

**`mts` — Mad Titan's Shadow** (`CampaignSetup(level)` gère 1 à 5)

| # | Scénario | Fichier | État |
|---|---|---|---|
| 1 | ebony_maw | `src/cards/pack/mts/ebony_maw/21074a.py` | déjà câblé |
| 2 | the_tower_defense | `src/cards/pack/mts/the_tower_defense/21098a.py` | à câbler |
| 3 | thanos | `src/cards/pack/mts/thanos/21114a.py` | déjà câblé |
| 4 | hela | `src/cards/pack/mts/hela/21138a.py` | à câbler |
| 5 | loki | `src/cards/pack/mts/loki/21165a.py` | à câbler |

**`mut_gen` — Mutant Genesis** (`CampaignSetup(level)` gère 1 à 5)

| # | Scénario | Fichier |
|---|---|---|
| 1 | sabretooth | `src/cards/pack/mut_gen/sabretooth/32063a.py` |
| 2 | project_wideawake | `src/cards/pack/mut_gen/project_wideawake/32087a.py` |
| 3 | master_mold | `src/cards/pack/mut_gen/master_mold/32112a.py` |
| 4 | mansion_attack | `src/cards/pack/mut_gen/mansion_attack/32125a.py` |
| 5 | magneto | `src/cards/pack/mut_gen/magneto/32141a.py` |

**`next_evol` — NeXt Evolution** (`CampaignSetup(level)` gère 2 à 5 ; le
niveau 1 n'ajoute que la partie commune)

| # | Scénario | Fichier |
|---|---|---|
| 1 | morlock_siege | `src/cards/pack/next_evol/morlock_siege/40077a.py` |
| 2 | on_the_run | `src/cards/pack/next_evol/on_the_run/40103a.py` |
| 3 | juggernaut | `src/cards/pack/next_evol/juggernaut/40121a.py` |
| 4 | mister_sinister | `src/cards/pack/next_evol/mister_sinister/40139a.py` |
| 5 | stryfe | `src/cards/pack/next_evol/stryfe/40166a.py` |

**`aoa` — Age of Apocalypse** (importer depuis
`cards.pack.aoa.campaign_setup`)

| # | Scénario | Fichier |
|---|---|---|
| 1 | unus | `src/cards/pack/aoa/unus/45062a.py` |
| 2 | four_horsemen | `src/cards/pack/aoa/four_horsemen/45085a.py` |
| 3 | apocalypse | `src/cards/pack/aoa/apocalypse/45103a.py` |
| 4 | dark_beast | `src/cards/pack/aoa/dark_beast/45121a.py` |
| 5 | en_sabah_nur | `src/cards/pack/aoa/en_sabah_nur/45147a.py` |

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
`RAPPORT`.

Le critère : la carte du carnet doit apparaître dans une zone du joueur ou du
monde. Tant qu'elle n'y est pas, le scénario n'est pas câblé, quoi que dise le
code.

### Ensuite seulement, les fichiers de campagne

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

---

## 9. Après le câblage

Par ordre d'intérêt :

1. **Identité verrouillée, deck modifiable** entre deux scénarios. Aujourd'hui
   le deck est figé tel qu'il a été choisi à la création de la campagne. Le
   livret autorise à changer d'aspect et de cartes entre les scénarios, mais
   jamais de héros, et interdit de retirer les cartes gagnées en campagne.
2. **Haut fait** de fin de campagne, et la défaite finale en campagne experte
   qui perd la campagne (règle codée côté données mais pas côté écran).
3. **Éprouver `cartes_sous_complot` et `pv_restants` en jeu.** Ils sont testés
   unitairement sur des formes mesurées, mais n'ont jamais été vus dans une
   vraie fin de scénario Zola ni en campagne experte. C'est exactement le
   contexte où le bug des armes expérimentales s'était glissé — un détecteur
   plausible qui relevait quatre cartes au lieu d'une.
4. **`gmw`** : jouable en séquence, sans récompense codée. À décider si on
   l'expose comme campagne ou pas.
