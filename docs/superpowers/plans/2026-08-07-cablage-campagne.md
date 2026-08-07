# Câblage des quatre boîtes-campagne — plan d'implémentation

> **Pour les agents :** SOUS-SKILL REQUISE : utiliser superpowers:subagent-driven-development (recommandé) ou superpowers:executing-plans pour exécuter ce plan tâche par tâche. Les étapes utilisent des cases à cocher (`- [ ]`).

**But :** rendre les campagnes `mts`, `mut_gen`, `next_evol` et `aoa` réellement jouables, en appelant `CampaignSetup(niveau)` depuis les 18 manigances 1A concernées, en prouvant chaque scénario à la sonde, puis en donnant au plateau le carnet que le moteur calcule déjà.

**Architecture :** trois couches indépendantes. Le moteur (18 fichiers de cartes, une ligne chacun). L'outil de mesure (`tools/sonde_campagne.py`, étendu à la fin de partie). Le pont moteur-plateau (une route HTTP, une fonction pure de pré-remplissage côté React). Chaque couche est livrable et vérifiable seule.

**Spec :** [`docs/superpowers/specs/2026-08-07-cablage-campagne-design.md`](../specs/2026-08-07-cablage-campagne-design.md)

**Stack :** Python 3.10 (moteur, aiohttp), TypeScript strict + React + Vitest (plateau).

## Contraintes globales

- Python **3.10 obligatoire**, binaire `~/marvel-work/python/bin/python3.10`. Tout passe par WSL.
- Répertoire du moteur : `Fusion/marvel-lcg-src/`. Le serveur et la sonde ont pour répertoire courant `.game`, jamais la racine.
- TypeScript strict, zéro `any` sans justification locale écrite sur place.
- Ne jamais éditer `public/js` ou `public/css` côté Windows sans pousser vers la copie WSL avant le prochain `deployer.sh` : le rsync `--delete` supprimerait le travail. Ce plan ne touche pas `public/`.
- Les clés de carnet se **copient** depuis le `campaign.py` du pack, jamais ne se retapent de mémoire. Une clé fausse ne lève aucune erreur, elle rend une valeur vide.
- Un scénario n'est câblé que si la sonde le prouve. « Le code a l'air bon » ne compte pas.
- Commits fréquents, un par tâche au minimum, en français, sans em dash.
- Les tests existants (`cd ui-app && npx vitest run`) doivent rester verts à chaque commit.

## Raccourcis de commandes

Les commandes ci-dessous sont réutilisées partout dans le plan. `$MOTEUR` désigne
`/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src`.

Lancer la sonde sur un scénario :

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  RAPPORT=/tmp/sonde.json FIN_DE_PARTIE=1 \
  CAMPAIGN_LOG='{\"Campaign Pool: Cosmo\":\"1\"}' \
  ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . ebony_maw captain_america 4801"
```

Lire un rapport de sonde :

```bash
wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json,sys
d=json.load(open('/tmp/sonde.json'))
print('ERREURS:', d['erreurs'][:3])
print('CARNET SORTANT:', json.dumps(d.get('carnet_sortant'), ensure_ascii=False)[:800])
m=d.get('monde') or {}
cible=sys.argv[1] if len(sys.argv)>1 else ''
def zones():
    for z,v in m.items():
        if isinstance(v,list): yield ('monde.'+z, v)
    for i,p in enumerate(m.get('players',[])):
        for z,v in p.items():
            if isinstance(v,list): yield ('J%d.%s'%(i,z), v)
for nom,v in zones():
    for c in (v if not v or isinstance(v[0],dict) else [x for s in v for x in s]):
        if isinstance(c,dict) and c.get('card_id')==cible: print('TROUVE', cible, 'en', nom)
\" 04072"
```

Le port (dernier argument) doit être **différent à chaque exécution parallèle**.
En séquentiel, réutiliser `4801` convient.

---

### Tâche 1 : la sonde va jusqu'à la fin de partie

Aujourd'hui `tools/sonde_campagne.py` s'arrête après `GameSetup()` et le
descripteur. Elle ne déclenche jamais `Message.WhenGameOver`, donc elle ne peut
pas observer `WriteCampaignLogAtGameOver`, la capacité qui calcule le carnet
SORTANT dans les quatre boîtes à câbler.

`ebony_maw` sert de témoin : il est déjà câblé, on connaît donc la réponse
attendue avant de coder.

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/tools/sonde_campagne.py`

**Interfaces :**
- Consomme : rien.
- Produit : la variable d'environnement `FIN_DE_PARTIE`, et la clé
  `carnet_sortant` du rapport JSON, de forme
  `{"players_won": bool, "suggestions": {clé: valeur}}` ou `null`.

- [ ] **Étape 1 : constater l'état actuel, avant de toucher au fichier**

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  RAPPORT=/tmp/sonde-avant.json \
  ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . ebony_maw captain_america 4801"
wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json; d=json.load(open('/tmp/sonde-avant.json'))
print('cles du rapport :', sorted(d.keys()))
print('carnet_sortant present :', 'carnet_sortant' in d)
\""
```

Attendu : `carnet_sortant present : False`. C'est le manque que la tâche comble.

- [ ] **Étape 2 : lire la variable et effacer le témoin avant la mesure**

Après la ligne `PUZZLE = json.loads(os.environ.get("PUZZLE", "[]"))`, ajouter :

```python
FIN_DE_PARTIE = os.environ.get("FIN_DE_PARTIE", "") == "1"

# Le moteur ecrit toujours dans le repertoire courant, soit .game. On efface
# le temoin AVANT la partie : sans cela on relirait le rapport de l'execution
# precedente et on croirait le scenario cable alors qu'il ne l'est pas.
CARNET_SORTANT = "campaign_log_last.json"
```

L'effacement lui-même vient plus bas, après le `os.chdir(GAME)` : le chemin est
relatif au répertoire courant. Juste après `sys.path.insert(0, GAME)`, ajouter :

```python
if FIN_DE_PARTIE and os.path.exists(CARNET_SORTANT):
    os.remove(CARNET_SORTANT)
```

- [ ] **Étape 3 : déclencher la fin de partie et relire le témoin**

Entre le bloc `PUZZLE` et le bloc `descripteur`, insérer :

```python
# Fin de partie : c'est le seul moment ou WriteCampaignLogAtGameOver s'execute.
# On passe par SetGameOverByRule, qui construit lui-meme l'Effect a partir de
# la manigance principale : rien a fabriquer a la main.
if FIN_DE_PARTIE:
    try:
        Engine.game.world.game_over.SetGameOverByRule(
            "The Final Stage of the Villain was Defeated"
        )
    except BaseException as exc:
        sortie["erreurs"].append(f"fin de partie : {type(exc).__name__}: {exc}")
    if os.path.exists(CARNET_SORTANT):
        try:
            with open(CARNET_SORTANT, encoding="utf-8") as f:
                sortie["carnet_sortant"] = json.load(f)
        except BaseException as exc:
            sortie["erreurs"].append(f"carnet sortant : {type(exc).__name__}: {exc}")
    else:
        sortie["carnet_sortant"] = None
```

`"The Final Stage of the Villain was Defeated"` vaut `players_won = True` dans
`GAME_OVER_REASON_MAP` (`src/game/world/game_over.py`). C'est la victoire, donc
le cas qui nous intéresse : une défaite n'écrit rien au carnet.

Le descripteur est capturé **après**, comme aujourd'hui : la fin de partie ne
retire pas de cartes du plateau, et on veut le monde tel qu'il est au moment où
le panneau de récompenses l'observerait.

- [ ] **Étape 4 : documenter la variable dans l'entête du fichier**

Dans la docstring, sous la ligne `RAPPORT  : ...`, ajouter :

```
  FIN_DE_PARTIE : "1" pour declencher WhenGameOver apres la mise en place et
                  capturer le carnet SORTANT dans la cle `carnet_sortant`
