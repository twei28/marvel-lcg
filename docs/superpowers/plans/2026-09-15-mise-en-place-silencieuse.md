# Plan d'exécution : la mise en place se tait, la manigance prend son temps

> **Pour un agent d'exécution :** SOUS-SKILL REQUISE : utiliser
> `superpowers:subagent-driven-development` (recommandé) ou
> `superpowers:executing-plans` pour dérouler ce plan tâche par tâche. Les
> étapes sont en cases à cocher (`- [ ]`).

**But :** vider l'ouverture d'une partie de tout mouvement, et poser un vrai
temps d'arrêt sur la face A de la manigance principale, validé par le premier
joueur, avant qu'elle se retourne sur sa face B avec sa menace de départ.

**Architecture :** une question posée par le MOTEUR dans l'unique branche qui
retourne une face A (`World.AdvanceMainScheme`), derrière un drapeau de règle
par défaut à faux qui protège les sauvegardes et les rejeux existants ; côté
plateau, un voile tenu jusqu'à l'arrivée de cette question, puis un panneau qui
montre la carte en grand, et son retournement.

**Pile technique :** moteur Python 3.10 (`Fusion/marvel-lcg-src/src`), client
React + TypeScript + Vitest (`ui-app`), pilote de test maison sur
`DeviceManager.DoGetInput`.

**Spec :** `docs/superpowers/specs/2026-09-15-mise-en-place-silencieuse-design.md`

## Contraintes globales

- **Une seule copie vivante du moteur** : `Fusion/marvel-lcg-src/`. On édite là,
  il n'y a aucune recopie à faire (GUIDE-CREATION-CONTENU §1.1).
- **Interpréteur** : `~/marvel-work/python/bin/python3.10`. Jamais le python du
  système.
- **Jamais deux harnais en parallèle sur le même dossier de jeu.** Les tâches
  moteur de ce plan visent `.game-src-par7`, pour ne pas croiser une batterie
  qui tournerait sur `.game-src`.
- **Aucun texte en dur côté plateau** : tout passe par `t()` (`board/langue.ts`)
  et sa contrepartie anglaise (`board/dico-en.ts`). Une gate refuse le reste.
- **TypeScript strict, zéro `any`.**
- **Le nom technique de l'option est `Reveal_Main_Scheme`**, sans espace : le
  moteur remplace les espaces par des underscores dans les noms d'options
  publiés, et un nom à espaces ne s'apparie jamais côté client.
- **Le drapeau de règle s'appelle `confirm_main_scheme`**, par défaut à faux.

## Ce qui est déjà mesuré, et qu'il ne faut pas re-supposer

Trois faits établis par trace le 15/09/2026, sur `.game-src-par7` :

1. **À la mise en place**, `world.py:548` appelle `scheme.Advance(None, ...)`
   sur `01097a` (face A), phase `Scenario Setup`, et c'est la PREMIÈRE branche de
   `AdvanceMainScheme` (`prev_scheme.card.printed_faces[0] == prev_scheme`) qui
   retourne la carte en `01097b`.
2. **À un changement d'étape**, `AdvanceMainScheme(01116b)` prend la branche
   `elif`, révèle `01117a`, dont `OnAfterCardRevealedEnd` rappelle `Advance`, qui
   repasse par la PREMIÈRE branche et retourne `01117b`. **Un seul crochet sert
   les deux cas.**
3. ⚠ **Une question à une seule option n'atteint JAMAIS le client avec
   `forced=True`** (le défaut de `AskChooseOneText`) : `ChoiceAndSpellEffect`
   pose `need_choose = False` et résout toute seule. Mesuré : « notre question a
   atteint le client 0 fois ». **Avec `forced=False`, `DoGetInput` est bien
   appelé.** C'est le point qui fait ou défait ce chantier.

---

### Tâche 1 : le drapeau de règle, et le harnais qui le prouve

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/world/world_rule.py:33`
- Créer : `Fusion/marvel-lcg-src/tools/test_manigance_face_a.py`

**Interfaces :**
- Produit : `world.rule.confirm_main_scheme` (`VariableBool`), activé en passant
  la chaîne `"confirm_main_scheme"` dans les `rules` de la scène.
- Produit : le harnais `tools/test_manigance_face_a.py`, réutilisé par les
  tâches 2 à 4.

- [ ] **Étape 1 : écrire le cas rouge**

Créer `Fusion/marvel-lcg-src/tools/test_manigance_face_a.py` :

```python
"""La face A de la manigance principale s'arrete et attend le premier joueur.

Usage:
    ~/marvel-work/python/bin/python3.10 tools/test_manigance_face_a.py \
        .game-src-par7 45100 [nom_du_cas]

Chaque cas tourne dans SON propre processus : le moteur est un singleton
global, impossible a reinitialiser proprement entre deux parties. Meme
technique que tools/test_capacites.py, en beaucoup plus petit : on detourne
DeviceManager.DoGetInput pour repondre a la place du client, et on observe.
"""
import json
import os
import subprocess
import sys
import threading
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def monter_le_moteur(game_dir, port, regles, scenario="rhino", heros="spider_man"):
    """Demarre une partie et rend (jeu, monde, journal_des_questions).

    `journal_des_questions` se remplit au fil des appels du moteur au client :
    une entree par question, avec les noms d'options publies.
    """
    game_dir = os.path.abspath(game_dir)
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)

    cfg = json.load(open("launch.json"))
    cfg["server_addresses"] = [f"127.0.0.1:{port}"]
    cfg["check_for_new_version_on_startup"] = False
    json.dump(cfg, open("launch.json", "w"), indent=2)

    from engine.network.web_server import WebServer
    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True

    from engine.device.manager.base import DeviceManager

    journal = []

    def pilote(self, data, player_id=None, check=None):
        options = data.options if isinstance(data.options, list) else []
        noms = [o.get("name") for o in options if isinstance(o, dict)]
        journal.append(noms)
        if len(journal) > 400:
            os._exit(3)
        for o in options:
            if isinstance(o, dict) and not o.get("failure_reason"):
                legales = [str(x) for x in (o.get("all_legal_targets") or [])]
                mini = (o.get("target_num_range") or [0, 0])[0]
                return json.dumps({"id": str(o.get("id", 0)),
                                   "targets": legales[:mini],
                                   "resources": []})
        return None

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, *a, **k: None
    DeviceManager.DoWaitSync = lambda self, *a, **k: None

    from engine import Engine
    Engine.Initialize()
    from game.scene.loader import SceneLoader
    from game.deck.hero import HeroDescriptor  # noqa: F401  (chargement des modeles)

    with open(_chemin_json("Campaign", scenario)) as f:
        campagne = f.read()
    with open(_chemin_json("Hero", heros)) as f:
        hero = f.read()
    scene = SceneLoader.NewFromJson(campagne, None, [hero], 42, regles, {})

    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")

    def run():
        try:
            if jeu.GameSetup():
                jeu.GameLoop()
        except BaseException:
            import traceback
            traceback.print_exc()

    threading.Thread(target=run, daemon=True).start()
    time.sleep(20)
    return jeu, jeu.world, journal


