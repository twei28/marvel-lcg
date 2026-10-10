// La fenetre des reglages : ce qu'elle range, et ce qu'elle ne cache pas.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `un sous-reglage inutilisable reste VISIBLE`.
// C'est le defaut que l'utilisateur a decrit le 14/09/2026 : on ne peut pas
// savoir qu'un reglage existe s'il n'apparait qu'une fois son parent active.
// Les autres cas verifient surtout qu'aucun reglage n'a ete perdu en chemin :
// c'est un rangement, pas une refonte.
import { fireEvent, render, screen, within } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { ContenuOnglet, FenetreReglages, ONGLETS, type ProprietesReglages } from './FenetreReglages'

function proprietes(sur: Partial<ProprietesReglages> = {}): ProprietesReglages {
  return {
    affichage: 'normal',
    changerAffichage: vi.fn(),
    animations: true,
    basculerAnimations: vi.fn(),
    sons: true,
    basculerSons: vi.fn(),
    musique: false,
    basculerMusique: vi.fn(),
    succes: true,
    basculerSucces: vi.fn(),
    scansFr: true,
    basculerScansFr: vi.fn(),
    textesCdb: false,
    basculerTextesCdb: vi.fn(),
    basculerLangue: vi.fn(),

    // Essais fermes par defaut, comme pour presque tout le monde : le mode
    // « Sur la table » ne doit alors pas etre propose.
    modePhase: 'detaille',
    changerModePhase: vi.fn(),
    libelleModePhase: (m) =>
      m === 'detaille' ? 'Détaillé' : m === 'sur-table' ? 'Sur la table' : 'Instantané',
    tempsParDecision: 0,
    texteTempsParDecision: () => 'le moteur n’attend pas',
    validationCourte: false,
    basculerValidationCourte: vi.fn(),
    autoCible: true,
    basculerAutoCible: vi.fn(),
    finTourAuto: false,
    basculerFinTourAuto: vi.fn(),
    paiementAuto: false,
    basculerPaiementAuto: vi.fn(),
    sauvegardeAuto: true,
    basculerSauvegardeAuto: vi.fn(),
    revelation: 'court',
    cyclerRevelation: vi.fn(),

    meteo: true,
    basculerMeteo: vi.fn(),
    apercuMeteo: undefined,
    reglerApercuMeteo: vi.fn(),
    reponseAmbiance: 'demander',
    cyclerReponseAmbiance: vi.fn(),

    designEssai: true,
    basculerDesignEssai: vi.fn(),
    modeActions: 'simple',
    changerModeActions: vi.fn(),
    curseurs: false,
    basculerCurseurs: vi.fn(),
    montrerDisposition: false,
    reglageMode: 'auto',
    cyclerReglageMode: vi.fn(),
    changerTeinte: vi.fn(),
    reinitialiserTeinte: vi.fn(),
    ...sur,
  }
}

function ligne(libelle: string) {
  return screen.getByText(libelle).closest('.ligne-option') as HTMLElement
}

describe('un sous-reglage inutilisable reste VISIBLE', () => {
  // ⚠ Le coeur du changement. Avant, « Vitesse du deroule » n'existait dans le
  // DOM que si « Avance toute seule » etait active : impossible de savoir
  // qu'elle existait. Maintenant elle est la, grisee.
  it('« Aide quand je joue une carte » est visible mais inerte sans le nouveau plateau', () => {
    render(<ContenuOnglet onglet="avance" p={proprietes({ designEssai: false })} />)
    const choix = ligne('Aide quand je joue une carte')
    expect(choix.className).toContain('est-desactive')
    for (const bouton of within(choix).getAllByRole('button')) expect(bouton).toBeDisabled()
  })

  it('un sous-reglage porte le retrait, son parent non', () => {
    render(<ContenuOnglet onglet="apparence" p={proprietes()} />)
    expect(ligne('Animations').className).toContain('est-enfant')
    expect(ligne('Langue').className).not.toContain('est-enfant')
  })
})

