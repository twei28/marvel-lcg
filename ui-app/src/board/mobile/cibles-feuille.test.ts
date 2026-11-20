// Les cibles montrees DANS la feuille de choix (maquette approuvee le 26/10/2026) : les memes ronds que sur la table, pris
// parmi les cartes que le moteur propose de CHOISIR (role `cible`). Fonction pure.
import { describe, expect, it } from 'vitest'
import type { ScanCardProps } from '../../components/ScanCard'
import type { EtatInteractif } from '../interaction'
import type { Plateau, UniteAffichee } from '../zones'
import { ciblesDeLaFeuille } from './cibles-feuille'

const carte = (id: string, kind: ScanCardProps['kind'] = 'minion'): ScanCardProps => ({ id, name: `Carte ${id}`, kind, imageUrl: `/scan/${id}.jpg` })
const unite = (id: string, attachees: ScanCardProps[] = [], kind: ScanCardProps['kind'] = 'minion'): UniteAffichee => ({
  cle: `u-${id}`,
  carte: carte(id, kind),
  attachees,
})
const etat = (role: EtatInteractif['role'], reste: Partial<EtatInteractif> = {}): EtatInteractif => ({ role, choisie: false, ...reste })
const plateau = (groupes: UniteAffichee[][][]): Plateau =>
  ({
    emplacements: groupes.map((g, i) => ({ cle: `e${i}`, titre: `E${i}`, groupes: g, nombreSurLaLigne: g.length })),
    nombreDeCartes: 0,
    idsAffiches: new Set<number>(),
    representantsDePile: new Map<number, number>(),
    nombreIgnore: 0,
  }) as unknown as Plateau

describe('les cibles de la feuille', () => {
  it('ne garde que les cartes que le moteur propose de choisir, dans l ordre de la table', () => {
    const p = plateau([[[unite('1'), unite('2')]], [[unite('3')]]])
    const interactifs = new Map<number, EtatInteractif>([
      [1, etat('cible')],
      [2, etat('indisponible')],
      [3, etat('cible')],
    ])
    expect(ciblesDeLaFeuille(p, interactifs).map((u) => u.carte.id)).toEqual(['1', '3'])
  })

  it('une cible deja choisie reste dans la rangee (on peut la retirer)', () => {
    const p = plateau([[[unite('1')]]])
    expect(ciblesDeLaFeuille(p, new Map([[1, etat('cible', { choisie: true })]])).map((u) => u.carte.id)).toEqual(['1'])
  })

  it('une amelioration ou un statut a choisir fait entrer sa carte porteuse : le rond la montre en petit', () => {
    const amelioration = carte('9', 'upgrade')
    const p = plateau([[[unite('1', [amelioration])]]])
    const interactifs = new Map<number, EtatInteractif>([[9, etat('cible')]])
    expect(ciblesDeLaFeuille(p, interactifs).map((u) => u.carte.id)).toEqual(['1'])
  })

  it('ne montre pas deux fois la meme carte et ignore les apercus', () => {
    const p = plateau([[[unite('1')]], [[unite('1')]], [[unite('4')]]])
    const interactifs = new Map<number, EtatInteractif>([
      [1, etat('cible')],
      [4, etat('cible-preview')],
    ])
    expect(ciblesDeLaFeuille(p, interactifs).map((u) => u.carte.id)).toEqual(['1'])
  })

  it('une fois le nombre de cibles atteint, les autres cibles LEGALES restent dans la rangee', () => {
    const p = plateau([[[unite('1'), unite('2'), unite('3')]]])
    // 1 est choisie ; 2 n'est plus « choisissable » (le maximum est atteint) mais le moteur l'avait proposee ; 3 n'a jamais ete une cible
    const interactifs = new Map<number, EtatInteractif>([
      [1, etat('cible', { choisie: true })],
      [2, etat('indisponible')],
      [3, etat('indisponible')],
    ])
    expect(ciblesDeLaFeuille(p, interactifs, [1, 2]).map((u) => u.carte.id)).toEqual(['1', '2'])
  })

  it('rend une liste vide quand rien n est a choisir sur la table (cible dans une pile : le selecteur reste)', () => {
    expect(ciblesDeLaFeuille(plateau([[[unite('1')]]]), new Map())).toEqual([])
  })
})