def _chemin_json(genre, nom):
    from core.file import FileManager
    chemin = FileManager.FindJsonPath(genre, nom)
    assert chemin, f"{genre} {nom} introuvable"
    return chemin


def cas_drapeau_pose(game_dir, port):
    """Le drapeau existe, et la liste de regles l'allume."""
    _, monde, _ = monter_le_moteur(game_dir, port, ["confirm_main_scheme"])
    assert bool(monde.rule.confirm_main_scheme) is True, \
        "la regle confirm_main_scheme n'a pas ete posee"
    return "le drapeau confirm_main_scheme est pose"


CAS = {"drapeau_pose": cas_drapeau_pose}


def main():
    game_dir = sys.argv[1]
    port = int(sys.argv[2])
    voulu = sys.argv[3] if len(sys.argv) > 3 else None
    noms = [voulu] if voulu else list(CAS)
    for rang, nom in enumerate(noms):
        fils = subprocess.run(
            [sys.executable, os.path.abspath(__file__), game_dir,
             str(port + rang), nom, "--fils"],
            cwd=RACINE, capture_output=True, text=True, timeout=180)
        verdict = "VERT" if fils.returncode == 0 else "ROUGE"
        print(f"{verdict} : {nom}")
        if fils.returncode != 0:
            print(fils.stdout[-3000:])
            print(fils.stderr[-3000:])
            sys.exit(1)


if __name__ == "__main__":
    if "--fils" in sys.argv:
        nom = sys.argv[3]
        print(CAS[nom](sys.argv[1], int(sys.argv[2])))
        os._exit(0)
    main()
```

- [ ] **Étape 2 : lancer le cas, le voir ROUGE**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 tools/test_manigance_face_a.py .game-src-par7 45100 drapeau_pose
```

Attendu : ROUGE, avec `AttributeError: 'WorldRule' object has no attribute
'confirm_main_scheme'`.

- [ ] **Étape 3 : poser le drapeau**

Dans `src/game/world/world_rule.py`, après la ligne
`self.create_player_deck_first = VariableBool(self, False, "create_player_deck_first")` :

```python
        # Le temps d'arret sur la face A de la manigance principale (spec du
        # 15/09/2026). PAR DEFAUT A FAUX, et ce n'est pas une precaution de
        # confort : une question de plus pendant la mise en place DECALE la
        # liste des operations rejouees (engine/controller/module/replay.py,
        # controle CRC). Une sauvegarde ecrite avant ce changement ne porte pas
        # la regle, ne pose donc pas la question, et se rejoue a l'identique.
        # Seules les parties neuves lancees depuis l'ecran de preparation
        # l'allument (public/js/prepare/launcher.js, buildRules).
        self.confirm_main_scheme            = VariableBool(self, False, "confirm_main_scheme")
```

- [ ] **Étape 4 : relancer, le voir VERT**

```bash
~/marvel-work/python/bin/python3.10 tools/test_manigance_face_a.py .game-src-par7 45100 drapeau_pose
```

Attendu : `VERT : drapeau_pose`.

- [ ] **Étape 5 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add Fusion/marvel-lcg-src/src/game/world/world_rule.py \
        Fusion/marvel-lcg-src/tools/test_manigance_face_a.py
git commit -m "feat(manigance): le drapeau confirm_main_scheme, et son harnais"
```

---

### Tâche 2 : la question atteint vraiment le client

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/world/world.py:896` (`AdvanceMainScheme`)
- Modifier : `Fusion/marvel-lcg-src/tools/test_manigance_face_a.py`

**Interfaces :**
- Consomme : `world.rule.confirm_main_scheme` (tâche 1), le harnais (tâche 1).
- Produit : `World.CONFIRM_MAIN_SCHEME_OPTION = "Reveal_Main_Scheme"` et
  `World.ConfirmMainSchemeReveal(scheme)`.

- [ ] **Étape 1 : écrire le cas rouge**

Ajouter dans `tools/test_manigance_face_a.py`, avant `CAS = {...}` :

```python
def cas_question_posee(game_dir, port):
    """Le client est VRAIMENT interroge sur la face A.

    ⚠ Ce cas existe parce que le contraire a ete mesure le 15/09/2026 : une
    question a une seule option avec `forced=True` (le defaut de
    `AskChooseOneText`) est resolue par le moteur SANS jamais atteindre le
    client. Le cas ne regarde donc pas l'etat final, il regarde le JOURNAL DES
    QUESTIONS.
    """
    _, monde, journal = monter_le_moteur(game_dir, port, ["confirm_main_scheme"])
    posees = [noms for noms in journal if "Reveal_Main_Scheme" in noms]
    assert len(posees) == 1, \
        f"la question devait etre posee 1 fois, journal={journal[:20]}"
    return "la question Reveal_Main_Scheme a atteint le client"
```

Et l'inscrire : `CAS = {"drapeau_pose": ..., "question_posee": cas_question_posee}`.

- [ ] **Étape 2 : lancer le cas, le voir ROUGE**

```bash
~/marvel-work/python/bin/python3.10 tools/test_manigance_face_a.py .game-src-par7 45110 question_posee
```

Attendu : ROUGE, `la question devait etre posee 1 fois`, journal sans
`Reveal_Main_Scheme`.

- [ ] **Étape 3 : poser la question dans le moteur**

Dans `src/game/world/world.py`, classe `World`, juste avant
`def AdvanceMainScheme` :

