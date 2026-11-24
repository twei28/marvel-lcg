// State of Flow (Shang-Chi) : « After you play an ATTACK event, place it faceup on top here, forming a pile ».
// Sur le plateau, les événements empilés ne doivent pas ressembler à des améliorations posées en jeu (rapport du 26/10/2026).
import { render } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { Unite } from './Board'
import type { ScanCardProps } from '../components/ScanCard'
import type { UniteAffichee } from './zones'

const carte = (id: number, nom: string, kind: ScanCardProps['kind']): ScanCardProps =>
  ({ id: String(id), name: nom, kind, imageUrl: '' }) as unknown as ScanCardProps

const rendre = (attachees: ScanCardProps[]) =>
  render(
    <Unite
      unite={{ cle: 'u', carte: carte(1, 'State of Flow', 'support'), attachees } as unknown as UniteAffichee}
      interactifs={new Map()}
      effets={new Map()}
      ouvrirPile={() => undefined}
      bloquerActionsPassives={false}
    />
  )

describe('une pile sous une carte se lit comme une pile', () => {
  it('deux événements empilés : marqués « empilée » et comptés sur le porteur', () => {
    const { container } = rendre([carte(2, 'Augmented Blow', 'event'), carte(3, 'Chi Jabs', 'event')])
    expect(container.querySelectorAll('.est-attachee.est-empilee')).toHaveLength(2)
    const pastille = container.querySelector('.pile-sous-carte')
    expect(pastille).not.toBeNull()
    expect(pastille?.textContent).toContain('2')
    expect(pastille?.getAttribute('aria-label')).toMatch(/2/)
  })

  it('une vraie amélioration reste une amélioration : ni marque ni pastille', () => {
    const { container } = rendre([carte(4, 'Stark Nunchaku', 'upgrade')])
    expect(container.querySelectorAll('.est-attachee')).toHaveLength(1)
    expect(container.querySelector('.est-empilee')).toBeNull()
    expect(container.querySelector('.pile-sous-carte')).toBeNull()
  })

  it('mélange : seule la pile est comptée', () => {
    const { container } = rendre([carte(2, 'Augmented Blow', 'event'), carte(4, 'Stark Nunchaku', 'upgrade')])
    expect(container.querySelectorAll('.est-empilee')).toHaveLength(1)
    expect(container.querySelector('.pile-sous-carte')?.textContent).toContain('1')
  })
})
