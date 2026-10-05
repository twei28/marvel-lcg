// LE MODELE DE VUE DU CARTOUCHE DU BAS (refonte du 04/10/2026, scene PC).
//
// Une etape et son contexte entrent, des DONNEES sortent (vignettes, jauges,
// textes deja en langue) : aucune closure, aucun DOM. Un describe par
// decision de `.planning/todos/2026-10-04-refonte-phase-mechant-decisions.md`.
import { afterEach, describe, expect, it } from 'vitest'
import type { ScanCardProps } from '../components/ScanCard'
import type { EtapeDeroule } from './deroule-phase'
import { DICO_EN_BASE } from './dico-en'
import { titreEtape } from './deroule-textes'
import {
  PASTILLES,
  bilanTroisColonnes,
  herosViseDe,
  pastilleDuTemps,
  pastilles,
  tempsAfficheDe,
  titreCourt,
  vueDeLEtape,
  type ContexteVue,
  type VueBilan,
  type VueCorps,
  type VueRangee,
  type VueRevelee,
  type VueStade,
} from './vue-cartouche'

afterEach(() => window.localStorage.clear())

const etape = (e: Partial<EtapeDeroule> & Pick<EtapeDeroule, 'cle' | 'temps' | 'titre'>): EtapeDeroule => ({
  regle: '',
  boosts: [],
  ...e,
})

const scan = (id: number, name: string, kind: ScanCardProps['kind'] = 'unknown'): ScanCardProps => ({
  id: String(id),
  name,
  kind,
  imageUrl: `scan/${id}.jpg`,
})

const CARTES = new Map<number, ScanCardProps>([
  [9, scan(9, 'Effraction', 'main-scheme')],
  [12, scan(12, 'Rhino', 'villain')],
  [13, scan(13, 'Rhino II', 'villain')],
  [40, scan(40, 'Spider-Man', 'hero')],
  [41, scan(41, 'Black Widow', 'ally')],
  [60, scan(60, 'Hydra Mercenary', 'minion')],
  [77, scan(77, 'Charge', 'treachery')],
  [78, scan(78, 'Sweeping Swoop', 'treachery')],
  [88, scan(88, 'Assaut', 'treachery')],
  [89, scan(89, 'Mines', 'treachery')],
])

const contexte = (etapes: EtapeDeroule[], index: number, extra: Partial<ContexteVue> = {}): ContexteVue => ({
  etapes,
  index,
  boostsMontres: 99,
  carteScene: (id) => CARTES.get(id),
  ...extra,
})

// Des gardes plutot que des casts : une vue du mauvais genre fait ECHOUER le
// cas avec son genre, au lieu de passer en silence sur des champs absents.
function enRangee(vue: VueCorps): VueRangee {
  if (vue.genre !== 'rangee') throw new Error(`vue ${vue.genre}, rangee attendue`)
  return vue
}
function enRevelee(vue: VueCorps): VueRevelee {
  if (vue.genre !== 'revelee') throw new Error(`vue ${vue.genre}, revelee attendue`)
  return vue
}
function enStade(vue: VueCorps): VueStade {
  if (vue.genre !== 'stade') throw new Error(`vue ${vue.genre}, stade attendu`)
  return vue
}
function enBilan(vue: VueCorps): VueBilan {
  if (vue.genre !== 'bilan') throw new Error(`vue ${vue.genre}, bilan attendu`)
  return vue
}

/** La vue d'une etape seule, dans une liste qui ne contient qu'elle. */
const vueSeule = (e: EtapeDeroule, extra: Partial<ContexteVue> = {}) => vueDeLEtape(e, contexte([e], 0, extra))
const rangee = (e: EtapeDeroule, extra: Partial<ContexteVue> = {}) => enRangee(vueSeule(e, extra))

// Les etapes de reference, comme `etapesDeroule` les fabrique.
const menace = etape({
  cle: 'menace:1:0:9', temps: 'menace', titre: 'menace', cibleId: 9, cibleNom: 'Effraction',
  montant: 1, restant: 3, plafond: 7,
})
const annonceRhino = etape({
  cle: 'activation:3', temps: 'mechant', titre: 'attaque', etat: 'annonce', carteId: 12, auteurNom: 'Rhino',
  cibleId: 40, cibleNom: 'Spider-Man', valeurAnnoncee: 2,
})
const boostsRhino = [
  { cle: 'boost:0:77', nom: 'Charge', cibleId: 77, apport: 1 },
  { cle: 'boost:1:78', nom: 'Sweeping Swoop', cibleId: 78, apport: 0, etoile: true },
]
const annonceEnrichie = etape({
  ...annonceRhino, defenseurId: 40, defenseurNom: 'Spider-Man', defense: 3, totalAvantDefense: 3,
  baseImprimee: 2, boosts: boostsRhino,
})
const resoluRhino = etape({
  ...annonceRhino, etat: 'resolu', valeurAnnoncee: undefined, base: 2, defense: 2, montant: 1, inflige: 1,
  restant: 9, defenseurId: 40, defenseurNom: 'Spider-Man', cibleAnnonceeId: 40, boosts: [boostsRhino[0]],
})

