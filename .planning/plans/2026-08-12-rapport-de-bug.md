# Rapport de bug — plan d'implémentation

> **Pour les agents :** SOUS-SKILL REQUIS — utiliser `superpowers:subagent-driven-development` (recommandé) ou `superpowers:executing-plans` pour dérouler ce plan tâche par tâche. Les étapes utilisent la syntaxe case à cocher (`- [ ]`).

**Objectif :** deux boutons dans le panneau « H » et un raccourci clavier qui sortent l'état de la partie sous une forme exploitable pour signaler un bug : un texte collable dans une conversation, et un `.json` complet.

**Architecture :** un module PUR (`rapport-bug.ts`) qui prend `(monde, demande, entrees, portée, contexte)` et rend un objet et un texte. Il ne touche ni au réseau ni au DOM, donc il se teste entièrement sous vitest. Une couche React mince (`RapportBug.tsx`) l'habille : sélecteur de portée, presse-papier, téléchargement. Le journal existant gagne UN champ (`brut`), le moteur ne change pas.

**Stack :** React 19 + TypeScript strict (`ui-app/`), vitest, `npx tsc --noEmit`.

**Spec :** `.planning/todos/2026-08-12-rapport-de-bug.md`

---

## Ce que la mesure a corrigé dans la spec

Trois points de la fiche sont FAUX ou sans objet, vérifiés dans le code le 12/8/2026. Les tâches ci-dessous en tiennent compte ; ne pas se fier à la fiche sur ces trois points.

1. **« Le rapport n'a qu'à ne pas nettoyer » est faux.** `texteSignificatif()` (`HistoriquePartie.tsx:73`) applique `sansIdentifiants()` **à la création de l'entrée** : ce qui est stocké en `sessionStorage` est DÉJÀ propre. Les identifiants `[(50,01113) Klaw]` sont perdus au moment où l'entrée naît, pas à l'affichage. D'où la tâche 1, qui garde le texte brut à côté du texte propre.
2. **« nom anglais en plus du français » est sans objet.** Le moteur n'envoie qu'UN nom, et il est anglais (mesuré sur les 35 fixtures : `"name": "None Shall Pass"`, `"name": "Absorbing Man"`). `TEXTES_FR` porte le TEXTE des cartes, jamais leur nom. Le rapport recopie `carte.name` tel quel.
3. **Les entrées `card`, `damage`, `heal`, `threat` gardent déjà leur `cibleId`**, donc leur object ID est récupérable sans rien changer. Seules les entrées `text` de narration perdent leurs identifiants.

## Décisions arrêtées avec l'utilisateur (12/8/2026)

| Question de la fiche §5 | Décision |
|---|---|
| Capture au clic ou en continu | **Au clic seulement.** Le rapport lit le `monde` et la `demande` du moment. Aucun tampon d'états, aucun coût mémoire. Le journal, lui, couvre déjà le passé |
| Où vivent les boutons | **Dans le panneau « H » ET derrière un raccourci clavier** (`B`), pour capturer sans ouvrir le panneau |
| Le rapport en multi | **Complet, avec un avertissement en tête.** Le `world` du siège contient déjà les mains adverses : le rapport ne révèle rien de neuf, et un rapport amputé rate justement le bug |

## Contraintes globales

- **Le moteur ne change pas.** Rien sous `src/`, `data/` ou `tools/`. Ce chantier ne touche que `ui-app/`.
- **`ui-app/` s'édite dans le dépôt** (`Jeu Marvel Champions/ui-app/`), au contraire de `public/js` et `public/css` qui s'éditent dans `~/marvel-work/fusion/marvel-lcg-src`. Déploiement : `bash ui-app/deployer.sh`.
- **TypeScript strict, zéro `any`.** Le contrat `/get_world` n'est connu que par mesure : ne rien supposer d'un champ absent des types de `world.ts`.
- **Toute chaîne visible passe par `t()`** et a son entrée dans `ui-app/src/board/dico-en.ts`. Une clé absente laisse le texte en français, rien ne casse, mais l'anglais est incomplet.
- **Pas d'em dash (—) ni de tiret parenthétique** dans les textes visibles ni dans les commentaires de code.
- **Avant chaque commit** : `cd ui-app && npx vitest run && npx tsc --noEmit`, tous les deux verts. Ne jamais annoncer un test vert sans l'avoir lancé.
- **Le journal est stocké du PLUS RÉCENT AU PLUS ANCIEN** (`ajouterNouvellesEntrees` fait `[...aAjouter.reverse(), ...courantes]`). « Les 20 dernières » se lit donc `entrees.slice(0, 20)`, jamais `slice(-20)`.
- **Object ID = `c` + le nombre** (`c48`). C'est la seule façon fiable de viser une carte depuis la console : par nom l'étoile des cartes uniques fait tout échouer en silence, par `card_id` une carte absente du jeu est FABRIQUÉE dans la zone mise de côté.

---

### Tâche 1 : le journal garde le texte brut

Sans elle, le rapport n'a aucun identifiant à donner sur les lignes de narration, qui sont justement les plus nombreuses. Le champ est optionnel : un journal restauré depuis l'ancien format reste lisible.

