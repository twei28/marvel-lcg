# Plan d'exécution : le mode manuel, moitié moteur

> **Pour un agent d'exécution :** SOUS-SKILL REQUISE : utiliser
> `superpowers:subagent-driven-development` (recommandé) ou
> `superpowers:executing-plans` pour dérouler ce plan tâche par tâche. Les
> étapes sont en cases à cocher (`- [ ]`).

**But :** rendre le moteur muet après la mise en place. Il tient l'état, il
exécute les gestes qu'on lui dépose, il ne conduit plus rien et ne déclenche
plus aucune capacité.

**Architecture :** une règle `mode_manuel` inscrite dans la scène, une boucle
manuelle qui remplace le déroulé des tours dans `World.OnGameLoop`, une porte
unique dans `EventManager.BroadcastMessage` qui coupe tous les déclenchements,
quatre ajouts à l'API `Puzzle`, et un champ de scène qui enregistre les gestes
pour la sauvegarde et l'annulation.

**Pile technique :** moteur Python 3.10 (`Fusion/marvel-lcg-src/src`), harnais
maison qui détourne `DeviceManager.DoGetInput`.

**Spec :** `docs/superpowers/specs/2026-09-18-mode-manuel-design.md`

**Ce plan ne couvre que le moteur.** Le plateau (masquage des couches,
glisser-déposer, clavier, recherche catalogue, case de l'écran de préparation)
fait l'objet d'un second plan, `2026-09-18-mode-manuel-plateau.md`. À la fin de
celui-ci, le mode se prouve au harnais, pas encore à la souris.

## Contraintes globales

- **Une seule copie vivante du moteur** : `Fusion/marvel-lcg-src/`. On édite
  là, il n'y a aucune recopie à faire (GUIDE-CREATION-CONTENU §1.1).
- **Interpréteur** : `~/marvel-work/python/bin/python3.10`. Jamais le python du
  système.
- **Ce plan travaille sur `.game-src-par8`**, jamais sur `.game` ni
  `.game-src` : lancer le moteur depuis WSL détruit le cache de la table qui
  sert aux vraies parties.
- **Jamais deux harnais en parallèle sur le même dossier de jeu** : chacun
  réécrit `launch.json` et le voisin relit le port de l'autre.
- **Aucun déploiement**, à aucune étape. Le mot « déploie » vient de
  l'utilisateur, et de lui seul.
- **Si quelqu'un joue, prévenir avant tout redémarrage.**
- **Le drapeau s'appelle `mode_manuel`**, faux par défaut, posé par la liste
  `rules` du descripteur, donc inscrit dans la sauvegarde.
- **L'attribut qui ouvre la porte du silence s'appelle `world.manuel_actif`**,
  posé juste avant d'entrer dans la boucle manuelle. Surtout pas déduit de la
  règle seule : la mise en place, elle, a besoin que tout fonctionne.

## Ce qui est déjà mesuré, et qu'il ne faut pas re-supposer

Trois faits établis le 18/09/2026, par lecture du code :

1. **Exécuter des commandes `Puzzle` hors de `DoGetInput` fonctionne déjà.**
   `PuzzleHelper.Exec` est appelé dans `GameSetup`
   (`game/game_run/game_session.py:133`), sur le fil du jeu, hors de toute
   attente d'entrée, à chaque partie Puzzle. La boucle manuelle fera pareil.
2. **Les identifiants d'objets sont un simple compteur de création**
   (`game/object/manager.py:59`), sans aucun lien avec le tirage. Tout le
   corpus de cas Puzzle vise déjà les cartes par `c1`, `c2`, `c5` d'une
   exécution à l'autre. La tâche 5 le prouve pour de bon.
4. **Le pilote naïf d'un harnais BOUCLE dès qu'on appelle `GameLoop()`**
   (constaté le 15/09/2026, redémontré le 18/09/2026). Il rechoisit sans fin
   une action payante qu'il ne sait pas payer (« Enhanced Ivory Horn » du
   Rhino). C'est pour cette raison que `tools/test_manigance_face_a.py`
   s'arrête à `GameSetup()`. Le harnais de ce plan, lui, a besoin de la
   boucle : il lui faut donc une anti-boucle, décrite dans la tâche 1.

3. **Le récit à l'écran ne passe pas par la diffusion des messages** : les
   messages texte appellent `Present` dans leur **constructeur**
   (`game/message/sender/sender_deck.py:13` et suivants), pas depuis
   `BroadcastMessage`. Couper la diffusion ne coupe donc ni l'affichage ni le
   journal.

---

### Tâche 0 : le dossier de jeu de ce plan

**Fichiers :** aucun fichier suivi. Un dossier de travail jetable.

