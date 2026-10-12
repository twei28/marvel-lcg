// Le cartouche du bas (refonte du 04/10/2026, scene PC, mode « Étape par
// étape ») : la PRESENTATION seule. Le rythme (index, validation, accuse de
// reception) reste a `DeroulePhase`, qui lui passe ses valeurs ; ces cas
// verifient ce qu'il dessine, etat par etat de la planche (D40), et ce qu'il
// appelle.
//
// Les textes passent par `ecran` (piege 24) : une phrase decoupee en plusieurs
// elements reste trouvable.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render } from '@testing-library/react'
import { CartoucheHorsPhase, CartouchePhase, RelectureJournal, type CartouchePhaseProps } from './CartouchePhase'
import type { EtapeDeroule } from './deroule-phase'
import type { ScanCardProps } from '../components/ScanCard'
import { ecran as screen } from '../test-textes'
import type { Demande, Option } from './ask'
import type { Interaction } from './interaction'
import type { QuestionDuMoteur } from './sous-cadre'
import type { WorldCard } from './world'

// jsdom n'implemente pas ResizeObserver : la loupe (usePlacement) observe son
// panneau. Meme bouchon inerte que Board.test.tsx.
class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
beforeEach(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
})

const scan = (id: number, faceVisible = true): ScanCardProps => ({
  id: String(id),
  name: `carte ${id}`,
  kind: 'minion',
  imageUrl: `/scan/${id}${faceVisible ? '' : '-dos'}`,
})

const RHINO = 50
const SPIDER = 12
const MANIGANCE = 70

const menace: EtapeDeroule = {
  cle: 'menace:1',
  temps: 'menace',
  titre: 'menace',
  regle: '',
  cibleId: MANIGANCE,
  cibleNom: 'The Break-In!',
  montant: 1,
  restant: 3,
  plafond: 7,
  boosts: [],
}

// Etat 3 de la planche : l'attaque resolue, un boost sans etoile.
const attaqueResolue: EtapeDeroule = {
  cle: 'activation:3',
  temps: 'mechant',
  titre: 'attaque',
  regle: '',
  etat: 'resolu',
  carteId: RHINO,
  cibleId: SPIDER,
  auteurNom: 'Rhino',
  cibleNom: 'Spider-Man',
  base: 2,
  montant: 3,
  restant: 7,
  boosts: [{ cle: 'b1', nom: 'Charge', cibleId: 91, apport: 1 }],
}

const annonce: EtapeDeroule = {
  cle: 'activation:4',
  temps: 'mechant',
  titre: 'attaque',
  regle: '',
  etat: 'annonce',
  carteId: RHINO,
  cibleId: SPIDER,
  auteurNom: 'Rhino',
  cibleNom: 'Spider-Man',
  valeurAnnoncee: 2,
  boosts: [],
}

const gestes = {
  onPointerDown: () => {},
  onPointerMove: () => {},
  onPointerUp: () => {},
  onPointerCancel: () => {},
}

function monter(sur: Partial<CartouchePhaseProps> & { etapes?: EtapeDeroule[] } = {}) {
  const etapes = sur.etapes ?? [menace, attaqueResolue]
  const index = sur.index ?? 0
  const props: CartouchePhaseProps = {
    refCartouche: () => {},
    gestes,
    etape: etapes[index],
    etapes,
    index,
    efface: false,
    questionAuJoueur: false,
    avancer: vi.fn(),
    enAttente: false,
    attendUnAutreJoueur: false,
    defaiteLocale: false,
    boostsMontres: 99,
    tempsParDecision: 0,
    cartesDistribuees: 0,
    carteScene: scan,
    pvMaxParNom: new Map([['Spider-Man', 10]]),
    ...sur,
  }
  return { ...render(<CartouchePhase {...props} />), props }
}

const section = () => document.querySelector<HTMLElement>('section.deroule-phase')
const corps = () => document.querySelector<HTMLElement>('.deroule-corps')

afterEach(() => {
  cleanup()
  document.body.className = ''
})

describe('le cadre du cartouche', () => {
  it('une section de dialogue en scene, jamais posee sur la table', () => {
    monter()
    expect(section()?.className).toContain('deroule-phase')
    expect(section()?.className).toContain('est-scene')
    expect(section()?.className).not.toContain('est-sur-table')
    expect(section()?.getAttribute('role')).toBe('dialog')
  })

  // 10/10/2026 : l'ancien « Bis » est LA presentation « Etape par etape ».
  // Seul le cartouche pose sur la table (`bis={false}`) garde l'ancienne.
  it('porte la presentation Etape par etape (ex-Bis) par defaut, pas sur la table', () => {
    const scene = monter()
    expect(section()?.className).toContain('est-bis')
    scene.unmount()
    monter({ bis: false })
    expect(section()?.className).not.toContain('est-bis')
  })

  it('l en-tete tient sur deux lignes : la frise des pastilles, puis le titre', () => {
    monter()
    const haut = document.querySelector('.deroule-ligne-haut')
    expect(haut).not.toBeNull()
    const [frise, titre] = Array.from(haut?.children ?? [])
    expect(frise?.classList.contains('deroule-frise')).toBe(true)
    expect(frise?.querySelectorAll('li.deroule-pastille')).toHaveLength(5)
    expect(titre?.tagName).toBe('H2')
    expect(titre?.classList.contains('deroule-titre-court')).toBe(true)
  })

  it('se deplace en l attrapant sur un fond libre, jamais sur une carte ni sur un bouton', () => {
    const onPointerDown = vi.fn()
    monter({ index: 1, gestes: { ...gestes, onPointerDown } })
    fireEvent.pointerDown(document.querySelector('.deroule-titre-court') as Element, { button: 0 })
    expect(onPointerDown).toHaveBeenCalledTimes(1)
    fireEvent.pointerDown(section() as Element, { button: 0 })
    expect(onPointerDown).toHaveBeenCalledTimes(2)
    fireEvent.pointerDown(document.querySelector('.deroule-rangee .deroule-vignette [data-card-id]') as Element, { button: 0 })
    fireEvent.pointerDown(screen.getByRole('button', { name: 'Suivant (espace)' }), { button: 0 })
    expect(onPointerDown).toHaveBeenCalledTimes(2)
  })

  it('le carre est ferme : aucune poignee reservee a une bande du haut', () => {
    monter()
    expect(document.querySelector('.deroule-ligne-haut')?.classList.contains('poignee-glisser')).toBe(false)
    expect(section()?.classList.contains('poignee-glisser')).toBe(true)
  })

  it('cinq pastilles ; la quatrieme dit « 1 carte distribuée » une fois passee', () => {
    const revelation: EtapeDeroule = {
      cle: 'revelation:1',
      temps: 'revelation',
      titre: 'revelation',
      regle: '',
      carteId: 88,
      cibleNom: 'Stampede',
      boosts: [],
    }
    monter({ etapes: [menace, revelation, { cle: 'bilan', temps: 'bilan', titre: 'bilan', regle: '', boosts: [] }], index: 2, cartesDistribuees: 1 })
    const pastilles = document.querySelectorAll('li.deroule-pastille')
    expect(pastilles).toHaveLength(5)
    expect(pastilles[3].getAttribute('title')).toBe('3. Cartes rencontre')
    expect(pastilles[3].querySelector('.deroule-pastille-resume')?.textContent).toMatch(/^1 carte distribuée/)
    expect(pastilles[4].className).toContain('est-courant')
  })

  it('le corps porte la phrase de l etape en nom accessible', () => {
    monter({ index: 1 })
    expect(corps()?.getAttribute('aria-label')).toBe('Rhino attaque Spider-Man')
  })

  it('aucun panneau de question d avant dans la section', () => {
    monter({ index: 1 })
    for (const ancien of ['.demande-centrale', '.cibles-scene', '.assistant-action']) {
      expect(section()?.querySelector(ancien), ancien).toBeNull()
    }
  })
})