```

- [ ] **Étape 5 : prouver l'extension sur le témoin**

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  RAPPORT=/tmp/sonde-apres.json FIN_DE_PARTIE=1 \
  ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . ebony_maw captain_america 4801"
wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json; d=json.load(open('/tmp/sonde-apres.json'))
c=d.get('carnet_sortant')
print('erreurs :', d['erreurs'][:3])
print('carnet_sortant :', 'ABSENT' if c is None else 'PRESENT')
if c:
    print('players_won :', c.get('players_won'))
    print('cles :', sorted((c.get('suggestions') or {}).keys()))
\""
```

Attendu : `carnet_sortant : PRESENT`, `players_won : True`, et parmi les clés au
moins `Player 1 Remaining hit points` et `Player 1 Identity`, que
`WriteCampaignLogAtGameOver` écrit systématiquement
(`src/cards/pack/mts/campaign.py:84-89`).

Si `carnet_sortant` est `ABSENT` alors que `ebony_maw` est câblé, ce n'est pas
la sonde qui est en cause : lire `d['erreurs']` et régler l'erreur avant de
continuer. Ne pas passer à la tâche 2 sur un témoin muet.

- [ ] **Étape 6 : vérifier que l'ancien usage est intact**

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  RAPPORT=/tmp/sonde-sans.json \
  ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . ebony_maw captain_america 4801"
wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json; d=json.load(open('/tmp/sonde-sans.json'))
print('erreurs :', d['erreurs'][:3]); print('monde present :', 'monde' in d)
\""
```

Attendu : `monde present : True`, aucune erreur nouvelle. Sans `FIN_DE_PARTIE`,
la sonde se comporte exactement comme avant.

- [ ] **Étape 7 : commit**

```bash
git add Fusion/marvel-lcg-src/tools/sonde_campagne.py
git commit -m "test(campagne): la sonde declenche la fin de partie et capture le carnet sortant"
```

---

### Tâche 2 : câbler `mts` et mesurer ses trois scénarios

`mts` a deux scénarios déjà câblés (`ebony_maw` niveau 1, `thanos` niveau 3) et
trois qui ne le sont pas. C'est la boîte la moins risquée : le geste s'y valide
contre deux exemples présents dans le même pack.

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/mts/the_tower_defense/21098a.py`
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/mts/hela/21138a.py`
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/mts/loki/21165a.py`

**Interfaces :**
- Consomme : `CampaignSetup` de la tâche 1 (aucune), et `FIN_DE_PARTIE` de la sonde.
- Produit : rien de programmatique. Un tableau de mesures, réutilisé en tâche 9.

- [ ] **Étape 1 : mesurer AVANT, pour avoir un rouge de référence**

Le carnet entrant de niveau 2 pose `Campaign Pool: Security Breach`, ce qui doit
mélanger la carte `21181` dans le deck de rencontre
(`ShuffleIntoEncounterIfPool('21181', 'Security Breach')`, `campaign.py:139`).

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  RAPPORT=/tmp/s-tower-avant.json FIN_DE_PARTIE=1 \
  CAMPAIGN_LOG='{\"Campaign Pool: Security Breach\":\"1\"}' \
  ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . the_tower_defense captain_america 4801"
wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json; d=json.load(open('/tmp/s-tower-avant.json'))
m=d.get('monde') or {}
trouve=any(isinstance(c,dict) and c.get('card_id')=='21181'
           for z,v in m.items() if isinstance(v,list)
           for c in (v if not v or isinstance(v[0],dict) else [x for s in v for x in s]))
print('21181 en jeu :', trouve)
print('carnet_sortant :', d.get('carnet_sortant') is not None)
\""
```

Attendu AVANT câblage : `21181 en jeu : False` et `carnet_sortant : False`. Les
deux moitiés sont mortes, ce qui est exactement le défaut à corriger.

- [ ] **Étape 2 : câbler `the_tower_defense`, niveau 2**

Dans `src/cards/pack/mts/the_tower_defense/21098a.py`, ajouter l'import sous
`from . import *` :

```python
from cards.pack.mts.campaign import CampaignSetup
```

et préfixer la liste rendue :

```python
    return [
        *CampaignSetup(2),
        AbilityFactory.WhenGameBeginSetup(under_siege_game_start),
        AbilityFactory.WhenCardSetup("This", under_siege),
    ]
```

L'ordre compte : les capacités de campagne s'enregistrent avant celles du
scénario, comme dans `21074a.py` et `21114a.py`, déjà câblés.

- [ ] **Étape 3 : mesurer APRÈS**

Rejouer exactement la commande de l'étape 1 avec
`RAPPORT=/tmp/s-tower-apres.json`.

Attendu : `21181 en jeu : True` et `carnet_sortant : True`. Si la première
reste `False`, le carnet entrant n'est pas appliqué et l'appel est mal placé ;
si la seconde reste `False`, `WriteCampaignLogAtGameOver` n'a pas tourné, ce qui
ne peut venir que d'un import ou d'un niveau erronés.

- [ ] **Étape 4 : câbler `hela`, niveau 4**

Import identique, puis :

```python
    return [
        *CampaignSetup(4),
        AbilityFactory.WhenCardSetup("This", odins_torment),
    ]
```

- [ ] **Étape 5 : mesurer `hela`**

Le niveau 4 mélange `21188` dans le deck de rencontre sans condition
(`AbilityFactoryCampaign.ShuffleCardIntoDeck('21188', 'EncounterDeck')`,
`campaign.py:150`), et distribue `21185` à chaque joueur si le pool contient
`System Shock`.

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  RAPPORT=/tmp/s-hela.json FIN_DE_PARTIE=1 \
  CAMPAIGN_LOG='{\"Campaign Pool: System Shock\":\"1\"}' \
  ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . hela captain_america 4801"
wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json; d=json.load(open('/tmp/s-hela.json'))
m=d.get('monde') or {}
def tout():
    for z,v in m.items():
        if isinstance(v,list):
            for c in (v if not v or isinstance(v[0],dict) else [x for s in v for x in s]):
                if isinstance(c,dict): yield c
    for p in m.get('players',[]):
        for z,v in p.items():
            if isinstance(v,list):
                for c in (v if not v or isinstance(v[0],dict) else [x for s in v for x in s]):
                    if isinstance(c,dict): yield c
ids={c.get('card_id') for c in tout()}
print('21188 present :', '21188' in ids)
print('21185 present :', '21185' in ids)
print('erreurs :', d['erreurs'][:3])
print('carnet_sortant :', d.get('carnet_sortant') is not None)
\""
```

Attendu : les deux `True`, `carnet_sortant : True`.

- [ ] **Étape 6 : câbler `loki`, niveau 5**

```python
    return [
        *CampaignSetup(5),
        AbilityFactory.WhenCardSetupBeforePutSetupCards(all_hail_king_loki_before),
        AbilityFactory.WhenCardSetup("This", all_hail_king_loki),
    ]
```

Conserver les autres entrées de la liste telles quelles : ne recopier que le
préfixe.

- [ ] **Étape 7 : mesurer `loki`**

Le niveau 5 met Odin en jeu sous contrôle si le pool le contient
(`PutIntoPlayIfPool('21139b,21139a', 'Odin', under_control=True)`).

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  RAPPORT=/tmp/s-loki.json FIN_DE_PARTIE=1 \
  CAMPAIGN_LOG='{\"Campaign Pool: Odin\":\"1\"}' \
  ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . loki captain_america 4801"
wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json; d=json.load(open('/tmp/s-loki.json'))
m=d.get('monde') or {}
for i,p in enumerate(m.get('players',[])):
    for z,v in p.items():
        if isinstance(v,list):
            for c in (v if not v or isinstance(v[0],dict) else [x for s in v for x in s]):
                if isinstance(c,dict) and str(c.get('card_id','')).startswith('21139'):
                    print('Odin TROUVE en J%d.%s'%(i,z))
print('erreurs :', d['erreurs'][:3])
print('carnet_sortant :', d.get('carnet_sortant') is not None)
\""
```

Attendu : une ligne `Odin TROUVE`, `carnet_sortant : True`.

- [ ] **Étape 8 : consigner les trois mesures**

Créer `docs/superpowers/plans/mesures-campagne.md` et y écrire le tableau au fur
et à mesure. Il alimentera CAMPAGNES.md en tâche 9.

```markdown
# Mesures de câblage, sonde `FIN_DE_PARTIE=1`

