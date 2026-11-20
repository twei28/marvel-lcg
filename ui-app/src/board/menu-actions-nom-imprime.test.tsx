// Rapport nicodede62 #158 (19/11/2026) : dans le menu de Captain America, le pouvoir restait « I Can Do This All Day! » en anglais.
import type { ComponentProps } from 'react'
import { cleanup, render } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import { MenuActionsCarte } from './MenuActionsCarte'

;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = class { observe() {} unobserve() {} disconnect() {} }
afterEach(cleanup)

const ANGLAIS = '"I Can Do This All Day!" — Action: Discard a card from your hand → ready Captain America. (Limit once per round.)'
const TEXTE_FR = '« Je peux faire ça toute la journée ! » — Action : défaussez 1 carte de votre main → redressez Captain America. (Limite d’une fois par round.)'

describe('menu des actions : le nom imprimé du pouvoir', () => {
  it('« I Can Do This All Day! » s’écrit avec son nom français', () => {
    const option = { id: 9, bind_id: 1, bind_player_id: 0, name: 'I_Can_Do_This_All_Day!', failure_reason: '', target_num_range: [0, 0],
      all_legal_targets: [], target_payment: {}, is_search: false }
    const changer = { ...option, id: 10, name: 'Change_Form' }
    const rendu = render(
      <MenuActionsCarte
        {...({
          carte: { id: '1', name: 'Captain America', kind: 'hero' },
          carteMonde: { id: 1, card_id: '03001a' },
          options: [option, changer], cartesParId: new Map(), catalogue: { texte: () => ANGLAIS }, choisirOption: () => {}, fermer: () => {}, playerId: 0,
          idsAffiches: new Set(), affichage: 'detailed', texteDeCarte: () => TEXTE_FR,
        } as unknown as ComponentProps<typeof MenuActionsCarte>)}
      />
    )
    expect(rendu.container.textContent).toContain('Je peux faire ça toute la journée !')
    expect(rendu.container.textContent).not.toContain('All Day')
    // « Changer de forme » n'est pas une capacité nommée de la carte : il garde son nom (régression vue sur Tony Stark)
    expect(rendu.container.textContent).toContain('Changer de forme')
  })
})