- [ ] **Étape 1 : créer `.game-src-par8`**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 - <<'PY'
import sys, os
sys.path.insert(0, os.path.abspath("tools"))
from test_capacites import preparer_dossiers_paralleles
print(preparer_dossiers_paralleles(".game-src", 9)[8])
PY
```

Attendu : le chemin `.../Fusion/marvel-lcg-src/.game-src-par8` s'affiche, et le
dossier existe. C'est une poignée de liens symboliques relatifs plus une copie
de `launch.json`, pas une copie du jeu.

- [ ] **Étape 2 : vérifier qu'aucun autre harnais ne tourne**

```bash
ps -ef | grep -E "test_capacites|autoplay|test_mode_manuel" | grep -v grep
```

Attendu : aucune ligne. Sinon, attendre la fin plutôt que de lancer par-dessus.

---

### Tâche 1 : la règle `mode_manuel`, et le harnais qui la prouve

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/world/world_rule.py:71`
- Modifier : `Fusion/marvel-lcg-src/src/game/render/descriptor/world.py:19`
- Modifier : `Fusion/marvel-lcg-src/src/game/render/to_descriptor.py:56`
- Créer : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py`

**Interfaces :**
- Produit : `world.rule.mode_manuel` (`VariableBool`), allumé en passant la
  chaîne `"mode_manuel"` dans les `rules` de la scène.
- Produit : `WorldDescriptor.mode_manuel: bool`, publié à chaque rendu.
- Produit : le harnais `tools/test_mode_manuel.py` et sa fonction
  `monter_le_moteur(game_dir, port, regles, scenario, heros)`, réutilisée par
  toutes les tâches suivantes.

- [ ] **Étape 1 : écrire le cas rouge**

Créer `Fusion/marvel-lcg-src/tools/test_mode_manuel.py` :

```python
"""Le mode manuel : le moteur se tait et ne fait plus que tenir l'etat.

Usage:
    ~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py \
        .game-src-par8 45200 [nom_du_cas]

Chaque cas tourne dans SON propre processus : le moteur est un singleton
global, impossible a reinitialiser proprement entre deux parties. On detourne
DeviceManager.DoGetInput pour repondre a la place du client, et on observe.
Meme gabarit que tools/test_manigance_face_a.py.
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

    ⚠ Contrairement au harnais de la manigance, celui-ci enchaine sur
    `GameLoop()` : tout le sujet du mode manuel est CE QUE FAIT LA BOUCLE, on
    ne peut pas s'arreter a la mise en place.
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
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            options = []
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
    from engine.file import FileManager
    chemin = FileManager.FindJsonPath(genre, nom)
    assert chemin, f"{genre} {nom} introuvable"
    return chemin


def deposer(jeu, *commandes):
    """Depose des commandes comme le ferait /sandbox_command, et laisse le fil
    du jeu les executer."""
    from game.puzzle import PuzzleHelper
    gestionnaire = jeu.controller_manager.device_manager
    gestionnaire.sandbox_executor = lambda cmds: PuzzleHelper.Exec(cmds, jeu.world)
    gestionnaire.QueueSandboxCommands(list(commandes))
    time.sleep(3)


def id_du_vilain(monde):
    from game.operate.worlds import Worlds
    vilains = Worlds.GetAllVillains(monde)
    assert vilains, "aucun vilain sur la table"
    return vilains[0].card.object_id


def cas_drapeau_pose(game_dir, port):
    """Le drapeau existe, la liste de regles l'allume, et la trame le publie."""
    _, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    assert bool(monde.rule.mode_manuel) is True, \
        "la regle mode_manuel n'a pas ete posee"
    descripteur = monde.render.descriptor
    assert getattr(descripteur, "mode_manuel", None) is True, \
        "la trame ne publie pas mode_manuel"
    return "le drapeau mode_manuel est pose et publie"


CAS = {
    "drapeau_pose": cas_drapeau_pose,
}


def main():
    game_dir = sys.argv[1]
    port = int(sys.argv[2])
    voulu = sys.argv[3] if len(sys.argv) > 3 else None
    noms = [voulu] if voulu else list(CAS)
    for rang, nom in enumerate(noms):
        fils = subprocess.run(
            [sys.executable, os.path.abspath(__file__), game_dir,
             str(port + rang), nom, "--fils"],
            cwd=RACINE, capture_output=True, text=True, timeout=300)
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
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45200 drapeau_pose
```

Attendu : ROUGE, avec `AttributeError: 'WorldRule' object has no attribute
'mode_manuel'`.

- [ ] **Étape 3 : poser le drapeau**

Dans `src/game/world/world_rule.py`, juste après la ligne
`self.mode_sandbox = VariableBool(self, False, "mode_sandbox")` :

```python
        # Mode manuel : apres la mise en place, le moteur ne conduit plus et ne
        # declenche plus rien, il tient l'etat (spec du 18/09/2026). Pose par
        # la liste `rules` du descripteur, donc conserve dans la sauvegarde :
        # on saura toujours qu'une partie n'a pas ete jouee par les regles.
        self.mode_manuel                    = VariableBool(self, False, "mode_manuel")
```

- [ ] **Étape 4 : publier le drapeau dans la trame**

Dans `src/game/render/descriptor/world.py`, après le champ `mode_sandbox` :

```python
    # Le plateau masque tout ce qui parle au nom du moteur quand ce drapeau est
    # vrai. Transmis a chaque rendu : il survit au rechargement de page et au
    # chargement d'une sauvegarde.
    mode_manuel: bool = field(default=False)
```

Dans `src/game/render/to_descriptor.py`, après la ligne `mode_sandbox` :

```python
        world_descriptor.mode_manuel = bool(world.rule.mode_manuel)
```

- [ ] **Étape 5 : relancer, le voir VERT**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45200 drapeau_pose
```

Attendu : `VERT : drapeau_pose`.

- [ ] **Étape 6 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add Fusion/marvel-lcg-src/src/game/world/world_rule.py \
        Fusion/marvel-lcg-src/src/game/render/descriptor/world.py \
        Fusion/marvel-lcg-src/src/game/render/to_descriptor.py \
        Fusion/marvel-lcg-src/tools/test_mode_manuel.py
git commit -m "feat(manuel): le drapeau mode_manuel, et son harnais"
```

---

### Tâche 2 : la boucle manuelle, et le moteur qui se tait

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/world/world.py:746` (`OnGameLoop`)
- Modifier : `Fusion/marvel-lcg-src/src/game/world/world.py` (constructeur, pour
  `manuel_actif`)