| Boîte | Niv. | Scénario | Carnet entrant appliqué | Carnet sortant écrit |
|---|---|---|---|---|
| mts | 2 | the_tower_defense | oui (21181) | oui |
| mts | 4 | hela | oui (21188, 21185) | oui |
| mts | 5 | loki | oui (21139) | oui |
```

- [ ] **Étape 9 : commit**

```bash
git add Fusion/marvel-lcg-src/src/cards/pack/mts docs/superpowers/plans/mesures-campagne.md
git commit -m "fix(campagne): cabler les trois scenarios mts restants"
```

---

### Tâche 3 : câbler `mut_gen` et mesurer ses cinq scénarios

Boîte entièrement inerte. `CampaignSetup` y gère les niveaux 1 à 5 et introduit
un choix de rôle par joueur (`EachPlayerRoleUpgrade`), auquel la sonde répond
seule en prenant la première option légale.

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/mut_gen/sabretooth/32063a.py` (niveau 1)
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/mut_gen/project_wideawake/32087a.py` (niveau 2)
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/mut_gen/master_mold/32112a.py` (niveau 3)
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/mut_gen/mansion_attack/32125a.py` (niveau 4)
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/mut_gen/magneto/32141a.py` (niveau 5)
- Modifier : `docs/superpowers/plans/mesures-campagne.md`

**Interfaces :**
- Consomme : la sonde étendue de la tâche 1.
- Produit : cinq lignes de mesures.

- [ ] **Étape 1 : mesurer AVANT sur `master_mold`, niveau 3**

Le niveau 3 mélange les alliés captifs dans le deck
(`ShuffleCaptiveAlliesIntoDeck()`), à partir de la clé `Captive Allies`.
`32089` est un allié captif de la boîte.

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  RAPPORT=/tmp/s-mm-avant.json FIN_DE_PARTIE=1 \
  CAMPAIGN_LOG='{\"Player 1 Role\":\"Brawler\",\"Captive Allies\":\"32089\"}' \
  ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . master_mold captain_america 4801"
wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json; d=json.load(open('/tmp/s-mm-avant.json'))
m=d.get('monde') or {}
trouve=False
for p in m.get('players',[]):
    for z,v in p.items():
        if isinstance(v,list):
            for c in (v if not v or isinstance(v[0],dict) else [x for s in v for x in s]):
                if isinstance(c,dict) and c.get('card_id')=='32089': trouve=True
print('32089 chez un joueur :', trouve)
print('carnet_sortant :', d.get('carnet_sortant') is not None)
\""
```

Attendu AVANT : les deux `False`.

- [ ] **Étape 2 : câbler les cinq fichiers**

Dans chacun, ajouter sous `from . import *` :

```python
from cards.pack.mut_gen.campaign import CampaignSetup
```

puis préfixer la liste rendue avec le niveau correspondant. Les cinq listes
actuelles et leur forme câblée :

```python
# 32063a.py, niveau 1
    return [
        *CampaignSetup(1),
        AbilityFactory.WhenCardSetup("This", stalked_by_sabretooth_1a),
    ]

# 32087a.py, niveau 2
    return [
        *CampaignSetup(2),
        AbilityFactory.WhenCardSetup("This", night_of_the_sentinels),
    ]

# 32112a.py, niveau 3
    return [
        *CampaignSetup(3),
        AbilityFactory.WhenCardSetup("This", the_sentinel_factory),
    ]

# 32125a.py, niveau 4 — garder la ligne commentee qui suit, telle quelle
    return [
        *CampaignSetup(4),
        AbilityFactory.WhenCardSetup("This", the_brotherhood_strikes_a),
        # AbilityFactory.When...
    ]

# 32141a.py, niveau 5
    return [
        *CampaignSetup(5),
        AbilityFactory.WhenCardSetup("This", asteroid_m),
    ]
```

Vérifier chaque fichier avant d'écrire : les noms de fonctions ci-dessus sont
relevés dans le code actuel, mais c'est la liste RÉELLE du fichier qu'on
préfixe, pas celle recopiée ici.

- [ ] **Étape 3 : mesurer APRÈS sur `master_mold`**

Rejouer la commande de l'étape 1 avec `RAPPORT=/tmp/s-mm-apres.json`.
Attendu : `32089 chez un joueur : True`, `carnet_sortant : True`.

- [ ] **Étape 4 : mesurer les quatre autres**

Le carnet entrant utile dépend du niveau. Pour chacun, la mesure minimale est :
la mise en place n'a pas planté, et `carnet_sortant` est présent.

```bash
for duo in "sabretooth 1" "project_wideawake 2" "mansion_attack 4" "magneto 5"; do
  set -- $duo
  wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
    RAPPORT=/tmp/s-mg-$1.json FIN_DE_PARTIE=1 \
    CAMPAIGN_LOG='{\"Player 1 Role\":\"Brawler\"}' \
    ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . $1 captain_america 4801"
  wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json; d=json.load(open('/tmp/s-mg-$1.json'))
c=d.get('carnet_sortant')
print('$1 -> erreurs:', d['erreurs'][:2])
print('$1 -> carnet:', 'ABSENT' if c is None else sorted((c.get('suggestions') or {}).keys())[:8])
\""
done
```

Attendu par scénario : aucune erreur de mise en place, et un carnet contenant au
moins `Player 1 Remaining hit points`, `Player 1 Identity`,
`Future Past in Victory Display` ou `Future Past in Encounter Deck` (que
`CollectMG` écrit à tous les niveaux).

Une erreur de mise en place est un vrai défaut : elle s'ouvre et se règle, on ne
retire pas l'appel pour faire passer la mesure.

- [ ] **Étape 5 : compléter le tableau de mesures**

Ajouter les cinq lignes à `docs/superpowers/plans/mesures-campagne.md`, au même
format que celles de `mts`.

- [ ] **Étape 6 : commit**

```bash
git add Fusion/marvel-lcg-src/src/cards/pack/mut_gen docs/superpowers/plans/mesures-campagne.md
git commit -m "fix(campagne): cabler les cinq scenarios de Mutant Genesis"
```

---

### Tâche 4 : câbler `next_evol` et mesurer ses cinq scénarios

Attention au niveau 1 : `CAMPAGNES.md` le dit dispensable, il ne l'est pas. Sans
lui, `PutEarnedEnvironmentsIntoPlay()`, `ShuffleChosenEncounterCards()`,
`ChooseCampaignPlayerSideScheme()` et l'écriture du carnet sortant ne tournent
pas, et toute la campagne part d'un carnet vide.

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/next_evol/morlock_siege/40077a.py` (niveau 1)
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/next_evol/on_the_run/40103a.py` (niveau 2)
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/next_evol/juggernaut/40121a.py` (niveau 3)
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/next_evol/mister_sinister/40139a.py` (niveau 4)
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/next_evol/stryfe/40166a.py` (niveau 5)
- Modifier : `docs/superpowers/plans/mesures-campagne.md`

**Interfaces :**
- Consomme : la sonde étendue de la tâche 1.
- Produit : cinq lignes de mesures.

- [ ] **Étape 1 : câbler les cinq fichiers**

Import commun, sous `from . import *` :

```python
from cards.pack.next_evol.campaign import CampaignSetup
```

Préfixes, niveau par niveau. Les cinq fichiers rendent une liste à une seule
entrée, sauf vérification contraire au moment d'éditer :

```python
# 40077a.py, niveau 1
    return [
        *CampaignSetup(1),
        AbilityFactory.WhenCardSetup("This", knock_knock),
    ]

# 40103a.py, niveau 2
    return [
        *CampaignSetup(2),
        AbilityFactory.WhenCardSetup("This", gotta_get_away),
    ]

# 40121a.py, niveau 3
    return [
        *CampaignSetup(3),
        AbilityFactory.WhenCardSetup("This", the_unstoppable_juggernaut),
    ]

# 40139a.py, niveau 4
    return [
        *CampaignSetup(4),
        AbilityFactory.WhenCardSetup("This", sinister_intent),
    ]

# 40166a.py, niveau 5
    return [
        *CampaignSetup(5),
        AbilityFactory.WhenCardSetup("This", uncontrollable_power),
    ]
```

