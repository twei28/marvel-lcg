# Guide de création de contenu — cartes, héros, scénarios

Référence unique pour ajouter du contenu au jeu. Mis au point le 1er août 2026,
après adoption du code source officiel (github.com/irefrixs/marvel-lcg, v0.5.9
build 201) en remplacement de la reconstruction bytecode.

Complété le 2 août 2026 avec la documentation officielle GitHub
`irefrixs/marvel-lcg`, branche `master`, commit
`a77154ab7e2f800a6ae82da6e67efd83dc3c8045` (`Fix doc`, 2026-07-31).
Les liens utiles :
- `https://github.com/irefrixs/marvel-lcg/blob/master/docs/card_scripting_guide.md`
- `https://github.com/irefrixs/marvel-lcg/blob/master/docs/editor_guide.md`
- `https://github.com/irefrixs/marvel-lcg/blob/master/docs/engine_architecture.md`
- `https://github.com/irefrixs/marvel-lcg/blob/master/docs/debug_guide.md`
- `https://github.com/irefrixs/marvel-lcg/blob/master/cards/example_event.py.txt`

---

## 1. Architecture : où vit quoi

### 1.1 La seule copie qui compte

> ## ✅ RANGEMENT DU 31/08/2026 : IL N'Y A PLUS QU'UNE COPIE
>
> Historique, pour comprendre les traces dans les vieux rapports : jusqu'au
> 29/08/2026 ce guide désignait `~/marvel-work/fusion/marvel-lcg-src/` (WSL)
> comme la copie vivante. C'était l'inverse depuis le 14/08, et cette
> confusion a effacé du travail à plusieurs reprises (rsync du vestige vers
> le jeu, deployer.sh à double cible). Le 31/08/2026, la copie WSL et toutes
> les autres copies mortes ont été **supprimées** (inventaire en §1.4).
>
> Le jeu vit à UN SEUL endroit, et c'est là qu'on édite :
>
> | Rôle | Chemin |
> |---|---|
> | **Copie VIVANTE (la seule)** | Windows : `C:\Users\arnau\Desktop\Marvel LCG\Fusion\marvel-lcg-src\`<br>Depuis WSL : `/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src/` |
>
> Ce qui garantit que c'est bien elle qui tourne :
> - Les trois lanceurs (`JOUER-*.bat` à la racine de `Marvel LCG`, suivis
>   par git) font `cd '<Windows>/Fusion/marvel-lcg-src'` avant de lancer le
>   jeu. Il n'existe qu'un seul jeu de lanceurs depuis le 31/08/2026.
> - `launcher_fast.py` pose `ROOT = dirname(__file__)`, puis `SRC = ROOT/src`
>   et `GAME = ROOT/.game` : il compile donc le `src/` de SON dossier, et lie
>   les `data`, `deck`, `assets` du même. Les `launcher*.sh` font pareil
>   avec `RACINE="$(dirname "$0")"`.
> - `~/marvel-work` (WSL) ne fournit que l'INTERPRÉTEUR
>   (`python/bin/python3.10`) et `tools/` (cloudflared, test_newgame.py…).
>   Aucune copie du jeu n'y vit plus.

En cas de doute sur le dossier dans lequel on se trouve, `readlink -f .` doit
commencer par
`/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src`.

Le dossier projet contient le miroir du moteur plus tout ce qui n'appartient
qu'à nous :

```
C:\Users\arnau\Desktop\Marvel LCG\
├── Fusion\marvel-lcg-src\     : le moteur (copie ①, celle qui tourne)
├── ui-app\                    : notre client React (source unique, pas de miroir)
├── docs\                      : toute la documentation, dont ce fichier
├── JOUER-SOLO.bat / JOUER-EN-MULTI.bat / JOUER-SERVEUR.bat
└── CLAUDE.md
```

### 1.2 Où créer chaque type de contenu

Les chemins ci-dessous sont **relatifs à la racine du moteur**, c'est-à-dire à
`Fusion/marvel-lcg-src/`. On les crée là, et c'est tout : il n'y a plus de
recopie à faire, la copie qu'on édite EST celle qui tourne (voir le correctif
en 1.1).

| Élément | Chemin (depuis la racine du moteur) |
|---|---|
| Code Python | `src/` (engine/, game/, cards/, core/, editor/) |
| Données cartes | `data/cards.json` |
| Index des packs | `data/sets_info.json` |
| Scénarios | `data/scenarios/*.json` (+ `data/scenarios_custom/`) |
| Sets de rencontre modulaires | `data/encounter_sets/*.json` |
| Sets némésis (référence UI) | `data/nemesis/<hero>_nemesis.json` |
| Decks de départ | `deck/starter/<hero>.json` (gabarit : `deck/temp/.temp_hero.json`) |
| Scripts de capacités | `src/cards/pack/<pack>/<set>/<card_id>.py` |
| Images des cartes | `assets/pics/<card_id>.<jpg\|png\|webp>` |
| Biographies des héros | `public/js/prepare/heros-info.js` (voir Étape 7 de PROCESSUS-HEROS.md) |
| Traits et compteurs du moteur | `src/game/card/face/card_face.py` (énums `TRAITS` et `COUNTER`) |

Exemple concret pour un nouveau héros, pack `human_torch`. On pose `W` une
fois pour toutes :

```bash
W="/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
```

```
$W/data/cards.json                      (éditer)
$W/data/sets_info.json                  (éditer)
$W/data/nemesis/human_torch_nemesis.json
$W/deck/starter/human_torch.json
$W/src/cards/pack/human_torch/…
$W/assets/pics/64001a.jpg
$W/public/js/prepare/heros-info.js      (éditer)
$W/tools/prefixes_fanmade.json          (éditer si le pack est fan-made)
```

Après toute modification de `data/*.json`, **recalculer les checksums**, sinon
le moteur rejette le fichier EN SILENCE :

```bash
cd "$W" && PYTHONPATH="$W/src" ~/marvel-work/python/bin/python3.10 \
    tools/recalculer_checksums.py "$W" data/cards.json data/sets_info.json
```

Le client React `ui-app/` n'existe QUE dans le dossier projet, à côté de
`Fusion/` : on l'édite là-bas, et `ui-app/deployer.sh` se charge de le déployer.

### 1.3 Recopie : il n'y en a plus

Il n'y a plus rien à recopier. On édite la copie ① et c'est fini : le lanceur
compile son `src/` et lie ses `data`, `deck` et `assets`. Le bloc `rsync` qui
existait ici avant le correctif du 29/08/2026 recopiait la copie WSL
(vestige, figée au 14/08/2026) **par-dessus** la copie Windows : le lancer
aujourd'hui effacerait cinq packs entiers et tous les correctifs postérieurs
au 14/08. Ne jamais le reconstituer de mémoire.

Si un jour on veut vraiment archiver ① vers la copie WSL, c'est le sens
inverse (`Windows` → `WSL`), et seulement avec `--dry-run` d'abord.

### 1.4 Les copies mortes : toutes supprimées le 31/08/2026

Le grand rangement du 31/08/2026 a supprimé TOUTES les copies mortes que
cette section recensait : `Marvel LCG\Fusion\` (vide),
`_archive-2026-08-08\`, les vieux dossiers `Marvel LCG` et
`Marvel LCG.backup-2026-07-07` du Bureau, et côté WSL `~/marvel-work/fusion/`
(l'ancienne copie vivante figée au 14/08, responsable des écrasements),
`boot*/`, `marvel-lcg-independent/`, `marvel-lcg-rebuilt/` et ~150 scripts en
vrac. `~/marvel-work` ne contient plus que `python/`, `tools/`,
`py310.tar.gz` et le projet Android (`android/`, `android-payload/`).

**La règle demeure** : toute copie du moteur qui réapparaît ailleurs que
`Fusion/marvel-lcg-src/` est un doublon jusqu'à preuve du contraire, et une
copie morte qu'on garde finit toujours par mordre. Sauvegarde de secours des
images (hors git) : `~/marvel-backups/pics-2026-08-31.tar` (2,7 Go).

**Si le dossier du projet est un jour déplacé ou renommé** : les liens
symboliques de `.game/` sont ABSOLUS et cassent en silence (constaté le
31/08/2026 : le moteur meurt sur `translate_fr.json` introuvable). Le remède
est documenté dans `launcher_fast.py` : `rm -rf .game`, il se reconstruit au
lancement suivant (~5 min). Mettre aussi à jour les chemins en dur des
`JOUER-*.bat` et de la doc.

### 1.5 Documentation de l'auteur original

Dépôt GitHub `irefrixs/marvel-lcg`, dossier `docs/` (`card_scripting_guide.md`,
`engine_architecture.md`, `editor_guide.md`, `debug_guide.md`).

Règles de travail sur le moteur :
- **Ne plus jamais reconstruire du bytecode à la main** : le source officiel est
  la référence. En cas de doute sur un comportement, comparer au clone GitHub.
- Toute divergence volontaire avec le source officiel doit être commentée
  `# CORRECTIF` (voir §9), sinon elle sera perdue à la prochaine synchro.

## 2. Format d'une carte dans `cards.json`

Structure : `{ "<pack>": [cartes...], "checksum": "..." }`. Une carte :

```json
{"card_id": "01001a", "type": "Hero", "name": "* Spider-Man", "subtitle": "",
 "desc": {"HP": "10", "ATK": "2", "THW": "1", "DEF": "3", "HS": "5"},
 "traits": ["AVENGER"], "set_name": "Spider-Man",
 "text": "Spider-Sense — <b>Interrupt</b>: ..."}
```

- `card_id` : unique. Faces d'une même carte : suffixes `a`/`b`(/`c`) —
  héros `01001a`, alter-ego `01001b` ; main scheme recto `01097a`, verso `01097b`.
- `name` : préfixe `"* "` = carte **unique**.
- `type` : `Hero, AlterEgo, Ally, Event, Upgrade, Support, Resource, Obligation,
  PlayerSideScheme, Villain, Minion, Treachery, Attachment, Environment,
  SideScheme, MainScheme, Leader, Evidence, Status, Insert, Challenge`.
- `traits` : liste en MAJUSCULES (la liste blanche est dans
  `src/game/card/face/card_face.py`, énum `TRAITS`).
- `set_name` : détermine le chemin du script Python (voir §3).
- `full_link` : la carte clone intégralement une autre (`{"card_id": X,
  "full_link": Y}` et rien d'autre). `ability_link` : mêmes capacités seulement.

Clés `desc` principales (toutes les valeurs sont des **strings**) :

| Clé | Sens |
|---|---|
| `Cost`, `HP`, `ATK`, `THW`, `DEF`, `REC`, `SCH`, `HS` | stats de base (HS = taille de main) |
| `RES` | icônes ressource : `R`=physique, `B`=mentale, `Y`=énergie, `G`=wild (source : `src/game/element/resources.py`, `RES_TEXT`) |
| `Boost` | nombre d'icônes boost |
| `Uses` | `"3,web"` = 3 compteurs nommés `web` |
| `StartingThreat`, `TargetThreat`, `EscalationThreat` | schemes ; `Stage` pour vilains/schemes |
| `Toughness, Guard, Quickstrike, Retaliate, Surge, Villainous, Hazard, Crisis, Acceleration, Amplify, Steady, Stalwart, Peril, Incite, Patrol, Hinder, Vulnerable` | mots-clés, exprimés en compteur (`"1"`, `"2"`...) |
| `GiveTo` | obligation : nom de l'alter-ego destinataire |
| `Victory`, `Restricted`, `Permanent`, `MaxPerDeck`, `MaxPerUnit`, `TeamUp`, `Setup` | divers |

Conventions de valeurs :
- `"14*"` sur `HP`/`TargetThreat`/`StartingThreat` = **par joueur** (14 × nb joueurs).
- `"1*"` sur `ATK`/`THW` d'un **allié** = dégâts consécutifs (1 dégât à l'allié
  par utilisation), un sens différent du précédent.

⚠️ **Checksum** : `cards.json` et `sets_info.json` finissent par une clé
`checksum`. Après édition manuelle, le moteur logge un avertissement
`Checksum mismatch` **non bloquant**. En mode dev (sans variable `RELEASE`),
l'avertissement affiche le checksum recalculé : le recopier dans le fichier
pour le faire taire. L'éditeur web (§7), lui, recalcule tout seul.

## 3. Scripter les capacités d'une carte

Un fichier par face avec capacités : `src/cards/pack/<pack>/<set_nettoyé>/<card_id>.py`.
Le dossier du set doit contenir un `__init__.py` avec `from cards.pack import *`.