describe('D30 : le titre court, une ligne, en Title Case', () => {
  const ctx = contexte([], 0, { infoCarte: (id) => (id === 13 ? { printed_stage: 2 } : undefined) })
  it('dit QUOI en deux ou trois mots', () => {
    expect(titreCourt(annonceRhino, ctx)).toBe('Attaque de Rhino')
    expect(titreCourt(etape({ cle: 'x', temps: 'mechant', titre: 'manigance', auteurNom: 'Rhino' }), ctx)).toBe('Manigance')
    expect(titreCourt(menace, ctx)).toBe('Menace')
    expect(titreCourt(etape({ cle: 'b', temps: 'bilan', titre: 'bilan' }), ctx)).toBe('Bilan')
    expect(titreCourt(etape({ cle: 'e', temps: 'mechant', titre: 'entree', carteId: 60, cibleNom: 'Drone' }), ctx)).toBe('Drone entre en jeu')
  })

  it('une carte revelee : son nom et son type, du fait sinon de la carte', () => {
    const assaut = etape({ cle: 'r', temps: 'revelation', titre: 'revelation', carteId: 88, cibleNom: 'Assaut' })
    expect(titreCourt({ ...assaut, typeCarte: 'Treachery' }, ctx)).toBe('Assaut (Traîtrise)')
    // Sans le fait `type` (moteur ancien) : le type de la carte du monde.
    expect(titreCourt(assaut, ctx)).toBe('Assaut (Traîtrise)')
    // Ni l'un ni l'autre : le nom seul, rien d'invente.
    expect(titreCourt({ ...assaut, carteId: 999 }, ctx)).toBe('Assaut')
    expect(titreCourt({ ...assaut, typeCarte: 'Minion', cibleNom: 'Hydra Mercenary' }, ctx)).toBe('Hydra Mercenary (Sbire)')
  })

  it('une carte revelee par Renfort nomme la carte qui l a declenchee', () => {
    const suite = etape({ cle: 'r2', temps: 'revelation', titre: 'revelation', carteId: 88, cibleNom: 'Assaut', parSurge: true, renfortDe: 'Mines' })
    expect(titreCourt(suite, ctx)).toBe('Renfort de Mines')
  })

  it('un stade : son numero imprime, sinon « Stade suivant »', () => {
    const stade = etape({ cle: 's', temps: 'mechant', titre: 'stade', stade: 'mechant', carteId: 13, cibleNom: 'Rhino' })
    expect(titreCourt(stade, ctx)).toBe('Stade II')
    expect(titreCourt({ ...stade, carteId: 14 }, ctx)).toBe('Stade suivant')
  })

  it('passe par le dictionnaire anglais', () => {
    window.localStorage.setItem('marvel-langue', 'en')
    expect(titreCourt(annonceRhino, ctx)).toBe('Rhino attacks')
    expect(titreCourt(menace, ctx)).toBe('Threat')
  })
})

describe('D7, D9 : la rangee d une attaque annoncee', () => {
  it('annonce simple : l attaquant a gauche avec son ATQ, le heros vise, aucun resultat', () => {
    const vue = rangee(annonceRhino)
    expect(vue.genre).toBe('rangee')
    expect(vue.acteur).toMatchObject({ carteId: 12, nom: 'Rhino', legende: 'ATQ 2', etat: 'inerte' })
    expect(vue.acteur?.scan?.name).toBe('Rhino')
    expect(vue.boosts).toEqual([])
    expect(vue.total).toBeUndefined()
    expect(vue.defenseur).toBeUndefined()
    expect(vue.cibles.map((c) => c.carteId)).toEqual([40])
    expect(vue.resultat).toBeUndefined()
    expect(vue.annulee).toBeUndefined()
    expect(vue.lignesEtoile).toEqual([])
    expect(vue.grisee).toBe(false)
  })

  it('annonce enrichie (fait boosts) : boosts colles, total, defenseur « défend · DÉF 3 »', () => {
    const vue = rangee(annonceEnrichie)
    expect(vue.boosts.map((b) => [b.carteId, b.legende, b.apport, b.etoile])).toEqual([
      [77, '+1', 1, undefined],
      [78, '+0 ★', 0, true],
    ])
    expect(vue.total).toEqual({ texte: '= 3', gros: false })
    expect(vue.defenseur).toMatchObject({ carteId: 40, nom: 'Spider-Man', legende: 'défend · DÉF 3' })
    // Le heros vise defend lui-meme : une seule vignette, pas deux.
    expect(vue.cibles).toEqual([])
    expect(vue.resultat).toBeUndefined()
  })

  it('les boosts suivent boostsMontres : la rangee s allonge quand une carte parait', () => {
    const vue = rangee(annonceEnrichie, { boostsMontres: 1 })
    expect(vue.boosts.map((b) => b.carteId)).toEqual([77])
    expect(vue.total?.texte).toBe('= 3')
    expect(rangee(annonceEnrichie, { boostsMontres: 0 }).total).toBeUndefined()
  })
})