describe('aucun reglage n’a ete perdu au rangement', () => {
  // Les 18 reglages de l'ancien panneau, avec l'onglet ou chacun doit se
  // trouver. Un reglage qui disparaitrait d'un onglet sans reapparaitre
  // ailleurs ferait rougir ce test.
  // Rangement du 04/10/2026 (questions une a une) : Apparence, Son, Jeu,
  // Avance ; intitules qui disent l'effet.
  const ATTENDUS: Record<string, string[]> = {
    apparence: [
      'Style d’affichage',
      'Couleur de la table',
      'Animations',
      'Météo et décor',
      'Aperçu d’ambiance',
      'Langue',
      'Cartes en français',
      'Texte des cartes en français',
      'Annonce des exploits',
    ],
    son: ['Bruitages', 'Musique de fond'],
    jeu: [
      'Phase du méchant',
      'Carte révélée en grand',
      'Le jeu agit pour moi quand il n’y a qu’un choix',
      'Choisir la seule cible possible',
      'Valider sans demander',
      'Payer avec la seule carte possible',
      'Finir mon tour quand je ne peux plus rien jouer',
      'Sauvegarde à chaque phase',
    ],
    avance: ['Nouveau plateau', 'Aide quand je joue une carte', 'Curseurs des autres joueurs'],
  }

  for (const [onglet, libelles] of Object.entries(ATTENDUS)) {
    it(`l’onglet ${onglet} porte ses ${libelles.length} reglages`, () => {
      render(<ContenuOnglet onglet={onglet as (typeof ONGLETS)[number]} p={proprietes()} />)
      for (const libelle of libelles) expect(screen.getByText(libelle)).toBeTruthy()
    })
  }

  it('« Disposition » n’apparait QUE sur un appareil mobile', () => {
    // Sur un PC le plateau est de toute facon rendu en mode PC : le reglage
    // n'aurait aucun effet, et c'est lui qui a un jour enferme l'utilisateur.
    const { unmount } = render(
      <ContenuOnglet onglet="avance" p={proprietes({ montrerDisposition: false })} />
    )
    expect(screen.queryByText('Table complète comme sur PC')).toBeNull()
    unmount()
    render(<ContenuOnglet onglet="avance" p={proprietes({ montrerDisposition: true })} />)
    expect(screen.getByText('Table complète comme sur PC')).toBeTruthy()
  })

  it('la note du « temps par decision » ne sort qu’en phase detaillee et si le moteur en a un', () => {
    const { unmount } = render(
      <ContenuOnglet onglet="jeu" p={proprietes({ modePhase: 'detaille', tempsParDecision: 0 })} />
    )
    expect(screen.queryByText(/n’attend pas/)).toBeNull()
    unmount()
    render(
      <ContenuOnglet onglet="jeu" p={proprietes({ modePhase: 'detaille', tempsParDecision: 30 })} />
    )
    expect(screen.getByText(/n’attend pas/)).toBeTruthy()
  })
})

