import { describe, expect, it } from 'vitest'
import { creerEtatTouches, interpreterDoubleClic, interpreterTouche, natureDe, type CarteVisee } from './clavier'

const carte = (type: string, id: number, plus: Partial<CarteVisee> = {}): CarteVisee => ({
  genre: 'carte',
  id,
  type,
  prete: true,
  faceVisible: true,
  statuts: { stunned: false, confused: false, tough: false },
  ...plus,
})
const HEROS = carte('Hero', 1)
const ALLIE = carte('Ally', 2)
const SBIRE = carte('Minion', 3)
const VILAIN = carte('EncounterVillain', 7)
const MANIGANCE = carte('SideScheme', 9)
const PRINCIPALE = carte('MainScheme', 10)
const EVENEMENT = carte('Event', 4)
const SOUTIEN = carte('Support', 5)
const DECK = { genre: 'pile', zone: 'PlayerDeck' } as const

const touche = (cle: string, plus: { majuscule?: boolean; ctrl?: boolean; alt?: boolean } = {}) => ({
  cle,
  majuscule: plus.majuscule ?? false,
  ctrl: plus.ctrl,
  alt: plus.alt,
})

describe('les touches du mode manuel, calquées sur OCTGN', () => {
  it('Ctrl+F retourne, Ctrl+V donne la victoire', () => {
    expect(interpreterTouche(touche('f', { ctrl: true }), SBIRE)).toEqual({ geste: 'retourner', id: 3 })
    expect(interpreterTouche(touche('v', { ctrl: true }), SBIRE)).toEqual({ geste: 'victoire', id: 3 })
  })

  it('F7 incline une carte redressée et redresse une carte inclinée', () => {
    expect(interpreterTouche(touche('F7'), ALLIE)).toEqual({ geste: 'incliner', id: 2 })
    expect(interpreterTouche(touche('F7'), carte('Ally', 2, { prete: false }))).toEqual({ geste: 'redresser', id: 2 })
    expect(interpreterTouche(touche('F7'), EVENEMENT)).toBeUndefined()
  })

  it('F3 / Maj+F3 : dégâts, jamais sur une manigance', () => {
    expect(interpreterTouche(touche('F3'), SBIRE)).toEqual({ geste: 'jetons', id: 3, nature: 'degats', nombre: 1 })
    expect(interpreterTouche(touche('F3', { majuscule: true }), SBIRE))
      .toEqual({ geste: 'jetons', id: 3, nature: 'degats', nombre: -1 })
    expect(interpreterTouche(touche('F3'), MANIGANCE)).toBeUndefined()
  })

  it('F5 / Maj+F5 : menace, seulement sur une manigance', () => {
    expect(interpreterTouche(touche('F5'), MANIGANCE)).toEqual({ geste: 'jetons', id: 9, nature: 'menace', nombre: 1 })
    expect(interpreterTouche(touche('F5', { majuscule: true }), MANIGANCE))
      .toEqual({ geste: 'jetons', id: 9, nature: 'menace', nombre: -1 })
    expect(interpreterTouche(touche('F5'), VILAIN)).toBeUndefined()
  })

  it('F4 / Maj+F4 : accélération', () => {
    expect(interpreterTouche(touche('F4'), PRINCIPALE)).toEqual({ geste: 'acceleration', id: 10, nombre: 1 })
    expect(interpreterTouche(touche('F4', { majuscule: true }), PRINCIPALE))
      .toEqual({ geste: 'acceleration', id: 10, nombre: -1 })
  })

  it('Alt+S/C/T pose un statut absent, Ctrl+Alt+S/C/T retire un statut présent', () => {
    expect(interpreterTouche(touche('s', { alt: true }), VILAIN))
      .toEqual({ geste: 'statut', id: 7, statut: 'stun', pose: true })
    expect(interpreterTouche(touche('c', { alt: true }), SBIRE))
      .toEqual({ geste: 'statut', id: 3, statut: 'confuse', pose: true })
    expect(interpreterTouche(touche('t', { alt: true }), HEROS))
      .toEqual({ geste: 'statut', id: 1, statut: 'tough', pose: true })
    const sonne = carte('Minion', 3, { statuts: { stunned: true, confused: false, tough: false } })
    expect(interpreterTouche(touche('s', { alt: true }), sonne)).toBeUndefined()
    expect(interpreterTouche(touche('s', { alt: true, ctrl: true }), sonne))
      .toEqual({ geste: 'statut', id: 3, statut: 'stun', pose: false })
    expect(interpreterTouche(touche('s', { alt: true, ctrl: true }), SBIRE)).toBeUndefined()
    expect(interpreterTouche(touche('t', { alt: true }), MANIGANCE)).toBeUndefined()
  })

  it('Suppr : défausse, vainc le stade du méchant, termine la manigance principale, rien sur un héros', () => {
    expect(interpreterTouche(touche('Delete'), ALLIE)).toEqual({ geste: 'defausser', id: 2 })
    expect(interpreterTouche(touche('Delete'), VILAIN)).toEqual({ geste: 'vaincreStade' })
    expect(interpreterTouche(touche('Delete'), PRINCIPALE)).toEqual({ geste: 'maniganceTerminee' })
    expect(interpreterTouche(touche('Delete'), HEROS)).toBeUndefined()
    expect(interpreterTouche(touche('Delete'), DECK)).toBeUndefined()
  })

  it('haut / bas : points de vie d’un héros ou d’un méchant, dégâts d’un allié, menace d’une manigance, marqueur ailleurs', () => {
    expect(interpreterTouche(touche('ArrowUp'), HEROS)).toEqual({ geste: 'jetons', id: 1, nature: 'pv', nombre: 1 })
    expect(interpreterTouche(touche('ArrowDown'), VILAIN)).toEqual({ geste: 'jetons', id: 7, nature: 'pv', nombre: -1 })
    // Haut soigne, bas blesse : comme sur un héros (écart voulu avec OCTGN).
    expect(interpreterTouche(touche('ArrowUp'), ALLIE)).toEqual({ geste: 'jetons', id: 2, nature: 'degats', nombre: -1 })
    expect(interpreterTouche(touche('ArrowDown'), ALLIE)).toEqual({ geste: 'jetons', id: 2, nature: 'degats', nombre: 1 })
    expect(interpreterTouche(touche('ArrowDown'), MANIGANCE))
      .toEqual({ geste: 'jetons', id: 9, nature: 'menace', nombre: -1 })
    expect(interpreterTouche(touche('ArrowUp'), SOUTIEN)).toEqual({ geste: 'compteur', id: 5, nombre: 1 })
  })

  it('droite / gauche : marqueur générique, sur tout type de carte', () => {
    expect(interpreterTouche(touche('ArrowRight'), VILAIN)).toEqual({ geste: 'compteur', id: 7, nombre: 1 })
    expect(interpreterTouche(touche('ArrowLeft'), MANIGANCE)).toEqual({ geste: 'compteur', id: 9, nombre: -1 })
  })

  it('sur une pile : Ctrl+S mélange, Ctrl+D pioche, Ctrl+Maj+D demande combien', () => {
    expect(interpreterTouche(touche('s', { ctrl: true }), DECK)).toEqual({ geste: 'melanger', zone: 'PlayerDeck' })
    expect(interpreterTouche(touche('d', { ctrl: true }), DECK))
      .toEqual({ geste: 'piocher', zone: 'PlayerDeck', nombre: 1 })
    expect(interpreterTouche(touche('d', { ctrl: true, majuscule: true }), DECK))
      .toEqual({ geste: 'piocherPlusieurs', zone: 'PlayerDeck' })
    expect(interpreterTouche(touche('f', { ctrl: true }), DECK)).toBeUndefined()
  })

  it('un chiffre sur une pile pioche autant de cartes, sur un méchant pose ses jetons (question 10)', () => {
    expect(interpreterTouche(touche('5'), DECK)).toEqual({ geste: 'piocher', zone: 'PlayerDeck', nombre: 5 })
    // Sur un méchant ou un héros aussi, le chiffre BLESSE (la nature « pv »
    // d'OCTGN soignerait : « plus » y compte les points de vie restants).
    expect(interpreterTouche(touche('3'), VILAIN)).toEqual({ geste: 'jetons', id: 7, nature: 'degats', nombre: 3 })
    expect(interpreterTouche(touche('3'), EVENEMENT)).toBeUndefined()
  })

  it('les gestes de table : Alt+Entrée, Ctrl+Q, F12, même sans rien survoler', () => {
    expect(interpreterTouche(touche('Enter', { alt: true }), DECK)).toEqual({ geste: 'amplification' })
    expect(interpreterTouche(touche('q', { ctrl: true }), DECK)).toEqual({ geste: 'toutRedresser' })
    expect(interpreterTouche(touche('F12'), DECK)).toEqual({ geste: 'finPhaseHeros' })
  })

  // Question 10 du 06/10/2026 : les touches maison restent, EN PLUS d'OCTGN.
  it('touches maison : F retourne, Q incline, R mélange une pile', () => {
    expect(interpreterTouche(touche('f'), VILAIN)).toEqual({ geste: 'retourner', id: 7 })
    expect(interpreterTouche(touche('q'), ALLIE)).toEqual({ geste: 'incliner', id: 2 })
    expect(interpreterTouche(touche('r'), DECK)).toEqual({ geste: 'melanger', zone: 'PlayerDeck' })
    expect(interpreterTouche(touche('r', { ctrl: true }), DECK)).toBeUndefined()
    expect(interpreterTouche(touche('r'), VILAIN)).toBeUndefined()
    expect(interpreterTouche(touche('q'), EVENEMENT)).toBeUndefined()
  })

  // ⚠ AZERTY : un chiffre s'y tape AVEC Maj. Maj ne peut donc pas vouloir
  // dire « retirer » : le chiffre pose toujours, le retrait reste aux flèches.
  it('touches maison : un chiffre pose autant de jetons naturels, Maj ou pas (AZERTY)', () => {
    expect(interpreterTouche(touche('3'), SBIRE)).toEqual({ geste: 'jetons', id: 3, nature: 'degats', nombre: 3 })
    expect(interpreterTouche(touche('2', { majuscule: true }), MANIGANCE)).toEqual({
      geste: 'jetons', id: 9, nature: 'menace', nombre: 2,
    })
    expect(interpreterTouche(touche('4'), SOUTIEN)).toEqual({ geste: 'compteur', id: 5, nombre: 4 })
    expect(interpreterTouche(touche('4', { ctrl: true }), SBIRE)).toBeUndefined()
  })

  // Lot 6 du 06/10/2026 : gestes OCTGN de pile restants.
  it('Ctrl+F sur une pile retourne la carte du dessus (FlipDeckTopCard)', () => {
    expect(interpreterTouche(touche('f', { ctrl: true }), { ...DECK, dessus: 40 })).toEqual({ geste: 'retourner', id: 40 })
    expect(interpreterTouche(touche('f', { ctrl: true }), DECK)).toBeUndefined()
  })

  it('Ctrl+U pioche face cachée, Ctrl+Maj+U demande combien (drawUnrevealed)', () => {
    expect(interpreterTouche(touche('u', { ctrl: true }), DECK)).toEqual({ geste: 'piocherCache', zone: 'PlayerDeck', nombre: 1 })
    expect(interpreterTouche(touche('U', { ctrl: true, majuscule: true }), DECK)).toEqual({
      geste: 'piocherCachePlusieurs', zone: 'PlayerDeck',
    })
  })

  it('F1 ouvre le choix du marqueur (le menu de la carte), Maj+F1 efface les marqueurs', () => {
    expect(interpreterTouche(touche('F1'), SBIRE)).toEqual({ geste: 'menuCarte', id: 3 })
    expect(interpreterTouche(touche('F1', { majuscule: true }), SBIRE)).toEqual({ geste: 'effacerMarqueurs', id: 3 })
  })

  it('la touche Menu et Maj+F10 ouvrent le menu de la carte survolée (clavier seul)', () => {
    expect(interpreterTouche(touche('ContextMenu'), ALLIE)).toEqual({ geste: 'menuCarte', id: 2 })
    expect(interpreterTouche(touche('F10', { majuscule: true }), ALLIE)).toEqual({ geste: 'menuCarte', id: 2 })
    expect(interpreterTouche(touche('F10'), ALLIE)).toBeUndefined()
  })

  it('une touche inconnue ne fait rien', () => {
    expect(interpreterTouche(touche('z'), VILAIN)).toBeUndefined()
  })
})

