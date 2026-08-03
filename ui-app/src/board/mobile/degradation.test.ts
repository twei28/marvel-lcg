import { describe, expect, it } from 'vitest'
import {
  chiffresResume,
  coutFixeTuiles,
  coutResume,
  MESURES_PAR_DEFAUT,
  ORDRE_DEGRADATION,
  planifier,
  plancherTuiles,
  type ExigenceBande,
  type MesuresBande,
} from './degradation'
import type { CleBande } from './bandes'
import { TUILE_PLANCHER } from './condensation'
import type { UniteAffichee } from '../zones'

const MESURES: MesuresBande = MESURES_PAR_DEFAUT

const POIDS: Record<CleBande, number> = {
  vilain: 140,
  complots: 110,
  terrain: 120,
  rencontre: 64,
  heros: 200,
  main: 76,
}

const TOUTES: CleBande[] = ['vilain', 'complots', 'terrain', 'rencontre', 'heros', 'main']

function exigences(cles: CleBande[] = TOUTES, supplements: Partial<Record<CleBande, number>> = {}): ExigenceBande[] {
  return cles.map((cle) => ({
    cle,
    poids: POIDS[cle],
    plancher: plancherTuiles(supplements[cle] ?? 0),
  }))
}

/**
 * Ce que le rendu prendra REELLEMENT, d'apres le plan. C'est cette somme qui
 * doit tenir dans la hauteur mesuree : c'est tout l'invariant.
 */
function hauteurRendue(
  bandes: ExigenceBande[],
  plan: ReturnType<typeof planifier>,
  mesures: MesuresBande
): number {
  let total = 0
  let resumes = 0
  for (const bande of bandes) {
    if (plan.modes.get(bande.cle) === 'tuiles') {
      total += coutFixeTuiles(mesures) + (plan.hauteurs.get(bande.cle) ?? 0)
    } else {
      resumes += 1
    }
  }
  const rangeesResumes = Math.ceil(resumes / plan.colonnes)
  return total + rangeesResumes * coutResume(mesures)
}

describe('mesures de bande', () => {
  it('chiffre le cout fixe d\'une bande a tuiles a partir des mesures, sans constante', () => {
    // 44 (titre) + 12 (padding) + 1 (bordure) + 4 (ecart) = 61. C'est la valeur
    // relevee en Chromium reel ; l'ancien OVERHEAD_BANDE affirmait 60.
    expect(coutFixeTuiles(MESURES)).toBe(61)
  })

  it('une ligne de resume ne coute que son titre et sa bordure', () => {
    expect(coutResume(MESURES)).toBe(45)
    expect(coutResume(MESURES)).toBeGreaterThanOrEqual(44)
  })

  it('le plancher d\'une bande non vide est celui de la pastille « +N »', () => {
    expect(plancherTuiles()).toBe(TUILE_PLANCHER.hauteur)
    expect(plancherTuiles(48)).toBe(TUILE_PLANCHER.hauteur + 48)
  })
})

