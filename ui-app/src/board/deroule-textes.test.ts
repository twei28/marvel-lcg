// Les phrases du deroule : ecrites par nous, pas la narration du moteur.
//
// « Ultron frappe Shuri » se lit ; « [(50,01113) Klaw] would deal 2 damage »
// se dechiffre. Et tout passe par le dictionnaire : le plateau est bilingue,
// rattraper les traductions apres coup coute plus cher que de les poser tout
// de suite.
import { describe, expect, it } from 'vitest'
import { regleEtape, titreEtape } from './deroule-textes'
import type { EtapeDeroule } from './deroule-phase'

const etape = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
  cle: 'k',
  temps: 'activations',
  titre: 'attaque',
  regle: 'regle:activations',
  carteId: 50,
  cibleId: 12,
  auteurNom: 'Ultron',
  cibleNom: 'Shuri',
  boosts: [],
  consequences: [],
  ...extra,
})

describe('phrases du deroule', () => {
  it('nomme l attaquant et sa cible', () => {
    expect(titreEtape(etape())).toBe('Ultron attaque Shuri')
  })

  it('dit la manigance autrement que l attaque', () => {
    expect(titreEtape(etape({ titre: 'manigance' }))).toBe('Ultron complote contre Shuri')
  })

  it('annonce la menace sans nommer de cible', () => {
    expect(
      titreEtape(etape({ temps: 'menace', titre: 'menace', carteId: undefined, cibleId: undefined, auteurNom: undefined, cibleNom: undefined }))
    ).toBe('Menace sur la manigance principale')
  })

  it('rappelle la regle du point 1', () => {
    expect(regleEtape(etape({ regle: 'regle:menace' })))
      .toBe('Point 1 : chaque joueur ajoute 1 menace à la manigance principale.')
  })

  it('rappelle la regle des activations', () => {
    expect(regleEtape(etape())).toBe('Point 2 : chaque ennemi s\'active contre le héros engagé avec lui.')
  })

  it('laisse passer un titre deja redige', () => {
    // Une carte revelee arrive avec son titre venu du journal : on ne le
    // reecrit pas.
    expect(titreEtape(etape({ temps: 'revelation', titre: 'Icy Grip révélée' })))
      .toBe('Icy Grip révélée')
  })

  it('rappelle la regle des cartes revelees', () => {
    expect(regleEtape(etape({ regle: 'regle:revelation' })))
      .toBe('Point 4 : chaque joueur révèle sa carte rencontre et en applique l\'effet.')
  })

  it('ne dit rien d une regle inconnue plutot que d inventer', () => {
    expect(regleEtape(etape({ regle: 'regle:inexistante' }))).toBe('')
  })

  it('nomme d apres le fait, pas d apres une recherche externe', () => {
    // Une carte morte pendant la phase n'est plus dans l'index du monde au
    // moment ou l'etape s'affiche : le titre doit rester juste puisqu'il lit
    // le nom porte par l'etape elle-meme, jamais une resolution a l'affichage.
    expect(titreEtape(etape({ auteurNom: 'Klaw', cibleNom: 'Drone détruit' })))
      .toBe('Klaw attaque Drone détruit')
  })
})