- Modifier : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py`

**Interfaces :**
- Consomme : `world.rule.mode_manuel` (tâche 1), `monter_le_moteur` et
  `deposer` (tâche 1).
- Produit : `World.manuel_actif: bool`, faux pendant la mise en place, vrai dès
  l'entrée dans la boucle manuelle.
- Produit : `World.ManualLoop() -> None`.

- [ ] **Étape 1 : écrire les deux cas rouges**

Ajouter dans `tools/test_mode_manuel.py`, avant `CAS = {...}` :

```python
def cas_moteur_muet(game_dir, port):
    """Apres la mise en place, plus rien ne bouge tout seul.

    Le temoin qui compte est le REFUS d'avancer : on regarde que le journal des
    questions ne grossit plus, et que le compteur de tours reste a zero. Un
    moteur qui conduit encore ferait les deux.
    """
    _, monde, journal = monter_le_moteur(game_dir, port, ["mode_manuel"])
    assert monde.manuel_actif is True, "la boucle manuelle n'a pas demarre"
    avant = len(journal)
    time.sleep(8)
    assert len(journal) == avant, \
        f"le moteur a repose {len(journal) - avant} question(s) apres la mise en place"
    assert monde.round_id == 0, \
        f"le moteur a demarre un tour tout seul : round_id={monde.round_id}"
    return "le moteur se tait apres la mise en place"


def cas_automatique_avance(game_dir, port):
    """Le controle : SANS la regle, le moteur conduit toujours.

    Sans ce cas, `cas_moteur_muet` passerait aussi sur un moteur casse qui ne
    demarre pas du tout.
    """
    _, monde, journal = monter_le_moteur(game_dir, port, [])
    assert getattr(monde, "manuel_actif", False) is False
    avant = len(journal)
    time.sleep(8)
    assert len(journal) > avant, \
        "le moteur automatique ne pose plus de question : le harnais est casse"
    assert monde.round_id >= 1, \
        f"le moteur automatique n'a pas demarre de tour : round_id={monde.round_id}"
    return "sans la regle, le moteur conduit toujours"


def cas_commande_executee(game_dir, port):
    """La boucle manuelle execute bien ce qu'on lui depose.

    C'est la preuve que `PuzzleHelper.Exec` tourne hors de `DoGetInput` : le
    fil du jeu dort dans la boucle manuelle, pas dans une attente de reponse.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    carte = monde.object_manager.card_dict[vilain]
    assert carte.face.GetLostHealth() == 3, \
        f"la commande n'a pas ete executee : degats={carte.face.GetLostHealth()}"
    return "la boucle manuelle execute les commandes deposees"
```

Et les inscrire :

```python
CAS = {
    "drapeau_pose": cas_drapeau_pose,
    "moteur_muet": cas_moteur_muet,
    "automatique_avance": cas_automatique_avance,
    "commande_executee": cas_commande_executee,
}
```

- [ ] **Étape 2 : lancer les trois cas, les voir ROUGES**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45210 moteur_muet
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45220 commande_executee
```

Attendu : ROUGE sur `moteur_muet` (`AttributeError: 'World' object has no
attribute 'manuel_actif'`), ROUGE sur `commande_executee` (les dégâts valent 0,
la boucle automatique n'a jamais rendu la main pour exécuter la commande).

`automatique_avance` doit être VERT dès maintenant : il décrit le
comportement actuel, et sert de contrôle.

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45230 automatique_avance
```

- [ ] **Étape 3 : poser `manuel_actif` dans le constructeur**

Dans `src/game/world/world.py`, dans `World.__init__`, à côté des autres
drapeaux d'état :

```python
        # Mode manuel : vrai UNIQUEMENT une fois la mise en place finie, quand
        # la boucle manuelle a pris la main. Surtout pas `rule.mode_manuel` :
        # la mise en place, elle, a besoin que tout fonctionne, questions et
        # capacites comprises.
        self.manuel_actif: bool = False
```

- [ ] **Étape 4 : écrire la boucle manuelle**

Dans `src/game/world/world.py`, dans la classe `World`, juste avant
`def OnGameLoop` :

```python
    def ManualLoop(self) -> None:
        """Le moteur ne conduit plus : il attend, il execute, il redessine.

        Trois choses en rond, et rien d'autre. Aucune question n'est posee,
        donc `asking_players` reste vide et le plateau n'a rien a afficher ni a
        filtrer.

        ⚠ L'attente passe par `notify.input`, la MEME condition que
        `QueueSandboxCommands` reveille (engine/device/manager/base.py:53). Une
        attente sur autre chose ne serait jamais reveillee par une commande.
        """
        device_manager = self.controller_manager.device_manager

        self.manuel_actif = True

        while not self.is_game_over:
            device_manager.notify.input.Wait(
                lambda: bool(device_manager.sandbox_commands)
                        or device_manager.notify.should_exit_wait
                        or self.is_game_over,
                None,
            )
            if self.is_game_over:
                break
            if device_manager.DrainSandboxCommands():
                # Un rendu FORCE : rien d'autre ne redessinera, puisque plus
                # aucune question ne part et que le rendu normal suit les
                # questions.
                self.render.PresentForceNoWait()
```

- [ ] **Étape 5 : brancher la boucle**

Dans `src/game/world/world.py`, remplacer la fin de `OnGameLoop` :

```python
        while not self.is_game_over:
            game_round()
```

par :

```python
        # Mode manuel : on n'entre JAMAIS dans le deroule des tours. C'est le
        # seul endroit qui conduit une partie, donc le seul a neutraliser.
        if self.rule.mode_manuel:
            return self.ManualLoop()

        while not self.is_game_over:
            game_round()
```

- [ ] **Étape 6 : relancer les trois cas, les voir VERTS**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45240 moteur_muet
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45250 commande_executee
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45260 automatique_avance
```

Attendu : `VERT` pour les trois.

- [ ] **Étape 7 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add Fusion/marvel-lcg-src/src/game/world/world.py \
        Fusion/marvel-lcg-src/tools/test_mode_manuel.py
git commit -m "feat(manuel): la boucle manuelle, le moteur ne conduit plus"
```

---

### Tâche 3 : la porte du silence, aucune capacité ne part

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/event/manager.py:650`
  (`BroadcastMessage`)
- Modifier : `Fusion/marvel-lcg-src/src/game/event/manager.py:638`
  (`BroadcastStackMessage`)
- Modifier : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py`

**Interfaces :**
- Consomme : `world.manuel_actif` (tâche 2), `deposer` et `id_du_vilain`
  (tâche 1).
- Produit : rien de nouveau. Une porte, dans deux méthodes existantes.

- [ ] **Étape 1 : écrire les deux cas rouges**

Ajouter dans `tools/test_mode_manuel.py`, avant `CAS = {...}` :

```python
def cas_aucun_declenchement(game_dir, port):
    """Un vilain reduit a zero n'est PAS vaincu tout seul.

    C'est le temoin du REFUS, et il porte sur un effet de REGLE, pas sur une
    capacite de carte : si celui-la ne part plus, aucun ne part. En manuel,
    c'est le joueur qui range la carte, comme sur une vraie table.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 999)")
    assert monde.is_game_over is False, \
        "le moteur a declare la partie finie : un effet de regle est parti"
    carte = monde.object_manager.card_dict[vilain]
    assert carte.face.IsInPlay(), \
        "le vilain a quitte la table tout seul"
    return "aucun declenchement en manuel : le vilain reste sur la table"


