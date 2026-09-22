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
//
// Ronde de correction 2 (revue finale, constat C1) : le cas du SECTEUR ci-
// dessous encodait le défaut comme voulu — « le secteur compte MÊME hors
// carte » était vrai, mais il écrasait alors `zone`, la seule chose que le
// mode ORDINAIRE lit. Un lâcher sans carte au milieu du secteur « ennemis
// engagés » (`terrain-combat-engages`, dessiné dans TOUTES les parties)
// rendait donc `zone: 'terrain-combat-engages'` au lieu de `zone:
// 'terrain-combat'`, une zone que le mode ordinaire ne connaît pas : la
// carte s'y voyait refusée à tort. Le secteur vit maintenant dans son PROPRE
// champ (`secteur`), que `zone` ne porte plus jamais.
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
  /** Pile vide (22/09/2026) : `.plateau-unite.pile-vide`, SANS `.scan-card`
   *  dedans — le rendu exact de `Board.tsx` pour une pile sans carte. */
  pileVide?: boolean
}): { scanCard?: HTMLElement; margeUnite?: HTMLElement; margeGroupe?: HTMLElement; pileVide?: HTMLElement } {
  document.body.innerHTML = ''
  const section = document.createElement('section')
  section.dataset.zone = options.zoneEmplacement
  const groupe = document.createElement('div')
  groupe.className = 'plateau-groupe'
  if (options.pileGroupe !== undefined) groupe.dataset.pile = options.pileGroupe

  const unite = document.createElement('div')
  unite.className = options.pileVide ? 'plateau-unite pile-vide' : 'plateau-unite'
  if (options.pileUnite !== undefined) unite.dataset.pile = options.pileUnite

  let pileVideSpan: HTMLElement | undefined
  if (options.pileVide) {
    pileVideSpan = document.createElement('span')
    unite.appendChild(pileVideSpan)
  }

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
  return { scanCard, margeUnite, margeGroupe, pileVide: pileVideSpan }
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

  // ⚠ LE CAS QUI MANQUAIT AU CORRECTIF DU 21/09/2026 (« les piles vides
  // acceptent la première carte », ca02560f). Il n'existait qu'un test de la
  // COUCHE DE DONNÉES (`glisser-manuel.test.ts`, `construirePlateau` rend
  // bien `pileVide: true`) : rien n'exerçait le VRAI hit-test DOM. Or
  // `Board.tsx` dessine une pile vide SANS `.scan-card` dedans (l'encadré en
  // pointillés) — et le cas du dessus prouve précisément que sans carte, un
  // lâcher retombe sur la zone LARGE, jamais sur la pile fine. Sans le
  // correctif de `cibleSousLePoint`, ce cas rendrait `zone: 'piles-joueur'`
  // au lieu de `'joueur-defausse'` : la pile vide resterait viséE, mais le
  // dépôt manuel la refuserait quand même (`PILE_PAR_ZONE['piles-joueur']`
  // n'existe pas), l'exact inverse de ce que le correctif promet.
  it('lâchée sur une pile VIDE (aucune carte dedans) : la pile fine quand même', () => {
    const { pileVide } = poserPlateau({
      zoneEmplacement: 'piles-joueur',
      pileUnite: 'joueur-defausse',
      pileVide: true,
    })
    document.elementFromPoint = () => pileVide!
    expect(cibleSousLePoint(0, 0)).toEqual({ carteId: undefined, zone: 'joueur-defausse' })
  })

  // ⚠ LE CAS C1. Le secteur (posé sur le GROUPE entier, ex. « ennemis
  // engagés ») compte même hors carte — le mode manuel en a besoin pour
  // engager un sbire lâché dans l'espace vide du secteur — mais il vit dans
  // SON PROPRE champ : `zone` reste l'emplacement LARGE, celui que le mode
  // ordinaire comprend, quoi qu'il arrive.
  it('lâchée dans l’espace vide d’un secteur (hors de toute carte) : la zone large, et le secteur à part', () => {
    const { margeGroupe } = poserPlateau({
      zoneEmplacement: 'terrain-combat',
      pileGroupe: 'terrain-combat-engages',
      margeDansLeGroupe: true,
    })
    document.elementFromPoint = () => margeGroupe!
    expect(cibleSousLePoint(0, 0)).toEqual({
      carteId: undefined,
      zone: 'terrain-combat',
      secteur: 'terrain-combat-engages',
    })
  })

  // Le pendant du cas ci-dessus : c'est justement parce que `zone` reste
  // l'emplacement large que le mode ORDINAIRE, qui ne lit jamais `secteur`,
  // continue de reconnaître ce lâcher comme un lâcher « sur le terrain » et
  // joue toujours la carte — au lieu du refus que C1 signalait.
  it('mode ordinaire : ce même lâcher garde une zone qu’il reconnaît', () => {
    const { margeGroupe } = poserPlateau({
      zoneEmplacement: 'terrain-combat',
      pileGroupe: 'terrain-combat-engages',
      margeDansLeGroupe: true,
    })
    document.elementFromPoint = () => margeGroupe!
    const { zone } = cibleSousLePoint(0, 0)
    // `ZONES_DU_TERRAIN` (glisser/cibles.ts) est ce que le mode ordinaire
    // sait accueillir sans cible : la zone rendue doit en faire partie.
    expect(zone).toBe('terrain-combat')
  })

  it('lâchée sur une carte qui vit dans un secteur : la zone large, le secteur, et la carte', () => {
    const { scanCard } = poserPlateau({
      zoneEmplacement: 'terrain-combat',
      pileGroupe: 'terrain-combat-engages',
      carteId: 7,
    })
    document.elementFromPoint = () => scanCard!
    expect(cibleSousLePoint(0, 0)).toEqual({
      carteId: 7,
      zone: 'terrain-combat',
      secteur: 'terrain-combat-engages',
    })
  })

  it('lâchée sur une carte ordinaire, sans pile ni secteur : la zone large, et la carte', () => {
    const { scanCard } = poserPlateau({ zoneEmplacement: 'terrain-combat', carteId: 9 })
    document.elementFromPoint = () => scanCard!
    expect(cibleSousLePoint(0, 0)).toEqual({ carteId: 9, zone: 'terrain-combat', secteur: undefined })
  })

  it('lâchée dans le vide (rien à cette position) : rien du tout', () => {
    document.body.innerHTML = ''
    document.elementFromPoint = () => null
    expect(cibleSousLePoint(0, 0)).toEqual({ carteId: undefined, zone: undefined })
  })
})