**Fichiers :**
- Modifier : `ui-app/src/board/HistoriquePartie.tsx` (type `EntreeHistorique`, `narrationsDuRendu`, l'effet qui construit les entrées, export de `MAX_ENTREES`)
- Créer : `ui-app/src/board/historique-brut.test.ts`

**Interfaces :**
- Consomme : rien.
- Produit : `EntreeHistorique.brut?: string` (le texte du moteur AVANT `sansIdentifiants()`, `trim()` appliqué) ; `export const MAX_ENTREES = 400`.

- [x] **Étape 1 : écrire le test qui échoue**

Créer `ui-app/src/board/historique-brut.test.ts` :

```ts
// Le rapport de bug se vise par OBJECT ID. Or les identifiants du moteur
// (« [(50,01113) Klaw] ») sont effaces des la creation de l'entree, par
// texteSignificatif(). Le journal garde donc le texte BRUT a cote du texte
// propre : l'affichage continue de lire le propre, le rapport lit le brut.
import { describe, expect, it } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useHistoriquePartie } from './HistoriquePartie'
import type { World } from './world'

const ZONES = {
  area_schemes_main: [], main_schemes_deck: [], area_schemes_side: [],
  additional_decks: [], additional_discard_piles: [], area_villain: [],
  villain_deck: [], encounter_deck: [], encounter_discard_pile: [],
  area_boost: [], area_environment: [], area_evidence: [], area_rule: [],
  area_processing: [], area_revealing: [], area_resources: [],
  area_removed: [], area_insert: [], area_set_aside: [],
  victory_display: [], area_status_cards: [], players: [],
  active_card_ids: [],
}

function monde(prompt: string): World {
  return {
    render_id: 1, round_id: 1, phase: 'Player 1 Turn',
    prompt, event_name: 'PlayerOnEvent_Text', ...ZONES,
  }
}

describe('le texte brut du journal', () => {
  it("garde les identifiants du moteur a cote du texte affiche", () => {
    const { result } = renderHook(() =>
      useHistoriquePartie(monde('[(50,01113) Klaw] would deal 2 damage'), undefined, 1)
    )
    const narration = result.current.entrees.find((e) => e.type === 'text')
    expect(narration?.titre).toBe('Klaw would deal 2 damage')
    expect(narration?.brut).toBe('[(50,01113) Klaw] would deal 2 damage')
  })

  it("laisse brut absent sur les entrees qui ne viennent pas d'une narration", () => {
    const { result } = renderHook(() => useHistoriquePartie(monde(''), undefined, 1))
    const phase = result.current.entrees.find((e) => e.type === 'phase')
    expect(phase?.brut).toBeUndefined()
  })
})
```

- [x] **Étape 2 : lancer le test, vérifier qu'il échoue**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/historique-brut.test.ts
```

Attendu : ROUGE, `expected undefined to be '[(50,01113) Klaw] would deal 2 damage'`.

- [x] **Étape 3 : ajouter le champ au type**

Dans `HistoriquePartie.tsx`, à la fin du type `EntreeHistorique` (après `acteur?: string`) :

```ts
  /**
   * Le texte du moteur AVANT sansIdentifiants(), quand l'entree vient d'une
   * narration. C'est la seule trace des identifiants « [(50,01113) Klaw] »,
   * que texteSignificatif() efface a la creation : l'affichage lit `titre`,
   * le rapport de bug lit `brut`. Absent sur les autres types d'entree, qui
   * portent deja leur object id dans `cibleId`.
   */
  brut?: string
```

- [x] **Étape 4 : rendre `narrationsDuRendu` porteuse du brut**

Remplacer la fonction entière (`HistoriquePartie.tsx`, autour de la ligne 245) par :

```ts
type Narration = { texte: string; brut: string }

function narrationsDuRendu(monde: World, demande: Demande | undefined): Narration[] {
  const sources = [monde.prompt, monde.prompt_last_text, demande?.prompt_text]
  const sorties: Narration[] = []
  const vus = new Set<string>()
  for (const source of sources) {
    const texte = texteSignificatif(source)
    if (texte === undefined || vus.has(texte)) continue
    vus.add(texte)
    sorties.push({ texte, brut: (source ?? '').trim() })
  }
  return sorties
}
```

- [x] **Étape 5 : brancher les deux consommateurs**

Dans l'effet de `useHistoriquePartie`, remplacer les deux lignes qui utilisent `narrations` :

```ts
    const narrations = narrationsDuRendu(monde, demande)
    for (const { texte } of narrations) noterCause(causes.current, texte, monde.render_id)

    const nouvelles = [
      ...(precedent.current
        ? analyserDelta(precedent.current, monde, causes.current)
        : [entree(monde, 'phase', `Round ${monde.round_id}`, monde.phase, 'initial')]),
      ...narrations.map(({ texte, brut }) => ({
        ...entree(monde, 'text', texte, undefined, `text:${texte}`),
        brut,
      })),
    ]
```

- [x] **Étape 6 : exporter le plafond**

Le rapport doit pouvoir DIRE qu'il est tronqué. Changer `const MAX_ENTREES = 400` en `export const MAX_ENTREES = 400` (le commentaire au-dessus reste tel quel).

- [x] **Étape 7 : relancer les tests**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/historique-brut.test.ts src/board/historique-partie-portee.test.ts && npx tsc --noEmit
```

Attendu : VERT des deux côtés. `historique-partie-portee.test.ts` est relancé exprès : il verrouille la persistance du journal, que cette tâche modifie.

- [x] **Étape 8 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/HistoriquePartie.tsx ui-app/src/board/historique-brut.test.ts
git commit -m "feat(journal): garder le texte brut du moteur a cote du texte affiche"
```

---

### Tâche 2 : les erreurs console sont collectées

Le point 4 du contenu retenu (« les erreurs console récentes ») n'existe nulle part : personne ne les garde. Un module minuscule, installé une fois au montage du plateau.

**Fichiers :**
- Créer : `ui-app/src/board/erreurs-console.ts`
- Créer : `ui-app/src/board/erreurs-console.test.ts`

**Interfaces :**
- Consomme : rien.
- Produit : `installerCollecteErreurs(): () => void` (rend la fonction de désinstallation) et `erreursRecentes(): string[]` (les 20 dernières, de la plus ancienne à la plus récente).

- [x] **Étape 1 : écrire le test qui échoue**

Créer `ui-app/src/board/erreurs-console.test.ts` :

```ts
// Une erreur console est souvent la seule trace d'un bug de rendu, et elle
// disparait avec l'onglet. On les garde donc en memoire, plafonnees, pour que
// le rapport de bug puisse les recopier.
import { afterEach, describe, expect, it } from 'vitest'
import { erreursRecentes, installerCollecteErreurs } from './erreurs-console'

let desinstaller: (() => void) | undefined
afterEach(() => {
  desinstaller?.()
  desinstaller = undefined
})

describe('collecte des erreurs console', () => {
  it('retient ce qui passe par console.error', () => {
    desinstaller = installerCollecteErreurs()
    console.error('boum', 42)
    expect(erreursRecentes()).toEqual(['boum 42'])
  })

  it('laisse console.error faire son travail', () => {
    const vus: unknown[][] = []
    const original = console.error
    console.error = (...args: unknown[]) => void vus.push(args)
    desinstaller = installerCollecteErreurs()
    console.error('toujours affiche')
    desinstaller()
    desinstaller = undefined
    console.error = original
    expect(vus).toEqual([['toujours affiche']])
  })

  it('plafonne a 20 et garde les plus RECENTES', () => {
    desinstaller = installerCollecteErreurs()
    for (let i = 0; i < 25; i += 1) console.error(`erreur ${i}`)
    const gardees = erreursRecentes()
    expect(gardees).toHaveLength(20)
    expect(gardees[0]).toBe('erreur 5')
    expect(gardees[19]).toBe('erreur 24')
  })

  it('rend la console intacte apres desinstallation', () => {
    const avant = console.error
    installerCollecteErreurs()()
    expect(console.error).toBe(avant)
  })
})
```

- [x] **Étape 2 : lancer le test, vérifier qu'il échoue**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/erreurs-console.test.ts
```

Attendu : ROUGE, `Failed to resolve import "./erreurs-console"`.

- [x] **Étape 3 : écrire le module**

Créer `ui-app/src/board/erreurs-console.ts` :

```ts
// Les erreurs console recentes, gardees pour le rapport de bug.
//
// Une exception de rendu s'affiche une fois dans la console et disparait avec
// l'onglet. Quand l'utilisateur signale « ca s'est bloque », c'est souvent la
// seule trace qui existe. On la garde donc en memoire, plafonnee, sans jamais
// empecher la console de faire son travail : le module s'INSERE devant
// console.error, il ne le remplace pas.

/** Plafond volontairement bas : au-dela, ce sont des repetitions. */
const MAX_ERREURS = 20

let erreurs: string[] = []
let installee = false

function enTexte(valeur: unknown): string {
  if (valeur instanceof Error) return `${valeur.name}: ${valeur.message}`
  if (typeof valeur === 'string') return valeur
  try {
    return JSON.stringify(valeur) ?? String(valeur)
  } catch {
    // Une valeur circulaire ou un objet hostile ne doit pas casser la collecte.
    return String(valeur)
  }
}

function noter(texte: string): void {
  erreurs = [...erreurs, texte].slice(-MAX_ERREURS)
}

/** Les erreurs relevees, de la plus ANCIENNE a la plus recente. */
export function erreursRecentes(): string[] {
  return [...erreurs]
}

/**
 * Installe la collecte. Rend la fonction qui la desinstalle et rend la console
 * exactement telle qu'elle etait. Un second appel sans desinstallation est sans
 * effet : sinon deux montages empileraient deux relais, et chaque erreur serait
 * comptee deux fois.
 */
export function installerCollecteErreurs(): () => void {
  if (installee) return () => undefined
  installee = true

  const originale = console.error
  console.error = (...args: unknown[]) => {
    noter(args.map(enTexte).join(' '))
    originale.apply(console, args as Parameters<typeof console.error>)
  }

  const surErreur = (evenement: ErrorEvent) =>
    noter(`${evenement.message} (${evenement.filename}:${evenement.lineno})`)
  const surRejet = (evenement: PromiseRejectionEvent) =>
    noter(`Promesse rejetee : ${enTexte(evenement.reason)}`)

  window.addEventListener('error', surErreur)
  window.addEventListener('unhandledrejection', surRejet)

  return () => {
    console.error = originale
    window.removeEventListener('error', surErreur)
    window.removeEventListener('unhandledrejection', surRejet)
    installee = false
  }
}
```

- [x] **Étape 4 : relancer le test**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/erreurs-console.test.ts && npx tsc --noEmit
```

Attendu : VERT.

Si le troisième cas échoue parce que les erreurs des cas précédents se cumulent, c'est le test qui a raison : le module garde un état de module. Ajouter dans le fichier de test un `beforeEach` qui vide, non en exportant une fonction de remise à zéro pour la production, mais en désinstallant/réinstallant. Si cela ne suffit pas, exporter `viderErreurs()` et l'appeler dans `beforeEach`, avec un commentaire disant qu'elle n'existe que pour les tests.

- [x] **Étape 5 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/erreurs-console.ts ui-app/src/board/erreurs-console.test.ts
git commit -m "feat(rapport): garder les erreurs console recentes en memoire"
```

---

### Tâche 3 : le module de rapport, version objet

Le cœur. Pur, sans DOM, sans réseau : c'est lui qui décide CE QUE le rapport contient. La version texte vient à la tâche 4, sur le même objet.

**Fichiers :**
- Créer : `ui-app/src/board/rapport-bug.ts`
- Créer : `ui-app/src/board/rapport-bug.test.ts`

**Interfaces :**
- Consomme : `World`, `WorldCard` (`./world`), `Demande`, `Option` (`./ask`), `EntreeHistorique`, `MAX_ENTREES` (`./HistoriquePartie`).
- Produit :

```ts
export type PorteeRapport = 'recent' | 'tour' | 'partie'
export type ContexteRapport = { horodatage: string; siege?: number; campagne?: { id: string; scenario: string }; decouverte?: boolean; erreurs?: string[]; url?: string }
export type RapportBug = { format: 1; contexte: ContexteBug; demande: DemandeBug | null; table: TableBug; journal: EntreeBug[]; tronque: boolean }
export function construireRapport(monde: World, demande: Demande | undefined, entrees: EntreeHistorique[], portee: PorteeRapport, contexte: ContexteRapport): RapportBug
export function entreesDeLaPortee(entrees: EntreeHistorique[], portee: PorteeRapport, roundCourant: number): EntreeHistorique[]
```

- [x] **Étape 1 : écrire le test qui échoue**

Créer `ui-app/src/board/rapport-bug.test.ts` :

```ts
// Ce que le rapport doit contenir, et ce qu'il ne doit JAMAIS taire.
//
// Le piege principal : le journal est stocke du PLUS RECENT AU PLUS ANCIEN
// (ajouterNouvellesEntrees fait un unshift). Une portee « les 20 dernieres »
// ecrite avec slice(-20) rendrait le DEBUT de la partie, silencieusement.
import { describe, expect, it } from 'vitest'
import { construireRapport, entreesDeLaPortee } from './rapport-bug'
import { MAX_ENTREES, type EntreeHistorique } from './HistoriquePartie'
import type { Demande } from './ask'
import type { World, WorldCard } from './world'

const ZONES = {
  area_schemes_main: [], main_schemes_deck: [], area_schemes_side: [],
  additional_decks: [], additional_discard_piles: [], area_villain: [],
  villain_deck: [], encounter_deck: [], encounter_discard_pile: [],
  area_boost: [], area_environment: [], area_evidence: [], area_rule: [],
  area_processing: [], area_revealing: [], area_resources: [],
  area_removed: [], area_insert: [], area_set_aside: [],
  victory_display: [], area_status_cards: [], players: [],
  active_card_ids: [],
}

function carte(id: number, nom: string, cardId: string, type: string, info: Record<string, number> = {}): WorldCard {
  return {
    id, is_ready: true, is_face_up: true, visible_for_players: [0],
    bind_object_id: 0, name: nom, info, traits: {}, buffs: {},
    card_id: cardId, pic_id: cardId, down_card_ids: [], card_type: type,
    cost: 0, resources: [],
  }
}

const CONTEXTE = { horodatage: '2026-08-12T21:00:00.000Z', siege: 0 }

function monde(surcharge: Partial<World> = {}): World {
  return {
    render_id: 43, round_id: 3, phase: 'Player 1 Turn', prompt: '',
    event_name: 'PlayerOnEvent_Text', ...ZONES,
    area_schemes_main: [carte(48, 'None Shall Pass', '04079b', 'MainScheme', { k_threat: 2, target_threat: 12 })],
    area_villain: [carte(50, 'Absorbing Man', '04077a', 'EncounterVillain', { health: 14 })],
    ...surcharge,
  }
}

const entree = (round: number, titre: string, reste: Partial<EntreeHistorique> = {}): EntreeHistorique => ({
  cle: `${round}:${titre}`, type: 'text', renderId: round, round, phase: '', titre, ...reste,
})

describe('la portee', () => {
  // Le plus recent est en TETE : « les 20 dernieres » se prend au debut.
  const journal = [entree(3, 'c'), entree(3, 'b'), entree(2, 'a')]

  it('« recent » prend les 20 premieres, qui sont les plus recentes', () => {
    const long = Array.from({ length: 30 }, (_, i) => entree(3, `e${i}`))
    const pris = entreesDeLaPortee(long, 'recent', 3)
    expect(pris).toHaveLength(20)
    expect(pris[0]?.titre).toBe('e0')
  })

  it('« tour » ne garde que le round courant', () => {
    expect(entreesDeLaPortee(journal, 'tour', 3).map((e) => e.titre)).toEqual(['c', 'b'])
  })

  it('« partie » garde tout', () => {
    expect(entreesDeLaPortee(journal, 'partie', 3)).toHaveLength(3)
  })
})

describe('le rapport', () => {
  it("dit que le journal est tronque quand le tampon est plein", () => {
    const plein = Array.from({ length: MAX_ENTREES }, (_, i) => entree(3, `e${i}`))
    expect(construireRapport(monde(), undefined, plein, 'partie', CONTEXTE).tronque).toBe(true)
    expect(construireRapport(monde(), undefined, plein.slice(1), 'partie', CONTEXTE).tronque).toBe(false)
  })

  it("ne pretend jamais etre tronque sur une portee courte", () => {
    const plein = Array.from({ length: MAX_ENTREES }, (_, i) => entree(3, `e${i}`))
    expect(construireRapport(monde(), undefined, plein, 'recent', CONTEXTE).tronque).toBe(false)
  })

  it('donne a chaque carte son object id sous la forme visable en console', () => {
    const rapport = construireRapport(monde(), undefined, [], 'recent', CONTEXTE)
    const complot = rapport.table.cartes.find((c) => c.objet === 'c48')
    expect(complot).toMatchObject({ objet: 'c48', card_id: '04079b', nom: 'None Shall Pass', zone: 'complot principal', menace: 2 })
  })

  it('recopie les points de vie du vilain', () => {
    const rapport = construireRapport(monde(), undefined, [], 'recent', CONTEXTE)
    expect(rapport.table.cartes.find((c) => c.objet === 'c50')).toMatchObject({ vie: 14, zone: 'vilain' })
  })

  it("garde le texte brut du journal, identifiants compris", () => {
    const journal = [entree(3, 'Klaw would deal 2 damage', { brut: '[(50,01113) Klaw] would deal 2 damage' })]
    const rapport = construireRapport(monde(), undefined, journal, 'recent', CONTEXTE)
    expect(rapport.journal[0]?.texte).toBe('[(50,01113) Klaw] would deal 2 damage')
  })

  it("retombe sur le texte affiche quand l'entree n'a pas de brut", () => {
    const rapport = construireRapport(monde(), undefined, [entree(3, 'Ball and Chain joue')], 'recent', CONTEXTE)
    expect(rapport.journal[0]?.texte).toBe('Ball and Chain joue')
  })

  it('recopie la demande avec ses cibles legales et son cout', () => {
    const demande: Demande = {
      prompt_text: 'Choisissez une action', event_name: 'WhenPlayerInTurn',
      show_cancel: true, ability_type: 'Hero_Response',
      options: [{
        id: 12, name: 'p_Play', bind_id: 57, bind_player_id: 0,
        all_legal_targets: [48, 50], target_num_range: [1, 1],
        target_payment: { 0: { cost: '2', payment: [{ effect_id: 91, res_text: 'physical' }], rule: [] } },
        select_rule: '', target_must_include_traits: [], failure_reason: '', is_search: false,
      }],
    }
    const rapport = construireRapport(monde(), demande, [], 'recent', CONTEXTE)
    expect(rapport.demande).toMatchObject({ type: 'Hero_Response', evenement: 'WhenPlayerInTurn', annulable: true })
    expect(rapport.demande?.options[0]).toMatchObject({
      id: 12, nom: 'Play', porteePar: 'c57', cibles: ['c48', 'c50'],
      nombreDeCibles: [1, 1], cout: '2', injouable: null,
    })
  })

  it("nomme la raison quand une option est injouable", () => {
    const demande: Demande = {
      prompt_text: '', event_name: '', show_cancel: false, ability_type: '',
      options: [{
        id: 13, name: 'p_Attack', bind_id: 0, bind_player_id: 0,
        all_legal_targets: [], target_num_range: [0, 0], target_payment: {},
        select_rule: '', target_must_include_traits: [],
        failure_reason: 'not enough resources', is_search: false,
      }],
    }
    const rapport = construireRapport(monde(), demande, [], 'recent', CONTEXTE)
    expect(rapport.demande?.options[0]?.injouable).toBe('not enough resources')
  })

  it("rend une demande nulle quand le moteur n'attend rien", () => {
    expect(construireRapport(monde(), undefined, [], 'recent', CONTEXTE).demande).toBeNull()
  })

  it('nomme le mode campagne, le bac a sable et le nombre de sieges', () => {
    const table = monde({ mode_sandbox: true, players: [
      { area_hero: [carte(1, 'She-Hulk', '04001a', 'Hero', { health: 20 })], allies: [], supports: [], player_deck: [], player_discard_pile: [], dealt_encounter_cards: [], hand_cards: [], engaged_enemies: [], set_aside_nemesis_sets: [], set_aside_deck: [], additional_deck: [], additional_discard_pile: [], obligations_area: [], environment_area: [], resources: '', is_eliminated: false },
    ] })
    const rapport = construireRapport(table, undefined, [], 'recent', {
      ...CONTEXTE, campagne: { id: 'trors-1', scenario: 'crossbones' },
    })
    expect(rapport.contexte).toMatchObject({
      sandbox: true, sieges: 1, round: 3, phase: 'Player 1 Turn', render_id: 43,
      campagne: { id: 'trors-1', scenario: 'crossbones' },
      scenario: 'None Shall Pass', vilain: 'Absorbing Man',
    })
  })
})
```

- [x] **Étape 2 : lancer le test, vérifier qu'il échoue**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/rapport-bug.test.ts
```

Attendu : ROUGE, `Failed to resolve import "./rapport-bug"`.

- [x] **Étape 3 : écrire le module**

Créer `ui-app/src/board/rapport-bug.ts` :

```ts
// Le rapport de bug : ce que le plateau sait, mis sous une forme qu'on peut
// coller dans une conversation ou joindre a un fichier.
//
// Deux regles de conception, toutes les deux payees par l'experience :
//
// 1. LE RAPPORT NE NETTOIE RIEN. Le panneau « H » efface les identifiants
//    avant d'afficher, parce qu'il est ecrit pour etre LU. Ici c'est l'inverse :
//    l'object id (« c48 ») est la seule facon fiable de viser une carte depuis
//    la console. Par nom, l'etoile des cartes uniques (« * Blockbuster ») fait
//    tout echouer en silence. Par card_id, une carte ABSENTE du jeu est
//    fabriquee dans la zone mise de cote.
//
// 2. LE RAPPORT DIT CE QU'IL NE SAIT PAS. Un journal plafonne qui se lit comme
//    complet est pire qu'un journal absent : il fait chercher au mauvais
//    endroit. D'ou le drapeau `tronque`.
//
// Module PUR : ni DOM, ni reseau, ni horloge. L'horodatage arrive par le
// contexte, ce qui le rend testable.
import { MAX_ENTREES, type EntreeHistorique } from './HistoriquePartie'
import type { Demande, Option } from './ask'
import type { World, WorldCard } from './world'

export type PorteeRapport = 'recent' | 'tour' | 'partie'

/** Combien d'entrees rend la portee « recent ». */
const ENTREES_RECENTES = 20

export type ContexteRapport = {
  /** Date de la capture, en ISO. Passee de l'exterieur : le module reste pur. */
  horodatage: string
  /** Siege depuis lequel le rapport est pris. */
  siege?: number
  campagne?: { id: string; scenario: string }
  decouverte?: boolean
  /** Erreurs console relevees, de la plus ancienne a la plus recente. */
  erreurs?: string[]
  url?: string
}

export type CarteBug = {
  /** Object id sous la forme que la console attend : « c48 ». */
  objet: string
  card_id: string
  nom: string
  type: string
  zone: string
  joueur?: number
  vie?: number
  menace?: number
  /** false = engagee. */
  prete: boolean
  /** false = face cachee. */
  visible: boolean
  /** != 0 : attachee a cette carte. */
  attacheeA?: string
}

export type OptionBug = {
  id: number
  nom: string
  /** Carte porteuse de l'option, ou null si aucune. */
  porteePar: string | null
  cibles: string[]
  nombreDeCibles: [number, number]
  cout: string
  /** La raison donnee par le moteur, ou null si l'option est jouable. */
  injouable: string | null
}

export type DemandeBug = {
  intitule: string
  evenement: string
  type: string
  annulable: boolean
  options: OptionBug[]
}

export type EntreeBug = {
  round: number
  phase: string
  type: string
  /** Le texte BRUT quand il existe, sinon le texte affiche. */
  texte: string
  detail?: string
  cible?: string
}

export type ContexteBug = {
  horodatage: string
  scenario: string | null
  vilain: string | null
  heros: string[]
  sieges: number
  siege?: number
  round: number
  phase: string
  render_id: number
  sandbox: boolean
  decouverte: boolean
  campagne?: { id: string; scenario: string }
  fin?: string
  erreurs: string[]
  url?: string
}

export type TableBug = {
  cartes: CarteBug[]
  /** Ressources disponibles annoncees par le moteur, par siege. */
  ressources: string[]
  encounter_deck: number
  encounter_discard: number
}

export type RapportBug = {
  /** Version du format. Un rapport ancien doit rester identifiable. */
  format: 1
  contexte: ContexteBug
  demande: DemandeBug | null
  table: TableBug
  journal: EntreeBug[]
  /** Vrai quand le journal a pu perdre son debut. */
  tronque: boolean
}

const UNIT_TYPES = new Set(['Ally', 'Minion', 'EncounterVillain', 'Hero', 'AlterEgo'])
const SCHEME_TYPES = new Set(['MainScheme', 'EncounterSideScheme', 'PlayerSideScheme'])

function objet(id: number): string {
  return `c${id}`
}

function nombre(carte: WorldCard, cle: string): number | undefined {
  const valeur = carte.info[cle]
  return typeof valeur === 'number' ? valeur : undefined
}

function decrire(carte: WorldCard, zone: string, joueur?: number): CarteBug {
  return {
    objet: objet(carte.id),
    card_id: carte.card_id,
    nom: carte.name,
    type: carte.card_type,
    zone,
    joueur,
    vie: UNIT_TYPES.has(carte.card_type) ? nombre(carte, 'health') : undefined,
    menace: SCHEME_TYPES.has(carte.card_type) ? nombre(carte, 'k_threat') : undefined,
    prete: carte.is_ready,
    visible: carte.is_face_up,
    attacheeA: carte.bind_object_id ? objet(carte.bind_object_id) : undefined,
  }
}

function ajouter(sortie: CarteBug[], cartes: readonly WorldCard[] | undefined, zone: string, joueur?: number): void {
  if (!Array.isArray(cartes)) return
  for (const carte of cartes) sortie.push(decrire(carte, zone, joueur))
}

/**
 * Les entrees que la portee retient.
 *
 * Le journal est stocke du PLUS RECENT AU PLUS ANCIEN. « Les 20 dernieres » se
 * prend donc AU DEBUT du tableau : un slice(-20) rendrait le debut de la partie
 * en se lisant comme la fin.
 */
export function entreesDeLaPortee(
  entrees: EntreeHistorique[],
  portee: PorteeRapport,
  roundCourant: number
): EntreeHistorique[] {
  if (portee === 'partie') return [...entrees]
  if (portee === 'tour') return entrees.filter((e) => e.round === roundCourant)
  return entrees.slice(0, ENTREES_RECENTES)
}

function decrireOption(option: Option): OptionBug {
  // Le moteur prefixe ses options techniques par « p_ » et soude les mots par
  // des underscores : « p_Play », « Discard_a_status_card ». On rend le nom
  // lisible SANS le traduire : le rapport parle au developpeur, et le nom
  // moteur est ce qu'on retrouvera dans le code.
  const brut = option.name.startsWith('p_') ? option.name.slice(2) : option.name
  // La cle 0 de target_payment est le cout quand il n'y a pas de cible.
  const paiement = option.target_payment[0] ?? option.target_payment[option.all_legal_targets[0] ?? -1]
  return {
    id: option.id,
    nom: brut.replaceAll('_', ' ').trim(),
    porteePar: option.bind_id ? objet(option.bind_id) : null,
    cibles: option.all_legal_targets.map(objet),
    nombreDeCibles: option.target_num_range,
    cout: paiement?.cost ?? '',
    injouable: option.failure_reason ? option.failure_reason : null,
  }
}

function decrireTable(monde: World): TableBug {
  const cartes: CarteBug[] = []
  ajouter(cartes, monde.area_schemes_main, 'complot principal')
  ajouter(cartes, monde.area_schemes_side, 'complot annexe')
  ajouter(cartes, monde.area_villain, 'vilain')
  ajouter(cartes, monde.area_environment, 'environnement')
  ajouter(cartes, monde.area_boost, 'boost')
  ajouter(cartes, monde.area_revealing, 'en revelation')
  ajouter(cartes, monde.area_processing, 'en resolution')
  ajouter(cartes, monde.area_status_cards, 'statut')
  ajouter(cartes, monde.area_evidence, 'preuve')
  ajouter(cartes, monde.area_set_aside, 'mise de cote')
  ajouter(cartes, monde.area_removed, 'retiree du jeu')
  ajouter(cartes, monde.victory_display, 'zone de victoire')
  ajouter(cartes, monde.encounter_discard_pile, 'defausse rencontre')

  for (const [siege, joueur] of (monde.players ?? []).entries()) {
    ajouter(cartes, joueur.area_hero, 'identite', siege)
    ajouter(cartes, joueur.allies, 'allies', siege)
    ajouter(cartes, joueur.supports, 'soutiens', siege)
    ajouter(cartes, joueur.engaged_enemies, 'ennemis engages', siege)
    ajouter(cartes, joueur.obligations_area, 'obligations', siege)
    ajouter(cartes, joueur.environment_area, 'environnement joueur', siege)
    ajouter(cartes, joueur.hand_cards, 'main', siege)
    ajouter(cartes, joueur.reserve, 'reserve', siege)
    ajouter(cartes, joueur.player_discard_pile, 'defausse', siege)
    ajouter(cartes, joueur.dealt_encounter_cards, 'rencontre attribuee', siege)
    ajouter(cartes, joueur.additional_deck, 'deck supplementaire', siege)
    ajouter(cartes, joueur.additional_discard_pile, 'defausse supplementaire', siege)
    ajouter(cartes, joueur.set_aside_deck, 'mise de cote joueur', siege)
  }

  return {
    cartes,
    ressources: (monde.players ?? []).map((joueur) => joueur.resources),
    encounter_deck: monde.encounter_deck?.length ?? 0,
    encounter_discard: monde.encounter_discard_pile?.length ?? 0,
  }
}

export function construireRapport(
  monde: World,
  demande: Demande | undefined,
  entrees: EntreeHistorique[],
  portee: PorteeRapport,
  contexte: ContexteRapport
): RapportBug {
  const retenues = entreesDeLaPortee(entrees, portee, monde.round_id)

  return {
    format: 1,
    contexte: {
      horodatage: contexte.horodatage,
      scenario: monde.area_schemes_main?.[0]?.name ?? null,
      vilain: monde.area_villain?.[0]?.name ?? null,
      heros: (monde.players ?? []).map((joueur) => joueur.area_hero?.[0]?.name ?? '?'),
      sieges: (monde.players ?? []).length,
      siege: contexte.siege,
      round: monde.round_id,
      phase: monde.phase,
      render_id: monde.render_id,
      sandbox: monde.mode_sandbox === true,
      decouverte: contexte.decouverte === true,
      campagne: contexte.campagne,
      fin: monde.game_over ? (monde.game_over_reason ?? 'partie terminee') : undefined,
      erreurs: contexte.erreurs ?? [],
      url: contexte.url,
    },
    demande: demande
      ? {
          intitule: demande.prompt_text,
          evenement: demande.event_name,
          type: demande.ability_type,
          annulable: demande.show_cancel,
          options: demande.options.map(decrireOption),
        }
      : null,
    table: decrireTable(monde),
    journal: retenues.map((e) => ({
      round: e.round,
      phase: e.phase,
      type: e.type,
      texte: e.brut && e.brut.length > 0 ? e.brut : e.titre,
      detail: e.detail,
      cible: e.cibleId !== undefined ? objet(e.cibleId) : undefined,
    })),
    // Le tampon plein signifie que des entrees ont ete jetees par le bas. La
    // question ne se pose que sur « toute la partie » : une portee courte ne
    // pretend rien couvrir d'autre qu'elle-meme.
    tronque: portee === 'partie' && entrees.length >= MAX_ENTREES,
  }
}
```

- [x] **Étape 4 : relancer le test**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/rapport-bug.test.ts && npx tsc --noEmit
```

Attendu : VERT.

- [x] **Étape 5 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/rapport-bug.ts ui-app/src/board/rapport-bug.test.ts
git commit -m "feat(rapport): le module qui assemble l'etat de la partie"
```

---

### Tâche 4 : la version texte

Celle qui doit être collable. La contrainte réelle est le volume : sur la portée « recent », le texte doit tenir dans un message.

**Fichiers :**
- Modifier : `ui-app/src/board/rapport-bug.ts` (ajout de `rapportEnTexte` et `nomFichierRapport`)
- Modifier : `ui-app/src/board/rapport-bug.test.ts` (ajout d'un bloc `describe`)

**Interfaces :**
- Consomme : `RapportBug` de la tâche 3.
- Produit : `rapportEnTexte(rapport: RapportBug): string`, `nomFichierRapport(rapport: RapportBug): string`.

- [x] **Étape 1 : écrire le test qui échoue**

Ajouter à la fin de `ui-app/src/board/rapport-bug.test.ts` :

```ts
describe('la version texte', () => {
  const base = () => construireRapport(monde(), undefined, [], 'recent', CONTEXTE)

  it('donne les object id, pas seulement les noms', () => {
    const texte = rapportEnTexte(base())
    expect(texte).toContain('c48')
    expect(texte).toContain('None Shall Pass')
    expect(texte).toContain('04079b')
  })

  it("rappelle qu'une commande se vise par object id", () => {
    expect(rapportEnTexte(base())).toContain('object id')
  })

  it('AVERTIT quand le journal est tronque', () => {
    const plein = Array.from({ length: MAX_ENTREES }, (_, i) => entree(3, `e${i}`))
    const texte = rapportEnTexte(construireRapport(monde(), undefined, plein, 'partie', CONTEXTE))
    expect(texte).toContain('tronqu')
  })

  it("ne parle pas de troncature quand il n'y en a pas", () => {
    expect(rapportEnTexte(base()).toLowerCase()).not.toContain('tronqu')
  })

  it('avertit que le rapport contient les mains de tous les sieges', () => {
    expect(rapportEnTexte(base())).toContain('mains de tous les sieges')
  })

  it("dit quand le moteur n'attend rien", () => {
    expect(rapportEnTexte(base())).toContain('Aucune demande en cours')
  })

  it('nomme le fichier avec le scenario et le round', () => {
    expect(nomFichierRapport(base())).toBe('rapport-none-shall-pass-r3.json')
  })

  it('nomme le fichier sans scenario quand la table est vide', () => {
    const vide = construireRapport(monde({ area_schemes_main: [] }), undefined, [], 'recent', CONTEXTE)
    expect(nomFichierRapport(vide)).toBe('rapport-partie-r3.json')
  })
})
```

Ajouter `rapportEnTexte, nomFichierRapport` à l'import en tête du fichier de test.

- [x] **Étape 2 : lancer le test, vérifier qu'il échoue**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/rapport-bug.test.ts
```

Attendu : ROUGE, `rapportEnTexte is not a function` (ou une erreur d'import).

- [x] **Étape 3 : écrire les deux fonctions**

Ajouter à la fin de `ui-app/src/board/rapport-bug.ts` :

```ts
/**
 * Le rappel qui accompagne chaque rapport. Il ne coute que trois lignes et il
 * evite la perte de temps la mieux documentee du projet : viser une carte
 * autrement que par son object id.
 */
const RAPPEL =
  'Une commande de console se vise par object id (« c48 »). Par nom, ' +
  "l'etoile des cartes uniques fait tout echouer en silence ; par card_id, une " +
  'carte absente du jeu est fabriquee dans la zone mise de cote.'

function ligneCarte(carte: CarteBug): string {
  const etats = [
    carte.vie !== undefined ? `${carte.vie} PV` : undefined,
    carte.menace !== undefined ? `${carte.menace} menace` : undefined,
    carte.prete ? undefined : 'engagee',
    carte.visible ? undefined : 'face cachee',
    carte.attacheeA ? `attachee a ${carte.attacheeA}` : undefined,
  ].filter((e): e is string => e !== undefined)
  const siege = carte.joueur !== undefined ? ` P${carte.joueur + 1}` : ''
  const suffixe = etats.length > 0 ? ` [${etats.join(', ')}]` : ''
  return `  ${carte.objet} ${carte.nom} (${carte.card_id}, ${carte.type})${siege}${suffixe}`
}

function ligneOption(option: OptionBug): string {
  const morceaux = [
    option.porteePar ? `portee par ${option.porteePar}` : undefined,
    option.cibles.length > 0 ? `cibles ${option.nombreDeCibles[0]}..${option.nombreDeCibles[1]} parmi ${option.cibles.join(' ')}` : undefined,
    option.cout ? `cout ${option.cout}` : undefined,
    option.injouable ? `INJOUABLE : ${option.injouable}` : undefined,
  ].filter((m): m is string => m !== undefined)
  return `  [${option.id}] ${option.nom}${morceaux.length > 0 ? ' — ' + morceaux.join(' ; ') : ''}`
}

export function rapportEnTexte(rapport: RapportBug): string {
  const c = rapport.contexte
  const lignes: string[] = []

  lignes.push('=== RAPPORT DE BUG — Marvel Champions ===')
  lignes.push(`Pris le ${c.horodatage}`)
  lignes.push('')
  lignes.push('--- CONTEXTE ---')
  lignes.push(`Scenario : ${c.scenario ?? '?'}${c.vilain ? ` (vilain : ${c.vilain})` : ''}`)
  lignes.push(`Heros : ${c.heros.length > 0 ? c.heros.map((h, i) => `P${i + 1} ${h}`).join(', ') : 'aucun'}`)
  lignes.push(`Round ${c.round}, phase « ${c.phase} », render_id ${c.render_id}`)
  const modes = [
    `${c.sieges} siege(s)`,
    c.siege !== undefined ? `rapport pris depuis P${c.siege + 1}` : undefined,
    c.sandbox ? 'bac a sable' : undefined,
    c.decouverte ? 'mode Decouverte' : undefined,
    c.campagne ? `campagne ${c.campagne.id}, scenario ${c.campagne.scenario}` : undefined,
    c.fin ? `PARTIE TERMINEE : ${c.fin}` : undefined,
  ].filter((m): m is string => m !== undefined)
  lignes.push(`Mode : ${modes.join(' ; ')}`)
  if (c.url) lignes.push(`Page : ${c.url}`)
  if (c.erreurs.length > 0) {
    lignes.push(`Erreurs console (${c.erreurs.length}) :`)
    for (const erreur of c.erreurs) lignes.push(`  ${erreur}`)
  }

  lignes.push('')
  lignes.push('--- DEMANDE EN COURS ---')
  if (rapport.demande === null) {
    lignes.push('Aucune demande en cours : le moteur ne nous attend pas.')
  } else {
    const d = rapport.demande
    lignes.push(`Intitule : ${d.intitule || '(vide)'}`)
    lignes.push(`Type ${d.type || '?'}, evenement ${d.evenement || '?'}, annulable : ${d.annulable ? 'oui' : 'non'}`)
    lignes.push(d.options.length > 0 ? 'Options :' : 'Aucune option proposee.')
    for (const option of d.options) lignes.push(ligneOption(option))
  }

  lignes.push('')
  lignes.push('--- TABLE ---')
  lignes.push(`Deck rencontre : ${rapport.table.encounter_deck} cartes ; defausse rencontre : ${rapport.table.encounter_discard}`)
  rapport.table.ressources.forEach((ressources, siege) => {
    lignes.push(`Ressources P${siege + 1} : ${ressources || '(aucune)'}`)
  })
  for (const carte of rapport.table.cartes) lignes.push(ligneCarte(carte))

  lignes.push('')
  lignes.push(`--- JOURNAL (${rapport.journal.length} entrees, de la plus recente a la plus ancienne) ---`)
  for (const entree of rapport.journal) {
    const cible = entree.cible ? ` {${entree.cible}}` : ''
    const detail = entree.detail ? ` — ${entree.detail}` : ''
    lignes.push(`R${entree.round} [${entree.type}]${cible} ${entree.texte}${detail}`)
  }
  if (rapport.tronque) {
    lignes.push('')
    lignes.push(`⚠ Journal TRONQUE : le tampon est plafonne a ${MAX_ENTREES} entrees, le debut de la partie a ete perdu.`)
  }

  lignes.push('')
  lignes.push('--- A SAVOIR ---')
  lignes.push(RAPPEL)
  lignes.push('Ce rapport contient les mains de tous les sieges : il decrit la table entiere, pas seulement ce que ce siege joue.')

  return lignes.join('\n')
}

/**
 * Nom du fichier telecharge. Le scenario et le round suffisent a distinguer
 * deux rapports pris dans la meme soiree, et evitent le « rapport (3).json »
 * du navigateur.
 */
export function nomFichierRapport(rapport: RapportBug): string {
  const base = (rapport.contexte.scenario ?? 'partie')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
  return `rapport-${base || 'partie'}-r${rapport.contexte.round}.json`
}
```

- [x] **Étape 4 : relancer le test**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/rapport-bug.test.ts && npx tsc --noEmit
```

Attendu : VERT.

- [x] **Étape 5 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/rapport-bug.ts ui-app/src/board/rapport-bug.test.ts
git commit -m "feat(rapport): la version texte, collable et honnete sur ce qu'elle ignore"
```

---

### Tâche 5 : les boutons et le sélecteur de portée

La couche React. Elle ne DÉCIDE rien : elle appelle le module et pousse le résultat vers le presse-papier ou vers un fichier.

**Fichiers :**
- Créer : `ui-app/src/board/RapportBug.tsx`
- Créer : `ui-app/src/board/RapportBug.test.tsx`
- Modifier : `ui-app/src/board/dico-en.ts`

**Interfaces :**
- Consomme : `construireRapport`, `rapportEnTexte`, `nomFichierRapport`, `PorteeRapport` (tâches 3 et 4) ; `erreursRecentes` (tâche 2) ; `lireContexte` (`./campagne/contexte`) ; `CLE_TUTORIEL` (`./CoucheCoach`).
- Produit :

```ts
export type OutilsRapport = { copier: (portee: PorteeRapport) => Promise<void>; telecharger: (portee: PorteeRapport) => void; message: string | null }
export function MessageRapport({ message }: { message: string | null }): JSX.Element | null
export function useRapportBug(monde: World | undefined, demande: Demande | undefined, entrees: EntreeHistorique[], siege?: number): OutilsRapport
export function BoutonsRapportBug({ outils }: { outils: OutilsRapport }): JSX.Element
```

- [x] **Étape 1 : écrire le test qui échoue**

Créer `ui-app/src/board/RapportBug.test.tsx` :

```tsx
// Les boutons ne decident rien : ils appellent le module et poussent le
// resultat dehors. Ce qui se teste ici, c'est donc le CHEMIN — que le texte
// parte vraiment au presse-papier, que le fichier porte le bon nom, et qu'un
// refus du navigateur se DISE au lieu de passer pour un succes.
import { describe, expect, it, vi, beforeEach } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { renderHook } from '@testing-library/react'
import { BoutonsRapportBug, useRapportBug } from './RapportBug'
import type { World } from './world'

const ZONES = {
  area_schemes_main: [], main_schemes_deck: [], area_schemes_side: [],
  additional_decks: [], additional_discard_piles: [], area_villain: [],
  villain_deck: [], encounter_deck: [], encounter_discard_pile: [],
  area_boost: [], area_environment: [], area_evidence: [], area_rule: [],
  area_processing: [], area_revealing: [], area_resources: [],
  area_removed: [], area_insert: [], area_set_aside: [],
  victory_display: [], area_status_cards: [], players: [],
  active_card_ids: [],
}

const MONDE: World = {
  render_id: 43, round_id: 3, phase: 'Player 1 Turn', prompt: '',
  event_name: 'PlayerOnEvent_Text', ...ZONES,
}

beforeEach(() => {
  window.sessionStorage.clear()
  window.localStorage.clear()
})

describe('les outils de rapport', () => {
  it('copie le texte dans le presse-papier', async () => {
    const ecrire = vi.fn().mockResolvedValue(undefined)
    Object.defineProperty(navigator, 'clipboard', { value: { writeText: ecrire }, configurable: true })

    const { result } = renderHook(() => useRapportBug(MONDE, undefined, [], 0))
    await act(async () => result.current.copier('recent'))

    expect(ecrire).toHaveBeenCalledOnce()
    expect(String(ecrire.mock.calls[0]?.[0])).toContain('RAPPORT DE BUG')
    expect(result.current.message).toBe('Rapport copié')
  })

  it('DIT quand le navigateur refuse la copie', async () => {
    const ecrire = vi.fn().mockRejectedValue(new Error('refus'))
    Object.defineProperty(navigator, 'clipboard', { value: { writeText: ecrire }, configurable: true })

    const { result } = renderHook(() => useRapportBug(MONDE, undefined, [], 0))
    await act(async () => result.current.copier('recent'))

    expect(result.current.message).toBe('Copie refusée par le navigateur')
  })

  it('ne fait rien tant que le monde n\'est pas charge', async () => {
    const ecrire = vi.fn().mockResolvedValue(undefined)
    Object.defineProperty(navigator, 'clipboard', { value: { writeText: ecrire }, configurable: true })

    const { result } = renderHook(() => useRapportBug(undefined, undefined, [], 0))
    await act(async () => result.current.copier('recent'))

    expect(ecrire).not.toHaveBeenCalled()
  })
})

describe('le panneau', () => {
  it('offre les trois portees et les deux sorties', () => {
    const outils = { copier: vi.fn().mockResolvedValue(undefined), telecharger: vi.fn(), message: null }
    render(<BoutonsRapportBug outils={outils} />)

    expect(screen.getByRole('button', { name: /Copier/ })).toBeTruthy()
    expect(screen.getByRole('button', { name: /Télécharger/ })).toBeTruthy()
    const selecteur = screen.getByLabelText(/Profondeur/) as HTMLSelectElement
    expect([...selecteur.options].map((o) => o.value)).toEqual(['recent', 'tour', 'partie'])
  })

  it('passe la portee choisie a la sortie', async () => {
    const outils = { copier: vi.fn().mockResolvedValue(undefined), telecharger: vi.fn(), message: null }
    render(<BoutonsRapportBug outils={outils} />)

    const selecteur = screen.getByLabelText(/Profondeur/) as HTMLSelectElement
    await act(async () => {
      selecteur.value = 'partie'
      selecteur.dispatchEvent(new Event('change', { bubbles: true }))
    })
    await act(async () => void screen.getByRole('button', { name: /Copier/ }).click())

    expect(outils.copier).toHaveBeenCalledWith('partie')
  })
})
```

- [x] **Étape 2 : lancer le test, vérifier qu'il échoue**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/RapportBug.test.tsx
```

Attendu : ROUGE, `Failed to resolve import "./RapportBug"`.

- [x] **Étape 3 : écrire le composant**

Créer `ui-app/src/board/RapportBug.tsx` :

```tsx
// Les deux sorties du rapport de bug : le presse-papier et un fichier.
//
// La capture se fait AU CLIC (decision du 12/8/2026) : le rapport lit le monde
// et la demande du moment. Le journal, lui, couvre deja le passe. Aucun tampon
// d'etats n'est garde, donc aucun cout memoire.
//
// Le message rendu par le crochet est volontairement le meme pour le panneau et
// pour le raccourci clavier : capturer sans ouvrir le panneau doit quand meme
// se voir, sinon on ne sait pas si le geste a pris.
import { useCallback, useRef, useState } from 'react'
import { CLE_TUTORIEL } from './CoucheCoach'
import { lireContexte } from './campagne/contexte'
import { erreursRecentes } from './erreurs-console'
import { t } from './langue'
import type { Demande } from './ask'
import type { EntreeHistorique } from './HistoriquePartie'
import {
  construireRapport,
  nomFichierRapport,
  rapportEnTexte,
  type PorteeRapport,
  type RapportBug as Rapport,
} from './rapport-bug'
import type { World } from './world'

export type OutilsRapport = {
  copier: (portee: PorteeRapport) => Promise<void>
  telecharger: (portee: PorteeRapport) => void
  /** Confirmation transitoire, ou null. Affichee aussi hors du panneau. */
  message: string | null
}

const DUREE_MESSAGE = 4000

function enModeDecouverte(): boolean {
  try {
    return window.localStorage.getItem(CLE_TUTORIEL) !== null
  } catch {
    return false
  }
}

function contexteCampagne(): { id: string; scenario: string } | undefined {
  const contexte = lireContexte()
  return contexte ? { id: contexte.id, scenario: contexte.scenario } : undefined
}

export function useRapportBug(
  monde: World | undefined,
  demande: Demande | undefined,
  entrees: EntreeHistorique[],
  siege?: number
): OutilsRapport {
  const [message, setMessage] = useState<string | null>(null)
  const minuterie = useRef<number | undefined>(undefined)

  const annoncer = useCallback((texte: string) => {
    setMessage(texte)
    window.clearTimeout(minuterie.current)
    minuterie.current = window.setTimeout(() => setMessage(null), DUREE_MESSAGE)
  }, [])

  const construire = useCallback(
    (portee: PorteeRapport): Rapport | null => {
      if (!monde) return null
      return construireRapport(monde, demande, entrees, portee, {
        horodatage: new Date().toISOString(),
        siege,
        campagne: contexteCampagne(),
        decouverte: enModeDecouverte(),
        erreurs: erreursRecentes(),
        url: window.location.href,
      })
    },
    [monde, demande, entrees, siege]
  )

  // Rend une promesse : sans elle, un test ne peut pas attendre la fin de
  // l'ecriture, et l'appelant clavier n'a aucun moyen de savoir que c'est fini.
  const copier = useCallback(
    async (portee: PorteeRapport) => {
      const rapport = construire(portee)
      if (!rapport) return
      // Le presse-papier peut etre refuse (page non securisee, permission
      // retiree). Un echec silencieux ferait croire a une copie reussie et
      // ferait coller le presse-papier PRECEDENT.
      try {
        await navigator.clipboard.writeText(rapportEnTexte(rapport))
        annoncer(t('Rapport copié'))
      } catch {
        annoncer(t('Copie refusée par le navigateur'))
      }
    },
    [construire, annoncer]
  )

  const telecharger = useCallback(
    (portee: PorteeRapport) => {
      const rapport = construire(portee)
      if (!rapport) return
      const contenu = new Blob([JSON.stringify(rapport, null, 1)], { type: 'application/json' })
      const url = URL.createObjectURL(contenu)
      const lien = document.createElement('a')
      lien.href = url
      lien.download = nomFichierRapport(rapport)
      lien.click()
      URL.revokeObjectURL(url)
      annoncer(t('Rapport téléchargé'))
    },
    [construire, annoncer]
  )

  return { copier, telecharger, message }
}

const PORTEES: Array<{ valeur: PorteeRapport; libelle: string }> = [
  { valeur: 'recent', libelle: '20 dernières' },
  { valeur: 'tour', libelle: 'Ce tour' },
  { valeur: 'partie', libelle: 'Toute la partie' },
]

export function BoutonsRapportBug({ outils }: { outils: OutilsRapport }) {
  const [portee, setPortee] = useState<PorteeRapport>('recent')

  return (
    <div className="hp-rapport">
      <label className="hp-rapport-portee">
        {t('Profondeur')}
        <select value={portee} onChange={(e) => setPortee(e.target.value as PorteeRapport)}>
          {PORTEES.map(({ valeur, libelle }) => (
            <option key={valeur} value={valeur}>
              {t(libelle)}
            </option>
          ))}
        </select>
      </label>
      <button type="button" onClick={() => outils.copier(portee)} title={t('Copier un rapport de bug')}>
        {t('Copier')}
      </button>
      <button type="button" onClick={() => outils.telecharger(portee)} title={t('Télécharger le rapport complet')}>
        {t('Télécharger')}
      </button>
    </div>
  )
}

/** Confirmation transitoire, visible meme quand le panneau est ferme. */
export function MessageRapport({ message }: { message: string | null }) {
  if (!message) return null
  return (
    <span className="hp-rapport-message" role="status" aria-live="polite">
      {message}
    </span>
  )
}
```

- [x] **Étape 4 : ajouter les chaînes au dictionnaire**

Dans `ui-app/src/board/dico-en.ts`, ajouter dans `DICO_EN_BASE`, sous un commentaire de section :

```ts
  // ---- Rapport de bug (panneau H) ----
  'Profondeur': 'Depth',
  '20 dernières': 'Last 20',
  'Ce tour': 'This round',
  'Toute la partie': 'Whole game',
  'Copier': 'Copy',
  'Télécharger': 'Download',
  'Copier un rapport de bug': 'Copy a bug report',
  'Télécharger le rapport complet': 'Download the full report',
  'Rapport copié': 'Report copied',
  'Rapport téléchargé': 'Report downloaded',
  'Copie refusée par le navigateur': 'Copy refused by the browser',
```

Vérifier avant d'ajouter que `'Copier'` et `'Télécharger'` ne sont pas déjà présents (`grep -n "'Copier'\|'Télécharger'" src/board/dico-en.ts`). S'ils le sont, ne pas les redoubler : une clé en double est une erreur TypeScript.

- [x] **Étape 5 : relancer le test**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run src/board/RapportBug.test.tsx && npx tsc --noEmit
```

Attendu : VERT.

- [x] **Étape 6 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board/RapportBug.tsx ui-app/src/board/RapportBug.test.tsx ui-app/src/board/dico-en.ts
git commit -m "feat(rapport): copier et telecharger, avec le choix de la profondeur"
```

---

### Tâche 6 : le branchement dans le plateau

Là où tout se rejoint : le panneau « H » reçoit les boutons, le raccourci `B` capture sans l'ouvrir, et la collecte d'erreurs s'installe au montage.

**Fichiers :**
- Modifier : `ui-app/src/board/HistoriquePartie.tsx` (le composant `HistoriquePartie` reçoit et rend les boutons)
- Modifier : `ui-app/src/board.tsx` (crochet, raccourci `B`, collecte d'erreurs, passage des props)
- Modifier : `ui-app/src/board/board.css` (les trois classes `hp-rapport*`)

**Interfaces :**
- Consomme : `useRapportBug`, `BoutonsRapportBug`, `MessageRapport`, `OutilsRapport` (tâche 5) ; `installerCollecteErreurs` (tâche 2).
- Produit : rien de consommé plus loin. C'est la fin de la chaîne.

- [x] **Étape 1 : le panneau accepte les boutons**

Dans `HistoriquePartie.tsx`, importer en tête :

```ts
import { BoutonsRapportBug, type OutilsRapport } from './RapportBug'
```

Changer la signature du composant :

```tsx
export function HistoriquePartie({
  entrees,
  effacer,
  rapport,
}: {
  entrees: EntreeHistorique[]
  effacer: () => void
  /** Absent hors partie : le panneau se contente alors du bouton « Effacer ». */
  rapport?: OutilsRapport
}) {
```

Et dans le `<header className="hp-entete">`, remplacer le bloc du bouton « Effacer » par :

```tsx
            <div className="hp-entete-actions">
              {rapport ? <BoutonsRapportBug outils={rapport} /> : null}
              <button type="button" onClick={effacer} disabled={entrees.length === 0}>
                {t('Effacer')}
              </button>
            </div>
```

- [x] **Étape 2 : brancher le plateau**

Dans `ui-app/src/board.tsx` :

a) importer, à côté des autres imports de `./board/` :

```ts
import { installerCollecteErreurs } from './board/erreurs-console'
import { MessageRapport, useRapportBug } from './board/RapportBug'
```

b) juste après la ligne `const historique = useHistoriquePartie(etat.monde, etat.demande, etat.partieId)` (ligne 1611), ajouter :

```ts
  // Le rapport de bug. Il ne capture qu'AU CLIC : il lit le monde et la demande
  // du moment, et le journal ci-dessus pour le passe.
  const rapport = useRapportBug(etat.monde, etat.demande, historique.entrees, etat.joueurDemande)
```

c) dans l'effet des raccourcis clavier (ligne 1793), ajouter une branche après celle de `u` :

```ts
      } else if (touche === 'b') {
        // « B » comme bug : copie les 20 dernieres entrees sans ouvrir le
        // panneau, parce que le symptome peut disparaitre au rendu suivant.
        rapportClavier.current()
      }
```

et déclarer, à côté de `finTourClavier` :

```ts
  // Meme mecanique que finTourClavier : le raccourci est installe une fois, sa
  // cible change a chaque rendu. Sans le ref, l'ecoute se reinstallerait a
  // chaque monde recu.
  const rapportClavier = useRef<() => void>(() => {})
```

puis, après la déclaration de `rapport` :

```ts
  rapportClavier.current = () => void rapport.copier('recent')
```

d) installer la collecte d'erreurs. Ajouter un effet à côté des autres effets de haut niveau :

```ts
  // Installee une fois pour la vie de la page : une erreur de rendu survenue
  // avant l'ouverture du panneau doit quand meme figurer au rapport.
  useEffect(() => installerCollecteErreurs(), [])
```

e) passer le rapport au panneau (ligne 2073) :

```tsx
            <HistoriquePartie entrees={historique.entrees} effacer={historique.effacer} rapport={rapport} />
            <MessageRapport message={rapport.message} />
```

- [x] **Étape 3 : habiller**

Dans `ui-app/src/board/board.css`, à côté des règles `.hp-entete` existantes :

```css
.hp-entete-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hp-rapport {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
}

.hp-rapport-portee {
  display: flex;
  align-items: center;
  gap: 4px;
}

.hp-rapport-message {
  font-size: 12px;
  opacity: 0.85;
  padding-inline: 6px;
}
```

- [x] **Étape 4 : vérifier que rien n'est cassé**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"
npx vitest run && npx tsc --noEmit
```

Attendu : VERT, et le nombre de cas doit avoir AUGMENTÉ par rapport aux 365 de la session précédente (les tâches 1 à 5 en ajoutent). Si un test de `Board.test.tsx` casse, c'est le branchement qui est en cause, pas le test.

- [x] **Étape 5 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add ui-app/src/board.tsx ui-app/src/board/HistoriquePartie.tsx ui-app/src/board/board.css
git commit -m "feat(rapport): le panneau H et le raccourci B sortent le rapport"
```

---

### Tâche 7 : déployer et éprouver en vraie partie

Un rapport qui n'a jamais été pris sur une vraie partie ne prouve rien. C'est la seule étape qui demande un navigateur.

**Fichiers :**
- Modifier : `.twei/SESSION.md`, `.planning/STATE.md`, `.planning/todos/2026-08-12-rapport-de-bug.md` (statut)

- [ ] **Étape 1 : déployer**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
bash ui-app/deployer.sh
```

Attendu : le build passe, le garde-fou de sortie ne signale rien, la recopie vers `~/marvel-work/fusion/marvel-lcg-src/public/app/` puis vers le dépôt se fait.

- [ ] **Étape 2 : lancer le serveur de dev et une partie**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
~/marvel-work/python/bin/python3.10 ui-check/scripts/serveur-dev.py --port 2346
```

Ouvrir le plateau, lancer une partie (n'importe quel héros contre Rhino suffit), jouer deux ou trois cartes.

- [ ] **Étape 3 : les quatre vérifications**

1. Ouvrir le panneau « H », choisir « 20 dernières », cliquer « Copier ». Coller ailleurs : le texte doit contenir au moins un `c<nombre>`, le nom du scénario, et la section « DEMANDE EN COURS » renseignée si le moteur attend une réponse.
2. Appuyer sur `B` panneau FERMÉ. La confirmation « Rapport copié » doit s'afficher, et le presse-papier changer.
3. Choisir « Toute la partie », cliquer « Télécharger ». Le fichier doit s'appeler `rapport-<scenario>-r<n>.json` et s'ouvrir sans erreur de syntaxe.
4. Cliquer dans un champ de saisie (le panneau des sauvegardes) et taper `b`. Le rapport NE DOIT PAS partir : la garde `INPUT/TEXTAREA` de l'effet clavier doit tenir.

- [ ] **Étape 4 : mesurer le tampon (point §4.5 de la fiche)**

Sur la partie en cours, ouvrir la console du navigateur et lire le compteur du bouton « H » (`<em>{entrees.length}</em>`). Noter combien d'entrées une partie normale produit par round. Si le compteur atteint 400 avant la fin de la partie, la portée « toute la partie » perd le début, et le rapport le DIT déjà (`tronque`). Écrire le chiffre mesuré dans `.twei/SESSION.md` : c'est la réponse à la question laissée ouverte par la fiche.

- [ ] **Étape 5 : mettre les documents à l'état mesuré**

- `.planning/todos/2026-08-12-rapport-de-bug.md` : passer le statut à `**IMPLÉMENTÉ** le 2026-08-12`, et corriger les trois points que la mesure a démentis (voir la section « Ce que la mesure a corrigé dans la spec » en tête de ce plan).
- `.twei/SESSION.md` : ce qui a été fait, le chiffre du tampon, et les pièges rencontrés.
- `.planning/STATE.md` : la continuité de session.

- [ ] **Étape 6 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git add .twei/SESSION.md .planning/STATE.md .planning/todos/2026-08-12-rapport-de-bug.md .planning/plans/2026-08-12-rapport-de-bug.md
git commit -m "docs(rapport): le rapport de bug est pris sur une vraie partie"
```

---

## Ce qui reste hors de ce plan, et pourquoi

- **Le re-zip vers `Fusion/`.** Le livrable n'a pas été re-zippé depuis les correctifs du 28/07 ; ce chantier ne change pas cette dette, et l'y mêler brouillerait le commit.
- **Un rapport limité au siège.** Décidé : rapport complet avec avertissement. Si le besoin de partager un rapport à un tiers apparaît, c'est un autre chantier (filtrage par `visible_for_players`).
- **Rejouer un rapport.** La fiche parle d'un objectif déclaré « pouvoir rejouer ou au moins reconstituer ». Ce plan livre la RECONSTITUTION. Rejouer demanderait de reposer un monde dans le moteur, ce qui est un sujet à part entière.


---

## Journal d'exécution (12/08/2026)

**Tâches 1 à 6 faites**, six commits, `b3d50d1` à `c8d94ce`. Vérifications lancées
et lues : `npx vitest run` **408 cas verts** (365 avant, 43 ajoutés),
`npx tsc --noEmit` sans erreur, `npx vite build` sans erreur.

### Le piège payé, à ne pas réapprendre

**Un monde construit DANS le callback de `renderHook` fait exploser le tas.**
Premier jet du test de la tâche 1 : `renderHook(() => useHistoriquePartie(monde('...'), ...))`.
`monde()` rend un objet neuf à chaque rendu, l'effet dépend de `[monde, ...]`, il
se relance, appelle `setEntrees`, qui redessine, qui reconstruit un objet neuf.
Résultat : `FATAL ERROR: Ineffective mark-compacts near heap limit`, après deux
minutes de silence. Le monde doit être hissé HORS du callback. C'est pour cela
que `historique-partie-portee.test.ts`, écrit avant, passe `undefined` comme monde :
il contournait le piège sans le nommer.

### Écarts par rapport au plan écrit

- **`viderErreurs()` a été ajoutée** à `erreurs-console.ts`. Le plan l'avait
  prévue comme recours ; elle s'est révélée nécessaire dès le premier jet, le
  module gardant un état de module que les cas de test se transmettaient.
- **Plus de cas que prévu** : 2 (tâche 1), 6 (tâche 2), 26 (tâches 3 et 4),
  9 (tâche 5). Les ajouts couvrent la cible du journal en object id, la main de
  CHAQUE siège, la fin de partie, le coût et la raison d'injouabilité dans le
  texte, le retrait des accents du nom de fichier, la campagne inscrite au
  rapport, et la confirmation annoncée aux lecteurs d'écran.
- **`useEffect` de nettoyage de la minuterie** ajouté dans `useRapportBug` : sans
  lui, un démontage pendant les quatre secondes du message laisse la minuterie
  appeler `setMessage` dans le vide.

### Ce qui reste : la tâche 7, qui demande un navigateur

Rien n'est déployé. `bash ui-app/deployer.sh` n'a pas été lancé : le plateau du
jeu tourne toujours sur la version d'avant.