def cas_declenchement_en_automatique(game_dir, port):
    """Le controle : la MEME commande, sans la regle, finit la partie.

    Sans ce cas, `cas_aucun_declenchement` passerait aussi sur une commande qui
    n'aurait rien fait du tout.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, [])
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 999)")
    time.sleep(5)
    assert monde.is_game_over is True, \
        "en automatique, 999 degats auraient du vaincre le vilain"
    return "en automatique, la meme commande vainc le vilain"
```

Et les inscrire dans `CAS` sous les clés `"aucun_declenchement"` et
`"declenchement_en_automatique"`.

- [ ] **Étape 2 : lancer les deux cas**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45300 aucun_declenchement
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45310 declenchement_en_automatique
```

Attendu : ROUGE sur `aucun_declenchement` (« le moteur a declare la partie
finie »), VERT sur `declenchement_en_automatique`, qui décrit l'existant.

- [ ] **Étape 3 : poser la porte**

Dans `src/game/event/manager.py`, tout au début de `BroadcastMessage`, avant
la garde `if self.world.is_game_over:` :

```python
        # LA PORTE DU MODE MANUEL (spec du 18/09/2026). Tout declencheur de
        # toute carte, et tout effet de regle, passe par ici : c'est le seul
        # endroit a fermer pour que le moteur se taise vraiment.
        #
        # ⚠ Le recit a l'ecran ne passe PAS par ici : les messages texte
        # appellent `Present` dans leur CONSTRUCTEUR (sender_deck.py:13 et
        # suivants). Le plateau continue donc d'annoncer « carte defaussee » et
        # le journal de la noter, sans qu'aucune capacite ne parte.
        #
        # ⚠ Les effets de REGLE passent par la meme porte, et c'est voulu : un
        # sbire a zero point de vie n'est plus defausse tout seul. Corollaire
        # assume : les modificateurs de caracteristiques ne s'appliquent plus
        # non plus, le plateau montre les valeurs imprimees.
        if self.world.manuel_actif:
            return
```

Et, à l'identique, tout au début de `BroadcastStackMessage` :

```python
        if self.world.manuel_actif:
            return
```

- [ ] **Étape 4 : relancer les deux cas, les voir VERTS**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45320 aucun_declenchement
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45330 declenchement_en_automatique
```

Attendu : `VERT` pour les deux.

- [ ] **Étape 5 : vérifier qu'on n'a rien cassé en automatique**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45340 automatique_avance
```

Attendu : `VERT`. La porte ne doit se fermer que sur `manuel_actif`.

- [ ] **Étape 6 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add Fusion/marvel-lcg-src/src/game/event/manager.py \
        Fusion/marvel-lcg-src/tools/test_mode_manuel.py
git commit -m "feat(manuel): la porte du silence, plus aucune capacite ne part"
```

---

### Tâche 4 : les quatre gestes qui manquent à l'API `Puzzle`

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/puzzle/puzzle.py`
- Modifier : `Fusion/marvel-lcg-src/src/game/puzzle/puzzle_.py`
- Modifier : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py`

**Interfaces :**
- Consomme : `monter_le_moteur`, `deposer` (tâche 1).
- Produit : `Puzzle.MoveTo(card, zone, position='Top', player=0)`,
  `Puzzle.Shuffle(zone, player=0)`, `Puzzle.Attach(card, cible)`,
  `Puzzle.Engage(card, player=0)`.
  `zone` est le nom d'un membre de `DeckType` (`game/deck/deck_type.py:193`),
  par exemple `'EncounterDeck'`, `'HandsArea'`, `'DiscardPile'`,
  `'RemovedArea'`, `'AsideDeck'`.

- [ ] **Étape 1 : écrire le cas rouge**

Ajouter dans `tools/test_mode_manuel.py`, avant `CAS = {...}` :

```python
def cas_deplacement_libre(game_dir, port):
    """N'importe quelle carte va dans n'importe quelle pile, regles ou pas.

    On envoie une carte de la MAIN du heros dans le DECK RENCONTRE : aucune
    regle du jeu ne permet ca. C'est precisement le sujet.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    joueur = monde.const_players[0]
    main = list(joueur.hand_cards.GetAll())
    assert main, "la main de depart est vide"
    carte = main[0].card.object_id

    from game.operate.worlds import Worlds
    avant = len(Worlds.GetEncounterDeckCards(monde))

    deposer(jeu, f"Puzzle.MoveTo({carte}, 'EncounterDeck')")

    apres = len(Worlds.GetEncounterDeckCards(monde))
    assert apres == avant + 1, \
        f"le deck rencontre devait passer de {avant} a {avant + 1}, il vaut {apres}"
    return "une carte de la main est allee dans le deck rencontre"