describe('les etats de la planche (sans question)', () => {
  it('etat 3 : la rangee resolue, boost colle, total en gros, resultat et jauge', () => {
    monter({ index: 1 })
    expect(document.querySelector('.deroule-titre-court')?.textContent).toBe('Attaque de Rhino')
    const rangee = document.querySelector('.deroule-rangee')
    expect(rangee).not.toBeNull()
    expect(rangee?.querySelectorAll('.deroule-vignette').length).toBeGreaterThanOrEqual(3)
    expect(screen.getByText('ATQ 2')).toBeInTheDocument()
    expect(screen.getByText('+1')).toBeInTheDocument()
    const total = document.querySelector('.deroule-total')
    expect(total?.textContent).toBe('= 3')
    expect(total?.classList.contains('est-gros')).toBe(true)
    expect(screen.getByText('3 dégâts subis')).toBeInTheDocument()
    expect(document.querySelector('.deroule-jauge')?.textContent).toBe('10 → 7 / 10')
    expect(document.querySelector('.deroule-etoile')).toBeNull()
  })

  it('etat 3 bis : un boost etoile ajoute sa ligne ★ sous la rangee', () => {
    const etoile: EtapeDeroule = { ...attaqueResolue, boosts: [{ cle: 'b1', nom: 'Sweeping Swoop', cibleId: 91, apport: 0, etoile: true }] }
    monter({ etapes: [etoile], index: 0, texteEtoile: () => 'sonnez ce personnage.' })
    expect(screen.getByText('★ Sweeping Swoop : sonnez ce personnage.')).toBeInTheDocument()
  })

  it('etat 4 : l activation annulee, barree, avec sa cause', () => {
    const annulee: EtapeDeroule = { ...annonce, etat: 'annule', annuleePar: 'stunned' }
    monter({ etapes: [annulee], index: 0 })
    expect(document.querySelector('.deroule-rangee.est-annulee')).not.toBeNull()
    expect(screen.getByText('Annulée · Sonné')).toBeInTheDocument()
  })

  it('etat 5 : la manigance du mechant, titre court et jauge sur le seuil', () => {
    const manigance: EtapeDeroule = {
      cle: 'activation:5',
      temps: 'mechant',
      titre: 'manigance',
      regle: '',
      etat: 'resolu',
      carteId: RHINO,
      cibleId: MANIGANCE,
      auteurNom: 'Rhino',
      cibleNom: 'The Break-In!',
      base: 2,
      montant: 2,
      restant: 6,
      plafond: 7,
      boosts: [],
    }
    monter({ etapes: [manigance], index: 0 })
    expect(document.querySelector('.deroule-titre-court')?.textContent).toBe('Manigance')
    expect(document.querySelector('.deroule-jauge')?.textContent).toBe('4 → 6 / 7')
  })

  it('etat 6 : deux sbires, la pastille ③ courante dit « 1 / 2 »', () => {
    const sbire = (n: number): EtapeDeroule => ({
      ...attaqueResolue,
      cle: `activation:s${n}`,
      temps: 'sbires',
      auteurNom: `Sbire ${n}`,
      carteId: 60 + n,
      boosts: [],
    })
    monter({ etapes: [sbire(1), sbire(2)], index: 0 })
    const courante = document.querySelector('li.deroule-pastille.est-courant')
    expect(courante?.getAttribute('title')).toBe('2B. Les sbires s’activent')
    expect(courante?.querySelector('.deroule-pastille-compteur')?.textContent).toBe('1 / 2')
  })

  it('etat 7 : le stade, ancienne carte puis nouvelle, et ce qui change', () => {
    const stade: EtapeDeroule = {
      cle: 'stade:1',
      temps: 'menace',
      titre: 'stade',
      regle: '',
      stade: 'mechant',
      carteId: 51,
      cibleNom: 'Rhino',
      auteurNom: 'Rhino',
      stadeAvantId: RHINO,
      statsAvant: { pv_max: 14, atq: 2, man: 1 },
      statsApres: { pv_max: 15, atq: 3, man: 1 },
      boosts: [],
    }
    monter({ etapes: [stade], index: 0, infoCarte: (id) => (id === 51 ? { printed_stage: 2 } : undefined) })
    expect(document.querySelector('.deroule-titre-court')?.textContent).toBe('Stade II')
    expect(document.querySelectorAll('.deroule-stade .deroule-vignette')).toHaveLength(2)
    expect(screen.getByText('PV 14 → 15')).toBeInTheDocument()
    expect(screen.getByText('ATQ 2 → 3')).toBeInTheDocument()
    expect(screen.queryByText(/MAN 1 → 1/)).toBeNull()
  })

  it('etat 8 : la carte revelee en grand, son type et son effet resume', () => {
    const revelee: EtapeDeroule = {
      cle: 'revelation:8',
      temps: 'revelation',
      titre: 'revelation',
      regle: '',
      carteId: 88,
      auteurNom: 'Spider-Man',
      cibleNom: 'Stampede',
      typeCarte: 'Treachery',
      effets: [{ genre: 'degats', cible: 'Spider-Man', cible_id: SPIDER, montant: 2, restant: 8 }],
      boosts: [],
    }
    monter({ etapes: [revelee], index: 0 })
    expect(document.querySelector('.deroule-revelee .deroule-carte-grande')).not.toBeNull()
    expect(document.querySelector('.deroule-titre-court')?.textContent).toBe('Stampede (Traîtrise)')
    expect(screen.getByText('→ Spider-Man subit 2 dégâts (8 PV)')).toBeInTheDocument()
  })

  it('etat 9 : le Renfort, une fleche et la carte suivante a cote', () => {
    const premiere: EtapeDeroule = {
      cle: 'revelation:9',
      temps: 'revelation',
      titre: 'revelation',
      regle: '',
      carteId: 88,
      cibleNom: 'Hard to Keep Down',
      suivieDUnRenfort: true,
      boosts: [],
    }
    const suivante: EtapeDeroule = {
      cle: 'revelation:10',
      temps: 'revelation',
      titre: 'revelation',
      regle: '',
      carteId: 89,
      cibleNom: 'Charge',
      parSurge: true,
      renfortDe: 'Hard to Keep Down',
      boosts: [],
    }
    monter({ etapes: [premiere, suivante], index: 0 })
    const revelee = document.querySelector('.deroule-revelee.a-renfort')
    expect(revelee).not.toBeNull()
    expect(revelee?.querySelectorAll('.deroule-carte-grande')).toHaveLength(2)
    expect(screen.getByText('→ Renfort')).toBeInTheDocument()
  })

  it('etat 9, avant le clic : le Renfort annonce une case vide « ? » a la place de la carte suivante', () => {
    const premiere: EtapeDeroule = {
      cle: 'revelation:9',
      temps: 'revelation',
      titre: 'revelation',
      regle: '',
      carteId: 88,
      cibleNom: 'Hard to Keep Down',
      boosts: [],
    }
    monter({ etapes: [premiere], index: 0, infoRevelee: () => ({ renfort: true }) })
    const revelee = document.querySelector('.deroule-revelee.a-renfort')
    expect(revelee).not.toBeNull()
    expect(revelee?.querySelectorAll('.deroule-carte-grande')).toHaveLength(1)
    expect(screen.getByText('→ Renfort')).toBeInTheDocument()
    expect(revelee?.querySelector('.deroule-renfort-vide')?.textContent).toBe('?')
  })

  // Rapport Yarro n72 (09/10/2026) : Weapons Runner → Renfort → Klaw's Vengeance
  // annulee par Stepford Cuckoos → Sonic Boom. La chaine se dessine en direct,
  // la case « ? » laisse place a la vraie carte des que son fait existe.
  const chaineN72: EtapeDeroule[] = [
    { cle: 'revelation:3:0:65', temps: 'revelation', titre: 'revelation', regle: '', carteId: 65,
      cibleNom: 'Weapons Runner', suivieDUnRenfort: true, boosts: [] },
    { cle: 'revelation:3:1:66', temps: 'revelation', titre: 'revelation', regle: '', carteId: 66,
      cibleNom: "Klaw's Vengeance", parSurge: true, renfortDe: 'Weapons Runner', annuleePar: 'Stepford Cuckoos',
      annuleeParId: 32, annuleeParSort: 'defaussee', suivieDUnRemplacement: true, boosts: [] },
    { cle: 'revelation:3:2:69', temps: 'revelation', titre: 'revelation', regle: '', carteId: 69,
      cibleNom: 'Sonic Boom', reveleePar: 'Stepford Cuckoos', reveleeParId: 32, boosts: [] },
  ]

  it('n72 : la chaine en petites vignettes, la carte annulee marquee, la sortie de Stepford dite', () => {
    monter({ etapes: chaineN72, index: 1, infoRevelee: () => ({ renfort: false }) })
    const maillons = [...document.querySelectorAll('.deroule-chaine .deroule-chaine-maillon')]
    expect(maillons).toHaveLength(3)
    expect(maillons[1].classList.contains('est-courante')).toBe(true)
    expect(maillons[1].classList.contains('est-annulee')).toBe(true)
    expect(maillons[1].querySelector('.deroule-chaine-annulee')?.textContent).toBe('Annulée par Stepford Cuckoos')
    expect(maillons[2].querySelector('.deroule-chaine-lien')?.textContent).toBe('→ Révélée par Stepford Cuckoos')
    expect(screen.getByText('Stepford Cuckoos : défaussée')).toBeInTheDocument()
    expect(screen.getByText('→ Révélée par Stepford Cuckoos', { selector: '.deroule-renfort-fleche' })).toBeInTheDocument()
  })

  it('n72 : la case « ? » laisse place a la carte du Renfort des qu elle est connue', () => {
    monter({ etapes: chaineN72, index: 0, infoRevelee: () => ({ renfort: true }) })
    const revelee = document.querySelector('.deroule-revelee')
    expect(revelee?.querySelector('.deroule-renfort-vide')).toBeNull()
    expect(revelee?.querySelectorAll('.deroule-carte-grande')).toHaveLength(2)
  })

  it('etat 12 : le bilan en trois colonnes, et « Terminer »', () => {
    const bilan: EtapeDeroule = { cle: 'bilan', temps: 'bilan', titre: 'bilan', regle: '', boosts: [] }
    const avancer = vi.fn()
    monter({ etapes: [menace, attaqueResolue, bilan], index: 2, avancer })
    expect(document.querySelectorAll('.deroule-bilan .deroule-colonne')).toHaveLength(3)
    expect(document.querySelector('.deroule-titre-court')?.textContent).toBe('Bilan')
    fireEvent.click(screen.getByRole('button', { name: 'Terminer' }))
    expect(avancer).toHaveBeenCalledTimes(1)
  })
})

