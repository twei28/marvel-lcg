import { describe, it, expect } from 'vitest'
import { fondDe } from './halo-heros'
// Module JavaScript nu de l'assistant, sans types. Il portait un
// `@ts-expect-error` devenu INUTILE : TypeScript résout désormais ce module
// seul, et une directive qui n'attrape plus rien est elle-même une erreur
// (TS2578). Elle cassait `npm run typecheck`, donc la construction du
// plateau, donc tout déploiement, depuis le 19/09/2026.
import { fondDe as fondEditeur } from '../../../Fusion/marvel-lcg-src/public/js/palettes/couleurs.js'

// L'ÉDITEUR DE PALETTES DOIT MONTRER LE VRAI FOND DU PLATEAU.
//
// Écrite le 19/09/2026 avec l'éditeur. Le cadrage disait, mot pour mot :
// « juger sur un échantillon est précisément ce qui a produit les couleurs
// fausses ; l'échantillon de chaque personnage doit reproduire le VRAI rendu
// du fond de plateau, pas un aplat de couleur ».
//
// La formule vit donc en deux exemplaires : ici en TypeScript pour le plateau
// (React), et en JavaScript nu pour la page de l'assistant, qui ne passe pas
// par le bundle. Deux copies dérivent toujours — sauf si quelque chose les
// compare. C'est ce fichier.
describe('le fond du plateau et celui de l’éditeur de palettes', () => {
  const CAS: Array<{ nom: string; couleurs: Array<[number, number, number]> }> = [
    { nom: 'trois couleurs', couleurs: [[140, 41, 31], [32, 43, 114], [219, 220, 222]] },
    { nom: 'deux couleurs', couleurs: [[47, 112, 63], [220, 226, 224]] },
    { nom: 'une seule couleur', couleurs: [[18, 18, 17]] },
    { nom: 'quatre couleurs (la quatrième est ignorée)', couleurs: [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]] },
  ]

  for (const cas of CAS) {
    it(`rendent la même bande : ${cas.nom}`, () => {
      expect(fondEditeur(cas.couleurs, '#101010')).toBe(fondDe(cas.couleurs, '#101010'))
    })
  }

  it('rendent le même fond nu quand il n’y a aucune couleur', () => {
    expect(fondEditeur([], '#101010')).toBe(fondDe([], '#101010'))
    expect(fondEditeur(undefined, '#101010')).toBe(fondDe(undefined, '#101010'))
  })
})