```python
    # Le nom TECHNIQUE de l'option de confirmation de la face A. Il ne
    # s'affiche jamais tel quel : le plateau le reconnait et pose son propre
    # libelle traduit. Sans espace, parce que le moteur remplace les espaces
    # par des underscores dans les noms d'options publies.
    CONFIRM_MAIN_SCHEME_OPTION = "Reveal_Main_Scheme"

    def ConfirmMainSchemeReveal(self, scheme: 'MainScheme') -> None:
        """Le premier joueur retourne la manigance, comme sur une vraie table.

        ⚠ `forced=False`, ET C'EST TOUT LE SUJET. Mesure du 15/09/2026 : avec
        `forced=True` (le defaut de `AskChooseOneText`), une question a une
        seule option ne quitte JAMAIS le moteur —
        `PlayerAction.ChoiceAndSpellEffect` pose `need_choose = False` et
        choisit a la place du joueur. Le client n'a rien vu passer : 0 appel a
        `DoGetInput`. Avec `forced=False`, il est bien interroge.

        ⚠ Le premier joueur SEUL (decision du 15/09/2026) : c'est lui qui tient
        le jeton et qui retourne la carte. Personne d'autre n'est retenu.
        """
        from game.ability.factory import AbilityFactory
        from game.effect.rule import GameRule

        if not self.rule.confirm_main_scheme:
            return
        if self.is_game_over:
            return
        player = self.GetFirstPlayer()
        if player is None or player.is_eliminated:
            return

        ability = AbilityFactory.ForChoiceAbility(
            World.CONFIRM_MAIN_SCHEME_OPTION,
            lambda targets: None,
        )
        player.ChooseAbilities(GameRule(scheme), ability, forced=False)
```

Puis, dans `AdvanceMainScheme`, la première branche devient :

```python
        if prev_scheme.card.printed_faces[0] == prev_scheme:
            card = prev_scheme.card
            # Le temps d'arret sur la face A. Cette branche est la SEULE qui
            # retourne une face A, mise en place et changements d'etape
            # confondus : trace du 15/09/2026, 01097a a la mise en place et
            # 01117a a l'etape 2 y passent tous les deux.
            self.ConfirmMainSchemeReveal(prev_scheme)
            card.Flip(GameRule(card.face))
```

- [ ] **Étape 4 : relancer, le voir VERT**

```bash
~/marvel-work/python/bin/python3.10 tools/test_manigance_face_a.py .game-src-par7 45110 question_posee
```

Attendu : `VERT : question_posee`.

- [ ] **Étape 5 : commit**

```bash
git add Fusion/marvel-lcg-src/src/game/world/world.py \
        Fusion/marvel-lcg-src/tools/test_manigance_face_a.py
git commit -m "feat(manigance): le moteur s'arrete sur la face A et interroge le premier joueur"
```

---

### Tâche 3 : sans le drapeau, rien ne change

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/tools/test_manigance_face_a.py`

**Interfaces :**
- Consomme : `World.ConfirmMainSchemeReveal` (tâche 2).
- Produit : la garde qui protège les sauvegardes et les rejeux.

- [ ] **Étape 1 : écrire le cas**

```python
def cas_sans_drapeau_aucune_question(game_dir, port):
    """Une partie SANS la regle ne pose pas la question.

    C'est la garde qui protege les sauvegardes et les campagnes en cours : une
    scene ecrite avant ce changement ne porte pas `confirm_main_scheme`, sa
    liste d'operations rejouees ne doit donc pas bouger d'un cran.
    """
    _, monde, journal = monter_le_moteur(game_dir, port, [])
    assert bool(monde.rule.confirm_main_scheme) is False
    posees = [noms for noms in journal if "Reveal_Main_Scheme" in noms]
    assert posees == [], f"question posee sans la regle : {posees}"
    from game.operate.worlds import Worlds
    schemes = Worlds.GetAllMainSchemes(monde)
    assert schemes and schemes[0].paper.card_id == "01097b", \
        f"la manigance devait etre retournee toute seule : {schemes}"
    return "sans la regle : aucune question, et la manigance est retournee"
```

L'inscrire dans `CAS` sous la clé `sans_drapeau`.

- [ ] **Étape 2 : lancer, le voir VERT du premier coup**

```bash
~/marvel-work/python/bin/python3.10 tools/test_manigance_face_a.py .game-src-par7 45120 sans_drapeau
```

Attendu : `VERT : sans_drapeau`. Ce cas naît vert : c'est un cas de NON-
RÉGRESSION, sa valeur est de rougir le jour où quelqu'un allumera la question
par défaut.

- [ ] **Étape 3 : commit**

```bash
git add Fusion/marvel-lcg-src/tools/test_manigance_face_a.py
git commit -m "test(manigance): sans la regle, aucune question et aucun rejeu decale"
```

---

### Tâche 4 : le même arrêt à chaque nouvelle étape

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/tools/test_manigance_face_a.py`

**Interfaces :**
- Consomme : `World.ConfirmMainSchemeReveal` (tâche 2).

- [ ] **Étape 1 : écrire le cas**

```python
def cas_etape_suivante(game_dir, port):
    """Une etape completee pose la meme question sur sa face A.

    Scenario Klaw : l'etape 1 est 01116a/b, l'etape 2 est 01117a/b. On force le
    passage plutot que de jouer la partie jusqu'au bout : c'est le meme appel
    (`MainScheme.Advance`) que celui d'une etape reellement completee.
    """
    _, monde, journal = monter_le_moteur(
        game_dir, port, ["confirm_main_scheme"], scenario="klaw")
    from game.operate.worlds import Worlds
    from game.effect.rule import GameRule

    avant = len([noms for noms in journal if "Reveal_Main_Scheme" in noms])
    assert avant == 1, f"mise en place : {avant} question(s)"

    courante = Worlds.GetAllMainSchemes(monde)[0]
    assert courante.paper.card_id == "01116b", courante.paper.card_id
    courante.Advance(None, GameRule(courante))
    time.sleep(3)

    apres = len([noms for noms in journal if "Reveal_Main_Scheme" in noms])
    assert apres == 2, f"changement d'etape : {apres} question(s) au total"
    suivante = Worlds.GetAllMainSchemes(monde)[0]
    assert suivante.paper.card_id == "01117b", suivante.paper.card_id
    return "l'etape 2 pose la question elle aussi, et se retourne ensuite"
```

L'inscrire dans `CAS` sous la clé `etape_suivante`.

- [ ] **Étape 2 : lancer, le voir VERT**

```bash
~/marvel-work/python/bin/python3.10 tools/test_manigance_face_a.py .game-src-par7 45130 etape_suivante
```

Attendu : `VERT : etape_suivante`.

- [ ] **Étape 3 : lancer la série complète**

```bash
~/marvel-work/python/bin/python3.10 tools/test_manigance_face_a.py .game-src-par7 45140
```

Attendu : quatre lignes VERT.

- [ ] **Étape 4 : commit**

```bash
git add Fusion/marvel-lcg-src/tools/test_manigance_face_a.py
git commit -m "test(manigance): l'etape suivante s'arrete sur sa face A elle aussi"
```

---

