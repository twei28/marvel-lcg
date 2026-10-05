// La table par briques, etape 2 : les zones a dessiner viennent des
// emplacements d'origine (zones.ts) et de la disposition.
import { describe, expect, it } from 'vitest'
import { DISPOSITION_ORIGINE, DISPOSITION_DE_DEPART, fusionner, separer, zoneDe, type CleBrique } from './table-briques'
import { assemblerZones } from './table-rendu'
import type { CleEmplacement, EmplacementAffiche, Plateau, UniteAffichee } from './zones'

// Une unite qui ne sert qu'a etre comptee : le test ne regarde pas la carte.
const unite = (cle: string) => ({ cle, attachees: [] }) as unknown as UniteAffichee

function emplacement(cle: CleEmplacement, groupes: string[][], extra: Partial<EmplacementAffiche> = {}): EmplacementAffiche {
  const g = groupes.map((cles) => cles.map(unite))
  return { cle, titre: cle, groupes: g, nombreSurLaLigne: g.reduce((n, x) => n + x.length, 0), ...extra }
}

// Deux joueurs : alliés, engagés, environnement, puis héros, soutiens, deck spécial.
const plateau: Plateau = {
  emplacements: [
    emplacement('rencontre', [['mechant']]),
    emplacement('terrain-combat', [['ally-1'], ['sbire-1'], ['ally-2'], ['sbire-2'], ['env']], {
      groupesPiles: [undefined, 'terrain-combat-engages', undefined, 'terrain-combat-engages', undefined],
      groupesBriques: ['allies', 'sbires', 'allies', 'sbires', 'environnements'],
    }),
    emplacement('deck-special', [['special']]),
    emplacement('terrain-soutien', [['heros-1'], ['soutien-1'], ['heros-2'], ['soutien-2']], {
      proprietaires: [0, 0, 1, 1],
      groupesBriques: ['heros', 'soutiens', 'heros', 'soutiens'],
    }),
  ],
  nombreDeCartes: 0,
  idsAffiches: new Set(),
  idCompacteVers: new Map(),
} as unknown as Plateau

const cles = (e: EmplacementAffiche | undefined) => e?.groupes.map((g) => g.map((u) => u.cle).join('+'))
const zoneAvec = (d: ReturnType<typeof assemblerZones>, brique: CleBrique) => d.find((z) => z.aire === brique)

describe('l origine : rien ne change', () => {
  it('chaque zone reprend tel quel son emplacement d origine', () => {
    const zones = assemblerZones(plateau, DISPOSITION_ORIGINE)
    expect(zoneAvec(zones, 'allies')?.emplacement).toBe(plateau.emplacements[1])
    expect(zoneAvec(zones, 'heros')?.emplacement).toBe(plateau.emplacements[3])
    expect(zoneAvec(zones, 'mechant')?.emplacement).toBe(plateau.emplacements[0])
  })

  it('le deck special suit la zone du heros', () => {
    const zones = assemblerZones(plateau, DISPOSITION_DE_DEPART)
    expect(zoneAvec(zones, 'heros')?.avecHeros).toBe(true)
    expect(zoneAvec(zones, 'heros')?.accompagnement.map((e) => e.cle)).toEqual(['deck-special'])
    expect(zoneAvec(zones, 'allies')?.accompagnement).toEqual([])
  })
})

describe('une zone eclatee', () => {
  it('les sbires sortis ne montrent que les sbires, de tous les joueurs, avec leur secteur', () => {
    const d = separer(DISPOSITION_DE_DEPART, 'sbires', 1, 3)!
    const zones = assemblerZones(plateau, d)
    const sbires = zoneAvec(zones, 'sbires')?.emplacement
    expect(cles(sbires)).toEqual(['sbire-1', 'sbire-2'])
    expect(sbires?.titre).toBe('Sbires')
    expect(sbires?.groupesPiles).toEqual(['terrain-combat-engages', 'terrain-combat-engages'])
    expect(sbires?.emplacementsDOrigine).toEqual(['terrain-combat'])
    expect(cles(zoneAvec(zones, 'allies')?.emplacement)).toEqual(['ally-1', 'ally-2', 'env'])
    expect(zoneAvec(zones, 'allies')?.emplacement?.titre).toBe('Alliés et environnement')
  })

  it('heros et soutiens separes : chacun garde ses joueurs', () => {
    const d = separer(DISPOSITION_DE_DEPART, 'soutiens', 1, 3)!
    const zones = assemblerZones(plateau, d)
    expect(cles(zoneAvec(zones, 'soutiens')?.emplacement)).toEqual(['soutien-1', 'soutien-2'])
    expect(zoneAvec(zones, 'soutiens')?.emplacement?.proprietaires).toEqual([0, 1])
    expect(zoneAvec(zones, 'soutiens')?.avecHeros).toBe(false)
    expect(zoneAvec(zones, 'heros')?.avecHeros).toBe(true)
  })

  it('une zone fusionnee de deux origines garde l origine de chaque groupe', () => {
    const d = fusionner(DISPOSITION_DE_DEPART, 'mechant', 'allies')
    expect(d).toBeDefined()
    const zone = zoneDe(d!, 'mechant')!
    const rendue = assemblerZones(plateau, d!).find((z) => z.zone === zone)
    expect(rendue?.emplacement?.emplacementsDOrigine).toEqual(['rencontre', 'terrain-combat'])
    expect(rendue?.emplacement?.groupesDOrigine).toEqual(['rencontre', 'terrain-combat', 'terrain-combat', 'terrain-combat', 'terrain-combat', 'terrain-combat'])
  })
})

describe('une zone vide', () => {
  it('garde sa place mais n a rien a montrer', () => {
    const vide: Plateau = { ...plateau, emplacements: plateau.emplacements.filter((e) => e.cle !== 'terrain-combat') }
    const d = separer(DISPOSITION_DE_DEPART, 'sbires', 1, 3)!
    const zone = zoneAvec(assemblerZones(vide, d), 'sbires')
    expect(zone?.emplacement).toBeUndefined()
    expect(zone?.zone).toBe(zoneDe(d, 'sbires'))
  })
})