def cas_melange(game_dir, port):
    """Melanger une pile change son ordre, sans rien perdre."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    joueur = monde.const_players[0]
    avant = [c.card.object_id for c in joueur.player_deck.GetAll()]
    assert len(avant) > 10, f"deck trop court pour un melange : {len(avant)}"

    deposer(jeu, "Puzzle.Shuffle('PlayerDeck')")

    apres = [c.card.object_id for c in joueur.player_deck.GetAll()]
    assert sorted(apres) == sorted(avant), "le melange a perdu ou ajoute des cartes"
    assert apres != avant, "le melange n'a rien change a l'ordre"
    return "le deck du joueur a ete melange sans rien perdre"
```

Et les inscrire dans `CAS` sous `"deplacement_libre"` et `"melange"`.

- [ ] **Étape 2 : lancer les deux cas, les voir ROUGES**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45400 deplacement_libre
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45410 melange
```

Attendu : ROUGE, le deck rencontre n'a pas bougé. La commande est refusée en
amont par l'analyse syntaxique du serveur ? Non : ici on dépose en direct, donc
c'est `AttributeError: 'RunPuzzle' object has no attribute 'MoveTo'` qui est
tracé dans `sandbox_last_error`, et le compte ne bouge pas.

- [ ] **Étape 3 : écrire les quatre méthodes**

Dans `src/game/puzzle/puzzle.py`, dans la classe `RunPuzzle`, juste avant
`def PutIntoDeck` :

```python
    # Les piles atteignables par `MoveTo`, nommees comme les membres de
    # `DeckType` (game/deck/deck_type.py:193). Table EXPLICITE et non
    # reflexive : le moteur n'expose aucun registre des piles, et deviner une
    # pile ferait disparaitre des cartes dans une zone qu'on ne regarde jamais.
    ZONES_JOUEUR = {
        'PlayerDeck':           lambda j: j.player_deck,
        'DiscardPile':          lambda j: j.discard_pile,
        'HandsArea':            lambda j: j.hand_cards,
        'AlliesArea':           lambda j: j.allies,
        'SupportsArea':         lambda j: j.supports,
        'HeroArea':             lambda j: j.area_hero,
        'EngagedEnemiesArea':   lambda j: j.engaged_minions,
        'ResourcesArea':        lambda j: j.area_resources,
        'ReserveArea':          lambda j: j.reserve,
        'AsideDeck':            lambda j: j.set_aside_deck,
        'ObligationsArea':      lambda j: j.obligations_area,
        'AdditionalDeck':       lambda j: j.additional_deck,
    }

    ZONES_MONDE = {
        'EncounterDeck':        lambda w: w.GetScenario().encounter_deck,
        'EncounterDiscardPile': lambda w: w.GetScenario().encounter_discard_pile,
        'VillainArea':          lambda w: w.GetScenario().area_villain,
        'MainSchemesArea':      lambda w: w.area_schemes_main,
        'SideSchemesArea':      lambda w: w.area_schemes_side,
        'EnvironmentArea':      lambda w: w.area_environment,
        'ProcessingArea':       lambda w: w.area_processing,
        'RemovedArea':          lambda w: w.area_removed,
        'VictoryDisplay':       lambda w: w.victory_display,
    }

    def _ZoneParNom(self, zone: str, player: int) -> 'Deck':
        """Rend la pile designee par son nom.

        ⚠ Un nom inconnu doit ECHOUER bruyamment. Un repli silencieux sur une
        pile par defaut ferait disparaitre la carte.
        """
        if zone in RunPuzzle.ZONES_MONDE:
            return RunPuzzle.ZONES_MONDE[zone](self.world)
        if zone in RunPuzzle.ZONES_JOUEUR:
            return RunPuzzle.ZONES_JOUEUR[zone](self.world.const_players[player])
        raise KeyError(f"zone inconnue : {zone}")

    def MoveTo(self, card: CardName, zone: str, position: str='Top', player: int=0):
        """Le deplacement LIBRE : n'importe quelle carte vers n'importe quelle
        pile, sans aucune verification.

        C'est l'echappatoire du mode manuel (spec du 18/09/2026) : sans elle,
        une zone oubliee bloque la partie. Le deplacement reel se fait dans
        `card.MoveToArea`, le message qui suit n'est qu'une notification, donc
        la porte du silence ne casse rien ici.
        """
        from game.operate.faces import Faces
        face = self.FindOrCreateFace(card)
        pile = self._ZoneParNom(zone, player)
        if position == 'Bottom':
            face.card.MoveToBottom(pile, self.debug_rule)
        else:
            Faces.MoveAllTo([face], pile, self.debug_rule)

    def Shuffle(self, zone: str, player: int=0):
        """Melange une pile."""
        self._ZoneParNom(zone, player).Shuffle(self.debug_rule)

    def Attach(self, card: CardName, cible: CardName):
        """Pose une amelioration ou un soutien SUR une carte precise."""
        from game.operate.faces import Faces
        face = self.FindOrCreateFace(card)
        hote = self.FindOrCreateFace(cible)
        Faces.MoveAllTo([face], hote.components.inventory.deck, self.debug_rule)

    def Engage(self, card: CardName, player: int=0):
        """Engage un sbire avec un joueur, ou l'en desengage s'il y est deja."""
        from game.operate.faces import Faces
        face = self.FindOrCreateFace(card)
        joueur = self.world.const_players[player]
        if face.card.area is joueur.engaged_minions:
            Faces.MoveAllTo([face], self.world.area_processing, self.debug_rule)
        else:
            Faces.MoveAllTo([face], joueur.engaged_minions, self.debug_rule)
```

⚠ `hote.components.inventory.deck` est la zone des ameliorations d'une carte
(`game/card/face/component/inventory.py:9`). Si le cas rouge dit que le chemin
n'existe pas sur la face visee, c'est que la carte ne porte pas d'inventaire :
`Attach` doit alors echouer bruyamment, pas se rabattre ailleurs.

Dans `src/game/puzzle/puzzle_.py`, ajouter les signatures pour l'aide à la
saisie, après `def PutIntoDeck` :

```python
def MoveTo(card: CardName, zone: str, position: str='Top', player: int=0): ...
def Shuffle(zone: str, player: int=0): ...
def Attach(card: CardName, cible: CardName): ...
def Engage(card: CardName, player: int=0): ...
```

- [ ] **Étape 4 : relancer les deux cas, les voir VERTS**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45420 deplacement_libre
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45430 melange
```

Attendu : `VERT` pour les deux.

- [ ] **Étape 5 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add Fusion/marvel-lcg-src/src/game/puzzle/puzzle.py \
        Fusion/marvel-lcg-src/src/game/puzzle/puzzle_.py \
        Fusion/marvel-lcg-src/tools/test_mode_manuel.py
git commit -m "feat(manuel): deplacement libre, melange, attache, engagement"
```

---

### Tâche 5 : la sauvegarde des gestes, et l'aller-retour qui la prouve

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/scene/scene.py:53` (champ `puzzle`)
- Modifier : `Fusion/marvel-lcg-src/src/game/world/world.py` (`ManualLoop`)
- Modifier : `Fusion/marvel-lcg-src/src/game/game_run/game_session.py:133`
- Modifier : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py`

**Interfaces :**
- Consomme : `World.ManualLoop` (tâche 2), `world.manuel_actif` (tâche 2).
- Produit : `Scene.manuel_commands: List[str]`, la liste ordonnée des gestes
  acceptés, écrite dans la sauvegarde et rejouée à la mise en place.
- Produit : `monter_le_moteur(..., sauvegarde=None)`, qui charge une
  sauvegarde au lieu de créer une partie neuve.

- [ ] **Étape 1 : écrire les deux cas rouges**

Dans `tools/test_mode_manuel.py`, remplacer la signature et le corps de
`monter_le_moteur` pour accepter une sauvegarde. La ligne

```python
def monter_le_moteur(game_dir, port, regles, scenario="rhino", heros="spider_man"):
```

devient

```python
def monter_le_moteur(game_dir, port, regles, scenario="rhino", heros="spider_man",
                     sauvegarde=None):
```

et le bloc qui construit la scène

```python
    with open(_chemin_json("Campaign", scenario)) as f:
        campagne = f.read()
    with open(_chemin_json("Hero", heros)) as f:
        hero = f.read()
    scene = SceneLoader.NewFromJson(campagne, None, [hero], 42, regles, {})
```

devient

```python
    if sauvegarde:
        # Une partie RECHARGEE : la scene porte deja ses regles et ses gestes.
        scene = SceneLoader.Load(sauvegarde)
        assert scene, f"sauvegarde illisible : {sauvegarde}"
    else:
        with open(_chemin_json("Campaign", scenario)) as f:
            campagne = f.read()
        with open(_chemin_json("Hero", heros)) as f:
            hero = f.read()
        scene = SceneLoader.NewFromJson(campagne, None, [hero], 42, regles, {})
```

Puis ajouter les deux cas, avant `CAS = {...}` :

```python
def cas_geste_enregistre(game_dir, port):
    """Un geste accepte entre dans la scene, donc dans la sauvegarde."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    gestes = jeu.session.scene.manuel_commands
    assert gestes == [f"Puzzle.Damage({vilain}, 3)"], \
        f"la scene n'a pas retenu le geste : {gestes}"
    return "le geste est enregistre dans la scene"