describe('planifier', () => {
  it('garde toutes les tuiles quand la hauteur suffit', () => {
    const bandes = exigences()
    // 6 * (61 + 64) = 750 : au-dessus, aucune bande n'est degradee.
    const plan = planifier(bandes, 900, MESURES)
    for (const cle of TOUTES) expect(plan.modes.get(cle)).toBe('tuiles')
    expect(plan.colonnes).toBe(1)
  })

  it('degrade dans l\'ordre annonce, la bande la moins urgente d\'abord', () => {
    const bandes = exigences()
    // Juste sous les 750 px requis : une seule bande doit tomber.
    const plan = planifier(bandes, 700, MESURES)
    const degradees = TOUTES.filter((cle) => plan.modes.get(cle) === 'resume')
    expect(degradees).toEqual(['rencontre'])
  })

  it('degrade cumulativement, et n\'atteint heros qu\'en dernier', () => {
    const bandes = exigences()
    const attendu: CleBande[] = []
    for (const cle of ORDRE_DEGRADATION) {
      attendu.push(cle)
      // Une hauteur qui force exactement `attendu.length` degradations.
      const restantes = TOUTES.length - attendu.length
      const disponible =
        restantes * (coutFixeTuiles(MESURES) + TUILE_PLANCHER.hauteur) +
        attendu.length * coutResume(MESURES)
      const plan = planifier(bandes, disponible, MESURES)
      const degradees = TOUTES.filter((c) => plan.modes.get(c) === 'resume')
      expect(new Set(degradees)).toEqual(new Set(attendu))
    }
    expect(ORDRE_DEGRADATION[ORDRE_DEGRADATION.length - 1]).toBe('heros')
    expect(ORDRE_DEGRADATION[0]).toBe('rencontre')
  })

  it('tient l\'invariant : le rendu ne depasse jamais la hauteur mesuree', () => {
    const bandes = exigences()
    // Le balayage part de 0 et non de 140 : c'est EN DESSOUS que l'invariant
    // se joue. Il n'y a que deux issues admises, jamais un rognage muet : ou
    // bien le rendu tient, ou bien le plan annonce le defilement.
    for (let disponible = 0; disponible <= 1100; disponible += 1) {
      const plan = planifier(bandes, disponible, MESURES)
      const rendu = hauteurRendue(bandes, plan, MESURES)
      expect(
        rendu <= disponible || plan.defilement,
        `hauteur disponible ${disponible} : rendu ${rendu}, defilement ${plan.defilement}`
      ).toBe(true)
      // Et le drapeau ne ment pas dans l'autre sens : pas de barre de
      // defilement la ou tout tient.
      expect(plan.defilement, `hauteur disponible ${disponible}`).toBe(rendu > disponible)
    }
  })

  it('ne donne jamais a une bande a tuiles moins que son plancher', () => {
    const bandes = exigences()
    for (let disponible = 0; disponible <= 1100; disponible += 1) {
      const plan = planifier(bandes, disponible, MESURES)
      for (const bande of bandes) {
        if (plan.modes.get(bande.cle) !== 'tuiles') continue
        expect(plan.hauteurs.get(bande.cle) ?? 0).toBeGreaterThanOrEqual(bande.plancher)
      }
    }
  })

  it('couvre les bandeaux joueurs replies : a 4 joueurs, heros garde de quoi montrer sa pastille', () => {
    // 3 bandeaux replies a 48 px chacun, comme sur le gabarit 390x844 ou le
    // « +5 » etait entierement invisible.
    const bandes = exigences(TOUTES, { heros: 3 * 48 })
    for (let disponible = 200; disponible <= 1100; disponible += 1) {
      const plan = planifier(bandes, disponible, MESURES)
      if (plan.modes.get('heros') !== 'tuiles') continue
      const hauteur = plan.hauteurs.get('heros') ?? 0
      // Ce qui reste APRES les bandeaux doit encore valoir une pastille.
      expect(hauteur - 3 * 48).toBeGreaterThanOrEqual(TUILE_PLANCHER.hauteur)
      expect(hauteurRendue(bandes, plan, MESURES)).toBeLessThanOrEqual(disponible)
    }
  })

  it('passe les resumes sur deux colonnes quand meme empiles ils ne tiennent pas', () => {
    const bandes = exigences()
    // 6 * 45 = 270 : en dessous, une colonne ne suffit plus.
    const plan = planifier(bandes, 200, MESURES)
    expect(plan.colonnes).toBe(2)
    for (const cle of TOUTES) expect(plan.modes.get(cle)).toBe('resume')
    expect(hauteurRendue(bandes, plan, MESURES)).toBeLessThanOrEqual(200)
  })

  it('reste a une colonne des que les resumes tiennent empiles', () => {
    const plan = planifier(exigences(), 270, MESURES)
    expect(plan.colonnes).toBe(1)
    expect(plan.defilement).toBe(false)
  })

  it('fait defiler quand meme les resumes en deux colonnes ne tiennent pas', () => {
    const bandes = exigences()
    // 6 bandes en 2 colonnes = 3 rangees de 45 = 135 px. A 135 tout tient
    // encore ; a 134, la rangee du bas etait rognee en silence.
    const juste = planifier(bandes, 135, MESURES)
    expect(juste.colonnes).toBe(2)
    expect(juste.defilement).toBe(false)

    const trop = planifier(bandes, 134, MESURES)
    expect(trop.colonnes).toBe(2)
    expect(trop.defilement).toBe(true)
    // Aucune bande n'est sacrifiee : elles sont toutes rendues, toutes
    // atteignables, et c'est le defilement qui donne acces au bas.
    for (const cle of TOUTES) expect(trop.modes.get(cle)).toBe('resume')
  })

  it('n\'exige rien d\'une bande sans unite et ne lui donne aucune hauteur', () => {
    const bandes: ExigenceBande[] = [
      { cle: 'vilain', poids: POIDS.vilain, plancher: plancherTuiles() },
      { cle: 'main', poids: 0, plancher: 0 },
    ]
    const plan = planifier(bandes, 200, MESURES)
    expect(plan.modes.get('main')).toBe('tuiles')
    expect(plan.hauteurs.get('main')).toBe(0)
  })

  it('ne plante pas sur une hauteur nulle', () => {
    const plan = planifier(exigences(), 0, MESURES)
    for (const cle of TOUTES) expect(plan.modes.get(cle)).toBe('resume')
    expect(plan.colonnes).toBe(2)
    expect(plan.defilement).toBe(true)
  })

  it('ignore une bande absente de la liste dans l\'ordre de degradation', () => {
    const bandes = exigences(['vilain', 'heros'])
    // 2 * 125 = 250 ne tient pas ; degrader vilain donne 45 + 125 = 170, qui tient.
    const plan = planifier(bandes, 175, MESURES)
    expect(plan.modes.get('vilain')).toBe('resume')
    expect(plan.modes.get('heros')).toBe('tuiles')
    expect(plan.modes.has('rencontre')).toBe(false)
  })
})

function unite(carte: Partial<UniteAffichee['carte']>, cle = 'u'): UniteAffichee {
  return {
    cle,
    carte: { id: '1', name: 'Carte', kind: 'ally', imageUrl: '', ...carte },
    attachees: [],
  }
}

describe('chiffresResume', () => {
  it('prend les PV, la menace et la hauteur de pile, dans cet ordre de priorite', () => {
    expect(
      chiffresResume([
        unite({ allyHp: '12/22' }, 'a'),
        unite({ schemeThreat: '3/12' }, 'b'),
        unite({ pileCount: 7 }, 'c'),
      ])
    ).toEqual(['12/22', '3/12', '7'])
  })

  it('ne divulgue rien d\'une carte face cachee', () => {
    expect(chiffresResume([unite({ facedown: true, allyHp: '4/4' }, 'a')])).toEqual([])
    expect(chiffresResume([unite({ facedown: true, peeking: true, allyHp: '4/4' }, 'a')])).toEqual([
      '4/4',
    ])
  })

  it('s\'arrete a trois chiffres pour que la ligne reste une ligne', () => {
    const unites = Array.from({ length: 8 }, (_, index) =>
      unite({ allyHp: `${index}/9` }, `u${index}`)
    )
    expect(chiffresResume(unites)).toHaveLength(3)
  })

  it('ne rend rien pour des cartes sans aucun chiffre (une main)', () => {
    expect(chiffresResume([unite({}, 'a'), unite({}, 'b')])).toEqual([])
  })
})
