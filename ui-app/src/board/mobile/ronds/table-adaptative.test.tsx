// La table en ronds en « grilles par zone » (27/10/2026, maquette dispo-ronds.html) : chaque zone rend ses ronds en
// colonnes, masque les zones vides, et pagine le surplus par ses fleches ◂ ▸. jsdom n'a pas de mise en page : on verifie
// la STRUCTURE rendue (zones, colonnes, fleches) et le comportement des fleches, pas les pixels. Avant, cette table etait
// « adaptative » (TableRonds mesurait son conteneur pour calculer un diametre et un nombre de colonnes variables) ; ce
// modele est abandonne, donc ces tests sont reecrits pour la nouvelle disposition.
import { fireEvent, render } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import type { ScanCardProps } from '../../../components/ScanCard'
import type { UniteAffichee } from '../../zones'
import type { BandesPortrait } from '../bandes-portrait'
import type { DecorRonds } from './Rond'
import { TableRonds } from './TableRonds'

const carte = (id: string, kind: ScanCardProps['kind'], reste: Partial<ScanCardProps> = {}): ScanCardProps => ({
  id,
  name: `Carte ${id}`,
  kind,
  imageUrl: `/scan/${id}.jpg`,
  ...reste,
})
const unite = (id: string, kind: ScanCardProps['kind']): UniteAffichee => ({ cle: `u-${id}`, carte: carte(id, kind), attachees: [] })
const plusieurs = (prefixe: string, kind: ScanCardProps['kind'], n: number): UniteAffichee[] =>
  Array.from({ length: n }, (_, i) => unite(`${prefixe}${i}`, kind))
const bandes = (reste: Partial<BandesPortrait> = {}): BandesPortrait => ({
  vilain: { epinglee: unite('rhino', 'villain'), unites: [] },
  manigances: { epinglee: unite('effraction', 'main-scheme'), unites: [] },
  engages: { unites: [] },
  heros: { epinglee: unite('spidey', 'hero'), unites: [] },
  soutiens: { unites: [] },
  ameliorations: { unites: [] },
  main: [],
  piles: [],
  ...reste,
})
const decor = (): DecorRonds => ({ interactifs: new Map(), effets: new Map(), ouvrirPile: vi.fn(), ouvrirCarte: vi.fn(), agir: vi.fn() })

function table(b: BandesPortrait) {
  const { container } = render(
    <div className="portrait-table">
      <TableRonds bandes={b} decor={decor()} />
    </div>,
  )
  const zone = (cle: string) => container.querySelector<HTMLElement>(`[data-zone="${cle}"]`)
  return { container, zone }
}

describe('grilles par zone', () => {
  it('The Hunger Core : 4 mechants en 2x2 (2 colonnes), 1 manigance (1 colonne), heros, 3 cartes en jeu (3 colonnes)', () => {
    const { zone } = table(
      bandes({
        vilain: { epinglee: unite('core', 'villain'), unites: plusieurs('meta', 'villain', 3) },
        manigances: { epinglee: unite('infection', 'main-scheme'), unites: [] },
        soutiens: { unites: plusieurs('soutien', 'support', 3) },
      }),
    )
    expect(zone('vilain')!.querySelectorAll('.ronds-colonne')).toHaveLength(2)
    expect(zone('vilain')!.querySelectorAll('.rond')).toHaveLength(4)
    expect(zone('manigances')!.querySelectorAll('.ronds-colonne')).toHaveLength(1)
    expect(zone('heros')!.querySelectorAll('.rond')).toHaveLength(1)
    expect(zone('enJeu')!.querySelectorAll('.ronds-colonne')).toHaveLength(3)
    expect(zone('enJeu')!.querySelectorAll('.rond')).toHaveLength(3)
  })

  it('une zone a 4 ronds ou moins (grille 2x2 ou 3x2 pleine) n\'a pas de fleches', () => {
    const { zone } = table(bandes({ engages: { unites: plusieurs('sbire', 'minion', 4) } }))
    expect(zone('sbires')!.querySelector('.ronds-fleches')).toBeNull()
  })
})

