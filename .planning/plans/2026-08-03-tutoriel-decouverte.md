# Mode Découverte — plan d'implémentation

> **Pour les agents :** SOUS-SKILL REQUIS — utiliser `superpowers:subagent-driven-development` (recommandé) ou `superpowers:executing-plans` pour dérouler ce plan tâche par tâche. Les étapes utilisent la syntaxe case à cocher (`- [ ]`).

**Objectif :** un mode « Découverte » qui lance une partie figée (Spider-Man contre Rhino, seed 42) et l'accompagne d'un coach donnant une mission à la fois, jusqu'à ce qu'un débutant total ait fini sa première partie.

**Architecture :** le contenu pédagogique vit dans un module pur (`lecons.ts`), testable sous Node. Une couche React (`CoucheCoach`) l'affiche par-dessus la table et compare l'état du monde à la mission courante. Le wizard gagne un mode qui saute ses 5 étapes. Le moteur n'est pas touché.

**Stack :** React 19 + TypeScript (`ui-app/`), JavaScript ES modules sans framework (`public/js/`), Node pour les vérifications hors navigateur, Python 3.10 pour le garde-fou du seed.

**Spec :** `.planning/todos/2026-08-03-tutoriel-decouverte.md`

## Contraintes globales

- **Le moteur ne change pas.** Aucune modification sous `src/` du moteur. Le coach observe, il n'agit jamais.
- **Le coach ne bloque jamais rien** : `pointer-events: none` sauf sur ses propres boutons, comme `SplashTour`.
- **Édition dans la copie VIVANTE** `~/marvel-work/fusion/marvel-lcg-src/` pour tout ce qui est sous `public/`, puis `rsync` (guide §1.3). `ui-app/` s'édite dans le dossier projet et se déploie par `ui-app/deployer.sh`.
- **Deux numérotations à ne pas confondre** : le coach lit `players[0]`, l'unique joueur du mode Découverte.
- Toute chaîne visible passe par `t()` et a son entrée dans `ui-app/src/board/dico-en.ts` (côté plateau) ou `public/js/prepare/dico-en.js` (côté wizard). Guide §11.
- **Pas d'em dash ni de tiret parenthétique** dans les textes visibles.
- Les leçons ne désignent **jamais** une carte par sa position dans la main : uniquement par son nom.

---

### Tâche 1 : le garde-fou du seed

C'est la fondation. Toutes les leçons supposent que la main de départ ne bouge pas ; si le moteur change un jour son tirage, ce test doit le dire **avant** que les leçons deviennent fausses.

**Fichiers :**
- Créer : `tools/test_seed_tutoriel.py`

**Interfaces :**
- Consomme : `SceneLoader.NewScene(scenario, None, [hero], seed)` du moteur.
- Produit : rien de consommé par une autre tâche. C'est un filet.

- [ ] **Étape 1 : écrire le test**

Créer `tools/test_seed_tutoriel.py` :