describe('chaque interrupteur appelle bien sa fonction', () => {
  it('choisir l affichage sobre', () => {
    const changerAffichage = vi.fn()
    render(<ContenuOnglet onglet="apparence" p={proprietes({ changerAffichage })} />)
    fireEvent.click(screen.getByText('Sobre'))
    expect(changerAffichage).toHaveBeenCalledWith('sobre')
  })

  it('en affichage sobre, « Animations » reste visible mais inerte et sur « Non »', () => {
    const basculerAnimations = vi.fn()
    render(<ContenuOnglet onglet="apparence" p={proprietes({ affichage: 'sobre', basculerAnimations })} />)
    const ligne = screen.getByText('Animations').closest('button')!
    expect(ligne).toBeDisabled()
    expect(ligne).toHaveAttribute('aria-checked', 'false')
    fireEvent.click(ligne)
    expect(basculerAnimations).not.toHaveBeenCalled()
  })

  it('basculer les animations', () => {
    const basculerAnimations = vi.fn()
    render(<ContenuOnglet onglet="apparence" p={proprietes({ basculerAnimations })} />)
    fireEvent.click(screen.getByText('Animations'))
    expect(basculerAnimations).toHaveBeenCalledTimes(1)
  })

  it('choisir la phase instantanee', () => {
    const changerModePhase = vi.fn()
    render(<ContenuOnglet onglet="jeu" p={proprietes({ changerModePhase })} />)
    fireEvent.click(screen.getByText('D’un coup'))
    expect(changerModePhase).toHaveBeenCalledWith('instantane')
  })

  it('« Façon de jouer » : Auto par défaut, et Manuel se retient pour le lanceur', () => {
    window.localStorage.removeItem('marvel-board-facon-de-jouer')
    render(<ContenuOnglet onglet="jeu" p={proprietes()} />)
    const groupe = screen.getByRole('group', { name: 'Façon de jouer' })
    expect(within(groupe).getByText('Auto').className).toContain('est-actif')
    fireEvent.click(within(groupe).getByText('Manuel'))
    expect(window.localStorage.getItem('marvel-board-facon-de-jouer')).toBe('manuel')
    expect(within(groupe).getByText('Manuel').className).toContain('est-actif')
    window.localStorage.removeItem('marvel-board-facon-de-jouer')
  })

  it('rechoisir la valeur deja active ne declenche rien', () => {
    // Sans quoi cliquer « Détaillé » alors qu'on y est ferait un aller-retour
    // inutile, visible a l'ecran sur les reglages qui se cyclent.
    const cyclerReglageMode = vi.fn()
    render(
      <ContenuOnglet
        onglet="avance"
        p={proprietes({ montrerDisposition: true, reglageMode: 'auto', cyclerReglageMode })}
      />
    )
    const table = within(ligne('Table complète comme sur PC'))
    fireEvent.click(table.getByText('Non'))
    expect(cyclerReglageMode).not.toHaveBeenCalled()
    fireEvent.click(table.getByText('Oui'))
    expect(cyclerReglageMode).toHaveBeenCalledTimes(1)
  })

  it('« Cartes revelees » atteint la valeur demandee en cyclant', () => {
    // Le moteur ne sait que cycler : off -> court -> long -> off. La fenetre
    // offre pourtant trois pastilles, donc elle cycle autant de fois qu'il
    // faut. Depuis « court », atteindre « off » demande deux pas.
    const cyclerRevelation = vi.fn()
    // « D'un coup » : en « Étape par étape », la ligne est grisée (D42, plus bas).
    render(<ContenuOnglet onglet="jeu" p={proprietes({ revelation: 'court', cyclerRevelation, modePhase: 'instantane' })} />)
    // ⚠ Chercher DANS la ligne : « Non » est aussi l'etat affiche par chaque
    // interrupteur coupe de l'onglet, un `getByText` global en trouve plusieurs.
    const cartes = within(ligne('Carte révélée en grand'))
    fireEvent.click(cartes.getByText('5 s'))
    expect(cyclerRevelation).toHaveBeenCalledTimes(1)
    cyclerRevelation.mockClear()
    fireEvent.click(cartes.getByText('Non'))
    expect(cyclerRevelation).toHaveBeenCalledTimes(2)
  })
})

// D42 (refonte du cartouche, 04/10/2026) : en « Étape par étape », la carte
// révélée se montre en grand DANS le cartouche du bas. La ligne reste dans les
// réglages, grisée, et dit pourquoi ; les deux autres modes la gardent active.
describe('« Carte révélée en grand » et le cartouche', () => {
  it('grisée en « Étape par étape », avec « Le cartouche s’en charge »', () => {
    render(<ContenuOnglet onglet="jeu" p={proprietes({ modePhase: 'detaille' })} />)
    const rangee = ligne('Carte révélée en grand')
    expect(rangee.className).toContain('est-desactive')
    expect(within(rangee).getByText('Le cartouche s’en charge')).toBeInTheDocument()
    for (const bouton of within(rangee).getAllByRole('button')) expect(bouton).toBeDisabled()
  })

  it('active, avec son explication d’origine, dans les deux autres modes', () => {
    for (const modePhase of ['instantane', 'sur-table'] as const) {
      const { unmount } = render(<ContenuOnglet onglet="jeu" p={proprietes({ modePhase })} />)
      const rangee = ligne('Carte révélée en grand')
      expect(rangee.className, modePhase).not.toContain('est-desactive')
      expect(within(rangee).getByText('Au centre de l’écran, le temps de la lire')).toBeInTheDocument()
      unmount()
    }
  })
})

