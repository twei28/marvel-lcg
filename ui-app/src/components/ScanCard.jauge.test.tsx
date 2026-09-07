// Rendu de la BANDE de jauge et de la PULSATION d'alerte.
//
// La bande vit HORS de `.scan-frame`, comme le marqueur de morsure : le cadre
// rogne son contenu. Elle est posee SOUS la carte : le long du bord gauche, les
// cartes voisines d'une meme rangee la serraient de trop pres pour qu'on sache
// a qui elle appartenait.
//
// La pulsation est une ALARME : elle ne se declenche que si la carte y a droit
// (`alarme`), a deux niveaux, et jamais toute seule sur une carte tranquille.
import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { ScanCard } from './ScanCard'
import type { CardGauge } from './ScanCard'

function rendre(jauge: CardGauge) {
  return render(<ScanCard id="1" name="Spider-Man" kind="hero" imageUrl="" jauge={jauge} />)
}

const pv = (remplissage: number, alarme = true): CardGauge => ({
  remplissage,
  genre: 'pv',
  alarme,
})
const menace = (remplissage: number, alarme = true): CardGauge => ({
  remplissage,
  genre: 'menace',
  alarme,
})

/** Teinte HSL posee par le composant, en degres. */
function teinteDe({ container }: { container: HTMLElement }): number {
  return Number(
    container
      .querySelector<HTMLElement>('.jauge-remplissage')
      ?.style.getPropertyValue('--jauge-teinte')
      .replace('deg', '')
  )
}

describe('bande de jauge', () => {
  it('peint la bande sur la largeur du remplissage', () => {
    // La bande est HORIZONTALE, posee sous la carte : c'est sa largeur qui suit
    // la valeur. A gauche le plein, a droite le vide.
    const { container } = rendre(pv(0.4))
    const peinture = container.querySelector<HTMLElement>('.jauge-remplissage')
    expect(peinture?.style.width).toBe('40%')
    expect(peinture?.style.height).toBe('')
  })

  it('pose la bande hors du cadre, qui rogne son contenu', () => {
    const { container } = rendre(pv(1))
    expect(container.querySelector('.jauge-carte')?.parentElement).toHaveClass('scan-visuel')
  })

  it('verdit une carte intacte et rougit une carte a l agonie', () => {
    expect(teinteDe(rendre(pv(1)))).toBeGreaterThan(100)
    expect(teinteDe(rendre(pv(0)))).toBe(0)
  })

  it('a deja vire au rouge quand il ne reste qu un tiers des PV', () => {
    // Une interpolation lineaire de 140 a 0 traine dans le jaune : un
    // personnage a 1/3 de PV sortait en jaune dore, ce qui se lit « ca va ».
    // La teinte suit donc une echelle qui tient le vert haut puis plonge.
    expect(teinteDe(rendre(pv(0.33)))).toBeLessThan(40)
  })

  it('tient le vert franc tant que la carte est peu entamee', () => {
    expect(teinteDe(rendre(pv(0.75)))).toBeGreaterThan(90)
  })

  it('lit la menace a l envers : pleine, elle est rouge', () => {
    const { container } = rendre(menace(1))
    const teinte = container
      .querySelector<HTMLElement>('.jauge-remplissage')
      ?.style.getPropertyValue('--jauge-teinte')
    expect(teinte).toBe('0deg')
  })

  // La menace ne passe JAMAIS par le vert (decide avec l'utilisateur, 7
  // septembre 2026) : une barre verte sous une manigance se lisait comme des
  // PV. Elle va du jaune Pepper Potts a l'orange puis au rouge.
  it('tient la menace basse en jaune, jamais en vert', () => {
    const teinte = teinteDe(rendre(menace(0.1)))
    expect(teinte).toBeGreaterThanOrEqual(34)
    expect(teinte).toBeLessThanOrEqual(45)
  })

  it('passe la menace a mi-chemin en orange', () => {
    const teinte = teinteDe(rendre(menace(0.5)))
    expect(teinte).toBeGreaterThanOrEqual(14)
    expect(teinte).toBeLessThanOrEqual(30)
  })

  it('distingue les deux genres par une classe', () => {
    const { container } = rendre(menace(0.5))
    expect(container.querySelector('.jauge-carte')).toHaveClass('jauge-menace')
  })

  it('ne rend aucune bande sans jauge', () => {
    const { container } = render(<ScanCard id="1" name="Spider-Man" kind="hero" imageUrl="" />)
    expect(container.querySelector('.jauge-carte')).toBeNull()
  })

  it('laisse la pastille chiffree parler pour les lecteurs d ecran', () => {
    const { container } = rendre(pv(0.4))
    expect(container.querySelector('.jauge-carte')?.getAttribute('aria-hidden')).toBe('true')
  })
})

describe('pulsation d alerte', () => {
  const classes = (jauge: CardGauge) => {
    const { container } = rendre(jauge)
    return container.querySelector('.scan-card')!.className
  }

  it('laisse tranquille une carte en bonne sante', () => {
    expect(classes(pv(0.8))).not.toMatch(/a-alerte/)
  })

  it('respire doucement des la moitie des PV perdue', () => {
    expect(classes(pv(0.5))).toContain('a-alerte-douce')
  })

  it('passe en alerte forte au quart des PV restants', () => {
    const c = classes(pv(0.25))
    expect(c).toContain('a-alerte-forte')
    expect(c).not.toContain('a-alerte-douce')
  })

  it('respire doucement quand la menace atteint 60 %', () => {
    expect(classes(menace(0.6))).toContain('a-alerte-douce')
  })

  it('passe en alerte forte quand la menace atteint 85 %', () => {
    expect(classes(menace(0.85))).toContain('a-alerte-forte')
  })

  it('se tait sur une carte sans droit d alarme, meme a l agonie', () => {
    expect(classes(pv(0.05, false))).not.toMatch(/a-alerte/)
  })

  it('se tait sur un complot du joueur, meme a menace pleine', () => {
    expect(classes(menace(1, false))).not.toMatch(/a-alerte/)
  })
})

describe('le texte dans la bande', () => {
  it('ecrit le texte de la jauge dans la bande', () => {
    const { container } = render(
      <ScanCard id="1" name="Spider-Man" kind="hero" imageUrl="" jauge={{ ...pv(0.5), texte: '6 / 12' }} />
    )
    expect(container.querySelector('.jauge-texte')?.textContent).toBe('6 / 12')
  })

  it('n affiche plus la pastille ronde quand la bande porte le chiffre', () => {
    const { container } = render(
      <ScanCard
        id="1"
        name="Spider-Man"
        kind="hero"
        imageUrl=""
        allyHp="6/12"
        jauge={{ ...pv(0.5), texte: '6 / 12' }}
      />
    )
    expect(container.querySelector('.ally-hp-badge')).toBeNull()
  })

  it('garde la pastille quand il n y a pas de bande', () => {
    const { container } = render(<ScanCard id="1" name="Spider-Man" kind="hero" imageUrl="" allyHp="6" />)
    expect(container.querySelector('.ally-hp-badge')).not.toBeNull()
  })
})
