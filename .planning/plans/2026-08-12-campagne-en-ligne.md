# Campagne en ligne à plusieurs — plan d'implémentation

> **Pour les agents :** SOUS-SKILL REQUIS — utiliser `superpowers:subagent-driven-development` (recommandé) ou `superpowers:executing-plans` pour dérouler ce plan tâche par tâche. Les étapes utilisent la syntaxe case à cocher (`- [ ]`).

**Objectif :** mener une campagne à plusieurs, chacun sur son appareil, du lancement d'un scénario à la validation des récompenses et à l'enchaînement du suivant.

**Architecture :** la campagne vit déjà côté serveur, entièrement. Ce chantier ajoute UNE route de lecture (« quelle campagne joue-t-on ? »), UNE route d'écriture étroite (« voici mes champs du carnet »), et adapte trois écrans. Le moteur de jeu n'est pas touché : tout se passe dans le serveur web, le plateau React et le salon.

**Stack :** Python 3.10 (aiohttp) pour `src/engine/device/web/server/`, JavaScript ES modules sans framework pour `public/js/`, React 19 + TypeScript strict pour `ui-app/`.

**Spec :** `.planning/todos/2026-08-12-campagne-en-ligne.md`

---

## Ce que la mesure a corrigé dans la spec

La fiche a été relue contre le code le 12/8/2026, après le chantier du rapport de bug. **Son affirmation centrale est fausse**, et deux de ses inquiétudes sont sans objet.

### 1. « Le blocage est là et nulle part ailleurs » : faux

La fiche désigne la clé `localStorage` comme seul obstacle. Il y en a un second, en amont, et plus dur.

- **L'écran des campagnes lance la partie tout seul, sans jamais passer par le salon.** `public/js/campagne/app.js:851` compose `joueurs` depuis `campagne.equipe`, pose la clé, appelle `launch()`. Les mots « salon », « multi » et « en ligne » n'apparaissent nulle part dans ce fichier.
- **Le salon est réservé au hot-seat.** `public/js/prepare/app.js:707` : `if (!state.salon.multi || state.mode.id !== "hotseat") return null`. La campagne lance avec `mode: { id: "campaign" }`. L'écran de préparation le dit lui-même en commentaire ligne 474 : « Cet écran ne lance donc jamais de partie de campagne. »

**Conséquence : aujourd'hui une campagne est toujours hot-seat.** Les distants n'ont pas « un plateau qui ignore la campagne » : rien ne les convoque. Le salon poll `get_play_scene_name` toutes les 2 s et basculerait les invités présents vers `/app/board.html?p=N` (`public/js/salon/app.js:136`), mais il leur aura d'abord demandé de choisir un héros, ce qui n'a aucun sens quand l'équipe est figée par le livret. **Non mesuré en vraie partie** : à confirmer au jalon E.

### 2. « `lireContexte()` est synchrone et devient asynchrone » : vrai, mais sans douleur

La fiche redoutait ce point. `lireContexte()` n'a que **deux** consommateurs : `PanneauRecompenses.tsx:102` et `RapportBug.tsx:44` (ajouté le 12/8). Les deux sont déjà dans un contexte où l'attente est possible.

### 3. « Le panneau s'ouvre-t-il chez tout le monde ? » : il s'ouvre déjà

`PanneauRecompenses` est monté **sans aucune condition de siège** (`ui-app/src/board.tsx:1384`), sur l'écran de fin de partie. Sa seule garde est `lireContexte()`, qui rend `null` chez les distants. **Dès que le contexte atteint tous les sièges, le panneau s'ouvre chez tout le monde sans autre travail.** Le « direct » de la question §4.3 est donc gratuit ; c'est l'attente qui coûterait du code. Décision : direct.

### 4. `parJoueur` est déjà pleinement câblé côté UI

La fiche le présente comme un attribut « qui existe déjà dans les définitions ». Il fait plus que cela : `cleCarnet(champ, joueurId)` (`detecteurs.ts:485`) préfixe en `Player N <clé>`, et le panneau affiche déjà **une ligne par joueur** pour ces champs (`PanneauRecompenses.tsx:412-427`). Il ne reste qu'à décider qui a le droit d'y écrire.

## Décisions arrêtées avec l'utilisateur

| Question | Décision | Date |
|---|---|---|
| Où vit la campagne | Côté serveur, partagée. C'est déjà le cas | 12/8 |
| Qui remplit le carnet | Chacun ses champs, l'hôte valide | 12/8 |
| Répartition des sièges | **Par ordre, sans écran** : le siège N tient `equipe[N]`. C'est déjà ce que fait le moteur (`launch({players: joueurs})` donne `players[0]` au siège 0) : rien à écrire pour l'assignation | 12/8 |
| Le panneau chez les distants | **En direct**, puisque c'est gratuit (voir §3 ci-dessus) | 12/8 |
| Le localStorage | **Gardé comme raccourci**, la route sert de recours. Une seule voie serait plus propre, mais l'hôte n'a alors plus rien qui marche hors ligne, et la clé est déjà écrite | 12/8 |

## Contraintes globales

- **Le moteur de jeu ne change pas.** Rien sous `src/game/`. Ce chantier touche `src/engine/device/web/server/`, `public/js/`, `ui-app/`.
- **Trois arborescences, trois sens de copie.** Ne pas s'y tromper coûte un cycle entier :
  - `src/`, `data/`, `tools/` : **le dépôt est la source**. Copier à la main vers `~/marvel-work/fusion/marvel-lcg-src/`, puis `launcher_fast.py --build-only`, puis **redémarrer le serveur de dev** (le bytecode n'est relu qu'au démarrage).
  - `public/js`, `public/css` : **`~/marvel-work/fusion/marvel-lcg-src` est la RÉFÉRENCE.** On y édite, puis `bash ui-app/deployer.sh` propage vers le dépôt. Éditer la copie du dépôt puis déployer efface l'édition, en silence.
  - `ui-app/` : le dépôt est la source, `bash ui-app/deployer.sh` déploie.
- **Les fins de ligne sont mélangées** dans les fichiers du jeu : lire ET écrire avec `newline=''` en Python.
- **`verifier_campagnes.py` et `verifier_grille_aos.py` doivent rester verts** après toute touche aux définitions ou au panneau.
- **TypeScript strict, zéro `any`.** Toute chaîne visible passe par `t()` avec son entrée dans `dico-en.ts` (plateau) ou `public/js/prepare/dico-en.js` (salon et wizard).
- **Pas d'em dash (—) ni de tiret parenthétique** dans les textes visibles ni dans les commentaires.
- **Avant chaque commit** : `cd ui-app && npx vitest run && npx tsc --noEmit`, et les vérificateurs Python concernés. Ne jamais annoncer un test vert sans l'avoir lancé.
- **Le secret d'A.I.M. ne sort jamais.** Toute réponse de route passe par `_sans_secret()`. Une route neuve qui l'oublie ouvre l'enveloppe devant les joueurs.
- **`~/marvel-work/python/bin/python3.10`** est l'interpréteur du projet, avec `RELEASE=1` pour tout ce qui touche au moteur.

---

## Jalon A : le contexte de campagne atteint tous les sièges

À la fin de ce jalon, un joueur distant qui termine un scénario voit le panneau de récompenses. C'est le jalon qui rend tout le reste observable.

### Tâche 1 : la route qui dit quelle campagne on joue