### Tâche 5 : le monde publie la règle, et les parties neuves la posent

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/render/descriptor/world.py:22` (zone des champs)
- Modifier : `Fusion/marvel-lcg-src/src/game/render/to_descriptor.py:74` (zone du remplissage)
- Modifier : `Fusion/marvel-lcg-src/public/js/prepare/launcher.js:24` (`buildRules`)
- Modifier : `ui-app/src/board/world.ts:347` (zone des champs du monde)

**Interfaces :**
- Produit : `world.confirm_main_scheme: boolean` dans la trame lue par le
  plateau (`World` de `ui-app/src/board/world.ts`).

**Pourquoi le plateau a besoin de le savoir :** la tâche 7 tient un voile
jusqu'à l'arrivée de la question. Sans ce champ, une partie où la règle n'est
PAS posée (une sauvegarde ancienne, un puzzle) resterait voilée pour toujours,
puisque la question n'arriverait jamais. On ne met pas de minuterie de secours :
on demande au monde s'il y a une question à attendre.

- [ ] **Étape 1 : écrire le cas rouge côté moteur**

Ajouter dans `tools/test_manigance_face_a.py` :

```python
def cas_regle_publiee(game_dir, port):
    """La trame dit si la question est attendue, pour que le plateau le sache."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["confirm_main_scheme"])
    from game.render.to_descriptor import ToDescriptor
    descripteur = ToDescriptor.World(monde)
    assert getattr(descripteur, "confirm_main_scheme", None) is True, \
        "la trame ne publie pas confirm_main_scheme"
    return "la trame publie confirm_main_scheme"
```

⚠ Vérifier le nom réel de l'entrée (`ToDescriptor.World` ou l'appelant utilisé
dans `to_descriptor.py:74`) en lisant le fichier, et ajuster l'appel : ce cas
doit mesurer le descripteur réellement envoyé, pas un objet reconstruit à côté.

L'inscrire dans `CAS` sous la clé `regle_publiee`.

- [ ] **Étape 2 : lancer, le voir ROUGE**

```bash
~/marvel-work/python/bin/python3.10 tools/test_manigance_face_a.py .game-src-par7 45150 regle_publiee
```

Attendu : ROUGE, `la trame ne publie pas confirm_main_scheme`.

- [ ] **Étape 3 : publier le champ**

Dans `src/game/render/descriptor/world.py`, ajouter au dataclass :

```python
    # Le plateau tient son voile d'ouverture jusqu'a la question de la face A.
    # Il doit donc savoir s'il y a une question a attendre : une sauvegarde
    # ancienne ou un puzzle ne porte pas la regle, et n'en posera jamais.
    confirm_main_scheme: bool = False
```

Dans `src/game/render/to_descriptor.py`, à côté de
`world_descriptor.main_schemes_deck = ...` :

```python
        world_descriptor.confirm_main_scheme = bool(world.rule.confirm_main_scheme)
```

- [ ] **Étape 4 : relancer, le voir VERT**

```bash
~/marvel-work/python/bin/python3.10 tools/test_manigance_face_a.py .game-src-par7 45150 regle_publiee
```

Attendu : `VERT : regle_publiee`.

- [ ] **Étape 5 : déclarer le champ côté plateau**

Dans `ui-app/src/board/world.ts`, à côté de `area_schemes_main`, ajouter au type
`World` :

```ts
  /**
   * Le moteur s'arrête-t-il sur la face A de la manigance ? Posé par les
   * parties neuves seulement : une sauvegarde antérieure au 15/09/2026 ne
   * porte pas la règle, et le voile d'ouverture ne doit pas l'attendre.
   */
  confirm_main_scheme?: boolean
```

- [ ] **Étape 6 : poser la règle sur les parties neuves**

Dans `Fusion/marvel-lcg-src/public/js/prepare/launcher.js`, dans `buildRules`,
avant le `return rules` :

```js
    // Le temps d'arrêt sur la face A de la manigance principale (spec du
    // 15/09/2026). Posé par les parties NEUVES uniquement : une sauvegarde
    // rechargée garde les règles inscrites dans sa scène, donc ne pose pas la
    // question et rejoue ses opérations sans décalage.
    rules.push("confirm_main_scheme");
```

- [ ] **Étape 7 : vérifier le typage du plateau**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app" && npm run typecheck
```

Attendu : aucune erreur.

- [ ] **Étape 8 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add Fusion/marvel-lcg-src/src/game/render/descriptor/world.py \
        Fusion/marvel-lcg-src/src/game/render/to_descriptor.py \
        Fusion/marvel-lcg-src/public/js/prepare/launcher.js \
        Fusion/marvel-lcg-src/tools/test_manigance_face_a.py \
        ui-app/src/board/world.ts
git commit -m "feat(manigance): la trame dit si la question est attendue, les parties neuves la posent"
```

---

### Tâche 6 : le plateau reconnaît la question

**Fichiers :**
- Créer : `ui-app/src/board/manigance-face-a.ts`
- Créer : `ui-app/src/board/manigance-face-a.test.ts`

**Interfaces :**
- Consomme : `Demande` et `Option` (`ui-app/src/board/ask.ts:52`), `World`
  (`ui-app/src/board/world.ts`).
- Produit :
  - `NOM_OPTION_MANIGANCE = 'Reveal_Main_Scheme'`
  - `questionDeLaManigance(demande: Demande | undefined): Option | undefined`
  - `maniganceAMontrer(monde: World | undefined): WorldCard | undefined`

- [ ] **Étape 1 : écrire les cas rouges**

Créer `ui-app/src/board/manigance-face-a.test.ts` :

```ts
import { describe, expect, it } from 'vitest'
import {
  NOM_OPTION_MANIGANCE,
  maniganceAMontrer,
  questionDeLaManigance,
} from './manigance-face-a'
import type { Demande, Option } from './ask'
import type { World } from './world'

function option(nom: string): Option {
  return {
    id: 7,
    name: nom,
    bind_id: 0,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
}

function demande(options: Option[]): Demande {
  return {
    options,
    refus: [],
    prompt_text: '',
    event_name: '',
    show_cancel: false,
    ability_type: '',
  }
}

describe('questionDeLaManigance', () => {
  it('reconnaît la question du moteur à son nom technique', () => {
    const trouvee = questionDeLaManigance(demande([option(NOM_OPTION_MANIGANCE)]))
    expect(trouvee?.id).toBe(7)
  })

  it('ne se déclenche pas sur une autre question', () => {
    expect(questionDeLaManigance(demande([option('Attack')]))).toBeUndefined()
  })

  it('ne se déclenche pas quand le moteur ne demande rien', () => {
    expect(questionDeLaManigance(undefined)).toBeUndefined()
  })

  it("refuse une question qui porte AUSSI d'autres options", () => {
    // Une option de plus veut dire que ce n'est pas notre moment : on ne
    // détourne pas une question à laquelle le joueur doit vraiment répondre.
    const melange = demande([option(NOM_OPTION_MANIGANCE), option('Attack')])
    expect(questionDeLaManigance(melange)).toBeUndefined()
  })
})

describe('maniganceAMontrer', () => {
  it('rend la manigance principale en jeu', () => {
    const monde = {
      area_schemes_main: [{ id: 48, card_id: '01097a', name: 'The Break-In!' }],
    } as unknown as World
    expect(maniganceAMontrer(monde)?.card_id).toBe('01097a')
  })

  it('rend undefined quand la zone est vide', () => {
    const monde = { area_schemes_main: [] } as unknown as World
    expect(maniganceAMontrer(monde)).toBeUndefined()
  })

  it('rend undefined sans monde', () => {
    expect(maniganceAMontrer(undefined)).toBeUndefined()
  })
})
```

- [ ] **Étape 2 : lancer, les voir ROUGES**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/manigance-face-a.test.ts
```

Attendu : ÉCHEC, `Failed to resolve import "./manigance-face-a"`.

- [ ] **Étape 3 : écrire le module**

Créer `ui-app/src/board/manigance-face-a.ts` :

```ts
// LE TEMPS D'ARRÊT SUR LA FACE A DE LA MANIGANCE PRINCIPALE.
//
// Le moteur pose une vraie question avant de retourner une face A
// (`World.ConfirmMainSchemeReveal`, world.py). Elle voyage comme n'importe
// quelle question, avec UNE option nommée `Reveal_Main_Scheme`.
//
// ⚠ CE MODULE EST PUR. Aucune lecture du DOM, aucun rendu : de quoi vérifier
// la règle de reconnaissance sans navigateur.

import type { Demande, Option } from './ask'
import type { World, WorldCard } from './world'

/**
 * Le nom TECHNIQUE de l'option, tel que le moteur le publie. Il ne s'affiche
 * jamais : le panneau pose son propre libellé traduit.
 *
 * ⚠ SANS ESPACE. Le moteur remplace les espaces par des underscores dans les
 * noms d'options publiés : un nom à espaces ne s'apparierait jamais.
 */
export const NOM_OPTION_MANIGANCE = 'Reveal_Main_Scheme'

/**
 * La question de la manigance, ou `undefined` si ce n'est pas ce moment-là.
 *
 * ⚠ EXIGE QU'ELLE SOIT SEULE. Si le moteur propose autre chose en même temps,
 * le joueur a un vrai choix à faire et le panneau n'a pas à s'en emparer.
 */
export function questionDeLaManigance(demande: Demande | undefined): Option | undefined {
  if (!demande) return undefined
  if (demande.options.length !== 1) return undefined
  const seule = demande.options[0]
  return seule && seule.name === NOM_OPTION_MANIGANCE ? seule : undefined
}

/**
 * La manigance à montrer en grand : celle qui est EN JEU à cet instant.
 *
 * Au moment de la question, le moteur n'a pas encore retourné la carte : la
 * zone porte donc la face A. On ne déduit pas son identifiant, on lit la table.
 */
export function maniganceAMontrer(monde: World | undefined): WorldCard | undefined {
  const zone = monde?.area_schemes_main
  if (!Array.isArray(zone)) return undefined
  return zone[0]
}
```

- [ ] **Étape 4 : relancer, les voir VERTS**

```bash
npx vitest run src/board/manigance-face-a.test.ts
```

Attendu : 7 cas verts.

- [ ] **Étape 5 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/manigance-face-a.ts ui-app/src/board/manigance-face-a.test.ts
git commit -m "feat(manigance): le plateau reconnait la question de la face A"
```

---

### Tâche 7 : le voile tenu, pour que la table n'apparaisse jamais en train de se monter

**Fichiers :**
- Modifier : `ui-app/src/board/manigance-face-a.ts`
- Modifier : `ui-app/src/board/manigance-face-a.test.ts`
- Modifier : `ui-app/src/board.tsx:2730` (la garde qui affiche « Connexion à la partie… »)

**Interfaces :**
- Consomme : `questionDeLaManigance` (tâche 6), `world.confirm_main_scheme`
  (tâche 5), `world.round_id`.
- Produit : `ouvertureEncoreVoilee(etat: EtatOuverture): boolean` avec
  `type EtatOuverture = { confirmAttendue: boolean; round: number; questionArrivee: boolean; dejaLevee: boolean }`.

- [ ] **Étape 1 : écrire les cas rouges**

Ajouter à `ui-app/src/board/manigance-face-a.test.ts` :

```ts
import { ouvertureEncoreVoilee } from './manigance-face-a'

describe('ouvertureEncoreVoilee', () => {
  const base = { confirmAttendue: true, round: 0, questionArrivee: false, dejaLevee: false }

  it('voile la table pendant que le moteur monte la partie', () => {
    expect(ouvertureEncoreVoilee(base)).toBe(true)
  })

  it('lève le voile quand la question arrive', () => {
    expect(ouvertureEncoreVoilee({ ...base, questionArrivee: true })).toBe(false)
  })

  it('ne revoile jamais une fois levé', () => {
    expect(ouvertureEncoreVoilee({ ...base, dejaLevee: true })).toBe(false)
  })

  it("ne voile pas une partie qui n'attend aucune question", () => {
    // Sauvegarde antérieure au 15/09/2026, ou puzzle : la règle n'est pas
    // posée, la question ne viendra jamais. Sans cette porte, le plateau
    // resterait voilé pour toujours.
    expect(ouvertureEncoreVoilee({ ...base, confirmAttendue: false })).toBe(false)
  })

  it('ne voile pas une partie déjà commencée', () => {
    expect(ouvertureEncoreVoilee({ ...base, round: 3 })).toBe(false)
  })
})
```

- [ ] **Étape 2 : lancer, les voir ROUGES**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/manigance-face-a.test.ts
```

Attendu : ÉCHEC, `ouvertureEncoreVoilee is not a function`.

- [ ] **Étape 3 : écrire la règle**

Ajouter à `ui-app/src/board/manigance-face-a.ts` :

```ts
/** Ce qu'il faut savoir pour décider si l'ouverture reste voilée. */
export type EtatOuverture = {
  /** Le monde dit qu'une question de face A est attendue (`confirm_main_scheme`). */
  confirmAttendue: boolean
  /** `round_id` : 0 pendant la mise en place, 1 au premier round. */
  round: number
  /** La question de la manigance est à l'écran. */
  questionArrivee: boolean
  /** Le voile a déjà été levé une fois dans cette partie. */
  dejaLevee: boolean
}

/**
 * Le voile d'ouverture : la table n'apparaît qu'une fois montée.
 *
 * ⚠ AUCUNE MINUTERIE DE SECOURS, et c'est voulu. Le repli « au bout de N
 * secondes on affiche quand même » masquerait un vrai défaut le jour où la
 * question ne vient pas. La porte est explicite : on ne voile QUE si le monde
 * dit qu'une question est attendue.
 */
export function ouvertureEncoreVoilee(etat: EtatOuverture): boolean {
  if (etat.dejaLevee) return false
  if (!etat.confirmAttendue) return false
  if (etat.round > 0) return false
  return !etat.questionArrivee
}
```

- [ ] **Étape 4 : relancer, les voir VERTS**

```bash
npx vitest run src/board/manigance-face-a.test.ts
```

Attendu : 12 cas verts.

- [ ] **Étape 5 : brancher le voile sur le plateau**

Dans `ui-app/src/board.tsx`, au composant qui porte la garde de la ligne 2730,
ajouter avant le `if (!etat.monde || !plateau)` :

```tsx
  // Le voile d'ouverture : on ne montre pas la table en train de se monter.
  // Levé une fois pour toutes dès que la question de la manigance arrive.
  const voileLeve = useRef(false)
  const questionManigance = questionDeLaManigance(etat.demande)
  const voile = ouvertureEncoreVoilee({
    confirmAttendue: etat.monde?.confirm_main_scheme === true,
    round: etat.monde?.round_id ?? 0,
    questionArrivee: questionManigance !== undefined,
    dejaLevee: voileLeve.current,
  })
  if (!voile) voileLeve.current = true
```

puis étendre la garde :

```tsx
  if (!etat.monde || !plateau || voile) {
    return (
      <p className="plateau-message" role={etat.erreur ? 'alert' : undefined}>
        {etat.erreur ?? t('Connexion à la partie…')}
      </p>
    )
  }
```

⚠ Importer `questionDeLaManigance` et `ouvertureEncoreVoilee` depuis
`./board/manigance-face-a`, et `useRef` s'il n'est pas déjà importé.

- [ ] **Étape 6 : vérifier le typage et toute la batterie du plateau**

```bash
npm run typecheck && npx vitest run
```

Attendu : aucune erreur de typage, aucun cas rouge.

- [ ] **Étape 7 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/manigance-face-a.ts ui-app/src/board/manigance-face-a.test.ts ui-app/src/board.tsx
git commit -m "feat(manigance): la table n'apparait plus en train de se monter"
```

---

### Tâche 8 : le panneau de la face A

**Fichiers :**
- Créer : `ui-app/src/board/PanneauManigance.tsx`
- Créer : `ui-app/src/board/PanneauManigance.test.tsx`
- Modifier : `ui-app/src/board/board.css` (à la suite du bloc `.vol-carte`)
- Modifier : `ui-app/src/board.tsx` (montage du panneau)
- Modifier : `ui-app/src/board/langue.ts` et `ui-app/src/board/dico-en.ts`

**Interfaces :**
- Consomme : `questionDeLaManigance`, `maniganceAMontrer` (tâche 6),
  `scanUrl` (`ui-app/src/board/card-model.ts`), `nomAffiche`
  (`ui-app/src/board/noms-cartes-fr.ts`), `repondre` (la fonction du plateau qui
  poste une `Reponse`).
- Produit : `<PanneauManigance carte={WorldCard} onValider={() => void} />`.

- [ ] **Étape 1 : écrire les cas rouges**

Créer `ui-app/src/board/PanneauManigance.test.tsx` :

```tsx
import { describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { PanneauManigance } from './PanneauManigance'
import type { WorldCard } from './world'

const carte = { id: 48, card_id: '01097a', name: 'The Break-In!' } as unknown as WorldCard

describe('PanneauManigance', () => {
  it('montre la carte en grand', () => {
    render(<PanneauManigance carte={carte} onValider={() => {}} />)
    const image = screen.getByRole('img')
    expect(image.getAttribute('src')).toContain('01097a')
  })

  it('valide au clic sur le bouton', async () => {
    const onValider = vi.fn()
    render(<PanneauManigance carte={carte} onValider={onValider} />)
    await userEvent.click(screen.getByRole('button'))
    expect(onValider).toHaveBeenCalledTimes(1)
  })

  it('ne valide pas deux fois, même sur double clic', async () => {
    // Le moteur n'attend qu'une réponse : une seconde poste dans le vide et
    // peut répondre à la question SUIVANTE.
    const onValider = vi.fn()
    render(<PanneauManigance carte={carte} onValider={onValider} />)
    const bouton = screen.getByRole('button')
    await userEvent.dblClick(bouton)
    expect(onValider).toHaveBeenCalledTimes(1)
  })
})
```

⚠ Vérifier comment les autres cas `.test.tsx` du dossier montent un composant
(`DemandeCentrale.test.tsx` est le plus proche) et suivre exactement leur façon
de faire : c'est ce montage-là qui est déjà configuré dans ce projet.

- [ ] **Étape 2 : lancer, les voir ROUGES**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/PanneauManigance.test.tsx
```

Attendu : ÉCHEC, module introuvable.

- [ ] **Étape 3 : écrire le composant**

Créer `ui-app/src/board/PanneauManigance.tsx` :

```tsx
// LA FACE A DE LA MANIGANCE, EN GRAND, AVANT QU'ELLE SE RETOURNE.
//
// Demande de l'utilisateur, 15/09/2026 : « on doit voir la face A de la
// première manigance, puis on fait ok, puis elle se place sur la face B ».
// Le moteur ATTEND vraiment cette réponse (World.ConfirmMainSchemeReveal).

import { useState } from 'react'
import { scanUrl } from './card-model'
import { t } from './langue'
import { nomAffiche } from './noms-cartes-fr'
import type { WorldCard } from './world'

export function PanneauManigance({
  carte,
  onValider,
}: {
  carte: WorldCard
  onValider: () => void
}) {
  // ⚠ UN SEUL ENVOI. Le moteur n'attend qu'une réponse ; une seconde partirait
  // dans le vide, ou pire, répondrait à la question suivante.
  const [envoye, setEnvoye] = useState(false)

  return (
    <div className="panneau-manigance" role="dialog" aria-modal="true">
      <img className="panneau-manigance-carte" src={scanUrl(carte)} alt={nomAffiche(carte)} />
      <button
        type="button"
        className="panneau-manigance-ok"
        disabled={envoye}
        onClick={() => {
          if (envoye) return
          setEnvoye(true)
          onValider()
        }}
      >
        {t('Retourner la manigance')}
      </button>
    </div>
  )
}
```

⚠ Vérifier la signature réelle de `scanUrl` et de `nomAffiche` dans
`card-model.ts` et `noms-cartes-fr.ts` avant d'écrire, et adapter l'appel : ces
deux fonctions sont déjà utilisées par `CoucheRevelation.tsx`, qui sert de
modèle.

- [ ] **Étape 4 : ajouter les deux clés de langue**

Dans `ui-app/src/board/dico-en.ts`, à côté de `'Mise en place': 'Setup'` :

```ts
  'Retourner la manigance': 'Flip the main scheme',
```

- [ ] **Étape 5 : habiller le panneau**

Dans `ui-app/src/board/board.css`, à la suite du bloc `.vol-carte` :

```css
  /* La face A de la manigance, montrée en grand avant son retournement.
     Le plateau reste visible derrière, assombri : on doit voir que la table
     est montée, c'est tout l'intérêt de l'avoir attendue. */
  .panneau-manigance {
    position: fixed;
    inset: 0;
    z-index: 700;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
    background: rgba(8, 9, 12, 0.72);
  }

  .panneau-manigance-carte {
    max-width: min(86vw, 620px);
    max-height: 62vh;
    border-radius: 12px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7);
  }

  .panneau-manigance-ok {
    min-height: 48px;
    padding: 0 28px;
    font-size: 1rem;
  }
```

- [ ] **Étape 6 : relancer les cas, les voir VERTS**

```bash
npx vitest run src/board/PanneauManigance.test.tsx
```

Attendu : 3 cas verts.

- [ ] **Étape 7 : monter le panneau sur le plateau**

Dans `ui-app/src/board.tsx`, après la garde du voile (tâche 7), là où les autres
couches sont rendues :

```tsx
        {questionManigance && maniganceAMontrer(etat.monde) ? (
          <PanneauManigance
            carte={maniganceAMontrer(etat.monde)!}
            onValider={() =>
              void repondre({ id: questionManigance.id, targets: [], resources: [] })
            }
          />
        ) : null}
```

⚠ Utiliser la fonction de réponse DÉJÀ en place dans ce composant (celle
qu'utilise le panneau central pour poster une `Reponse`), pas une nouvelle.

- [ ] **Étape 8 : la gate de langue et toute la batterie**

```bash
npm run typecheck && npx vitest run
```

Attendu : aucune erreur, aucun cas rouge. ⚠ Si la gate de langue rougit, c'est
qu'une clé manque dans `dico-en.ts` : l'ajouter, ne jamais contourner la gate.

- [ ] **Étape 9 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/PanneauManigance.tsx ui-app/src/board/PanneauManigance.test.tsx \
        ui-app/src/board/board.css ui-app/src/board/dico-en.ts ui-app/src/board.tsx
git commit -m "feat(manigance): la face A en grand, et le OK qui la retourne"
```

---

### Tâche 9 : le retournement, seul mouvement de l'ouverture

**Fichiers :**
- Modifier : `ui-app/src/board/PanneauManigance.tsx`
- Modifier : `ui-app/src/board/PanneauManigance.test.tsx`
- Modifier : `ui-app/src/board/board.css`

**Interfaces :**
- Consomme : `PanneauManigance` (tâche 8).
- Produit : la classe `est-retournee` posée sur le panneau après le clic, et le
  retrait du panneau à la fin de l'animation.

- [ ] **Étape 1 : écrire le cas rouge**

Ajouter à `PanneauManigance.test.tsx` :

```tsx
  it('se retourne au clic avant de disparaître', async () => {
    render(<PanneauManigance carte={carte} onValider={() => {}} />)
    const panneau = screen.getByRole('dialog')
    expect(panneau.className).not.toContain('est-retournee')
    await userEvent.click(screen.getByRole('button'))
    expect(panneau.className).toContain('est-retournee')
  })
```

- [ ] **Étape 2 : lancer, le voir ROUGE**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/PanneauManigance.test.tsx
```

Attendu : ÉCHEC sur `expect(panneau.className).toContain('est-retournee')`.

- [ ] **Étape 3 : poser le retournement**

Dans `PanneauManigance.tsx`, remplacer la `<div>` racine et le `onClick` :

```tsx
    <div
      className={`panneau-manigance${envoye ? ' est-retournee' : ''}`}
      role="dialog"
      aria-modal="true"
    >
```

Le `onClick` reste identique : c'est `envoye` qui porte les deux rôles, la garde
du double envoi et le déclenchement du retournement.

Et dans `board.css`, à la suite du bloc de la tâche 8 :

```css
  /* Le retournement : la carte pivote sur son axe vertical et s'efface.
     Même durée que le vol le plus long d'une carte (CoucheAnimations,
     DUREE_MAX = 400 ms) : l'ouverture n'a pas deux tempos. */
  .panneau-manigance.est-retournee .panneau-manigance-carte {
    transform: rotateY(90deg) scale(0.92);
    opacity: 0;
    transition:
      transform 400ms cubic-bezier(0.22, 0.75, 0.3, 1),
      opacity 400ms ease-in;
  }

  .panneau-manigance.est-retournee {
    background: rgba(8, 9, 12, 0);
    transition: background 400ms ease-in;
    pointer-events: none;
  }

  @media (prefers-reduced-motion: reduce) {
    .panneau-manigance.est-retournee .panneau-manigance-carte,
    .panneau-manigance.est-retournee {
      transition: none;
    }
  }
```

- [ ] **Étape 4 : relancer, le voir VERT**

```bash
npx vitest run src/board/PanneauManigance.test.tsx
```

Attendu : 4 cas verts.

- [ ] **Étape 5 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/PanneauManigance.tsx ui-app/src/board/PanneauManigance.test.tsx \
        ui-app/src/board/board.css
git commit -m "feat(manigance): le retournement, seul mouvement de l'ouverture"
```

---

### Tâche 10 : l'étape 8 bis, ce que le plateau DESSINE

**Fichiers :**
- Modifier : `ui-app/src/board/plateau-de-test.ts` (si une entrée est nécessaire)
- Créer : `ui-app/src/board/manigance-sur-le-plateau.test.ts`

**Interfaces :**
- Consomme : `plateau-de-test.ts` (poser un état de table, demander ce qui est
  dessiné).

**Pourquoi cette tâche existe :** `test_capacites.py` prouve ce que le moteur
FAIT, jamais ce que le plateau DESSINE. Un pack peut être livré vert 32 fois sur
32 et injouable à l'œil. C'est l'étape 8 bis de `PROCESSUS-CARTE.md`.

- [ ] **Étape 1 : lire le mode d'emploi du harnais**

```bash
sed -n 1,80p "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app/src/board/plateau-de-test.ts"
```

Relever la façon exacte de poser un état de table et d'interroger le rendu
(cinq lignes par carte, d'après l'en-tête du fichier).

- [ ] **Étape 2 : écrire le cas rouge**

Créer `ui-app/src/board/manigance-sur-le-plateau.test.ts`, sur le modèle relevé
à l'étape 1, qui pose une table où la manigance est en `01097a` avec la question
`Reveal_Main_Scheme` ouverte, et qui affirme deux choses :

1. la carte DESSINÉE en grand porte bien `01097a`, la face A, et pas `01097b` ;
2. aucune carte de la table n'est masquée derrière le voile à ce moment-là : le
   plateau est bien monté, c'est le panneau qui est par-dessus.

⚠ Écrire les assertions contre ce que le harnais rend réellement (la liste des
unités dessinées), pas contre le DOM d'un rendu React improvisé : c'est
exactement la confusion que l'étape 8 bis existe pour empêcher.

- [ ] **Étape 3 : lancer, le voir ROUGE, puis corriger jusqu'au VERT**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/manigance-sur-le-plateau.test.ts
```

Si le cas est vert du premier coup, c'est suspect : retirer temporairement le
montage du panneau (tâche 8, étape 7) et vérifier qu'il rougit. Le remettre.

- [ ] **Étape 4 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/manigance-sur-le-plateau.test.ts
git commit -m "test(manigance): l'etape 8 bis, c'est bien la face A qui est dessinee"
```

---

### Tâche 11 : le pilote d'autoplay et les specs `ui-check` répondent à la question

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/tools/autoplay.py`
- Modifier : les specs `ui-check` qui lancent une vraie partie (les repérer à
  l'étape 1)

**Interfaces :**
- Consomme : la question `Reveal_Main_Scheme` (tâche 2), la règle posée par
  `buildRules` (tâche 5).

- [ ] **Étape 1 : repérer qui joue de vraies parties**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
grep -rln "buildRules\|nouvelle partie\|new_game" ui-check/tests/ | sort
grep -n "def pilote\|options" Fusion/marvel-lcg-src/tools/autoplay.py | head -20
```

- [ ] **Étape 2 : lancer une spec `ui-check` telle quelle, la voir ROUGE**

Lancer une des specs repérées. Attendu : elle bloque sur le panneau de la
manigance, qui n'existait pas quand elle a été écrite. **C'est la preuve que le
moment existe** : ne pas la contourner, lui apprendre à cliquer.

- [ ] **Étape 3 : apprendre le OK aux deux pilotes**

Côté `autoplay.py` : le pilote choisit déjà la première option jouable ; vérifier
qu'il répond bien à une question à une seule option et, si ce n'est pas le cas,
la traiter explicitement par son nom `Reveal_Main_Scheme`.

Côté `ui-check` : cliquer le bouton du panneau (`.panneau-manigance-ok`) au
démarrage de chaque partie neuve, avant les assertions existantes.

- [ ] **Étape 4 : relancer, les voir VERTS**

- [ ] **Étape 5 : commit**

```bash
git add Fusion/marvel-lcg-src/tools/autoplay.py ui-check/tests/
git commit -m "test(manigance): le pilote et les specs repondent au panneau de la face A"
```

---

### Tâche 12 : la vérification en jeu, et la fiche

**Fichiers :**
- Modifier : `.twei/SESSION.md`
- Créer : `.planning/todos/2026-09-15-mise-en-place-silencieuse.md`

⚠ **Rien de ce plan n'est « fini » avant cette tâche.** Le moteur vert ne prouve
rien sur le rendu, et une partie lancée à la main est le seul juge de « trop de
bruit ».

- [ ] **Étape 1 : reconstruire le plateau, puis déployer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
bash ui-app/deployer.sh
```

Puis vérifier le hash du bundle servi. ⚠ `deployer.ps1` ne reconstruit PAS le
plateau : sans `deployer.sh` d'abord, la partie testée serait l'ancienne.

⚠ **Ne rien mettre en production sans le feu vert explicite de l'utilisateur.**

- [ ] **Étape 2 : jouer une ouverture, et la mesurer**

Lancer une partie neuve et vérifier, capture à l'appui :
1. la table n'apparaît jamais en train de se monter ;
2. la face A est montrée en grand, la main est vide, rien ne bouge ;
3. le OK retourne la carte, la menace de départ est là ;
4. le mulligan s'ouvre ensuite sur une table qui ne bouge plus ;
5. une sauvegarde ANTÉRIEURE se recharge sans panneau et sans erreur.

- [ ] **Étape 3 : écrire la fiche et la session**

Fiche `.planning/todos/2026-09-15-mise-en-place-silencieuse.md` : ce qui a été
fait, ce qui a été mesuré (les trois faits de trace), et ce qui reste. Entrée
en tête de `.twei/SESSION.md`.

- [ ] **Étape 4 : commit**

```bash
git add .twei/SESSION.md .planning/todos/2026-09-15-mise-en-place-silencieuse.md
git commit -m "docs(manigance): l'ouverture silencieuse, verifiee en jeu"
```

---

## Relecture du plan contre la spec

- **Ouverture silencieuse** : tâches 5 (le champ publié) et 7 (le voile).
- **Face A en grand, OK, retournement** : tâches 6, 8, 9.
- **Menace posée d'un coup** : aucune tâche, et c'est volontaire. Le moteur pose
  la menace en retournant la carte ; le compteur la porte donc dès que la table
  reparaît. Rien à écrire, et c'est vérifié à l'étape 2 de la tâche 12.
- **Le moteur attend vraiment** : tâche 2, avec le piège `forced` documenté.
- **Le premier joueur seul** : tâche 2 (`GetFirstPlayer`).
- **Ouverture ET chaque nouvelle étape** : tâche 4.
- **Main vide assumée** : aucune tâche, c'est l'ordre naturel du moteur. Vérifié
  à l'étape 2 de la tâche 12.
- **Drapeau et protection des rejeux** : tâches 1, 3, 5.
- **Étape 8 bis** : tâche 10.
- **Pilote et specs** : tâche 11.
- **Deux manigances simultanées** (`21098a`) : couvert sans code par la tâche 2,
  puisque la question est posée par manigance retournée. ⚠ Non testé : à ajouter
  au harnais si ce scénario est un jour porté.
- **Face A avec seuil imprimé** : couvert sans code, `OnAfterCardRevealedEnd`
  n'avance pas ces manigances-là, la branche n'est donc jamais atteinte.