```python
"""Garde-fou du mode Decouverte : la partie du tutoriel doit rester IDENTIQUE.

Le tutoriel nomme des cartes precises (« joue Coup de pied volant ») parce que
la main de depart est garantie par le seed. Si le moteur change son tirage, les
lecons deviennent fausses SANS que rien ne plante : ce test est le seul endroit
qui s'en apercevra.

Reference relevee le 3/8/2026 : Spider-Man contre Rhino, seed 42.

Usage: python3.10 tools/test_seed_tutoriel.py <game_dir> <port>
"""
import json
import os
import sys

os.environ.setdefault("RELEASE", "1")

GAME_DIR = os.path.expanduser(sys.argv[1])
PORT = int(sys.argv[2])

MAIN_ATTENDUE = ["01092", "01065", "01009", "01005", "01061", "01060"]
DECK_ATTENDU = ["01061", "01059", "01058", "01064", "01004"]

CONFIG = os.path.join(GAME_DIR, "launch.json")
CONFIG_ORIGINE = open(CONFIG, encoding="utf-8").read()

os.chdir(GAME_DIR)
sys.path.insert(0, GAME_DIR)

cfg = json.loads(CONFIG_ORIGINE)
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), indent=2)

SORTIE = sys.stdout
sys.stdout = open("/tmp/test_seed_tutoriel_moteur.log", "w", buffering=1)
sys.stderr = sys.stdout

releve = {}

from engine.network.web_server import WebServer
WebServer.IsAuthenticate = lambda self, request=None: True
WebServer.IsVersionMatch = lambda self, request=None: True
from engine.device.manager.base import DeviceManager
DeviceManager.DoWaitConnect = lambda self, p, c: None
DeviceManager.DoWaitSync = lambda self, p, c: None


def pilote(self, data, player_id, check):
    # Des que le moteur demande quoi que ce soit, la mise en place est faite :
    # on releve la main et le dessus du deck, puis on sort.
    if not releve:
        from engine import Engine
        joueur = Engine.game.world.players[0]
        releve["main"] = [getattr(f.paper, "card_id", "?")
                          for f in joueur.hand_cards.GetAll()]
        releve["deck"] = [getattr(f.paper, "card_id", "?")
                          for f in joueur.player_deck.Get()[:5]]
    return json.dumps({"id": "0", "targets": [], "resources": []})


DeviceManager.DoGetInput = pilote

try:
    from engine import Engine
    Engine.Initialize()
    from game.scene.loader import SceneLoader
    scene = SceneLoader.NewScene("rhino", None, ["spider_man"], 42)
    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")
    if jeu.GameSetup():
        jeu.GameLoop()
finally:
    with open(CONFIG, "w", encoding="utf-8") as f:
        f.write(CONFIG_ORIGINE)

soucis = []
if releve.get("main") != MAIN_ATTENDUE:
    soucis.append(f"main = {releve.get('main')} (attendu {MAIN_ATTENDUE})")
if releve.get("deck") != DECK_ATTENDU:
    soucis.append(f"dessus du deck = {releve.get('deck')} (attendu {DECK_ATTENDU})")

for souci in soucis:
    print("ECHEC " + souci, file=SORTIE)
if not soucis:
    print("OK    la partie du tutoriel est inchangee", file=SORTIE)
    print("      main :", releve["main"], file=SORTIE)
print(("\nTOUT PASSE" if not soucis else
       "\nLA PARTIE DU TUTORIEL A CHANGE : relire les lecons de ui-app/src/board/lecons.ts"),
      file=SORTIE)
SORTIE.flush()
os._exit(0 if not soucis else 1)
```

- [ ] **Étape 2 : lancer et vérifier qu'il PASSE**

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 \
    tools/test_seed_tutoriel.py ~/marvel-work/fusion/marvel-lcg-src/.game-src 26200
```
Attendu : `TOUT PASSE`. Ce test décrit l'existant : il doit être vert du premier coup.

- [ ] **Étape 3 : vérifier qu'il sait ÉCHOUER**

Changer temporairement `MAIN_ATTENDUE[0]` en `"99999"`, relancer, constater l'échec, puis remettre `"01092"`. Un garde-fou qui ne peut pas se déclencher ne protège rien.

- [ ] **Étape 4 : recopier**

```bash
rsync -a ~/marvel-work/fusion/marvel-lcg-src/tools/ \
  "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src/tools/"