describe('la fenetre elle-meme', () => {
  it('ne rend rien tant qu’elle est fermee', () => {
    const { container } = render(
      <FenetreReglages ouvert={false} fermer={vi.fn()} {...proprietes()} />
    )
    expect(container.querySelector('.reglages-fenetre')).toBeNull()
  })

  it('ouvre sur l’onglet « Apparence », et on peut changer d’onglet', () => {
    render(<FenetreReglages ouvert fermer={vi.fn()} {...proprietes()} />)
    expect(screen.getByText('Animations')).toBeTruthy()
    expect(screen.getAllByRole('tab').map((o) => o.textContent)).toEqual(['Apparence', 'Son', 'Jeu', 'Avancé'])
    fireEvent.click(screen.getByRole('tab', { name: 'Son' }))
    expect(screen.getByText('Bruitages')).toBeTruthy()
    expect(screen.queryByText('Animations')).toBeNull()
  })

  it('affiche les quatre onglets, et un seul est selectionne', () => {
    render(<FenetreReglages ouvert fermer={vi.fn()} {...proprietes()} />)
    const onglets = screen.getAllByRole('tab')
    expect(onglets).toHaveLength(4)
    expect(onglets.filter((o) => o.getAttribute('aria-selected') === 'true')).toHaveLength(1)
  })

  it('se ferme par la croix, par Echap et par le fond', () => {
    // ⚠ Trois sorties, et c'est voulu : une fenetre qu'on ne ferme que par un
    // bouton precis est une fenetre dont on se sent prisonnier, exactement le
    // reproche fait a l'ancien empilement de menus.
    const fermer = vi.fn()
    const { container } = render(<FenetreReglages ouvert fermer={fermer} {...proprietes()} />)

    fireEvent.click(screen.getByTitle('Fermer'))
    expect(fermer).toHaveBeenCalledTimes(1)

    fireEvent.keyDown(document, { key: 'Escape' })
    expect(fermer).toHaveBeenCalledTimes(2)

    fireEvent.click(container.querySelector('.reglages-fond') as HTMLElement)
    expect(fermer).toHaveBeenCalledTimes(3)
  })

  it('un clic DANS la fenetre ne la ferme pas', () => {
    const fermer = vi.fn()
    const { container } = render(<FenetreReglages ouvert fermer={fermer} {...proprietes()} />)
    fireEvent.click(container.querySelector('.reglages-fenetre') as HTMLElement)
    expect(fermer).not.toHaveBeenCalled()
  })

  it('Echap ne ferme plus rien une fois la fenetre demontee', () => {
    // Un ecouteur clavier laisse en place capterait les raccourcis du plateau
    // (E = fin du tour, U = annuler) longtemps apres la fermeture.
    const fermer = vi.fn()
    const { unmount } = render(<FenetreReglages ouvert fermer={fermer} {...proprietes()} />)
    unmount()
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(fermer).not.toHaveBeenCalled()
  })
})

