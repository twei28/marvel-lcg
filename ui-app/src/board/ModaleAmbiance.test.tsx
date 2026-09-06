// Ce que ces cas protègent : une ambiance qui s'allume TOUTE SEULE. Le plateau
// passait en noir et blanc sans un mot, et le joueur n'avait aucun moyen de
// savoir ni pourquoi ni comment revenir en arrière.
//
// Le piège central est la distinction des trois états d'ApercuMeteo :
// `undefined` (Auto, les cartes décident) n'est pas `[]` (Aucun, le vide
// imposé). Le refus du joueur vaut `[]` : c'est le seul état qui éteint une
// ambiance qu'une carte voudrait allumer. Confondre les deux rendrait le
// « Non » sans effet, et le bug serait invisible en test comme en jeu.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { ModaleAmbiance } from './ModaleAmbiance'
import { CLE_AMBIANCE_DEMANDE } from './moteur'
import { CLE_TUTORIEL } from './CoucheCoach'
import type { ApercuMeteo } from './CoucheMeteo'
import type { World } from './world'

const carte = (cardId: string, nom: string) => ({
  id: 1,
  card_id: cardId,
  card_type: 'Support',
  name: nom,
  bind_object_id: 0,
})

/** Un monde minimal : seules les zones qui comptent pour le cas sont remplies. */
const monde = (zones: Record<string, unknown>): World => zones as unknown as World

/** Le décor du Mojoverse qui passe le plateau en noir et blanc. */
const AVEC_DECOR = monde({ area_environment: [carte('39035', 'Dial M for Mojo')] })
/** Un autre décor, pour vérifier qu'on ne redemande pas à la carte suivante. */
const AUTRE_DECOR = monde({ area_environment: [carte('45127', 'The Savage Land')] })
const SANS_DECOR = monde({ area_environment: [carte('01034', 'Toile résistante')] })

function poser(options: { monde?: World; ambianceActive?: boolean; apercu?: ApercuMeteo } = {}) {
  const reglerApercu = vi.fn<(valeur: ApercuMeteo) => void>()
  const rendu = render(
    <ModaleAmbiance
      monde={options.monde ?? AVEC_DECOR}
      ambianceActive={options.ambianceActive ?? true}
      apercu={options.apercu}
      reglerApercu={reglerApercu}
    />
  )
  return { reglerApercu, rendu }
}

const cliquer = async (nom: string | RegExp) => {
  await act(async () => {
    screen.getByRole('button', { name: nom }).click()
  })
}

const cocher = async () => {
  await act(async () => {
    screen.getByRole('checkbox').click()
  })
}

const modaleVisible = () => screen.queryByRole('alertdialog') !== null