describe('le double-clic d’OCTGN', () => {
  it('retourne une carte face cachée', () => {
    expect(interpreterDoubleClic(carte('Minion', 3, { faceVisible: false }))).toEqual({ geste: 'retourner', id: 3 })
  })
  it('sur le méchant : amplification', () => {
    expect(interpreterDoubleClic(VILAIN)).toEqual({ geste: 'amplification' })
  })
  it('incline ou redresse un allié, une amélioration, un soutien, un héros', () => {
    expect(interpreterDoubleClic(ALLIE)).toEqual({ geste: 'incliner', id: 2 })
    expect(interpreterDoubleClic(carte('Support', 5, { prete: false }))).toEqual({ geste: 'redresser', id: 5 })
  })
  // Lot 6 du 06/10/2026 : comme `defaultCardAction` d'OCTGN, une manigance se
  // retourne ; le moteur repose sa menace de départ (`Scheme2.OnFlip`).
  it('sur une manigance : la retourner', () => {
    expect(interpreterDoubleClic(MANIGANCE)).toEqual({ geste: 'retourner', id: 9 })
    expect(interpreterDoubleClic(PRINCIPALE)).toEqual({ geste: 'retourner', id: 10 })
  })
  it('rien sur un sbire ou un événement', () => {
    expect(interpreterDoubleClic(SBIRE)).toBeUndefined()
    expect(interpreterDoubleClic(EVENEMENT)).toBeUndefined()
  })
})

