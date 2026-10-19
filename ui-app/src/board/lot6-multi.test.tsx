// Refonte de la phase du méchant, lot 6 (essai, MULTI, 12/10/2026) : qui fait
// avancer (decisions 10, 32, 33), et le pied de la boite qui le montre.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render } from '@testing-library/react'
import { CartouchePhase, type CartouchePhaseProps, type PiedMulti } from './CartouchePhase'
import { CommandesMultiSurTable } from './TableSansModale'
import { DeroulePhase } from './DeroulePhase'
import { publierEtape } from './etape-partagee'
import type { EtapeDeroule } from './deroule-phase'
import { lectureASuivre, lirePolitique, peutAvancer, siegeMeneur, siegesPrets, tousPrets } from './avance-multi'
import type { EtapesLues } from './etape-partagee'

describe('qui donne le rythme', () => {
  it('lirePolitique ne garde que les trois regles', () => {
    expect(lirePolitique('concerne')).toBe('concerne')
    expect(lirePolitique('tous')).toBe('tous')
    expect(lirePolitique('quiconque')).toBe('quiconque')
    expect(lirePolitique('')).toBeUndefined()
    expect(lirePolitique('nimporte')).toBeUndefined()
  })

  it('« concerne » : le joueur vise, sinon le premier joueur', () => {
    expect(siegeMeneur(1, 0)).toBe(1)
    expect(siegeMeneur(undefined, 0)).toBe(0)
    // Klaw attaque J2 : seul J2 avance.
    expect(peutAvancer('concerne', 1, 1, 0)).toBe(true)
    expect(peutAvancer('concerne', 0, 1, 0)).toBe(false)
    // La menace (moment commun) : le premier joueur.
    expect(peutAvancer('concerne', 0, undefined, 0)).toBe(true)
    expect(peutAvancer('concerne', 1, undefined, 0)).toBe(false)
  })

  it('« quiconque » : tout le monde ; pas encore choisi : personne', () => {
    expect(peutAvancer('quiconque', 1, 0, 0)).toBe(true)
    expect(peutAvancer(undefined, 0, 0, 0)).toBe(false)
  })

  it('un meneur inconnu (monde sans jeton) ne fige personne', () => {
    expect(peutAvancer('concerne', 1, undefined, undefined)).toBe(true)
  })
})

describe('ce que l on suit', () => {
  const lues = {
    0: { cle: 'b', t: 10, boosts: 1 },
    1: { cle: 'a', t: 20, boosts: 0 },
  } as unknown as EtapesLues

  it('« concerne » : l etape et les boosts du meneur, rien quand on est le meneur', () => {
    expect(lectureASuivre('concerne', lues, 1, 0)).toMatchObject({ siege: 0, cle: 'b', boosts: 1 })
    expect(lectureASuivre('concerne', lues, 0, 0)).toBeUndefined()
  })

  it('« quiconque » : le plus recent des AUTRES, meme si nous avons republie apres lui', () => {
    expect(lectureASuivre('quiconque', lues, 0, undefined)).toMatchObject({ siege: 1, cle: 'a' })
    // Mesure du 12/10 : J1 clique et valide, J0 republie la meme etape plus tard ;
    // J1 ne doit pas cesser d etre suivi, sinon J0 ne valide jamais (blocage).
    expect(lectureASuivre('quiconque', lues, 1, undefined)).toMatchObject({ siege: 0, cle: 'b' })
    expect(lectureASuivre('quiconque', { 0: { cle: 'b', t: 1 } } as unknown as EtapesLues, 0, undefined)).toBeUndefined()
  })

  it('« tous » : personne ne suit personne', () => {
    expect(lectureASuivre('tous', lues, 0, 0)).toBeUndefined()
  })

  it('« tous » : on avance quand chaque siege est pret pour CETTE etape', () => {
    const prets = { 0: { cle: 'x', t: 1, pret: 'x' }, 1: { cle: 'x', t: 2, pret: 'w' } } as unknown as EtapesLues
    expect(siegesPrets(prets, 'x', [0, 1])).toEqual([0])
    expect(tousPrets(prets, 'x', [0, 1])).toBe(false)
    const tous = { 0: { cle: 'x', t: 1, pret: 'x' }, 1: { cle: 'x', t: 2, pret: 'x' } } as unknown as EtapesLues
    expect(tousPrets(tous, 'x', [0, 1])).toBe(true)
    expect(tousPrets(tous, undefined, [0, 1])).toBe(false)
    expect(tousPrets(tous, 'x', [])).toBe(false)
  })
})

