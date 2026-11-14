// Les cartes posées « sous » une autre (State of Flow de Shang-Chi, cartes glissées de Corsair ou de Havok…) ne sont PAS des
// améliorations : le texte de la carte dit « place it faceup on top here, forming a pile ».
//
// Rapport du 26/10/2026, partie réelle sur téléphone : « j'ai joué Augmented Blow, il l'a laissé en jeu, comme si c'était un upgrade ».
// Le moteur faisait exactement ce que dit State of Flow (la pile est dans `docs/packs/shang-chi/`, cas `[ch] ch002` verts) : c'est le
// plateau qui dessinait l'événement empilé comme une amélioration ordinaire. Ces tests fixent la règle d'affichage.
import { describe, expect, it } from 'vitest'
import type { ScanCardProps } from '../components/ScanCard'
import { compterEmpilees, estEmpilee, libelleEmpilees } from './empilees'

const carte = (id: number, nom: string, kind: ScanCardProps['kind']): ScanCardProps =>
  ({ id: String(id), name: nom, kind, imageUrl: '' }) as unknown as ScanCardProps

describe('une carte posée sous une autre est empilée, pas attachée', () => {
  it('un événement ou une ressource posés sous une carte forment une pile', () => {
    expect(estEmpilee(carte(1, 'Augmented Blow', 'event'))).toBe(true)
    expect(estEmpilee(carte(2, 'Energy', 'resource'))).toBe(true)
  })

  it('une amélioration, un allié ou un statut restent des attachements', () => {
    expect(estEmpilee(carte(3, 'Stark Nunchaku', 'upgrade'))).toBe(false)
    expect(estEmpilee(carte(4, 'Hawkeye', 'ally'))).toBe(false)
    expect(estEmpilee(carte(5, 'Tenace', 'status'))).toBe(false)
    expect(estEmpilee(carte(6, 'Combat Training', 'attachment'))).toBe(false)
  })

  it('on compte seulement les cartes empilées', () => {
    const attachees = [carte(1, 'A', 'event'), carte(2, 'B', 'upgrade'), carte(3, 'C', 'event'), carte(4, 'D', 'status')]
    expect(compterEmpilees(attachees)).toBe(2)
    expect(compterEmpilees([])).toBe(0)
  })

  it('le libellé dit combien de cartes sont dans la pile', () => {
    expect(libelleEmpilees(1)).toMatch(/1/)
    expect(libelleEmpilees(3)).toMatch(/3/)
    expect(libelleEmpilees(3).toLowerCase()).toContain('pile')
  })
})