describe('D10, D11 : la rangee resolue, figee, le chiffre final en gros', () => {
  it('« 1 dégât subi » et la jauge avant → apres / PV max', () => {
    const vue = rangee(resoluRhino, { pvMaxParNom: new Map([['Spider-Man', 10]]) })
    expect(vue.total).toEqual({ texte: '= 3', gros: true })
    expect(vue.defenseur).toMatchObject({ carteId: 40, legende: 'défend · DÉF 2' })
    expect(vue.resultat).toEqual({ texte: '1 dégât subi', jauge: { avant: 10, apres: 9, plafond: 10 } })
  })

  it('le PV max se cherche par le nom ANGLAIS de l etape brute, meme si la vue lit le francais', () => {
    const enFrancais = { ...resoluRhino, cibleNom: 'Homme-Araignée' }
    const vue = enRangee(vueDeLEtape(enFrancais, contexte([resoluRhino], 0, { pvMaxParNom: new Map([['Spider-Man', 10]]) })))
    expect(vue.resultat?.jauge?.plafond).toBe(10)
  })

  it('un allie defend : le heros vise ET le defenseur se voient', () => {
    const vue = rangee({ ...resoluRhino, cibleId: 41, cibleNom: 'Black Widow', defenseurId: 41, defenseurNom: 'Black Widow', defense: 1 })
    expect(vue.defenseur).toMatchObject({ carteId: 41, legende: 'défend · DÉF 1' })
    expect(vue.cibles.map((c) => c.carteId)).toEqual([40])
  })

  it('un allie n a pas de DEF : « défend » seul, jamais « DÉF 0 » (planche du lot 6)', () => {
    const allie = { ...resoluRhino, cibleId: 41, cibleNom: 'Black Widow', defenseurId: 41, defenseurNom: 'Black Widow', defense: 0 }
    expect(rangee(allie).defenseur?.legende).toBe('défend')
    expect(rangee({ ...annonceEnrichie, defense: 0 }).defenseur?.legende).toBe('défend')
  })

  it('D10 : une ligne par boost etoile, le texte FR de la capacite quand on l a', () => {
    const etoile = { ...resoluRhino, boosts: boostsRhino }
    expect(rangee(etoile, { texteEtoile: (id) => (id === 78 ? 'Rhino inflige 1 dégât supplémentaire.' : undefined) }).lignesEtoile).toEqual([
      '★ Sweeping Swoop : Rhino inflige 1 dégât supplémentaire.',
    ])
    expect(rangee(etoile).lignesEtoile).toEqual(['★ Sweeping Swoop : son effet de boost s’applique'])
    // Un boost etoile pas encore retourne ne dit rien.
    expect(rangee(etoile, { boostsMontres: 1 }).lignesEtoile).toEqual([])
  })
})

describe('D24 : l activation annulee', () => {
  it('la rangee normale, barree, la cause en clair', () => {
    const annulee = { ...annonceRhino, etat: 'annule' as const, annuleePar: 'Stunned' }
    const vue = rangee(annulee)
    expect(vue.annulee).toEqual({ cause: 'Sonné' })
    expect(vue.total).toBeUndefined()
    expect(vue.resultat).toBeUndefined()
  })

  it('sans cause connue : « Annulée » seule, rien d invente (piege 41)', () => {
    expect(rangee({ ...annonceRhino, etat: 'annule' }).annulee).toEqual({})
  })
})

describe('D12 : la menace du point 1', () => {
  it('la manigance en vignette, le detail du calcul, la jauge', () => {
    const vue = rangee({ ...menace, montant: 2, restant: 4, escalade: 1, acceleration: 1, joueurs: 1 })
    expect(vue.acteur).toMatchObject({ carteId: 9, nom: 'Effraction' })
    expect(vue.calcul).toBe('1 par joueur + 1 accélération = 2')
    expect(vue.resultat).toEqual({ texte: '+2 menaces', jauge: { avant: 2, apres: 4, plafond: 7 } })
  })

  it('« par joueur » seulement si l escalade se divise, sinon « d’escalade »', () => {
    expect(rangee({ ...menace, montant: 2, escalade: 2, acceleration: 0, joueurs: 2 }).calcul).toBe('1 par joueur = 2')
    expect(rangee({ ...menace, montant: 3, escalade: 3, acceleration: 0, joueurs: 2 }).calcul).toBe('3 d’escalade = 3')
  })

  it('sans decomposition (moteur ancien) : le total et la jauge seuls', () => {
    const vue = rangee(menace)
    expect(vue.calcul).toBeUndefined()
    expect(vue.resultat).toEqual({ texte: '+1 menace', jauge: { avant: 2, apres: 3, plafond: 7 } })
  })
})