describe('ce que mesure une carte', () => {
  it('suit le type', () => {
    expect(natureDe('Hero')).toBe('pv')
    expect(natureDe('Villain')).toBe('pv')
    expect(natureDe('Minion')).toBe('degats')
    expect(natureDe('MainScheme')).toBe('menace')
    expect(natureDe('Upgrade')).toBe('marqueur')
  })
})

describe("l'etat des touches enfoncees (pour la tache 5)", () => {
  it('retient une touche enfoncee', () => {
    const etat = creerEtatTouches()
    etat.enregistrer({ key: 'Shift', type: 'keydown' })
    expect(etat.estEnfoncee('shift')).toBe(true)
  })

  it('oublie une touche relachee', () => {
    const etat = creerEtatTouches()
    etat.enregistrer({ key: 'Shift', type: 'keydown' })
    etat.enregistrer({ key: 'Shift', type: 'keyup' })
    expect(etat.estEnfoncee('shift')).toBe(false)
  })

  it('ignore la casse', () => {
    const etat = creerEtatTouches()
    etat.enregistrer({ key: 'A', type: 'keydown' })
    expect(etat.estEnfoncee('a')).toBe(true)
  })

  it('vaut faux avant toute touche', () => {
    const etat = creerEtatTouches()
    expect(etat.estEnfoncee('shift')).toBe(false)
  })
})