- [ ] **Étape 2 : mesurer les cinq**

```bash
for duo in "morlock_siege 1" "on_the_run 2" "juggernaut 3" "mister_sinister 4" "stryfe 5"; do
  set -- $duo
  wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
    RAPPORT=/tmp/s-ne-$1.json FIN_DE_PARTIE=1 \
    ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . $1 captain_america 4801"
  wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json; d=json.load(open('/tmp/s-ne-$1.json'))
c=d.get('carnet_sortant')
print('$1 -> erreurs:', d['erreurs'][:2])
print('$1 -> carnet:', 'ABSENT' if c is None else sorted((c.get('suggestions') or {}).keys())[:8])
\""
done
```

Attendu par scénario : aucune erreur, `carnet` non `ABSENT`.

- [ ] **Étape 3 : mesurer le carnet ENTRANT sur `juggernaut`, niveau 3**

Le niveau 3 pose des compteurs d'élan
(`JuggernautMomentumCounters()`) à partir du carnet. C'est la moitié entrante,
que le test précédent ne couvre pas.

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  ~/marvel-work/python/bin/python3.10 -c \"
import re
src=open('src/cards/pack/next_evol/campaign.py').read()
for m in re.finditer(r\\\"CampaignLog\\.Get\\w+\\(\\s*'([^']+)'\\\", src): print(m.group(1))
\" | sort -u"
```

Prendre dans la sortie une clé lue au niveau 3, la poser en `CAMPAIGN_LOG`, et
relancer la sonde sur `juggernaut` pour constater son effet dans le descripteur
(compteur sur la manigance, ou carte supplémentaire en jeu). Consigner la clé
utilisée et l'effet observé dans le tableau de mesures.

- [ ] **Étape 4 : compléter le tableau et commit**

```bash
git add Fusion/marvel-lcg-src/src/cards/pack/next_evol docs/superpowers/plans/mesures-campagne.md
git commit -m "fix(campagne): cabler les cinq scenarios de NeXt Evolution"
```

---

### Tâche 5 : câbler `aoa` et mesurer ses cinq scénarios

Seule boîte dont le module s'appelle `campaign_setup` et non `campaign`. Son
`CampaignSetup` n'a pas de branche par niveau au premier abord : c'est
`SetupMissionAndOverseer(level)` qui porte la différence, et il s'exécute à tous
les niveaux, y compris 1.

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/aoa/unus/45062a.py` (niveau 1)
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/aoa/four_horsemen/45085a.py` (niveau 2)
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/aoa/apocalypse/45103a.py` (niveau 3)
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/aoa/dark_beast/45121a.py` (niveau 4)
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/aoa/en_sabah_nur/45147a.py` (niveau 5)
- Modifier : `docs/superpowers/plans/mesures-campagne.md`

**Interfaces :**
- Consomme : la sonde étendue de la tâche 1.
- Produit : cinq lignes de mesures.

- [ ] **Étape 1 : câbler les cinq fichiers**

Import commun, différent des trois autres boîtes :

```python
from cards.pack.aoa.campaign_setup import CampaignSetup
```

Préfixes :

```python
# 45062a.py, niveau 1
    return [
        *CampaignSetup(1),
        AbilityFactory.WhenCardSetup("This", hunting_gene_traitors),
    ]

# 45085a.py, niveau 2
    return [
        *CampaignSetup(2),
        AbilityFactory.WhenCardSetup("This", the_horsemen_of_apocalypse),
    ]

# 45103a.py, niveau 3
    return [
        *CampaignSetup(3),
        AbilityFactory.WhenCardSetup("This", the_age_of_apocalypse),
    ]

# 45121a.py, niveau 4
    return [
        *CampaignSetup(4),
        AbilityFactory.WhenCardSetup("This", dark_beasts_bogus_journey),
    ]

# 45147a.py, niveau 5
    return [
        *CampaignSetup(5),
        AbilityFactory.WhenCardSetup("This", en_sabah_nurs_pyramid),
    ]
```

- [ ] **Étape 2 : mesurer les cinq, moitié sortante**

```bash
for duo in "unus 1" "four_horsemen 2" "apocalypse 3" "dark_beast 4" "en_sabah_nur 5"; do
  set -- $duo
  wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
    RAPPORT=/tmp/s-aoa-$1.json FIN_DE_PARTIE=1 \
    ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . $1 captain_america 4801"
  wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json; d=json.load(open('/tmp/s-aoa-$1.json'))
c=d.get('carnet_sortant')
print('$1 -> erreurs:', d['erreurs'][:2])
print('$1 -> carnet:', 'ABSENT' if c is None else sorted((c.get('suggestions') or {}).keys())[:8])
\""
done
```

Attendu par scénario : aucune erreur, et un carnet contenant `Current Mission`
ou `Mission Done: …`, que `CollectAoA` produit.

- [ ] **Étape 3 : mesurer la moitié entrante sur un scénario de niveau 2 ou plus**

`CampaignSetup` d'`aoa` distribue `45178` à chaque joueur si le pool contient
`Panicked Refugees` (`EachPlayerShufflesCopyIfPool('45178', 'Panicked Refugees')`).

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  RAPPORT=/tmp/s-aoa-entrant.json FIN_DE_PARTIE=1 \
  CAMPAIGN_LOG='{\"Campaign Pool: Panicked Refugees\":\"1\"}' \
  ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . four_horsemen captain_america 4801"
wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json; d=json.load(open('/tmp/s-aoa-entrant.json'))
m=d.get('monde') or {}
trouve=False
for p in m.get('players',[]):
    for z,v in p.items():
        if isinstance(v,list):
            for c in (v if not v or isinstance(v[0],dict) else [x for s in v for x in s]):
                if isinstance(c,dict) and c.get('card_id')=='45178': trouve=True
print('45178 chez un joueur :', trouve)
\""
```

Attendu : `True`.

- [ ] **Étape 4 : compléter le tableau et commit**

```bash
git add Fusion/marvel-lcg-src/src/cards/pack/aoa docs/superpowers/plans/mesures-campagne.md
git commit -m "fix(campagne): cabler les cinq scenarios de Age of Apocalypse"
```

---

### Tâche 6 : la route `/get_carnet_suggere`

Le moteur calcule déjà le carnet sortant complet et l'écrit dans
`campaign_log_last.json`, dans son répertoire courant, soit `.game`. Personne ne
le lit. Cette tâche l'expose au plateau, sur le modèle exact des six routes
voisines : réponse JSON, aucune écriture, aucun état.

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py`

**Interfaces :**
- Consomme : le fichier écrit par `WriteCampaignLogAtGameOver`
  (`src/cards/pack/mts/campaign.py:96`).
- Produit : la route `GET /get_carnet_suggere`, rendant
  `{"players_won": bool, "suggestions": {clé: valeur}}`, ou
  `{"players_won": false, "suggestions": {}}` si le fichier est absent.

- [ ] **Étape 1 : déclarer le chemin, près des deux dossiers existants**

Sous la ligne `CAMPAGNES_FOLDER = ConfigVariables.Folder(...)`, ajouter :

```python
# Carnet SORTANT, ecrit par WriteCampaignLogAtGameOver a la fin de chaque
# partie de campagne (voir src/cards/pack/mts/campaign.py). Chemin relatif au
# repertoire courant du serveur, soit .game, comme les deux dossiers ci-dessus.
CARNET_SUGGERE_FILE = ConfigVariables.File('campaign_log_last_file', "./campaign_log_last.json")
```

`ConfigVariables.File` existe déjà (`src/engine/config.py:252`) et sert
notamment à `achievements_file`.

- [ ] **Étape 2 : écrire la route**

Après `get_campagne_definition`, avant le commentaire
`# ------- campagnes en cours --`, ajouter :

```python
    async def get_carnet_suggere(self, request: web.Request) -> web.Response:
        """Le carnet que le MOTEUR a calcule a la derniere fin de partie.

        Les quatre boites cablees en 2026 (mts, mut_gen, next_evol, aoa)
        relevent elles-memes leur carnet a `WhenGameOver` : le plateau n'a
        aucune raison de le redeviner depuis le descripteur. Il pre-remplit
        d'abord avec ces valeurs, et ne retombe sur ses detecteurs que pour les
        cles absentes — ce qui est le cas de toutes celles de trors et sm, qui
        n'ont pas de collecteur cote moteur.

        Fichier absent : reponse vide et 200, pas 404. Une partie hors campagne
        ou une boite sans collecteur n'est pas une erreur.
        """
        import json as json_lib
        import os

        chemin = CARNET_SUGGERE_FILE.value
        if not os.path.isfile(chemin):
            return web.json_response({'players_won': False, 'suggestions': {}})
        try:
            with open(chemin, encoding='utf-8') as f:
                brut = json_lib.load(f)
        except Exception:
            return web.json_response({'players_won': False, 'suggestions': {}})
        suggestions = brut.get('suggestions') or {}
        return web.json_response({
            'players_won': bool(brut.get('players_won')),
            'suggestions': {str(k): str(v) for k, v in suggestions.items() if v is not None},
        })
```

- [ ] **Étape 3 : enregistrer la route**

Dans `__init__`, sous la ligne de `get_campagne_definition` :

```python
        self.AddAwaitGetSecurity('/get_carnet_suggere', self.get_carnet_suggere)
```

- [ ] **Étape 4 : vérifier fichier absent**

```bash
wsl.exe -e bash -lc "pkill -f 'launcher_[f]ast'" ; true
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  rm -f .game/campaign_log_last.json && \
  nohup ~/marvel-work/python/bin/python3.10 launcher_fast.py >/tmp/serveur.log 2>&1 &"
```

Attendre que `http://127.0.0.1:2345` réponde, puis :

```bash
wsl.exe -e bash -lc "curl -s http://127.0.0.1:2345/get_carnet_suggere"
```

Attendu : `{"players_won": false, "suggestions": {}}`.

- [ ] **Étape 5 : vérifier fichier présent**

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  printf '%s' '{\"players_won\": true, \"suggestions\": {\"Campaign Pool: Cosmo\": \"1\", \"Vide\": null}}' > .game/campaign_log_last.json"
wsl.exe -e bash -lc "curl -s http://127.0.0.1:2345/get_carnet_suggere"
```

Attendu : `{"players_won": true, "suggestions": {"Campaign Pool: Cosmo": "1"}}`.
La clé `Vide` est bien retirée : une valeur `null` du moteur signifie « efface
cette entrée », pas « écris une chaîne vide ».

- [ ] **Étape 6 : arrêter le serveur et commit**

```bash
wsl.exe -e bash -lc "pkill -f 'launcher_[f]ast'"
git add Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py
git commit -m "feat(campagne): exposer le carnet calcule par le moteur sur /get_carnet_suggere"
```

---

### Tâche 7 : le plateau pré-remplit depuis le moteur, détecteurs en secours

`PanneauRecompenses` calcule aujourd'hui son pré-remplissage dans un `useMemo`
de 20 lignes, mêlé au composant, donc intestable sans rendu. On extrait cette
logique dans une fonction pure, on lui ajoute la source moteur, et on la teste.

**Fichiers :**
- Créer : `ui-app/src/board/campagne/preremplissage.ts`
- Créer : `ui-app/src/board/campagne/preremplissage.test.ts`
- Modifier : `ui-app/src/board/campagne/contexte.ts`
- Modifier : `ui-app/src/board/campagne/PanneauRecompenses.tsx:94-113`

**Interfaces :**
- Consomme : `/get_carnet_suggere` de la tâche 6 ; `cleCarnet`, `conditionRemplie`,
  `detecter`, `joueurElimine`, `ChampVictoire` de `./detecteurs` ; `Campagne` de `./contexte`.
- Produit :
  - `chargerCarnetSuggere(): Promise<Record<string, string>>` dans `contexte.ts` ;
  - `preRemplir(entree: EntreePreRemplissage): Record<string, string>` dans
    `preremplissage.ts`, avec
    `type EntreePreRemplissage = { champs: ChampVictoire[]; monde: World; carnet?: Record<string, string>; suggestions: Record<string, string>; total: number }`.

- [ ] **Étape 1 : écrire le test qui échoue**

Créer `ui-app/src/board/campagne/preremplissage.test.ts` :

```typescript
// L'ordre des sources est la seule chose que ce fichier protege, et c'est la
// seule chose qui compte : une suggestion du moteur DOIT battre un detecteur,
// parce que le moteur connait son propre etat et que le detecteur le redevine.
import { describe, expect, it } from 'vitest'
import type { World } from '../world'
import type { ChampVictoire } from './detecteurs'
import { preRemplir } from './preremplissage'

const CHAMP_AUTO: ChampVictoire = {
  cle: 'Tech Upgrade',
  type: 'auto',
  format: 'liste',
  detection: 'cartes_en_jeu',
  options: ['04155'],
  libelle: 'Amélioration technologique',
}

const CHAMP_CHOIX: ChampVictoire = {
  cle: 'Weapon',
  type: 'choix',
  format: 'liste',
  libelle: 'Arme',
}

/** Monde minimal : 04155 en jeu, un héros vivant, ce qui suffit aux détecteurs. */
const monde = (): World =>
  ({
    area_schemes_side: [
      { id: 1, card_id: '04155', card_type: 'Upgrade', name: '04155', bind_object_id: 0 },
    ],
    players: [
      {
        area_hero: [
          {
            id: 2,
            card_id: '03001b',
            card_type: 'AlterEgo',
            name: 'hero',
            bind_object_id: 0,
            info: { health: 11, max_health: 11 },
          },
        ],
      },
    ],
  }) as unknown as World

describe('preRemplir', () => {
  it('prend la valeur du moteur quand elle existe, pas celle du détecteur', () => {
    const sortie = preRemplir({
      champs: [CHAMP_AUTO],
      monde: monde(),
      suggestions: { 'Tech Upgrade': '04156' },
      total: 1,
    })
    expect(sortie['Tech Upgrade']).toBe('04156')
  })

  it('retombe sur le détecteur quand le moteur ne dit rien', () => {
    const sortie = preRemplir({
      champs: [CHAMP_AUTO],
      monde: monde(),
      suggestions: {},
      total: 1,
    })
    expect(sortie['Tech Upgrade']).toBe('04155')
  })

  it('retombe sur le carnet existant quand ni moteur ni détecteur ne répondent', () => {
    const sortie = preRemplir({
      champs: [{ ...CHAMP_AUTO, options: ['09999'] }],
      monde: monde(),
      carnet: { 'Tech Upgrade': '04150' },
      suggestions: {},
      total: 1,
    })
    expect(sortie['Tech Upgrade']).toBe('04150')
  })

  it('laisse un champ de type choix au joueur, même si le moteur a une valeur', () => {
    const sortie = preRemplir({
      champs: [CHAMP_CHOIX],
      monde: monde(),
      suggestions: { Weapon: '04072' },
      total: 1,
    })
    expect(sortie.Weapon).toBeUndefined()
  })

  it('préfixe la clé par joueur quand le champ est parJoueur', () => {
    const sortie = preRemplir({
      champs: [{ ...CHAMP_AUTO, parJoueur: true }],
      monde: monde(),
      suggestions: { 'Player 1 Tech Upgrade': '04157' },
      total: 1,
    })
    expect(sortie['Player 1 Tech Upgrade']).toBe('04157')
  })

  it('un carnet moteur vide ne change rien au comportement actuel', () => {
    const avec = preRemplir({ champs: [CHAMP_AUTO], monde: monde(), suggestions: {}, total: 1 })
    expect(avec).toEqual({ 'Tech Upgrade': '04155' })
  })
})
```

- [ ] **Étape 2 : lancer le test et le voir échouer**

```bash
cd ui-app && npx vitest run src/board/campagne/preremplissage.test.ts
```

Attendu : ÉCHEC, `Failed to resolve import "./preremplissage"`.

- [ ] **Étape 3 : écrire la fonction**

Créer `ui-app/src/board/campagne/preremplissage.ts` :

```typescript
// Pré-remplissage du panneau de récompenses : d'où vient chaque valeur.
//
// Trois sources, dans cet ordre strict :
//
//   1. le MOTEUR, quand la boîte a un collecteur `WriteCampaignLogAtGameOver`
//      (mts, mut_gen, next_evol, aoa). Il relève son propre état à la fin de
//      partie : il n'y a rien de plus sûr, et rien à redeviner ;
//   2. les DÉTECTEURS, qui relisent le descripteur de monde. C'est la seule
//      source pour trors et sm, qui n'ont pas de collecteur ;
//   3. le CARNET déjà écrit, parce qu'il est cumulatif et que ce qui y était
//      noté ne doit pas se perdre.
//
// Les champs de type `choix` ne sont jamais pré-remplis par le moteur : ce sont
// les décisions que le livret laisse au joueur, et une décision ne se détecte
// pas. Leur valeur ancienne reste proposée, comme avant.
import type { World } from '../world'
import { cleCarnet, conditionRemplie, detecter, joueurElimine, type ChampVictoire } from './detecteurs'

export type EntreePreRemplissage = {
  champs: ChampVictoire[]
  monde: World
  /** Carnet déjà enregistré pour cette campagne. */
  carnet?: Record<string, string>
  /** Ce que le moteur a relevé à la fin de partie, par clé de carnet. */
  suggestions: Record<string, string>
  /** Nombre de héros de la campagne : les clés « Player N » en dépendent. */
  total: number
}

export function preRemplir({
  champs,
  monde,
  carnet,
  suggestions,
  total,
}: EntreePreRemplissage): Record<string, string> {
  const sortie: Record<string, string> = {}
  for (const champ of champs) {
    if (!conditionRemplie(champ, monde)) continue
    const joueurs = champ.parJoueur ? [...Array(total).keys()] : [0]
    for (const joueurId of joueurs) {
      // Un héros éliminé ne participe à AUCUNE étape de victoire (livret p17).
      if (champ.parJoueur && joueurElimine(monde, joueurId)) continue
      const cle = cleCarnet(champ, joueurId)
      const duMoteur = champ.type === 'auto' ? suggestions[cle] : undefined
      const detectee = champ.type === 'auto' ? detecter(champ, monde, joueurId) : undefined
      const valeur = duMoteur ?? detectee ?? carnet?.[cle]
      if (valeur !== undefined) sortie[cle] = valeur
    }
  }
  return sortie
}
```

- [ ] **Étape 4 : lancer le test et le voir passer**

```bash
cd ui-app && npx vitest run src/board/campagne/preremplissage.test.ts
```

Attendu : 6 tests PASS.

- [ ] **Étape 5 : ajouter le client de la route**

Dans `ui-app/src/board/campagne/contexte.ts`, sous `chargerDefinition` :

```typescript
/**
 * Le carnet que le MOTEUR a relevé à la dernière fin de partie.
 *
 * Vide pour trors et sm, qui n'ont pas de collecteur côté moteur : le panneau
 * retombe alors sur ses détecteurs, exactement comme avant cette route.
 */
export const chargerCarnetSuggere = async (): Promise<Record<string, string>> => {
  try {
    const brut = await lireJson<{ suggestions?: Record<string, string> }>('/get_carnet_suggere')
    return brut.suggestions ?? {}
  } catch {
    // Une route indisponible ne doit pas empêcher de valider ses récompenses :
    // sans suggestion, les détecteurs reprennent la main.
    return {}
  }
}
```

- [ ] **Étape 6 : brancher le panneau**

Dans `ui-app/src/board/campagne/PanneauRecompenses.tsx` :

Ajouter `chargerCarnetSuggere` à l'import depuis `./contexte`, ajouter
`preRemplir` en import depuis `./preremplissage`, et retirer de l'import
`./detecteurs` les noms devenus inutilisés dans ce fichier (`conditionRemplie`
et `joueurElimine` restent utilisés plus bas, `detecter` et `cleCarnet` sont à
vérifier avant retrait ; `npx tsc --noEmit` tranchera).

Ajouter `suggestions` à la branche `pret` du type `Etat` :

```typescript
  | {
      phase: 'pret'
      campagne: Campagne
      definition: DefinitionCampagne
      scenario: ScenarioCampagne
      champs: ChampVictoire[]
      suggestions: Record<string, string>
    }
```

Dans le `useEffect` de chargement, charger la route en même temps que le reste
et la passer à l'état :

```typescript
        const campagne = await chargerCampagne(contexte.id)
        const definition = await chargerDefinition(campagne.code)
        const suggestions = await chargerCarnetSuggere()
        const scenario = definition.scenarios.find((s) => s.id === contexte.scenario)
        if (!scenario) throw new Error(`scénario inconnu : ${contexte.scenario}`)
        if (annule) return
        const champs = champsDuScenario(definition, scenario, campagne.difficulte)
        setEtat({ phase: 'pret', campagne, definition, scenario, champs, suggestions })
```

Remplacer le corps du `useMemo` de pré-remplissage par un appel :

```typescript
  const preRemplissage = useMemo(() => {
    if (etat.phase !== 'pret' || !monde) return {}
    return preRemplir({
      champs: etat.champs,
      monde,
      carnet: etat.campagne.carnet,
      suggestions: etat.suggestions,
      total: nbJoueurs(etat.campagne, monde),
    })
  }, [etat, monde])
```

- [ ] **Étape 7 : vérifier que rien n'a régressé**

```bash
cd ui-app && npx vitest run && npx tsc --noEmit
```

Attendu : tous les tests PASS, dont les 40 de `detecteurs.test.ts` inchangés, et
aucune erreur de types.

- [ ] **Étape 8 : déployer le plateau**

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions' && bash ui-app/deployer.sh"
```

Toucher `ui-app/src` ne change rien tant que ce script n'a pas tourné.

- [ ] **Étape 9 : commit**

```bash
git add ui-app/src/board/campagne
git commit -m "feat(campagne): le panneau pre-remplit depuis le moteur, detecteurs en secours"
```

---

### Tâche 8 : cloisonner le carnet par place de serveur

**Cette tâche va un cran plus loin que la spec**, qui assumait la collision en
multijoueur. Elle coûte trois lignes et referme un défaut déjà rencontré : les
campagnes et les hauts faits étaient partagés entre les quatre places avant
d'être cloisonnés par config. `campaign_log_last.json` reprend exactement le même
travers, puisque les quatre serveurs partagent le répertoire courant `.game`.
La supprimer du plan ne casse rien d'autre.

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/cards/pack/mts/campaign.py:96`
- Modifier : `Fusion/marvel-lcg-src/tools/config_serveur.py:34-35`
- Modifier : `Fusion/marvel-lcg-src/tools/test_config_serveur.py`

**Interfaces :**
- Consomme : `CARNET_SUGGERE_FILE` de la tâche 6.
- Produit : la clé de configuration `campaign_log_last_file`, par place.

- [ ] **Étape 1 : faire lire la config au writer**

Dans `src/cards/pack/mts/campaign.py`, remplacer la ligne
`with open('campaign_log_last.json', 'w') as file:` par :

```python
            from engine.config import ConfigVariables
            chemin = ConfigVariables.File('campaign_log_last_file', './campaign_log_last.json').value
            with open(chemin, 'w') as file:
```

L'import est local, comme le `import json` deux lignes plus haut : ce module de
cartes ne doit pas dépendre de la configuration au chargement.

- [ ] **Étape 2 : ajouter la clé par place**

Dans `tools/config_serveur.py`, sous `cfg["achievements_file"] = ...` :

```python
    cfg["campaign_log_last_file"] = f"./campaign-log-last-serveur-{place}.json"
```

- [ ] **Étape 3 : couvrir la clé dans le test existant**

Ouvrir `tools/test_config_serveur.py`, trouver l'assertion qui vérifie
`achievements_file`, et lui ajouter la même vérification pour
`campaign_log_last_file` : la valeur doit contenir le numéro de place, et deux
places différentes doivent produire deux chemins différents.

- [ ] **Étape 4 : lancer le test**

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  ~/marvel-work/python/bin/python3.10 -m pytest tools/test_config_serveur.py -v"
```

Attendu : PASS. Si `pytest` n'est pas disponible, exécuter le fichier
directement : `~/marvel-work/python/bin/python3.10 tools/test_config_serveur.py`.

- [ ] **Étape 5 : vérifier que la sonde tourne toujours**

La sonde efface `campaign_log_last.json` par son nom littéral. Avec la config par
défaut, le chemin reste `./campaign_log_last.json` : rien ne change. Le
confirmer :

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  RAPPORT=/tmp/s-verif.json FIN_DE_PARTIE=1 \
  ~/marvel-work/python/bin/python3.10 tools/sonde_campagne.py . ebony_maw captain_america 4801"
wsl.exe -e bash -lc "~/marvel-work/python/bin/python3.10 -c \"
import json; d=json.load(open('/tmp/s-verif.json'))
print('carnet_sortant :', d.get('carnet_sortant') is not None)
\""
```

Attendu : `True`.

- [ ] **Étape 6 : commit**

```bash
git add Fusion/marvel-lcg-src/src/cards/pack/mts/campaign.py Fusion/marvel-lcg-src/tools/config_serveur.py Fusion/marvel-lcg-src/tools/test_config_serveur.py
git commit -m "fix(campagne): cloisonner le carnet sortant par place de serveur"
```

---

### Tâche 9 : `data/campagnes/mts.json`

La boîte devient jouable depuis l'écran des campagnes. Les clés viennent de
`CollectMTS` (`src/cards/pack/mts/campaign.py:105-128`) et de
`WriteCampaignLogAtGameOver`, relevées et non retapées.

**Fichiers :**
- Créer : `Fusion/marvel-lcg-src/data/campagnes/mts.json`

**Interfaces :**
- Consomme : la route et le pré-remplissage des tâches 6 et 7.
- Produit : une définition de campagne lisible par `/get_campagne_definition`.

- [ ] **Étape 1 : relever les clés, sans les recopier de mémoire**

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  ~/marvel-work/python/bin/python3.10 -c \"
import re
src=open('src/cards/pack/mts/campaign.py').read()
bloc=src[src.index('def CollectMTS'):src.index('def CampaignSetup')]
for m in re.finditer(r\\\"updates\\['([^']+)'\\]\\\", bloc): print(m.group(1))
\""
```

Sortie attendue, dans l'ordre des niveaux :

```
Campaign Pool: Cosmo
Campaign Pool: Security Breach
Campaign Pool: Shawarma
Campaign Pool: Black Swan
Avengers Tower Damaged
Campaign Pool: System Shock
The Infinity Stones 1B completed
Campaign Pool: Norn Stone
Campaign Pool: Odin
```

`WriteCampaignLogAtGameOver` ajoute en plus, à tous les niveaux,
`Player N Remaining hit points` et `Player N Identity`. Seule la première
compte : elle est relue par
`ExpertCampaignSetPlayersHPToTheirRemainingHP` via
`CampaignLog.GetIntByPlayer("Remaining hit points", ...)`
(`src/game/ability/factory/campaign.py:44`).

- [ ] **Étape 2 : écrire le fichier**

Créer `Fusion/marvel-lcg-src/data/campagnes/mts.json`. Structure et clés
exactes ; les textes `resume` et `enjeu` sont à écrire, ceux ci-dessous sont
livrables tels quels.

```json
{
  "version": "1.0",
  "code": "mts",
  "cle_extension": "21. The Mad Titan's Shadow",
  "nom": "L'Ombre du Titan Fou",
  "nom_en": "The Mad Titan's Shadow",
  "resume": "Thanos cherche les Pierres d'Infinité, et chaque victoire vous laisse un allié, une dette ou une cicatrice que le scénario suivant vous réclamera.",
  "resume_en": "Thanos hunts the Infinity Stones, and every victory leaves behind an ally, a debt or a scar the next scenario will come to collect.",
  "expert": {
    "pv_persistants": true,
    "note": "Les PV restants sont reportés d'un scénario au suivant à partir du deuxième."
  },
  "scenarios": [
    {
      "id": "ebony_maw",
      "numero": 1,
      "nom": "Ebony Maw",
      "nom_fr": "Ebony Maw",
      "resume": "L'émissaire de Thanos s'infiltre dans la Tour des Vengeurs et y retourne vos propres défenses. Rien n'explose, rien ne hurle : il se contente de parler, et les portes s'ouvrent.",
      "enjeu": "Ce que Maw laisse derrière lui vous suit. Une brèche de sécurité non refermée reviendra hanter le deck de rencontre du scénario suivant ; Cosmo, s'il est encore là, se battra à vos côtés.",
      "victoire": [
        {
          "cle": "Campaign Pool: Cosmo",
          "type": "auto",
          "format": "int",
          "libelle": "Cosmo rallié",
          "aide": "Cosmo entre en jeu sous votre contrôle au scénario 3 s'il est noté ici."
        },
        {
          "cle": "Campaign Pool: Security Breach",
          "type": "auto",
          "format": "int",
          "libelle": "Brèche de sécurité laissée ouverte",
          "aide": "La carte Security Breach sera mélangée au deck de rencontre des scénarios suivants."
        }
      ]
    },
    {
      "id": "the_tower_defense",
      "numero": 2,
      "nom": "Tower Defense",
      "nom_fr": "La Défense de la Tour",
      "resume": "Proxima Midnight et Corvus Glaive attaquent la Tour ensemble. Deux vilains, un seul bâtiment, et personne pour vous relever.",
      "enjeu": "La Tour peut sortir debout ou éventrée de cette nuit. Ce qu'elle perd ici, aucun scénario suivant ne le lui rendra.",
      "victoire": [
        {
          "cle": "Campaign Pool: Shawarma",
          "type": "auto",
          "format": "int",
          "libelle": "Shawarma partagé",
          "aide": "Chaque joueur mélangera une copie de Shawarma dans son deck aux scénarios suivants."
        },
        {
          "cle": "Campaign Pool: Black Swan",
          "type": "auto",
          "format": "int",
          "libelle": "Black Swan en fuite",
          "aide": "Non vaincue, elle revient en jeu au scénario 3."
        },
        {
          "cle": "Avengers Tower Damaged",
          "type": "auto",
          "format": "int",
          "libelle": "Tour des Vengeurs endommagée",
          "aide": "Pénalité appliquée à la mise en place des scénarios suivants."
        }
      ]
    },
    {
      "id": "thanos",
      "numero": 3,
      "nom": "Thanos",
      "nom_fr": "Thanos",
      "resume": "Le Titan descend lui-même. Il ne vient pas gagner, il vient prendre, et il a déjà compté combien de temps cela lui prendrait.",
      "enjeu": "Ce que Thanos emporte des Pierres d'Infinité décide de la puissance qu'il aura contre Hela, puis contre Loki.",
      "victoire": [
        {
          "cle": "Campaign Pool: System Shock",
          "type": "auto",
          "format": "int",
          "libelle": "Choc systémique subi",
          "aide": "Chaque joueur mélangera une copie de System Shock dans son deck aux scénarios suivants."
        },
        {
          "cle": "The Infinity Stones 1B completed",
          "type": "auto",
          "format": "int",
          "libelle": "Les Pierres d'Infinité rassemblées par Thanos",
          "aide": "Pénalité appliquée à la mise en place des scénarios 4 et 5."
        }
      ]
    },
    {
      "id": "hela",
      "numero": 4,
      "nom": "Hela",
      "nom_fr": "Hela",
      "resume": "Le royaume des morts n'est plus un lieu de passage. Hela y retient Odin, et Garm garde la porte que vous devrez franchir dans les deux sens.",
      "enjeu": "Odin délivré vous suivra jusqu'à Asgard. Laissé derrière, il n'y sera pas.",
      "victoire": [
        {
          "cle": "Campaign Pool: Norn Stone",
          "type": "auto",
          "format": "int",
          "libelle": "Pierre de Norn récupérée",
          "aide": "Chaque joueur en reçoit une copie au scénario 5."
        },
        {
          "cle": "Campaign Pool: Odin",
          "type": "auto",
          "format": "int",
          "libelle": "Odin délivré",
          "aide": "Odin entre en jeu sous votre contrôle au scénario 5 s'il est noté ici."
        }
      ]
    },
    {
      "id": "loki",
      "numero": 5,
      "nom": "Loki",
      "nom_fr": "Loki",
      "resume": "Loki règne sur Asgard et rien de ce que vous voyez n'est sûr d'exister. La campagne se termine ici, avec tout ce que vous y avez traîné.",
      "enjeu": "Rien à reporter : c'est le dernier scénario.",
      "final": true,
      "victoire": []
    }
  ],
  "victoire_commune_expert": [
    {
      "cle": "Remaining hit points",
      "parJoueur": true,
      "type": "auto",
      "format": "int",
      "detection": "pv_restants",
      "libelle": "Points de vie restants",
      "aide": "En campagne experte, vous reprenez le scénario suivant avec ces points de vie."
    }
  ]
}
```

Le champ `Remaining hit points` garde un `detection` : c'est le seul de ce
fichier qui a un détecteur équivalent, et le garder rend le fichier fonctionnel
même si la route du moteur tombe.

- [ ] **Étape 3 : vérifier que le fichier est du JSON valide et complet**

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  ~/marvel-work/python/bin/python3.10 -c \"
import json,re
d=json.load(open('data/campagnes/mts.json',encoding='utf-8'))
sets=json.load(open('data/sets_info.json',encoding='utf-8'))
assert d['cle_extension'] in sets, 'cle_extension inconnue de sets_info.json'
attendus=sets[d['cle_extension']]['scenarios']
obtenus=[s['id'] for s in d['scenarios']]
assert obtenus==attendus, ('ordre des scenarios', obtenus, attendus)
src=open('src/cards/pack/mts/campaign.py').read()
bloc=src[src.index('def CollectMTS'):src.index('def CampaignSetup')]
connues=set(re.findall(r\\\"updates\\['([^']+)'\\]\\\", bloc)) | {'Remaining hit points'}
for s in d['scenarios']:
    for c in s.get('victoire',[]):
        assert c['cle'] in connues, ('cle inconnue du moteur', c['cle'])
for c in d.get('victoire_commune_expert',[]):
    assert c['cle'] in connues, ('cle inconnue du moteur', c['cle'])
print('mts.json valide :', len(d['scenarios']), 'scenarios')
\""
```

Attendu : `mts.json valide : 5 scenarios`. Toute assertion qui saute désigne
une clé fausse ou un ordre de scénarios erroné, et se corrige avant de
continuer.

- [ ] **Étape 4 : voir la campagne apparaître dans l'écran**

```bash
wsl.exe -e bash -lc "cd '/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src' && \
  nohup ~/marvel-work/python/bin/python3.10 launcher_fast.py >/tmp/serveur.log 2>&1 &"
wsl.exe -e bash -lc "curl -s http://127.0.0.1:2345/list_campagnes_definies"
wsl.exe -e bash -lc "curl -s 'http://127.0.0.1:2345/get_campagne_definition?mts' | head -c 300"
```

Attendu : `mts` figure dans la liste avec `nb_scenarios: 5`, et la définition se
charge. Ouvrir ensuite `http://127.0.0.1:2345/campagne.html` et vérifier que la
tuile apparaît, puis arrêter le serveur :

```bash
wsl.exe -e bash -lc "pkill -f 'launcher_[f]ast'"
```

- [ ] **Étape 5 : commit**

```bash
git add Fusion/marvel-lcg-src/data/campagnes/mts.json
git commit -m "feat(campagne): definition de campagne pour The Mad Titan's Shadow"
```

---

### Tâche 10 : mettre `CAMPAGNES.md` à jour

Le document de reprise doit décrire l'état réel après ce chantier, sinon la
prochaine session repart du tableau périmé.

**Fichiers :**
- Modifier : `CAMPAGNES.md`
- Supprimer : `docs/superpowers/plans/mesures-campagne.md` une fois son contenu reporté

**Interfaces :**
- Consomme : le tableau de mesures des tâches 2 à 5.
- Produit : rien de programmatique.

- [ ] **Étape 1 : §1, remplacer le compte des boîtes**

« Deux boîtes sur sept fonctionnent aujourd'hui » devient le compte réel après
mesures, en listant celles qui ont un fichier `data/campagnes/*.json` (jouables
depuis l'écran) et celles qui sont câblées mais sans fichier.

- [ ] **Étape 2 : §6, remplacer le tableau de constat par les mesures**

Reporter le tableau de `docs/superpowers/plans/mesures-campagne.md`, avec ses
deux colonnes de vérification, entrante et sortante. Retirer les listes « à
câbler » devenues fausses.

- [ ] **Étape 3 : §6, corriger l'affirmation sur `next_evol`**

Remplacer « le niveau 1 n'ajoute que la partie commune » par le fait mesuré : le
niveau 1 doit être câblé, sa partie commune contenant
`PutEarnedEnvironmentsIntoPlay`, `ChooseCampaignPlayerSideScheme` et l'écriture
du carnet sortant.

- [ ] **Étape 4 : §3, ajouter la route et les nouveaux fichiers**

Ajouter à la liste des routes `/get_carnet_suggere`, et aux tableaux de
chemins :

| `ui-app/src/board/campagne/preremplissage.ts` | D'où vient chaque valeur pré-remplie |
| `Fusion/marvel-lcg-src/campaign_log_last.json` | Carnet calculé par le moteur, écrasé à chaque fin de partie |

- [ ] **Étape 5 : §5, dire que `detection` est facultatif**

Noter que les boîtes dotées d'un `WriteCampaignLogAtGameOver` n'ont pas besoin
de `detection` : le moteur fournit la valeur, et le champ garde un détecteur
seulement s'il en existe un équivalent, comme filet.

- [ ] **Étape 6 : §2, documenter `FIN_DE_PARTIE`**

Ajouter la variable à la liste des variables acceptées par la sonde, avec sa
signification.

- [ ] **Étape 7 : §8, la limite du carnet du moteur**

Si la tâche 8 a été faite, écrire que le carnet est cloisonné par place via
`campaign_log_last_file`. Sinon, écrire que le fichier est partagé entre les
quatre places d'un serveur multi et que deux parties simultanées se marcheraient
dessus.

- [ ] **Étape 8 : §9, retirer ce qui est fait, ajouter ce qui reste**

Le chantier suivant devient : `mut_gen.json`, `next_evol.json` et `aoa.json`,
sur le modèle de `mts.json`.

- [ ] **Étape 9 : commit**

```bash
git rm docs/superpowers/plans/mesures-campagne.md
git add CAMPAGNES.md
git commit -m "docs(campagne): CAMPAGNES.md reflete l'etat apres cablage"
```

---

## Vérification finale

- [ ] `cd ui-app && npx vitest run && npx tsc --noEmit` : vert.
- [ ] Les 18 scénarios ont une ligne de mesure dans le §6 de `CAMPAGNES.md`, avec les deux colonnes remplies.
- [ ] `curl -s http://127.0.0.1:2345/get_carnet_suggere` répond, serveur démarré.
- [ ] `curl -s 'http://127.0.0.1:2345/get_campagne_definition?mts'` rend les 5 scénarios.
- [ ] `git status` ne montre aucun fichier de travail oublié dans `/tmp` ou à la racine.