describe('D13 : la manigance du mechant, et les replis du seuil', () => {
  const manigance = etape({
    cle: 'activation:5', temps: 'mechant', titre: 'manigance', etat: 'resolu', carteId: 12, auteurNom: 'Rhino',
    cibleId: 9, cibleNom: 'Effraction', base: 1, montant: 2, restant: 6,
  })
  it('meme gabarit que l attaque : MAN, puis la manigance avec sa jauge', () => {
    const vue = rangee({ ...manigance, plafond: 7 })
    expect(vue.acteur?.legende).toBe('MAN 1')
    expect(vue.cibles.map((c) => c.carteId)).toEqual([9])
    expect(vue.resultat).toEqual({ texte: '+2 menaces', jauge: { avant: 4, apres: 6, plafond: 7 } })
  })

  it('seuil absent du fait : celui de l etape de menace du round, puis celui du monde, sinon rien', () => {
    const avecMenace = enRangee(vueDeLEtape(manigance, contexte([{ ...menace, plafond: 8 }, manigance], 1)))
    expect(avecMenace.resultat?.jauge?.plafond).toBe(8)
    expect(rangee(manigance, { infoCarte: (id) => (id === 9 ? { target_threat: 9 } : undefined) }).resultat?.jauge?.plafond).toBe(9)
    expect(rangee(manigance).resultat?.jauge).toEqual({ avant: 4, apres: 6 })
  })
})

describe('piege 40 : des valeurs nulles, rien d invente', () => {
  it('restant absent : aucune jauge ; subi negatif tel quel ; apport 0 sans etoile tait sa legende', () => {
    const sansCompteur = rangee({ ...resoluRhino, restant: undefined })
    expect(sansCompteur.resultat).toEqual({ texte: '1 dégât subi' })
    expect(rangee({ ...resoluRhino, montant: -1 }).resultat?.texte).toBe('-1 dégât subi')
    const zero = rangee({ ...resoluRhino, boosts: [{ cle: 'b', nom: 'Rien', cibleId: 77, apport: 0 }] })
    expect(zero.boosts[0]?.legende).toBeUndefined()
  })

  // Planche du lot 5 (etat 15b) : un allie de 2 PV defend contre 4 ; le moteur
  // publie `restant: -2`, et la jauge disait « 2 → -2 / 2 ». Des PV ne
  // descendent pas sous zero : l'allie est vaincu, la jauge s'arrete a 0.
  it('des PV ne passent jamais sous zero dans la jauge', () => {
    const vaincu = rangee(
      { ...resoluRhino, cibleId: 41, cibleNom: 'Black Widow', montant: 4, restant: -2 },
      { pvMaxParNom: new Map([['Black Widow', 2]]) }
    )
    expect(vaincu.resultat).toEqual({ texte: '4 dégâts subis', jauge: { avant: 2, apres: 0, plafond: 2 } })
  })

  it('PV max inconnu : la jauge n a pas de plafond', () => {
    expect(rangee(resoluRhino).resultat?.jauge).toEqual({ avant: 10, apres: 9 })
  })
})

describe('D16, D17 : la carte revelee en grand, et le Renfort', () => {
  const mines = etape({
    cle: 'revelation:1:5:89', temps: 'revelation', titre: 'revelation', carteId: 89, cibleNom: 'Mines', typeCarte: 'Treachery',
    effets: [{ genre: 'degats', cible: 'Spider-Man', cible_id: 40, montant: 2, restant: 7 }],
    suivieDUnRenfort: true,
  })
  const assaut = etape({
    cle: 'revelation:1:6:88', temps: 'revelation', titre: 'revelation', carteId: 88, cibleNom: 'Assaut',
    parSurge: true, renfortDe: 'Mines',
  })
  it('la carte, son type, son effet resume et sa jauge', () => {
    const vue = enRevelee(vueDeLEtape(mines, contexte([mines, assaut], 0)))
    expect(vue.genre).toBe('revelee')
    expect(vue.carte).toMatchObject({ carteId: 89, nom: 'Mines' })
    expect(vue.typeFr).toBe('Traîtrise')
    expect(vue.lignes).toEqual(['→ Spider-Man subit 2 dégâts (7 PV)'])
    expect(vue.jauge).toEqual({ avant: 9, apres: 7 })
  })

  it('suivie d un Renfort : la carte suivante est a cote', () => {
    const vue = enRevelee(vueDeLEtape(mines, contexte([mines, assaut], 0)))
    expect(vue.renfort).toMatchObject({ carteId: 88, nom: 'Assaut' })
    const suite = enRevelee(vueDeLEtape(assaut, contexte([mines, assaut], 1)))
    expect(suite.surtitreRenfort).toBe('Renfort de Mines')
    expect(suite.renfort).toBeUndefined()
  })

  it('les consequences rangees sous la carte deviennent des lignes', () => {
    const consequence = etape({ ...resoluRhino, temps: 'revelation', cause: 'Assaut' })
    const vue = enRevelee(vueSeule({ ...mines, effets: undefined, consequences: [consequence] }))
    expect(vue.lignes).toHaveLength(1)
    expect(vue.lignes[0]).toMatch(/^→ Rhino attaque Spider-Man/)
  })
})