def cas_aller_retour(game_dir, port):
    """Geste, sauvegarde, rechargement : l'etat est identique.

    C'est LE cas qui leve le dernier doute du cadrage, celui sur la
    reproductibilite des identifiants d'objets : le rejeu vise la carte par son
    identifiant, et doit retomber sur la meme.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")

    chemin = os.path.join(os.path.abspath(game_dir), "manuel-aller-retour.json")
    ecrit = jeu.session.SaveScene(name=chemin, delete_old=False)
    assert ecrit, "la sauvegarde n'a pas ete ecrite"

    env = dict(os.environ)
    env["MC_SAUVEGARDE"] = chemin
    env["MC_VILAIN"] = str(vilain)
    fils = subprocess.run(
        [sys.executable, os.path.abspath(__file__), game_dir,
         str(port + 1), "relire_sauvegarde", "--fils"],
        cwd=RACINE, capture_output=True, text=True, timeout=300, env=env)
    assert fils.returncode == 0, \
        f"le rechargement a echoue :\n{fils.stdout[-3000:]}\n{fils.stderr[-3000:]}"
    return "aller-retour de sauvegarde : l'etat est identique"


def cas_relire_sauvegarde(game_dir, port):
    """Le fils de `cas_aller_retour` : il recharge et verifie les degats."""
    chemin = os.environ["MC_SAUVEGARDE"]
    vilain = int(os.environ["MC_VILAIN"])
    _, monde, _ = monter_le_moteur(game_dir, port, [], sauvegarde=chemin)
    assert bool(monde.rule.mode_manuel) is True, \
        "la sauvegarde a perdu la regle mode_manuel"
    carte = monde.object_manager.card_dict[vilain]
    assert carte.face.GetLostHealth() == 3, \
        f"apres rechargement : degats={carte.face.GetLostHealth()}, attendu 3"
    return "la partie rechargee porte bien le geste"
```

Et les inscrire dans `CAS` sous `"geste_enregistre"`, `"aller_retour"` et
`"relire_sauvegarde"`.

⚠ `relire_sauvegarde` ne doit PAS tourner dans la batterie complète : il n'a de
sens qu'appelé par `cas_aller_retour`, qui lui passe le chemin de la sauvegarde
par l'environnement. Le sortir de la liste par défaut, dans `main()` :

```python
    # Les cas appeles par un AUTRE cas, jamais tout seuls.
    SUR_DEMANDE = {"relire_sauvegarde"}
    noms = [voulu] if voulu else [n for n in CAS if n not in SUR_DEMANDE]
```

- [ ] **Étape 2 : lancer les deux cas, les voir ROUGES**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45500 geste_enregistre
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45510 aller_retour
```

Attendu : ROUGE sur `geste_enregistre` (`AttributeError: 'Scene' object has no
attribute 'manuel_commands'`), ROUGE sur `aller_retour` pour la même raison.

- [ ] **Étape 3 : ajouter le champ à la scène**

Dans `src/game/scene/scene.py`, après le champ `puzzle` :

```python
    # LES GESTES DU MODE MANUEL (spec du 18/09/2026), dans l'ordre ou le joueur
    # les a faits. Rejoues a la mise en place, comme `puzzle` l'est pour une
    # partie Puzzle.
    #
    # ⚠ CHAMP SEPARE de `puzzle`, et c'est deliberé : les deux usages ne
    # doivent pas se melanger, et un champ a defaut vide laisse les
    # sauvegardes existantes se recharger sans changer de sens.
    manuel_commands: List[str] = field(default_factory=lambda: [])
```

- [ ] **Étape 4 : enregistrer les gestes acceptés**

Dans `src/game/world/world.py`, dans `ManualLoop`, remplacer le corps de la
boucle par :

```python
            if self.is_game_over:
                break
            # On note AVANT de vider : `DrainSandboxCommands` consomme la liste.
            en_attente = list(device_manager.sandbox_commands)
            if device_manager.DrainSandboxCommands():
                if not device_manager.sandbox_last_error:
                    self.scene.manuel_commands += en_attente
                # Un rendu FORCE : rien d'autre ne redessinera, puisque plus
                # aucune question ne part et que le rendu normal suit les
                # questions.
                self.render.PresentForceNoWait()
```

- [ ] **Étape 5 : rejouer les gestes à la mise en place**

Dans `src/game/game_run/game_session.py`, dans `GameSetup`, remplacer

```python
        if self.world.scene.is_puzzle:
            from game.puzzle import PuzzleHelper
            PuzzleHelper.Exec(self.world.scene.puzzle, self.world)
        return not self.world.is_game_over
```

par

```python
        if self.world.scene.is_puzzle:
            from game.puzzle import PuzzleHelper
            PuzzleHelper.Exec(self.world.scene.puzzle, self.world)

        if self.world.rule.mode_manuel:
            # Le silence commence ICI, avant le rejeu : les gestes ont ete
            # appliques porte fermee, ils doivent se rejouer porte fermee,
            # sinon l'etat rechargé diverge de l'etat sauvegarde.
            self.world.manuel_actif = True
            if self.world.scene.manuel_commands:
                from game.puzzle import PuzzleHelper
                PuzzleHelper.Exec(self.world.scene.manuel_commands, self.world)

        return not self.world.is_game_over
```

- [ ] **Étape 6 : relancer les cas, les voir VERTS**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45520 geste_enregistre
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45530 aller_retour
```

Attendu : `VERT` pour les deux. Le second lance lui-même son fils
`relire_sauvegarde`.

- [ ] **Étape 7 : vérifier qu'une sauvegarde ancienne se recharge encore**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45540 automatique_avance
```

Attendu : `VERT`. Le champ est à défaut vide, une scène écrite avant ce
changement ne porte rien et se rejoue à l'identique.

- [ ] **Étape 8 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add Fusion/marvel-lcg-src/src/game/scene/scene.py \
        Fusion/marvel-lcg-src/src/game/world/world.py \
        Fusion/marvel-lcg-src/src/game/game_run/game_session.py \
        Fusion/marvel-lcg-src/tools/test_mode_manuel.py
git commit -m "feat(manuel): les gestes entrent dans la sauvegarde et se rejouent"
```

---

### Tâche 6 : annuler le dernier geste

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/game_run/game_session.py`
- Modifier : `Fusion/marvel-lcg-src/src/engine/device/web/server/server_get.py`
- Modifier : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py`

**Interfaces :**
- Consomme : `Scene.manuel_commands` (tâche 5).
- Produit : `GameSession.AnnulerDernierGeste() -> bool`, qui retire le dernier
  geste et relance la partie depuis la scène.
- Produit : la route `POST /manuel_undo`, qui rend
  `{"result": "annule", "restants": N}` ou `{"error": "..."}` en 409.

- [ ] **Étape 1 : rendre le harnais capable de rejouer une mise en place**

Dans `tools/test_mode_manuel.py`, remplacer la fonction `run` interne de
`monter_le_moteur` :

```python
    def run():
        try:
            if jeu.GameSetup():
                jeu.GameLoop()
        except BaseException:
            import traceback
            traceback.print_exc()
```

par

```python
    def run():
        # Une partie peut REDEMARRER sur place : c'est ce que fait
        # `LoadScene`, donc ce que fait l'annulation d'un geste. `GameSetup`
        # appelle `state.ResetStartState()`, donc `start_state` est vide
        # pendant qu'on joue et repose des qu'une scene est rechargee.
        import traceback
        premier = True
        while premier or jeu.state.start_state:
            premier = False
            try:
                if jeu.GameSetup():
                    jeu.GameLoop()
            except BaseException:
                traceback.print_exc()
                return
```

- [ ] **Étape 2 : écrire le cas rouge**

Ajouter dans `tools/test_mode_manuel.py`, avant `CAS = {...}` :

```python
def cas_annulation(game_dir, port):
    """Ctrl+Z : le dernier geste part, les precedents restent.

    Deux gestes, 3 puis 4 degats. Apres annulation il doit rester 3, et un seul
    geste dans la scene. Le monde est RECONSTRUIT par le rechargement : on
    relit `jeu.world`, jamais la reference d'avant.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    deposer(jeu, f"Puzzle.Damage({vilain}, 4)")
    carte = monde.object_manager.card_dict[vilain]
    assert carte.face.GetLostHealth() == 7, \
        f"avant annulation : degats={carte.face.GetLostHealth()}, attendu 7"

    assert jeu.session.AnnulerDernierGeste() is True
    time.sleep(20)

    scene = jeu.session.scene
    assert len(scene.manuel_commands) == 1, \
        f"il devait rester 1 geste, il en reste {len(scene.manuel_commands)}"
    monde2 = jeu.world
    carte2 = monde2.object_manager.card_dict[vilain]
    assert carte2.face.GetLostHealth() == 3, \
        f"apres annulation : degats={carte2.face.GetLostHealth()}, attendu 3"
    return "l'annulation retire le dernier geste et garde les precedents"