describe('le mode « Sur la table » est proposé à tous', () => {
  // ⚠ FERMÉ PUIS ROUVERT le 14/09/2026. Fermé après la première partie jouée
  // dedans (« je le retire jusqu'à ce que ce soit prêt »), rouvert une fois les
  // 32 décisions de la refonte traitées, à sa demande.
  //
  // ⚠ CE FICHIER RESTE LE TÉMOIN DE L'INTERRUPTEUR : le jour où
  // `MODE_SUR_TABLE_OUVERT` repasse à faux, ces cas rougissent et rappellent de
  // réécrire ce qu'on attend. Ils ont déjà joué ce rôle une fois.
  const modes = () =>
    within(screen.getByText('Phase du méchant').closest('.ligne-option') as HTMLElement)
      .getAllByRole('button')
      .map((b) => b.textContent)

  it('⚠ le réglage de langue prévient pour les cartes sans scan', () => {
    // Demande du 16/09/2026. Tous les scans n'existent pas dans les deux
    // langues : une carte restée en anglais au milieu d'une partie française
    // ressemble à un défaut tant que personne ne l'a annoncé. La phrase est
    // ici, au moment du choix, et elle nomme le relais : la traduction posée sur la carte agrandie.
    // ⚠ Le `detail` d'une ligne de réglage devient un attribut `title`, pas du
    // texte : c'est l'infobulle du bouton lui-même. On cherche donc là.
    render(<ContenuOnglet onglet="apparence" p={proprietes()} />)
    const ligne = screen.getByTitle(/Langue de l’interface et de la narration/)
    expect(ligne.getAttribute('title')).toMatch(/sans scan dans cette langue reste en anglais/)
    expect(ligne.getAttribute('title')).toMatch(/traduction est posée sur son texte/)
  })

  it('il apparaît entre les deux autres, pour tous les joueurs', () => {
    // OUVERT À TOUS le 05/10/2026 : la fenêtre de préparation le présente à
    // chacun, il doit donc se retrouver ici sans condition. Il raconte la même
    // chose que « Détaillé », au même rythme : sa place est à côté de lui.
    render(<ContenuOnglet onglet="jeu" p={proprietes()} />)
    expect(modes()).toEqual(['Étape par étape', 'Sur la table', 'D’un coup'])
  })

  it('un mode déjà choisi reste dans la liste', () => {
    render(<ContenuOnglet onglet="jeu" p={proprietes({ modePhase: 'sur-table' })} />)
    expect(modes()).toEqual(['Étape par étape', 'Sur la table', 'D’un coup'])
  })
})

describe('le volume des bruitages (refonte des sons, 07/10/2026)', () => {
  it('l’onglet Son propose un curseur de volume, à 20 % par défaut', () => {
    window.localStorage.removeItem('marvel-board-volume-sons')
    render(<ContenuOnglet onglet="son" p={proprietes()} />)
    const curseur = screen.getByRole('slider', { name: /volume des bruitages/i })
    expect((curseur as HTMLInputElement).value).toBe('20')
  })

  it('bouger le curseur enregistre le volume', () => {
    window.localStorage.removeItem('marvel-board-volume-sons')
    render(<ContenuOnglet onglet="son" p={proprietes()} />)
    const curseur = screen.getByRole('slider', { name: /volume des bruitages/i })
    fireEvent.change(curseur, { target: { value: '65' } })
    expect(window.localStorage.getItem('marvel-board-volume-sons')).toBe('65')
    expect((curseur as HTMLInputElement).value).toBe('65')
  })

  it('bruitages coupés : le curseur reste VISIBLE mais grisé', () => {
    render(<ContenuOnglet onglet="son" p={proprietes({ sons: false })} />)
    expect((screen.getByRole('slider', { name: /volume des bruitages/i }) as HTMLInputElement).disabled).toBe(true)
  })
})

describe('FenetreReglages en lecture seule (relecture et spectateur)', () => {
  it('dit que ce sont les reglages du joueur et grise le contenu', () => {
    render(<FenetreReglages ouvert fermer={vi.fn()} lectureSeule {...proprietes()} />)
    expect(screen.getByText('Réglages du joueur, en lecture seule.')).toBeTruthy()
    const panneau = screen.getByRole('tabpanel')
    expect(panneau.querySelector('[inert]')).not.toBeNull()
  })

  it('temoin : hors lecture seule, rien n est grise ni annonce', () => {
    render(<FenetreReglages ouvert fermer={vi.fn()} {...proprietes()} />)
    expect(screen.queryByText('Réglages du joueur, en lecture seule.')).toBeNull()
    expect(screen.getByRole('tabpanel').querySelector('[inert]')).toBeNull()
  })
})