describe('D17 : le Renfort dont la carte suivante n est pas encore connue', () => {
  const sansSuite = etape({
    cle: 'revelation:1:5:89', temps: 'revelation', titre: 'revelation', carteId: 89, cibleNom: 'Mines', typeCarte: 'Treachery',
    effets: [{ genre: 'degats', cible: 'Spider-Man', cible_id: 40, montant: 2, restant: 7 }],
  })
  const avecRenfort = (id: number) => (id === 89 ? { renfort: true } : undefined)

  it('la carte a Renfort, sans suite connue : une case vide « ? » a droite', () => {
    const vue = enRevelee(vueDeLEtape(sansSuite, contexte([sansSuite], 0, { infoRevelee: avecRenfort })))
    expect(vue.renfort).toBeUndefined()
    expect(vue.renfortInconnu).toBe(true)
  })

  it('sans mot-cle Renfort, pas de case vide', () => {
    const vue = enRevelee(vueDeLEtape(sansSuite, contexte([sansSuite], 0, { infoRevelee: () => ({ renfort: false }) })))
    expect(vue.renfortInconnu).toBeUndefined()
    expect(enRevelee(vueDeLEtape(sansSuite, contexte([sansSuite], 0))).renfortInconnu).toBeUndefined()
  })

  it('des que la carte suivante est connue, la vraie vignette remplace la case vide', () => {
    const suivie = etape({ ...sansSuite, suivieDUnRenfort: true })
    const assaut = etape({ cle: 'revelation:1:6:88', temps: 'revelation', titre: 'revelation', carteId: 88, cibleNom: 'Assaut', parSurge: true, renfortDe: 'Mines' })
    const vue = enRevelee(vueDeLEtape(suivie, contexte([suivie, assaut], 0, { infoRevelee: avecRenfort })))
    expect(vue.renfort).toMatchObject({ carteId: 88 })
    expect(vue.renfortInconnu).toBeUndefined()
  })
})

describe('D16 : le texte imprimé quand le résumé de l effet manque', () => {
  const muette = etape({ cle: 'revelation:1:7:91', temps: 'revelation', titre: 'revelation', carteId: 91, cibleNom: 'Chantage', typeCarte: 'Treachery' })
  const imprime = (id: number) => (id === 91 ? { renfort: false, texteImprime: ['Quand révélée : subis 2 dégâts.'] } : undefined)

  it('sans effet ni consequence publies, le texte imprime tient lieu de resume', () => {
    const vue = enRevelee(vueDeLEtape(muette, contexte([muette], 0, { infoRevelee: imprime })))
    expect(vue.lignes).toEqual(['Quand révélée : subis 2 dégâts.'])
  })

  it('avec un resume du moteur, le texte imprime n est pas ajoute', () => {
    const avecEffet = etape({ ...muette, effets: [{ genre: 'degats', cible: 'Spider-Man', cible_id: 40, montant: 2, restant: 7 }] })
    const vue = enRevelee(vueDeLEtape(avecEffet, contexte([avecEffet], 0, { infoRevelee: imprime })))
    expect(vue.lignes).toEqual(['→ Spider-Man subit 2 dégâts (7 PV)'])
  })

  it('un texte long garde toutes ses lignes : le carre grandit, rien n est coupe', () => {
    const longue = (id: number) => (id === 91 ? { renfort: false, texteImprime: ['a', 'b', 'c', 'd'] } : undefined)
    const vue = enRevelee(vueDeLEtape(muette, contexte([muette], 0, { infoRevelee: longue })))
    expect(vue.lignes).toEqual(['a', 'b', 'c', 'd'])
  })

  it('sans texte connu : pas de ligne inventee', () => {
    const vue = enRevelee(vueDeLEtape(muette, contexte([muette], 0)))
    expect(vue.lignes).toEqual([])
  })
})

