// useGlisser.test.ts — `cibleSousLePoint`, la lecture du DOM sous le pointeur.
//
// Ronde de correction 1 de la tâche 5 (19/09/2026) : cette fonction est
// PARTAGÉE par le glisser ordinaire et le glisser manuel, mais aucun test
// existant ne posait de `data-pile` sur une unité — `cibles.test.ts` et
// `geste.test.tsx` construisent leurs plateaux de test sans jamais utiliser
// ce champ. Le risque théorique (signalé au rapport de la tâche 5) : un
// lâcher qui touche une pile SANS toucher sa carte (marge de son unité)
// retombait sur la pile fine plutôt que sur la zone large que le mode
// ORDINAIRE attend (ses règles sont bâties sur `emplacement.cle`, jamais sur
// une pile fine — `board.tsx`, `zoneDeLaCarte`). Ce fichier remplace ce
// raisonnement par une garantie.
import { describe, expect, it } from 'vitest'
import { cibleSousLePoint } from './useGlisser'

/** Construit `<section data-zone><div class="plateau-groupe" [data-pile]>
 *  <div class="plateau-unite" [data-pile]>[.scan-card]</div>[reste]</div>
 *  </section>` et pose le résultat dans le DOM réel du test. */
function poserPlateau(options: {
  zoneEmplacement: string
  pileGroupe?: string
  pileUnite?: string
  carteId?: number
  /** Un élément supplémentaire DANS l'unité mais HORS de `.scan-card`
   *  (une marge, un décor) : c'est lui qu'on survolera pour simuler un
   *  lâcher qui touche la pile sans toucher sa carte. */
  margeDansLUnite?: boolean
  /** Un élément DANS le groupe mais hors de toute unité (l'espace vide
   *  d'un secteur, entre deux cartes). */
  margeDansLeGroupe?: boolean
}): { scanCard?: HTMLElement; margeUnite?: HTMLElement; margeGroupe?: HTMLElement } {
  document.body.innerHTML = ''
  const section = document.createElement('section')
  section.dataset.zone = options.zoneEmplacement
  const groupe = document.createElement('div')
  groupe.className = 'plateau-groupe'
  if (options.pileGroupe !== undefined) groupe.dataset.pile = options.pileGroupe

  const unite = document.createElement('div')
  unite.className = 'plateau-unite'
  if (options.pileUnite !== undefined) unite.dataset.pile = options.pileUnite

  let scanCard: HTMLElement | undefined
  if (options.carteId !== undefined) {
    scanCard = document.createElement('div')
    scanCard.className = 'scan-card'
    scanCard.dataset.cardId = String(options.carteId)
    unite.appendChild(scanCard)
  }

  let margeUnite: HTMLElement | undefined
  if (options.margeDansLUnite) {
    margeUnite = document.createElement('span')
    margeUnite.className = 'marge-unite'
    unite.appendChild(margeUnite)
  }

  groupe.appendChild(unite)

  let margeGroupe: HTMLElement | undefined
  if (options.margeDansLeGroupe) {
    margeGroupe = document.createElement('span')
    margeGroupe.className = 'marge-groupe'
    groupe.appendChild(margeGroupe)
  }

  section.appendChild(groupe)
  document.body.appendChild(section)
  return { scanCard, margeUnite, margeGroupe }
}

describe('cibleSousLePoint', () => {
  it('lâchée sur la carte d’une pile : la pile fine, et la carte', () => {
    const { scanCard } = poserPlateau({
      zoneEmplacement: 'piles-joueur',
      pileUnite: 'joueur-deck',
      carteId: 5,
    })
    document.elementFromPoint = () => scanCard!
    expect(cibleSousLePoint(0, 0)).toEqual({ carteId: 5, zone: 'joueur-deck' })
  })

  // ⚠ LE CAS QUI COMPTE. Une pile ne DOIT compter que si on touche vraiment
  // sa carte : sinon la marge d'une unité de pile retomberait sur cette pile
  // précise, là où le mode ORDINAIRE (qui ignore les piles fines) attend la
  // zone large de l'emplacement pour reconnaître un lâcher « sans cible ».
  it('lâchée dans la marge d’une unité de pile, sans toucher sa carte : la zone large, pas la pile', () => {
    const { margeUnite } = poserPlateau({
      zoneEmplacement: 'piles-joueur',
      pileUnite: 'joueur-deck',
      carteId: 5,
      margeDansLUnite: true,
    })
    document.elementFromPoint = () => margeUnite!
    expect(cibleSousLePoint(0, 0)).toEqual({ carteId: undefined, zone: 'piles-joueur' })
  })

  // Le secteur (posé sur le GROUPE entier, ex. « ennemis engagés ») est une
  // autre famille : le mode manuel a besoin qu'il compte même hors carte,
  // pour engager un sbire lâché dans l'espace vide du secteur.
  it('lâchée dans l’espace vide d’un secteur (hors de toute carte) : le secteur', () => {
    const { margeGroupe } = poserPlateau({
      zoneEmplacement: 'terrain-combat',
      pileGroupe: 'terrain-combat-engages',
      margeDansLeGroupe: true,
    })
    document.elementFromPoint = () => margeGroupe!
    expect(cibleSousLePoint(0, 0)).toEqual({ carteId: undefined, zone: 'terrain-combat-engages' })
  })

  it('lâchée sur une carte qui vit dans un secteur : le secteur, et la carte', () => {
    const { scanCard } = poserPlateau({
      zoneEmplacement: 'terrain-combat',
      pileGroupe: 'terrain-combat-engages',
      carteId: 7,
    })
    document.elementFromPoint = () => scanCard!
    expect(cibleSousLePoint(0, 0)).toEqual({ carteId: 7, zone: 'terrain-combat-engages' })
  })

  it('lâchée sur une carte ordinaire, sans pile ni secteur : la zone large, et la carte', () => {
    const { scanCard } = poserPlateau({ zoneEmplacement: 'terrain-combat', carteId: 9 })
    document.elementFromPoint = () => scanCard!
    expect(cibleSousLePoint(0, 0)).toEqual({ carteId: 9, zone: 'terrain-combat' })
  })

  it('lâchée dans le vide (rien à cette position) : rien du tout', () => {
    document.body.innerHTML = ''
    document.elementFromPoint = () => null
    expect(cibleSousLePoint(0, 0)).toEqual({ carteId: undefined, zone: undefined })
  })
})