describe('le pied de la boite', () => {
  afterEach(() => cleanup())
  const etape: EtapeDeroule = {
    cle: 'activation:1',
    temps: 'mechant',
    titre: 'attaque',
    regle: 'regle:activations',
    boosts: [],
  } as EtapeDeroule
  const monter = (multi: PiedMulti | undefined, avancer = vi.fn()) => {
    const props = {
      refCartouche: () => {},
      gestes: { onPointerDown: () => {}, onPointerMove: () => {}, onPointerUp: () => {}, onPointerCancel: () => {} },
      etape,
      etapes: [etape],
      index: 0,
      efface: false,
      questionAuJoueur: false,
      avancer,
      multi,
      enAttente: false,
      attendUnAutreJoueur: false,
      defaiteLocale: false,
      boostsMontres: 99,
      tempsParDecision: 0,
      cartesDistribuees: 0,
      essai: true,
    } as unknown as CartouchePhaseProps
    return render(<CartouchePhase {...props} />)
  }

  it('sans multi : le Continuer habituel', () => {
    const { container } = monter(undefined)
    const bouton = container.querySelector('.essai-continuer') as HTMLButtonElement
    expect(bouton.disabled).toBe(false)
    expect(container.querySelector('.essai-multi-attente')).toBeNull()
  })

  it('un autre donne le rythme : meme emplacement, grise, « J2 (Hulk) regarde… », sans Continuer', () => {
    const avancer = vi.fn()
    const { container } = monter({ genre: 'regarde', nom: 'J2 (Hulk)' }, avancer)
    const boutons = [...container.querySelectorAll('.essai-continuer')] as HTMLButtonElement[]
    expect(boutons).toHaveLength(1)
    expect(boutons[0].disabled).toBe(true)
    expect(boutons[0].classList.contains('essai-multi-attente')).toBe(true)
    expect(boutons[0].textContent).toContain('J2 (Hulk) regarde')
    fireEvent.click(boutons[0])
    expect(avancer).not.toHaveBeenCalled()
  })

  it('l hote choisit : trois regles, le clic transmet la regle', () => {
    const choisir = vi.fn()
    const { container } = monter({ genre: 'choix-hote', choisir })
    const options = [...container.querySelectorAll('[data-politique]')] as HTMLButtonElement[]
    expect(options.map((o) => o.dataset.politique)).toEqual(['concerne', 'tous', 'quiconque'])
    fireEvent.click(options[1])
    expect(choisir).toHaveBeenCalledWith('tous')
    expect((container.querySelector('.essai-multi-attente') as HTMLButtonElement).disabled).toBe(true)
  })

  it('les autres attendent le choix de l hote', () => {
    const { container } = monter({ genre: 'attente-choix' })
    expect(container.querySelector('[data-politique]')).toBeNull()
    expect(container.querySelector('.essai-multi-attente')?.textContent).toContain('hôte')
  })

  it('« tout le monde valide » : Pret, puis grise avec le compte ; les pastilles', () => {
    const marquer = vi.fn()
    const pastilles = [
      { nom: 'J1', pret: false },
      { nom: 'J2', pret: true },
    ]
    const { container, unmount } = monter({ genre: 'pret', pret: false, pastilles, marquer })
    const pret = container.querySelector('[data-pret]') as HTMLButtonElement
    expect(pret.textContent).toContain('Prêt')
    fireEvent.click(pret)
    expect(marquer).toHaveBeenCalledTimes(1)
    expect(container.querySelectorAll('.essai-pret')).toHaveLength(2)
    expect(container.querySelectorAll('.essai-pret.est-pret')).toHaveLength(1)
    // Un seul bouton au pied : le Continuer habituel laisse sa place au Pret.
    expect(container.querySelectorAll('.essai-continuer')).toHaveLength(1)
    unmount()
    const { container: c2 } = monter({ genre: 'pret', pret: true, pastilles, marquer })
    const fait = c2.querySelector('[data-pret]') as HTMLButtonElement
    expect(fait.disabled).toBe(true)
    expect(fait.textContent).toContain('1 / 2')
  })
})