describe('D25 : le stade, ancienne carte → nouvelle, les stats qui changent', () => {
  const stade = etape({
    cle: 'stade:1:2:13', temps: 'mechant', titre: 'stade', stade: 'mechant', carteId: 13, auteurNom: 'Rhino', cibleNom: 'Rhino',
    stadeAvantId: 12, statsAvant: { pv_max: 14, atq: 2, man: 1 }, statsApres: { pv_max: 15, atq: 3, man: 1 },
  })
  it('avec le fait : avant, apres, et seulement ce qui change', () => {
    const vue = enStade(vueSeule(stade))
    expect(vue.genre).toBe('stade')
    expect(vue.avant).toMatchObject({ carteId: 12, nom: 'Rhino' })
    expect(vue.apres).toMatchObject({ carteId: 13 })
    expect(vue.deltas).toEqual(['PV 14 → 15', 'ATQ 2 → 3'])
  })

  // Le moteur REPREND l'objet du mechant pour son stade suivant
  // (`SetAsCard`, scenario.py) : `avant_id` vaut alors `carte_id`, et la carte
  // d'avant dessinee depuis le monde montrait la NOUVELLE face deux fois
  // (« Rhino II → Rhino II », planche du lot 3, etat 7). La vue se tait
  // plutot que de montrer une carte fausse ; les stats qui changent restent.
  it('le meme objet repris par la nouvelle carte : aucune carte d avant, les stats restent', () => {
    const vue = enStade(vueSeule({ ...stade, stadeAvantId: 13 }))
    expect(vue.avant).toBeUndefined()
    expect(vue.apres).toMatchObject({ carteId: 13 })
    expect(vue.deltas).toEqual(['PV 14 → 15', 'ATQ 2 → 3'])
  })

  it('une manigance : son seuil', () => {
    const vue = enStade(vueSeule({ ...stade, stade: 'manigance', statsAvant: { seuil: 7 }, statsApres: { seuil: 9 } }))
    expect(vue.deltas).toEqual(['Menace 7 → 9'])
  })

  it('sans le fait (moteur ancien) : la nouvelle carte seule et ses stats du monde, sans fleche', () => {
    const ancien = { ...stade, stadeAvantId: undefined, statsAvant: undefined, statsApres: undefined }
    const vue = enStade(vueSeule(ancien, { infoCarte: (id) => (id === 13 ? { max_health: 15, attack: 3, scheme: 1 } : undefined) }))
    expect(vue.avant).toBeUndefined()
    expect(vue.deltas).toEqual(['PV 15', 'ATQ 3', 'MAN 1'])
  })
})

describe('les etapes sans rangee', () => {
  it('un temps vide se dit en une phrase', () => {
    expect(vueSeule(etape({ cle: 'vide:sbires', temps: 'sbires', titre: 'vide' }))).toEqual({ genre: 'vide', texte: 'Aucun sbire engagé' })
  })
})

describe('D19 : le bilan en trois colonnes, une seule regle de comptage', () => {
  const attaque = etape({
    cle: 'a1', temps: 'mechant', titre: 'attaque', etat: 'resolu', carteId: 12, auteurNom: 'Rhino',
    cibleId: 40, cibleNom: 'Spider-Man', montant: 3, restant: 7,
  })
  const consequence = etape({
    cle: 'c', temps: 'revelation', titre: 'attaque', etat: 'resolu', carteId: 12, auteurNom: 'Rhino',
    cibleId: 40, cibleNom: 'Spider-Man', montant: 4, restant: 3,
  })
  const revelation = etape({
    cle: 'r', temps: 'revelation', titre: 'revelation', carteId: 88, cibleNom: 'Assaut',
    effets: [
      { genre: 'menace', cible: 'Effraction', cible_id: 9, montant: 2, restant: 5 },
      { genre: 'entree', carte: 'Hydra Mercenary', carte_id: 60, type: 'sbire' },
    ],
    consequences: [consequence],
  })
  const sonne = etape({ cle: 's', temps: 'mechant', titre: 'statut', statut: 'Stunned', cibleId: 40, cibleNom: 'Spider-Man', montant: 1 })
  const bilan = etape({ cle: 'bilan', temps: 'bilan', titre: 'bilan' })
  const etapes = [menace, attaque, sonne, revelation, bilan]

  it('menace, heros et allies, nouveautes', () => {
    const vue = bilanTroisColonnes(etapes, contexte(etapes, 4, { pvMaxParNom: new Map([['Spider-Man', 10]]) }))
    expect(vue.genre).toBe('bilan')
    expect(vue.menace).toEqual([{ cle: 'menaces:9', carteId: 9, nom: 'Effraction', total: 3, jauge: { avant: 2, apres: 5, plafond: 7 } }])
    expect(vue.heros).toEqual([
      { cle: 'degats:40', carteId: 40, nom: 'Spider-Man', total: 7, jauge: { avant: 10, apres: 3, plafond: 10 }, statuts: ['Sonné'] },
    ])
    expect(vue.nouveautes).toMatchObject([{ carteId: 60, nom: 'Hydra Mercenary' }])
    expect(vue.vide).toBe(false)
  })

  it('une phase sans rien : vide', () => {
    const vue = bilanTroisColonnes([bilan], contexte([bilan], 0))
    expect(vue).toEqual({ genre: 'bilan', menace: [], heros: [], nouveautes: [], vide: true })
  })

  it('vueDeLEtape sur le bilan rend les trois colonnes', () => {
    expect(enBilan(vueDeLEtape(bilan, contexte(etapes, 4))).genre).toBe('bilan')
  })
})

describe('revirement du 05/10 : plus de pagination imposee', () => {
  it('le module ne decoupe plus rien : le carre grandit en hauteur', async () => {
    const module = await import('./vue-cartouche')
    expect(module).not.toHaveProperty('pagesDe')
    expect(module).not.toHaveProperty('CAPACITE')
  })
})

