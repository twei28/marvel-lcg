// Ce que ce cas protège : la recherche par nom du mode manuel
// (`Catalogue.chercherParNom`) est le seul endroit du plateau où l'on cherche
// une carte qui N'EST PAS dans la partie — le catalogue réel dépasse les 6000
// cartes, donc trois défauts casseraient le mode manuel en silence : chercher
// sur une seule lettre (illisible), ne jamais couper (fenêtre qui déborde), et
// oublier le scan de la carte trouvée (liste de noms nus, invérifiable à cette
// échelle).
import { describe, expect, it } from 'vitest'
import { catalogueVide, construire } from './catalogue'

const catalogue = (cartes: unknown[]) => construire({ paquet: cartes })

describe('Catalogue.chercherParNom', () => {
  it('ne cherche pas en dessous de deux caractères', () => {
    const c = catalogue([{ card_id: '01094', name: 'Rhino' }])
    expect(c.chercherParNom('r')).toEqual([])
    expect(c.chercherParNom('')).toEqual([])
  })

  it('trouve une carte par un fragment de son nom, insensible à la casse', () => {
    const c = catalogue([
      { card_id: '01094', name: 'Rhino' },
      { card_id: '01001a', name: 'Spider-Man' },
    ])
    expect(c.chercherParNom('RHI')).toEqual([{ card_id: '01094', name: 'Rhino' }])
  })

  it('ne trouve rien qui ne correspond pas', () => {
    const c = catalogue([{ card_id: '01094', name: 'Rhino' }])
    expect(c.chercherParNom('zzzz')).toEqual([])
  })

  it('rapporte le pic_id de la carte, quand la carte en emprunte un', () => {
    const c = catalogue([{ card_id: '01098b', name: 'Rhino (verso)', pic_id: '01098' }])
    expect(c.chercherParNom('rhino')).toEqual([
      { card_id: '01098b', name: 'Rhino (verso)', pic_id: '01098' },
    ])
  })

  it('coupe à la limite demandée', () => {
    const cartes = Array.from({ length: 5 }, (_, i) => ({ card_id: `id${i}`, name: `Carte ${i}` }))
    const c = catalogue(cartes)
    expect(c.chercherParNom('carte', 2)).toHaveLength(2)
  })

  it('coupe à 40 résultats par défaut', () => {
    const cartes = Array.from({ length: 50 }, (_, i) => ({ card_id: `id${i}`, name: `Carte ${i}` }))
    const c = catalogue(cartes)
    expect(c.chercherParNom('carte')).toHaveLength(40)
  })

  it('un catalogue vide ne trouve jamais rien', () => {
    expect(catalogueVide.chercherParNom('rhino')).toEqual([])
  })
})