Résolution du module (dans l'ordre, `src/cards/database.py`) :
1. `cards.pack.<pack>.<set_name nettoyé>.<card_id>`
2. `cards.pack.<pack>.<card_id>`
3. si `set_name` finit par `_nemesis` : le même chemin sans `_nemesis`
Aucun module trouvé = carte sans capacité (pas d'erreur).

Squelette minimal :

```python
from . import *

def GetAbilities() -> Sequence['Ability']:
    def mon_effet(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()
        ...
    return [AbilityFactory.WhenCardRevealed(AbilityType.WhenRevealed, mon_effet)]
```

L'essentiel de l'API (détails dans `docs/card_scripting_guide.md`) :
- **AbilityFactory** : 41 sous-fabriques (`WhenUnitWouldAttack`, `Setup`,
  `CanPlayThisUpgradeCard`, `ForChoiceAbility`...). Surface complète exposée
  aux cartes : `src/cards/pack/__init__.py`.
- **AbilityType** : `Interrupt, ForcedInterrupt, Response, ForcedResponse,
  Action, HeroAction, AlterEgoAction, WhenRevealed, WhenDefeated, Boost,
  Setup, Resource...` (vocabulaire officiel du jeu).
- **API fluide** : `.SetName()`, `.SetPlay(hero_form_only=)`, `.SetCost(Cost("Y"))`,
  `.SetCostFunc(CostFunc.Exhaust("This"))`, `.SetTarget(Enemy)`,
  `.SetLabel('attack'|'thwart'|'defense')`, `.LimitOncePerRound()`.
- **Cibles chaînes** : `"This"`, `"You"`, `"YourIdentity"`, `"AnyPlayer"`,
  `"Attacker"`, `"Trigger"`, `"AttachedEnemy"`...
- **Opérations** : `this.DealDamage`, `player.DrawUp`,
  `Faces.GiveStatus(targets, "Stunned", effect)`, `Faces.DiscardAll`,
  `this.RemoveThreatFromSchemes`, `Search.PlayerCard`, `player.ChooseAbilities`...
- **Timing** : tout passe par le bus de messages, en couple
  `Message.WhenXWould...` (annulable via `message.is_be_instead`) puis
  `Message.AfterX...`. S'accrocher au bon moment plutôt que de forcer l'état.

### 3.1 Référence rapide de scripting

Les scripts de cartes sont du **Python exécutable**. Ne jamais importer ni lancer
un pack tiers sans confiance explicite dans sa source.

Types courants à utiliser avec `effect.this.CastTo(...)` :

| Type Python | Usage |
|---|---|
| `Hero`, `AlterEgo` | faces d'identité (`01001a.py`, `01001b.py`) |
| `Ally`, `Event`, `Upgrade`, `Support`, `Resource` | cartes joueur |
| `Obligation` | obligation donnée au joueur |
| `Villain`, `Minion`, `Treachery`, `Attachment`, `Environment` | cartes Rencontre |
| `MainScheme`, `EncounterSideScheme`, `PlayerSideScheme` | manigances |

`AbilityFactory` - déclencheurs fréquents :

| Besoin | Fabrique |
|---|---|
| Action jouable pendant ton tour | `WhenInYourPlayTurn(AbilityType.HeroAction|AlterEgoAction|Action, fn)` |
| Réponse après entrée en jeu | `AfterCardEnterPlay(AbilityType.Response, joueur, carte, fn)` |
| Réponse après avoir joué une carte | `AfterPlayerPlayedCard(AbilityType.Response|ForcedResponse, joueur, carte, fn)` |
| Prévenir/remplacer des dégâts | `WhenUnitWouldTakeDamage(AbilityType.Interrupt, cible, fn, is_from_attack=...)` |
| Interrompre une attaque | `WhenUnitWouldAttack(AbilityType.Interrupt|ForcedInterrupt, cible, fn)` |
| Effet `When Revealed` | `WhenThisRevealed(condition, fn)` ou `WhenPlayerRevealCard(...)` |
| Effet `When Defeated` | `WhenUnitBeDefeated(AbilityType.WhenDefeated|ForcedInterrupt, cible, fn)` |
| Jouer une amélioration attachée | `CanPlayThisUpgradeCard(cible)` |
| Jouer un soutien | `CanPlayThisSupportCard(...)` |
| Générer une ressource | `CanGenerateResources(AbilityType.Resource|HeroResource|AlterEgoResource, Resources("G"))` |
| Début/fin de tour | `WhenPlayerTurnBegin(...)`, `WhenPlayerTurnEnd(...)` |
| Choix proposé au joueur | `ForChoiceAbility("libellé", fn)` |

Dans un handler `(effect, message)` :
- `effect.this` = face qui porte la capacité ; commencer par `CastTo(Type)`.
- `effect.targets` = cibles choisies via `.SetTarget(...)`.
- `effect.GetInitiator()` = joueur qui résout l'effet.
- `effect.world` = état de partie.
- `message` dépend du timing : `PreventDamage(...)` sur les dégâts, `trigger`
  sur une carte révélée/entrée en jeu, `GetGaveToPlayer()` sur une obligation.

Chaînage utile :

```python
(AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, mon_effet)
    .SetName("Nom affiché")
    .SetPlay()
    .SetLabel("attack")        # attack | thwart | defense
    .SetCost(Cost("Y"))
    .SetCostFunc(CostFunc.Exhaust("This"))
    .SetTarget(Enemy)
    .LimitOncePerRound())
```

Cibles et filtres fréquents :
- Chaînes : `"This"`, `"You"`, `"YourIdentity"`, `"AnyPlayer"`, `"Players"`,
  `"Initiator"`, `"Trigger"`, `"AttachedEnemy"`, `"AttachedMinion"`,
  `"YourHandCards"`.
- Types : `Enemy`, `Ally`, `Minion`, `Scheme2`, `MainScheme`, `Upgrade`,
  `Support`.
- Modificateurs : `.SetTarget(Enemy, range="All")`,
  `.SetTarget(Scheme2, range=("Zero", 3))`,
  `.SetTarget(Enemy, canbe_confused=True)`.
- Recherche : `CardFinder(traits=["AVENGER"], card_type=Ally)`,
  `CardFinder(non_trait="ELITE", card_type=Minion)`,
  `CardFinder(has_printed_res="B")`, `CardFinder(name="...")`.

Opérations communes :
- Dégâts/soins : `this.DealDamage(targets, n, effect)`,
  `target.TakeDamage(this, n, effect)`, `this.HealthUnits(targets, n, effect)`.
- Menace : `this.RemoveThreatFromSchemes(targets, n, effect)`,
  `this.PlaceThreatOnSchemes(targets, n, effect)`.
- Statuts : `Faces.GiveStatus(targets, "Stunned"|"Confused"|"Tough", effect)`.
- Mouvement : `Faces.DiscardAll(faces, effect)`,
  `Faces.ShuffleAllTo(faces, "EncounterDeck", effect)`,
  `Faces.RemoveAllFromGame(faces, effect)`, `this.PutIntoPlay(player, effect)`,
  `this.Reveal(player, effect)`.
- Pioche/recherche : `player.DrawUp(n, effect)`, `Search.PlayerCard(...)`,
  `player.LookAtDeck("EncounterDeck", n, effect)`.
- Choix : `player.ChooseAbilities(effect, ...)`,
  `player.MayChooseOneAbility(effect, ...)`.
- État persistant maison : préférer un `Buff` ou un attribut clairement nommé
  sur `effect.world`, comme le font les bulles de Gwenpool.

Exemples officiels à consulter avant d'écrire une carte neuve :
- `cards/example_event.py.txt` : action simple avec cible, soin, pioche, limite.
- `docs/card_scripting_guide.md` : Swinging Web Kick, Backflip, Black Cat,
  Spider-Tracer, Web-Shooter, Eviction Notice, Shocker, Steve Rogers.

## 4. Nouvelle carte

Voir `PROCESSUS-CARTE.md`, qui couvre construction ET validation dans
l'ordre d'exécution. Ce fichier-ci reste la référence pour le format des
données (§2) et l'API de scripting (§3).

## 5. Nouveau héros

Voir `PROCESSUS-HEROS.md`, qui couvre toutes les étapes (cartes, scripts,
deck, biographie, texte français, validation) et exige un
`PROCESSUS-CARTE.md` rempli pour chaque carte du pack. Les deux points
d'attention ci-dessous restent ici car ils décrivent un mécanisme du moteur,
pas une étape du processus.

### 5.2 Ne jamais mettre une carte signature d'un autre héros dans un deck

Une carte de classe `Hero` (`desc.Class = "Hero"`) appartient à **un** héros et
n'est jouable que par lui. Le deck-builder l'applique
(`public/js/deckbuilder/app.js`, `estCarteJoueur` : `if (c.class === "Hero")
return false`), la seule exception étant Stan Lee, dont la capacité
« Marvelous » consiste justement à emprunter 15 cartes signature.

⚠️ **Le moteur ne valide PAS les decks de départ au chargement.** Une partie qui
se crée sans erreur ne prouve donc rien sur la légalité du deck : le contrôle
doit être fait à la main.

Le piège concret rencontré sur les packs Quatre Fantastiques : chaque héros FF
a un coéquipier en carte signature n°1 (The Thing `64002` chez Human Torch,
Invisible Woman `65002` chez Mister Fantastic, Mister Fantastic `66002` chez
Invisible Woman, Human Torch `67002` chez The Thing), et les decklists
réclament **en plus** un autre coéquipier dans leur section « Basic Cards ».
Ce sont deux cartes différentes : la même Invisible Woman apparaît en
« Hero Cards 1 » chez Mister Fantastic et en « Basic Cards 17 » chez The Thing.
La série basique n'a jamais été fournie ; les alliés signature ne peuvent pas
la remplacer.

Contrôle à passer après toute modification d'un deck :

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

### 5.3 Identité alternative (art alternatif) : un seul héros dans la grille

Certains packs fournissent un second couple héros/alter-ego au texte identique,
seule l'illustration change (The Thing en tenue de Gardien de la Galaxie,
`67001c/67001d`). **Ne pas créer un deuxième deck de départ** : le wizard liste
un héros par fichier de `deck/starter/`, un second fichier ferait donc apparaître
deux fois le même personnage dans la grille.

La variante se déclare dans le deck existant, sous `metadata.hero_alts` :

```json
"metadata": {
    "url": "https://...",
    "hero_alts": [
        { "name": "The Thing (Guardian)", "hero": ["67001c,67001d"] }
    ]
}
```

`catalog.heroes()` (dans `public/js/prepare/catalog.js`) en déduit un tableau
`hero.variants`, et `blocIdentiteHeros()` (dans `app.js`) affiche à l'étape 2 un
**sélecteur d'identité** : une vignette par version, libellée par le trait qui la
distingue (« AVENGER » / « GUARDIAN »), sur le modèle du bloc « art alternatif »
juste en dessous. Le choix part dans le deck envoyé au moteur via `launcher.js`.

À ne pas confondre avec `ARTS_HEROS` / `blocArtHeros()`, qui gère les arts
alternatifs **purement cosmétiques** (mêmes valeurs de jeu). Ici les traits
changent, donc le deckbuilding change : The Thing en version Guardian perd le
trait AVENGER, et Quincarrier (« Play only if your identity has the Avenger
trait ») devient injouable.

Le moteur ignore `metadata`, le champ ne le dérange donc pas ; un héros sans
`hero_alts` n'affiche aucun sélecteur.

Les faces alternatives ont malgré tout besoin de leur entrée dans `cards.json`,
de leurs scripts (les fabriques partagées du set évitent la duplication) et de
leurs images. En revanche, **pas de biographie** dans `heros-info.js` : le
panneau de survol s'indexe sur la face du deck de base, une entrée pour la
variante resterait orpheline.

### 5.4 Règles de deckbuilding propres au héros

Certains héros impriment sur leur alter-ego des contraintes que le deck-builder
doit connaître : Fatalis (`dd001b`) interdit tout allié supplémentaire et
autorise jusqu'à 6 cartes TECH/SPELL d'autres aspects. Ces règles se déclarent
**dans le deck de départ du héros**, sous `metadata.deckbuilding` — même voie
que `metadata.hero_alts` (§5.3), et pour la même raison : le moteur ignore
`metadata`, et un héros neuf apporte ses règles avec lui au lieu d'exiger une
retouche de `public/js/deckbuilder/app.js`.

```json
"metadata": {
    "deckbuilding": {
        "aspects":         { "min": 1, "max": 1 },
        "hors_aspect":     { "max": 6, "traits": ["TECH", "SPELL"],
                             "label": "6 cartes TECH/SPELL d’autres aspects" },
        "types_interdits": ["Ally"]
    }
}
```

Les trois clés sont facultatives :

| Clé | Effet |
|---|---|
| `aspects` | `min` / `max` d'aspects distincts. `max: 99` = aspects libres. `label` remplace le libellé calculé |
| `hors_aspect` | Quota de cartes empruntées à d'AUTRES aspects. `traits` restreint aux cartes portant l'un d'eux ; liste vide ou absente = n'importe quelle carte |
| `hors_aspect.types` | *(ajouté le 07/09/2026, Ares)* Restreint en plus le quota à certains types de carte (`["Upgrade"]` pour « up to 5 TACTIC **upgrades** ») ; absent = tous les types |
| `types_interdits` | Types de cartes que le héros refuse (`"Ally"`, `"Upgrade"`…). Ne touche PAS les cartes signature, qui vivent dans `hero_deck` et non dans la sélection |

Deux points de sémantique à connaître, tous deux dans `valider()` :

- **L'aspect « choisi » est celui qui pèse le plus lourd**, pas un champ à
  renseigner. Les autres aspects ne sortent du décompte que si **toutes** leurs
  cartes passent le test de `hors_aspect` ; s'il en reste une qui échoue, la
  classe entière reste comptée et c'est l'erreur d'aspect ordinaire qui parle.
  Un quota silencieux masquerait quel aspect de trop a été introduit.
- **Une carte hors quota n'est pas la seule faute possible** : depuis le
  02/09/2026, la validation refuse aussi toute carte qui n'appartient pas à un
  deck de joueur (type de rencontre, ou carte signature d'un autre héros). Cette
  faille avait laissé `15026 Magical Suspension`, un attachement du set némésis
  de la Sorcière Rouge, dans le `player_deck` de Fatalis : sans `class`, elle
  échappait à tous les contrôles et le deck ressortait « légal ».

La table câblée de `reglesAspect()` reste en place pour les héros officiels
(Spider-Woman, Cloak & Dagger, Adam Warlock, Moon Knight), qu'on ne va pas
rouvrir un par un ; **le déclaratif l'emporte** quand il est présent.

## 6. Checklist — nouveau scénario

> **Où créer tout ça** : dans la copie vivante `Fusion/marvel-lcg-src/`
> (voir §1.1). Depuis le 29/08/2026 il n'y a plus de recopie à faire.

1. **Cartes** dans `data/cards.json` :
   - un `Villain` par stade (`Stage: "1"`, `"2"`, `"3"`, `HP` souvent en `"N*"`) ;
   - main schemes en paires `a`/`b` (`Stage`, `StartingThreat`, `TargetThreat`,
     `EscalationThreat`, éventuellement `Acceleration`) ;
   - le set de rencontre propre : `Minion`, `Treachery`, `Attachment`,
     `SideScheme`, `Environment`.
2. **Scripts** des cartes (When Revealed, boost étoilés, setup...).
3. `data/scenarios/<nom>.json` :
   ```json
   { "version": "0.5.8", "name": "Mon Vilain",
     "villain": ["id_stade1", "id_stade2"],
     "expert": false,
     "schemes": ["idA,idB"],
     "set_aside": [],
     "encounters": ["...cartes du set du scénario..."],
     "encounter_sets": ["standard"],
     "modular_sets": ["bomb_scare"] }
   ```
   et `data/scenarios/<nom>_expert.json` (stades décalés + `"expert"` dans
   `encounter_sets`).
4. Sets modulaires éventuels : `data/encounter_sets/<set>.json`
   (`{version, name, encounters[]}`).
5. Référencer dans `sets_info.json` (`scenarios` et `encounters` du pack).
6. Valider (§8) + partie test en solo ET à 2 joueurs (les valeurs `"N*"`,
   Hazard et la limite de side schemes ne se voient qu'en multi).

## 7. Éditeur web (optionnel mais recommandé pour les cartes)

Voir `docs/editor_guide.md`. Lancer le moteur **sans** la variable `RELEASE`,
puis ouvrir l'éditeur : saisie de l'ID → « Load Json » pré-remplit depuis
marvelcdb → « Submit » écrit dans `cards.json` (checksum recalculé
automatiquement, tri des packs) **et** génère un squelette de script adapté au
type de la carte. Vérifier à la main les champs sur fond vert.

Procédure GitHub originale :
1. Mettre `release = False` dans `build.py`.
2. Démarrer le jeu normalement.
3. Ouvrir `http://localhost:2340`.
4. Renseigner l'ID de carte, puis `Load Json`.
5. Cocher `Ability` si la carte a un script.
6. `Submit` ajoute la carte et, si besoin, crée le fichier `{card_id}.py`.

Dans notre environnement, la variable `RELEASE` et les lanceurs existants
remplacent souvent l'étape `build.py`. Le principe reste le même : l'éditeur
doit tourner en mode développement, sinon il est désactivé. Ne jamais faire
confiance aveuglément aux champs importés de marvelcdb : les champs verts du
formulaire restent à vérifier/remplir à la main.

## 8. Validation — obligatoire avant de considérer le travail fini

**Viser la copie qui SERT.** Les commandes ci-dessous portaient jadis sur
`~/marvel-work/fusion/marvel-lcg-src` (copie WSL, en retard dès le 09/08 et
supprimée le 31/08/2026). On vise donc `.game-src` **côté Windows**, dans la
seule installation restante :

> ### ⚠️ POURQUOI `.game-src` ET JAMAIS `"$W"` DIRECTEMENT (leçon du 29/08/2026)
>
> `.game-src/` n'est pas une copie : ses dossiers de code et de données sont des
> **liens symboliques** vers `src/`, `data/`, `deck/`, `assets/`. Il voit donc
> toujours le travail en cours, à la seconde près. Mais il a son **propre
> `launch.json`, sur un port dédié (26100)**, et c'est là tout l'intérêt.
>
> `tools/test_cards.py` (comme plusieurs autres outils du §8) **RÉÉCRIT le
> `launch.json` du dossier qu'on lui donne** : il y force `server_addresses`
> sur le port passé en argument. Viser `"$W"` au lieu de `"$W/.game-src"`
> laisse donc le vrai `launch.json` avec un port de test.
>
> Constaté le 29/08/2026 : après une série de lancements sur `"$W"`,
> `launch.json` portait `127.0.0.1:46694`. Or `JOUER-SOLO.bat` teste et ouvre
> `http://127.0.0.1:2345/` : la partie solo serait partie sur un port que rien
> n'allait chercher, et le `.bat` se serait refermé sans expliquer pourquoi.
>
> Contrôle après toute campagne de validation, et remise en état si besoin :
>
> ```bash
> $PY -c "import json;print(json.load(open('$W/launch.json'))['server_addresses'])"
> # doit afficher ['127.0.0.1:2345']
> ```

```bash
W="/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
PY=$HOME/marvel-work/python/bin/python3.10
```

**Espacer les ports d'au moins 400.** Les valeurs données plus bas se
recouvraient : l'étape 4 ouvre un port par cas, donc 440 ports à partir de sa
base, ce qui mordait sur la base de l'étape 5. Un recouvrement tue des cas
avec « processus mort », et ce ne sont pas des régressions.

**Compter 75 minutes pour l'étape 4**, pas moins. Elle lance un processus par
cas, séquentiellement. Si elle est interrompue, RIEN n'est perdu : chaque cas
dépose son résultat dans `/tmp/capacites_<prefixe><index>.json`, le préfixe
étant le PID du parent. On peut donc reprendre à l'index voulu avec
`CAS_INDEX=<n>` au lieu de tout refaire. Attention en revanche à ne pas lire
les fichiers d'un run précédent : filtrer par date.

Depuis WSL :

```bash
# 1. Syntaxe de tout le moteur
cd "$W" && $PY -m compileall -q src

# 2. Construction des capacités de TOUTES les cartes
#    (référence : 4189 ok / 0 err, 9/8/2026 ; 4122 / 0 le 4/8)
#    VISER .game-src, PAS .game : voir l'avertissement juste en dessous.
cd "$W" && $PY \
    tools/test_cards.py "$W/.game-src" 24521 /tmp/rapport-cartes.json

# 3. Cohérence texte imprimé <-> capacités construites (référence 9/8/2026 :
#    0 type, 0 texte-seul, 0 construction impossible, 132 suspicions et
#    2 exhaust_sans_cout (70003, 75012) ; 129 suspicions le 4/8)
cd "$W" && $PY \
    tools/audit_cartes.py "$W/.game-src" 24800 /tmp/audit-cartes.json

# 4. Comportement réel des capacités (référence : 354 cas, 4/8/2026 au soir.
#    Les échecs qui subsistent n'appartiennent pas à cette campagne : 20001a
#    Symbiotic Bond, dont le coût OPTIONNEL « prendre 1 dégât » est refusé par
#    le pilote, et les 12 cas `cloak_dagger` mis à rouge par la refonte en
#    cours du pack en DEUX identités — ils redeviendront verts avec elle)
#
#    ⚠ Le pilote décline les `MayChooseOneAbility` : un chemin de code placé
#    derrière un menu optionnel n'est JAMAIS exercé, même quand le cas est vert.
#    Depuis le 5/8/2026, la clé de cas `accepter_choix: True` le fait au
#    contraire prendre le MAXIMUM de cibles, ce qui ouvre ces branches. Elle
#    n'agit que pendant le déclenchement du cas, jamais pendant le setup : sinon
#    le mulligan défausse toute la main et le relevé ne veut plus rien dire.
#    Deux autres manques comblés le même jour, tous deux dans `puzzle.py` :
#    `Puzzle.Attack(carte, defender=...)` (et son raccourci `Puzzle.Defend`)
#    déclare un défenseur, seul moyen d'envoyer `WhenUnitWouldDefend` et donc
#    d'atteindre une carte « Hero Interrupt (defense) » ; et
#    `Puzzle.PutIntoPlay(carte, under_control=True)` pose la carte SOUS CONTRÔLE
#    du joueur, sans quoi ses capacités `Resource` ne sont jamais proposées au
#    paiement et tout ce qui parle d'« une carte que tu contrôles » l'ignore.
#    C'est ce qui a caché `identity.ChangeForm` pendant toute une session ;
#    `verifier_api_cartes.py` est le seul filet pour ces branches-là.
#    En revanche il ACCEPTE les coûts optionnels d'un effet déjà en cours
#    (« you may take 2 damage to... » de Self-Sacrifice 72004) et il dépense
#    volontiers une capacité Resource de l'identité pour payer. Ne pas
#    généraliser : vérifier au cas par cas ce que le journal montre.
#
#    ⚠ Chaque cas ouvre un port `port + index`. Deux lancements dont les plages
#    se recouvrent (ou un run précédent encore en TIME_WAIT) tuent des cas avec
#    « processus mort » + AssertionError IsPortAvailable : ce ne sont PAS des
#    régressions. Espacer les plages de base d'au moins 200 et relancer le cas
#    isolé (`CAS_INDEX=<n>`) avant de conclure.
cd "$W" && $PY \
    tools/test_capacites.py "$W/.game-src" 25600 /tmp/rapport-capacites.json

# 5. API réellement appelées par les scripts de cartes (référence : 4697
#    fichiers, 0 en faute, 9/8/2026 ; 4620 le 4/8)
cd "$W" && $PY \
    tools/verifier_api_cartes.py "$W/.game-src" 26050 /tmp/api-cartes.json

# 6. Cohérence des données, couverture des tests, collisions de noms
#    (ne charge pas le moteur, tourne en une seconde)
cd "$W" && python3 tools/verifier_coherence_cartes.py \
    /tmp/coherence-cartes.json

# 6 bis. Création de partie pour CHAQUE deck de départ (référence : 105/105 le
#    31/08/2026, 89/89 le 9/8/2026. `cloak_dagger` et `wonder_man`, en échec
#    le 4/8, passent tous les deux depuis)
#
#    ⚠ COMBIEN DE DECKS MONTER : ça dépend de ce qu'on a touché. Voir la
#    règle de portée juste après le §8, « Vérifier un deck ou les cent ».
#    En bref : un pack neuf qui ne touche QUE ses propres fichiers se
#    contrôle avec DECK_NOM (le sien + un témoin) ; dès qu'un fichier
#    PARTAGÉ bouge, la passe complète est obligatoire.
cd "$W" && $PY \
    tools/verifier_tous_les_decks.py "$W/.game-src" \
    27000 /tmp/rapport-decks.json

#    Un seul deck (rapide, ~40 s) :
cd "$W" && DECK_NOM=venompool $PY \
    tools/verifier_tous_les_decks.py "$W/.game-src" 27000 /tmp/rapport-decks.json
#    puis lire /tmp/deck_venompool.json

# 7. Création de partie
cd ~/marvel-work && $PY tools/test_newgame.py "$W/.game-src"

# 8. Parties REELLEMENT jouees (ajoutee au guide le 9/8/2026)
#    Aucun des outils ci-dessus ne voit une carte FIGER une partie : ils
#    montent une position, declenchent, verifient, puis s'arretent. autoplay
#    joue jusqu'au bout et compte les parties « bloquee ».
#
#    ⚠ Un taux de blocage absolu ne veut RIEN dire : le pilote est une
#    heuristique, il se coince aussi tout seul. Toujours lancer un HEROS
#    TEMOIN dans la meme fournee et comparer. Reference 9/8/2026, 8 parties
#    contre Rhino, profil equilibre : spider_man (temoin) 1 bloquee,
#    agent_13 1, brawn 2, spider_man_rainy 0, venom_rainy 0. A 24 parties,
#    brawn reste a 2 et le temoin a 1 : l'ecart etait du bruit.
cd "$W" && $PY tools/autoplay.py "$W/.game-src" --deck <nom> \
    --vilains rhino --profils equilibre --parties 8
```

⚠️ **Passer un chemin ABSOLU au dossier de jeu.** Ces outils font `os.chdir(GAME_DIR)`
puis relisent `GAME_DIR/launch.json` : avec un chemin relatif, la seconde lecture
cherche `.game-src/.game-src/launch.json` et échoue sur un `FileNotFoundError`.

⚠️ **Ne jamais tester sur `.game/`** : ce dossier ne contient presque que du
**bytecode** (4339 `.pyc` pour 8 `.py`), donc une photo figée du moteur, pas les
sources vivantes. `.game-src/` a été créé pour ça : ses dossiers de code
(`cards`, `core`, `engine`, `game`, `editor`, `main.py`) sont des **liens
symboliques vers `src/`**, ses données pointent sur les vrais dossiers. Si le
dossier a disparu, le recréer ainsi (port dédié dans son `launch.json`).

Quatre clés du harnais servent à rendre un cas DÉTERMINISTE. Sans elles, la
relecture du pack `madame_web` serait passée à côté de deux vrais défauts :

| Clé | À quoi elle sert |
|---|---|
| `main_exclusive` | **Vide la main** puis y dépose les cartes listées. Avec `main` seul, la main de départ reste là et le pilote y pioche ses ressources : le bonus « payé uniquement en [physical] » d'Ashley Barton se testait avec un paiement `R Y`, donc jamais. |
| `cibles` | Désigne des cibles précises, par `card_id`. Indispensable dès que le minimum de cibles est 0 (« exhaust up to X allies ») : le pilote envoie toujours le MINIMUM, donc rien. |
| `surpayer` | Dépense tout ce qui est disponible. Sans cela, une carte à **coût X** annonce un coût nul, le pilote ne paie rien, X vaut 0 et la carte paraît inerte alors qu'elle est correcte. |
| `payer_avec` | Impose quelles cartes financent le coût. Utile quand la ressource dépensée a elle-même un effet (The Power of Forgiveness) — mais elle ne peut que PRIORISER parmi les candidats proposés par le moteur : pour un contrôle total, préférer `main_exclusive`. |

Trois commandes ajoutées à l'API Puzzle le 4/8/2026 ouvrent les capacités qui
ne partent que pendant un vrai tour de jeu. Avant elles, une soixantaine de
cartes étaient hors de portée du harnais, dans tous les packs :

| Commande | Ce qu'elle déclenche |
|---|---|
| `Puzzle.Attack('01094')` | Un ennemi frappe le joueur courant ; sur un héros ou un allié, c'est son attaque de base. Ouvre tous les `WhenUnitWouldAttack`, `AfterUnitAttackUnit`, `WhenUnitWouldTakeDamage`, `AfterUnitDefendEnd`, les interruptions de défense et les Response « après avoir subi des dégâts ». |
| `Puzzle.Scheme('01094')` | Un ennemi manigance contre le joueur courant. |
| `Puzzle.Action('74010', 'HeroAction', 0)` | Active une action offerte par une carte **en jeu**. Le 2ᵉ argument restreint au type (`HeroAction`, `AlterEgoAction`, `Action`…), le 3ᵉ choisit parmi les actions **encore disponibles** quand la carte en offre plusieurs du même type. |

Quatre pièges rencontrés en les écrivant, tous corrigés dans `puzzle.py` :

- **la copie visée**. `FindOrCreateFace` fouille le deck du joueur AVANT le
  terrain. Un second exemplaire dans le deck et la commande visait ce double
  face cachée : la capacité était rejetée pour « out of play ». Ces trois
  commandes passent par `FindFaceInPlay`, qui regarde le terrain d'abord.
- **la liaison au message**. Résoudre l'effet directement lève une
  `AssertionError` opaque (`bind_message` absent) dès que la capacité est
  limitée, et prive de cibles celles qui en attendent. Il faut passer par
  `EventManager.FilterAvailableEffects` puis `player.ChooseEffects`.
- **le paiement en ressources**. `ChooseEffects(..., forced=True)` saute la
  question posée au joueur — or c'est dans cette question que se paie le coût
  coloré. `Puzzle.Action` ne force donc que les actions **sans** coût en
  ressources ; pour les autres, `payer_avec` désigne les cartes de paiement.
- **la fenêtre du défenseur**. `WhenUnitWouldAttack` est envoyé AVANT le choix
  du défenseur : `attacked_targets` n'y contient jamais d'allié. Une capacité
  « quand cet ennemi attaque un allié » doit utiliser
  `WhenUnitWouldAttackUnit`, envoyé une fois par unité réellement attaquée.
  C'est ce qui rendait Infected Scorpion 74015 définitivement inerte.
- **l'attaque est une ACTIVATION**. Appeler `DoAttackYou` seul saute le message
  `WhenEnemyWouldActivate`, donc toutes les interruptions « quand un sbire
  s'active, annulez son activation » (Spider-Man 74002, Jaw Lock 78004).
  `Puzzle.Attack` reproduit la branche « attaque » de `DoActivate` sans sa
  bifurcation vers la manigance. Corollaire pour l'écriture des cas : un allié
  porteur d'une telle interruption ANNULE l'attaque qu'on voulait tester —
  priver la main de la ressource exigée est le moyen le plus simple de le
  neutraliser sans changer la position.

Deux détails de mise en place que ces cas ont révélés : les alliés **Companion**
ne peuvent pas défendre (inutile d'en poser un pour tester une redirection de
dégâts), et un héros **incliné** ne défend pas, ce qui est le seul moyen fiable
de faire arriver une attaque jusqu'à l'identité.

`test_capacites.py` est le seul niveau qui **joue** vraiment la carte : chaque
cas monte une position avec l'API Puzzle (`Puzzle.PutIntoPlay`, `Reveal`,
`Boost`, `Damage`, `Counter`, `ChangeForm`, `Attack`, `Scheme`, `Action`…),
déclenche la capacité, puis
vérifie l'état du monde (statut, compteur, PV, menace). C'est lui qui attrape
« la capacité ne part jamais » et « elle ne fait pas ce qu'elle annonce », que
l'audit statique ne peut pas voir. Un cas = un processus (le moteur est un
singleton). **Toujours désigner une carte par son `card_id`, jamais par son
nom** : les noms ne sont pas uniques (deux « Venom Blast », 04035 et 56177) et
on teste alors silencieusement la mauvaise carte. Ajouter un cas = une entrée
dans la liste `CAS` + une fonction de vérification.

Règle d'or pour tout nouveau test : **vérifier qu'il échoue sur le code bugué**
avant de le déclarer bon (remettre le bug, lancer, constater l'échec,
restaurer). Un test qui ne peut pas échouer ne prouve rien.

**Deux pièges du harnais trouvés le 5/8/2026, qui faisaient passer des cartes
correctes pour cassées :**

- **`Puzzle.Reveal` ne faisait pas venir la carte du deck Rencontre.**
  `FindOrCreateFace` la fabrique dans la réserve quand elle n'est nulle part
  ailleurs, donc `message.IsFromEncounterDeck()` était faux et **toutes** les
  interruptions déclarées `from_encounter=True` (« quand une traîtrise est
  révélée depuis le deck Rencontre ») n'étaient jamais proposées. Rien ne le
  signalait : le test échouait, la carte semblait inerte. Foresight 69009 a
  ainsi été soupçonnée à tort pendant toute une session. La commande dépose
  désormais la carte sur le dessus du deck Rencontre avant de la révéler.
- **`Puzzle.Attack` faisait agir le joueur COURANT**, pas le contrôleur de la
  carte. Dans une partie à deux joueurs, faire attaquer le héros du second ne
  produisait rien du tout.

Morale : quand un cas reste rouge sans explication, **soupçonner le harnais
avant la carte**. Le moyen le plus rapide de trancher est de donner à la carte
suspecte les paramètres exacts d'une carte qui marche : si elle reste inerte,
le défaut n'est pas dans la carte.

La clé `heros2` monte une **vraie partie à deux joueurs**, indispensable aux
cartes dont le texte parle des autres joueurs (« play under any player's
control », « give to the X player ») : en solo elles ne peuvent pas être
exercées, et rien ne le signale.

Le vérificateur générique `etat_attendu` couvre la majorité des cas sans écrire
une seule fonction. Clés disponibles : `attributs`, `traits`, `en_jeu`,
`hors_jeu`, `compteurs`, `jetons`, `compteurs_total`, `menace`,
`attributs_carte`, `degats`, `degats_min`, `degats_identite`,
`dans_deck_rencontre`, `forme`, `en_jeu_trait`, `exhausted`, `pret`,
`statuts`, `taille_main`, `en_main`, `defausse`, `defausse_joueur`.
Deux pièges : **`jetons` et `compteurs` sont deux stocks distincts** (la menace
posée sur une carte joueur, façon Beat Cop, est un JETON `threat` — la
contrôler avec `compteurs` renvoie toujours 0, donc un test qui passe pour de
mauvaises raisons) ; et **`defausse` est le seul moyen de prouver qu'un
événement a été JOUÉ**, puisqu'une carte restée en main n'est pas « en jeu »
non plus et satisfait donc `hors_jeu`.

**Deuxième campagne du 4/8/2026** (après l'ajout de `Attack`/`Scheme`/`Action`) :
sept défauts de plus, dans cinq packs, tous invisibles jusque-là parce que la
carte n'était pas atteignable.

| Carte | Défaut | Correction |
|---|---|---|
| 74015 Infected Scorpion | `WhenUnitWouldAttack` ne voit jamais le défenseur : capacité **jamais** déclenchée | `WhenUnitWouldAttackUnit` + prévention temporaire posée sur l'allié |
| 66006 Vanishing Act, 66007 Force Shields | `SetPlay(...)` sur l'action d'une **amélioration** : une fois posée, la carte devenait inerte | `SetCondition(...)`, qui porte la même condition sans revendiquer le rôle de capacité de jeu |
| 66010 Forceful | `from_where=["YouControlCards"]` : les cartes de statut n'y figurent jamais, l'événement était **injouable** | `bind_to=CardFinder(card_type=Friend)` |
| 65001b Reed Richards | `for_targets` (les cibles) lu à la place de `for_effect.this` (la carte payée) | `message.for_effect.this` |
| 73004 Crack the Case, 72007/72008/72009 | `IsInField()` n'existe sur **aucune** face du moteur : plantage à l'usage | `IsInPlay()` — l'appel est désormais dans la liste noire de `verifier_api_cartes.py` |
| 78023 Protect The Pack | `TakeIndirectDamage(valeur, effect)` : la source est le **premier** argument | `TakeIndirectDamage(this, valeur, effect)` |
| 70015 Mister Negative | `message.target` n'existe pas sur `AfterUnitAttackUnit` : plantage à chaque attaque | `message.attacked` |
| 61012 Goddess of Thunder | la fonction passée en 2ᵉ argument **positionnel**, qui est `resources` et non `resources_fn` : la capacité générait un objet fonction | `resources_fn=` nommé |
| 78001a Fetch!, 68007 The Power of Forgiveness | `Select.From(liste)` : une liste de faces en 1ᵉʳ positionnel sert de clé de dictionnaire, d'où `TypeError: unhashable type: 'list'` | `Select.From(faces=liste)` |
| 78001a Fetch! (2ᵉ défaut) | `GetOwner()` peut rendre le **Scénario**, pas un joueur ; le garde `hasattr` laissait passer | tester `isinstance(..., Player)` |
| 66006/66007 (rappel) | voir plus haut | |

Un huitième défaut n'était pas dans une carte mais dans le **moteur** :
`Identity.GetAbilities` construisait `DoGenerateResources` sans transmettre
`ex_operation`, alors que `CardPlayer` le transmet. Toute identité dont la
capacité Resource a un second effet (« … puis redressez cette carte ») en
perdait la moitié en silence : Sue Storm 66001b et Reed Richards 65001b ne se
redressaient jamais.

### Vérifier un deck, ou les cent — la règle de portée

Monter les 105 decks prend **~18 minutes**. Ce n'est pas toujours nécessaire,
et ce n'est pas toujours facultatif. Le critère n'est pas « combien de héros
ai-je créés » mais **quels fichiers ai-je touchés**.

| Ce qu'on a modifié | Ce qu'il faut monter |
|---|---|
| **Uniquement** les fichiers propres à un pack : `src/cards/pack/<pack>/`, ses entrées dans `data/cards.json`, son `deck/starter/<pack>.json`, son entrée `sets_info.json` | **Son deck + un témoin**, via `DECK_NOM` |
| **N'importe quel fichier partagé** : `src/game/`, `src/engine/`, la liste blanche de `game/card/factory.py`, l'énum `COUNTER` de `card_face.py`, ou une modification/suppression d'entrées EXISTANTES de `data/cards.json` | **Les 105, sans exception** |

La raison est simple : un fichier partagé est lu par tous les héros. Le
portage de `venompool` (31/08/2026) a justement dû toucher **trois** fichiers
partagés — la liste blanche de `factory.py` (événement à deux capacités
`Play`), l'énum `COUNTER` (compteur `adrenaline`) et `data/cards.json` — d'où
passe complète obligatoire ce jour-là. À l'inverse, ajouter une carte à un
pack déjà en place ne peut casser que ce pack.

**Un deck seul** (`DECK_NOM`, non documenté ailleurs, lu dans `main()` de
l'outil) :

```bash
cd "$W" && DECK_NOM=<nom_du_deck> $PY \
    tools/verifier_tous_les_decks.py "$W/.game-src" 27000 /tmp/rapport.json
cat /tmp/deck_<nom_du_deck>.json
```

Toujours passer **un témoin** avec le deck testé (un héros au kit proche, ou
simplement `spider_man`) : un échec qui touche les deux vient de la machine
ou du moteur, un échec qui ne touche que le nouveau vient du pack.

> ### ⚠ NE JAMAIS LANCER DEUX HARNAIS EN PARALLÈLE
>
> `verifier_tous_les_decks.py`, `test_capacites.py` et `autoplay.py` ouvrent
> chacun un port par cas. Deux lancements simultanés se volent leurs ports et
> saturent la machine. Mesuré le 31/08/2026 : la passe complète est tombée à
> **73/105**, dont **31 faux échecs** `AssertionError: ip=..., port=...` plus
> un faux « main vide après le setup » — zéro régression réelle derrière.
> Ces échecs-là ne sont PAS des régressions (voir aussi l'avertissement de
> l'étape 4). En série, la même passe rend 105/105.

`verifier_tous_les_decks.py` (étape 6 bis) monte une **vraie partie pour chacun
des 88 decks de départ**. C'est le seul outil qui exerce le SETUP de toutes les
cartes d'un deck d'un coup, et il a trouvé le 4/8/2026 ce qu'aucun autre niveau
ne voyait : **onze héros sur 88 ne pouvaient pas commencer de partie**, dont
quatre de packs officiels. Les autres outils ne pouvaient pas les voir :
`test_cards.py` construit les capacités sans jamais monter de partie,
`test_newgame.py` n'essaie qu'un seul héros, et `test_capacites.py` ne touche
que les cartes pour lesquelles un cas existe.

Cinq familles de défauts en sont sorties, toutes des plantages secs au setup :

| Famille | Cartes | Correction |
|---|---|---|
| Événement « Choose one » à **deux** capacités de jeu, absent de la liste blanche de `game/card/factory.py` | 61004, 71006, 76008, 76010, 78024 | ajout à la liste, comme 64009 avant elles |
| Événement **sans aucune** capacité de jeu | 60040a/b/c Photographic Reflexes (pack officiel `fne`) | ajout à la liste `play_count == 0` |
| Carte joueur sans `desc.Class` : `card_classes` reste vide et le moteur casse | 59005, 59006, 59007 (Hercule), 76021-76024 (artefacts Age of Khonshu) | `"Class": "Hero"` |
| Obligation sans `desc.GiveTo` | 90129 Wounded Civilians | `"GiveTo": "Pepper Potts"` |
| `DoDiscardThisToGenerateResources` déclaré en `HeroInterrupt`, que `check_sub_type` n'autorise pas | 74006 Anti-Venom Goo, 58006 Energy Siphon (officielle) | `AbilityType.Interrupt`, comme 50014 |

Deux corrections tenaient à côté : la clé `TeamUp` de 78029, qui suppose deux
identités en jeu (même verdict que Power Couple 73022, elle est retirée), et le
type `AlterEgoResponse` absent de la chaîne `check_sub_type`, qui interdisait à
une Response d'alter-ego de porter un label `thwart` (The Other Guy 90110).

**Reste un défaut connu et NON corrigé** : `wonder_man` ne monte pas de partie.
`58001a` combine `GiveKeywordToAttached` et `get_new_value`, ce qui passe par
`asset_helper.check_fn` et fait `CastTo(CanAttach)` sur une identité, qui ne
s'attache pas. Remplacer la cible ne suffit pas, c'est `get_new_value` qui
impose ce chemin ; la bonne construction est probablement
`ThisGainKeyword(fn, attack=1, change_on_event=...)` (modèle Madame Web
69001a), non appliquée faute d'avoir pu prouver que le bonus se réévalue au bon
moment. Le diagnostic est écrit en commentaire sur la carte.

`audit_cartes.py` croise le texte imprimé de chaque carte avec ses capacités
réellement construites : arguments de fabrique mal typés (une chaîne là où
seule une liste est acceptée), marqueur imprimé sans capacité du même type,
coût d'inclinaison annoncé sans `CostFunc.Exhaust`, carte à texte sans script.
Il signale beaucoup de faux positifs par construction (le moteur rend souvent
une capacité sous un autre type) : **relire chaque suspicion, ne rien corriger
en masse**. Voir `RAPPORT-AUDIT-CARTES.md` pour la campagne du 2/8/2026 et la
liste des cartes déjà innocentées.

`verifier_api_cartes.py` (étape 5) comble le trou entre les deux outils
précédents : `test_cards.py` ne construit que les capacités sans jamais
exécuter le corps des handlers, et `test_capacites.py` ne joue que ce que l'API
Puzzle sait déclencher, jamais ce qui se cache derrière un choix optionnel (le
pilote décline systématiquement les choix optionnels). Entre les deux, un appel
à une méthode inexistante passe inaperçu jusqu'à la partie réelle. Il a trouvé
**cinq défauts le 4/8/2026 dans quatre packs** (`jessica_jones`,
`agent_anti_venom`, `the_thing`, `fne`, `lockjaw`), dont un protégé par un
`hasattr` qui ne plantait pas mais rendait la carte **définitivement inerte**.
Aucun test ne sait distinguer « pas encore déclenchée » de « ne fera jamais
rien » : c'est le seul outil qui attrape ça. Il signale aussi les **gardes
`hasattr`** dans les scripts de cartes (elles étouffent l'erreur au lieu de la
lever) et les **handlers définis mais jamais branchés** à une fabrique.

`verifier_coherence_cartes.py` (étape 6) ne charge pas le moteur et couvre
quatre familles, toutes nées d'un défaut réellement rencontré :
- **collisions de noms d'identité** entre packs (relevé informatif : deux
  personnages distincts peuvent légitimement partager un nom) ;
- **désignation d'une carte par son nom** dans `test_capacites.py` quand ce nom
  est ambigu. Le guide l'interdit depuis longtemps, personne ne le vérifiait, et
  c'est ce qui a fait passer au rouge un cas du Venom officiel le jour où le
  pack `agent_anti_venom` a introduit un second « Flash Thompson » ;
- **mot-clé imprimé sans clé `desc`** : 5 cartes officielles en étaient
  atteintes (Apocalypse sans `Stalwart`, deux A.I.M. Interference sans `Incite`,
  Draugr Buddy sans `Guard`, Defend Hell's Kitchen sans `Hinder`) ; elles
  affichaient un mot-clé qu'elles n'appliquaient pas ;
- **images manquantes** dans un pack custom. A révélé que les 17 scans de
  `spider_man_rainy` n'existaient QUE côté Windows : à l'époque le `rsync`
  allait de la copie WSL vers Windows, et un `--delete` sur `assets/pics/` les
  aurait effacées. C'est exactement le risque décrit par le correctif du
  29/08/2026 (§1.1), et la raison pour laquelle ce `rsync` a disparu.

Il produit enfin le **taux de couverture de chaque pack custom** par les cas de
comportement. Sans ce relevé, « le pack est validé » veut seulement dire « il se
charge » : au 4/8/2026, `mister_fantastic` et `the_thing` étaient à 0 %.

Deux chiffres sont affichés, et seul le premier compte. **Carte sujet d'un cas**
= son identifiant apparaît dans le NOM d'un cas, donc le cas porte vraiment sur
elle. **Carte citée** = son identifiant apparaît n'importe où dans un cas, ce
qui inclut les cartes servant seulement de ressource pour payer autre chose ou
de décor dans la mise en place. L'écart est large et systématiquement flatteur :
`spider_man_rainy` affiche 77 % de cartes citées pour 50 % de cartes réellement
testées. Ne jamais annoncer le second chiffre comme un taux de couverture.

Puis une **vraie partie** via `JOUER-SOLO.bat` : la carte doit être jouée dans
son contexte (leçon du HANDOFF : plusieurs bugs ne se voient qu'en partie).
Le moteur est rejouable de façon déterministe (seed + inputs) : une partie
sauvegardée dans `replays/` sert de test de régression.

Debug manuel pendant la partie :
- Ajouter `&debug` à l'URL pour activer le mode debug.
- Clic droit sur une carte : menu debug de carte.
- Touche `~` : console debug ; `Alt` l'étend en pleine hauteur.
- Commandes utiles vues dans la doc officielle : `gain 03012`, `discard c11`.
- Flèches `Up` / `Down` : historique des commandes.

### 8 bis. « À vérifier en partie réelle » : la liste est vide

Cinq fiches de pack portaient une mention « Non couverts par le harnais », au
motif que l'API Puzzle n'avait ni déclencheur d'attaque, ni déclaration de
défenseur, ni activation d'action de carte en jeu. **Ces trois manques ont été
comblés depuis, et les mentions n'ont pas suivi.** Vérifié le 10/8/2026, carte
par carte : sur les 26 nommées, 26 ont un cas dans `tools/test_capacites.py`.
Les trois qui semblaient manquer sont des capacités portées par une IDENTITÉ et
non par une carte — Fetch! est couverte par le cas `78001a`, Just Like Flies par
`71001a` — et « Cheer Up » n'existe même pas dans le catalogue.

Ce qui a comblé le trou, dans `src/game/puzzle/puzzle.py` : `Puzzle.Attack(carte)`
fait attaquer la carte visée, **y compris un ennemi** ; son paramètre `defender=`
déclare un défenseur, seul moyen d'envoyer `WhenUnitWouldDefend` ; `Puzzle.Scheme`
et `Puzzle.Action(carte, type)` couvrent la manigance et l'action de plateau.

**How to apply :** avant d'écrire qu'une capacité est hors de portée du harnais,
relire cette liste d'outils. Et si elle l'est vraiment, dire LEQUEL manque, pas
« pas de déclencheur » : c'est cette formule vague qui a survécu trois semaines
à sa propre péremption, et qui m'a fait annoncer à l'utilisateur une todo qui
n'existait plus.

## 9. Divergences volontaires à préserver (ne jamais écraser sans réfléchir)

Notre moteur diverge du source officiel sur ces points, tous commentés
`# CORRECTIF` ou en français dans le code :

| Fichier | Nature |
|---|---|
| `game/ability/factory/do_attack.py` | bug du jeu original ('AttachedIdentity'/'AttachedAlly'/types de carte → AssertionError) |
| `game/ability/factory/environment.py` | bug du jeu original (import `Leader` manquant, carte 56200b) |
| `game/ability/factory/resources.py` | Coordinated Effort 58032 (paiement partagé) |
| `game/world/limit_monitor/player_side_scheme_limit.py` | schemes « does not count against the limit » (NeXt Evolution) |
| `game/message/sender/sender_damage.py` | règle RR 1.8 : overkill basé sur les dégâts subis |
| `game/render/to_descriptor.py` + `descriptor/world.py` | fin de partie exposée au client (`game_over`, `players_won`, `game_over_reason`) |
| `engine/device/web/server/server_get.py` | endpoint `/save_deck` (deck-builder de l'UI) |
| `engine/network/web_server.py` | service des images demandées avec extension (scans de livret) |
| `engine/device/web/server/server_files.py` + `server_html.py` | la racine `/` et `/main` ouvrent directement le wizard (`public/prepare.html`) au lieu de l'ancien menu `public/main.html`, qui n'est plus servi (le fichier reste sur le disque, inerte). Les pages qu'il listait restent joignables par URL : `/scene`, `/replay`, `/deck`, `/cards`, `/puzzle`, `/credits` |
| `cards/pack/aoa/age_of_apocalypse/45164.py` + pack aoa | contournement du stub `ScenarioArea` (mission area jamais implémentée par l'original) |
| `cards/pack/tt/god_of_lies/__init__.py`, `cards/pack/wonder_man/58030/31/33.py` | implémentations à nous (stubs ou versions incomplètes côté officiel) |
| 379 fichiers de cartes absents du dépôt officiel | packs scriptés par nous (campagne AoA, Civil War, Wonder Man...) |
| pack `rainy` (61001a-61031) | héros custom Thor (Jane Foster) COMPLET créé le 1/8/2026 depuis les scans Drive de « Rainy » : 16 cartes signature + obligation Chemotherapy + set némésis (War of the Realms, Malekith, War Witches, Execute, Hostile Takeover) |
| pack `albert` (62001a-62016) | héros custom Albert (Wolverine robot, par « Kajislav ») COMPLET créé le 2/8/2026 depuis les scans Drive : 15 cartes signature + obligation Counterpart Elimination + set némésis (Wolverine, Crack in the Multiverse, Patch, Weapon X, Zombie Wolvie) ; deck de départ Agression `deck/starter/albert.json` |
| `game/card/face/card_face.py` (TRAITS) | traits `ENHANCEMENT`, `WOLVERINE`, `ZOMBIE` ajoutés pour le pack albert, `VARIANT` pour gwenpool, `FANTASTIC FOUR`/`FIRE`/`MUTATE`/`WATER` pour human_torch, `INVISIBLE`/`SCIENTIST`/`TRAANIAN` pour invisible_woman, `OLYMPUS`/`QUEEN`/`MONSTER` pour totally_awesome_hulk (`# CORRECTIF`) |
| **10 cartes corrigées par l'audit du 2/8/2026** : `04162b`, `27009`, `40187`, `41013`, `45160`, `55003`, `55022`, `55041`, `56177`, `57068` | capacité absente, mal typée, déclenchée au mauvais moment ou sans coût. Détail et preuves : `RAPPORT-AUDIT-CARTES.md` |
| `data/cards.json` : `09014`, `16062a`, `38031` | textes de cartes faux dans les données (vérifiés sur marvelcdb), code correct. Checksum recalculé |
| `cards/pack/rainy/rescue_rainy/90114a.py`, `90121.py` | Rescue « Rapid Responder » (`powers=["DEF"]`) et First Responder (restreint aux personnages amis, **choix de confort**) |
| `game/card/face/card_face.py` (COUNTER) | compteur `flame` ajouté pour le pack human_torch (`# CORRECTIF`) |
| pack `gwenpool` (63001a-63017) | héros custom Gwenpool (par « ekAugust ») COMPLET créé le 2/8/2026 depuis les scans Drive : 15 cartes signature + mécanique des BULLES (« ____ » rempli via `ResolveBlank()` dans `cards/pack/gwenpool/gwenpool/__init__.py`, limite 1×/bulle/phase, bloquée par THE END, forcée par Rules of the Universe) + obligation THE END + set némésis (Rules of the Universe, Evil Gwenpool, Break Reality ×2, Future Me Scares Me) + variantes d'art des ressources basiques (63015-17 en `full_link`) ; deck de départ aspect 'Pool `deck/starter/gwenpool.json` |
| pack `human_torch` (64001a-64014) | héros custom Human Torch (par « DesignHacker ») COMPLET créé le 2/8/2026 depuis les scans Drive : 15 cartes signature autour des **compteurs `flame`** (Flame On! inflige 1 dégât par compteur posé, plafond de 3 par ennemi) + obligation Flame Off + set némésis Hydro-Man (Dam It, Tidal Surge ×3) ; deck de départ Agression `deck/starter/human_torch.json`. **3 cartes de la decklist n'existent pas dans le moteur** (Mister Fantastic en version BASIQUE, Fiery Projections, Light It Up : cartes basiques Fantastic Four du même auteur, non fournies — voir §5.2) et sont remplacées par Ironheart (13018) et Haymaker (01087) ×2 |
| pack `mister_fantastic` (65001a-65017) | héros custom Mister Fantastic (par « DesignHacker ») COMPLET créé le 2/8/2026 depuis les scans Drive : 15 cartes signature (main vidée puis rechargée : Stretched Thin, Big Reach et Mental Gymnastics récompensent la main vide, H.E.R.B.I.E. cycle) + obligation Ben's Cure + set némésis Wizard (Hubris, Projection ×2, Execution) ; deck de départ Leadership `deck/starter/mister_fantastic.json`. Traits `SCIENTIST`/`ROBOT` et compteur `flare` ajoutés au moteur. **4 cartes de la decklist n'existent pas dans le moteur** (The Thing en version BASIQUE, Brainstorm, Better Together, Smart Move — voir §5.2) et sont remplacées par Nick Fury (01084), Helicarrier (01092), Emergency (01085) et First Aid (01086) |
| pack `the_thing` (67001a-67015) | héros custom The Thing (par « DesignHacker ») COMPLET créé le 2/8/2026 depuis les scans Drive : 15 cartes signature autour des **jetons Tenace** (les gagner puis les dépenser via Give 'Er / Take That!) + obligation Annual Shedding + set némésis Puppet Master (Pulling The Strings, Hulk asservi, Friendly Fire ×2). **Deux identités** : classique (`67001a/b`) et variante Guardian (`67001c/d`), au texte identique, gérées par des fabriques partagées dans le `__init__.py` du set. Un seul deck de départ, la variante étant déclarée en identité alternative (voir §5.3). Traits `PILOT`/`GANG` ajoutés au moteur. **3 cartes de la decklist n'existent pas dans le moteur** (Invisible Woman en version BASIQUE, Light it Up, Shields Up — voir §5.2) et sont remplacées par Spider-Man/Miles (13019), First Aid (01086) et Tenacity (01093) |
| pack `totally_awesome_hulk` (68001a-68018) | héros custom Totally Awesome Hulk (par « DesignHacker ») COMPLET créé le 2/8/2026 depuis les scans Drive : **identité à trois faces** Totally Awesome Hulk (CHAMPION) / Amadeus Cho / Uncontrollable Hulk (BRUTE), sur le modèle d'Ant-Man. Le passage d'une forme à l'autre n'est jamais libre : il est piloté par le soutien recto-verso **« The Trunk » (68012a/b)** et ses compteurs `rage` (4 compteurs → forme BRUTE, 0 compteur → retour à Amadeus Cho), les changements manuels étant interceptés par `LosingControlGuard()` (voir plus bas) et par `PlayersCannotChangeForms` sur la face BRUTE. 16 cartes signature + obligation Get Under Control + set némésis Lady Hellbender (For The Queen!, Fin Fang Foom, Krackalakassian, Threat Assessment) ; deck de départ Agression `deck/starter/totally_awesome_hulk.json`, dont **toutes** les cartes de la decklist d'origine existent déjà dans notre collection. Carte-gabarit `tah_hellbender_ally` (copie de `karma_controlled_ally`) pour le « treat Lady Hellbender as an ally » via `Faces.TreatAsAlly`. **Validé par 14 cas de comportement** ajoutés à `tools/test_capacites.py` (57/57 au 2/8/2026), qui ont fait tomber quatre vrais défauts : (a) « The Trunk » est UNE carte à deux faces, elle se déclare `"68012a,68012b"` en `set_aside` et sort au setup via `SetupPutIntoPlay` sur l'alter-ego, comme Vision 26002a/b — déclarée en une seule face dans le deck, `Card.Flip` la retournait face cachée et la sortait du jeu ; (b) Motivation et Gamma Barrier visaient le type `Hero` dans `GiveKeywordToAttached`, qui ne fonctionne que pour les cartes explicitement attachées : il faut `"You"`, et surtout PAS de `CanPlayThisUpgradeCard` sur une amélioration signature ; (c) « Losing Control » ne pouvait pas se contenter de bloquer le changement de forme. En quittant l'alter-ego le moteur fait CHOISIR entre les deux formes héros (`DefaultChangeToForm`), et répondre « BRUTE » annulait tout : action perdue, joueur coincé en alter-ego. La garde `LosingControlGuard()` REDIRIGE désormais vers la forme CHAMPION, et vit sur 68001a ET 68001b ; (d) The Power of Forgiveness ne faisait rien du tout : son effet différé était porté par la ressource elle-même, défaussée au moment du paiement, et le retrait des compteurs était conditionné à la présence d'une cible de soin (absente en solo sans allié). L'abilité est désormais portée par l'identité et les deux effets sont dissociés. Trois écarts d'implémentation assumés : **Hypermind** (68001a) convertit les ressources générées en [wild] en interceptant `Message.CheckEffectGeneratedResources` plutôt qu'en modifiant le pool ; les **+2 PV par joueur** de Fin Fang Foom et Krackalakassian passent par `ThisGainKeyword` permanent au lieu d'un `When Revealed` ; le **« You can only spend [wild] resources »** de Wild Lunge est encodé par le coût coloré `"Cost": "G"` (mécanisme natif, cf. Crushing Blow 10002). L'audit signale 5 suspicions `marqueur_sans_capacite` (68002, 68012a/b, 68016, 68017) : faux positifs, les fabriques employées produisent des `DelayAbility` / `NonKeyword` là où le texte imprimé dit Response / Interrupt / When Revealed, exactement comme Wasp 13001a et Bell Tower 27077a |
| pack `invisible_woman` (65001a-65018) | héros custom Invisible Woman (par « DesignHacker ») COMPLET créé le 2/8/2026 depuis les scans Drive : identité triple face Invisible / Sue Storm / Psionic, 15 cartes signature, obligation Family Time + set némésis Psycho-Man (Emotional Masterplan, Microversal Maneuvers, Titanic Terror, End Of The Line). Deck de départ `deck/starter/invisible_woman.json`. **4 cartes basiques custom de la decklist d'origine n'existent pas dans le moteur** (Human Torch - Johnny Storm, Powerhouse - Franklin Richards, Better Together, Flaming Force) ; elles sont documentées dans `metadata.missing_custom_basic_cards` et remplacées par des cartes existantes du deck. |
| pack `madame_web` (69001a-69029 + `mweb_veranke_minion`) | héros custom Madame Web (par « Kajislav ») COMPLET créé le 2/8/2026 depuis les scans Drive : identité Madame Web / Cassandra Webb dont **ATK, THW et DEF sont imprimés « X »** et valent le nombre d'alliés contrôlés (plafond 3) — `cards.json` les déclare à 0 et `ThisGainKeyword` les remonte ; s'y ajoute *A Bond with the Allies*, qui donne à l'héroïne les traits de chaque allié (`ThisGainTraitsOfEachCardInPlay`, fabrique qu'aucune carte du moteur n'employait jusqu'ici). 15 cartes signature + obligation Neurological Deterioration + **deux sets némésis complets** : Spider-Woman/Charlotte Witter (`69013-69016`, celui du deck de départ) et The Grim Hunt/Kraven (`69017-69021`, disponible pour un deck perso, décrit dans `metadata.alternate_nemesis_set`). Deck de départ Leadership+ `deck/starter/madame_web.json`, dont **les 25 cartes existent toutes** : 17 officielles et 8 cartes d'aspect custom du même auteur (`69022-69029`). Deux variantes d'aspect fournies sur les scans (« Determination » pour Mattie Franklin, « Anti-Hero » pour Veranke) sont **écartées** : ce sont des aspects non officiels que le moteur ne connaît pas ; seules les versions Basic et Leadership sont retenues. **Validé par 30 cas de comportement** ajoutés à `tools/test_capacites.py` (87/87 au 2/8/2026). La première passe a fait tomber un défaut de données : `desc.Uses` posé sur un **allié** faisait planter la création de partie (`KeyError: 'Uses'`), car `Ally` n'hérite pas de `HasUses` — les compteurs `psionic` de Julia Carpenter passent donc par `ThisEnterPlayWithCounters`, comme Hawkeye 01066. La relecture a ensuite corrigé quatre points : (a) **Astral Form** (69005) retirait X menaces sur CHAQUE complot au lieu de X RÉPARTIES — il fallait `repeat_rules="Threat"` + `RemoveThreatFromSchemesTotal`, montage de Mutant Peacekeepers 34018 ; (b) **Webb's Team Strikes!** (69008) déclarait `range=("Zero", "All")`, qui veut dire « tous ou aucun » et non « jusqu'à X » — `(0, "All")` ; (c) **Ashley Barton** (69023) n'appliquait jamais son +1 ATK : `ThisGainKeyword` est évalué à l'ENTRÉE EN JEU, donc avant que le paiement soit connu, et ne se réévalue pas — le bonus est désormais posé directement depuis `AfterPlayerPlayedCard`, dont le message expose `paid_resources` ; (d) **Ana Kraven** (69017) visait `Identity` (n'importe quelle identité de la table) au lieu de `"You"`. **Order of the Web** (69027) portait en plus un `desc.MaxPerUnit` erroné : la limite « Max 1 TEAM card per player » est purement textuelle, Mighty Avengers 21015 n'a aucune clé pour elle. Écart assumé sur **The Grim Hunt** (69018) : `TargetThreat` et `EscalationThreat` ne sont gérés que sur les complots PRINCIPAUX, les 5 menaces par joueur et le +1 par joueur par phase du vilain sont donc câblés dans le script. L'audit signale 1 suspicion `marqueur_sans_capacite` (69025) : faux positif, le moteur n'expose pas d'interruption sur l'entrée en main, le « Forced Interrupt » de Mattie Franklin est donc un `AfterCardEnterHand`. |
| `game/ability/factory/enhance_self.py` (`ThisGainKeyword`) | paramètre `defense` ajouté (`# CORRECTIF`) : `Gain()` l'acceptait déjà, la fabrique ne l'exposait pas. Nécessaire aux stats « X » de Madame Web 69001a |
| `game/card/face/card_face.py` (TRAITS) | trait `SKRULL` ajouté pour le pack madame_web (`# CORRECTIF`) |
| `public/js/module/card_info.js` + `card_statistics.js` | champ **`custom`** des cartes fan-made (nom de l'auteur) propagé de `cards.json` jusqu'au client (`# CORRECTIF`). Voir §14 |
| `public/js/deckbuilder/app.js` + `public/deck-builder.html` | pastille « CUSTOM » sur les cartes fan-made, et exemption Arachnophilia de la limite d'aspect pour Madame Web. Voir §14 |
| pack `cloak_dagger` (70001a-70018) | héros custom **Cloak & Dagger** (par « DesignHacker », scans Drive « MC4 Sealed ») créé le 3/8/2026, **refondu le 5/8/2026 en DEUX IDENTITÉS**. Le pack physique fait jouer deux héros à un seul joueur : deux mini-decks, deux mains, les deux identités en jeu. La première adaptation rendait Dagger en alliée signature, faute de savoir tenir deux identités. Le moteur le sait depuis le 5/8/2026, sans toucher aux ~770 lectures de `GetIdentity()` : le deck déclare une clé **`linked_identity`** (identité, mini-deck, obligations propres) que `SceneLoader.ExpandLinkedIdentity` développe en un **second joueur**. Le moteur crée alors naturellement une seconde identité avec son deck, sa main et sa défausse ; `HeroDescriptor` porte le nouveau champ. Conséquence : les synergies imprimées se lisent enfin au pied de la lettre. *Protective Pair* (70001a, +2 DEF tant que Dagger est en jeu), *Destructive Duo* (70002a, +2 ATK tant que Cloak est en jeu), *Enlightening* (70001b, stalwart) et *Harmony* (70002b, +2 REC) sont quatre `ThisGainKeyword` conditionnés à la présence de la face de l'AUTRE joueur. ⚠ **Piège trouvé à cette occasion** : `OnEvent.CardInPlay` ne voit PAS un changement de face — la carte d'identité reste en jeu, seule la face change — donc le bonus ne retombait jamais quand l'autre héros basculait en alter-ego. Il faut `OnEvent.Form(Identity)`, qui écoute `AfterUnitChangeForm` sur n'importe quelle identité de la table. Les deux moitiés croisées d'Enlightening et Harmony (« Tandy ET Tyrone ») sont portées par chaque face pour elle-même : vue depuis sa propre carte, la condition « tant que je suis en jeu » est toujours vraie. **Bright Barrage** et **Forces Combined** sont câblées au texte depuis le 5/8/2026. La première est un simple `ThisCanAttack(canbe_divided=True)` sur la face héros, modèle Wasp 13001c : l'ancienne adaptation devait passer par une action dédiée faute d'attaque de base à modifier, la face héros en a une. La seconde se rend en DEUX morceaux, ce qui la met au texte imprimé. L'AUTORISATION étend `CheckAnyPlayerMayHelpPay` (game/ability/factory/resources.py), le crochet par lequel le moteur laisse déjà un autre joueur financer un coût (mot-clé Alliance, Coordinated Effort 58032) : elle exige que Forces Combined soit en jeu et PRÊTE. L'INCLINAISON est portée par la carte, sur `AfterGenerateResources` : dès qu'une carte venue de l'autre main est réellement dépensée, Forces Combined s'incline et ferme le robinet jusqu'au redressement. L'ancienne adaptation « Resource : exhaust → 1 [wild] » est **supprimée** : la carte imprimée ne génère aucune ressource, elle ne fait qu'autoriser. Un coût de 3 payé depuis l'autre main passe malgré l'inclinaison en cours de paiement, l'autorisation étant contrôlée avant les dépenses. **Lovers Quarrel** garde sa seconde option réduite. **Validé par 19 cas** dans `tools/test_capacites.py`, chacun vérifié rouge sur le code bugué : le +2 DEF de Cloak retombe quand Dagger repasse en alter-ego ; l'attaque de base de Dagger frappe DEUX sbires ; et une carte à coût 3 se joue depuis une main vide côté Cloak, mais plus si Forces Combined est incliné. Leçon de harnais au passage : `Puzzle.Attack` faisait agir le joueur COURANT, pas le contrôleur de la carte — dans une partie à deux joueurs, faire attaquer le héros du second ne produisait rien du tout. Le deck de départ est bi-aspect Protection (Cloak) + Aggression (Dagger), règle « exactement 2 aspects » dans `reglesAspect`. |

| pack `spider_man_rainy` (71001a-71017) | héros custom **Spider-Man (Peter Parker)** (par « Rainy », scans Drive) créé le 3/8/2026 : 15 cartes signature autour des **compteurs toile** (« web an enemy » = 1 compteur `web`, plafond 3 par ennemi) + carte de règles **Impact Webbing** (71012, Permanent/Setup, `set_aside` + `SetupPutIntoPlay` sur l'alter-ego, modèle The Trunk) qui porte le plafond ET l'effet : à l'activation d'un ennemi entoilé, retrait de tous les compteurs et `-1 SCH / -1 ATK` par compteur pour cette activation (`GainATKForThisAttack` / `GainSCHForThisScheme` négatifs sur `WhenUnitWouldAttack` / `WhenUnitWouldScheme`). Ressources signature Great Power / Great Responsibility à effet différé (montage 68007, `WhenYouSpendThisCardToPlay` + abilité portée par l'identité). Obligation Bad Publicity (Uses 3 menace, retrait à chaque ennemi/plan vaincu par le joueur) + set némésis **Mysterio** (compteurs `illusion` encaissant les dégâts à sa place, cartes rencontre face cachée). Deck de départ Justice du Spider-Man officiel (`deck/starter/spider_man_rainy.json`). Écarts assumés : Webbed Up pose toujours ses 3 compteurs (« up to 3 », jamais désavantageux) ; le « picture of Spider-Man » de J. Jonah Jameson est lu comme « carte du set signature autre que JJJ » ; l'Interrupt de Ben Reilly est rendu en interruption sur ses pouvoirs de base attaque/parade. **Validé par 10 cas** dans `tools/test_capacites.py`. Audit : 2 suspicions `marqueur_sans_capacite` (71001a, 72001a), faux positifs — les Responses « après ennemi vaincu » passent par `WhenUnitWouldBeDefeated` en interne, même famille que Wasp 13001a. **~~Non couverts par le harnais~~ — PERIME, tous couverts depuis le 10/8/2026** (voir la note en fin de §8) ; motif d'epoque (pas de déclencheur d'attaque ennemie dans l'API Puzzle) : Impact Webbing en situation réelle, Webbed Up (défense), Spider-Sense (pioche + annulation de boost via `CancelBoostAbility`), Just Like Flies (engagement) — fabriques standards, à vérifier en partie réelle. |
| pack `venom_rainy` (72001a-72015) | héros custom **Venom (Eddie Brock)** (par « Rainy », scans Drive) créé le 3/8/2026 : 15 cartes signature (tempo agressif : Symbiotic Bond génère 1 [wild] contre 1 dégât, Hunger soigne à chaque ennemi vaincu, Symbiotic Fury redresse après dégâts subis, Bulletproof se remélange au deck, Just A Snack lit `paid_this_resources` pour son bonus [physical] — montage Stand Fast/Ashley Barton). Obligation We Hunger (flip FORCÉ en forme héros + choix dégâts/menace) + set némésis **Carnage** (Forced Response « après un soin, 1 dégât » construit à la main sur `Message.AfterUnitHealHealth`, modèle The Thing 67001b ; Symbiote Rioter ×3 Guard/Patrol). Deck de départ Protection du Black Panther officiel (`deck/starter/venom_rainy.json`). **Validé par 10 cas** dans `tools/test_capacites.py` (124/124 au 3/8/2026, les 2 packs confondus). Non couverts : Camouflage et Lethal Protector (interruptions sur attaque ennemie), Sharp Teeth overkill/piercing (attaque de base non pilotable). |
| `game/card/face/card_face.py` (TRAITS + COUNTER) | traits `MIDNIGHT SON`, `WEB`, `JOURNALIST`, `TITLE` et compteurs `illusion`, `menace` ajoutés pour les packs spider_man_rainy / venom_rainy (`# CORRECTIF`) |
| pack `jessica_jones` (73001a-73022) | héroïne custom **Jessica Jones** (par « ekAugust », scans Drive) créée le 4/8/2026. Tout le kit tourne autour des **manigances secondaires** : *Hard-Hitting Investigation* frappe pour la valeur d'ATK à chaque manigance vaincue, 8 des 15 cartes signature comptent ou exigent une manigance en jeu. Le pack apporte deux choses que le moteur ne connaissait pas. (a) Le set de rencontre **« On the Job »** (73012-73016, `data/encounter_sets/on_the_job.json`), mélangé au deck Rencontre par le **Setup de l'alter-ego** : le seul point d'accroche possible est `Message.WhenGameBeginSetup`, où l'on ajoute `"on_the_job"` à `message.encounter_set_names` — après, `World.Begin` a déjà créé PUIS mélangé le deck (étape 10), et un `ShuffleAllTo` arriverait trop tard. L'ability est enregistrée en `RegisterTemp` depuis `WhenPlayerSelectHero`, qui passe avant. (b) Le mot-clé maison **INVESTIGATE X** (« When revealed, move X threat from the main scheme to here ») (mécanisme détaillé dans mots-cles/investigate-x.md). Compteur `evidence` ajouté au moteur pour Jessica's Camera, dont les trois paliers (1/2/3 → +1 DEF/THW/ATK) sont trois `GiveKeywordToAttached` distincts sur `OnEvent.Counter`. Obligation Stable Home Life + set némésis **Purple Man** (« Look At Me! », Purple Man, « I've Got Everyone » ×2, The Purple Children). Deck de départ Justice de l'insert (`deck/starter/jessica_jones.json`), dont **les 25 cartes d'aspect existent toutes** dans la collection. Les trois ressources doubles redessinées du pack (JJ23-25) sont livrées en **collection d'art alternatif** `ekaug_jj` (§12 bis) et non en cartes : valeurs de jeu identiques à 01088-01090, seule l'image change. Écarts assumés : (a) **Power Couple** (73022) est imprimée « Team-Up (Jessica Jones and Luke Cage) », mais Luke Cage est ici l'**allié signature** 73002, pas un héros — la clé `TeamUp` de `cards.json` suppose deux identités en jeu, la restriction est donc portée par une condition de jeu du script ; (b) l'ATK de **Purple Man** est imprimée « ★ » (il n'attaque jamais, son Forced Interrupt remplace l'attaque par de la menace) et vaut 0 dans les données, aucune valeur non numérique n'étant acceptée ; (c) « si tu as vaincu une manigance secondaire **ce round** » (The Truth Hurts) n'existe pas dans `player_stat.py` : un marqueur maison est posé sur `effect.world` par une capacité silencieuse `Temp0` portée par les DEUX faces d'identité, Crack the Case étant une simple « Action » jouable aussi en alter-ego. **Validé par 7 cas** ajoutés à `tools/test_capacites.py` (dont un témoin sur les paliers de la caméra, et la règle d'or vérifiée en cassant `Investigate`). L'audit signale 1 suspicion `marqueur_sans_capacite` (73006 Out in the Open) : faux positif identique à Enhanced Spider-Sense 01004 et Get Behind Me! 01078, la carte ANNULE un « When Revealed » au lieu d'en porter un. **~~Non couverts par le harnais~~ — PERIME, tous couverts depuis le 10/8/2026** (voir la note en fin de §8) ; motif d'epoque (pas de déclencheur d'attaque dans l'API Puzzle) : le Forced Interrupt de Purple Man, l'Interrupt de Jessica's Jacket et celui d'Out in the Open, à vérifier en partie réelle. |
| `game/card/face/card_face.py` (COUNTER) | compteur `evidence` ajouté pour le pack jessica_jones (`# CORRECTIF`) |
| pack `agent_anti_venom` (74001a-74016 + `aav_traitor_minion`) | héros custom **Agent Anti-Venom / Flash Thompson** (par « DesignHacker », scans Drive, version 3.0) créé le 4/8/2026. Le kit entier lit **« exactly 10 hit points remaining »** : 10 est aussi le total imprimé, la condition vaut donc « intact », mais on compare bien les PV COURANTS à 10 et jamais `health` à `max_health`, sinon un bonus de PV la satisferait à tort. Elle pilote *Ten Out of Ten!* (+1 THW/ATK/DEF et piercing) et les moitiés conditionnelles de Dig Deep et d'Extricate. **Deux mots-clés maison** : (a) **`drain X`**, utilisé par Unlikely Allies et Bear Arms mais **défini nulle part sur les cartes fournies** (aucun insert dans les trois dossiers Drive, rien trouvé en ligne) — lecture arrêtée avec l'utilisateur le 4/8/2026 : *X dégâts à l'ennemi, puis X soins sur Agent Anti-Venom, et sur lui seul* (mécanisme détaillé dans mots-cles/drain-x.md) ; (b) **`traitor`**, lui défini en toutes lettres sur les cartes qui le posent (mécanisme détaillé dans mots-cles/traitor.md). Obligation Spread Too Thin + set némésis **Maniac** (The Made Men, Infected Scorpion, Infected ×2). Écarts assumés : (a) **Bear Arms** « next attack gains ranged » n'a pas de durée équivalente dans le moteur : capacité `UnitAttackGainKeyword` temporaire sur l'identité, retirée dès sa première exécution ; (c) **Anti-Venom Goo** cumule une réduction de coût et un décompte de surpaiement : montage Pure Lightforce 70006 (effet différé porté par l'identité, `paid_this_resources` vs `this_effect_need_cost`) doublé d'un `ReduceCostToPlayFaceWhen` ciblé sur l'effet en cours ; (d) **The Made Men** est imprimée « Forced Interrupt: **After** Maniac schemes or attacks » (contradictoire) et est câblée en `ForcedResponse` sur `AfterEnemyActivationEnd` ; (e) **aucune decklist d'aspect n'est fournie** par l'auteur : deck Protection du Core Set retenu (soin, retaliate, défense), choix consigné dans `metadata.aspect_note` de `deck/starter/agent_anti_venom.json`. **"I've Got This!"** (« 7 damage instead if this attack has ranged or piercing ») ne devine RIEN : la carte porte `SetLabel('attack')`, donc `DealDamage` passe par `CanAttack.SpecialAttack` (voir `is_like_attack`) et c'est une vraie attaque. Le moteur résout les mots-clés (`CheckIfAttackMessageHasKeyword`) puis envoie `WhenUnitMakeKeyWordAttack` si l'attaque en a au moins un : la carte s'y accroche via une capacité temporaire et ajoute ses 2 dégâts. Conséquence voulue, demandée le 4/8/2026 : n'importe quelle carte d'aspect **extérieure au pack** qui accorde ranged ou piercing aux attaques du héros compte pour le bonus. Deux impasses avant d'y arriver, à ne pas refaire : `WhenRecalculateAttackDamage` posé en `Ability` brute n'est jamais appelé, et `UnitGetATKWhileAttackingInternal` filtre sur les attaques **de base** uniquement. **Validé par 9 cas** ajoutés à `tools/test_capacites.py`, dont un témoin blessé qui tombe si le buff de Ten Out of Ten! devient inconditionnel (règle d'or vérifiée). Leçon de données : le bonus d'un **attachement** se déclare avec la clé `ATK+` (Concussion Blasters 01153) et non `ATK`, faute de quoi la création de partie plante sur `KeyError: 'ATK'`. L'audit signale 1 suspicion `marqueur_sans_capacite` (74014), faux positif du point (d). **~~Non couverts par le harnais~~ — PERIME, tous couverts depuis le 10/8/2026** (voir la note en fin de §8) ; motif d'epoque (l'API Puzzle n'a ni déclencheur d'attaque ni activation d'action de carte en jeu) : le `drain 1` de Bear Arms, Unlikely Allies, Anti-Venom Goo, l'Interrupt de Spider-Man 74002, Maniac, The Made Men et le `traitor` d'Infected Scorpion, à vérifier en partie réelle. |

| pack `moon_knight` (76001a-76024) | héros custom **Moon Knight** (par « DesignHacker », scans Drive « MC4 Sealed ») créé le 4/8/2026. **Première identité du moteur à CINQ faces** : Moon Knight (héros, Aggression -1), Marc Spector (alter-ego de départ, main de 7), Mr. Knight (héros, Protection -1), Steven Grant (alter-ego, Leadership -1), Jake Lockley (alter-ego, Justice -1) — chaque personnalité réduit de 1 le coût des cartes de « son » aspect via `ReduceCostToPlayFaceWhen`, doublé d'un second réducteur pour l'événement signature bi-classe correspondant (« This card is both a Moon Knight card and an X card », le moteur n'ayant qu'une classe par carte). Deck de départ = **decklist officielle du scan** (27 cartes d'aspect, toutes présentes dans la collection), règle *Cheap Shots* (tous les aspects, aucun coût imprimé ≥ 3, ≥ 4 cartes par aspect en comptant les bi-classes) vérifiée à la main et affichée dans `reglesAspect` du deck-builder. Le pack apporte aussi le **set modulaire « Age of Khonshu »** (`data/encounter_sets/age_of_khonshu.json`) : 4 héros corrompus en sbires ELITE Villainous dont le When Defeated **crée à la volée l'artefact lié** (Mjolnir, Eye of Agamotto, Hell Charger, Iron Fist) via `CardFactory.GenerateCard` et le met en jeu sous le contrôle du joueur qui a porté le coup (`has_defeating_player=True`) — les 4 artefacts ne sont dans aucun deck. Écarts assumés : (a) la **pile d'identités** de l'insert (interdiction de revenir à une face quittée avant la fin de la phase) n'est pas câblée — bloquer un choix du menu coûterait l'action (leçon Losing Control TAH) ; (b) **Seek Help** : « discard Steven Grant and Jake Lockley from the IDENTITY stack » devient « exhaust Marc Spector », le moteur ne sachant pas retirer des faces ; (c) **Gear Up** « until the end of the round » rendu par `GainUntilPhaseEnd` (l'attaque a lieu en phase du méchant) ; (d) **Versatility** « treat as any aspect » est purement deck-building, non câblé. Traits `IDENTITY`/`ARTIFACT` ajoutés (`# CORRECTIF`). **Validé par 16 cas** (dont : départ sur la bonne face parmi 5, réduction en chaîne FoF→Deck and Cover gratuite, Echo copiant les stats du héros actif, Frenchie annulant la menace, Bushman immortel une fois, Thor→Mjolnir, limite par aspect de Different Strokes). **Leçons harnais** (corrigées dans `tools/test_capacites.py`) : les identités multi-faces exposent des options `Change_To_<Face>` (et non `Change_Form`), ajoutées aux déclencheurs du pilote ; `AfterPlayerPlayedCard` a pour trigger le JOUEUR, la carte jouée est `message.played_face` ; c'est `WhenUnitWouldBeDefeated` (modèle Loki 55029a) qu'il faut pour un « heal instead of defeat », pas `WhenUnitBeDefeated` ; poser la menace AVANT Frenchie en mise en place, sinon le pilote le défausse sur le SetThreat. **~~Non couverts par le harnais~~ — PERIME, tous couverts depuis le 10/8/2026** (voir la note en fin de §8) ; motif d'epoque : Gear Up et Khonshu-action (pas de déclencheur d'attaque/d'activation de plateau), Mjolnir/Eye/Hell Charger/Iron Fist artefacts (créés en jeu mais capacités à vérifier en partie réelle). ⚠ Le pack a d'abord été numéroté 71xxx puis 73xxx : tranches prises en parallèle par `spider_man_rainy`, `venom_rainy` et `jessica_jones` — TOUJOURS vérifier les doublons de `card_id` sur TOUTE la collection avant de choisir une tranche. |

⚠️ **`identity.ChangeForm(effect)` N'EXISTE PAS.** Pour faire changer une
identité de forme depuis une carte, c'est `identity.ChangeToForm(Hero, effect)`
ou `ChangeToForm(AlterEgo, effect)` (`game/card/face/card_type/identity.py`),
comme le fait We Hunger 72012. Le piège est vicieux : `test_cards.py` ne voit
rien (la construction des capacités ne touche pas au corps des handlers), et
`test_capacites.py` non plus quand l'appel est dans une branche **optionnelle**
(`MayChooseOneAbility`) — le pilote de test décline systématiquement les choix
optionnels, donc la ligne fautive n'est jamais exécutée. Défaut trouvé le
4/8/2026 sur les obligations de `jessica_jones` et d'`agent_anti_venom`, par
introspection des attributs plutôt que par les tests.

| pack `lockjaw` (78001a-78030) | héros custom **Lockjaw** (par « Nugget », Marvel Champions Custom Project Cycle I, scans Drive) créé le 4/8/2026. Le chien téléporteur des Inhumains : 15 cartes signature bâties sur le trait **TELEPORT** (la plupart font changer de forme), plus **13 cartes d'aspect « Lockjaw and the Pet Avengers »** (78018-78030 : Zabu/Agression, Throg/Justice, Redwing/Leadership, Hairball et Lockheed/Protection, Ms. Lion, Ms. Marvel, Central Park et 4 autres en Basic). Deck de départ = **decklist officielle du scan** (aspect Protection, 15 + 25 cartes, toutes présentes). Écarts assumés : (a) ~~la carte imprime une ressource « os » propre au pack~~ **FAUX, corrigé le 10/8/2026** : cette icône est la ressource **mentale**, et la lire comme un os avait fait rendre quatre cartes par un [wild]. Fetch!, Fast Travel, Zooming Around et Ruff Ambush testent désormais la couleur **B**. Voir le §4.1 sur la façon de vérifier une icône ; (b) **Companion** (« ne compte pas dans la limite d'alliés et ne peut pas défendre ») est un mot-clé maison (mécanisme détaillé dans mots-cles/companion.md) ; (c) **Tuning Fork** : `during="YourTurn"` est refusé par le moteur dès que la carte visée n'est pas « This » (assert dans `YouMayPlayCardLikeInHand`), la clause est omise — sans effet pratique, un soutien ne se jouant que pendant son tour ; (d) **Ms. Marvel** : ses deux « Interrupt » étoilés se déclenchant à chaque activation, ils sont rendus par un bonus permanent `attack/thwart + *_consequential_damage` (même écart que Fin Fang Foom 68016) ; (e) **Provoked** vérifie son seuil de 3 compteurs `calm` dans la Response qui les pose, plutôt qu'en Interrupt séparé. Traits `PET AVENGER`/`GOOD BOY`/`TELEPORT`/`KING`/`ARTHROSIAN`/`HAMSTER`/`SAVAGE LAND`/`X-MAN` et compteur `calm` ajoutés au moteur (`# CORRECTIF`). **Validé par 12 cas** (setup de Tuning Fork, Kamala's Room, Ms. Marvel, Annihilus renvoyé au deck Rencontre, Provoked qui verrouille la forme héros, Dognapped! nourri par les TELEPORT, paiement par la fourchette, Wet Slobbering Kiss, Zooming Around, Companionship, Animals Unleashed, Psionic Tracking). **Leçon** : « chaque ennemi engagé avec ce joueur » ne se cherche PAS par un filtre d'engagement — le moteur n'en expose pas pour le vilain ; il faut le montage de la carte officielle **Energy Daggers (01046)**, `Worlds.FindVillain()` + `player.GetEngagedMinions()`. L'audit signale 2 suspicions `marqueur_sans_capacite` (78017, 78026) : faux positifs, ce sont les écarts (d) et (e). **~~Non couverts par le harnais~~ — PERIME, tous couverts depuis le 10/8/2026** (voir la note en fin de §8) ; motif d'epoque (pas de déclencheur d'attaque ni d'action de plateau dans l'API Puzzle) : Fetch!, Cheer Up, Doc Jaw's Lab, New Attilan, Ruff Ambush, Teleport To Safety, Jaw Lock, Black Bolt, Hairball, Zabu, Lockheed, Dog Catcher — à vérifier en partie réelle. |

| `game/selector/selector.py` + `game/card/face/model/face_gain.py` | **deux points d'accroche** posés pour le pack `squirrel_girl` : une face peut déclarer `refuse_target_fn(effect)` (elle n'apparaît plus dans les cibles légales) et `refuse_gain_fn(effect)` (elle refuse tout bonus). Inertes tant qu'aucune carte ne les arme (`getattr` rend `None`), donc sans effet sur les 4600 autres cartes. Seul moyen de rendre « les écureuils ne peuvent être ni choisis ni renforcés par une carte joueur hors du set » : `Gain` est `@final` et appelée en direct, sans message interceptable, et la sélection de cibles n'a qu'un seul entonnoir, `GetAllLegalTargets`. |
| pack `squirrel_girl` (75001a-75022) | héroïne custom **Squirrel Girl** créée le 5/8/2026 à partir d'un brief markdown, **arbitrée carte par carte avec l'utilisateur** (9 décisions, voir plus bas). Un **DECK ÉCUREUIL** de six alliés mis de côté au setup, monté comme le deck d'invocation de **Doctor Strange (09001b)** : `BeginGameWithSetAside` puis `Faces.ShuffleAllTo(additional_deck)`, et un `WhenCardWouldMoveToArea` posé sur chaque écureuil renvoie sa défausse vers `additional_discard_pile`. Deux notions maison, toutes deux dans le `__init__` du set : **appeler** un écureuil (révéler le dessus, le mettre en jeu épuisé, remélanger la défausse écureuil si le deck est vide) et **dépenser** un écureuil. La « réduction de coût de 1 » du matériel d'origine est rendue par une capacité `Resource` portée par chaque écureuil (défausse en coût, `for_card=CardFinder(set_name="Squirrel Girl")`) : effet identique à la table, et le moteur sait alors dire « si tu as dépensé un écureuil » par le message `WhenCardBeSpendAsResource`, sur lequel s'accrochent Unbeatable Army (identité), Nuts!, The Gatherer et The Forager. Mot-clé maison **Squirrel** (mécanisme détaillé dans mots-cles/squirrel.md). Écarts assumés : (a) **Network of Trees** n'a pas de capacité propre — le moteur n'a pas de message « quand tu appellerais un écureuil », l'interruption est résolue dans `AppelerEcureuil`, seul point de passage de tous les appels ; (b) **Discord in the Branches** ne porte pas le blanchiment : le moteur ne rend blanche qu'une face désignée, donc chaque capacité d'écureuil teste elle-même la présence de la manigance (`PasDeDiscorde`) — un septième écureuil devrait reprendre la condition ; (c) **Ratatoskr's Whispers** ne porte pas l'interdiction de dépense : c'est la capacité `Resource` de chaque écureuil qui vérifie sa présence ; (d) le Boost de Poisoned Rumors épuise dès le retournement au lieu de « after this activation ends » (sans conséquence : un écureuil n'agit jamais pendant l'activation d'un ennemi). **Écarts au brief d'origine, tous validés en multichoix le 5/8/2026** : le Costume déclenche sur « un sbire est vaincu » et non sur l'attaque de base (ATK 1, le moteur ne démarrait jamais) ; The Bruiser absorbe le **dégât conséquent** d'un autre écureuil en s'épuisant, au lieu de rediriger des dégâts de rencontre que les écureuils ne subissent jamais (ils ne défendent pas) ; Squirrel Swarm passe à 3 dégâts +3 si un écureuil a été dépensé ; The Forager récompense la dépense et non l'entrée en jeu ; l'obligation reprend le gabarit officiel (« défausse cette obligation », 1 écureuil) ; Poisoned Rumors reprend le squelette « sinon » sans choix libre. Traits `SQUIRREL`/`STUDENT`/`SUIT`/`NETWORK`/`ASGARDIAN` ajoutés au moteur. Deck de départ Agression du brief (25 cartes d'aspect, toutes présentes), **sans Boot Camp** : remplacé par Martial Prowess, puisque les écureuils refusent les bonus extérieurs. **Validé par 19 cas** ajoutés à `tools/test_capacites.py`, dont un **témoin** qui prouve que Boot Camp augmente bien un allié ordinaire, sans quoi le cas du refus de bonus passerait même si le point d'accroche était mort. **Leçon** : les cartes d'un deck (hors jeu) ne se désignent PAS par `SetTarget(Select.From(faces=...))` — le sélecteur ne les restreint pas, et le pilote a choisi le vilain puis l'a déplacé dans le deck écureuil ; il faut `player.MayChooseFace(faces, effect)`. Autre leçon : `Puzzle.PutIntoPlay` crée une copie NEUVE de la carte, qui n'a reçu aucune règle du setup — tout cas portant sur les règles d'écureuil doit faire APPELER l'écureuil par le jeu. **Validé par 28 cas, 22 cartes sur 23** — seul The Lookout, carte volontairement vierge, n'a pas de cas dédié. Y arriver a demandé **trois ajouts au harnais**, décrits au §8 : `Puzzle.Attack(defender=...)`, `Puzzle.PutIntoPlay(under_control=True)` et la clé de cas `accepter_choix`. La limite « **1 seul écureuil par carte jouée** » a coûté une refonte du montage, le 6/8/2026 : la capacité `Resource` n'est PAS portée par les six écureuils mais par les deux faces d'**identité** (« Squirrel Aid »), avec pour coût de défausser un écureuil que tu contrôles. Le moteur recense les sources de paiement une seule fois, avant toute dépense, et une capacité ne compte que pour une source : six capacités = six écureuils dépensables, et refuser une source déjà recensée fait tomber l'assertion `len(resources_effects) == 1` de `ProcessPayingEffect`. La limite n'est donc pas exprimable a posteriori ; avec une source unique elle est structurelle, et le joueur choisit toujours quel écureuil part, via le coût. Conséquence : les réponses « après avoir dépensé cet écureuil » (The Gatherer, The Forager) ne se lisent plus sur `WhenCardBeSpendAsResource` — le déclencheur serait l'identité — mais sur le **départ du jeu** de l'écureuil, quand la marque de dépense le désigne (`ReponseALaDepense`). L'audit signale 2 suspicions sur le pack, toutes deux faux positifs : **75012** (marqueur `Interrupt` et `exhaust_sans_cout`, l'interruption vit dans l'appel — même cas que Forces Combined 70003) et **75003** (marqueur `Response` : le moteur transforme un `AfterUnitDefeatedUnit` en capacité « Delay Ability », exactement comme l'allié Hercules 68002 ; le comportement est prouvé par son cas). |

| **La zone RÉSERVE** : `game/deck/deck_type.py`, `game/player/player.py`, `game/card/card.py`, `game/player/action/player_get.py`, `game/world/game_area/game_area.py`, `game/render/to_descriptor.py` + `descriptor/world.py`, `game/effect/effect_context.py`, `game/player/action/player_action.py`, `game/ability/cost_func.py`, `game/ability/factory/resources.py` | Mécanique maison du pack `brawn` (7/8/2026), et **première zone de joueur ajoutée au moteur**. L'insert la définit comme « an out of play area that functions in a similar manner to the hand » : 3 cartes au plus, on y joue des cartes en payant leur coût, on peut y défausser des cartes pour générer leurs ressources, et **les deux zones ne se mélangent jamais dans un même paiement**. Montage : (a) `DeckType.ReserveArea` **arme le drapeau `is_like_in_hand`**, qui était déclaré dans `DeckTypeFlags.Base` sans qu'aucune zone ne s'en serve ; (b) `Card.IsLikeInHand()` lit ce drapeau AVANT son cache `can_state` — sinon la réponse serait figée avant que la carte n'entre en Réserve ; (c) `player.reserve` est créée pour TOUS les joueurs (une zone vide ne coûte rien et le descripteur la rend vide), avec `PutIntoReserve` / `EnforceReserveLimit` qui font redescendre à 3 en faisant CHOISIR au joueur, comme la limite de main ; (d) `CostFunc.ReturnToReserve`, calque de `ReturnToHand`, pour le coût imprimé de Silk 77002 ; (e) le cloisonnement du paiement dans `CheckThisCanDropPay`. ⚠ **Le piège du cloisonnement** : la liste des payeurs est dressée par `UpdatePayResources` AVANT que la carte jouée parte en zone de traitement, et relue APRÈS au moment de dépenser — à ce moment plus rien ne dit d'où elle venait. D'où `effect.context.play_from_area`, posé dans `ResolveEffect` juste avant le déplacement. Le moteur ne peut trancher que la moitié déterministe de la règle (carte jouée depuis la main → payeurs de la main seulement, et symétriquement) : pour un coût qui n'est ni l'un ni l'autre (capacité d'une carte en jeu, carte de rencontre), il propose légitimement les deux zones puisque le joueur n'a encore rien choisi. **Le mélange est donc fermé côté plateau**, au moment du clic (`ui-app/src/board/interaction.ts`, couvert par `reserve-cloisonnement.test.ts`, 4 cas dont 3 vérifiés rouges sans le correctif) |
| pack `brawn` (77001a-77025) | héros custom **Brawn / Amadeus Cho** (par « Rainy », scans Drive + zip `Brawn-20260807T065409Z-1-001.zip`) créé le 7/8/2026. 15 cartes signature bâties sur la **Réserve** (voir la ligne ci-dessus) : *Mastermind Excello* la remplit depuis le dessus du deck, *Cho's Lab* depuis le dessous à chaque changement de forme, et **trois cartes récompensent le fait de jouer DEPUIS la Réserve** (Brawn's Suit → 1 dégât, Forward-Thinking → redresse l'identité, Totally Awesome → 1 menace retirée). *The Complete Package* inverse le réflexe habituel des identités génératrices : Brawn génère un [mental] **parce qu'il est déjà épuisé**, là où Peter Parker ou Star-Lord s'épuisent POUR générer. Obligation Analysis Paralysis + set némésis **Namor** (Rising Tide pose 1 jeton d'accélération par round, et Namor gagne +X ATK/SCH pour X jetons EN JEU — la manigance se nourrit elle-même). Deux alliés signature **alternatifs** portant le même numéro (Silk 77002, Ironheart 77003), chacun avec son Team-Up. Deck de départ Protection `deck/starter/brawn.json`. **Écarts assumés** : (a) **aucune decklist d'aspect n'est fournie** par l'auteur — Protection retenu avec l'utilisateur, motif dans `metadata.aspect_note` ; (b) les deux **Team-Up** sont imprimés « Brawn and Silk » / « Brawn and Ironheart » alors que Silk et Ironheart sont ici des ALLIÉS : la clé `TeamUp` de `cards.json` suppose deux identités en jeu et rendrait les cartes mortes en solo, la restriction est donc une condition de jeu (`SetCondition(only_if_you_control_face=...)`), montage de Power Couple 73022 ; (c) **Hulk Out** est imprimée « For each rage counter here, Brawn gets +1 ATK and +1 DEF and gains retaliate 1 » — arbitré avec l'utilisateur le 7/8/2026 : le « for each » porte sur l'ATK et la DEF, **pas** sur riposte, qui reste à 1 ; (d) une icône **[wild]** défaussée compte pour chaque couleur dans Shockwave et Brains and Brawn, comme le fait Hulk 01050 (carte officielle au montage jumeau). **Validé par 29 cas** ajoutés à `tools/test_capacites.py` (429/429 au 7/8/2026), dont **trois témoins** : Gamma Strike payée en [energy] doit faire 7 dégâts et pas 10, Namor doit voir ses stats MONTER quand un jeton s'ajoute (un bonus figé à l'entrée en jeu passerait sinon), et Strong as Silk doit être jouable AVEC Silk en jeu — ce dernier a fait tomber un vrai défaut. ⚠ **`SetCondition(only_if_you_control_face=...)` ne voit pas les alliés** : la clause fouille `GetIdentity().GetInventoryDeck()`, c'est-à-dire les cartes ATTACHÉES à l'identité. Employée pour les deux Team-Up, elle était donc silencieusement TOUJOURS fausse et les rendait injouables en toutes circonstances — le cas « injouable sans Silk » passait pour la mauvaise raison. Il faut une condition maison dans le paramètre `conditions=` de la fabrique, qui parcourt `joueur.allies`. C'est exactement le faux vert que le cas symétrique existe pour attraper. La clé de vérification `en_reserve` / `taille_reserve` a été ajoutée au harnais. **Leçon de test** : le premier cas de Gamma Strike était faux, pas la carte — Haymaker 01087 porte une ressource **énergie**, pas physique ; le paiement « uniquement [physical] » se monte avec Counter-Punch 01077. Même chose pour Silk, dont le cas posait 01096 (Rhino, le **vilain**) là où son action réclame un sbire. ⚠ **« Put this card into your reserve » ne se code PAS en déplaçant la carte** : un événement est défaussé par `Event.OnAfterPlay` APRÈS la résolution de son effet, et le déplacement fait pendant l'opération est écrasé (mesuré : la carte arrivait bien en `ReserveArea`, puis repartait en défausse). Le crochet est `Message.WhenCardWouldDiscard` + `SetToArea`, centralisé dans `RecyclerVersLaReserve()` du `__init__.py` du set. **Deux pièges s'y cachent** : (a) le moteur envoie ce message **plusieurs fois** pour une même carte (4 fois, mesuré) — les premiers envois sont des contrôles, seul le dernier défausse ; avec `unregister_after_exec=True` l'abilité disparaissait donc après un simple contrôle et la vraie défausse partait sans redirection ; (b) l'abilité restant armée, elle doit refuser de rediriger une défausse **venant de la Réserve**, sans quoi la carte y resterait prisonnière même quand la limite de 3 veut l'en sortir — d'où le filtre `is_processing`. ⚠ **Collision de nom** : `* Amadeus Cho` existe déjà en 68001b (pack `totally_awesome_hulk`), et `Worlds.FindPlayerByName` (obligation `GiveTo`) rend le PREMIER joueur qui porte le nom. **Instruit le 7/8/2026, conclusion : rien à corriger dans le moteur.** (a) La configuration n'est pas atteignable : Brawn et Totally Awesome Hulk sont deux versions du MÊME personnage, que les règles interdisent d'asseoir à la même table — et le projet vit déjà avec 9 collisions identiques (Peter Parker 01001b/71001b, Venom, Thor, Spider-Man…). (b) Le correctif tenté — préférer le propriétaire de la carte — **ne peut pas fonctionner** : mesuré, `Obligation.GetOwner()` rend le SCÉNARIO (`Rhino`) et non le joueur, l'obligation vivant dans le deck Rencontre. Il a donc été retiré plutôt que de laisser dans le moteur un correctif inopérant touchant tous les packs. Seule conséquence pratique, déjà connue : **ne jamais désigner cette identité par son nom dans un cas de test** (le harnais Puzzle cherche aussi par nom). ⚠⚠ **UNE CARTE QUI SE RECYCLE VERS LA RÉSERVE PENDANT UNE FENÊTRE DE RÉACTION DOIT BORNER SON DÉCLENCHEUR.** Trouvé en partie réelle le 7/8/2026 sur Calculated Defense 77004/77005. La carte payée en [mental] depuis la main revient en Réserve — or la Réserve est une zone « comme en main » : la carte y **redevenait immédiatement jouable, dans la même fenêtre de défense**, qui n'était pas encore refermée. Le jeu reproposait « Play Calculated Defense » sans fin, chaque tour de boucle relançant la séquence d'attaque, et le joueur finissait sans aucun paiement possible. Une carte ordinaire ne connaît pas ce problème : elle part en défausse et cesse d'être jouable. Correctif : `.LimitOncePerEvent()` sur le déclencheur — **par ÉVÉNEMENT et non par phase**, pour qu'un second exemplaire reste jouable sur la même défense, ce que le texte imprimé autorise. Gamma Strike 77006/77007 se recycle aussi mais n'est PAS concernée : son déclencheur est une action de tour (`WhenInYourPlayTurn`), pas une fenêtre forcée — le joueur garde la main et la rejouer est le cycle voulu. |

⚠ **Corollaire côté plateau** : une option engagée doit TOUJOURS offrir une issue. `BarreAction.tsx` masquait le bouton secondaire dès qu'une option était choisie (`option !== undefined ? null`), si bien qu'un joueur incapable de payer restait coincé et que le moteur reposait la même question à l'infini. Un bouton « Abandonner » est désormais affiché dans ce cas (couvert par `BarreAction.test.tsx`). Le cloisonnement main/réserve rend cette impasse bien plus facile à atteindre, puisqu'il retire des payeurs.

⚠ **Pour tester une carte JOUÉE DEPUIS LA RÉSERVE**, deux clés de cas ont été ajoutées au harnais : `reserve` (dépose des cartes en réserve) et `jouer_reserve` (joue une carte qui s'y trouve, en payant vraiment). **Le carburant doit être DANS la réserve** — c'est tout l'objet du cloisonnement — et il en faut **un de plus que le coût** (parade du §10 sur la collision d'ids du pilote). Sans cela la carte reste impayée et se fait défausser, ce qui imite à la perfection une capacité morte : c'est ce qui a fait croire un moment que Brawn's Suit et Totally Awesome étaient cassées, alors qu'elles sont justes. **Non couvertes, à vérifier en partie réelle** : les seules capacités **Boost** d'Imperius Rex 77021 et de Tidal Surge 77022/23. ⚠ **`Puzzle.Boost` n'émet PAS `Message.WhenCardBecomeBoost`** — mesuré le 7/8/2026 en armant les deux fabriques à la fois : seul `WhenBoostCardTurnedFaceUp` part par cette voie. Ne pas en conclure que la carte est fausse et basculer de fabrique : **170 traîtrises officielles** emploient `WhenCardBecomeBoost` (Concussive Blast 01154, Heart-Shaped Herb 01158, Titania's Fury 01164…), c'est bien la fabrique des « [star] Boost: ». `Puzzle.Boost` pose la carte au sommet du deck Rencontre puis active le vilain, sans passer par la distribution normale : c'est une limite du HARNAIS. Les deux cas de test écrits pour ces branches ont donc été retirés plutôt que de tordre les cartes pour satisfaire le pilote. Tout le reste du pack est couvert, **y compris l'effet de Strong as Silk** (Brawn à 3 ATK et Silk à 2 : le bonus touche bien les DEUX, pas seulement le héros). |

Règle : toute nouvelle divergence = commentaire `# CORRECTIF` + ligne dans ce
tableau. À chaque synchro avec le dépôt officiel, réappliquer ce tableau
(procédure du 1/8/2026 consignée dans `HANDOFF-V2.md`).

## 10. Pièges connus

- `set_name` → nom de dossier **nettoyé** (minuscules, `_`) ; en cas de doute,
  regarder comment un set voisin est rangé.
- Type `SideScheme` en JSON = classe `EncounterSideScheme` dans les scripts.
- Oublier le `__init__.py` d'un nouveau dossier de set = cartes silencieusement
  sans capacités.
- Les effets « texte seul » connus (non câblés) sont recensés dans
  `docs/rapports/archive-marvel-work/TODO.md` (ex `~/marvel-work/TODO.md`,
  archivé le 31/08/2026) — vérifier avant de croire à un bug.
- **Tests de comportement, jouer une carte** : `Puzzle.PutIntoPlay` POSE la carte sans la payer, donc ne teste ni la génération de ressources, ni les conditions « si vous avez payé uniquement avec... », ni les capacités Resource. Le harnais expose pour cela les clés `main` (cartes déposées en main comme carburant), `jouer` (cartes jouées depuis la main en payant vraiment) et `payer_avec` (impose QUELLES cartes financent le coût, indispensable quand la ressource dépensée a elle-même un effet). Le pilote remplit le champ `resources` de la réponse à partir de `target_payment` ; sans cela le coût reste impayé et la carte n'est jamais jouée.
- ~~**Limite connue** : les événements qui ciblent un complot ne se jouent pas par cette voie.~~ **CORRIGÉ le 7/8/2026** : ce n'était pas une limite du harnais. Un événement qui RETIRE de la menace n'a aucune cible légale tant qu'aucun complot n'en porte — `CanPlayBy` rend alors `False` et la carte reste en main, sans le moindre ASK pour le signaler. Il faut donc **poser de la menace en mise en place** : `Puzzle.PlaceThreat('The Break-In!', 3)`. ⚠ Et la doser : à 8, le complot principal AVANCE, la partie repart pour un tour, le joueur repioche, et le cas mesure alors tout autre chose. Heavy Lifting 77008 est couverte depuis. Calculated Strike 68008 et For Justice! 01060 devraient l'être de la même façon.
- **Tests de comportement, paiement** : les clés du champ `payment` des options
  ne sont PAS toujours des ids d'objets (espace d'ids propre aux effets de
  ressource, vu sur venom_rainy où l'identité elle-même est candidate via
  Symbiotic Bond). Deux conséquences : (a) le pilote exclut du paiement la clé
  égale au `bind_id` de la carte jouée — une COLLISION d'ids peut donc lui
  faire perdre une vraie carte de financement (symptôme : coût jamais payé,
  « effect failed » après l'ASK) ; parade : donner une carte de carburant de
  plus que le coût. (b) `payer_avec` traduit les card_id en ids d'objets ; si
  aucune clé ne correspond, un REPLI par couleur de ressource imprimée
  s'applique, seulement quand la couleur désigne un candidat unique (chez
  Totally Awesome Hulk, Hypermind convertit tout en G et le repli se ferait
  au hasard).
- **`Select.From(liste)` est un piège** : l'argument positionnel n'accepte pas
  une liste de faces (TypeError `unhashable type` à la résolution seulement,
  jamais à la construction). Écrire `Select.From(faces=mes_faces)`. Et pour
  cibler « un plan » dans un `ForChoiceAbility`, préférer
  `.SetTarget(Scheme2, range=(1, 1))` : `FindCardsOnField(card_type=...)` ne
  filtre pas les types de plan.
- **Tests de comportement, désignation des cartes** : `Puzzle.*` cherche par NOM (`FindOrCreateFace`), pas par `card_id`. Un `card_id` d'identité fabrique une carte orpheline dans `aside_deck` et fait planter le rendu sur un `AssertionError` opaque. Écrire `Puzzle.ChangeForm('Amadeus Cho')`, pas `Puzzle.ChangeForm('68001b')`. Même chose pour le complot principal : `Puzzle.PlaceThreat('The Break-In!', 8)`. Corollaire : seul `ChangeForm` va dans `mise_en_place`, tout le reste dans `declencher`, sinon la nouvelle forme n'est pas encore active quand la commande suivante cherche son nom.
- **`Puzzle.Attack(x)` fait attaquer X, pas attaquer X.** Pour qu'un héros
  frappe un sbire, on écrit `Puzzle.Attack('<identité héros>')` avec le sbire
  dans `cibles`. Écrire `Puzzle.Attack('<sbire>')` fait activer le SBIRE, qui
  frappe le héros : le relevé montre alors des dégâts sur l'identité et une
  cible toujours en jeu, ce qui se lit comme une capacité qui n'a pas marché.
- **`Puzzle.Damage` sur un sbire ne fait RIEN**, ni par `card_id` ni par nom, et
  sans le moindre message dans le journal : `FindOrCreateFace` rend une face qui
  n'est pas `CanHealth` et la fonction sort en silence. Pour qu'une attaque de
  base achève une cible, monter l'ATK de l'attaquant (une amélioration en jeu)
  plutôt que baisser les PV de la cible.
- **Écrire un cas de comportement : trois pièges qui coûtent plus cher que le
  cas lui-même.** `mise_en_place` ET `declencher` sont obligatoires même vides,
  sinon le harnais lève un `KeyError` brut au lieu d'un message. Une carte qui
  coûte quelque chose ne part pas si la main ne contient aucune ressource, et
  le relevé dit « 0 dégât », exactement comme une carte morte : toujours mettre
  de quoi payer. Et surtout, **un cas peut être vert en n'exerçant rien** :
  Secret Agent ne s'épuisait pas parce que Genius (01089) fournit BB à lui seul
  et couvrait tout le coût ; il a fallu une carte à 3 pour rendre sa ressource
  nécessaire. Vérifier dans le journal du cas que la capacité visée est bien
  passée.
- **`payer_avec` ne fait que PRÉFÉRER une carte, `ne_pas_depenser` en interdit
  une.** Le pilote choisit librement ses ressources : une source déjà en jeu
  passe souvent avant la main. C'est ainsi que Tuning Fork, qui démarre en jeu
  chez Lockjaw, fournissait un wild et faussait deux cas censés prouver un
  paiement en mental. `ne_pas_depenser` prend des `card_id` et écarte leurs
  effets payants. À réserver aux cas dont la COULEUR payée est le sujet.
- **Un wild vaut n'importe quelle couleur.** Une main de wilds satisfait « payé
  en [mental] » : elle ne peut donc pas servir de témoin négatif. Pour prouver
  qu'une clause bonus ne part PAS, payer en physique ou en énergie.
- **Actions RÉPARTIES : les doublons de `all_legal_targets` sont du sens, pas
  du bruit.** Quand un effet se répartit (43006 Regenerative Longevity, « Heal
  a total of 4 damage from your identity and Honey Badger »), le moteur répète
  la même carte dans `all_legal_targets`, autant de fois qu'elle peut recevoir
  d'attributions. Mesuré avec X-23 à 5 dégâts et Honey Badger à 1 :
  `target_num_range = [1, 4]` et `all_legal_targets = [1, 1, 1, 1, 9]`. Un clic
  = une attribution ; il faut donc cliquer QUATRE fois sur la même carte.
  Côté moteur c'est correct (`HealthUnits` compte les occurrences via
  `FacesHelper.ListToDict` et soigne `valeur × occurrences`). Le piège est à
  l'affichage : le panneau annonçait « 1/1 requise(s) » (le minimum) et
  « Confirmer » s'allumait dès le premier clic. Les libellés vivent maintenant
  dans `ui-app/src/board/libelles-cible.ts`, couverts par
  `node outils/verifier-libelles-cible.mjs`. **Toute action à `target_num_range`
  large doit être vérifiée là.** Le seul sélecteur qui produit ces doublons est
  `repeat_rules` (`src/game/selector/selector_rule.py`) : `Sustained` (dégâts
  subis), `Threat`, `Health`, `CanHasConfused`, `Any`.
- **Une carte peut porter DEUX rôles à la fois : payeur, et cible ou source.**
  Le plateau donnait la priorité au premier rôle et sautait la carte pour le
  paiement (`if (etats.has(id)) continue` dans
  `ui-app/src/board/interaction.ts`), rendant sa ressource inatteignable.
  Deux familles étaient touchées :
  - **cible + payeur** : toute amélioration posée sur une carte qui génère
    elle-même des ressources. Venom reçoit le *Sonic Rifle* et le finance avec
    *Symbiotic Bond* ; une fois désigné, le cliquer ne faisait plus que le
    **dé-cibler**. Concerne les **12 identités génératrices** (Peter Parker,
    Star-Lord, Venom, Spider-Ham, SP//dr, Shadowcat, Phoenix, Jubilee, Echo,
    Reed Richards, Sue Storm, Venom/Rainy) et les alliés générateurs (Brawn).
  - **source + payeur** : la carte qui PORTE l'action et la finance elle-même.
  Depuis, on ne saute la carte que si son premier rôle a encore besoin du clic,
  c'est-à-dire tant qu'il reste des cibles à désigner (`roleLibere`). Une carte
  jouée depuis la main n'est jamais proposée comme payeuse d'elle-même par le
  moteur : elle est écartée plus bas, sans traitement particulier.
  Couvert par `src/board/paiement-identite.test.ts` (8 cas, dont l'allié et la
  source) et `src/board/mobile/paiement-identite-mobile.test.tsx`.
  ⚠️ Ces rôles sont les seuls atteignables dans la branche du paiement :
  `porteur`, `cible-preview` et `indisponible` n'existent que dans le menu
  d'actions, qui rend avant. Tout NOUVEAU rôle posé avant ce bloc devra être
  ajouté à `roleLibere`.
  ⚠️ Le moteur, lui, était innocent : il proposait bien les trois moyens de
  paiement. Avant de soupçonner une carte, **capturer le `target_payment` réel**
  (cas `20001a Symbiotic Bond` de `tools/test_capacites.py`, avec
  `TRACE_OPTIONS=1`) : cela départage en une minute le moteur et le plateau.
  ⚠️ Quand une seule cible est légale, le plateau la **désigne tout seul** : un
  test qui simule un clic de ciblage de plus paie en fait une ressource.
- **Deux numérotations de sièges en multi.** L'index technique (`p=` dans l'URL,
  cookie `seat_token_<p>`, index joueur du moteur) commence à **0 pour l'hôte** ;
  l'affichage, lui, parle de « Joueur 1 » à « Joueur 4 ». Les confondre donne à
  quelqu'un le deck de son voisin. La conversion se fait dans un seul endroit,
  `public/js/prepare/salon-etat.js`, vérifié par `node outils/verifier-salon-etat.mjs`.
  Corollaire : le réglage « premier joueur » du wizard est **grisé en multi**,
  parce que `buildDescriptor()` l'applique en faisant TOURNER l'ordre des
  joueurs, ce qui décollerait les sièges des personnes.
- **`launcher-multi.sh` vit dans `Fusion/marvel-lcg-src/`** : c'est de là que
  `JOUER-EN-MULTI.bat` le lance. `~/marvel-work/` ne fournit que
  l'interpréteur Python et `tools/cloudflared`.
- Côté UI, l'affichage multi-vilains (Sinister Six...) repose sur une
  heuristique par noms (`ui-app/src/board/zones.ts`) : à revalider si un
  nouveau scénario multi-vilains est ajouté.
- **Un seul `public/` existe** depuis le 31/08/2026 (le vestige WSL est
  supprimé) : `ui-app/deployer.sh` déploie `dist/` dans la seule
  installation. Le dossier `js/prepare/` (wizard, prefs, deck-builder,
  biographies) est édité à la main, hors dépôt, et directement dans la copie
  vivante : il n'y a aucune recopie à faire ensuite (voir §1.3). Le sens
  destructeur du vieux `deployer.sh` (rsync `--delete` depuis le vestige) a
  été corrigé le 30/08 puis rendu impossible le 31/08 avec la suppression du
  vestige.
- Plusieurs vieilles copies du moteur traînent encore sur la machine et ne
  doivent jamais servir de référence : la liste complète est en §1.4.

## 11. Traduction française

- La narration du moteur est traduite via `data/translate_fr.json` (gabarit
  anglais → gabarit français, mêmes clés que `translate_cn.json`). Activée par
  `translate_file: './data/translate_fr.json'` dans `launch.json` /
  `launch.online.json`. **Pour revenir à l'anglais : mettre `translate_file`
  à `""`** (le moteur retombe alors sur les gabarits d'origine). Redémarrer le
  serveur après changement.
- **Bouton langue 🌐 FR/EN** : présent dans le header du wizard et du plateau.
  Il écrit `localStorage['marvel-langue']`, appelle la route `/set_language?fr|en`
  (bascule à chaud de la table TransText, route dans `server_get.py`) puis
  recharge la page. Côté client, `t('texte français')` pioche dans un
  dictionnaire FR→EN (`ui-app/src/board/langue.ts`, `public/js/prepare/langue.js`) :
  toute NOUVELLE chaîne visible doit passer par `t()` et avoir son entrée EN.
- Un gabarit absent du JSON s'affiche en anglais (fallback silencieux) : après
  une mise à jour du moteur, comparer les clés avec `translate_cn.json`.
- Le vocabulaire suit le glossaire OFFICIEL FFG/Asmodee (Méchant, Contre/CTR,
  Manigance/MNG, Renfort=Surge, Déferlement=Overkill, Perçant, Tenace, Sonné,
  Désorienté, incliner/redresser, pile de victoire, deck Rencontre...). Ne pas
  improviser de traduction : vérifier sur fr.marvelcdb ou dans les PDF officiels.
- Le client (plateau, wizard, deck-builder) est traduit dans le code, mais ses
  détections sur la narration (regex de `ui-app/src/board/moteur.ts`, filtres de
  l'historique) sont BILINGUES exprès : ne jamais retirer la branche anglaise,
  elle sert quand `translate_file` est vide.
- Ne JAMAIS traduire : `world.phase`, `option.name`, les codes de stats
  ATK/THW/SCH/REC/DEF passés au catalogue, les noms de zones internes. La
  traduction de ces valeurs se fait uniquement à l'affichage
  (`phaseAffichee()` dans `Board.tsx`, triplets de `STATS_BASE`).

### 11.1 Texte français des cartes FAN-MADE (obligatoire à chaque pack)

Tout ce qui précède traduit **l'interface**. Le **texte des cartes**, lui, est
une autre affaire, et c'est l'étape qu'on oublie : un pack livré sans elle
laisse ses cartes **sans aucun tooltip français**, sans que rien ne le signale.
Constaté sur le pack `brawn` (7/8/2026), livré complet et validé, mais muet en
français.

Le plateau cherche le français d'une carte dans cet ordre
(`ApercuMarvelcdb` dans `ui-app/src/board/Board.tsx`) :

| Source | Fichier | Nature |
|---|---|---|
| 1. scan français | `assets/pics-fr/` | image, rien à écrire |
| 2. texte officiel | `ui-app/src/board/textes-fr.ts` | **GÉNÉRÉ** depuis marvelcdb — ne jamais l'éditer à la main |
| 3. texte fan-made | `ui-app/src/board/textes-fr-fanmade.ts` | **ÉCRIT À LA MAIN** — c'est ici qu'on travaille |
| 4. marvelcdb en ligne | — | option coupée par défaut, et sans effet sur du fan-made |

Une carte fan-made n'a ni scan français, ni page marvelcdb : **la ligne 3 est le
seul français que le joueur verra dessus.** Sans entrée, le tooltip reste vide.

Ajouter une entrée par `card_id` dans `TEXTES_FR_FANMADE`, **y compris pour les
exemplaires en double** (chaque `card_id` est une clé distincte ; recopier le
même texte). Conventions rappelées en tête du fichier :

- mots-clés de `mots-cles.ts` : Renfort, Déferlement, Robuste, Coup Rapide ;
- statistiques **ATQ, CTR, DEF, REC, MNG** ;
- aspects Agressivité, Justice, Leadership, Protection ;
- **noms propres et traits `[[...]]` laissés en ANGLAIS** : le joueur a la carte
  anglaise sous les yeux et doit s'y retrouver ;
- jetons recopiés tels quels : `[mental]`, `[physical]`, `[star]`, `[per_hero]`.

⚠ **Deux pièges** :
- le catalogue du jeu tient en **DEUX fichiers**, `data/cards.json` ET
  `data/cards_custom.json` — ne lire que le premier laisse Rescue, Hulk (Rainy)
  et Stan Lee muettes ;
- classer les packs « par tranche 61 à 75 » est **faux** : il y en a en 76xxx,
  77xxx, 78xxx et 90xxx.

Et comme pour tout ce qui touche `ui-app/src`, **rien n'apparaît dans le jeu
tant que `ui-app/deployer.sh` n'a pas tourné**.

## 12. Cosmétique du plateau (vague 8)

- **Météo de Storm** : les Soutiens 36003/36004/36005 (Hurricane, Thunderstorm,
  Blizzard) en jeu affichent pluie/orage/neige via l'iframe
  `public/effects/weather/*.html` (`ui-app/src/board/CoucheMeteo.tsx`,
  mapping `METEO_PAR_CARTE` à étendre pour de nouvelles cartes météo).
  Bouton « Météo » du plateau, localStorage `marvel-board-meteo`.
- **Musique d'ambiance** : AUCUN fichier n'est livré. Déposer
  `assets/sounds/musique-<slug-du-mechant>.mp3` (ex. `musique-rhino.mp3`)
  ou `assets/sounds/musique-plateau.mp3` (thème générique) : le plateau les
  cherche via la route `.mp3` du serveur. Bouton « Musique », INACTIF par
  défaut (localStorage `marvel-board-musique`).
- **Écran de fin** : affiche héros contre méchant(s), nombre de rounds,
  confettis en victoire (coupés par le bouton Anim).

## 12 bis. Arts alternatifs (cosmétique)

Deux mécanismes jumeaux, purement visuels : la carte reste la même pour le
moteur, seule l'image change.

- **Ressources doubles** : `COLLECTIONS` dans `ui-app/src/board/variantes.ts`
  et `COLLECTIONS_RESSOURCES` dans `public/js/prepare/app.js`. Clé
  `mc_resource_art_v1`. 31 collections (promos FFG « Play-and-Share » des 15
  héros, rééditions d'extension, et 16 collections « DesignHacker »).
  L'aperçu au survol montre les **trois** cartes de la collection ; le triplet
  est déduit de l'aperçu, qui est toujours la carte du milieu (Genius).
- **Cartes de héros** : `ARTS_HEROS` dans les deux mêmes fichiers. Clé
  `mc_hero_art_v1`. Images `assets/pics/<card_id>_<code>.jpg`.

**Les deux tables doivent rester alignées** entre le plateau et le wizard,
sinon le sélecteur propose un art que le plateau n'affichera pas.

⚠️ **Règle d'acceptation d'un art** : les VALEURS IMPRIMÉES sur l'image
(statistiques, points de vie, taille de main, traits) doivent être identiques à
celles de notre carte. Un art qui affiche autre chose ment au joueur en pleine
partie. C'est à ce titre qu'ont été écartés le Wasp, Beta Ray Bill et le
Spider-Man « Bag-Man » de la planche M3T4LB0X.

## 13. Panneau ⚙, succès, galerie (vagues 9 à 12)

- Tous les réglages du plateau vivent dans le panneau ⚙ Options
  (`PanneauOptions` dans `board.tsx`) : Animations, Sons, Musique, Météo,
  Succès, Textes marvelcdb, Curseurs, Auto-ciblage, Cartes révélées. Toute
  NOUVELLE option doit y prendre une ligne + une clé localStorage
  `marvel-board-*`. Raccourcis : E = fin du tour, U = annuler.
- Curseurs multi : routes `/set_cursor` (POST) et `/get_cursors`
  (server_get.py, périmés en 5 s). Proxy textes FR : `/marvelcdb_card?<code>`
  (code AVEC suffixe de face, ex. `01001a`).
- Succès : `game/rule/achievement.py` notifie « Achievement: X » ; la bannière
  du plateau (`CoucheSucces.tsx`, mapping NOMS) et l'écran Stats du wizard les
  affichent. Un nouveau succès moteur = ajouter son nom FR dans les deux.
- Galerie : `public/galerie.html` + `public/js/galerie/app.js` (autonome,
  filtre types/extensions/fan-made, images via `cardImageUrl()` de
  `js/prepare/api.js`, rendu par lots de 60). Bouton 🃏 dans la préparation
  (`js/prepare/lien-galerie.js`).
- **Mode Découverte** : partie FIGÉE (Spider-Man / Rhino / seed 42) doublée d'un
  coach qui donne une mission à la fois. Contenu dans `ui-app/src/board/lecons.ts`
  (module pur, vérifié par `node outils/verifier-lecons.mjs`), affichage dans
  `CoucheCoach.tsx`, armé par la clé localStorage `marvel-board-tutoriel` que
  le wizard gère. Le coach s'affiche dès que cette clé existe et vaut autre
  chose que `fini`.
  ⚠️ **Cette clé est un état GLOBAL, que rien ne rattache à la partie qui l'a
  posée.** Le plateau ne peut pas savoir s'il est la bonne partie : c'est le
  wizard qui garantit l'exclusivité, via `public/js/prepare/tutoriel-etat.js`
  (module pur). `app.js` **désarme** à chaque chargement de la préparation, et
  `launcher.js` **réarme** seulement si le mode choisi est Découverte. Le coach
  survit donc à un F5 sur le plateau, mais jamais à un retour au wizard.
  Sans ce désarmement, un tutoriel abandonné en cours de route laissait la clé
  sur le nom d'une leçon et le coach revenait sur **toutes** les parties
  suivantes, y compris les puzzles, les reprises et le multi, qui n'arment
  pourtant jamais rien (bug corrigé le 4/8/2026).
  Garde-fou : `node outils/verifier-tutoriel-etat.mjs`.
  ⚠️ Après toute modification de `js/prepare/`, **bumper le `?v=`** du fichier
  touché (dans `prepare.html` pour `app.js`, dans `app.js` pour ses imports) :
  sinon le navigateur sert la version en cache et le correctif reste invisible.
  ⚠️ **Les leçons NOMMENT des cartes précises** (« joue Coup de pied volant »),
  ce qui n'est vrai que parce que le seed fige la main. Le garde-fou est
  `tools/test_seed_tutoriel.py`, à relancer après toute mise à jour du moteur :
  s'il tombe, relire les leçons AVANT de mettre à jour ses valeurs attendues.
  Ne jamais désigner une carte par sa POSITION dans la main, l'ordre varie.
  ⚠️ **Le mulligan est la première leçon**, et ce n'est pas cosmétique : il a
  lieu avant le premier tour, son écran s'ouvre TOUT SEUL
  (`optionDemarreAuto` dans `interaction.ts`), et un joueur qui y défausse
  Coup de pied volant rend la leçon `jouer-carte` impossible à valider (son
  repère est pris après le mulligan, la carte n'y est donc jamais). La leçon
  `mulligan` dit explicitement de tout garder. Elle se détecte sur
  `round_id >= 1` : le compteur vaut 0 pendant toute la mise en place et passe
  à 1 dans `start_round` (`game/world/world.py`), donc juste après le mulligan.
  Préférer ce signal au libellé de phase, qui est du texte d'affichage.
  ⚠️ **L'identifiant de la première leçon est écrit EN DUR des deux côtés** :
  `PREMIERE_LECON` dans `CoucheCoach.tsx` et le `setItem` de
  `public/js/prepare/launcher.js`. `public/js/` et `ui-app/` sont deux mondes
  séparés, aucun import n'est possible entre eux : changer l'ordre des leçons
  impose de toucher les deux.
- Wizard avancé : bloc « Avancé » de l'étape finale (seed, temps par décision,
  premier joueur = rotation des joueurs dans `launcher.js`, règles v16).

## 14. Marquer une carte fan-made (champ `custom`)

Les packs custom apportent parfois des cartes d'**aspect** (Leadership,
Protection, Agression, Justice, Basic). Contrairement aux cartes signature,
elles se mélangent aux officielles dans le pool du deck-builder : rien ne
permettait de les reconnaître.

Chaque carte d'un pack fan-made porte donc une clé de PREMIER NIVEAU dans
`cards.json`, à côté de `card_id` :

```json
{"card_id": "69028", "type": "Event", "name": "Advice", "custom": "Kajislav",
 "desc": {"Cost": "1", "RES": "B", "Class": "Leadership"}, ...}
```

- La valeur est le **nom de l'auteur**, jamais un booléen : c'est ce qui
  s'affiche en infobulle.
- Le moteur Python **ignore** les clés inconnues (`Paper.Load` ne lit que
  `card_id`, `pic_id`, `type`, `name`, `subtitle`, `desc`, `traits`,
  `set_name`, `text`). Aucun risque côté partie.
- Le client, lui, reçoit `cards.json` brut par `/get_cards_json`.
  `CardStatistics.createCardObjects` recopie le champ sur l'objet `Card`
  (une réimpression `full_link` hérite de sa carte source).
- Le deck-builder affiche alors une pastille **CUSTOM** sur la vignette et
  dans la liste du deck (`badgeCustom()` dans `public/js/deckbuilder/app.js`,
  style `.db-badge-custom` dans `public/deck-builder.html`).

À ne pas confondre avec le filtre **fan-made de la galerie**, qui reste basé
sur la clé de `sets_info.json` (`/custom/i`, voir §12 bis) : les deux
mécanismes coexistent, l'un range les cartes par extension, l'autre les
distingue carte par carte.

### 14.1 Règle de deck-building propre à un héros

Certaines identités changent les règles de construction. Le deck-builder les
applique dans `public/js/deckbuilder/app.js` :

- `reglesAspect(hero)` — nombre d'aspects autorisés (Spider-Woman en exige
  exactement 2, Adam Warlock les libère tous).
- `exemptDeLaLimiteAspect(hero, carte)` — cartes qui **ne comptent pas** dans
  ce décompte. C'est là que vit *Arachnophilia* (Cassandra Webb) : les alliés
  au trait `WEB-WARRIOR` ou avec « Spider » dans le titre sont autorisés quel
  que soit leur aspect.

Le moteur ne valide **jamais** un deck au chargement (voir §5.2) : ces règles
n'existent que dans le deck-builder, et un deck de départ livré à la main les
contourne. Le contrôle reste donc manuel.