describe('DeroulePhase en multi (essai)', () => {
  // Deux attaques sur Hulk (siege 1, l'autre joueur) : en « concerne », c'est lui
  // qui donne le rythme ; ce joueur-ci (siege 0) voit le meme ecran sans bouton.
  const attaques: EtapeDeroule[] = [
    { cle: 'a1', temps: 'mechant', titre: 'attaque', regle: 'regle:activations', carteId: 50, cibleId: 99, auteurNom: 'Klaw', cibleNom: 'Hulk', boosts: [] },
    { cle: 'a2', temps: 'mechant', titre: 'attaque', regle: 'regle:activations', carteId: 51, cibleId: 99, auteurNom: 'Rhino', cibleNom: 'Hulk', boosts: [] },
  ] as EtapeDeroule[]
  const reponses = (politique: string, etapesLues: Record<string, unknown>) =>
    vi.fn((url: string, _init?: RequestInit) =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(String(url).includes('get_avance_phase') ? { politique } : String(url).includes('get_etapes') ? etapesLues : {}),
      } as Response)
    )
  const cadres = [
    { couleurs: ['#f2c200'], raye: false, siege: 1 },
    { couleurs: ['#2e7d32'], raye: false, siege: 2 },
  ]
  const joueurDeCarte = (id: number | undefined) => (id === 99 ? 1 : id === 12 ? 0 : undefined)
  afterEach(() => {
    cleanup()
    vi.unstubAllGlobals()
  })

  it('le suiveur voit « regarde… » et rejoint l etape du meneur', async () => {
    const fetchSimule = reponses('concerne', { 1: { cle: 'a2', t: 5, boosts: 0 } })
    vi.stubGlobal('fetch', fetchSimule)
    const { container, findByText } = render(
      <DeroulePhase
        etapes={attaques}
        onTerminer={() => {}}
        essai
        phaseMechantEnCours
        herosLocauxIds={new Set([12])}
        herosDesAutresIds={new Set([99])}
        cadresJoueurs={cadres}
        joueurDeCarte={joueurDeCarte}
        siegeLocal={0}
        premierJoueur={0}
        nomsJoueurs={['Shuri', 'Hulk']}
      />
    )
    await findByText(/J2 \(Hulk\) regarde/)
    expect(container.querySelector('.essai-continuer:not(.essai-multi-attente)')).toBeNull()
    // Le meneur est deja a l'etape 2 : le cartouche l'a suivi.
    await vi.waitFor(() => expect(container.textContent).toContain('Rhino'))
  })

  it('le meneur valide la derniere etape connue : le suiveur la valide aussi (son accuse part)', async () => {
    const fetchSimule = reponses('concerne', { 1: { cle: 'a2', t: 5, boosts: 0, valide: 'a2' } })
    vi.stubGlobal('fetch', fetchSimule)
    // Le plateau publie l'etape lue (board.tsx) ; les extras partent avec elle.
    publierEtape(0, 'a1')
    const { container } = render(
      <DeroulePhase
        etapes={attaques}
        onTerminer={() => {}}
        essai
        phaseMechantEnCours
        herosLocauxIds={new Set([12])}
        herosDesAutresIds={new Set([99])}
        cadresJoueurs={cadres}
        joueurDeCarte={joueurDeCarte}
        siegeLocal={0}
        premierJoueur={0}
        nomsJoueurs={['Shuri', 'Hulk']}
      />
    )
    await vi.waitFor(() => expect(container.textContent).toContain('Rhino'))
    // Notre validation est publiee pour a2, comme celle du meneur.
    await vi.waitFor(() =>
      expect(
        fetchSimule.mock.calls.some(
          ([url, init]) => String(url).includes('set_etape') && String(init?.body ?? '').includes('"valide":"a2"')
        )
      ).toBe(true)
    )
  })

  it('le suiveur valide aussi la résolution qui remplace une annonce de même clé', async () => {
    vi.stubGlobal('fetch', reponses('concerne', { 1: { cle: 'a1', t: 5, boosts: 0, valide: 'a1' } }))
    const valider = vi.fn()
    const props = {
      onTerminer: () => {}, onEtapeValidee: valider, essai: true, phaseMechantEnCours: true,
      herosLocauxIds: new Set([12]), herosDesAutresIds: new Set([99]),
      cadresJoueurs: cadres, joueurDeCarte, siegeLocal: 0, premierJoueur: 0,
    }
    const annonce = { ...attaques[0]!, etat: 'annonce' as const }
    const { rerender } = render(<DeroulePhase {...props} etapes={[annonce]} />)
    await vi.waitFor(() => expect(valider).toHaveBeenCalledWith('a1', 'annonce'))
    rerender(<DeroulePhase {...props} etapes={[{ ...annonce, etat: 'resolu', montant: 2 }]} />)
    await vi.waitFor(() => expect(valider).toHaveBeenCalledWith('a1', 'resolu'))
  })

  it('sans essai : rien ne change, aucune lecture de la regle', () => {
    const fetchSimule = reponses('concerne', {})
    vi.stubGlobal('fetch', fetchSimule)
    const { container } = render(
      <DeroulePhase
        etapes={attaques}
        onTerminer={() => {}}
        phaseMechantEnCours
        herosLocauxIds={new Set([12])}
        herosDesAutresIds={new Set([99])}
        siegeLocal={0}
        premierJoueur={0}
      />
    )
    expect(fetchSimule.mock.calls.some(([url]) => String(url).includes('get_avance_phase'))).toBe(false)
    expect(container.querySelector('.essai-multi-attente')).toBeNull()
  })

  it('en solo (aucun autre heros) : aucune lecture de la regle', () => {
    const fetchSimule = reponses('concerne', {})
    vi.stubGlobal('fetch', fetchSimule)
    render(
      <DeroulePhase
        etapes={attaques}
        onTerminer={() => {}}
        essai
        phaseMechantEnCours
        herosLocauxIds={new Set([12])}
        herosDesAutresIds={new Set()}
        cadresJoueurs={cadres}
        joueurDeCarte={joueurDeCarte}
        siegeLocal={0}
        premierJoueur={0}
      />
    )
    expect(fetchSimule.mock.calls.some(([url]) => String(url).includes('get_avance_phase'))).toBe(false)
  })
})