```

Et l'inscrire dans `CAS` sous `"annulation"`.

- [ ] **Étape 3 : lancer le cas, le voir ROUGE**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45600 annulation
```

Attendu : ROUGE, `AttributeError: 'GameSession' object has no attribute
'AnnulerDernierGeste'`.

- [ ] **Étape 4 : écrire l'annulation**

Dans `src/game/game_run/game_session.py`, dans la classe `GameSession`, juste
après `def Undo` :

```python
    def AnnulerDernierGeste(self) -> bool:
        """Retire le dernier geste manuel et rejoue la partie sans lui.

        ⚠ Rien a voir avec `Undo`, qui rejoue les ENTREES du joueur : en mode
        manuel il n'y en a aucune. Ici on rejoue la mise en place, puis la
        liste des gestes amputee de son dernier element.

        Rend faux s'il n'y a rien a annuler, pour que l'appelant puisse le dire
        au joueur au lieu de relancer une partie pour rien.
        """
        scene = self.scene
        if scene is None or not scene.manuel_commands:
            return False
        scene.manuel_commands.pop()
        self.LoadScene(scene, None, "Load")
        return True
```

- [ ] **Étape 5 : relancer le cas, le voir VERT**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45610 annulation
```

Attendu : `VERT : annulation`.

- [ ] **Étape 6 : ouvrir la route au plateau**

Dans `src/engine/device/web/server/server_get.py`, juste après la méthode qui
sert `/sandbox_command` :

```python
    async def manuel_undo(self, request: web.Request) -> web.Response:
        """Ctrl+Z du mode manuel : retire le dernier geste et rejoue sans lui.

        Aucun corps de requete : il n'y a qu'un seul geste annulable, le
        dernier. Le plateau n'a donc rien a envoyer, et rien a tenir a jour de
        son cote.
        """
        world = self.game.world
        if world is None or not world.rule.mode_manuel:
            return web.json_response({'error': 'pas une partie manuelle'}, status=409)
        if not self.game.session.AnnulerDernierGeste():
            return web.json_response({'error': 'rien a annuler'}, status=409)
        return web.json_response({
            'result': 'annule',
            'restants': len(self.game.scene.manuel_commands),
        })