describe('la vue est serialisable : aucune closure', () => {
  it('JSON aller-retour egale la vue', () => {
    const ctx = contexte([menace, resoluRhino], 1, { pvMaxParNom: new Map([['Spider-Man', 10]]) })
    for (const vue of [vueDeLEtape(resoluRhino, ctx), vueDeLEtape(menace, ctx), bilanTroisColonnes([menace, resoluRhino], ctx)]) {
      expect(JSON.parse(JSON.stringify(vue))).toEqual(vue)
    }
  })
})

describe('D15, D22, D27, D34 : les cinq pastilles', () => {
  const attaqueMechant = etape({ ...resoluRhino, cle: 'a1' })
  const sbire1 = etape({ cle: 's1', temps: 'sbires', titre: 'attaque', etat: 'resolu', montant: 1, cibleNom: 'Spider-Man' })
  const sbire2 = etape({ cle: 's2', temps: 'sbires', titre: 'attaque', etat: 'resolu', montant: 2, cibleNom: 'Spider-Man' })
  const revelation = etape({
    cle: 'r', temps: 'revelation', titre: 'revelation', carteId: 88, cibleNom: 'Assaut',
    effets: [{ genre: 'menace', cible: 'Effraction', cible_id: 9, montant: 2 }],
  })
  const args = (extra: Partial<Parameters<typeof pastilles>[0]> = {}): Parameters<typeof pastilles>[0] => ({
    etapes: [menace, attaqueMechant, revelation],
    index: 1,
    tempsAffiche: 'mechant',
    cartesDistribuees: 0,
    questionAuJoueur: false,
    plusieursHeros: false,
    ...extra,
  })

  it('cinq pastilles numerotees, nom complet en clair, la distribution sous ④', () => {
    expect(PASTILLES.map((p) => [p.cle, p.numero, p.court])).toEqual([
      ['menace', '①', '1'],
      ['mechant', '②', '2A'],
      ['sbires', '③', '2B'],
      ['cartes-rencontre', '④', '3'],
      ['bilan', '⑤', 'Bilan'],
    ])
    expect(pastilleDuTemps('distribution')).toBe('cartes-rencontre')
    expect(pastilleDuTemps('revelation')).toBe('cartes-rencontre')
    expect(pastilleDuTemps('premier-joueur')).toBeUndefined()
    expect(pastilles(args()).map((p) => p.libelle)).toEqual([
      '1. Placer les menaces',
      '2A. Le méchant s’active',
      '2B. Les sbires s’activent',
      '3. Cartes rencontre',
      'Bilan',
    ])
  })

  it('chaque nom de pastille a son anglais (il passe par une variable, la gate du dictionnaire ne le voit pas)', () => {
    expect(PASTILLES.filter((p) => !(p.libelle in DICO_EN_BASE)).map((p) => p.libelle)).toEqual([])
  })

  it('passe, courant, a venir, avec leur resultat court', () => {
    const vue = pastilles(args())
    expect(vue.map((p) => [p.etat, p.resume])).toEqual([
      ['passe', '+1 menace'],
      ['courant', '1 dégât'],
      ['a-venir', ''],
      ['a-venir', ''],
      ['a-venir', ''],
    ])
  })

  it('la pastille COURANTE tait « aucun » tant que son temps n a rien resolu (planche du lot 6)', () => {
    // Rhino annonce son attaque : rien n'est encore arrive, « ② aucun » se
    // lisait comme une attaque sans effet.
    const vue = pastilles(args({ etapes: [menace, annonceRhino], index: 1 }))
    expect(vue[1]).toMatchObject({ etat: 'courant', resume: '' })
    // Une pastille PASSEE vide le dit toujours : son temps est fini.
    expect(pastilles(args({ index: 2, tempsAffiche: 'revelation' }))[2]).toMatchObject({ etat: 'passe', resume: 'aucun' })
  })

  it('« 1 carte distribuée » en tete de la pastille ④', () => {
    const vue = pastilles(args({ index: 2, tempsAffiche: 'revelation', cartesDistribuees: 1 }))
    expect(vue[3]).toMatchObject({ etat: 'courant', resume: '1 carte distribuée · +2 menaces' })
    expect(vue[2]).toMatchObject({ etat: 'passe', resume: 'aucun' })
    expect(pastilles(args({ index: 1, tempsAffiche: 'revelation', cartesDistribuees: 2, etapes: [menace, attaqueMechant] }))[3]?.resume).toBe('2 cartes distribuées')
  })

  it('une passee se relit d un clic, jamais pendant une question', () => {
    expect(pastilles(args())[0]?.relisible).toBe(true)
    expect(pastilles(args({ questionAuJoueur: true }))[0]?.relisible).toBe(false)
    expect(pastilles(args())[2]?.relisible).toBe(false)
    expect(pastilles(args({ relecture: 'menace' }))[0]?.relu).toBe(true)
  })

  it('D14 : « 1 / 2 » sur la pastille courante quand son temps compte plusieurs etapes', () => {
    const etapes = [menace, attaqueMechant, sbire1, sbire2]
    expect(pastilles(args({ etapes, index: 3, tempsAffiche: 'sbires' }))[2]?.compteur).toBe('2 / 2')
    expect(pastilles(args({ etapes, index: 1, tempsAffiche: 'mechant' }))[1]?.compteur).toBeUndefined()
  })

  it('pendant une question, la frise suit le temps de la question quand il a pris de l avance', () => {
    expect(tempsAfficheDe(attaqueMechant, true, 'sbires')).toBe('sbires')
    expect(tempsAfficheDe(attaqueMechant, false, 'sbires')).toBe('mechant')
    expect(tempsAfficheDe(attaqueMechant, true, 'menace')).toBe('mechant')
    expect(tempsAfficheDe(attaqueMechant, true, undefined)).toBe('mechant')
    const vue = pastilles(args({ tempsAffiche: tempsAfficheDe(attaqueMechant, true, 'sbires'), questionAuJoueur: true }))
    expect(vue.map((p) => p.etat)).toEqual(['passe', 'passe', 'courant', 'a-venir', 'a-venir'])
  })

  it('D27 : le portrait du heros vise, seulement a plusieurs heros', () => {
    expect(pastilles(args({ herosViseId: 40, plusieursHeros: true }))[1]?.portraitId).toBe(40)
    expect(pastilles(args({ herosViseId: 40, plusieursHeros: false }))[1]?.portraitId).toBeUndefined()
    expect(pastilles(args({ herosViseId: 40, plusieursHeros: true }))[0]?.portraitId).toBeUndefined()
  })

  it('le heros vise : la cible annoncee d abord (le defenseur a pris sa place), et seulement un heros', () => {
    const heros = new Set([40])
    expect(herosViseDe({ ...resoluRhino, cibleId: 41, cibleAnnonceeId: 40 }, heros)).toBe(40)
    expect(herosViseDe({ ...resoluRhino, cibleId: 41, cibleAnnonceeId: undefined }, heros)).toBeUndefined()
    expect(herosViseDe({ ...annonceRhino }, heros)).toBe(40)
    expect(herosViseDe(menace, heros)).toBeUndefined()
  })
})

