// Signalement Yarro n°45 : du monde du moteur jusqu'a ce qui est DESSINE
// (etape 8 bis de PROCESSUS-CARTE). Le compteur seul ne prouve pas que le
// jeton est a l'ecran.
import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { ScanCard } from '../components/ScanCard'
import { construirePlateau } from './zones'
import { catalogueVide } from './catalogue'
import { carteSurTable, siege, tableAvec } from './plateau-de-test'

describe('le jeton d acceleration d Ivan Banionis, a l ecran', () => {
  it('est dessine sur la carte du sbire', () => {
    const ivan = carteSurTable(78, '60200', 'Minion', 'Ivan Banionis', {
      info: { k_acceleration_token: 1, max_health: 5, health: 5 },
    })
    const plateau = construirePlateau(tableAvec(siege({ engaged_enemies: [ivan] })), {
      playerId: 0,
      catalogue: catalogueVide,
    })
    const carte = plateau.emplacements
      .flatMap((e) => e.groupes.flat())
      .find((u) => u.carte.id === '78')?.carte
    expect(carte).toBeDefined()
    const { container } = render(<ScanCard {...carte!} />)
    expect(container.querySelector('.jeton-acceleration')).not.toBeNull()
  })
})
