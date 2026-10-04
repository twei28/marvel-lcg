// La frise de la phase du mechant (decisions du 03/10/2026) : six onglets,
// un resultat court par onglet, et les temps vides dits par une etape courte.
import { afterEach, describe, expect, it } from 'vitest'
import type { EtapeDeroule } from './deroule-phase'
import { ONGLETS, avecTempsVides, resumeOnglet } from './frise-phase'
import { titreEtape } from './deroule-textes'

afterEach(() => window.localStorage.clear())

const etape = (e: Partial<EtapeDeroule> & Pick<EtapeDeroule, 'cle' | 'temps' | 'titre'>): EtapeDeroule => ({
  regle: '',
  boosts: [],
  ...e,
})

const menace = etape({ cle: 'm', temps: 'menace', titre: 'menace', cibleNom: 'Effraction', montant: 1 })
const attaqueMechant = etape({
  cle: 'a1', temps: 'mechant', titre: 'attaque', etat: 'resolu', auteurNom: 'Rhino', cibleNom: 'Spider-Man', montant: 3,
})
const distribution = etape({ cle: 'd', temps: 'distribution', titre: 'distribution', auteurNom: 'Spider-Man', montant: 1 })
const revelation = etape({
  cle: 'r', temps: 'revelation', titre: 'revelation', cibleNom: 'Hard to Keep Down',
  effets: [{ genre: 'menace', cible: 'Effraction', cible_id: 9, montant: 2 }],
})

describe('les six onglets', () => {
  it('portent les noms officiels numerotes, puis le Bilan', () => {
    expect(ONGLETS.map((o) => o.libelle)).toEqual([
      '1. Placer les menaces',
      '2a. Le méchant s’active',
      '2b. Les sbires s’activent',
      '3. Attribuer les cartes Rencontre',
      '4. Révéler les cartes Rencontre',
      'Bilan',
    ])
  })
})

describe('resumeOnglet : le resultat court, total par effet', () => {
  it('additionne par effet', () => {
    const deuxCoups = [attaqueMechant, { ...attaqueMechant, cle: 'a2', montant: 2 }]
    expect(resumeOnglet(deuxCoups, 'mechant')).toBe('5 dégâts')
    expect(resumeOnglet([menace], 'menace')).toBe('+1 menace')
  })

  it('melange les effets dans un ordre fixe, separes par un point median', () => {
    const manigance = etape({ cle: 'a3', temps: 'mechant', titre: 'manigance', etat: 'resolu', montant: 1 })
    expect(resumeOnglet([attaqueMechant, manigance], 'mechant')).toBe('3 dégâts · +1 menace')
  })

  it('dit « aucun » d un onglet sans effet', () => {
    expect(resumeOnglet([menace], 'sbires')).toBe('aucun')
    const annulee = etape({ cle: 'x', temps: 'sbires', titre: 'attaque', etat: 'annule' })
    expect(resumeOnglet([annulee], 'sbires')).toBe('aucun')
  })

  it('compte les cartes distribuees, et les effets des cartes revelees', () => {
    expect(resumeOnglet([distribution, { ...distribution, cle: 'd2', montant: 2 }], 'distribution')).toBe('3 cartes')
    expect(resumeOnglet([revelation], 'revelation')).toBe('+2 menaces')
  })

  it('une carte revelee sans effet mesure se compte comme carte revelee', () => {
    const muette = etape({ cle: 'r2', temps: 'revelation', titre: 'revelation', cibleNom: 'Rien' })
    expect(resumeOnglet([muette], 'revelation')).toBe('1 carte révélée')
  })

  it('compte les consequences rangees sous une carte revelee', () => {
    const consequence = etape({ cle: 'c', temps: 'revelation', titre: 'attaque', etat: 'resolu', montant: 4 })
    expect(resumeOnglet([{ ...revelation, consequences: [consequence] }], 'revelation')).toBe('4 dégâts · +2 menaces')
  })

  it('statuts et sbires entres en jeu', () => {
    const sonne = etape({ cle: 's', temps: 'mechant', titre: 'statut', statut: 'Stunned', cibleNom: 'Spider-Man', montant: 1 })
    const drone = etape({ cle: 'e', temps: 'mechant', titre: 'entree', cibleNom: 'Drone' })
    expect(resumeOnglet([attaqueMechant, sonne, drone], 'mechant')).toBe('3 dégâts · Sonné · +1 sbire')
  })

  it('le Bilan resume toute la phase', () => {
    expect(resumeOnglet([menace, attaqueMechant, distribution, revelation], 'bilan')).toBe('3 dégâts · +3 menaces')
  })
})

describe('avecTempsVides : un temps passe sans rien a son etape courte', () => {
  it('insere les temps vides AVANT le dernier temps qui a des etapes, a leur place', () => {
    const liste = avecTempsVides([menace, distribution], false)
    expect(liste.map((e) => e.cle)).toEqual(['m', 'vide:mechant', 'vide:sbires', 'd'])
    expect(liste[1]).toMatchObject({ temps: 'mechant', titre: 'vide' })
  })

  it('n invente rien apres le dernier temps connu tant que la phase court', () => {
    expect(avecTempsVides([menace], false).map((e) => e.cle)).toEqual(['m'])
  })

  it('phase finie : tous les temps sans etape ont la leur', () => {
    expect(avecTempsVides([menace, attaqueMechant, distribution], true).map((e) => e.cle)).toEqual([
      'm', 'a1', 'vide:sbires', 'd', 'vide:revelation',
    ])
  })

  it('une liste vide reste vide', () => {
    expect(avecTempsVides([], true)).toEqual([])
  })

  it('rien avant le premier temps connu (journal incomplet)', () => {
    expect(avecTempsVides([distribution], true).map((e) => e.cle)).toEqual(['d', 'vide:revelation'])
  })

  it('chaque etape vide se dit en une phrase', () => {
    const textes = avecTempsVides([menace], true).slice(1).map(titreEtape)
    expect(textes).toEqual([
      'Le méchant ne s’active pas',
      'Aucun sbire engagé',
      'Aucune carte rencontre distribuée',
      'Rien à révéler',
    ])
    expect(titreEtape(etape({ cle: 'v', temps: 'menace', titre: 'vide' }))).toBe('Aucune menace posée')
  })
})
