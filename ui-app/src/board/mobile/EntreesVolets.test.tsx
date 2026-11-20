// Les volets du bord droit rangés dans le menu « … » du téléphone (16/11/2026, demande de l'utilisateur) : une ligne par languette présente,
// un clic de la ligne clique la languette, le menu se referme, les non-lus du tchat sont repris.
import { fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { EntreesVolets, lireEntrees } from './EntreesVolets'
import { BandeauPortrait } from './BandeauPortrait'
import type { World } from '../world'

const monde = { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [{ area_hero: [{ name: '* Steve Rogers' }] }] } as unknown as World

function poserLanguettes(avecFeuillets: boolean, nonLus?: string) {
  const clics: string[] = []
  const ajouter = (classe: string, texte: string, pastille?: string) => {
    const b = document.createElement('button')
    b.className = classe
    const span = document.createElement('span')
    span.className = classe + '-texte'
    span.textContent = texte
    b.append(span)
    if (pastille) {
      const p = document.createElement('span')
      p.className = 'volet-tchat-pastille'
      p.textContent = pastille
      b.append(p)
    }
    b.addEventListener('click', () => clics.push(classe))
    document.body.append(b)
  }
  ajouter('volet-aide-languette', 'Aide')
  if (avecFeuillets) ajouter('volet-feuillets-languette', 'Feuillets')
  ajouter('volet-tchat-languette', 'Tchat', nonLus)
  ajouter('volet-journal-languette', 'Journal')
  return clics
}

/** La LIGNE du menu (pas la languette masquee, qui est elle aussi un bouton de la page). */
const ligne = (nom: string): HTMLElement => {
  const trouve = [...document.querySelectorAll<HTMLElement>('.bh-volet')].find((b) => b.textContent?.startsWith(nom))
  if (!trouve) throw new Error(`pas de ligne « ${nom} »`)
  return trouve
}

beforeEach(() => {
  document.body.classList.add('mode-plateau-portrait')
})

afterEach(() => {
  document.body.innerHTML = ''
  document.body.className = ''
})

describe('EntreesVolets', () => {
  it('lit les languettes presentes, dans l’ordre Aide, Feuillets, Tchat, Journal, et saute celles qui n’existent pas', () => {
    poserLanguettes(false)
    expect(lireEntrees().map((e) => e.libelle)).toEqual(['Aide', 'Tchat', 'Journal'])
    document.body.innerHTML = ''
    poserLanguettes(true)
    expect(lireEntrees().map((e) => e.libelle)).toEqual(['Aide', 'Feuillets', 'Tchat', 'Journal'])
  })

  it('une ligne clique la languette de son volet', () => {
    const clics = poserLanguettes(false)
    render(<EntreesVolets />)
    fireEvent.click(ligne('Journal'))
    expect(clics).toEqual(['volet-journal-languette'])
  })

  it('reprend les messages non lus du tchat sur sa ligne', () => {
    poserLanguettes(false, '3')
    render(<EntreesVolets />)
    expect(ligne('Tchat').textContent).toContain('3')
  })

  it('ne dessine rien quand aucun volet n’existe', () => {
    const { container } = render(<EntreesVolets />)
    expect(container.querySelector('.bh-volet')).toBeNull()
  })
})

describe('le menu « … » se referme sur une ligne de volet', () => {
  it('un clic sur une ligne marquee data-ferme-menu ferme la feuille ; une autre ligne la laisse ouverte', () => {
    poserLanguettes(false)
    render(
      <BandeauPortrait
        monde={monde}
        menu={
          <div className="board-actions">
            <EntreesVolets />
            <button type="button" className="bh-bouton">Options</button>
          </div>
        }
      />
    )
    fireEvent.click(screen.getByRole('button', { name: 'Menu' }))
    expect(document.querySelector('.portrait-menu')).not.toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Options' }))
    expect(document.querySelector('.portrait-menu'), 'Options laisse le menu ouvert').not.toBeNull()
    fireEvent.click(ligne('Tchat'))
    expect(document.querySelector('.portrait-menu'), 'une ligne de volet referme le menu').toBeNull()
  })
})