Le serveur sait déjà le déduire : `secret_pour_le_moteur()` retrouve la campagne par la `partieEnCours` la plus récente, précisément parce que le client n'envoie pas l'identifiant dans `/new` (contrat gelé). On factorise cette déduction et on l'expose.

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py`
- Créer : `Fusion/marvel-lcg-src/tools/test_campagne_en_cours.py`

**Interfaces :**
- Consomme : `CAMPAGNES_FOLDER`, `CLE_SECRET`, `CLE_CARNET_SECRET`, `_sans_secret` (déjà dans le fichier).
- Produit : `_campagne_la_plus_recente() -> 'Optional[Dict[str, Any]]'` (le dict complet, secret compris, usage interne) et la route `GET /get_campagne_en_cours` qui rend `{"id": str, "scenario": str}` ou `{}`.

- [x] **Étape 1 : écrire le test**

Créer `Fusion/marvel-lcg-src/tools/test_campagne_en_cours.py` :

```python
"""La deduction « quelle campagne joue-t-on ? », eprouvee sur des fichiers.

Elle existait deja, enfouie dans secret_pour_le_moteur() : la campagne dont
`partieEnCours.depuis` est la plus recente. Ce test la verrouille AVANT de
l'extraire, pour qu'une extraction ratee se voie.

Lancer : ~/marvel-work/python/bin/python3.10 tools/test_campagne_en_cours.py
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
os.environ.setdefault('RELEASE', '1')

from engine.device.web.server import server_campagne


def ecrire(dossier, nom, campagne):
    with open(os.path.join(dossier, nom + '.json'), 'w', encoding='utf-8', newline='') as f:
        json.dump(campagne, f)


def cas(nom, obtenu, attendu):
    if obtenu == attendu:
        print('  ok   %s' % nom)
        return 0
    print('  ECHEC %s : attendu %r, obtenu %r' % (nom, attendu, obtenu))
    return 1


def main():
    echecs = 0
    with tempfile.TemporaryDirectory() as dossier:
        server_campagne.CAMPAGNES_FOLDER.value = dossier

        echecs += cas('dossier vide', server_campagne._campagne_la_plus_recente(), None)

        ecrire(dossier, 'ancienne', {
            'code': 'trors', 'nom': 'Ancienne',
            'partieEnCours': {'scenario': 'crossbones', 'depuis': '2026-08-01T10:00:00'},
        })
        ecrire(dossier, 'recente', {
            'code': 'sm', 'nom': 'Recente',
            'partieEnCours': {'scenario': 'sandman', 'depuis': '2026-08-12T21:00:00'},
        })
        # Sans partie en cours : ne doit jamais l'emporter, meme ecrite en dernier.
        ecrire(dossier, 'au_repos', {'code': 'aoa', 'nom': 'Au repos', 'partieEnCours': None})

        trouvee = server_campagne._campagne_la_plus_recente()
        echecs += cas('la plus recente gagne', trouvee and trouvee.get('id'), 'recente')
        echecs += cas('le scenario suit', trouvee and trouvee['partieEnCours']['scenario'], 'sandman')

        # Une campagne au repos SEULE ne designe rien : la partie en cours n'est
        # pas une campagne, et pretendre le contraire ferait s'ouvrir le panneau
        # de recompenses sur une partie ordinaire.
        os.remove(os.path.join(dossier, 'recente.json'))
        os.remove(os.path.join(dossier, 'ancienne.json'))
        echecs += cas('au repos ne designe rien', server_campagne._campagne_la_plus_recente(), None)

        # Un fichier illisible ne doit pas faire tomber la deduction.
        with open(os.path.join(dossier, 'casse.json'), 'w', encoding='utf-8', newline='') as f:
            f.write('{ pas du json')
        ecrire(dossier, 'valide', {
            'code': 'sm', 'nom': 'Valide',
            'partieEnCours': {'scenario': 'venom', 'depuis': '2026-08-12T22:00:00'},
        })
        trouvee = server_campagne._campagne_la_plus_recente()
        echecs += cas('un fichier casse est saute', trouvee and trouvee.get('id'), 'valide')

    print('ECHECS : %d' % echecs)
    return 1 if echecs else 0


if __name__ == '__main__':
    sys.exit(main())
```

- [x] **Étape 2 : lancer le test, vérifier qu'il échoue**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 tools/test_campagne_en_cours.py
```

Attendu : ROUGE, `AttributeError: module ... has no attribute '_campagne_la_plus_recente'`.

- [x] **Étape 3 : extraire la déduction**

Dans `server_campagne.py`, juste AVANT `def secret_pour_le_moteur()`, ajouter :

```python
def _campagne_la_plus_recente() -> 'Optional[Dict[str, Any]]':
    """La campagne dont une partie a ete lancee en dernier, ou None.

    Le client n'envoie pas l'identifiant de campagne dans le descripteur de
    `/new` : ce contrat est gele. Mais l'ecran des campagnes ecrit
    `partieEnCours` AVANT de lancer. La campagne concernee est donc celle dont
    la partie en cours est la plus recente, et c'est vrai pour tous les sieges :
    la deduction ne depend d'aucun navigateur.

    Rend le dict COMPLET, secret compris. Tout appelant qui repond a une route
    doit le passer par `_sans_secret()`.
    """
    import json as json_lib
    import os

    dossier = CAMPAGNES_FOLDER.value
    if not os.path.isdir(dossier):
        return None
    meilleure = None
    for nom in os.listdir(dossier):
        if not nom.endswith('.json'):
            continue
        try:
            with open(os.path.join(dossier, nom), encoding='utf-8', newline='') as f:
                campagne = json_lib.load(f)
        except Exception:
            # Un fichier illisible ne doit pas faire tomber la deduction pour
            # les autres : la campagne d'a cote reste jouable.
            continue
        en_cours = campagne.get('partieEnCours') or {}
        if not en_cours.get('depuis'):
            continue
        campagne['id'] = nom[:-5]
        if (meilleure is None) or (en_cours['depuis'] > meilleure['partieEnCours']['depuis']):
            meilleure = campagne
    return meilleure
```

Vérifier que `Optional` est importé en tête du fichier ; sinon l'ajouter à l'import `typing` existant.

- [x] **Étape 4 : faire passer `secret_pour_le_moteur()` par la déduction extraite**

Remplacer tout le corps de `secret_pour_le_moteur()` (en gardant sa docstring) par :

```python
    campagne = _campagne_la_plus_recente()
    secret = (campagne or {}).get(CLE_SECRET)
    return {CLE_CARNET_SECRET: secret} if secret else {}
```

- [x] **Étape 5 : relancer le test**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 tools/test_campagne_en_cours.py
```

Attendu : `ECHECS : 0`.

- [x] **Étape 6 : exposer la route**

Dans la classe du serveur, à côté de `get_campagne`, ajouter :

```python
    async def get_campagne_en_cours(self, request: web.Request) -> web.Response:
        """La campagne a laquelle appartient la partie en cours, pour TOUS.

        Un joueur qui rejoint n'a jamais pose la cle `mc-campagne-partie` dans
        son navigateur : c'est l'ecran des campagnes qui l'ecrit, et il ne
        l'ouvre pas. Sans cette route, son plateau ignore la campagne, donc pas
        de panneau de recompenses, pas de regle de defaite, pas de carnet.

        On ne rend que l'identifiant et le scenario : le carnet se lit par
        `/get_campagne`, qui filtre deja le secret.
        """
        campagne = _campagne_la_plus_recente()
        if not campagne:
            return web.json_response({})
        return web.json_response({
            'id': campagne.get('id', ''),
            'scenario': (campagne.get('partieEnCours') or {}).get('scenario', ''),
        })
```

Et dans `__init__`, à côté des autres :

```python
        self.AddAwaitGetSecurity('/get_campagne_en_cours', self.get_campagne_en_cours)
```

- [x] **Étape 7 : vérifier que rien n'a bougé côté campagnes**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 tools/test_campagne_en_cours.py
~/marvel-work/python/bin/python3.10 tools/verifier_campagnes.py
~/marvel-work/python/bin/python3.10 tools/verifier_grille_aos.py
```

Attendu : les trois verts. `secret_pour_le_moteur()` vient d'être réécrit : si `verifier_grille_aos.py` rougit, c'est là qu'il faut chercher.

- [x] **Étape 8 : porter vers l'arborescence vivante et commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
cp Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py \
   ~/marvel-work/fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py
cp Fusion/marvel-lcg-src/tools/test_campagne_en_cours.py \
   ~/marvel-work/fusion/marvel-lcg-src/tools/test_campagne_en_cours.py
git add Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py \
        Fusion/marvel-lcg-src/tools/test_campagne_en_cours.py
git commit -m "feat(campagne): une route dit a tous les sieges quelle campagne on joue"
```

---

### Tâche 2 : le plateau interroge la route quand le localStorage est muet

**Fichiers :**
- Modifier : `ui-app/src/board/campagne/contexte.ts`
- Modifier : `ui-app/src/board/campagne/PanneauRecompenses.tsx:102`
- Modifier : `ui-app/src/board/RapportBug.tsx:44`
- Créer : `ui-app/src/board/campagne/contexte.test.ts`

**Interfaces :**
- Consomme : `GET /get_campagne_en_cours` (tâche 1).
- Produit : `lireContexte(): ContexteCampagne | null` **reste inchangée** (lecture locale seule), et `resoudreContexte(): Promise<ContexteCampagne | null>` s'y ajoute : localStorage d'abord, route ensuite. Garder les deux évite de rendre asynchrone le rapport de bug, qui se prend au clic et n'a pas à attendre le réseau.

- [x] **Étape 1 : écrire le test**

Créer `ui-app/src/board/campagne/contexte.test.ts` :

```ts
// Un joueur qui REJOINT n'a jamais posé la clé `mc-campagne-partie` : c'est
// l'écran des campagnes qui l'écrit, et il ne l'ouvre pas. Son plateau doit
// donc demander au serveur, qui le déduit de la partie en cours.
//
// Le localStorage reste prioritaire : l'hôte l'a, il est juste, et il évite un
// aller-retour réseau à chaque fin de partie.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CLE_CAMPAGNE, lireContexte, resoudreContexte } from './contexte'

beforeEach(() => window.localStorage.clear())
afterEach(() => vi.unstubAllGlobals())

function serveurRend(charge: unknown, ok = true) {
  const fetchFeint = vi.fn().mockResolvedValue({
    ok,
    json: async () => charge,
  })
  vi.stubGlobal('fetch', fetchFeint)
  return fetchFeint
}

describe('le contexte de campagne', () => {
  it('préfère le localStorage et ne touche pas au réseau', async () => {
    const fetchFeint = serveurRend({ id: 'autre', scenario: 'autre' })
    window.localStorage.setItem(CLE_CAMPAGNE, JSON.stringify({ id: 'trors-1', scenario: 'crossbones' }))

    expect(await resoudreContexte()).toEqual({ id: 'trors-1', scenario: 'crossbones' })
    expect(fetchFeint).not.toHaveBeenCalled()
  })

  it('interroge le serveur quand la clé est absente', async () => {
    serveurRend({ id: 'trors-1', scenario: 'crossbones' })
    expect(await resoudreContexte()).toEqual({ id: 'trors-1', scenario: 'crossbones' })
  })

  it("rend null quand le serveur dit qu'aucune campagne n'est en cours", async () => {
    serveurRend({})
    expect(await resoudreContexte()).toBeNull()
  })

  it('rend null quand le serveur est injoignable', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('coupé')))
    expect(await resoudreContexte()).toBeNull()
  })

  it('rend null sur une réponse incomplète', async () => {
    serveurRend({ id: 'trors-1' })
    expect(await resoudreContexte()).toBeNull()
  })

  it('laisse lireContexte purement locale', () => {
    serveurRend({ id: 'trors-1', scenario: 'crossbones' })
    expect(lireContexte()).toBeNull()
  })
})
```

- [x] **Étape 2 : lancer le test, vérifier qu'il échoue**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-app"
npx vitest run src/board/campagne/contexte.test.ts
```

Attendu : ROUGE, `resoudreContexte is not a function`.

- [x] **Étape 3 : écrire `resoudreContexte`**

Dans `ui-app/src/board/campagne/contexte.ts`, juste après `lireContexte`, ajouter :

```ts
/**
 * Le contexte de campagne, d'où qu'il vienne.
 *
 * Le localStorage d'abord : l'hôte l'a posé avant de lancer, il est juste, et
 * il évite un aller-retour à chaque fin de partie. Le serveur ensuite, pour
 * TOUS les autres sièges, qui n'ont jamais ouvert l'écran des campagnes et
 * n'ont donc aucune clé. Sans ce recours, leur plateau ignore la campagne :
 * pas de panneau de récompenses, pas de règle de défaite, pas de carnet.
 */
export async function resoudreContexte(): Promise<ContexteCampagne | null> {
  const local = lireContexte()
  if (local) return local
  try {
    const reponse = await fetch('/get_campagne_en_cours', { cache: 'no-store' })
    if (!reponse.ok) return null
    const valeur = (await reponse.json()) as Partial<ContexteCampagne>
    if (!valeur?.id || !valeur.scenario) return null
    return { id: valeur.id, scenario: valeur.scenario }
  } catch {
    // Serveur injoignable : mieux vaut un plateau sans campagne qu'un plateau
    // qui refuse de s'afficher.
    return null
  }
}
```

- [x] **Étape 4 : brancher le panneau de récompenses**

Dans `PanneauRecompenses.tsx`, remplacer l'import `lireContexte` par `resoudreContexte`, puis dans l'effet (ligne 102) :

```tsx
    let annule = false
    ;(async () => {
      try {
        const contexte = await resoudreContexte()
        if (annule) return
        if (!contexte || !monde) {
          setEtat({ phase: 'absent' })
          return
        }
        const campagne = await chargerCampagne(contexte.id)
```

Le `if (!contexte || !monde)` qui précédait l'`async` disparaît : il est remonté à l'intérieur. Vérifier que le `return` anticipé qui posait `phase: 'absent'` avant la fonction asynchrone a bien été retiré, sinon le panneau reste « absent » chez les distants quoi qu'il arrive.

- [x] **Étape 5 : laisser le rapport de bug tranquille**

`RapportBug.tsx:44` garde `lireContexte()`. Ajouter au-dessus de `contexteCampagne()` :

```ts
// Lecture LOCALE seulement, à dessein : le rapport se prend au clic et ne doit
// pas attendre le réseau. Chez un siège distant, la ligne « campagne » manquera
// au rapport ; c'est un moindre mal comparé à un bouton qui rame.
```

- [x] **Étape 6 : relancer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-app"
npx vitest run && npx tsc --noEmit
```

Attendu : VERT, avec plus de cas qu'avant (408 + 6).

- [x] **Étape 7 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add ui-app/src/board/campagne/contexte.ts ui-app/src/board/campagne/contexte.test.ts \
        ui-app/src/board/campagne/PanneauRecompenses.tsx ui-app/src/board/RapportBug.tsx
git commit -m "feat(campagne): le plateau demande au serveur quand il n'a pas la cle"
```

---

## Jalon B : chacun ses champs, l'hôte valide

À la fin de ce jalon, un distant remplit ses champs personnels, l'hôte les voit arriver et valide pour tous.

### Tâche 3 : une route étroite pour écrire SES champs du carnet

**`/save_campagne` ne change pas.** Il écrit la campagne entière, il est le seul à poser `termines`, `perdue` et `partieEnCours`, et c'est très bien ainsi : un siège distant ne doit pas pouvoir déclarer la campagne gagnée. On ajoute une route qui ne sait faire qu'une chose.

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py`
- Créer : `Fusion/marvel-lcg-src/tools/test_carnet_partiel.py`

**Interfaces :**
- Consomme : `_campagne_la_plus_recente` (tâche 1), `ecrire_json` (`engine.ecriture_atomique`), `_sans_secret`.
- Produit : `POST /save_carnet_partiel` avec `{"id": str, "champs": {clé: valeur}}`, qui FUSIONNE dans `campagne['carnet']` et rend `{"result": "merged", "carnet": {...}}`.

- [x] **Étape 1 : écrire le test**

Créer `Fusion/marvel-lcg-src/tools/test_carnet_partiel.py` :

```python
"""L'ecriture partielle du carnet : chacun ses champs, sans s'ecraser.