describe('le bilan vide', () => {
  it('une phrase plutot que trois colonnes vides', () => {
    const bilan: EtapeDeroule = { cle: 'bilan', temps: 'bilan', titre: 'bilan', regle: '', boosts: [] }
    monter({ etapes: [bilan], index: 0 })
    expect(screen.getByText('Aucun dégât, aucune menace.')).toBeInTheDocument()
    expect(document.querySelector('.deroule-colonne')).toBeNull()
    expect(screen.getByRole('button', { name: 'Terminer' })).toBeInTheDocument()
  })
})

describe('le pied du cartouche', () => {
  it('« Suivant (espace) » appelle avancer', () => {
    const { props } = monter()
    fireEvent.click(screen.getByRole('button', { name: 'Suivant (espace)' }))
    expect(props.avancer).toHaveBeenCalledTimes(1)
  })

  it('« Continuer » sur la chute de notre heros, et la phase s arrete la', () => {
    const fatal: EtapeDeroule = { ...attaqueResolue, restant: 0, defaite: true }
    monter({ etapes: [fatal], index: 0, defaiteLocale: true })
    expect(screen.getByRole('button', { name: 'Continuer' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Suivant/ })).toBeNull()
    expect(screen.getByText('La phase s\'arrête ici.')).toBeInTheDocument()
  })

  it('une annonce ne porte jamais « Suivant » : elle se complete sur place (piege 2)', () => {
    // La rangee d'annonce porte la question, ou rien ; la rangee resolue porte
    // toujours « Suivant ». Un clic sur l'annonce la validerait dans cet etat,
    // et le resultat passerait sans etre lu.
    monter({ etapes: [annonce], index: 0 })
    expect(screen.queryByRole('button', { name: /Suivant/ })).toBeNull()
  })

  it('une annonce DEPASSEE (une etape la suit deja) porte « Suivant » : sinon le joueur reste bloque', () => {
    // Releve sur la planche du lot 3 : un coup qui fait changer Rhino de stade
    // en pleine attaque, l'activation n'est jamais close, l'etape suivante
    // (le stade) arrive derriere. Sans bouton, plus rien ne bouge.
    const { props } = monter({ etapes: [annonce, { ...attaqueResolue, cle: 'stade:9', titre: 'stade' }], index: 0 })
    fireEvent.click(screen.getByRole('button', { name: 'Suivant (espace)' }))
    expect(props.avancer).toHaveBeenCalledTimes(1)
  })

  it('« La suite arrive… » pendant l attente, bouton toujours la', () => {
    monter({ enAttente: true })
    expect(screen.getByText('La suite arrive…')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Suivant (espace)' })).toBeInTheDocument()
  })

  it('le filet annonce ses dernieres secondes', () => {
    monter({ secondesFilet: 9 })
    expect(screen.getByText('La phase reprend dans 9 s')).toBeInTheDocument()
  })
})

describe('une etape, une page (revirement du 05/10 : le carre grandit, rien ne se pagine)', () => {
  const cinqEffets: EtapeDeroule = {
    cle: 'revelation:p',
    temps: 'revelation',
    titre: 'revelation',
    regle: '',
    carteId: 88,
    cibleNom: 'Explosion',
    effets: [1, 2, 3, 4, 5].map((n) => ({ genre: 'degats' as const, cible: `Cible ${n}`, cible_id: 100 + n, montant: 1 })),
    boosts: [],
  }

  it('cinq effets : les cinq lignes d un coup, aucun numero de page, « Suivant » avance', () => {
    const avancer = vi.fn()
    monter({ etapes: [cinqEffets], index: 0, avancer })
    expect(document.querySelectorAll('.deroule-revelee .deroule-lignes li')).toHaveLength(5)
    expect(document.querySelector('.deroule-page')).toBeNull()
    const bouton = screen.getByRole('button', { name: 'Suivant (espace)' })
    expect(bouton.hasAttribute('data-page-suivante')).toBe(false)
    fireEvent.click(bouton)
    expect(avancer).toHaveBeenCalledTimes(1)
  })

  it('une seule page : aucun numero de page', () => {
    monter()
    expect(document.querySelector('.deroule-page')).toBeNull()
  })

  it('le corps change d identite avec l etape', () => {
    const { rerender, props } = monter()
    const avant = corps()
    rerender(<CartouchePhase {...props} etape={attaqueResolue} index={1} />)
    expect(corps()).not.toBe(avant)
  })
})

describe('pendant une question du moteur (avant le sous-cadre du lot 4)', () => {
  it('sans question rendue : rangee grisee, aucun bouton, la fenetre dite sur une annonce', () => {
    monter({ etapes: [annonce], index: 0, questionAuJoueur: true })
    expect(document.querySelector('.deroule-rangee.est-grisee')).not.toBeNull()
    expect(screen.getByText('tu peux défendre ou répondre')).toBeInTheDocument()
    expect(screen.queryByRole('button')).toBeNull()
    expect(screen.queryByText('La suite arrive…')).toBeNull()
  })

  it('sans question rendue, hors annonce : « Le moteur attend ta réponse »', () => {
    monter({ index: 1, questionAuJoueur: true, enAttente: true })
    expect(screen.getByText('Le moteur attend ta réponse')).toBeInTheDocument()
    expect(screen.queryByText('La suite arrive…')).toBeNull()
    expect(screen.queryByRole('button')).toBeNull()
  })

  it('la question rendue par le plateau se loge dans un sous-cadre provisoire', () => {
    monter({ etapes: [annonce], index: 0, questionAuJoueur: true, question: <button type="button">Passer</button> })
    const provisoire = document.querySelector('.deroule-sous-cadre.est-provisoire')
    expect(provisoire).not.toBeNull()
    expect(provisoire?.querySelector('button')?.textContent).toBe('Passer')
    expect(document.querySelector('.deroule-rangee.est-grisee')).not.toBeNull()
    expect(screen.queryByRole('button', { name: /Suivant/ })).toBeNull()
  })

  it('une question avant toute etape s affiche quand meme', () => {
    monter({ etapes: [], index: 0, etape: undefined, questionAuJoueur: true, question: <button type="button">Passer</button> })
    expect(section()).not.toBeNull()
    expect(document.querySelector('.deroule-sous-cadre.est-provisoire')).not.toBeNull()
  })
})

describe('la table reste visible et jouable (revirement du 05/10)', () => {
  it('le cartouche ne pose jamais de classe sur le body : main, barre et fin de tour restent a l ecran', () => {
    const { unmount } = monter()
    expect(document.body.classList.contains('cartouche-scene')).toBe(false)
    unmount()
    expect(document.body.classList.contains('cartouche-scene')).toBe(false)
  })

  it('rien a l ecran quand le cartouche ne rend rien', () => {
    const { container } = monter({ etapes: [], index: 0, etape: undefined })
    expect(container).toBeEmptyDOMElement()
  })

  it('efface (phase rendue, partie finie) : rien, meme avec une question', () => {
    const { container } = monter({ efface: true, questionAuJoueur: true, question: <button type="button">Passer</button> })
    expect(container).toBeEmptyDOMElement()
  })
})

// ------------------------------------------------------------------ LOT 4 --
// Les questions du moteur DANS le cartouche (D4 a D8, D18, D28, D29, D37) :
// la defense et le choix d'une carte revelee dans la rangee, tout le reste
// dans le sous-cadre, par-dessus la rangee grisee. Plus aucun panneau a cote.

const carteMonde = (id: number, name: string, extra: Partial<WorldCard> = {}): WorldCard => ({
  id,
  is_ready: true,
  is_face_up: true,
  visible_for_players: [],
  bind_object_id: 0,
  name,
  info: {},
  traits: {},
  buffs: {},
  card_id: `c${id}`,
  pic_id: `c${id}`,
  down_card_ids: [],
  card_type: 'Hero',
  cost: 0,
  resources: [],
  ...extra,
})

const VEUVE = 41
const PANTHERE = 13
const BACKFLIP = 90
const CARTES_MONDE = new Map<number, WorldCard>([
  [RHINO, carteMonde(RHINO, 'Rhino', { card_type: 'Villain', info: { attack: 2 } })],
  [SPIDER, carteMonde(SPIDER, 'Spider-Man', { info: { defense: 3 } })],
  [VEUVE, carteMonde(VEUVE, 'Black Widow', { card_type: 'Ally', info: { defense: 1 } })],
  [PANTHERE, carteMonde(PANTHERE, 'Black Panther', { info: { defense: 2 } })],
  [BACKFLIP, carteMonde(BACKFLIP, 'Backflip', { card_type: 'Event' })],
])

const optionMoteur = (id: number, name: string, bind_id: number, extra: Partial<Option> = {}): Option => ({
  id,
  name,
  bind_id,
  bind_player_id: 0,
  all_legal_targets: [],
  target_num_range: [0, 0],
  target_payment: {},
  select_rule: '',
  target_must_include_traits: [],
  failure_reason: '',
  is_search: false,
  ...extra,
})

const demandeMoteur = (options: Option[], extra: Partial<Demande> = {}): Demande => ({
  options,
  refus: [],
  prompt_text: '',
  event_name: 'WhenUnitBeingAttack',
  show_cancel: true,
  ability_type: 'Interrupt',
  ...extra,
})

const interactionMoteur = (options: Option[], extra: Partial<Interaction> = {}): Interaction => ({
  cibles: [],
  ressources: [],
  options,
  defocaliser: vi.fn(),
  focaliserCarte: vi.fn(),
  focaliserCible: vi.fn(),
  cartes: new Map(),
  ciblesHorsTable: [],
  raison: '',
  prete: false,
  coutAffiche: '',
  surpaiementRecompense: false,
  ciblesRestantes: 0,
  assistant: {
    etape: 'action',
    titre: '',
    cibleMinimum: 0,
    cibleMaximum: 0,
    cibleNombre: 0,
    ciblePossibles: 0,
    cibleRepetable: false,
    coutPaye: 0,
    coutSlots: [],
    coutRegles: [],
  },
  choisirOption: vi.fn(),
  abandonnerOption: vi.fn(),
  valider: vi.fn(),
  annuler: vi.fn(),
  paiementAutoChoix: 'pas-demande',
  basculerPaiementAuto: vi.fn(),
  ...extra,
})

const questionMoteur = (d: Demande, extra: Partial<QuestionDuMoteur> = {}): QuestionDuMoteur => ({
  demande: d,
  interaction: interactionMoteur(d.options),
  cartesParId: CARTES_MONDE,
  choisirOption: vi.fn(),
  survolerOption: vi.fn(),
  nomPorteur: (id) => CARTES_MONDE.get(id)?.name,
  texteCapacite: () => undefined,
  estEnMain: (id) => id === BACKFLIP,
  carteScene: (id) => scan(id),
  ...extra,
})

const defenseSM = optionMoteur(1, 'Defense', SPIDER, { all_legal_targets: [RHINO], target_num_range: [1, 1] })
const defenseBW = optionMoteur(2, 'Defense', VEUVE, { all_legal_targets: [RHINO], target_num_range: [1, 1] })
const sensAraignee = optionMoteur(3, 'Spider-Sense', SPIDER)
const jouerBackflip = optionMoteur(4, 'Play', BACKFLIP)

const choixDuCartouche = () => [...document.querySelectorAll<HTMLButtonElement>('button.deroule-vignette[data-choix]')]
const refusDuCartouche = () => document.querySelector<HTMLButtonElement>('button.bh-bouton[data-refus]')

describe('etat 1 : la question de defense, dans la rangee (D7, D37)', () => {
  function etat1() {
    const q = questionMoteur(demandeMoteur([defenseSM, defenseBW, sensAraignee]), { ligneSansDefense: 'ATQ 2 + 1 carte boost' })
    monter({ etapes: [annonce], index: 0, questionAuJoueur: true, questionDuMoteur: q })
    return q
  }

  it('l attaquant a gauche, les defenseurs puis la capacite en vignettes numerotees', () => {
    etat1()
    const rangee = document.querySelector('.deroule-rangee')
    expect(rangee?.classList.contains('est-grisee')).toBe(false)
    expect(rangee?.querySelector('.deroule-vignette')?.textContent).toContain('ATQ 2 + 1 carte boost')
    expect(choixDuCartouche().map((b) => [b.dataset.choix, b.getAttribute('aria-label')])).toEqual([
      ['1', 'Défendre avec Spider-Man (DÉF 3)'],
      ['2', 'Défendre avec Black Widow (DÉF 1)'],
      ['3', 'Spider-Sense'],
    ])
    expect(choixDuCartouche()[0]?.textContent).toContain('(1)')
    expect(document.querySelector('.deroule-sous-cadre')).toBeNull()
  })

  it('« Ne pas défendre (ATQ 2 + 1 carte boost) » a droite, aucun « Suivant »', () => {
    const q = etat1()
    expect(refusDuCartouche()?.textContent).toBe('Ne pas défendre (ATQ 2 + 1 carte boost)')
    expect(screen.queryByRole('button', { name: /Suivant/ })).toBeNull()
    fireEvent.click(refusDuCartouche()!)
    expect(q.interaction.annuler).toHaveBeenCalledTimes(1)
  })

  it('un clic sur Spider-Man defend avec lui', () => {
    const q = etat1()
    fireEvent.click(choixDuCartouche()[0]!)
    expect(q.choisirOption).toHaveBeenCalledWith(defenseSM)
  })
})

describe('essai : le choix du defenseur en boutons de meme taille (10/10/2026)', () => {
  function etat1Essai() {
    const q = questionMoteur(demandeMoteur([defenseSM, defenseBW, sensAraignee]), { ligneSansDefense: 'ATQ 2 + 1 carte boost' })
    monter({ etapes: [annonce], index: 0, questionAuJoueur: true, questionDuMoteur: q, essai: true })
    return q
  }

  it('un bouton vert « Défendre avec X » par defenseur, son picto DEF en tete, puis « Ne pas défendre »', () => {
    etat1Essai()
    const rangee = document.querySelector('.essai-choix-defense')!
    const boutons = [...rangee.querySelectorAll<HTMLButtonElement>('button.essai-choix')]
    expect(boutons.map((b) => [b.classList.contains('est-defendre'), b.textContent])).toEqual([
      [true, '3DÉFDéfendre avec Spider-Man'],
      [true, '1DÉFDéfendre avec Black Widow'],
      [false, 'Ne pas défendre (ATQ 2 + 1 carte boost)'],
    ])
    expect(boutons[0]?.querySelector('.essai-stat.est-def')?.getAttribute('aria-label')).toBe('DÉF 3')
    // Plus de petit refus a part : un seul « Ne pas défendre », dans la rangee.
    expect(refusDuCartouche()).toBeNull()
  })

  it('les deux boutons agissent : defendre avec Spider-Man, ou ne pas defendre', () => {
    const q = etat1Essai()
    const boutons = [...document.querySelectorAll<HTMLButtonElement>('.essai-choix-defense button')]
    fireEvent.click(boutons[0]!)
    expect(q.choisirOption).toHaveBeenCalledWith(defenseSM)
    fireEvent.click(boutons[2]!)
    expect(q.interaction.annuler).toHaveBeenCalledTimes(1)
  })
})

describe('etat 2 : pendant la defense (D8)', () => {
  const annonceEnrichie: EtapeDeroule = { ...annonce, defenseurId: SPIDER, defenseurNom: 'Spider-Man', defense: 3 }

  it('defenseur connu : « défend · DÉF 3 », les cartes jouables a la suite, « Continuer sans rien jouer »', () => {
    const q = questionMoteur(demandeMoteur([jouerBackflip], { event_name: 'WhenDamage' }))
    monter({ etapes: [annonceEnrichie], index: 0, questionAuJoueur: true, questionDuMoteur: q })
    expect(screen.getByText('défend · DÉF 3')).toBeInTheDocument()
    expect(document.querySelector('.deroule-rangee')?.classList.contains('est-grisee')).toBe(false)
    expect(choixDuCartouche().map((b) => b.getAttribute('aria-label'))).toEqual(['Backflip'])
    expect(refusDuCartouche()?.textContent).toBe('Continuer sans rien jouer')
    expect(document.querySelector('.deroule-sous-cadre')).toBeNull()
    fireEvent.click(choixDuCartouche()[0]!)
    expect(q.choisirOption).toHaveBeenCalledWith(jouerBackflip)
  })

  it('sans fait boosts (defenseur inconnu) : le sous-cadre par-dessus la rangee grisee et cachee', () => {
    const q = questionMoteur(demandeMoteur([jouerBackflip], { event_name: 'WhenDamage' }))
    monter({ etapes: [annonce], index: 0, questionAuJoueur: true, questionDuMoteur: q })
    const rangee = document.querySelector('.deroule-rangee')
    expect(rangee?.classList.contains('est-grisee')).toBe(true)
    expect(rangee?.getAttribute('aria-hidden')).toBe('true')
    expect(document.querySelector('.deroule-sous-cadre.est-reponses')).not.toBeNull()
    expect(refusDuCartouche()?.textContent).toBe('Ne pas jouer Backflip')
  })

  it('le repli provisoire n est jamais rendu quand la question structuree est la', () => {
    const q = questionMoteur(demandeMoteur([jouerBackflip], { event_name: 'WhenDamage' }))
    monter({
      etapes: [annonce],
      index: 0,
      questionAuJoueur: true,
      questionDuMoteur: q,
      question: <button type="button">Passer</button>,
    })
    expect(document.querySelector('.deroule-sous-cadre.est-provisoire')).toBeNull()
    expect(screen.queryByRole('button', { name: 'Passer' })).toBeNull()
  })
})

describe('une question structuree avant toute etape (12/09/2026)', () => {
  it('le sous-cadre s affiche quand meme, avec son refus', () => {
    const q = questionMoteur(demandeMoteur([jouerBackflip], { event_name: 'WhenSchemeWouldPlaceThreat' }))
    monter({ etapes: [], index: 0, etape: undefined, questionAuJoueur: true, questionDuMoteur: q })
    expect(section()).not.toBeNull()
    expect(document.querySelector('.deroule-sous-cadre.est-reponses')).not.toBeNull()
    expect(refusDuCartouche()?.textContent).toBe('Ne pas jouer Backflip')
    expect(screen.queryByRole('button', { name: /Suivant/ })).toBeNull()
  })

  it('une defense avant toute etape : l attaquant dit l attaque dans le titre court', () => {
    const q = questionMoteur(demandeMoteur([defenseSM]))
    monter({ etapes: [], index: 0, etape: undefined, questionAuJoueur: true, questionDuMoteur: q })
    expect(document.querySelector('.deroule-titre-court')?.textContent).toBe('Attaque de Rhino')
    expect(choixDuCartouche()).toHaveLength(1)
  })
})

describe('etat 10 : la carte revelee pose sa question, a sa droite (D18)', () => {
  const chantage: EtapeDeroule = {
    cle: 'revelation:10',
    temps: 'revelation',
    titre: 'revelation',
    regle: '',
    carteId: 88,
    cibleNom: 'Chantage',
    boosts: [],
  }

  it('les choix a droite de la carte en grand, pas de sous-cadre', () => {
    const subir = optionMoteur(7, 'Take_2_damage', 0)
    const defausser = optionMoteur(8, 'Discard_2_cards', 0)
    const q = questionMoteur(
      demandeMoteur([subir, defausser], {
        event_name: 'WhenPlayerChooseAbility',
        ability_type: 'Normal',
        prompt_text: 'Chantage : choisis',
        show_cancel: false,
      })
    )
    monter({ etapes: [chantage], index: 0, questionAuJoueur: true, questionDuMoteur: q, tempsQuestion: 'revelation' })
    expect(document.querySelector('.deroule-revelee .deroule-carte-grande')).not.toBeNull()
    const choix = [...document.querySelectorAll('.deroule-revelee .deroule-question-carte [data-choix]')]
    expect(choix.map((b) => (b as HTMLElement).dataset.choix)).toEqual(['1', '2'])
    expect(screen.getByText('Chantage : choisis')).toBeInTheDocument()
    expect(document.querySelector('.deroule-sous-cadre')).toBeNull()
    fireEvent.click(choix[1] as HTMLElement)
    expect(q.choisirOption).toHaveBeenCalledWith(defausser)
  })
})

describe('etat 14 : un autre joueur choisit (D28, lecture seule)', () => {
  it('la rangee grisee, ses defenseurs sans bouton, « Black Panther choisit… » qui pulse', () => {
    monter({
      etapes: [{ ...annonce, cibleId: PANTHERE, cibleNom: 'Black Panther' }],
      index: 0,
      attendUnAutreJoueur: true,
      nomJoueurAttendu: 'Black Panther',
      questionDUnAutre: { options: [{ id: 1, bindId: PANTHERE, nom: 'Black Panther' }, { id: 2, bindId: 0, nom: 'Pass' }] },
    })
    const rangee = document.querySelector('.deroule-rangee.est-attente')
    expect(rangee).not.toBeNull()
    expect(rangee?.querySelector('.deroule-pulse')?.textContent).toBe('Black Panther choisit…')
    expect(rangee?.querySelectorAll('.deroule-vignette.est-grisee').length).toBeGreaterThanOrEqual(1)
    expect(document.querySelectorAll('[data-choix], [data-refus]')).toHaveLength(0)
    expect(screen.queryAllByRole('button')).toHaveLength(0)
  })

  // Multi, 11/10/2026 : au tout debut de la phase, le moteur interroge l'hote
  // AVANT la premiere etape. Les autres joueurs ne voyaient alors RIEN : le
  // cartouche ne s'affichait sans etape que pour une question posee ici.
  it('avant toute etape, un autre joueur interroge : « Black Panther choisit… » plutot que rien', () => {
    monter({
      etapes: [],
      index: 0,
      etape: undefined,
      ...{
        attendUnAutreJoueur: true,
        nomJoueurAttendu: 'Black Panther',
        questionDUnAutre: { options: [{ id: 1, bindId: PANTHERE, nom: 'Black Panther' }] },
      },
    })
    expect(section()).not.toBeNull()
    expect(document.querySelector('.deroule-pulse')?.textContent).toBe('Black Panther choisit…')
    expect(screen.queryAllByRole('button', { name: /Suivant/ })).toHaveLength(0)
  })

  it('sans nom connu : « Un autre joueur choisit… »', () => {
    monter({ etapes: [annonce], index: 0, attendUnAutreJoueur: true, questionDUnAutre: { options: [] } })
    expect(document.querySelector('.deroule-pulse')?.textContent).toBe('Un autre joueur choisit…')
  })

  const attenteDePanthere = {
    attendUnAutreJoueur: true,
    nomJoueurAttendu: 'Black Panther',
    questionDUnAutre: { options: [{ id: 1, bindId: PANTHERE, nom: 'Black Panther' }] },
  }

  it('sur la derniere etape connue, meme resolue : aucun « Suivant » tant qu il choisit', () => {
    monter({ etapes: [attaqueResolue], index: 0, ...attenteDePanthere })
    expect(document.querySelector('.deroule-rangee.est-attente')).not.toBeNull()
    expect(screen.queryByRole('button', { name: /Suivant/ })).toBeNull()
  })

  // Verification adverse du lot 4 : en retard sur la table, l'etape lue est
  // une etape PASSEE. Lui coller les cartes de la question d'un autre siege
  // montrait « Rhino → Spider-Man, 1 dégât » suivi de Black Panther grise et
  // « Black Panther choisit… », comme si cette etape-la attendait sa reponse.
  it('en retard sur la table : l etape lue reste la sienne, « X choisit… » passe au pied, « Suivant » reste', () => {
    monter({
      etapes: [attaqueResolue, { ...annonce, cibleId: PANTHERE, cibleNom: 'Black Panther' }],
      index: 0,
      ...attenteDePanthere,
    })
    expect(document.querySelector('.deroule-rangee.est-attente')).toBeNull()
    expect(document.querySelector(`.deroule-rangee [data-card-id="${PANTHERE}"]`)).toBeNull()
    expect(document.querySelector('.deroule-mentions .deroule-pulse')?.textContent).toBe('Black Panther choisit…')
    expect(screen.getByRole('button', { name: /Suivant/ })).toBeInTheDocument()
  })
})

describe('la loupe devant le carre (D29, revue le 05/10 : placement normal, a droite)', () => {
  it('le survol d une vignette ouvre UN apercu devant le carre ; ailleurs, rien', () => {
    monter({ index: 1 })
    const carte = document.querySelector('.deroule-rangee .deroule-vignette [data-card-id]')
    expect(carte).not.toBeNull()
    fireEvent.mouseOver(carte as Element)
    expect(document.querySelectorAll('.carte-apercu')).toHaveLength(1)
    expect(document.querySelector('.carte-apercu')?.classList.contains('au-dessus-du-deroule')).toBe(true)
    expect(document.querySelector('.carte-apercu')?.classList.contains('au-dessus-du-cartouche')).toBe(false)
    fireEvent.mouseOver(document.querySelector('.deroule-titre-court') as Element)
    expect(document.querySelector('.carte-apercu')).toBeNull()
  })

  it('la carte qui quitte le cartouche emporte son apercu', () => {
    const { rerender, props } = monter({ index: 1 })
    fireEvent.mouseOver(document.querySelector(`.deroule-rangee [data-card-id="${SPIDER}"]`) as Element)
    expect(document.querySelector('.carte-apercu')).not.toBeNull()
    rerender(<CartouchePhase {...props} etape={menace} index={0} />)
    expect(document.querySelector('.carte-apercu')).toBeNull()
  })

  it('le survol d une option la signale a la table (pulse des cibles), et le quitter l eteint', () => {
    const q = questionMoteur(demandeMoteur([defenseSM, defenseBW]))
    monter({ etapes: [annonce], index: 0, questionAuJoueur: true, questionDuMoteur: q })
    fireEvent.mouseOver(choixDuCartouche()[1]!)
    expect(q.survolerOption).toHaveBeenLastCalledWith(defenseBW)
    fireEvent.mouseLeave(section()!)
    expect(q.survolerOption).toHaveBeenLastCalledWith(undefined)
  })
})

// ------------------------------------------------------------------ LOT 5 --
// LA RELECTURE (D22, D23, D38) et LE HORS PHASE (D26). Meme gabarit, meme
// hauteur : la relecture remplace la rangee par celle de l'etape relue, sous
// un bandeau « Relecture » ; le hors phase remplace les pastilles par le
// bandeau « Pendant ton tour ».

const sbireResolu = (cle: string, auteur: string, montant: number): EtapeDeroule => ({
  ...attaqueResolue,
  cle,
  temps: 'sbires',
  carteId: 60,
  auteurNom: auteur,
  base: montant,
  montant,
  boosts: [],
})
const revelationStampede: EtapeDeroule = {
  cle: 'revelation:20',
  temps: 'revelation',
  titre: 'revelation',
  regle: '',
  carteId: 88,
  cibleNom: 'Stampede',
  typeCarte: 'Treachery',
  boosts: [],
}
const PHASE_RELUE: EtapeDeroule[] = [
  menace,
  attaqueResolue,
  sbireResolu('activation:s1', 'Drone', 1),
  sbireResolu('activation:s2', 'Hydra', 2),
  revelationStampede,
]
const pastille = (rang: number) => document.querySelectorAll<HTMLElement>('li.deroule-pastille')[rang]

describe('la relecture d une pastille passee (D22, D23)', () => {
  it('une pastille passee se clique ; la courante et celles a venir, non', () => {
    const setRelecture = vi.fn()
    monter({ etapes: PHASE_RELUE, index: 2, setRelecture })
    expect(pastille(0).querySelector('button')).not.toBeNull()
    expect(pastille(1).querySelector('button')).not.toBeNull()
    expect(pastille(2).querySelector('button')).toBeNull()
    expect(pastille(3).querySelector('button')).toBeNull()
    expect(pastille(4).querySelector('button')).toBeNull()
    fireEvent.click(pastille(1).querySelector('button') as HTMLElement)
    expect(setRelecture).toHaveBeenCalledWith({ temps: 'mechant' })
  })

  it('relue : bandeau « Relecture », la rangee de l etape relue, « Revenir à 2B », aucun « Suivant »', () => {
    const setRelecture = vi.fn()
    const { props } = monter({ etapes: PHASE_RELUE, index: 3, relecture: { temps: 'mechant' }, setRelecture })
    expect(section()?.classList.contains('est-relecture')).toBe(true)
    expect(document.querySelector('.deroule-bandeau')?.textContent).toBe('Relecture')
    expect(corps()?.getAttribute('aria-label')).toBe('Rhino attaque Spider-Man')
    expect(pastille(1).className).toContain('est-relu')
    // L'onglet de l'etape en cours reste marque « en cours » (D23).
    expect(pastille(2).className).toContain('est-courant')
    expect(screen.queryByRole('button', { name: /Suivant \(espace\)/ })).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Revenir à 2B' }))
    expect(setRelecture).toHaveBeenCalledWith(undefined)
    expect(props.avancer).not.toHaveBeenCalled()
  })

  it('plusieurs coups dans la pastille relue : « 1 / 2 », puis « Suivant » montre le second', () => {
    monter({ etapes: PHASE_RELUE, index: 4, relecture: { temps: 'sbires' }, setRelecture: vi.fn() })
    expect(document.querySelector('.deroule-page')?.textContent).toBe('1 / 2')
    expect(corps()?.getAttribute('aria-label')).toBe('Drone attaque Spider-Man')
    fireEvent.click(screen.getByRole('button', { name: 'Suivant' }))
    expect(document.querySelector('.deroule-page')?.textContent).toBe('2 / 2')
    expect(corps()?.getAttribute('aria-label')).toBe('Hydra attaque Spider-Man')
    expect(screen.queryByRole('button', { name: 'Suivant' })).toBeNull()
    expect(screen.getByRole('button', { name: 'Revenir à 3' })).toBeInTheDocument()
  })

  it('pendant une question, la relecture cede la place a l etape en cours, et rien ne se relit', () => {
    monter({ etapes: PHASE_RELUE, index: 3, relecture: { temps: 'mechant' }, setRelecture: vi.fn(), questionAuJoueur: true })
    expect(section()?.classList.contains('est-relecture')).toBe(false)
    expect(document.querySelectorAll('li.deroule-pastille button')).toHaveLength(0)
  })

  it('entrer en relecture remonte le corps : le glissement d entree rejoue (D35)', () => {
    const { rerender, props } = monter({ etapes: PHASE_RELUE, index: 3, setRelecture: vi.fn() })
    const avant = corps()
    rerender(<CartouchePhase {...props} relecture={{ temps: 'mechant' }} />)
    expect(corps()).not.toBe(avant)
  })
})

describe('la relecture depuis le journal (D38)', () => {
  const PHASE_FINIE: EtapeDeroule[] = [
    menace,
    attaqueResolue,
    { cle: 'distribution:1', temps: 'distribution', titre: 'distribution', regle: '', auteurNom: 'Spider-Man', montant: 1, boosts: [] },
    revelationStampede,
  ]

  it('bandeau « Relecture », cinq pastilles cliquables, la premiere etape, et « Fermer »', () => {
    const onFermer = vi.fn()
    render(<RelectureJournal etapes={PHASE_FINIE} carteScene={scan} onFermer={onFermer} />)
    expect(section()?.classList.contains('est-scene')).toBe(true)
    expect(section()?.classList.contains('est-relecture')).toBe(true)
    expect(document.querySelector('.deroule-bandeau')?.textContent).toBe('Relecture')
    expect(document.querySelectorAll('li.deroule-pastille button')).toHaveLength(5)
    expect(document.querySelector('.deroule-titre-court')?.textContent).toBe('Menace')
    fireEvent.click(pastille(1).querySelector('button') as HTMLElement)
    expect(corps()?.getAttribute('aria-label')).toBe('Rhino attaque Spider-Man')
    expect(screen.queryByRole('button', { name: /Suivant \(espace\)|Terminer/ })).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Fermer' }))
    expect(onFermer).toHaveBeenCalledTimes(1)
  })

  it('la distribution n est pas une etape : « 1 carte distribuée » en tete de la quatrieme pastille', () => {
    render(<RelectureJournal etapes={PHASE_FINIE} carteScene={scan} onFermer={() => {}} />)
    expect(pastille(3).querySelector('.deroule-pastille-resume')?.textContent).toMatch(/^1 carte distribuée/)
    fireEvent.click(pastille(3).querySelector('button') as HTMLElement)
    expect(document.querySelector('.deroule-revelee .deroule-carte-grande')).not.toBeNull()
  })

  it('le bilan se relit, en trois colonnes', () => {
    render(<RelectureJournal etapes={PHASE_FINIE} carteScene={scan} pvMaxParNom={new Map([['Spider-Man', 10]])} onFermer={() => {}} />)
    fireEvent.click(pastille(4).querySelector('button') as HTMLElement)
    expect(document.querySelectorAll('.deroule-bilan .deroule-colonne')).toHaveLength(3)
  })

  it('ne pose aucune classe sur le body', () => {
    render(<RelectureJournal etapes={PHASE_FINIE} carteScene={scan} onFermer={() => {}} />)
    expect(section()).not.toBeNull()
    expect(document.body.classList.contains('cartouche-scene')).toBe(false)
  })
})

describe('pendant ton tour (D26) : le cartouche hors phase', () => {
  const coupHP = (cle: string, extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
    ...attaqueResolue,
    cle,
    horsPhase: true,
    ...extra,
  })
  const annonceHP: EtapeDeroule = { ...annonce, cle: 'activation:40', horsPhase: true }
  const horsPhase = (props: Partial<Parameters<typeof CartoucheHorsPhase>[0]> = {}) => (
    <CartoucheHorsPhase coups={[]} questionAuJoueur={false} carteScene={scan} pvMaxParNom={new Map([['Spider-Man', 10]])} {...props} />
  )

  it('un coup pendant le tour : bandeau « Pendant ton tour », pas de pastilles, sa rangee ; « Continuer » le ferme', () => {
    const { rerender } = render(horsPhase())
    expect(section()).toBeNull()
    rerender(horsPhase({ coups: [coupHP('activation:30')] }))
    expect(section()?.classList.contains('est-scene')).toBe(true)
    expect(section()?.classList.contains('est-hors-phase')).toBe(true)
    expect(document.querySelector('.deroule-bandeau')?.textContent).toBe('Pendant ton tour')
    expect(document.querySelectorAll('.deroule-pastille')).toHaveLength(0)
    expect(corps()?.getAttribute('aria-label')).toBe('Rhino attaque Spider-Man')
    expect(document.querySelector('.deroule-rangee .deroule-resultat-texte')).not.toBeNull()
    expect(document.body.classList.contains('cartouche-scene')).toBe(false)
    fireEvent.click(screen.getByRole('button', { name: 'Continuer' }))
    expect(section()).toBeNull()
  })

  it('les coups deja la au chargement ne se montrent pas (rechargement de page)', () => {
    render(horsPhase({ coups: [coupHP('activation:30')] }))
    expect(section()).toBeNull()
  })

  it('un coup vu ne revient pas, le suivant se montre', () => {
    const { rerender } = render(horsPhase())
    rerender(horsPhase({ coups: [coupHP('activation:30')] }))
    fireEvent.click(screen.getByRole('button', { name: 'Continuer' }))
    rerender(horsPhase({ coups: [coupHP('activation:30')] }))
    expect(section()).toBeNull()
    rerender(horsPhase({ coups: [coupHP('activation:30'), coupHP('activation:31', { auteurNom: 'Hydra' })] }))
    expect(corps()?.getAttribute('aria-label')).toBe('Hydra attaque Spider-Man')
  })

  it('une annonce sans question attend sa resolution ; avec la question de defense, la rangee de defense', () => {
    const { rerender } = render(horsPhase())
    rerender(horsPhase({ coups: [annonceHP] }))
    expect(section()).toBeNull()
    const q = questionMoteur(demandeMoteur([defenseSM, defenseBW]), { ligneSansDefense: 'ATQ 2' })
    rerender(horsPhase({ coups: [annonceHP], questionAuJoueur: true, questionDuMoteur: q }))
    expect(document.querySelector('.deroule-bandeau')?.textContent).toBe('Pendant ton tour')
    expect(choixDuCartouche()).toHaveLength(2)
    expect(refusDuCartouche()?.textContent).toMatch(/^Ne pas défendre/)
    expect(screen.queryByRole('button', { name: 'Continuer' })).toBeNull()
    fireEvent.click(choixDuCartouche()[0]!)
    expect(q.choisirOption).toHaveBeenCalledWith(defenseSM)
  })

  it('une defense deja posee au chargement se montre quand meme (sinon, plus aucun bouton)', () => {
    const q = questionMoteur(demandeMoteur([defenseSM]))
    render(horsPhase({ coups: [annonceHP], questionAuJoueur: true, questionDuMoteur: q }))
    expect(choixDuCartouche()).toHaveLength(1)
  })

  it('le coup resolu apres la defense se montre, meme s il etait annonce au chargement', () => {
    const q = questionMoteur(demandeMoteur([defenseSM]))
    const { rerender } = render(horsPhase({ coups: [annonceHP], questionAuJoueur: true, questionDuMoteur: q }))
    rerender(horsPhase({ coups: [{ ...annonceHP, etat: 'resolu', base: 2, montant: 2, restant: 8 }] }))
    expect(document.querySelector('.deroule-rangee .deroule-resultat-texte')).not.toBeNull()
    expect(screen.getByRole('button', { name: 'Continuer' })).toBeInTheDocument()
  })

  it('une carte revelee pendant le tour se montre en grand', () => {
    const { rerender } = render(horsPhase())
    rerender(horsPhase({ coups: [{ ...revelationStampede, horsPhase: true }] }))
    expect(document.querySelector('.deroule-revelee .deroule-carte-grande')).not.toBeNull()
    expect(screen.getByRole('button', { name: 'Continuer' })).toBeInTheDocument()
  })

  // Planche du lot 5 (etat 15c) : Advance revelee pendant le tour fait
  // manigancer Rhino. La manigance (temps ②) se range AVANT la revelation
  // (temps ④) et prenait sa place a l'ecran, sans un clic.
  it('le coup a l ecran ne change pas sous les yeux quand un autre arrive', () => {
    const revelee = { ...revelationStampede, horsPhase: true }
    const manigance = coupHP('activation:50', { titre: 'manigance', cibleNom: 'The Break-In!', cibleId: MANIGANCE })
    const { rerender } = render(horsPhase())
    rerender(horsPhase({ coups: [revelee] }))
    rerender(horsPhase({ coups: [manigance, revelee] }))
    expect(document.querySelector('.deroule-revelee .deroule-carte-grande')).not.toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Continuer' }))
    expect(document.querySelector('.deroule-titre-court')?.textContent).toBe('Manigance')
    fireEvent.click(screen.getByRole('button', { name: 'Continuer' }))
    expect(section()).toBeNull()
  })

  it('dit au plateau quand il est a l ecran (la narration du centre se tait)', () => {
    const onAffiche = vi.fn()
    const { rerender } = render(horsPhase({ onAffiche }))
    expect(onAffiche).toHaveBeenLastCalledWith(false)
    rerender(horsPhase({ coups: [coupHP('activation:30')], onAffiche }))
    expect(onAffiche).toHaveBeenLastCalledWith(true)
    fireEvent.click(screen.getByRole('button', { name: 'Continuer' }))
    expect(onAffiche).toHaveBeenLastCalledWith(false)
  })

  it('masque (relecture du journal ouverte) : rien a l ecran, et le coup attend', () => {
    const { rerender } = render(horsPhase({ masque: true }))
    rerender(horsPhase({ coups: [coupHP('activation:30')], masque: true }))
    expect(section()).toBeNull()
    rerender(horsPhase({ coups: [coupHP('activation:30')] }))
    expect(corps()?.getAttribute('aria-label')).toBe('Rhino attaque Spider-Man')
  })
})