describe('fleches de surplus (pagination par colonne, par zone)', () => {
  it('5 sbires : une paire de fleches apparait, ◂ est desactivee au depart ; ▸ fait defiler d\'une colonne', () => {
    const { zone } = table(bandes({ engages: { unites: plusieurs('sbire', 'minion', 5) } }))
    const fleches = zone('sbires')!.querySelector('.ronds-fleches')!
    expect(fleches).not.toBeNull()
    const [reculer, avancer] = Array.from(fleches.querySelectorAll('button')) as [HTMLButtonElement, HTMLButtonElement]
    expect(reculer.disabled).toBe(true) // page 0 : rien a gauche
    expect(avancer.disabled).toBe(false)
    // 5 sbires en 2x2 = 3 colonnes ; la grille en montre 2.
    expect(zone('sbires')!.querySelectorAll('.ronds-colonne')).toHaveLength(2)
    fireEvent.click(avancer)
    // On a avance d'une colonne : ◂ s'active, ▸ se desactive (derniere colonne atteinte).
    const [reculer2, avancer2] = Array.from(zone('sbires')!.querySelectorAll('.ronds-fleches button')) as [HTMLButtonElement, HTMLButtonElement]
    expect(reculer2.disabled).toBe(false)
    expect(avancer2.disabled).toBe(true)
    expect(zone('sbires')!.querySelectorAll('.ronds-colonne')).toHaveLength(2)
  })

  it('la pagination est INDEPENDANTE par zone : avancer les sbires ne touche pas les cartes en jeu', () => {
    const { zone } = table(
      bandes({ engages: { unites: plusieurs('sbire', 'minion', 5) }, soutiens: { unites: plusieurs('soutien', 'support', 7) } }),
    )
    const avancerSbires = zone('sbires')!.querySelectorAll('.ronds-fleches button')[1] as HTMLButtonElement
    const avancerEnJeu = zone('enJeu')!.querySelector('.ronds-fleches button')!
    expect(avancerEnJeu).not.toBeNull()
    fireEvent.click(avancerSbires)
    // Les cartes en jeu n'ont pas bouge : leur ◂ reste desactivee.
    const reculerEnJeu = zone('enJeu')!.querySelectorAll('.ronds-fleches button')[0] as HTMLButtonElement
    expect(reculerEnJeu.disabled).toBe(true)
  })
})

describe('zones et rangees vides', () => {
  it('une zone vide est masquee et sa voisine occupe la rangee seule (sans separateur)', () => {
    const { container, zone } = table(bandes({ engages: { unites: plusieurs('sbire', 'minion', 3) } }))
    expect(zone('allies')).toBeNull() // pas d'allie : la zone n'est pas rendue
    expect(zone('sbires')).not.toBeNull()
    const rangeeAllies = container.querySelector('.ronds-rangee.rangee-allies')!
    expect(rangeeAllies.querySelectorAll('.ronds-zone')).toHaveLength(1)
    expect(rangeeAllies.querySelector('.ronds-separateur')).toBeNull()
  })

  it('une rangee dont les deux zones sont vides disparait entierement', () => {
    const { container } = table(bandes()) // ni allie ni sbire
    expect(container.querySelector('.ronds-rangee.rangee-allies')).toBeNull()
    // Les rangees du mechant (mechant + manigance epingles) et du heros restent.
    expect(container.querySelector('.ronds-rangee.rangee-vilain')).not.toBeNull()
    expect(container.querySelector('.ronds-rangee.rangee-heros')).not.toBeNull()
  })

  it('les deux zones pleines d\'une rangee sont separees par un fin separateur', () => {
    const { container } = table(bandes({ heros: { epinglee: unite('spidey', 'hero'), unites: plusieurs('allie', 'ally', 2) }, engages: { unites: plusieurs('sbire', 'minion', 2) } }))
    const rangeeAllies = container.querySelector('.ronds-rangee.rangee-allies')!
    expect(rangeeAllies.querySelectorAll('.ronds-zone')).toHaveLength(2)
    expect(rangeeAllies.querySelector('.ronds-separateur')).not.toBeNull()
  })
})