describe('commandes multi sur table', () => {
  afterEach(cleanup)
  it('donne à l’hôte les trois règles et transmet son choix', () => {
    const choisir = vi.fn()
    const { container } = render(<CommandesMultiSurTable multi={{ genre: 'choix-hote', choisir }} enTrajet={false} />)
    expect(container.querySelectorAll('[data-politique]')).toHaveLength(3)
    fireEvent.click(container.querySelector('[data-politique="tous"]')!)
    expect(choisir).toHaveBeenCalledWith('tous')
  })
  it('bloque Prêt pendant le vol et après l’accord du joueur', () => {
    const marquer = vi.fn()
    const multi: PiedMulti = { genre: 'pret', pret: false, pastilles: [{ nom: 'J1', pret: false }], marquer }
    const { container, rerender } = render(<CommandesMultiSurTable multi={multi} enTrajet />)
    fireEvent.click(container.querySelector('[data-pret]')!)
    expect(marquer).not.toHaveBeenCalled()
    rerender(<CommandesMultiSurTable multi={multi} enTrajet={false} />)
    fireEvent.click(container.querySelector('[data-pret]')!)
    expect(marquer).toHaveBeenCalledOnce()
    rerender(<CommandesMultiSurTable multi={{ ...multi, pret: true }} enTrajet={false} />)
    expect(container.querySelector('[data-pret]')).toBeDisabled()
  })
})