describe('ESSAI « Nouvelle phase du méchant » (10/10/2026)', () => {
  const attaqueDeuxBoosts: EtapeDeroule = {
    ...attaqueResolue,
    cle: 'activation:9',
    base: 1,
    montant: 1,
    restant: 3,
    boosts: [
      { cle: 'b1', nom: 'Sonic Boom', cibleId: 91, apport: 0, etoile: true },
      { cle: 'b2', nom: 'Melter', cibleId: 92, apport: 0, etoile: true },
    ],
  }

  it('sans l’interrupteur, rien ne change : ni classe, ni compteur, ni « Réduire »', () => {
    monter({ etapes: [attaqueDeuxBoosts] })
    expect(section()?.classList.contains('est-essai')).toBe(false)
    expect(document.querySelector('.essai-outils')).toBeNull()
    expect(document.querySelector('.essai-calcul')).toBeNull()
  })

  it('le calcul se pose entre les cartes : opérateurs, chiffres, résultat en boîte', () => {
    monter({ etapes: [attaqueDeuxBoosts], essai: true, montrerBoostSuivant: vi.fn() })
    expect(section()?.classList.contains('est-essai')).toBe(true)
    const calcul = document.querySelector('.essai-calcul')
    expect(calcul).not.toBeNull()
    const operateurs = [...calcul!.querySelectorAll('.essai-operateur')].map((e) => e.textContent)
    expect(operateurs).toEqual(['+', '+'])
    // Sous l'acteur, le picto ATQ et sa valeur ; sous chaque boost, sa pastille « +0 BOOST ★ ».
    expect(calcul!.querySelector('.essai-stat.est-atq')?.getAttribute('aria-label')).toBe('ATQ 1')
    expect([...calcul!.querySelectorAll('.essai-stat.est-boost')].map((e) => e.getAttribute('aria-label'))).toEqual([
      '+0 BOOST ★',
      '+0 BOOST ★',
    ])
    // L'effet ★ de chaque boost se lit sous ses icones.
    expect(calcul!.querySelectorAll('.essai-etoile')).toHaveLength(2)
    expect(calcul!.querySelector('.essai-boite .deroule-resultat-texte')?.textContent).toBe('1 dégât subi')
    // Spider-Man à 3 PV sur 10 : critique, en couleur fixe.
    expect(calcul!.querySelector('.essai-boite.est-critique')).not.toBeNull()
  })

  it('les boosts se retournent au clic : « Continuer » montre le suivant sans valider l’étape', () => {
    const montrerBoostSuivant = vi.fn()
    const { props } = monter({ etapes: [attaqueDeuxBoosts], essai: true, boostsMontres: 1, montrerBoostSuivant })
    const bouton = document.querySelector<HTMLButtonElement>('button[data-boost-suivant]')
    expect(bouton?.textContent).toContain('Continuer')
    expect(screen.getByText('Boost 1 / 2 retourné')).toBeInTheDocument()
    fireEvent.click(bouton!)
    expect(montrerBoostSuivant).toHaveBeenCalledTimes(1)
    expect(props.avancer).not.toHaveBeenCalled()
  })

  it('tous les boosts retournés : « Continuer » valide l’étape', () => {
    const { props } = monter({ etapes: [attaqueDeuxBoosts], essai: true, boostsMontres: 2, montrerBoostSuivant: vi.fn() })
    expect(document.querySelector('button[data-boost-suivant]')).toBeNull()
    const bouton = document.querySelector<HTMLButtonElement>('button.deroule-suivant')
    expect(bouton?.textContent).toContain('Continuer')
    fireEvent.click(bouton!)
    expect(props.avancer).toHaveBeenCalledTimes(1)
  })

  it('« Réduire » replie le panneau en barre, un second clic le rouvre', () => {
    monter({ etapes: [attaqueDeuxBoosts], essai: true })
    const reduire = document.querySelector<HTMLButtonElement>('.essai-reduire')!
    fireEvent.click(reduire)
    expect(section()?.classList.contains('est-reduit')).toBe(true)
    fireEvent.click(reduire)
    expect(section()?.classList.contains('est-reduit')).toBe(false)
  })

  it('la chaîne du n°72 : tampon « ANNULÉE », la carte qui annule, et le compteur de cartes', () => {
    const coureur: EtapeDeroule = {
      cle: 'rev:1', temps: 'revelation', titre: 'revelation', regle: '', carteId: 65, cibleNom: 'Weapons Runner',
      boosts: [], suivieDUnRenfort: true,
    }
    const vengeance: EtapeDeroule = {
      cle: 'rev:2', temps: 'revelation', titre: 'revelation', regle: '', carteId: 66, cibleNom: "Klaw's Vengeance",
      boosts: [], parSurge: true, renfortDe: 'Weapons Runner', annuleePar: 'Stepford Cuckoos', annuleeParId: 32,
    }
    const boom: EtapeDeroule = {
      cle: 'rev:3', temps: 'revelation', titre: 'revelation', regle: '', carteId: 69, cibleNom: 'Sonic Boom',
      boosts: [], reveleePar: 'Stepford Cuckoos', reveleeParId: 32,
    }
    monter({ etapes: [coureur, vengeance, boom], index: 2, essai: true, cartesDistribuees: 1 })
    expect(document.querySelector('.essai-tampon')?.textContent).toBe('ANNULÉE')
    expect(document.querySelector('.essai-annuleur [data-card-id], .essai-annuleur .deroule-vignette')).not.toBeNull()
    expect(document.querySelector('.essai-compteur b')?.textContent).toBe('Carte 3 / 3')
    expect(document.querySelector('.essai-compteur small')?.textContent).toContain('Renfort (Weapons Runner)')
    expect(document.querySelector('.essai-compteur small')?.textContent).toContain('Stepford Cuckoos')
  })
})