`/save_campagne` remplace la campagne ENTIERE. Deux joueurs qui valident en
meme temps se perdent l'un l'autre, en silence. Cette route-ci ne sait que
fusionner des cles de carnet, et rien d'autre : elle ne peut ni terminer un
scenario, ni gagner une campagne, ni toucher au secret.

Lancer : ~/marvel-work/python/bin/python3.10 tools/test_carnet_partiel.py
"""
import asyncio
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
os.environ.setdefault('RELEASE', '1')

from engine.device.web.server import server_campagne


class RequeteFeinte:
    def __init__(self, charge):
        self._charge = charge

    async def json(self):
        return self._charge


def lire(dossier, nom):
    with open(os.path.join(dossier, nom + '.json'), encoding='utf-8', newline='') as f:
        return json.load(f)


def ecrire(dossier, nom, campagne):
    with open(os.path.join(dossier, nom + '.json'), 'w', encoding='utf-8', newline='') as f:
        json.dump(campagne, f)


def cas(nom, obtenu, attendu):
    if obtenu == attendu:
        print('  ok   %s' % nom)
        return 0
    print('  ECHEC %s : attendu %r, obtenu %r' % (nom, attendu, obtenu))
    return 1


def main():
    echecs = 0
    serveur = server_campagne.ServeurCampagne.__new__(server_campagne.ServeurCampagne)
    boucle = asyncio.new_event_loop()

    with tempfile.TemporaryDirectory() as dossier:
        server_campagne.CAMPAGNES_FOLDER.value = dossier
        ecrire(dossier, 'ma_campagne', {
            'code': 'trors', 'nom': 'Ma campagne', 'id': 'ma_campagne',
            'termines': ['crossbones'],
            'carnet': {'Player 1 Upgrade': 'A'},
            server_campagne.CLE_SECRET: 'preuve-secrete',
        })

        # Le joueur 2 ecrit SON champ. Celui du joueur 1 doit survivre.
        boucle.run_until_complete(serveur.save_carnet_partiel(RequeteFeinte({
            'id': 'ma_campagne', 'champs': {'Player 2 Upgrade': 'B'},
        })))
        apres = lire(dossier, 'ma_campagne')
        echecs += cas('le champ du joueur 2 est ecrit', apres['carnet'].get('Player 2 Upgrade'), 'B')
        echecs += cas('celui du joueur 1 survit', apres['carnet'].get('Player 1 Upgrade'), 'A')

        # Rien d'autre que le carnet ne bouge, meme si le client l'envoie.
        boucle.run_until_complete(serveur.save_carnet_partiel(RequeteFeinte({
            'id': 'ma_campagne',
            'champs': {'Player 3 Upgrade': 'C'},
            'termines': ['crossbones', 'absorbing_man'],
            'perdue': True,
        })))
        apres = lire(dossier, 'ma_campagne')
        echecs += cas('termines intact', apres.get('termines'), ['crossbones'])
        echecs += cas('perdue non pose', apres.get('perdue'), None)
        echecs += cas('le secret survit', apres.get(server_campagne.CLE_SECRET), 'preuve-secrete')

        # Une reponse ne montre JAMAIS le secret.
        reponse = boucle.run_until_complete(serveur.save_carnet_partiel(RequeteFeinte({
            'id': 'ma_campagne', 'champs': {'Player 4 Upgrade': 'D'},
        })))
        corps = json.loads(reponse.body.decode('utf-8'))
        echecs += cas('le secret ne sort pas', server_campagne.CLE_SECRET in json.dumps(corps), False)

        # Une campagne inconnue est refusee, sans creer de fichier.
        reponse = boucle.run_until_complete(serveur.save_carnet_partiel(RequeteFeinte({
            'id': 'inconnue', 'champs': {'X': '1'},
        })))
        echecs += cas('campagne inconnue -> 404', reponse.status, 404)
        echecs += cas('aucun fichier cree', os.path.exists(os.path.join(dossier, 'inconnue.json')), False)

        # Des champs qui ne sont pas des chaines sont refuses : le carnet est
        # un dict de chaines, et le moteur le lit tel quel.
        reponse = boucle.run_until_complete(serveur.save_carnet_partiel(RequeteFeinte({
            'id': 'ma_campagne', 'champs': {'X': {'imbrique': 1}},
        })))
        echecs += cas('champ non-chaine -> 400', reponse.status, 400)

    boucle.close()
    print('ECHECS : %d' % echecs)
    return 1 if echecs else 0


if __name__ == '__main__':
    sys.exit(main())
```

**Avant d'écrire l'implémentation**, relever le vrai nom de la classe du serveur de campagne (le test suppose `ServeurCampagne`) :

```bash
grep -n "^class" "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py"
```

Corriger le test si le nom diffère.

- [x] **Étape 2 : lancer le test, vérifier qu'il échoue**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 tools/test_carnet_partiel.py
```

Attendu : ROUGE, `AttributeError: ... has no attribute 'save_carnet_partiel'`.

- [x] **Étape 3 : écrire la route**

Dans la classe, après `save_campagne` :

```python
    async def save_carnet_partiel(self, request: web.Request) -> web.Response:
        """Fusionne des cles de carnet, et RIEN d'autre.

        `/save_campagne` remplace la campagne entiere : deux joueurs qui
        valident se perdent l'un l'autre, en silence. Cette route-ci est
        deliberement etroite. Elle ne peut ni terminer un scenario, ni gagner
        une campagne, ni approcher le secret : un siege distant n'a aucune
        raison de pouvoir faire ces trois choses, et le lui interdire ici coute
        moins cher que de le verifier partout ailleurs.
        """
        import json as json_lib
        import os

        donnees = await request.json()
        identifiant = _nom_de_fichier(donnees.get('id') or '')
        champs = donnees.get('champs')
        if not isinstance(champs, dict):
            return web.json_response({'error': 'champs invalides'}, status=400)
        for cle, valeur in champs.items():
            if not isinstance(cle, str) or not isinstance(valeur, str):
                return web.json_response({'error': 'le carnet ne porte que des chaines'}, status=400)

        chemin = os.path.join(CAMPAGNES_FOLDER.value, '%s.json' % identifiant)
        if not os.path.isfile(chemin):
            return web.json_response({'error': 'campagne introuvable : %s' % identifiant}, status=404)
        with open(chemin, encoding='utf-8', newline='') as f:
            campagne = json_lib.load(f)

        carnet = dict(campagne.get('carnet') or {})
        carnet.update(champs)
        campagne['carnet'] = carnet

        from engine.ecriture_atomique import ecrire_json
        ecrire_json(chemin, campagne)
        return web.json_response({'result': 'merged', 'carnet': carnet})
```

Et dans `__init__` :

```python
        self.AddPostSecurity('/save_carnet_partiel', self.save_carnet_partiel)
```

- [x] **Étape 4 : relancer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/Fusion/marvel-lcg-src"
~/marvel-work/python/bin/python3.10 tools/test_carnet_partiel.py
~/marvel-work/python/bin/python3.10 tools/test_campagne_en_cours.py
~/marvel-work/python/bin/python3.10 tools/test_ecriture_atomique.py
```

Attendu : les trois verts.

- [x] **Étape 5 : porter et commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
cp Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py \
   ~/marvel-work/fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py
cp Fusion/marvel-lcg-src/tools/test_carnet_partiel.py \
   ~/marvel-work/fusion/marvel-lcg-src/tools/test_carnet_partiel.py
git add Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py \
        Fusion/marvel-lcg-src/tools/test_carnet_partiel.py
git commit -m "feat(campagne): une route etroite pour fusionner ses champs du carnet"
```

---

### Tâche 4 : le panneau n'ouvre à la saisie que les champs du siège

**Fichiers :**
- Créer : `ui-app/src/board/campagne/droits-carnet.ts`
- Créer : `ui-app/src/board/campagne/droits-carnet.test.ts`
- Modifier : `ui-app/src/board/campagne/PanneauRecompenses.tsx`
- Modifier : `ui-app/src/board.tsx` (passer le siège au panneau)

**Interfaces :**
- Consomme : `ChampVictoire`, `cleCarnet` (`./detecteurs`).
- Produit : `type DroitCarnet = 'saisie' | 'lecture'`, `droitSurChamp(champ: ChampVictoire, joueurId: number, siege: number, estHote: boolean): DroitCarnet`, et `peutValider(siege: number): boolean`.

- [x] **Étape 1 : écrire le test**

Créer `ui-app/src/board/campagne/droits-carnet.test.ts` :

```ts
// Qui a le droit d'écrire quoi dans le carnet.
//
// La règle en une phrase : un champ `parJoueur` appartient au siège qu'il
// nomme, tout le reste appartient à l'hôte. Sans elle, deux joueurs écrivent
// la même case et le dernier gagne, en silence.
import { describe, expect, it } from 'vitest'
import { droitSurChamp, peutValider } from './droits-carnet'
import type { ChampVictoire } from './detecteurs'

const commun: ChampVictoire = { cle: 'Bombs Defused', type: 'choix', libelle: '' }
const personnel: ChampVictoire = { cle: 'Upgrade', type: 'choix', parJoueur: true, libelle: '' }

describe('les droits sur le carnet', () => {
  it('un champ personnel appartient au siège qu il nomme', () => {
    expect(droitSurChamp(personnel, 1, 1, false)).toBe('saisie')
    expect(droitSurChamp(personnel, 0, 1, false)).toBe('lecture')
  })

  it("l'hôte ne s'approprie pas les champs personnels des autres", () => {
    // Sinon deux personnes remplissent la même case, et « chacun ses champs »
    // ne veut plus rien dire.
    expect(droitSurChamp(personnel, 2, 0, true)).toBe('lecture')
    expect(droitSurChamp(personnel, 0, 0, true)).toBe('saisie')
  })

  it("un champ commun n'appartient qu'à l'hôte", () => {
    expect(droitSurChamp(commun, 0, 0, true)).toBe('saisie')
    expect(droitSurChamp(commun, 0, 2, false)).toBe('lecture')
  })

  it('un siège inconnu ne peut rien écrire', () => {
    expect(droitSurChamp(personnel, 1, -1, false)).toBe('lecture')
    expect(droitSurChamp(commun, 0, -1, false)).toBe('lecture')
  })
})

describe('qui valide pour la table', () => {
  it("seul l'hôte valide", () => {
    expect(peutValider(0)).toBe(true)
    expect(peutValider(1)).toBe(false)
    expect(peutValider(3)).toBe(false)
  })

  it('un siège inconnu ne valide pas', () => {
    // Une page ouverte sans `?p=` ne doit pas pouvoir terminer le scénario de
    // toute la table depuis un écran qu'elle n'a pas rempli.
    expect(peutValider(-1)).toBe(false)
  })
})
```

- [x] **Étape 2 : lancer le test, vérifier qu'il échoue**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-app"
npx vitest run src/board/campagne/droits-carnet.test.ts
```

Attendu : ROUGE, import non résolu.

- [x] **Étape 3 : écrire le module**

Créer `ui-app/src/board/campagne/droits-carnet.ts` :

```ts
// Qui écrit quoi dans le carnet, quand la table est répartie sur plusieurs
// appareils.
//
// La règle tient en une phrase : un champ `parJoueur` appartient au siège
// qu'il nomme, tout le reste appartient à l'hôte. Elle vient de la décision du
// 12/8/2026, « chacun ses champs, l'hôte valide ».
//
// Deux conséquences volontaires. L'hôte ne s'approprie PAS les champs
// personnels des autres : s'il le pouvait, deux personnes rempliraient la même
// case et « chacun ses champs » ne voudrait plus rien dire. Et un siège inconnu
// (URL sans `?p=`, spectateur) ne peut rien écrire du tout.
import type { ChampVictoire } from './detecteurs'

export type DroitCarnet = 'saisie' | 'lecture'

export function droitSurChamp(
  champ: ChampVictoire,
  joueurId: number,
  siege: number,
  estHote: boolean
): DroitCarnet {
  if (siege < 0) return 'lecture'
  if (champ.parJoueur) return joueurId === siege ? 'saisie' : 'lecture'
  return estHote ? 'saisie' : 'lecture'
}

/**
 * Qui termine le scénario pour toute la table.
 *
 * L'hôte, et lui seul. Un distant qui verrait « Valider » reporterait le
 * scénario au carnet depuis un écran où il n'a rempli qu'une case, et les
 * autres perdraient la leur.
 */
export function peutValider(siege: number): boolean {
  return siege === 0
}
```

- [x] **Étape 4 : brancher le panneau**

Dans `PanneauRecompenses.tsx` :

a) la signature reçoit le siège :

```tsx
export function PanneauRecompenses({
  monde,
  gagne,
  siege,
  onTermine,
}: {
  monde: World | undefined
  gagne: boolean
  /** Siège de CE navigateur, tel que l'URL le donne (`?p=`). Le 0 est l'hôte. */
  siege: number
  onTermine: (retourCampagne: boolean) => void
}) {
```

b) à l'endroit qui dessine une ligne par joueur (autour de la ligne 412), remplacer le champ de saisie par une version qui respecte le droit. Le rendu existant boucle déjà sur `joueurs` ; ajouter dans la boucle, avant le rendu de la ligne :

```tsx
        const droit = droitSurChamp(champ, joueurId, siege, siege === 0)
```

et rendre le contrôle inerte quand le droit est `lecture` : ajouter `disabled={droit === 'lecture'}` sur l'`input` ou le `select`, et faire suivre le libellé de la mention du propriétaire :

```tsx
        {droit === 'lecture' && champ.parJoueur ? (
          <small className="camp-recomp-proprietaire">
            {t('à remplir par')} {`P${joueurId + 1}`}
          </small>
        ) : null}
```

Importer `droitSurChamp` en tête.

c) dans `board.tsx`, passer le siège (ligne 1384) :

```tsx
        <PanneauRecompenses
          monde={monde}
          gagne={gagne}
          siege={playerId}
```

Vérifier que `playerId` est bien dans la portée du composant de fin de partie ; sinon le faire descendre depuis `parametres()`, comme le reste.

d) ajouter au dictionnaire `dico-en.ts` :

```ts
  'à remplir par': 'to be filled by',
```

- [x] **Étape 5 : relancer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-app"
npx vitest run && npx tsc --noEmit
```

Attendu : VERT. Si un test existant de `PanneauRecompenses` casse faute de la nouvelle prop `siege`, lui passer `siege={0}` : l'hôte est le comportement d'avant, et le test décrit ce comportement-là.

- [x] **Étape 6 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add ui-app/src/board/campagne/droits-carnet.ts ui-app/src/board/campagne/droits-carnet.test.ts \
        ui-app/src/board/campagne/PanneauRecompenses.tsx ui-app/src/board.tsx ui-app/src/board/dico-en.ts
git commit -m "feat(campagne): chacun ne saisit que ses champs, les autres en lecture"
```

---

### Tâche 5 : les distants postent, l'hôte voit arriver et valide

**Fichiers :**
- Modifier : `ui-app/src/board/campagne/contexte.ts` (l'appel de route)
- Modifier : `ui-app/src/board/campagne/PanneauRecompenses.tsx`
- Créer : `ui-app/src/board/campagne/PanneauRecompenses.multi.test.tsx`

**Interfaces :**
- Consomme : `POST /save_carnet_partiel` (tâche 3), `droitSurChamp` (tâche 4).
- Produit : `enregistrerCarnetPartiel(id: string, champs: Record<string, string>): Promise<{ carnet: Record<string, string> }>`.

- [x] **Étape 0 : sortir le gabarit de monde partagé**

`preremplissage.test.ts` et `detecteurs.test.ts` construisent déjà le même monde
minimal. Créer `ui-app/src/board/campagne/world-de-test.ts` qui exporte
`mondeDeTest(surcharge?: Partial<World>): World`, en y DÉPLAÇANT le gabarit de
`preremplissage.test.ts` (ne pas le recopier : deux gabarits qui divergent sont
pires qu'un seul). Faire pointer `preremplissage.test.ts` dessus, relancer
`npx vitest run src/board/campagne/`, et vérifier que les cas existants restent
verts AVANT d'écrire le test ci-dessous.

- [x] **Étape 1 : écrire le test**

Créer `ui-app/src/board/campagne/PanneauRecompenses.multi.test.tsx` :

```tsx
// Le panneau à plusieurs : un distant envoie ses champs, l'hôte les voit
// arriver, et lui seul peut valider.
//
// Le piège que ce fichier verrouille : un distant qui verrait « Valider »
// terminerait le scénario pour toute la table, depuis un écran où il n'a
// rempli qu'une case.
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { PanneauRecompenses } from './PanneauRecompenses'
import { CLE_CAMPAGNE } from './contexte'
import { mondeDeTest } from './world-de-test'

beforeEach(() => {
  window.localStorage.clear()
  vi.restoreAllMocks()
})

describe('le panneau à plusieurs', () => {
  it("ne montre pas « Valider » à un siège qui n'est pas l'hôte", async () => {
    window.localStorage.setItem(CLE_CAMPAGNE, JSON.stringify({ id: 'trors-1', scenario: 'crossbones' }))
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={2} onTermine={() => {}} />)
    await waitFor(() => expect(screen.queryByRole('button', { name: /Valider/ })).toBeNull())
  })

  it("montre « Valider » à l'hôte", async () => {
    window.localStorage.setItem(CLE_CAMPAGNE, JSON.stringify({ id: 'trors-1', scenario: 'crossbones' }))
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={0} onTermine={() => {}} />)
    await waitFor(() => expect(screen.getByRole('button', { name: /Valider/ })).toBeInTheDocument())
  })
})
```

**Note pour l'implémenteur :** ce test rend le panneau ENTIER, qui charge la campagne, sa définition et le carnet suggéré par trois appels réseau. Il faut donc bouchonner `fetch` (voir `contexte.test.ts` de la tâche 2, qui montre la forme). Si le montage se révèle trop coûteux à bouchonner, `peutValider()` est déjà couverte par `droits-carnet.test.ts` : abandonner alors ce fichier, et couvrir le rendu au jalon E en vraie partie. Consigner le choix dans le journal d'exécution plutôt que de laisser un test fragile.

- [x] **Étape 2 : lancer le test, vérifier qu'il échoue**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-app"
npx vitest run src/board/campagne/PanneauRecompenses.multi.test.tsx
```

- [x] **Étape 3 : l'appel de route**

Dans `contexte.ts`, à côté d'`enregistrerCampagne` :

```ts
/**
 * Envoie SES champs du carnet, sans toucher au reste de la campagne.
 *
 * Le serveur fusionne : deux sièges qui écrivent en même temps ne se perdent
 * pas. C'est la seule écriture qu'un siège autre que l'hôte peut faire.
 */
export const enregistrerCarnetPartiel = (
  id: string,
  champs: Record<string, string>
): Promise<{ carnet: Record<string, string> }> =>
  posterJson<{ carnet: Record<string, string> }>('/save_carnet_partiel', { id, champs })
```

- [x] **Étape 4 : le panneau, côté distant**

Dans `PanneauRecompenses.tsx` :

a) le bouton de validation ne se rend que pour l'hôte. Envelopper le bouton « Valider » existant dans `{siege === 0 ? (...) : null}`, et rendre à sa place, pour les distants, un bouton « Envoyer mes champs » :

```tsx
      {peutValider(siege) ? (
        <button type="button" onClick={valider} disabled={manquants.length > 0 || enregistrement}>
          {t('Valider')}
        </button>
      ) : (
        <>
          <button type="button" onClick={envoyerMesChamps} disabled={enregistrement}>
            {t('Envoyer mes champs')}
          </button>
          <p className="camp-recomp-attente">{t("L'hôte valide les récompenses pour la table.")}</p>
        </>
      )}
```

b) la fonction d'envoi, à côté de `valider` :

```tsx
  async function envoyerMesChamps() {
    if (enregistrement) return
    setEnregistrement(true)
    setEchec('')
    try {
      // On n'envoie QUE ce qui nous appartient : le serveur fusionne, donc
      // envoyer le carnet entier ecraserait les champs des autres avec la
      // copie qu'on en a lue, qui peut deja etre perimee.
      const miens: Record<string, string> = {}
      for (const champ of champs) {
        const total = monde?.players?.length ?? 1
        const joueurs = champ.parJoueur ? [...Array(total).keys()] : [0]
        for (const joueurId of joueurs) {
          if (droitSurChamp(champ, joueurId, siege, siege === 0) !== 'saisie') continue
          const cle = cleCarnet(champ, joueurId)
          const valeur = valeurs[cle]
          if (valeur !== undefined) miens[cle] = valeur
        }
      }
      await enregistrerCarnetPartiel(campagne.id, miens)
      setEchec('')
    } catch (e) {
      setEchec((e as Error).message)
    } finally {
      setEnregistrement(false)
    }
  }
```

c) l'hôte voit arriver les champs des autres. Ajouter un effet qui recharge la campagne tant que le panneau est ouvert :

```tsx
  // L'hôte attend les champs des autres sièges. Trois secondes suffisent : on
  // regarde quelqu'un remplir un formulaire, pas une animation. Le poll
  // s'arrête dès que le panneau se ferme, et n'existe pas chez les distants,
  // qui n'attendent personne.
  useEffect(() => {
    if (!peutValider(siege) || etat.phase !== 'pret') return
    const minuteur = window.setInterval(() => {
      void chargerCampagne(campagne.id)
        .then((fraiche) => setValeurs((v) => ({ ...(fraiche.carnet ?? {}), ...v })))
        .catch(() => undefined)
    }, 3000)
    return () => window.clearInterval(minuteur)
  }, [siege, etat.phase, campagne.id])
```

`'pret'` est bien le nom de la phase (`PanneauRecompenses.tsx:47`) : le composant
ne rend ses champs que dans cet état, et le poll n'a rien à faire avant.

```tsx
```

**Attention à l'ordre du `spread`** : `{ ...(fraiche.carnet ?? {}), ...v }` garde ce que l'hôte est en train de taper au-dessus de ce que le serveur renvoie. L'inverse effacerait sa saisie toutes les trois secondes.

d) ajouter au dictionnaire :

```ts
  'Envoyer mes champs': 'Send my fields',
  "L'hôte valide les récompenses pour la table.": 'The host validates the rewards for the table.',
```

- [x] **Étape 5 : relancer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-app"
npx vitest run && npx tsc --noEmit
```

- [x] **Étape 6 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add ui-app/src/board/campagne/ ui-app/src/board/dico-en.ts
git commit -m "feat(campagne): les distants envoient leurs champs, l'hote valide pour la table"
```

---

## Jalon C : le salon dit la vérité quand une campagne attend

Sans ce jalon, l'invité arrive sur « Choisis ton héros » alors que l'équipe est figée depuis la création de la campagne. Il choisirait pour rien, et jouerait autre chose.

### Tâche 6 : le salon reconnaît une campagne

**Fichiers :**
- Modifier : `~/marvel-work/fusion/marvel-lcg-src/public/js/salon/app.js` (RÉFÉRENCE, pas le dépôt)
- Modifier : `~/marvel-work/fusion/marvel-lcg-src/public/js/prepare/dico-en.js`
- Modifier : `Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py` (la route rend aussi l'équipe)

**Interfaces :**
- Consomme : `GET /get_campagne_en_cours` (tâche 1).
- Produit : la route rend en plus `equipe: [{heros, nomHeros}]` ; le salon affiche « Tu tiens X » au lieu de la grille de héros.

- [x] **Étape 1 : la route rend l'équipe**

Dans `get_campagne_en_cours`, remplacer le corps de la réponse par :

```python
        equipe = campagne.get('equipe') or []
        return web.json_response({
            'id': campagne.get('id', ''),
            'scenario': (campagne.get('partieEnCours') or {}).get('scenario', ''),
            'nom': campagne.get('nom', ''),
            # Le siege N tient equipe[N] : c'est deja ce que fait le moteur, qui
            # recoit `players` dans cet ordre (voir lancerScenario). Le salon
            # n'a donc rien a choisir, seulement a le DIRE.
            'equipe': [
                {'heros': m.get('heros', ''), 'nomHeros': m.get('nomHeros', '')}
                for m in equipe
            ],
        })
```

Étendre `tools/test_campagne_en_cours.py` d'un cas :

```python
        ecrire(dossier, 'avec_equipe', {
            'code': 'trors', 'nom': 'Avec equipe',
            'equipe': [{'heros': 'spider_man', 'nomHeros': 'Spider-Man'},
                       {'heros': 'she_hulk', 'nomHeros': 'She-Hulk'}],
            'partieEnCours': {'scenario': 'crossbones', 'depuis': '2026-08-13T09:00:00'},
        })
        trouvee = server_campagne._campagne_la_plus_recente()
        echecs += cas("l'equipe est portee", len(trouvee.get('equipe') or []), 2)
```

Lancer : `~/marvel-work/python/bin/python3.10 tools/test_campagne_en_cours.py`. Attendu : `ECHECS : 0`.

- [x] **Étape 2 : le salon interroge la route au démarrage**

Dans `public/js/salon/app.js` (dans `~/marvel-work/...`), avant le rendu des héros :

```js
/* ---------------- Campagne : l'equipe est deja composee ---------------- */

/**
 * En campagne, il n'y a RIEN a choisir : l'equipe a ete arretee a la creation
 * de la campagne, et le livret interdit d'en changer. Le siege N tient le
 * N-ieme membre. Montrer la grille des heros ici serait un mensonge, et le
 * choix serait ecrase au lancement.
 */
async function campagneEnCours() {
    try {
        const reponse = await fetch("get_campagne_en_cours?", { cache: "no-store" });
        if (!reponse.ok) return null;
        const brut = await reponse.json();
        return brut && brut.id ? brut : null;
    } catch (e) {
        return null;
    }
}

function rendreCampagne(campagne) {
    const membre = (campagne.equipe || [])[siege];
    const nom = membre ? (membre.nomHeros || membre.heros) : null;
    $("#salon-choix").replaceChildren(
        el("h2", {}, campagne.nom || t("Campagne en cours")),
        nom
            ? el("p", { class: "salon-campagne-heros" },
                el("b", {}, t("Tu tiens")), " ", nom)
            : el("p", { class: "salon-campagne-heros est-erreur" },
                t("Aucun héros n'est prévu pour ce siège dans cette campagne.")),
    );
    bandeauAttente(true);
}
```

et au démarrage, avant `rendreHeros()` :

```js
    const campagne = await campagneEnCours();
    if (campagne) {
        rendreCampagne(campagne);
        surveillerLeLancement();
        return;
    }
```

Placer ce bloc là où le salon décide aujourd'hui d'afficher la grille. Lire la fonction de démarrage en entier avant de l'insérer : `reprendreChoixExistant()` ne doit pas tourner en campagne, puisqu'il n'y a aucun choix à reprendre.

- [x] **Étape 3 : les trois chaînes au dictionnaire du salon**

Dans `public/js/prepare/dico-en.js` (RÉFÉRENCE) :

```js
  "Campagne en cours": "Campaign in progress",
  "Tu tiens": "You play",
  "Aucun héros n'est prévu pour ce siège dans cette campagne.":
    "No hero is assigned to this seat in this campaign.",
```

- [x] **Étape 4 : déployer et vérifier statiquement**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
bash ui-app/deployer.sh
node --check "//wsl.localhost/Ubuntu/home/arnau/marvel-work/fusion/marvel-lcg-src/public/js/salon/app.js"
```

Attendu : le déploiement passe, `node --check` ne dit rien. Rappel : Node est le binaire **Windows**, il ne lit pas un chemin WSL sans la forme `//wsl.localhost/`.

- [x] **Étape 5 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
cp Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py \
   ~/marvel-work/fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py
git add Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py \
        Fusion/marvel-lcg-src/tools/test_campagne_en_cours.py \
        public/js/salon/app.js public/js/prepare/dico-en.js
git commit -m "feat(salon): en campagne, on ne choisit pas son heros, on apprend lequel on tient"
```

---

## Jalon D : enchaîner le scénario suivant

### Tâche 7 : les distants suivent l'hôte sans naviguer à la main

Après validation, l'hôte revient sur `/campagne.html` et lance le scénario suivant. Les distants restent sur l'écran de fin du précédent.

**Fichiers :**
- Modifier : `ui-app/src/board/campagne/PanneauRecompenses.tsx`
- Créer : `ui-app/src/board/campagne/attente-scenario.ts`
- Créer : `ui-app/src/board/campagne/attente-scenario.test.ts`

**Interfaces :**
- Consomme : `GET /get_campagne_en_cours` (tâche 1).
- Produit : `scenarioSuivantLance(scenarioCourant: string, lu: { id?: string; scenario?: string } | null): boolean`, et un effet qui recharge la page quand elle rend `true`.

- [x] **Étape 1 : écrire le test**

Créer `ui-app/src/board/campagne/attente-scenario.test.ts` :

```ts
// Quand l'hôte lance le scénario suivant, les distants doivent suivre.
//
// Le signal le moins coûteux est celui qui existe déjà : la route dit quelle
// campagne et quel scénario sont en cours. Dès que le scénario change, une
// nouvelle partie a démarré.
import { describe, expect, it } from 'vitest'
import { scenarioSuivantLance } from './attente-scenario'

describe('le signal du scénario suivant', () => {
  it('dit oui quand le scénario en cours a changé', () => {
    expect(scenarioSuivantLance('crossbones', { id: 'trors-1', scenario: 'absorbing_man' })).toBe(true)
  })

  it("dit non tant que c'est le même scénario", () => {
    expect(scenarioSuivantLance('crossbones', { id: 'trors-1', scenario: 'crossbones' })).toBe(false)
  })

  it("dit non quand la route ne répond rien d'utile", () => {
    expect(scenarioSuivantLance('crossbones', null)).toBe(false)
    expect(scenarioSuivantLance('crossbones', {})).toBe(false)
    expect(scenarioSuivantLance('crossbones', { id: 'trors-1' })).toBe(false)
  })

  it("dit non quand la campagne n'a plus de partie en cours", () => {
    // Entre la validation de l'hôte et son prochain lancement, `partieEnCours`
    // vaut null : la route rend un scénario vide. Recharger à ce moment-là
    // renverrait les distants sur un plateau mort.
    expect(scenarioSuivantLance('crossbones', { id: 'trors-1', scenario: '' })).toBe(false)
  })
})
```

- [x] **Étape 2 : lancer, vérifier le rouge**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-app"
npx vitest run src/board/campagne/attente-scenario.test.ts
```

- [x] **Étape 3 : écrire le module**

Créer `ui-app/src/board/campagne/attente-scenario.ts` :

```ts
// « L'hôte a-t-il lancé le scénario suivant ? »
//
// Aucune route nouvelle : `/get_campagne_en_cours` dit déjà quel scénario est
// en cours, et l'écran des campagnes réécrit `partieEnCours` AVANT de lancer.
// Un scénario différent du nôtre signifie donc qu'une nouvelle partie a
// démarré, et qu'il est temps de recharger.
//
// Le cas qui compte, et qui n'est pas évident : entre la validation de l'hôte
// et son prochain lancement, `partieEnCours` vaut null et la route rend un
// scénario VIDE. Recharger là renverrait les distants sur un plateau mort.

export function scenarioSuivantLance(
  scenarioCourant: string,
  lu: { id?: string; scenario?: string } | null
): boolean {
  if (!lu?.scenario) return false
  return lu.scenario !== scenarioCourant
}
```

- [x] **Étape 4 : brancher l'attente chez les distants**

Dans `PanneauRecompenses.tsx`, ajouter :

```tsx
  // Les distants suivent l'hôte. L'hôte, lui, navigue tout seul : c'est lui qui
  // relance depuis l'écran des campagnes, il n'a personne à attendre.
  useEffect(() => {
    if (peutValider(siege) || etat.phase !== 'pret') return
    const minuteur = window.setInterval(() => {
      void fetch('/get_campagne_en_cours', { cache: 'no-store' })
        .then((r) => (r.ok ? r.json() : null))
        .then((lu) => {
          if (scenarioSuivantLance(scenario.id, lu)) window.location.reload()
        })
        .catch(() => undefined)
    }, 4000)
    return () => window.clearInterval(minuteur)
  }, [siege, etat.phase, scenario.id])
```

- [x] **Étape 5 : relancer et commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-app"
npx vitest run && npx tsc --noEmit
cd ..
git add ui-app/src/board/campagne/
git commit -m "feat(campagne): les distants suivent quand l'hote lance le scenario suivant"
```

---

## Jalon E : l'éprouver pour de vrai

### Tâche 8 : une campagne à deux, de bout en bout

C'est le critère d'acceptation de la fiche, et rien de ce qui précède ne le remplace.

**Fichiers :**
- Créer : `ui-check/tests/campagne-multi.spec.ts`
- Modifier : `docs/CAMPAGNES.md`, `docs/MULTIJOUEUR.md`, `.twei/SESSION.md`, `.planning/STATE.md`, `.planning/todos/2026-08-12-campagne-en-ligne.md`

- [ ] **Étape 1 : déployer l'ensemble**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
cp Fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py \
   ~/marvel-work/fusion/marvel-lcg-src/src/engine/device/web/server/server_campagne.py
cd ~/marvel-work/fusion/marvel-lcg-src && ~/marvel-work/python/bin/python3.10 launcher_fast.py --build-only
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions" && bash ui-app/deployer.sh
```

Puis **redémarrer le serveur de dev** : le bytecode n'est relu qu'au démarrage, et les deux routes neuves n'existeront pas sans cela.

- [ ] **Étape 2 : le test automatisé, sur deux contextes de navigateur**

Créer `ui-check/tests/campagne-multi.spec.ts`, sur le modèle de `campagne-pilote.spec.ts` et en réutilisant `ui-check/pilote-campagne.ts`, qui sait déjà **servir tous les sièges**. Le test doit établir, dans cet ordre :

1. `/get_campagne_en_cours` rend `{id, scenario, equipe}` pendant une partie de campagne, et `{}` pendant une partie ordinaire.
2. Un second contexte de navigateur ouvert sur `/app/board.html?p=1`, **sans jamais poser la clé `mc-campagne-partie`**, voit le panneau de récompenses à la fin. C'est la preuve du jalon A, et le cœur du chantier.
3. Sur ce second contexte, un champ `parJoueur` du siège 0 est en lecture, celui du siège 1 en saisie.
4. Le bouton « Valider » est absent du siège 1 et présent du siège 0.
5. Après « Envoyer mes champs » côté siège 1 puis « Valider » côté siège 0, le carnet relu par `/get_campagne` contient **les deux** saisies.

Lancer :

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/ui-check"
export UI_CHECK_BASE=http://127.0.0.1:2346 WSLENV=UI_CHECK_BASE
npx playwright test tests/campagne-multi.spec.ts --project=pc
```

- [ ] **Étape 3 : la vraie partie, à deux navigateurs**

Ce que le test ne couvre pas et qui demande un humain : le salon. Lancer `JOUER-EN-MULTI.bat`, ouvrir le lien du joueur 2 dans un autre navigateur, et vérifier qu'il lit « Tu tiens <héros> » et non « Choisis ton héros ». Puis mener un scénario, valider à deux, et lancer le suivant pour voir le second navigateur suivre tout seul.

**Vérifier aussi la prémisse non mesurée** notée en tête de ce plan : que se passait-il AVANT ce chantier quand l'hôte lançait une campagne pendant qu'un invité attendait au salon ? Le noter, même si la réponse n'a plus d'importance : elle dit si la fiche décrivait un bug ou une absence.

- [ ] **Étape 4 : mettre les documents à l'état mesuré**

- `.planning/todos/2026-08-12-campagne-en-ligne.md` : statut, et **corriger l'affirmation « le blocage est là et nulle part ailleurs »**, qui a envoyé ce chantier sur une fausse piste.
- `docs/CAMPAGNES.md` : une section sur la campagne à plusieurs, les deux routes, la règle des droits.
- `docs/MULTIJOUEUR.md` : ce qui change pour l'hôte et pour les invités.
- `.twei/SESSION.md` et `.planning/STATE.md` : la continuité.

- [ ] **Étape 5 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions"
git add ui-check/tests/campagne-multi.spec.ts docs/ .twei/SESSION.md .planning/
git commit -m "test(campagne): une campagne menee a deux, du lancement a la validation"
```

---

## Ce qui reste hors de ce plan, et pourquoi

- **Le secret d'A.I.M. à quatre sièges (§4.5 de la fiche).** `_sans_secret()` protège les routes, et la fermeture du 12/8 (§17 de `docs/CAMPAGNES.md`) fabrique une preuve seulement au moment du droit de la voir. La route neuve `/get_campagne_en_cours` ne rend ni carnet ni preuve. Reste à éprouver que la répartition ne se déduit pas d'un carnet partagé lu par plusieurs : c'est une campagne de tests à soi seule, et elle a besoin des jalons A à D pour exister.
- **Changer l'équipe en cours de campagne.** Interdit par le livret. Si le besoin apparaît (un joueur qui abandonne), c'est une décision de règle, pas un chantier technique.
- **Le serveur permanent** (`.planning/todos/2026-07-28-serveur-permanent-multijoueur.md`). Ce chantier-ci marche sur le multi actuel, tunnel et mot de passe compris.
- **Le re-zip vers `Fusion/`.** Dette antérieure, déjà signalée par le plan du rapport de bug. À solder à part.


---

## Journal d'exécution (12/08/2026)

**Tâches 1 à 7 faites**, huit commits, `e596187` à `2ccd41c`. Jalons A, B, C et D
livrés. Vérifications lancées et lues :

| Vérification | Résultat |
|---|---|
| `npx vitest run` | **434 cas verts** (429 avant la tâche 7, 415 avant le chantier) |
| `npx tsc --noEmit` | sans erreur |
| `tools/test_campagne_en_cours.py` | 15 vérifications |
| `tools/test_carnet_partiel.py` | 14 vérifications |
| `tools/verifier_campagnes.py` | vert |
| `tools/verifier_grille_aos.py` | 8/8 |
| `tools/test_ecriture_atomique.py` | 8/8 |
| `node --check` sur `salon/app.js` et `prepare/dico-en.js` | sans erreur |
| `launcher_fast.py --build-only` | 1 compilé, 0 échec |
| Les deux routes en **HTTP réel** sur le serveur de dev | conformes, voir ci-dessous |

### Les routes éprouvées en HTTP, pas seulement en appel direct

Les tests Python appellent les méthodes du serveur en direct : ils ne prouvent
pas que les routes sont SERVIES. Sondées sur le serveur de dev (port 2346), avec
une campagne de test créée puis supprimée :

- `GET /get_campagne_en_cours` hors campagne : `200 {}`.
- Avec une campagne : `{"id", "scenario", "nom", "equipe"}`, **sans secret ni carnet**.
- `POST /save_carnet_partiel` : fusionne (le champ du joueur 1 survit à l'écriture du joueur 2).
- Le même POST portant `termines` et `perdue` : ignorés. Après écriture, `termines`
  vaut toujours `[]`, `perdue` est absent, le secret est intact.

### Les pièges payés

1. **Les fins de ligne, deux fois.** `server_campagne.py` et `prepare/dico-en.js`
   sont en CRLF intégral. Une lecture `newline=''` avec des motifs en LF ne
   correspond à rien, et l'assertion tombe sans expliquer pourquoi. La méthode
   qui marche : lire `newline=''`, normaliser en LF, éditer, réécrire en CRLF.
2. **Le poll de l'hôte réécrivait ses propres cases.** Le plan disait de fusionner
   `{...carnet, ...valeurs}`. Ce n'est pas suffisant : une case que l'hôte vient
   d'EFFACER est retirée de `valeurs` (par `poser`, qui fait `delete`), donc le
   serveur la réinjecte trois secondes plus tard. D'où `cleDUnAutreSiege()`, qui
   ne reprend que les clés `Player N ` d'un autre siège. Ajout non prévu au plan,
   avec ses quatre cas de test.
3. **Une empreinte périmée trouvée en passant.** `prepare.html` portait
   `app.js?v=9e61a4a9` alors que le fichier vaut `e9c6f532`. Un navigateur ayant
   l'ancien en cache ne l'aurait jamais rechargé. Corrigé par `deployer.sh` et
   commité à part (`cf551f1`), sans rapport avec ce chantier.

### Écarts par rapport au plan écrit

- **`world-de-test.ts` créé sans vider `preremplissage.test.ts`.** Le plan
  demandait d'y DÉPLACER le gabarit commun. Toucher un test vert qui couvre le
  pré-remplissage pour un gain de forme est un risque gratuit : le nouveau
  fichier sert au seul test neuf, et le commentaire en tête le dit.
- **`PanneauRecompenses.multi.test.tsx` a bien été écrit.** Le plan prévoyait de
  l'abandonner si le bouchonnage se révélait trop coûteux ; un seul stub de
  `fetch` routant par URL a suffi. Les quatre cas ont été **vérifiés par
  mutation** (`peutValider -> true` en fait tomber 3, `droitSurChamp -> 'saisie'`
  en fait tomber 1) : ils passaient du premier coup, ce qui ne prouve rien tant
  qu'on ne les a pas vus mordre.
- **Un état `envoye`** ajouté au panneau : un distant n'a pas de « Valider », donc
  sans retour il ne saurait pas si son envoi a pris.

### Ajouté après coup : la tâche 8 étape 2 est faite (`5e2f990`)

`ui-check/tests/campagne-multi.spec.ts`, 2/2 verts, 26 autres cas de campagne sans
régression. **Vérifié par mutation** : `resoudreContexte()` réduite à
`lireContexte()` fait rougir le test sur « Le siège 1 doit voir le panneau sans
avoir jamais eu la clé » — l'assertion centrale mord.

Trois choses apprises en l'écrivant :

1. **Un défaut d'interface révélé** : le panneau listait aux sièges distants
   « À choisir avant de continuer : <champ> » pour des cases appartenant à
   d'autres joueurs. Le message ne sert qu'à bloquer le bouton de l'hôte ; il lui
   est désormais réservé.
2. **Compter les boutons de tout le panneau est fragile** : la première version
   supposait trois options par champ là où `Tech Upgrade` en porte quatre, et
   pointait la mauvaise carte en ayant l'air juste. Le test cible maintenant le
   champ par sa NATURE (`:has(.camp-champ-joueur)`) et les cartes DANS leur ligne.
3. **Deux rôles ne partagent pas un sélecteur** : `.camp-recomp-bloque` servait au
   message d'attente du distant ET à la liste des manquants. Le premier a pris sa
   propre classe.

### Ce qui reste vraiment : l'essai humain



Le serveur de dev tourne sur le port 2346, prêt pour l'essai. Rien n'a été mené
en vraie partie : **le critère d'acceptation de la fiche n'est pas atteint**, et
la prémisse notée en tête de ce plan (ce que voyait un invité au salon AVANT ce
chantier) reste non mesurée.
