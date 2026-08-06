// Le texte FR de repli ne doit apparaitre QUE la ou il manque un scan francais.
// Sur une carte deja en francais il ferait doublon avec l'image, et sur une
// carte fan-made il n'existe pas du tout.
import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import { ApercuMarvelcdb } from './Board'
import { CLE_SCANS_FR } from './scans-fr'
import { CODES_SCAN_FR } from './scans-fr-liste'
import { TEXTES_FR } from './textes-fr'

const AVEC_SCAN = '01001a'
const SANS_SCAN = '01043b'

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

  it('n affiche rien pour une carte inconnue du dictionnaire', () => {
    render(<ApercuMarvelcdb codeCarte={'75001a'} />)
    expect(screen.queryByText(/Action de héros de repli/)).not.toBeInTheDocument()
  })
})
