// Le LISERE DE L'IDENTITE d'un héros en Épuré (18/10/2026) : un dégradé de ses trois couleurs de palette
// (`data/palettes-heros.json` + corrections), comme une carte Dual, tel quel : même une couleur presque noire
// (Black Widow) reste telle que choisie, sur décision de l'utilisateur.
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { render } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { ScanCard } from '../components/ScanCard'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { couleursDeHeros, degradeDeHeros, oublierPalettes, palettes } from './halo-heros'
import { carteSurTable } from './plateau-de-test'

const ici = dirname(fileURLToPath(import.meta.url))
const contexte = () => ({ playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })

afterEach(() => {
  oublierPalettes()
  vi.unstubAllGlobals()
})

describe('degradeDeHeros', () => {
  it('trois couleurs : un dégradé de gauche à droite, dans l ordre de la palette', () => {
    expect(degradeDeHeros([[22, 30, 105], [136, 24, 26], [29, 23, 23]])).toBe(
      'linear-gradient(90deg, rgb(22,30,105), rgb(136,24,26), rgb(29,23,23))'
    )
  })

  it('deux couleurs : un dégradé à deux (Norman Osborn)', () => {
    expect(degradeDeHeros([[139, 15, 77], [24, 53, 28]])).toBe('linear-gradient(90deg, rgb(139,15,77), rgb(24,53,28))')
  })

  it('une seule couleur : un trait uni, deux fois la même pour que le dégradé reste valide', () => {
    expect(degradeDeHeros([[1, 2, 3]])).toBe('linear-gradient(90deg, rgb(1,2,3), rgb(1,2,3))')
  })

  it('sans palette : rien', () => {
    expect(degradeDeHeros(undefined)).toBeUndefined()
    expect(degradeDeHeros([])).toBeUndefined()
  })
})

describe('l identite porte son liseré une fois les palettes chargées', () => {
  const charger = async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, json: async () => ({ palettes: { '01001a': [[22, 30, 105], [136, 24, 26], [29, 23, 23]] } }) })))
    await palettes()
  }

  it('avant le chargement : aucun liseré, la carte reste comme avant', () => {
    const carte = carteSurTable(1, '01001a', 'Hero', 'Spider-Man')
    expect(toScanCard(carte, contexte()).lisereHeros).toBeUndefined()
  })

  it('apres : l identité (Hero ou AlterEgo) a son dégradé', async () => {
    await charger()
    expect(couleursDeHeros('01001a')?.length).toBe(3)
    const carte = carteSurTable(1, '01001a', 'Hero', 'Spider-Man')
    expect(toScanCard(carte, contexte()).lisereHeros).toBe('linear-gradient(90deg, rgb(22,30,105), rgb(136,24,26), rgb(29,23,23))')
  })

  it('une carte qui n est pas une identité n en porte pas, même avec le meme card_id', async () => {
    await charger()
    const carte = carteSurTable(2, '01001a', 'Upgrade', 'Lance-Toile')
    expect(toScanCard(carte, contexte()).lisereHeros).toBeUndefined()
  })

  it('un héros sans palette n a pas de liseré', async () => {
    await charger()
    const carte = carteSurTable(3, '99999a', 'Hero', 'Inconnu')
    expect(toScanCard(carte, contexte()).lisereHeros).toBeUndefined()
  })
})

describe('ScanCard, liseré de l identite', () => {
  it('pose la classe et la variable CSS, rien sans liseré', () => {
    const avec = render(<ScanCard id="1" name="Spider-Man" kind="hero" imageUrl="/scan/01001a" lisereHeros="linear-gradient(90deg, red, blue)" />)
    const racine = avec.container.querySelector('.scan-card') as HTMLElement
    expect(racine.classList.contains('est-identite')).toBe(true)
    expect(racine.style.getPropertyValue('--lisere-heros')).toBe('linear-gradient(90deg, red, blue)')
    const sans = render(<ScanCard id="2" name="Rhino" kind="villain" imageUrl="/scan/01095" />)
    expect((sans.container.querySelector('.scan-card') as HTMLElement).classList.contains('est-identite')).toBe(false)
  })

  it('une carte face cachée ne porte jamais de liseré (son identité ne se voit pas)', () => {
    const { container } = render(<ScanCard id="1" name="?" kind="unknown" imageUrl="/scan/x" facedown lisereHeros="linear-gradient(90deg, red, blue)" />)
    expect((container.querySelector('.scan-card') as HTMLElement).classList.contains('est-identite')).toBe(false)
  })
})

describe('affichage-epure.css, liseré de l identite', () => {
  const epure = readFileSync(join(ici, '../../styles/affichage-epure.css'), 'utf8')

  it('l identité a une bordure de 1,5 px dont le fond, étalé dessous, est le dégradé du héros', () => {
    expect(epure).toContain('html[data-epure] .scan-card.est-identite .scan-frame')
    expect(epure).toContain('background-image: var(--lisere-heros)')
  })
})