describe('etat 04 : l etape Sonne (decision du 05/10/2026)', () => {
  const sonne = etape({
    cle: 'sonne:1:12', temps: 'mechant', titre: 'sonne', carteId: 12, auteurNom: 'Rhino',
    sonneTemps: 'attaque', statutRetire: true, annuleePar: 'Stunned',
  })

  it('la carte de l ennemi en grand, « Sonné : n’attaque pas » et « perd Sonné »', () => {
    const vue = enRevelee(vueSeule(sonne))
    expect(vue.carte).toMatchObject({ carteId: 12, nom: 'Rhino' })
    expect(vue.lignes).toEqual(['Sonné : n’attaque pas', 'perd Sonné'])
    expect(vue.renfort).toBeUndefined()
  })

  it('une manigance annulee dit « ne manigance pas »', () => {
    const vue = enRevelee(vueSeule({ ...sonne, sonneTemps: 'manigance' }))
    expect(vue.lignes[0]).toBe('Sonné : ne manigance pas')
  })

  it('un ennemi Constant reste Sonné', () => {
    const vue = enRevelee(vueSeule({ ...sonne, statutRetire: false }))
    expect(vue.lignes).toEqual(['Sonné : n’attaque pas', 'reste Sonné'])
  })

  it('le titre court est « Sonné », et une phrase de titre complete existe', () => {
    expect(titreCourt(sonne, contexte([sonne], 0))).toBe('Sonné')
    expect(titreEtape(sonne)).toBe('Rhino : Sonné, n’attaque pas')
  })

  it('les textes ont leur anglais', () => {
    for (const cle of ['Sonné : n’attaque pas', 'Sonné : ne manigance pas', 'perd Sonné', 'reste Sonné', 'Sonné']) {
      expect(cle in DICO_EN_BASE, cle).toBe(true)
    }
  })
})

describe('D14 bis : le compteur des sbires vient du moteur (05/10/2026)', () => {
  const sbire = (cle: string, rang: number, total: number) =>
    etape({ cle, temps: 'sbires', titre: 'attaque', etat: 'resolu', montant: 1, rangSbire: rang, totalSbires: total })

  it('« 1 / 2 » des la premiere etape, meme si une seule est connue', () => {
    const premiere = sbire('s1', 1, 2)
    const vue = pastilles({
      etapes: [premiere], index: 0, tempsAffiche: 'sbires', cartesDistribuees: 0,
      questionAuJoueur: false, plusieursHeros: false,
    })
    expect(vue[2]?.compteur).toBe('1 / 2')
  })

  it('un seul sbire : pas de compteur', () => {
    const vue = pastilles({
      etapes: [sbire('s1', 1, 1)], index: 0, tempsAffiche: 'sbires', cartesDistribuees: 0,
      questionAuJoueur: false, plusieursHeros: false,
    })
    expect(vue[2]?.compteur).toBeUndefined()
  })
})
