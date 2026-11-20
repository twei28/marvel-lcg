// Quasar (Galactic Storm, Kajislav, lot GS-2) : ce que le plateau DESSINE. Etape 8 bis de PROCESSUS-CARTE.md.
//
// ⚠ LES FIXTURES NE SONT PAS ECRITES A LA MAIN. Elles sortent du moteur : cas « [quasar] ... plateau : fixture ... »
// de `Fusion/marvel-lcg-src/tools/cas/quasar.py` (verificateur `qz_fixture_plateau`), lances avec
// QUASAR_FIXTURE_DIR=<dossier> ; le monde est `ToDescriptor.World` (ce que sert `/get_world`), siege 0 sans ses
// decks ni sa main, plus les zones communes. Pour les regenerer : relancer ces deux cas, recopier les JSON ici.
//
// Position 1 (quasar-maelstrom.json) : Quasar en forme heros, Protector of the Universe revelee (3 pions duty),
// Martinex en jeu et Tenace, Maelstrom revele (Quantum Bands GLISSEES sous lui), Entropy Ascendant revelee,
// Shocker en jeu puis Avatar of Oblivion revele (attache a Shocker).
// Position 2 (quasar-bandes-revenues.json) : Maelstrom revele puis vaincu, les Bandes sont revenues en jeu.
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { picIdCarte } from './arts-cartes'
import { catalogueVide } from './catalogue'
import { dessinee } from './plateau-de-test'
import type { World } from './world'
import { construirePlateau } from './zones'

const ici = dirname(fileURLToPath(import.meta.url))
type Fixture = { monde: World; identite: number }
const lire = (nom: string) => JSON.parse(readFileSync(join(ici, '__fixtures__', nom), 'utf8')) as Fixture

type CarteBrute = { id?: number; object_id?: number; card_id?: string }

/** Identifiant d'objet de la carte `cardId` dans le descripteur (siege 0 ou zones communes). */
function objetDe(world: World, cardId: string): number {
  const zones: unknown[] = []
  const siege = (world as unknown as { players: Array<Record<string, unknown>> }).players[0] ?? {}
  for (const v of Object.values(siege)) if (Array.isArray(v)) zones.push(...v)
  for (const [k, v] of Object.entries(world as unknown as Record<string, unknown>))
    if (k.startsWith('area_') && Array.isArray(v)) zones.push(...v)
  for (const c of zones as CarteBrute[]) {
    if (c && c.card_id === cardId) return Number(c.id ?? c.object_id)
  }
  throw new Error(`${cardId} absente du descripteur`)
}

function compteursDe(world: World, id: number) {
  const plateau = construirePlateau(world, { playerId: 0, catalogue: catalogueVide })
  for (const e of plateau.emplacements)
    for (const g of e.groupes) for (const u of g) if (Number(u.carte.id) === id) return u.carte.counters ?? []
  throw new Error(`carte ${id} absente du plateau`)
}

describe('Quasar : arts alternatifs du deck de depart (serie « quasar »)', () => {
  it("sans choix, le joueur Quasar voit l'illustration de Kajislav ; un autre heros, l'officielle", () => {
    expect(picIdCarte('56046', 'gs300a', {})).toBe('56046_quasar')
    expect(picIdCarte('19012', 'gs300b', {})).toBe('19012_quasar')
    expect(picIdCarte('19012', '01001a', {})).toBe('19012')
  })
  it("le choix « standard » rend l'officielle au joueur Quasar", () => {
    expect(picIdCarte('19012', 'gs300a', { '19012': 'standard' })).toBe('19012')
  })
})

describe('Quasar : ce que ses cartes dessinent (descripteur produit par le moteur)', () => {
  const p1 = lire('quasar-maelstrom.json')
  const monde = p1.monde

  // gs099q Maelstrom : « When Revealed: Tuck Quantum Bands under Maelstrom ».
  // Le descripteur les rattache a Maelstrom (bind_object_id), face cachee.
  it('les Quantum Bands glissees sont dessinees sous Maelstrom', () => {
    const bandes = dessinee(monde, objetDe(monde, 'gs301'))
    expect(bandes).toBeDefined()
    expect(bandes?.portePar).toBe(objetDe(monde, 'gs099q'))
  })

  // gs065 : « Uses (3 duty counters) ».
  it("l'obligation est sur la table avec ses 3 pions duty", () => {
    const id = objetDe(monde, 'gs065')
    expect(dessinee(monde, id)).toBeDefined()
    expect(compteursDe(monde, id)).toContainEqual(expect.objectContaining({ value: 3 }))
  })

  // gs237q : « Attach to the minion with the highest ATK ». Shocker et Maelstrom ont ATK 2 a egalite : le moteur
  // l'a attache a Maelstrom dans cette position (egalite = choix, regle ordinaire) ; le plateau doit le dessiner
  // SUR son porteur, quel qu'il soit.
  it("Avatar of Oblivion est dessine sur le sbire qui le porte", () => {
    expect(dessinee(monde, objetDe(monde, 'gs237q'))?.portePar).toBe(objetDe(monde, 'gs099q'))
  })

  // gs239q : la manigance annexe nemesis.
  it('Entropy Ascendant est sur la table', () => {
    expect(dessinee(monde, objetDe(monde, 'gs239q'))).toBeDefined()
  })

  // gs309 / gs349 : une carte d'etat Tenace sur un allie (Martinex).
  it("la Tenace est dessinee sur l'allie qui la porte", () => {
    const martinex = objetDe(monde, '21065')
    const tenace = objetDe(monde, 'tough')
    expect(dessinee(monde, tenace)?.portePar).toBe(martinex)
  })

  // gs099q (Reponse forcee) / gs300b (Setup) : les Bandes en jeu, sur Quasar, face visible.
  it('apres la defaite de Maelstrom, les Bandes sont de nouveau sur Quasar, face visible', () => {
    const p2 = lire('quasar-bandes-revenues.json')
    const bandes = dessinee(p2.monde, objetDe(p2.monde, 'gs301'))
    expect(bandes).toBeDefined()
    expect(bandes?.portePar).toBe(p2.identite)
    expect(bandes?.facedown).toBe(false)
    expect(bandes?.peeking).toBe(false)
  })
})