```

---

### Tâche 2 : les leçons, en module pur

**Fichiers :**
- Créer : `ui-app/src/board/lecons.ts`
- Créer : `ui-app/outils/verifier-lecons.mjs`

**Interfaces :**
- Consomme : le type `World` de `ui-app/src/board/world.ts`.
- Produit :
  - `export type Repere = { pvVilain: number; menacePrincipale: number; pvIdentite: number; round: number; cartesEnMain: string[] }`
  - `export type Lecon = { id: string; titre: string; texte: string; manuelle?: boolean; accomplie: (monde: World, repere: Repere) => boolean }`
  - `export const LECONS: Lecon[]`
  - `export function prendreRepere(monde: World): Repere`

- [ ] **Étape 1 : écrire le vérificateur qui échoue**

Créer `ui-app/outils/verifier-lecons.mjs`. Il compile le module avec tsc (même montage que `verifier-libelles-cible.mjs` : sortie CommonJS dans un dossier local, `package.json` `{"type":"commonjs"}`, jamais `process.exit` dans le `try`) puis vérifie chaque détection sur des mondes fabriqués.

```js
// Vérifie les détections de fin de leçon du mode Découverte.
// Le module lecons.ts est pur : Node peut l'exécuter après compilation.
// Usage : node outils/verifier-lecons.mjs
import { execFileSync } from 'node:child_process'
import { mkdirSync, rmSync, writeFileSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { createRequire } from 'node:module'

const sortie = '.tmp-verif-lecons'
let code = 1

try {
  execFileSync(process.execPath,
    ['node_modules/typescript/bin/tsc', 'src/board/lecons.ts',
      '--outDir', sortie, '--module', 'commonjs', '--target', 'es2022',
      '--moduleResolution', 'bundler', '--skipLibCheck', '--ignoreConfig'],
    { stdio: 'inherit' })
  mkdirSync(sortie, { recursive: true })
  writeFileSync(join(sortie, 'package.json'), '{"type":"commonjs"}')

  const requerir = createRequire(import.meta.url)
  const { LECONS, prendreRepere } = requerir(resolve(sortie, 'lecons.js'))

  let echecs = 0
  const verifier = (nom, obtenu, attendu) => {
    const ok = JSON.stringify(obtenu) === JSON.stringify(attendu)
    if (!ok) echecs += 1
    console.log(`${ok ? 'OK   ' : 'ECHEC'} ${nom}`)
    if (!ok) console.log(`      obtenu ${JSON.stringify(obtenu)} / attendu ${JSON.stringify(attendu)}`)
  }

  /** Monde minimal, ajustable par ce qu'on lui passe. */
  const monde = (o = {}) => ({
    round_id: o.round ?? 1,
    area_schemes_main: [{ info: { k_threat: o.menace ?? 5 } }],
    players: [{
      area_hero: [{ card_type: o.forme ?? 'AlterEgo', info: { health: o.pv ?? 10 } }],
      allies: o.allies ?? [],
      hand_cards: (o.main ?? ['01005', '01060']).map((id) => ({ card_id: id })),
      engaged_enemies: [],
    }],
    area_enemies: [{ card_id: '01095', info: { health: o.pvVilain ?? 14 } }],
  })

  const lecon = (id) => LECONS.find((l) => l.id === id)
  const repere = prendreRepere(monde())

  verifier('les 11 leçons sont là', LECONS.length, 11)
  verifier('toutes ont un identifiant unique',
    new Set(LECONS.map((l) => l.id)).size, LECONS.length)

  verifier('1 changer de forme : pas encore',
    lecon('forme-heros').accomplie(monde({ forme: 'AlterEgo' }), repere), false)
  verifier('1 changer de forme : fait',
    lecon('forme-heros').accomplie(monde({ forme: 'Hero' }), repere), true)

  verifier('2 jouer la carte : encore en main',
    lecon('jouer-carte').accomplie(monde({ main: ['01005', '01060'] }), repere), false)
  verifier('2 jouer la carte : partie de la main',
    lecon('jouer-carte').accomplie(monde({ main: ['01060'] }), repere), true)

  verifier('3 attaquer : le vilain n’a rien perdu',
    lecon('attaquer').accomplie(monde({ pvVilain: 14 }), repere), false)
  verifier('3 attaquer : le vilain a perdu des PV',
    lecon('attaquer').accomplie(monde({ pvVilain: 12 }), repere), true)

  verifier('4 contrer : 1 seule menace retirée',
    lecon('contrer').accomplie(monde({ menace: 4 }), repere), false)
  verifier('4 contrer : 2 menaces retirées',
    lecon('contrer').accomplie(monde({ menace: 3 }), repere), true)

  verifier('5 finir son tour : même round',
    lecon('finir-tour').accomplie(monde({ round: 1 }), repere), false)
  verifier('5 finir son tour : round suivant',
    lecon('finir-tour').accomplie(monde({ round: 2 }), repere), true)

  verifier('6 allié : aucun',
    lecon('allie').accomplie(monde({ allies: [] }), repere), false)
  verifier('6 allié : un en jeu',
    lecon('allie').accomplie(monde({ allies: [{ card_id: '01059' }] }), repere), true)

  verifier('7 récupérer : en héros, PV inchangés',
    lecon('recuperer').accomplie(monde({ forme: 'Hero', pv: 10 }), repere), false)
  verifier('7 récupérer : en alter-ego mais PV inchangés',
    lecon('recuperer').accomplie(monde({ forme: 'AlterEgo', pv: 10 }), repere), false)
  verifier('7 récupérer : en alter-ego et PV remontés',
    lecon('recuperer').accomplie(monde({ forme: 'AlterEgo', pv: 13 }), repere), true)

  verifier('les 4 leçons du plateau sont manuelles',
    LECONS.slice(7).every((l) => l.manuelle === true), true)
  verifier('aucune leçon de jeu n’est manuelle',
    LECONS.slice(0, 7).some((l) => l.manuelle), false)

  console.log(echecs === 0 ? '\nTOUT PASSE' : `\n${echecs} ECHEC(S)`)
  code = echecs === 0 ? 0 : 1
} finally {
  rmSync(sortie, { recursive: true, force: true })
}

process.exit(code)
```

- [ ] **Étape 2 : lancer, vérifier l'échec**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-app" && node outils/verifier-lecons.mjs
```
Attendu : échec de compilation, `lecons.ts` n'existe pas.

- [ ] **Étape 3 : écrire le module**

Créer `ui-app/src/board/lecons.ts`. Points d'attention : les accès à `World` doivent tolérer des zones vides (une partie qui démarre n'a pas encore d'ennemi en jeu), et le vilain se trouve par `card_type === 'Villain'` parmi les cartes de la table, pas à une position fixe.

```ts
// lecons.ts — le contenu du mode Découverte, et rien d'autre.
//
// Module PUR : aucun DOM, aucun React, aucun import de composant. Il se teste
// sous Node (ui-app/outils/verifier-lecons.mjs), comme libelles-cible.ts.
//
// ⚠️ Les leçons nomment des cartes précises parce que la partie est FIGÉE
// (Spider-Man contre Rhino, seed 42). Ce postulat est protégé par
// tools/test_seed_tutoriel.py. Si ce test tombe, les textes d'ici sont à revoir.
//
// Une leçon ne désigne JAMAIS une carte par sa position dans la main : l'ordre
// d'affichage dépend de ce que le joueur a déjà joué.

import { t } from './langue'
import type { World, WorldCard } from './world'

export type Repere = {
  pvVilain: number
  menacePrincipale: number
  pvIdentite: number
  round: number
  cartesEnMain: string[]
}

export type Lecon = {
  id: string
  titre: string
  texte: string
  /** Vrai si la mission ne se détecte pas et s'enchaîne au clic. */
  manuelle?: boolean
  /** Vrai quand la mission est remplie. Lit l'état, ne modifie rien. */
  accomplie: (monde: World, repere: Repere) => boolean
}

const nombre = (v: unknown): number => (typeof v === 'number' ? v : 0)

/** Toutes les cartes de la table, quelles que soient les zones. */
function toutesLesCartes(monde: World): WorldCard[] {
  const cartes: WorldCard[] = []
  const parcourir = (valeur: unknown) => {
    if (Array.isArray(valeur)) { for (const e of valeur) parcourir(e); return }
    if (typeof valeur !== 'object' || valeur === null) return
    const objet = valeur as Record<string, unknown>
    if (typeof objet.card_id === 'string') cartes.push(objet as unknown as WorldCard)
    for (const enfant of Object.values(objet)) parcourir(enfant)
  }
  parcourir(monde)
  return cartes
}

function pvVilain(monde: World): number {
  const villains = toutesLesCartes(monde).filter((c) => c.card_type === 'Villain')
  return villains.length ? nombre(villains[0].info?.health) : 0
}

function identite(monde: World): WorldCard | undefined {
  return monde.players?.[0]?.area_hero?.[0]
}

function menacePrincipale(monde: World): number {
  return nombre(monde.area_schemes_main?.[0]?.info?.k_threat)
}

function mainCartes(monde: World): string[] {
  return (monde.players?.[0]?.hand_cards ?? []).map((c) => c.card_id)
}

export function prendreRepere(monde: World): Repere {
  return {
    pvVilain: pvVilain(monde),
    menacePrincipale: menacePrincipale(monde),
    pvIdentite: nombre(identite(monde)?.info?.health),
    round: nombre(monde.round_id),
    cartesEnMain: mainCartes(monde),
  }
}

export const LECONS: Lecon[] = [
  {
    id: 'forme-heros',
    titre: t('Deviens Spider-Man'),
    texte: t('Tu commences en Peter Parker, ton identité civile. En civil on récupère et on prépare, mais on ne se bat pas. Clique sur ta carte d’identité et change de forme.'),
    accomplie: (m) => identite(m)?.card_type === 'Hero',
  },
  {
    id: 'jouer-carte',
    titre: t('Joue ta première carte'),
    texte: t('Joue « Coup de pied volant ». Pour la payer, tu défausses d’autres cartes de ta main : chaque carte vaut une ressource. Tout se paie comme ça.'),
    accomplie: (m, r) => r.cartesEnMain.includes('01005') && !mainCartes(m).includes('01005'),
  },
  {
    id: 'attaquer',
    titre: t('Frappe Rhino'),
    texte: t('Ton héros peut attaquer une fois par tour. Clique sur Spider-Man, choisis Attaque, puis Rhino. Ta carte s’incline : elle a servi.'),
    accomplie: (m, r) => pvVilain(m) < r.pvVilain,
  },
  {
    id: 'contrer',
    titre: t('Retire 2 menaces'),
    texte: t('La manigance principale monte à chaque tour. Si elle se remplit, la partie est perdue, même si Rhino est en pleine forme. Contre-la pour faire baisser la menace.'),
    accomplie: (m, r) => menacePrincipale(m) <= r.menacePrincipale - 2,
  },
  {
    id: 'finir-tour',
    titre: t('Termine ton tour'),
    texte: t('Regarde bien ce qui suit : Rhino attaque, la manigance monte, et une carte Rencontre t’est distribuée. C’est la phase du méchant.'),
    accomplie: (m, r) => nombre(m.round_id) > r.round,
  },
  {
    id: 'allie',
    titre: t('Appelle un allié'),
    texte: t('Les alliés attaquent et contrent à ta place, sans t’incliner. Ils encaissent un dégât à chaque fois qu’ils agissent : ils sont là pour être dépensés.'),
    accomplie: (m) => (m.players?.[0]?.allies ?? []).length > 0,
  },
  {
    id: 'recuperer',
    titre: t('Reprends ton souffle'),
    texte: t('Repasse en Peter Parker et récupère des points de vie. Tu ne pourras plus attaquer ce tour, mais Rhino ne t’attaquera pas non plus : il ira comploter à la place.'),
    accomplie: (m, r) =>
      identite(m)?.card_type === 'AlterEgo' &&
      nombre(identite(m)?.info?.health) > r.pvIdentite,
  },
  {
    id: 'apercu',
    titre: t('Lis une carte'),
    texte: t('Survole n’importe quelle carte : elle s’agrandit sur le côté, avec ses mots-clés expliqués. Garde, Renfort, Déferlement : tout y est défini.'),
    manuelle: true,
    accomplie: () => false,
  },
  {
    id: 'reglages',
    titre: t('Le panneau ⚙'),
    texte: t('En haut à droite : animations, sons, musique, météo, succès. Tout est débrayable, rien n’est imposé.'),
    manuelle: true,
    accomplie: () => false,
  },
  {
    id: 'annuler',
    titre: t('Annuler une erreur'),
    texte: t('La touche U annule le dernier coup. Tu peux essayer sans crainte : rien n’est définitif tant que tu n’as pas fini ton tour.'),
    manuelle: true,
    accomplie: () => false,
  },
  {
    id: 'historique',
    titre: t('L’historique'),
    texte: t('En bas, tout ce qui s’est passé est rejoué ligne à ligne. Quand tu ne comprends pas pourquoi quelque chose est arrivé, la réponse est là.'),
    manuelle: true,
    accomplie: () => false,
  },
]
```

- [ ] **Étape 4 : relancer, vérifier que tout passe**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-app" && node outils/verifier-lecons.mjs
```
Attendu : 19 lignes OK, `TOUT PASSE`.

- [ ] **Étape 5 : typecheck**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-app" && npm run typecheck
```
Attendu : aucune sortie.

- [ ] **Étape 6 : ajouter `.tmp-verif-lecons/` au `.gitignore` de `ui-app`, puis committer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
printf '.tmp-verif-lecons/\n' >> ui-app/.gitignore
git add ui-app/src/board/lecons.ts ui-app/outils/verifier-lecons.mjs ui-app/.gitignore
git commit -m "feat(tutoriel): les 11 lecons du mode Decouverte, en module pur"
```

---

### Tâche 3 : la couche coach

**Fichiers :**
- Créer : `ui-app/src/board/CoucheCoach.tsx`
- Modifier : `ui-app/src/board.tsx` (import, puis pose de la couche à côté de `<SplashTour monde={etat.monde} />`, ligne ~1747)
- Modifier : `ui-app/src/board/board.css` (styles de la couche)
- Modifier : `ui-app/src/board/dico-en.ts` (chaînes du coach et des 11 leçons)

**Interfaces :**
- Consomme : `LECONS`, `prendreRepere`, les types `Lecon` et `Repere` de `lecons.ts` (tâche 2) ; le type `World`.
- Produit : `export const CLE_TUTORIEL = 'marvel-board-tutoriel'`, `export function lireLeconCourante(): string | null`, `export function CoucheCoach({ monde }: { monde?: World })`.

- [ ] **Étape 1 : écrire la couche**

```tsx
// CoucheCoach — le mode Découverte : une mission à la fois, par-dessus la table.
//
// Ne bloque JAMAIS rien (pointer-events: none sauf sur ses boutons), même règle
// que SplashTour : un panneau qui avale les clics coûte plus cher qu'il ne
// rapporte. Il observe l'état du monde et n'agit sur rien.
//
// Ne s'affiche que si localStorage marvel-board-tutoriel existe et vaut autre
// chose que 'fini'. Une partie normale n'est donc jamais concernée.

import { useEffect, useRef, useState } from 'react'
import { LECONS, prendreRepere, type Repere } from './lecons'
import { t } from './langue'
import type { World } from './world'

export const CLE_TUTORIEL = 'marvel-board-tutoriel'

export function lireLeconCourante(): string | null {
  try {
    return window.localStorage.getItem(CLE_TUTORIEL)
  } catch {
    return null
  }
}

function ecrireLeconCourante(valeur: string): void {
  try {
    window.localStorage.setItem(CLE_TUTORIEL, valeur)
  } catch {
    /* stockage indisponible : le tutoriel reste jouable, sans reprise */
  }
}

export function CoucheCoach({ monde }: { monde?: World }) {
  const [idLecon, setIdLecon] = useState<string | null>(() => lireLeconCourante())
  const [replie, setReplie] = useState(false)
  const [felicite, setFelicite] = useState(false)
  const repere = useRef<Repere | null>(null)

  const index = LECONS.findIndex((l) => l.id === idLecon)
  const lecon = index >= 0 ? LECONS[index] : undefined

  // Le repère est pris À L'ENTRÉE dans la leçon : c'est lui qui permet de
  // mesurer une VARIATION (« Rhino a encore perdu des PV »), impossible à voir
  // sur le seul état courant.
  useEffect(() => {
    if (monde && lecon) repere.current = prendreRepere(monde)
  }, [idLecon, lecon, monde])

  const avancer = () => {
    const suivante = LECONS[index + 1]
    setFelicite(true)
    window.setTimeout(() => setFelicite(false), 1800)
    if (suivante) {
      setIdLecon(suivante.id)
      ecrireLeconCourante(suivante.id)
    } else {
      setIdLecon('fini')
      ecrireLeconCourante('fini')
    }
  }

  useEffect(() => {
    if (!monde || !lecon || lecon.manuelle || !repere.current) return
    if (lecon.accomplie(monde, repere.current)) avancer()
  })

  if (!lecon) return null

  if (replie) {
    return (
      <aside className="coach coach-replie">
        <button type="button" onClick={() => setReplie(false)}>
          {t('Coach')} · {index + 1}/{LECONS.length}
        </button>
      </aside>
    )
  }

  return (
    <aside className="coach" aria-live="polite">
      <span className="coach-eyebrow">
        {t('Leçon')} {index + 1}/{LECONS.length}
      </span>
      <strong>{lecon.titre}</strong>
      <p>{lecon.texte}</p>
      {felicite ? <span className="coach-bravo">{t('Bien joué !')}</span> : null}
      <div className="coach-boutons">
        <button type="button" onClick={() => setReplie(true)}>{t('Replier')}</button>
        <button type="button" onClick={avancer}>
          {lecon.manuelle ? t('J’ai compris') : t('Passer cette leçon')}
        </button>
        <button
          type="button"
          className="coach-quitter"
          onClick={() => { setIdLecon('fini'); ecrireLeconCourante('fini') }}
        >
          {t('Quitter le tutoriel')}
        </button>
      </div>
    </aside>
  )
}
```

- [ ] **Étape 2 : poser la couche dans le plateau**

Dans `ui-app/src/board.tsx`, ajouter l'import à côté des autres couches (ligne ~46) :

```tsx
import { CoucheCoach } from './board/CoucheCoach'
```

et la couche juste après `<SplashTour monde={etat.monde} />` (ligne ~1747) :

```tsx
      <CoucheCoach monde={etat.monde} />
```

- [ ] **Étape 3 : styles**

Ajouter à la fin de `ui-app/src/board/board.css`, à l'intérieur du même bloc de portée que `.assistant-action` :

```css
  /* Coach du mode Découverte. Ne prend jamais le pointeur, sauf ses boutons :
     même règle que SplashTour. */
  .coach {
    position: fixed;
    left: 16px;
    bottom: 16px;
    z-index: 40;
    max-width: 340px;
    display: grid;
    gap: 4px;
    padding: 12px 14px;
    background: rgba(16, 18, 25, 0.94);
    border: 1px solid #2c313c;
    border-left: 3px solid #8ddff2;
    border-radius: 10px;
    pointer-events: none;
  }
  .coach-eyebrow {
    color: #8ddff2;
    font-size: 0.66rem;
    font-weight: 900;
    text-transform: uppercase;
    line-height: 1;
  }
  .coach strong { color: #ffffff; font-size: 1rem; line-height: 1.15; }
  .coach p { margin: 2px 0 0; color: #cbd5e1; font-size: 0.82rem; line-height: 1.35; }
  .coach-bravo { color: #ffd45a; font-weight: 900; font-size: 0.82rem; }
  .coach-boutons { pointer-events: auto; display: flex; gap: 6px; margin-top: 8px; }
  .coach-boutons button {
    font: inherit;
    font-size: 0.74rem;
    font-weight: 800;
    color: #f2f4f8;
    background: #1e2128;
    border: 1px solid #2c313c;
    border-radius: 7px;
    padding: 4px 9px;
    cursor: pointer;
  }
  .coach-boutons .coach-quitter { color: #97a0b0; }
  .coach-replie { padding: 0; border: none; background: none; }
  .coach-replie button {
    pointer-events: auto;
    font: inherit;
    font-size: 0.76rem;
    font-weight: 900;
    color: #0a0c10;
    background: #8ddff2;
    border: none;
    border-radius: 8px;
    padding: 6px 11px;
    cursor: pointer;
  }
```

- [ ] **Étape 4 : traductions**

Ajouter dans `ui-app/src/board/dico-en.ts` les entrées de toutes les chaînes du coach et des 11 leçons. Exemple pour les libellés d'interface ; procéder de même pour chaque `titre` et chaque `texte` de `lecons.ts` :

```ts
  // ---- Mode Découverte (coach) ----
  'Coach': 'Coach',
  'Leçon': 'Lesson',
  'Bien joué !': 'Well done!',
  'Replier': 'Collapse',
  'Passer cette leçon': 'Skip this lesson',
  'J’ai compris': 'Got it',
  'Quitter le tutoriel': 'Quit the tutorial',
  'Deviens Spider-Man': 'Become Spider-Man',
  'Joue ta première carte': 'Play your first card',
  'Frappe Rhino': 'Hit Rhino',
  'Retire 2 menaces': 'Remove 2 threat',
  'Termine ton tour': 'End your turn',
  'Appelle un allié': 'Call an ally',
  'Reprends ton souffle': 'Catch your breath',
  'Lis une carte': 'Read a card',
  'Le panneau ⚙': 'The ⚙ panel',
  'Annuler une erreur': 'Undo a mistake',
  'L’historique': 'The history',
```

- [ ] **Étape 5 : typecheck et build**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-app"
npm run typecheck && npm run build
```
Attendu : aucune erreur.

- [ ] **Étape 6 : vérifier qu'une partie NORMALE n'est pas touchée**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions" && bash ui-app/deployer.sh
```
Puis `JOUER-SOLO.bat`, lancer une partie ordinaire : **aucun coach ne doit apparaître** (la clé `marvel-board-tutoriel` n'existe pas). C'est la vérification la plus importante de cette tâche.

- [ ] **Étape 7 : committer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add ui-app/src/board/CoucheCoach.tsx ui-app/src/board.tsx ui-app/src/board/board.css ui-app/src/board/dico-en.ts
git commit -m "feat(tutoriel): couche coach, une mission a la fois, jamais bloquante"
```

---

### Tâche 4 : le mode Découverte dans le wizard, et la doc

**Fichiers :**
- Modifier : `public/js/prepare/app.js` (tableau `MODES`, ligne ~40 ; démarrage d'une partie Découverte)
- Modifier : `public/js/prepare/launcher.js` (pose de la clé du tutoriel après `/new`, ligne ~133)
- Modifier : `public/js/prepare/dico-en.js`
- Modifier : `MULTIJOUEUR.md` — non. Modifier : `GUIDE-CREATION-CONTENU.md` §13

**Interfaces :**
- Consomme : `CLE_TUTORIEL` = `'marvel-board-tutoriel'` et l'identifiant de la première leçon `'forme-heros'` (tâche 2). Ces deux valeurs sont écrites en dur côté wizard : `public/js/` et `ui-app/` sont deux mondes séparés, sans import possible de l'un vers l'autre.
- Produit : rien.

- [ ] **Étape 1 : ajouter le mode**

Dans `public/js/prepare/app.js`, tableau `MODES` :

```js
    // Mode Decouverte : partie FIGEE (Spider-Man / Rhino / seed 42) doublee d'un
    // coach qui donne une mission a la fois. Les lecons nomment des cartes
    // precises, d'ou le seed impose : voir tools/test_seed_tutoriel.py.
    { id: "decouverte", label: t("Découverte"), desc: t("Apprendre à jouer"), players: 1, fixed: true, mark: "?" },
```

- [ ] **Étape 2 : préremplir et lancer**

Toujours dans `app.js`, au moment où l'on choisit le mode (fonction qui applique un mode au `state`), ajouter le cas :

```js
    // Le mode Decouverte ne passe pas par les 5 etapes : la partie est imposee.
    if (mode.id === "decouverte") {
        state.seed = 42;
        state.premierJoueur = 0;
        const heroes = await catalog.heroes();
        const spiderman = heroes.find((h) => h.id === "spider_man");
        // Les scenarios se listent PAR EXTENSION : catalog.scenarios() n'existe
        // pas. Rhino appartient au Core Set, dont la cle commence par « 1. ».
        const exts = await catalog.extensions();
        const core = exts.find((e) => (e.scenarios || []).includes("rhino"));
        const scs = core ? await catalog.scenariosForExtension(core.key) : [];
        const rhino = scs.find((sc) => sc.id === "rhino");
        if (spiderman && rhino) {
            assignHero(0, spiderman);
            selectScenario(rhino);
            state.step = LAST_STEP;
        }
    }
```

- [ ] **Étape 3 : poser la clé du tutoriel au lancement**

Dans `public/js/prepare/launcher.js`, à côté du cas `sandbox` :

```js
    // Mode Decouverte : on arme le coach du plateau. La cle est lue par
    // ui-app/src/board/CoucheCoach.tsx (CLE_TUTORIEL). Les deux valeurs sont
    // ecrites en dur de part et d'autre : public/js/ et ui-app/ sont deux
    // mondes separes, aucun import n'est possible entre eux.
    if (state.mode && state.mode.id === "decouverte") {
        try {
            window.localStorage.setItem("marvel-board-tutoriel", "forme-heros");
        } catch (e) { /* stockage indisponible : le coach ne s'armera pas */ }
    }
```

- [ ] **Étape 4 : traductions du wizard**

Dans `public/js/prepare/dico-en.js` :

```js
    "Découverte": "Learn to play",
    "Apprendre à jouer": "Learn the game",
```

- [ ] **Étape 5 : vérifier**

```bash
cd ~/marvel-work/fusion/marvel-lcg-src && node --check public/js/prepare/app.js && node --check public/js/prepare/launcher.js && node --check public/js/prepare/dico-en.js
```
Puis `JOUER-SOLO.bat` : le mode Découverte doit apparaître dans la bande des modes, un clic doit amener directement à l'étape finale avec Spider-Man et Rhino déjà choisis, et le lancement doit ouvrir le plateau **avec le coach sur la leçon 1**.

- [ ] **Étape 6 : consigner au guide**

Dans `GUIDE-CREATION-CONTENU.md` §13 :

```markdown
- **Mode Découverte** : partie FIGÉE (Spider-Man / Rhino / seed 42) doublée d'un
  coach qui donne une mission à la fois (`ui-app/src/board/CoucheCoach.tsx`,
  contenu dans `lecons.ts`, clé localStorage `marvel-board-tutoriel`). Les
  leçons NOMMENT des cartes précises : ce postulat est protégé par
  `tools/test_seed_tutoriel.py`, à relancer après toute mise à jour du moteur.
  Si ce test tombe, les textes des leçons sont à revoir. Ne jamais désigner une
  carte par sa position dans la main : l'ordre d'affichage varie.
```

- [ ] **Étape 7 : recopier, déployer, committer**

```bash
S=~/marvel-work/fusion/marvel-lcg-src
M="/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
rsync -a "$S/public/" "$M/public/"
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add GUIDE-CREATION-CONTENU.md 2>/dev/null || true
git commit -m "feat(tutoriel): mode Decouverte dans la preparation de partie"
```

⚠️ `GUIDE-CREATION-CONTENU.md` et tout `Fusion/` sont **hors versionnement** dans ce dépôt : le commit ne portera que sur ce qui est suivi. Ne pas ajouter le moteur à git au passage.

---

## Auto-relecture du plan

**Couverture de la spec** — §5.1 `lecons.ts` → tâche 2 ; §5.2 `CoucheCoach` → tâche 3 ; §5.3 mode du wizard → tâche 4 ; §6 les 11 leçons → tâche 2 étape 3 ; §7 mémorisation localStorage → tâche 3 étape 1 ; §9 test 1 (module pur) → tâche 2, test 2 (déterminisme) → tâche 1, test 3 (bout en bout) → tâches 3 étape 6 et 4 étape 5.

**Cas limites de la spec §8** — « leçon faite en avance » : la détection est évaluée à chaque rendu, donc validée dès qu'on entre dans la leçon (couvert par le `useEffect` sans tableau de dépendances de la tâche 3). « Leçon devenue impossible » : le bouton **Passer cette leçon** est présent sur toutes les leçons non manuelles. « Partie perdue ou gagnée en cours de tutoriel » : non traité par du code — le joueur garde ses boutons Passer et Quitter, ce qui suffit ; à revoir si l'usage montre le contraire.

**Cohérence des types** — `Repere` et `Lecon` sont définis en tâche 2 et consommés sous ces noms exacts en tâche 3. `prendreRepere(monde)` rend un `Repere`, passé en second argument d'`accomplie`. `CLE_TUTORIEL` vaut `'marvel-board-tutoriel'` en tâche 3 comme en tâche 4, et la première leçon a l'identifiant `'forme-heros'` dans les deux.

**Vérification faite pendant la rédaction** — `catalog.scenarios()` **n'existe pas** : `catalog.js` n'expose que `extensions()` et `scenariosForExtension(cle)`. Le code de la tâche 4 étape 2 a été corrigé en conséquence. Le scénario porte bien l'identifiant `"rhino"` (`data/scenarios/rhino.json`, avec une variante `rhino_expert.json` à ne pas prendre).