```

Et l'inscrire auprès du routeur, à côté de `/sandbox_command`, en suivant
exactement la forme employée là-bas pour déclarer une route POST.

- [ ] **Étape 7 : relancer toute la batterie**

```bash
~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py .game-src-par8 45700
```

Attendu : `VERT` pour les dix cas, dans l'ordre : `drapeau_pose`,
`moteur_muet`, `automatique_avance`, `commande_executee`,
`aucun_declenchement`, `declenchement_en_automatique`, `deplacement_libre`,
`melange`, `geste_enregistre`, `aller_retour`, `annulation`.
`relire_sauvegarde` n'y figure pas : `aller_retour` le lance lui-même.

- [ ] **Étape 8 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add Fusion/marvel-lcg-src/src/game/game_run/game_session.py \
        Fusion/marvel-lcg-src/src/engine/device/web/server/server_get.py \
        Fusion/marvel-lcg-src/tools/test_mode_manuel.py
git commit -m "feat(manuel): annuler le dernier geste"
```

- [ ] **Étape 9 : ranger le dossier de travail**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"
rm -rf .game-src-par8
```

Attendu : le dossier disparaît. `.game` et `.game-src` ne sont pas touchés.

---

## Ce que ce plan ne fait pas

- Le mode n'est **pas atteignable depuis l'écran de préparation** : la case
  « Partie manuelle » est dans le plan plateau. Ici, la règle se pose par la
  liste `rules`, ce que fait le harnais.
- Le plateau continue d'afficher ses bandeaux, son assistant et son déroulé de
  phase, qui ne diront plus rien de juste. C'est attendu, et c'est la première
  tâche du plan plateau.
- La victoire, la défaite et le journal de campagne restent ceux du mode
  automatique.
