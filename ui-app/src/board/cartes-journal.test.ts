import { describe, expect, it } from 'vitest'
import { decouperNoms, referencesDeBrut, referencesDeEntree } from './cartes-journal'
import { sansIdentifiantsEnFrancais } from './DemandeCentrale'

describe('les cartes nommees dans une ligne du journal', () => {
  it('lit les identifiants du moteur dans le texte brut', () => {
    expect(referencesDeBrut('[(50,01113) Klaw] attacks [[(12,01001a) Spider-Man]]')).toEqual([
      { id: 50, nom: 'Klaw' },
      { id: 12, nom: 'Spider-Man' },
    ])
  })

  it('donne le nom francais quand on joue en francais, pour retrouver le texte affiche', () => {
    expect(referencesDeBrut('[(61,01106) Stampede] discarded')).toEqual([{ id: 61, nom: 'Ruée' }])
    window.localStorage.setItem('marvel-board-scans-fr', 'off')
    try {
      expect(referencesDeBrut('[(61,01106) Stampede] discarded')).toEqual([{ id: 61, nom: 'Stampede' }])
    } finally {
      window.localStorage.removeItem('marvel-board-scans-fr')
    }
  })

  // Rapport n°134 (16/11/2026, « encore quelques infos en anglais ») : le journal ecrivait « "Too Good to be True" retournee »
  // alors que le scan dit « Trop Beau pour Etre Vrai » : le journal ne lisait que NOMS_FR (cartes officielles), jamais les
  // noms des cartes fan-made (NOMS_FR_FANMADE).
  it('donne le nom francais des cartes FAN-MADE (Dazzler) dans le journal et dans les liens', () => {
    const brut = '[(19,dz012) "Too Good to be True"] retournée(s)'
    expect(referencesDeBrut(brut)).toEqual([{ id: 19, nom: '"Trop Beau pour Être Vrai"' }])
    expect(sansIdentifiantsEnFrancais(brut)).toBe('"Trop Beau pour Être Vrai" retournée(s)')
    expect(sansIdentifiantsEnFrancais('[(5,bl016) Embraced] entre en jeu')).toBe('Étreinte entre en jeu')
  })

  it('une carte fan-made sans nom francais garde son nom du moteur', () => {
    expect(sansIdentifiantsEnFrancais('[(9,dz024) Song of Aggression] entre en jeu')).toBe('Song of Aggression entre en jeu')
  })

  it('reprend la carte visee par une entree de jeu, sans texte brut', () => {
    expect(referencesDeEntree({ cibleId: 7, nomCarte: 'Rhino' })).toEqual([{ id: 7, nom: 'Rhino' }])
  })

  it('ne retient rien sans identifiant', () => {
    expect(referencesDeBrut('Rhino attacks Spider-Man')).toEqual([])
    expect(referencesDeEntree({ nomCarte: 'Rhino' })).toEqual([])
    expect(referencesDeEntree({})).toEqual([])
  })

  it('decoupe le texte autour des noms identifies', () => {
    expect(
      decouperNoms('Klaw attaque Spider-Man', [
        { id: 50, nom: 'Klaw' },
        { id: 12, nom: 'Spider-Man' },
      ])
    ).toEqual([{ id: 50, nom: 'Klaw' }, ' attaque ', { id: 12, nom: 'Spider-Man' }])
  })

  it('laisse le texte intact quand aucune carte n est identifiee', () => {
    expect(decouperNoms('Rhino attaque Spider-Man', [])).toEqual(['Rhino attaque Spider-Man'])
  })

  it('laisse le texte intact quand le nom identifie n y figure pas', () => {
    expect(decouperNoms('Le méchant attaque', [{ id: 50, nom: 'Klaw' }])).toEqual(['Le méchant attaque'])
  })

  it('ne devine pas : un meme nom porte par deux cartes reste du texte', () => {
    expect(
      decouperNoms('Brute frappe Brute', [
        { id: 3, nom: 'Brute' },
        { id: 4, nom: 'Brute' },
      ])
    ).toEqual(['Brute frappe Brute'])
  })

  it('prefere le nom le plus long et ne coupe pas un mot', () => {
    expect(
      decouperNoms('Rhino Charge révélée, Rhinoceros non', [
        { id: 1, nom: 'Rhino' },
        { id: 2, nom: 'Rhino Charge' },
      ])
    ).toEqual([{ id: 2, nom: 'Rhino Charge' }, ' révélée, Rhinoceros non'])
  })

  it('souligne chaque occurrence du meme nom', () => {
    expect(decouperNoms('Rhino, puis Rhino', [{ id: 1, nom: 'Rhino' }])).toEqual([
      { id: 1, nom: 'Rhino' },
      ', puis ',
      { id: 1, nom: 'Rhino' },
    ])
  })
})