beforeEach(() => {
  window.localStorage.clear()
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('quand la modale se montre', () => {
  it('nomme la carte qui allume l ambiance et l effet obtenu', () => {
    poser()
    expect(modaleVisible()).toBe(true)
    expect(screen.getByText('Dial M for Mojo')).toBeTruthy()
    expect(screen.getByText(/Noir et blanc/)).toBeTruthy()
  })

  it('dit où reprendre la main', () => {
    poser()
    expect(screen.getByText(/Aperçu d’ambiance/)).toBeTruthy()
  })

  it('ne dit rien quand aucune carte n allume d ambiance', () => {
    poser({ monde: SANS_DECOR })
    expect(modaleVisible()).toBe(false)
  })

  it('ne dit rien quand l interrupteur général de l ambiance est coupé', () => {
    // Le joueur a déjà tout coupé : lui demander s'il veut une ambiance
    // serait absurde.
    poser({ ambianceActive: false })
    expect(modaleVisible()).toBe(false)
  })

  it('ne dit rien en mode « Aucun » : le joueur a déjà décidé', () => {
    poser({ apercu: [] })
    expect(modaleVisible()).toBe(false)
  })

  it('ne dit rien quand des effets sont choisis à la main', () => {
    poser({ apercu: ['rain', 'fog'] })
    expect(modaleVisible()).toBe(false)
  })

  it('ne dit rien pendant le mode Découverte', () => {
    // Une modale de plus par-dessus un tutoriel qui en affiche déjà une est
    // du bruit : la leçon « le panneau ⚙ » montre justement ce réglage.
    window.localStorage.setItem(CLE_TUTORIEL, 'mulligan')
    poser()
    expect(modaleVisible()).toBe(false)
  })

  it('ne demande qu UNE FOIS par partie, même si un autre décor arrive', async () => {
    // Un scénario Mojoverse enchaîne les décors : une question par carte
    // serait insupportable.
    const { rendu } = poser()
    await cliquer(/Oui/)
    expect(modaleVisible()).toBe(false)
    rendu.rerender(
      <ModaleAmbiance monde={AUTRE_DECOR} ambianceActive apercu={undefined} reglerApercu={vi.fn()} />
    )
    expect(modaleVisible()).toBe(false)
  })
})

describe('ce que font les deux boutons', () => {
  it('« Oui » laisse l ambiance s allumer sans toucher au réglage', async () => {
    // En mode Auto l'ambiance est DÉJÀ allumée : accepter, c'est ne rien
    // changer. Toucher à l'aperçu ferait passer le réglage de « Auto » à une
    // liste figée, et la carte suivante n'allumerait plus rien.
    const { reglerApercu } = poser()
    await cliquer(/Oui/)
    expect(reglerApercu).not.toHaveBeenCalled()
    expect(modaleVisible()).toBe(false)
  })

  it('« Non » éteint TOUTES les ambiances, pas seulement celle de la carte', async () => {
    // `[]` et non `undefined` : c'est le seul état qui impose le vide même
    // quand une carte voudrait allumer quelque chose.
    const { reglerApercu } = poser()
    await cliquer(/Non/)
    expect(reglerApercu).toHaveBeenCalledWith([])
    expect(modaleVisible()).toBe(false)
  })

  it('sans la case cochée, rien n est écrit : la question revient la partie d après', async () => {
    poser()
    await cliquer(/Non/)
    expect(window.localStorage.getItem(CLE_AMBIANCE_DEMANDE)).toBeNull()
  })
})

describe('la case « ne plus me montrer ça »', () => {
  it('cochée avec « Non », gèle le refus et n affiche plus la modale', async () => {
    const { reglerApercu } = poser()
    await cocher()
    await cliquer(/Non/)
    expect(window.localStorage.getItem(CLE_AMBIANCE_DEMANDE)).toBe('jamais')
    expect(reglerApercu).toHaveBeenCalledWith([])

    // Une NOUVELLE partie : le composant est remonté de zéro.
    const suivante = poser()
    expect(modaleVisible()).toBe(false)
    // Et l'ambiance reste éteinte, sans quoi le refus n'aurait tenu qu'une
    // partie alors que la case dit le contraire.
    expect(suivante.reglerApercu).toHaveBeenCalledWith([])
  })

  it('cochée avec « Oui », laisse l ambiance s allumer sans plus rien demander', async () => {
    const { reglerApercu } = poser()
    await cocher()
    await cliquer(/Oui/)
    expect(window.localStorage.getItem(CLE_AMBIANCE_DEMANDE)).toBe('toujours')
    expect(reglerApercu).not.toHaveBeenCalled()

    const suivante = poser()
    expect(modaleVisible()).toBe(false)
    // Rien n'est forcé : le mode Auto laisse les cartes décider, donc
    // l'ambiance s'allume comme avant.
    expect(suivante.reglerApercu).not.toHaveBeenCalled()
  })

  it('prévient le panneau Options du réglage figé', async () => {
    // Sans ce signal, la ligne « Demande d’ambiance » afficherait « Demander »
    // alors que la case vient d'écrire « jamais », et le joueur croirait la
    // question encore armée.
    const onReponseFigee = vi.fn()
    render(
      <ModaleAmbiance
        monde={AVEC_DECOR}
        ambianceActive
        apercu={undefined}
        reglerApercu={vi.fn()}
        onReponseFigee={onReponseFigee}
      />
    )
    await cocher()
    await cliquer(/Oui/)
    expect(onReponseFigee).toHaveBeenCalledWith('toujours')
  })

  it('ne prévient personne quand la case n est pas cochée', async () => {
    const onReponseFigee = vi.fn()
    render(
      <ModaleAmbiance
        monde={AVEC_DECOR}
        ambianceActive
        apercu={undefined}
        reglerApercu={vi.fn()}
        onReponseFigee={onReponseFigee}
      />
    )
    await cliquer(/Non/)
    expect(onReponseFigee).not.toHaveBeenCalled()
  })

  it('se décoche comme elle se coche', async () => {
    poser()
    await cocher()
    await cocher()
    await cliquer(/Non/)
    expect(window.localStorage.getItem(CLE_AMBIANCE_DEMANDE)).toBeNull()
  })
})

describe('quand le stockage refuse', () => {
  /** Un localStorage qui lève à chaque accès, comme Safari en navigation privée. */
  function stockageQuiLeve() {
    const refuser = () => {
      throw new Error('stockage refusé')
    }
    vi.stubGlobal('localStorage', {
      get length(): number {
        return refuser()
      },
      key: refuser,
      getItem: refuser,
      setItem: refuser,
      removeItem: refuser,
      clear: refuser,
    } as unknown as Storage)
  }

  it('ne fait pas tomber le plateau et pose quand même la question', () => {
    stockageQuiLeve()
    expect(() => poser()).not.toThrow()
    expect(modaleVisible()).toBe(true)
  })

  it('ne fait pas tomber le plateau quand la case cochée ne peut pas être écrite', async () => {
    stockageQuiLeve()
    const { reglerApercu } = poser()
    await cocher()
    await cliquer(/Non/)
    // Le refus vaut au moins pour la partie en cours : c'est tout ce qu'on
    // peut promettre sans stockage.
    expect(reglerApercu).toHaveBeenCalledWith([])
    expect(modaleVisible()).toBe(false)
  })
})