describe('refonte du 12/10/2026, lot 1 : la boite de la colonne de gauche', () => {
  const pc = (largeurPc: boolean) => {
    window.matchMedia = ((requete: string) => ({
      matches: largeurPc && requete.includes('min-width: 768px'),
      media: requete,
      addEventListener() {},
      removeEventListener() {},
      addListener() {},
      removeListener() {},
      onchange: null,
      dispatchEvent: () => false,
    })) as unknown as typeof window.matchMedia
  }

  it("sans l'essai, rien ne change : ni colonne reservee, ni cadre, ni pastille", () => {
    pc(true)
    monter({ cadre: { genre: 'joueur', joueur: 0, couleurs: ['#e6be3c'], raye: false, siege: 1 } })
    expect(document.body.classList.contains('phase-essai-colonne')).toBe(false)
    expect(section()?.className).not.toMatch(/est-cadre/)
    expect(document.querySelector('.essai-pastille-joueur')).toBeNull()
  })

  it('avec l\'essai sur PC, la colonne de gauche est reservee tant que la boite est affichee', () => {
    pc(true)
    const { unmount } = monter({ essai: true })
    expect(document.body.classList.contains('phase-essai-colonne')).toBe(true)
    unmount()
    expect(document.body.classList.contains('phase-essai-colonne')).toBe(false)
  })

  it("monte mais efface (hors de la phase : mise en place, tour du joueur), la table n'est pas decalee", () => {
    pc(true)
    monter({ essai: true, efface: true })
    expect(document.body.classList.contains('phase-essai-colonne')).toBe(false)
  })

  it('au telephone, pas de colonne : la feuille basse', () => {
    pc(false)
    monter({ essai: true })
    expect(document.body.classList.contains('phase-essai-colonne')).toBe(false)
  })

  it('le joueur concerne : bord a sa couleur, pastille avec son numero de siege', () => {
    pc(true)
    monter({ essai: true, cadre: { genre: 'joueur', joueur: 1, couleurs: ['#d1382c'], raye: true, siege: 2 } })
    expect(section()?.className).toContain('est-cadre-joueur')
    expect(section()?.className).toContain('est-cadre-raye')
    expect(document.querySelector('.essai-pastille-joueur b')?.textContent).toBe('J2')
  })

  it('un moment commun (menace) : cadre commun, pastille sans numero', () => {
    pc(true)
    monter({ essai: true, cadre: { genre: 'commun' } })
    expect(section()?.className).toContain('est-cadre-commun')
    expect(document.querySelector('.essai-pastille-joueur b')).toBeNull()
  })
})
