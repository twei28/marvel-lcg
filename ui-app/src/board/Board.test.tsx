// Le texte FR de repli ne doit apparaitre QUE la ou il manque un scan francais.
// Sur une carte deja en francais il ferait doublon avec l'image.
//
// Les cartes des packs FAN-MADE sont le cas qui compte le plus : elles n'auront
// jamais de scan francais ni de page marvelcdb, donc ce bloc est le seul
// francais que le joueur verra dessus.
import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import { ApercuMarvelcdb } from './Board'
import { CLE_SCANS_FR } from './scans-fr'
import { CODES_SCAN_FR } from './scans-fr-liste'
import { TEXTES_FR } from './textes-fr'
import { TEXTES_FR_FANMADE } from './textes-fr-fanmade'

const AVEC_SCAN = '01001a'
const SANS_SCAN = '01043b'
const FANMADE = '75001a'
/** Code au bon format, absent des deux dictionnaires : rien ne doit s'afficher. */
const INCONNU = '99999'

beforeEach(() => {
  window.localStorage.clear()
  ;(CODES_SCAN_FR as Set<string>).clear()
  ;(CODES_SCAN_FR as Set<string>).add(AVEC_SCAN)
  ;(TEXTES_FR as Record<string, string | undefined>)[SANS_SCAN] = 'Action de héros de repli'
})

describe('ApercuMarvelcdb', () => {
  it('affiche le texte francais quand la carte n a pas de scan francais', () => {
    render(<ApercuMarvelcdb codeCarte={SANS_SCAN} />)
    expect(screen.getByText(/Action de héros de repli/)).toBeInTheDocument()
  })

  it('n affiche rien quand la carte a deja son scan francais', () => {
    render(<ApercuMarvelcdb codeCarte={AVEC_SCAN} />)
    expect(screen.queryByText(/Action de héros de repli/)).not.toBeInTheDocument()
  })

  it('n affiche rien quand l option scans FR est coupee', () => {
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    render(<ApercuMarvelcdb codeCarte={SANS_SCAN} />)
    expect(screen.queryByText(/Action de héros de repli/)).not.toBeInTheDocument()
  })

  it('n affiche rien pour une carte inconnue des deux dictionnaires', () => {
    const { container } = render(<ApercuMarvelcdb codeCarte={INCONNU} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('affiche le texte francais traduit a la main d une carte fan-made', () => {
    expect(TEXTES_FR_FANMADE[FANMADE]).toBeDefined()
    render(<ApercuMarvelcdb codeCarte={FANMADE} />)
    expect(screen.getByText(/Armée imbattable/)).toBeInTheDocument()
  })

  it('ne montre aucune carte fan-made quand l option est coupee', () => {
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    const { container } = render(<ApercuMarvelcdb codeCarte={FANMADE} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('rend les sauts de ligne visibles au lieu de coller les capacites', () => {
    ;(TEXTES_FR as Record<string, string | undefined>)[SANS_SCAN] =
      'Première capacité.\nSeconde capacité.'
    const { container } = render(<ApercuMarvelcdb codeCarte={SANS_SCAN} />)
    expect(container.querySelectorAll('br')).toHaveLength(1)
  })
})
