// La frise de la phase du mechant (decisions du 03/10/2026) : six onglets,
// un resultat court par onglet, et les temps vides dits par une etape courte.
import { afterEach, describe, expect, it } from 'vitest'
import type { EtapeDeroule } from './deroule-phase'
import { ONGLETS, avecTempsVides, compter, fusionnerDistribution, resumeOnglet, retenirCartesDistribuees, totauxVides } from './frise-phase'
import { titreEtape } from './deroule-textes'
import { bilanTroisColonnes } from './vue-cartouche'

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
    // Trois et non quatre : la distribution n'est jamais declaree vide (voir
    // le cas suivant). Sa phrase reste dans `TEXTE_TEMPS_VIDE`, sans emploi.
    const textes = avecTempsVides([menace], true).slice(1).map(titreEtape)
    expect(textes).toEqual([
      'Le méchant ne s’active pas',
      'Aucun sbire engagé',
      'Rien à révéler',
    ])
    expect(titreEtape(etape({ cle: 'v', temps: 'menace', titre: 'vide' }))).toBe('Aucune menace posée')
  })
})

// LA DISTRIBUTION FONDUE (decision D15 du 04/10/2026) : en scene PC, le point 3
// ne coute plus de clic. Ses etapes sont retirees de la liste AVANT le
// controleur, et leur compte voyage a part (« 1 carte distribuée » en tete de
// la pastille « 3. Cartes rencontre »).
describe('fusionnerDistribution : le point 3 sans clic', () => {
  it('retire les etapes du temps distribution et compte les cartes, dans l ordre', () => {
    const deux = { ...distribution, cle: 'd2', auteurNom: 'Hulk', montant: 2 }
    const { etapes, cartesDistribuees } = fusionnerDistribution([menace, attaqueMechant, distribution, deux, revelation])
    expect(etapes.map((e) => e.cle)).toEqual(['m', 'a1', 'r'])
    expect(cartesDistribuees).toBe(3)
  })

  it('rend la MEME reference quand il n y a rien a retirer', () => {
    const liste = [menace, attaqueMechant, revelation]
    const fusion = fusionnerDistribution(liste)
    expect(fusion.etapes).toBe(liste)
    expect(fusion.cartesDistribuees).toBe(0)
  })

  it('une etape de distribution sans montant compte une carte', () => {
    const { cartesDistribuees } = fusionnerDistribution([{ ...distribution, montant: undefined }])
    expect(cartesDistribuees).toBe(1)
  })

  it('une liste vide reste vide', () => {
    expect(fusionnerDistribution([])).toEqual({ etapes: [], cartesDistribuees: 0 })
  })
})

describe('avecTempsVides : la distribution n est jamais declaree vide', () => {
  it('une liste deja fondue ne fabrique pas d etape vide:distribution', () => {
    const liste = avecTempsVides([menace, attaqueMechant, revelation], true)
    expect(liste.map((e) => e.cle)).not.toContain('vide:distribution')
    expect(liste.map((e) => e.cle)).toEqual(['m', 'a1', 'vide:sbires', 'r'])
  })
})

describe('compter : la regle unique de comptage, exportee', () => {
  it('additionne une carte revelee, ses effets et ses consequences', () => {
    const consequence = etape({ cle: 'c', temps: 'revelation', titre: 'attaque', etat: 'resolu', montant: 4 })
    const totaux = totauxVides()
    compter({ ...revelation, consequences: [consequence] }, totaux)
    expect(totaux).toMatchObject({ degats: 4, menaces: 2, sbires: 0, autres: 0 })
  })

  it('ne compte pas une activation seulement annoncee', () => {
    const totaux = totauxVides()
    compter({ ...attaqueMechant, etat: 'annonce' }, totaux)
    expect(totaux.degats).toBe(0)
  })
})

// ⚠ PIEGE 43 DE LA CARTE (04/10/2026) : `lignesBilan` et `resumeOnglet` ne
// comptaient pas la meme chose (l'un ignorait les effets et les consequences
// d'une carte revelee). Le bilan du cartouche du bas lit la MEME regle que les
// onglets (`compter`, `coupsDe`) : leurs totaux ne peuvent plus diverger.
describe('une seule regle de comptage : onglets et bilan en trois colonnes', () => {
  it('donnent le meme total de degats et de menaces sur les fixtures du fichier', () => {
    const consequence = etape({ cle: 'c', temps: 'revelation', titre: 'attaque', etat: 'resolu', montant: 4, cibleNom: 'Spider-Man', cibleId: 40 })
    const etapes = [menace, attaqueMechant, distribution, { ...revelation, consequences: [consequence] }]
    const totaux = totauxVides()
    for (const e of etapes) compter(e, totaux)
    expect(resumeOnglet(etapes, 'bilan')).toBe(`${totaux.degats} dégâts · +${totaux.menaces} menaces`)
    const bilan = bilanTroisColonnes(etapes, { etapes, index: 0, boostsMontres: 0 })
    expect(bilan.heros.reduce((somme, c) => somme + c.total, 0)).toBe(totaux.degats)
    expect(bilan.menace.reduce((somme, c) => somme + c.total, 0)).toBe(totaux.menaces)
    expect(totaux).toMatchObject({ degats: 7, menaces: 3 })
  })
})

// Le compte des cartes distribuees, RETENU pour la phase (board.tsx) : le
// moteur incremente le round en quittant la phase, le journal du round se vide,
// et le bilan doit encore dire « 1 carte distribuée ».
describe('retenirCartesDistribuees', () => {
  const vide = { round: undefined, compte: 0 }

  it('retient le plus grand compte vu pendant la phase', () => {
    let r = retenirCartesDistribuees(vide, { round: 3, compte: 1, enPhase: true })
    r = retenirCartesDistribuees(r, { round: 3, compte: 2, enPhase: true })
    r = retenirCartesDistribuees(r, { round: 3, compte: 0, enPhase: true })
    expect(r).toEqual({ round: 3, compte: 2 })
  })

  it('le garde quand le round tourne en sortant de la phase (le bilan le lit)', () => {
    const pendant = retenirCartesDistribuees(vide, { round: 3, compte: 1, enPhase: true })
    expect(retenirCartesDistribuees(pendant, { round: 4, compte: 0, enPhase: false })).toEqual({ round: 3, compte: 1 })
  })

  it('repart de zero a la phase du mechant du round suivant', () => {
    const pendant = retenirCartesDistribuees(vide, { round: 3, compte: 1, enPhase: true })
    expect(retenirCartesDistribuees(pendant, { round: 4, compte: 0, enPhase: true })).toEqual({ round: 4, compte: 0 })
  })

  it('rend la meme reference quand rien ne change', () => {
    const pendant = retenirCartesDistribuees(vide, { round: 3, compte: 1, enPhase: true })
    expect(retenirCartesDistribuees(pendant, { round: 3, compte: 1, enPhase: true })).toBe(pendant)
  })
})
