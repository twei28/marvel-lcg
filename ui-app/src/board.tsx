// Page du nouveau plateau.
//
//   /app/board.html                -> la partie en cours, JOUABLE
//   /app/board.html?etat=<fichier> -> un etat de partie enregistre, lecture seule
//   /app/board.html?p=1            -> le plateau vu par le joueur 1
//
// Le plateau est AJOUTE a cote de l'ancien, il ne le remplace pas : la barre du
// haut ramene a l'ancienne interface a tout moment. Aucun fichier du jeu n'est
// modifie.
//
// Attention : en mode partie en cours, cette page ouvre le socket du moteur et
// devient donc un vrai client de jeu. Elle DOIT accuser reception des rendus,
// sinon la partie se figerait (voir moteur.ts).
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type FocusEvent as ReactFocusEvent,
  type MouseEvent as ReactMouseEvent,
} from 'react'
import { createRoot, type Root } from 'react-dom/client'
import '../styles/tokens.css'
import { ScanCard, type CardEffectDelta, type ScanCardProps } from './components/ScanCard'
import { AssistantAction } from './board/AssistantAction'
import { BarreAction } from './board/BarreAction'
import { Board, CarteApercu } from './board/Board'
import { PlateauMobile } from './board/mobile/PlateauMobile'
import { useModeMobile, type ReglageMode } from './board/mobile/useModeMobile'
import { CoucheAnimations } from './board/CoucheAnimations'
import { CoucheCharge } from './board/CoucheCharge'
import { CoucheRevelation } from './board/CoucheRevelation'
import { useSons } from './board/sons'
import { useHaloStatut } from './board/halo-statut'
import { catalogueVide, chargerCatalogue, type Catalogue } from './board/catalogue'
import { toScanCard, type ContexteCarte } from './board/card-model'
import {
  DemandeCentrale,
  EvenementCentrale,
  demandeDoitApparaitreAuCentre,
} from './board/DemandeCentrale'
import { HistoriquePartie, useHistoriquePartie } from './board/HistoriquePartie'
import { JournalHeros } from './board/JournalHeros'
import { RecapPhaseMechant } from './board/RecapPhaseMechant'
import { SplashTour } from './board/SplashTour'
import { CoucheCoach } from './board/CoucheCoach'
import {
  CLE_AUTO_CIBLE,
  CLE_VALIDATION_COURTE,
  lireAutoCible,
  lireValidationCourte,
  useInteraction,
  type EtatInteractif,
} from './board/interaction'
import { MenuActionsCarte } from './board/MenuActionsCarte'
import { basculerLangue, langueActuelle, synchroniserLangueServeur, t } from './board/langue'
import { CLE_TEXTES_CDB, lireTextesCdb } from './board/marvelcdb'
import { CLE_SCANS_FR, scansFrActifs } from './board/scans-fr'
import { CoucheMeteo, CLE_METEO, lireMeteoActive } from './board/CoucheMeteo'
import { CoucheCurseurs, CLE_CURSEURS, lireCurseursActifs } from './board/CoucheCurseurs'
import { CoucheHautsFaits } from './board/CoucheHautsFaits'
import { CoucheSucces, CLE_SUCCES, lireSuccesActifs } from './board/CoucheSucces'
import { CLE_MUSIQUE, lireMusiqueActive, useMusique } from './board/musique'
import {
  CLE_PHASE_RAPIDE,
  Moteur,
  evenementNarreImportant,
  lirePhaseRapide,
  type EtatMoteur,
} from './board/moteur'
import { SelecteurCibles } from './board/SelecteurCibles'
import { nomLisible } from './board/BarreAction'
import { construirePlateau, type Plateau } from './board/zones'
import type { Demande, Option, Reponse } from './board/ask'
import {
  chargerCatalogueEtats,
  chargerEtat,
  type EntreeCatalogue,
} from './board/sources'
import { isScheme, isVisibleFor, type World, type WorldCard } from './board/world'

/** L'ancien plateau. Le serveur sert marvel.html des que l'adresse a une query. */
const ANCIEN_PLATEAU = '/?p='

/** Table pas encore decoupee : aucune carte dessinee. */
const AUCUN_ID: Set<number> = new Set()
const CLE_MODE_ACTIONS = 'marvel-board-action-mode'
const CLE_ANIMATIONS = 'marvel-board-animations'

type ModeActions = 'simple' | 'detailed'

function lireModeActions(): ModeActions {
  try {
    return window.localStorage.getItem(CLE_MODE_ACTIONS) === 'detailed' ? 'detailed' : 'simple'
  } catch {
    return 'simple'
  }
}

/** Animations de deplacement activees ? Par defaut oui, sauf choix contraire. */
function lireAnimations(): boolean {
  try {
    return window.localStorage.getItem(CLE_ANIMATIONS) !== 'off'
  } catch {
    return true
  }
}

const CLE_SONS = 'marvel-board-sons'
const CLE_REVELATION = 'marvel-board-revelation'

/** Sons du moteur actifs ? Par defaut oui, comme le client d'origine. */
function lireSons(): boolean {
  try {
    return window.localStorage.getItem(CLE_SONS) !== 'off'
  } catch {
    return true
  }
}

/** Presentation des cartes revelees : coupee, breve ou longue. */
type ModeRevelation = 'off' | 'court' | 'long'
const DUREES_REVELATION: Record<ModeRevelation, number> = { off: 0, court: 2600, long: 5000 }

function lireRevelation(): ModeRevelation {
  try {
    const valeur = window.localStorage.getItem(CLE_REVELATION)
    return valeur === 'off' || valeur === 'long' ? valeur : 'court'
  } catch {
    return 'court'
  }
}

function parametres() {
  const url = new URLSearchParams(window.location.search)
  const joueur = Number(url.get('p') ?? '0')
  return {
    etat: url.get('etat'),
    playerId: Number.isInteger(joueur) && joueur >= 0 ? joueur : 0,
  }
}

function messageDErreur(cause: unknown): string {
  return cause instanceof Error ? cause.message : String(cause)
}

/** Nom d'une carte du monde, par identifiant d'objet. Pour situer une action. */
function nomDeCarte(world: World | undefined, id: number): string | undefined {
  if (!world || id === 0) return undefined
  let trouve: string | undefined
  const parcourir = (valeur: unknown) => {
    if (trouve !== undefined) return
    if (Array.isArray(valeur)) {
      for (const element of valeur) parcourir(element)
      return
    }
    if (typeof valeur !== 'object' || valeur === null) return
    const objet = valeur as Record<string, unknown>
    if (objet.id === id && typeof objet.name === 'string') {
      trouve = objet.name
      return
    }
    for (const enfant of Object.values(objet)) parcourir(enfant)
  }
  parcourir(world)
  return trouve
}

function indexerCartesMonde(world: World | undefined): Map<number, WorldCard> {
  const index = new Map<number, WorldCard>()
  if (!world) return index

  const parcourir = (valeur: unknown) => {
    if (Array.isArray(valeur)) {
      for (const element of valeur) parcourir(element)
      return
    }
    if (typeof valeur !== 'object' || valeur === null) return
    const objet = valeur as Partial<WorldCard>
    if (typeof objet.id === 'number' && typeof objet.card_type === 'string') {
      index.set(objet.id, objet as WorldCard)
    }
    for (const enfant of Object.values(objet)) parcourir(enfant)
  }

  parcourir(world)
  return index
}

function valeurCompteur(carte: WorldCard, cle: 'health' | 'k_threat'): number | undefined {
  const valeur = carte.info[cle]
  return typeof valeur === 'number' && Number.isFinite(valeur) ? valeur : undefined
}

/** Capture les variations de compteurs entre deux rendus du moteur. */
function useEffetsCartes(monde: World | undefined): Map<number, CardEffectDelta> {
  const [effets, setEffets] = useState<Map<number, CardEffectDelta>>(() => new Map())
  const precedent = useRef<World | undefined>(undefined)
  const minuteurs = useRef(new Map<number, number>())

  useEffect(() => {
    if (!monde) return
    const avant = precedent.current
    if (avant) {
      const precedentes = indexerCartesMonde(avant)
      const courantes = indexerCartesMonde(monde)
      const changements: Array<[number, CardEffectDelta]> = []

      for (const [id, carte] of courantes) {
        const ancienne = precedentes.get(id)
        if (!ancienne) continue
        const vieAvant = valeurCompteur(ancienne, 'health')
        const vieApres = valeurCompteur(carte, 'health')
        if (vieAvant !== undefined && vieApres !== undefined && vieAvant !== vieApres) {
          changements.push([id, { value: vieApres - vieAvant, kind: vieApres < vieAvant ? 'damage' : 'heal' }])
          continue
        }
        const menaceAvant = valeurCompteur(ancienne, 'k_threat')
        const menaceApres = valeurCompteur(carte, 'k_threat')
        if (menaceAvant !== undefined && menaceApres !== undefined && menaceAvant !== menaceApres) {
          changements.push([id, { value: menaceApres - menaceAvant, kind: 'threat' }])
        }
      }

      if (changements.length > 0) {
        setEffets((courants) => {
          const suivants = new Map(courants)
          for (const [id, effet] of changements) {
            const ancienMinuteur = minuteurs.current.get(id)
            if (ancienMinuteur !== undefined) window.clearTimeout(ancienMinuteur)
            suivants.set(id, effet)
            const minuteur = window.setTimeout(() => {
              setEffets((actuels) => {
                if (actuels.get(id) !== effet) return actuels
                const sans = new Map(actuels)
                sans.delete(id)
                return sans
              })
              minuteurs.current.delete(id)
            }, 1700)
            minuteurs.current.set(id, minuteur)
          }
          return suivants
        })
      }
    }
    precedent.current = monde
  }, [monde, monde?.render_id])

  useEffect(
    () => () => {
      for (const minuteur of minuteurs.current.values()) window.clearTimeout(minuteur)
    },
    []
  )

  return effets
}

function indexerCartesAffichees(plateau: Plateau | undefined): Map<number, ScanCardProps> {
  const index = new Map<number, ScanCardProps>()
  if (!plateau) return index
  for (const emplacement of plateau.emplacements) {
    for (const groupe of emplacement.groupes) {
      for (const unite of groupe) {
        index.set(Number(unite.carte.id), unite.carte)
        for (const attachee of unite.attachees) index.set(Number(attachee.id), attachee)
      }
    }
  }
  return index
}

function optionAvecCibles(option: Option | undefined): option is Option {
  return option !== undefined && option.target_num_range[1] > 0 && option.all_legal_targets.length > 0
}

function idsPulsePourOption(
  option: Option | undefined,
  plateau: Plateau | undefined,
  cibleVerrouillee?: number
): Set<number> {
  const ids = new Set<number>()
  if (!optionAvecCibles(option) || !plateau) return ids
  if (option.bind_id !== 0 && plateau.idsAffiches.has(option.bind_id)) ids.add(option.bind_id)
  if (cibleVerrouillee !== undefined) {
    if (plateau.idsAffiches.has(cibleVerrouillee)) {
      ids.add(cibleVerrouillee)
      return ids
    }
    const representant = plateau.representantsDePile.get(cibleVerrouillee)
    if (representant !== undefined) ids.add(representant)
    return ids
  }
  for (const cible of new Set(option.all_legal_targets)) {
    if (plateau.idsAffiches.has(cible)) {
      ids.add(cible)
      continue
    }
    const representant = plateau.representantsDePile.get(cible)
    if (representant !== undefined) ids.add(representant)
  }
  return ids
}

/**
 * Pendant l'activation ennemie, le moteur laisse les cartes impliquees dans
 * le prompt sous la forme [(id, card_id) Nom]. On les met toutes en evidence
 * pour que la relation source/cible reste lisible sans ouvrir une action.
 */
function idsPulsePourDemandeEnnemie(
  monde: World | undefined,
  demande: Demande | undefined,
  plateau: Plateau | undefined
): Set<number> {
  const ids = new Set<number>()
  if (!monde || !plateau || monde.phase !== 'Enemy Activation') return ids

  const texte = [monde.prompt, monde.prompt_last_text, demande?.prompt_text]
    .filter((valeur): valeur is string => typeof valeur === 'string')
    .join(' ')
  const references = [...texte.matchAll(/\[\(\s*(\d+)\s*,/g)]
    .map((correspondance) => Number(correspondance[1]))
    .filter((id) => Number.isFinite(id))

  // Les prompts d'activation contiennent normalement toutes les cartes liees.
  // Le repli couvre les demandes techniques dont le texte ne porte pas de
  // references, en reutilisant les porteurs et leurs cibles legales.
  const candidats = references.length > 0
    ? references
    : demande?.options.flatMap((option) => [option.bind_id, ...option.all_legal_targets]) ?? []

  for (const id of new Set(candidats)) {
    if (id <= 0) continue
    if (plateau.idsAffiches.has(id)) {
      ids.add(id)
      continue
    }
    const representant = plateau.representantsDePile.get(id)
    if (representant !== undefined) ids.add(representant)
  }
  return ids
}

function ciblesHorsTablePourOption(
  option: Option,
  cartesParId: Map<number, WorldCard>,
  plateau: Plateau,
  playerId: number,
  catalogue: Catalogue
): ScanCardProps[] {
  const cartes: ScanCardProps[] = []
  for (const id of new Set(option.all_legal_targets)) {
    if (plateau.idsAffiches.has(id)) continue
    const carte = cartesParId.get(id)
    if (!carte) continue
    const visible = isVisibleFor(carte, playerId) || option.is_search
    cartes.push(
      toScanCard(
        visible ? { ...carte, visible_for_players: [playerId], is_face_up: true } : carte,
        { playerId, actives: new Set(), catalogue }
      )
    )
  }
  return cartes
}

function optionDisponible(option: Option): boolean {
  return option.failure_reason === ''
}

function optionsDisponiblesVersCible(options: Option[], cible: number): Option[] {
  return options.filter(
    (option) =>
      optionDisponible(option) &&
      option.target_num_range[1] > 0 &&
      option.all_legal_targets.includes(cible)
  )
}

function estCibleExpliquee(carte: WorldCard | undefined): boolean {
  if (!carte) return false
  return isScheme(carte) || carte.card_type === 'EncounterVillain' || carte.card_type === 'Minion'
}

function ajouterPulse(
  interactifs: Map<number, EtatInteractif>,
  ids: Set<number>
): Map<number, EtatInteractif> {
  if (ids.size === 0) return interactifs
  const resultat = new Map(interactifs)
  for (const id of ids) {
    const courant = resultat.get(id)
    if (courant) {
      resultat.set(id, { ...courant, pulse: true })
      continue
    }
    resultat.set(id, { role: 'cible-preview', choisie: false, pulse: true })
  }
  return resultat
}

type GroupeCartesRegardees = {
  cle: string
  titre: string
  cartes: ScanCardProps[]
}

function cartesRegardeesDansPile(
  cle: string,
  titre: string,
  pile: readonly WorldCard[] | undefined,
  contexte: ContexteCarte
): GroupeCartesRegardees | undefined {
  if (!Array.isArray(pile)) return undefined

  const visibles = pile.filter(
    (carte) => isVisibleFor(carte, contexte.playerId) && !carte.is_face_up
  )
  if (visibles.length <= 1) return undefined

  return {
    cle,
    titre,
    cartes: visibles.map((carte) => toScanCard(carte, contexte)),
  }
}

function cartesRegardees(
  world: World,
  playerId: number,
  catalogue: Catalogue
): GroupeCartesRegardees[] {
  const contexte: ContexteCarte = {
    playerId,
    actives: new Set(world.active_card_ids ?? []),
    catalogue,
  }
  const groupes: Array<GroupeCartesRegardees | undefined> = [
    cartesRegardeesDansPile('rencontre', 'Encounter deck', world.encounter_deck, contexte),
    cartesRegardeesDansPile('vilain', 'Villain deck', world.villain_deck, contexte),
    cartesRegardeesDansPile('complot', 'Main scheme deck', world.main_schemes_deck, contexte),
  ]

  for (const [index, joueur] of (world.players ?? []).entries()) {
    groupes.push(
      cartesRegardeesDansPile(
        `joueur-${index}`,
        index === playerId ? 'Your deck' : `Player ${index + 1} deck`,
        joueur.player_deck,
        contexte
      )
    )
    groupes.push(
      cartesRegardeesDansPile(
        `joueur-${index}-suppl`,
        index === playerId ? 'Your additional deck' : `Player ${index + 1} additional deck`,
        joueur.additional_deck,
        contexte
      )
    )
    groupes.push(
      cartesRegardeesDansPile(
        `joueur-${index}-mise-de-cote`,
        index === playerId ? 'Your set-aside deck' : `Player ${index + 1} set-aside deck`,
        joueur.set_aside_deck,
        contexte
      )
    )
  }

  for (const [index, deck] of (world.additional_decks ?? []).entries()) {
    groupes.push(
      cartesRegardeesDansPile(`deck-supplementaire-${index}`, `Additional deck ${index + 1}`, deck, contexte)
    )
  }

  return groupes.filter((groupe): groupe is GroupeCartesRegardees => groupe !== undefined)
}

function signatureCartesRegardees(groupes: GroupeCartesRegardees[]): string {
  return groupes
    .map((groupe) => `${groupe.cle}:${groupe.cartes.map((carte) => carte.id).join(',')}`)
    .join('|')
}

function ModaleCartesRegardees({ groupes }: { groupes: GroupeCartesRegardees[] }) {
  const signature = useMemo(() => signatureCartesRegardees(groupes), [groupes])
  const [signatureFermee, setSignatureFermee] = useState<string | undefined>(undefined)
  const [apercuId, setApercuId] = useState<string | null>(null)

  const cartesParId = useMemo(() => {
    const index = new Map<string, ScanCardProps>()
    for (const groupe of groupes) {
      for (const carte of groupe.cartes) index.set(carte.id, carte)
    }
    return index
  }, [groupes])

  const pointerCarte = useCallback((cible: EventTarget | null) => {
    if (!(cible instanceof HTMLElement)) {
      setApercuId(null)
      return
    }
    const carte = cible.closest<HTMLElement>('.scan-card')
    setApercuId(carte?.dataset.cardId ?? null)
  }, [])

  const survoler = useCallback(
    (evenement: ReactMouseEvent<HTMLElement>) => pointerCarte(evenement.target),
    [pointerCarte]
  )

  const focaliser = useCallback(
    (evenement: ReactFocusEvent<HTMLElement>) => pointerCarte(evenement.target),
    [pointerCarte]
  )

  const perdreFocus = useCallback((evenement: ReactFocusEvent<HTMLElement>) => {
    const prochaine = evenement.relatedTarget
    if (prochaine instanceof Node && evenement.currentTarget.contains(prochaine)) return
    setApercuId(null)
  }, [])

  useEffect(() => {
    if (!signature) setSignatureFermee(undefined)
  }, [signature])

  if (!signature || signatureFermee === signature) return null

  const total = groupes.reduce((somme, groupe) => somme + groupe.cartes.length, 0)
  const carteApercu = apercuId ? cartesParId.get(apercuId) : undefined

  return (
    <div className="plateau-regardees-voile">
      <section
        className="plateau-regardees"
        role="dialog"
        aria-label={t('Cartes regardées')}
        onMouseOver={survoler}
        onMouseLeave={() => setApercuId(null)}
        onFocus={focaliser}
        onBlur={perdreFocus}
      >
        <header className="plateau-regardees-entete">
          <div>
            <span className="plateau-eyebrow">{t('Cartes regardées')}</span>
            <strong>
              {total} card{total > 1 ? 's' : ''}
            </strong>
          </div>
          <button type="button" onClick={() => setSignatureFermee(signature)}>
            {t('Fermer')}
          </button>
        </header>

        <div className="plateau-regardees-corps">
          {groupes.map((groupe) => (
            <section className="plateau-regardees-groupe" key={groupe.cle}>
              <h2>
                {groupe.titre} · {groupe.cartes.length}
              </h2>
              <div className="plateau-regardees-cartes">
                {groupe.cartes.map((carte) => (
                  <ScanCard {...carte} key={carte.id} />
                ))}
              </div>
            </section>
          ))}
        </div>
      </section>
      {carteApercu ? <CarteApercu carte={carteApercu} /> : null}
    </div>
  )
}

function ModaleCiblesMenu({
  titre,
  cartes,
  fermer,
}: {
  titre: string
  cartes: ScanCardProps[]
  fermer: () => void
}) {
  const [apercuId, setApercuId] = useState<string | null>(null)

  const cartesParId = useMemo(() => {
    const index = new Map<string, ScanCardProps>()
    for (const carte of cartes) index.set(carte.id, carte)
    return index
  }, [cartes])

  const pointerCarte = useCallback((cible: EventTarget | null) => {
    if (!(cible instanceof HTMLElement)) {
      setApercuId(null)
      return
    }
    const carte = cible.closest<HTMLElement>('.scan-card')
    setApercuId(carte?.dataset.cardId ?? null)
  }, [])

  const survoler = useCallback(
    (evenement: ReactMouseEvent<HTMLElement>) => pointerCarte(evenement.target),
    [pointerCarte]
  )

  const focaliser = useCallback(
    (evenement: ReactFocusEvent<HTMLElement>) => pointerCarte(evenement.target),
    [pointerCarte]
  )

  const perdreFocus = useCallback((evenement: ReactFocusEvent<HTMLElement>) => {
    const prochaine = evenement.relatedTarget
    if (prochaine instanceof Node && evenement.currentTarget.contains(prochaine)) return
    setApercuId(null)
  }, [])

  useEffect(() => {
    const fermerClavier = (evenement: KeyboardEvent) => {
      if (evenement.key === 'Escape') fermer()
    }
    document.addEventListener('keydown', fermerClavier)
    return () => document.removeEventListener('keydown', fermerClavier)
  }, [fermer])

  const carteApercu = apercuId ? cartesParId.get(apercuId) : undefined

  return (
    <div className="plateau-regardees-voile plateau-cibles-menu-voile" onPointerDown={fermer}>
      <section
        className="plateau-regardees plateau-cibles-menu"
        role="dialog"
        aria-label="Possible off-table targets"
        onPointerDown={(evenement) => evenement.stopPropagation()}
        onMouseOver={survoler}
        onMouseLeave={() => setApercuId(null)}
        onFocus={focaliser}
        onBlur={perdreFocus}
      >
        <header className="plateau-regardees-entete">
          <div>
            <span className="plateau-eyebrow">{t('Cibles possibles')}</span>
            <strong>
              {titre} - {cartes.length} card{cartes.length > 1 ? 's' : ''}
            </strong>
          </div>
          <button type="button" onClick={fermer}>
            {t('Fermer')}
          </button>
        </header>
        <div className="plateau-regardees-corps">
          <div className="plateau-regardees-cartes">
            {cartes.map((carte) => (
              <ScanCard {...carte} key={carte.id} />
            ))}
          </div>
        </div>
      </section>
      {carteApercu ? <CarteApercu carte={carteApercu} /> : null}
    </div>
  )
}

/**
 * Outils de la barre du haut : source affichee, joueur regarde, retour a
 * l'ancien plateau. Tout tient sur une ligne : la table a besoin de la hauteur.
 */
function Outils({
  etat,
  playerId,
  catalogueEtats,
  modeActions,
  changerModeActions,
}: {
  etat: string | null
  playerId: number
  catalogueEtats: EntreeCatalogue[]
  modeActions: ModeActions
  changerModeActions: (mode: ModeActions) => void
}) {
  const aller = (nouveau: { etat?: string | null; p?: number }) => {
    const url = new URLSearchParams()
    const prochainEtat = nouveau.etat === undefined ? etat : nouveau.etat
    const prochainJoueur = nouveau.p === undefined ? playerId : nouveau.p
    if (prochainEtat) url.set('etat', prochainEtat)
    if (prochainJoueur !== 0) url.set('p', String(prochainJoueur))
    const requete = url.toString()
    window.location.search = requete ? `?${requete}` : ''
  }

  return (
    <>
      <select
        aria-label={t('État affiché')}
        value={etat ?? ''}
        onChange={(evenement) => aller({ etat: evenement.target.value || null })}
      >
        <option value="">{t('Partie en cours')}</option>
        {catalogueEtats.map((entree) => (
          <option value={entree.fichier} key={entree.fichier}>
            {entree.titre}
          </option>
        ))}
      </select>

      <input
        aria-label={t('Joueur affiché')}
        type="number"
        min={0}
        max={3}
        value={playerId}
        onChange={(evenement) => aller({ p: Number(evenement.target.value) })}
      />

      <div className="mode-actions" role="group" aria-label={t('Mode d’affichage des actions')}>
        <button
          type="button"
          className={modeActions === 'simple' ? 'est-actif' : ''}
          onClick={() => changerModeActions('simple')}
        >
          Simple
        </button>
        <button
          type="button"
          className={modeActions === 'detailed' ? 'est-actif' : ''}
          onClick={() => changerModeActions('detailed')}
        >
          {t('Détaillé')}
        </button>
      </div>

      <a href={`${ANCIEN_PLATEAU}${playerId}`}>{t('Ancien plateau')}</a>
    </>
  )
}

/** Un etat enregistre : chargement unique, aucune interaction. */
function useEtatEnregistre(fichier: string) {
  const [monde, setMonde] = useState<World | undefined>(undefined)
  const [erreur, setErreur] = useState<string | undefined>(undefined)

  useEffect(() => {
    let vivant = true
    setMonde(undefined)
    setErreur(undefined)
    chargerEtat(fichier)
      .then((nouveau) => {
        if (vivant) setMonde(nouveau)
      })
      .catch((cause: unknown) => {
        if (vivant) setErreur(messageDErreur(cause))
      })
    return () => {
      vivant = false
    }
  }, [fichier])

  return { monde, erreur }
}

/** La partie en cours : socket, accuse de reception, demandes du moteur. */
function usePartieEnCours(playerId: number) {
  const [moteur] = useState(() => new Moteur(playerId))
  const [etat, setEtat] = useState<EtatMoteur>({
    hautsFaits: [],
    aNous: false,
    connecte: false,
    validationRequise: false,
    tentatives: 0,
  })

  useEffect(() => {
    const arreter = moteur.ecouter(setEtat)
    moteur.demarrer()
    return () => {
      arreter()
      moteur.arreter()
    }
  }, [moteur])

  const repondre = useCallback(
    (reponse: Reponse | null, bindPlayerId: number) => {
      void moteur.repondre(reponse, bindPlayerId)
    },
    [moteur]
  )

  return {
    etat,
    repondre,
    continuer: () => moteur.continuer(),
    reconnecter: () => moteur.reconnecterMaintenant(),
    reglerPhaseRapide: (actif: boolean) => moteur.setPhaseRapide(actif),
  }
}

/** Metadonnees d'un emplacement de sauvegarde, via /get_replay_json. */
type MetaSauvegarde = { villain?: string; step?: number; time?: string }

async function lireMetaSauvegarde(nom: string): Promise<MetaSauvegarde | undefined> {
  try {
    const reponse = await fetch(`/get_replay_json?${nom}`, { cache: 'no-store' })
    if (!reponse.ok) return undefined
    const brut = (await reponse.json()) as MetaSauvegarde
    return typeof brut === 'object' && brut !== null ? brut : undefined
  } catch {
    return undefined
  }
}

/**
 * Popover de sauvegardes : 3 emplacements nommes (save_1..3.json, comme le
 * client original), chacun avec Save / Load, plus l'export en fichier.
 * Les fichiers vivent dans replays/ (hors .game : ils survivent aux rebuilds).
 */
function PopoverSauvegardes() {
  const [ouvert, setOuvert] = useState(false)
  const [metas, setMetas] = useState<Record<number, MetaSauvegarde | undefined>>({})
  const [occupe, setOccupe] = useState<string | undefined>(undefined)

  const rafraichir = useCallback(() => {
    for (const slot of [1, 2, 3]) {
      void lireMetaSauvegarde(`../replays/save_${slot}.json`).then((meta) =>
        setMetas((m) => ({ ...m, [slot]: meta }))
      )
    }
  }, [])

  const basculer = useCallback(() => {
    setOuvert((o) => {
      if (!o) rafraichir()
      return !o
    })
  }, [rafraichir])

  const sauverSlot = useCallback(
    (slot: number) => {
      setOccupe(`save-${slot}`)
      // Chemin EXPLICITE vers replays/ (hors .game) : la commande /save ecrit
      // sinon dans le repertoire courant, detruit a chaque reconstruction.
      fetch(`/debug?/save ../replays/save_${slot}.json`)
        .then(() => window.setTimeout(rafraichir, 600))
        .catch(() => undefined)
        .finally(() => setOccupe(undefined))
    },
    [rafraichir]
  )

  const chargerSlot = useCallback((slot: number) => {
    if (!window.confirm(`${t('Charger la sauvegarde')} ${slot} ? ${t('La partie en cours sera remplacée.')}`)) return
    setOccupe(`load-${slot}`)
    // `:-1` = reprendre au DERNIER pas enregistre (semantique du client original).
    fetch(`/debug?/load ../replays/save_${slot}.json:-1`)
      .then(() => {
        window.location.href = '/app/board.html?p=0'
      })
      .catch(() => setOccupe(undefined))
  }, [])

  const exporter = useCallback(() => {
    setOccupe('export')
    fetch('/save_replay_data')
      .then((r) => r.json())
      .then((data) => {
        const blob = new Blob([JSON.stringify(data)], { type: 'application/json' })
        const lien = document.createElement('a')
        lien.href = URL.createObjectURL(blob)
        const date = new Date().toISOString().slice(0, 16).replace(/[T:]/g, '-')
        lien.download = `marvel-partie-${date}.json`
        lien.click()
        URL.revokeObjectURL(lien.href)
      })
      .catch(() => undefined)
      .finally(() => setOccupe(undefined))
  }, [])

  return (
    <span className="popover-sauvegardes-ancre">
      <button
        type="button"
        className={`bh-bouton bh-save${ouvert ? ' est-actif' : ''}`}
        onClick={basculer}
        aria-expanded={ouvert}
        title={t('Emplacements de sauvegarde, chargement, export')}
      >
        <span aria-hidden="true">💾</span> {t('Sauver')}
      </button>
      {ouvert ? (
        <div className="popover-sauvegardes" role="menu">
          {[1, 2, 3].map((slot) => {
            const meta = metas[slot]
            return (
              <div className="ligne-sauvegarde" key={slot}>
                <span className="slot-titre">
                  <b>Slot {slot}</b>
                  <small>
                    {meta?.villain
                      ? `${meta.villain} · step ${meta.step ?? '?'}${meta.time ? ` · ${meta.time}` : ''}`
                      : t('Vide')}
                  </small>
                </span>
                <button type="button" onClick={() => sauverSlot(slot)} disabled={occupe !== undefined}>
                  {occupe === `save-${slot}` ? '...' : t('Sauver')}
                </button>
                <button
                  type="button"
                  onClick={() => chargerSlot(slot)}
                  disabled={occupe !== undefined || !meta?.villain}
                >
                  {occupe === `load-${slot}` ? '...' : t('Charger')}
                </button>
              </div>
            )
          })}
          <div className="ligne-sauvegarde">
            <span className="slot-titre">
              <b>{t('Fichier')}</b>
              <small>{t('Télécharger cette partie en .json')}</small>
            </span>
            <button type="button" onClick={exporter} disabled={occupe !== undefined}>
              {occupe === 'export' ? '...' : t('Exporter')}
            </button>
          </div>
        </div>
      ) : null}
    </span>
  )
}

/**
 * Barre de relecture (ouverte via « Watch replay » du wizard : ?revoir=1&pas=N).
 * Navigue dans la partie rejouee via les commandes serveur /goto et /step.
 */
function BarreRevoir({ pasTotal }: { pasTotal: number }) {
  const [position, setPosition] = useState(0)

  const aller = useCallback((pas: number) => {
    setPosition(pas)
    void fetch(`/debug?/goto ${pas}`).catch(() => undefined)
  }, [])

  const avancer = useCallback(() => {
    setPosition((p) => Math.min(p + 1, pasTotal))
    void fetch('/debug?/step 1').catch(() => undefined)
  }, [pasTotal])

  return (
    <div className="barre-revoir" role="toolbar" aria-label={t('Contrôles de relecture')}>
      <span className="revoir-titre">▶ {t('Relecture')}</span>
      <button type="button" onClick={() => aller(0)} title={t('Retour au début')}>
        ⏮
      </button>
      <input
        type="range"
        min={0}
        max={pasTotal}
        value={position}
        onChange={(e) => aller(Number(e.currentTarget.value))}
      />
      <button type="button" onClick={avancer} title={t('Pas suivant')}>
        ▶
      </button>
      <button type="button" onClick={() => aller(pasTotal)} title={t('Aller à la fin')}>
        ⏭
      </button>
      <span className="revoir-position">
        {position}/{pasTotal}
      </span>
    </div>
  )
}

/**
 * Bandeau de reconnexion : visible des que le socket tombe pendant une partie,
 * avec compte a rebours de la prochaine tentative et bouton immediat.
 */
function BandeauConnexion({ etat, reconnecter }: { etat: EtatMoteur; reconnecter: () => void }) {
  const [, forcer] = useState(0)
  useEffect(() => {
    if (etat.connecte) return
    const t = window.setInterval(() => forcer((n) => n + 1), 500)
    return () => window.clearInterval(t)
  }, [etat.connecte])

  if (etat.connecte || !etat.monde) return null
  const restant = etat.prochaineTentative
    ? Math.max(0, Math.ceil((etat.prochaineTentative - Date.now()) / 1000))
    : undefined
  return (
    <div className="bandeau-connexion" role="alert">
      <span aria-hidden="true">⚠</span>
      <span>
        {t('Connexion perdue')}
        {restant !== undefined
          ? ` — ${t('nouvel essai dans')} ${restant}s`
          : ` — ${t('reconnexion...')}`}
        {etat.tentatives > 1 ? ` (${t('essai')} ${etat.tentatives})` : ''}
      </span>
      <button type="button" onClick={reconnecter}>
        {t('Reconnecter maintenant')}
      </button>
    </div>
  )
}

function PageEtat({
  fichier,
  playerId,
  catalogue,
  outils,
}: {
  fichier: string
  playerId: number
  catalogue: Catalogue
  outils: React.ReactNode
}) {
  const { monde, erreur } = useEtatEnregistre(fichier)
  const plateau = useMemo(
    () => (monde ? construirePlateau(monde, { playerId, catalogue }) : undefined),
    [monde, playerId, catalogue]
  )
  const { mode } = useModeMobile()

  if (!monde || !plateau) {
    return (
      <p className="plateau-message" role={erreur ? 'alert' : undefined}>
        {erreur ?? t('Chargement...')}
      </p>
    )
  }

  const Rendu = mode === 'mobile' ? PlateauMobile : Board
  return (
    <Rendu
      world={monde}
      playerId={playerId}
      plateau={plateau}
      source="Saved state, read only"
      outils={outils}
      bas={
        <footer className="plateau-action plateau-action-attente" role="status">
          <strong>Saved state.</strong>
          <span>
            {t('Aucune partie derrière cette vue : rien à jouer. Choisis « Partie en cours » pour agir.')}
          </span>
        </footer>
      }
    />
  )
}

/** Ligne interrupteur du panneau d'options. */
function LigneOption({
  libelle,
  detail,
  actif,
  onBascule,
}: {
  libelle: string
  detail?: string
  actif: boolean
  onBascule: () => void
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={actif}
      className={`ligne-option${actif ? ' est-actif' : ''}`}
      onClick={onBascule}
      title={detail}
    >
      <span className="ligne-option-libelle">{libelle}</span>
      <span className="ligne-option-etat" aria-hidden="true">
        {actif ? t('Oui') : t('Non')}
      </span>
    </button>
  )
}

/** Panneau d'options du plateau : tous les reglages regroupes derriere ⚙. */
function PanneauOptions({
  animations,
  basculerAnimations,
  sons,
  basculerSons,
  musique,
  basculerMusique,
  meteo,
  basculerMeteo,
  revelation,
  cyclerRevelation,
  autoCible,
  basculerAutoCible,
  curseurs,
  basculerCurseurs,
  textesCdb,
  basculerTextesCdb,
  scansFr,
  basculerScansFr,
  succes,
  basculerSucces,
  phaseRapide,
  basculerPhaseRapide,
  validationCourte,
  basculerValidationCourte,
  reglageMode,
  cyclerReglageMode,
}: {
  animations: boolean
  basculerAnimations: () => void
  sons: boolean
  basculerSons: () => void
  musique: boolean
  basculerMusique: () => void
  meteo: boolean
  basculerMeteo: () => void
  revelation: ModeRevelation
  cyclerRevelation: () => void
  autoCible: boolean
  basculerAutoCible: () => void
  curseurs: boolean
  basculerCurseurs: () => void
  textesCdb: boolean
  basculerTextesCdb: () => void
  scansFr: boolean
  basculerScansFr: () => void
  succes: boolean
  basculerSucces: () => void
  phaseRapide: boolean
  basculerPhaseRapide: () => void
  validationCourte: boolean
  basculerValidationCourte: () => void
  reglageMode: ReglageMode
  cyclerReglageMode: () => void
}) {
  const [ouvert, setOuvert] = useState(false)
  return (
    <span className="popover-sauvegardes-ancre">
      <button
        type="button"
        className={`bh-bouton bh-options${ouvert ? ' est-actif' : ''}`}
        onClick={() => setOuvert((o) => !o)}
        aria-expanded={ouvert}
        title={t('Tous les réglages du plateau (animations, sons, musique, météo, révélation)')}
      >
        <span aria-hidden="true">{'\u2699'}</span> {t('Options')}
      </button>
      {ouvert ? (
        <div className="popover-sauvegardes popover-options" role="menu">
          <LigneOption
            libelle={t('Animations')}
            detail={t('Déplacements de cartes, secousse d\u2019impact, halo de statut')}
            actif={animations}
            onBascule={basculerAnimations}
          />
          <LigneOption
            libelle={t('Sons')}
            detail={t('Effets sonores du moteur')}
            actif={sons}
            onBascule={basculerSons}
          />
          <LigneOption
            libelle={t('Musique')}
            detail={t('Musique coupée : déposer musique-<méchant>.mp3 dans assets/sounds puis activer')}
            actif={musique}
            onBascule={basculerMusique}
          />
          <LigneOption
            libelle={t('Succès')}
            detail={t('Bannière quand un exploit est réalisé (Premier sang, Double K.O. ...)')}
            actif={succes}
            onBascule={basculerSucces}
          />
          <LigneOption
            libelle={t('Scans en français')}
            detail={t('Images des cartes en français quand elles existent')}
            actif={scansFr}
            onBascule={basculerScansFr}
          />
          <LigneOption
            libelle={t('Textes marvelcdb (réseau)')}
            detail={t('Texte officiel FR sous l\u2019aperçu des cartes, via fr.marvelcdb.com')}
            actif={textesCdb}
            onBascule={basculerTextesCdb}
          />
          <LigneOption
            libelle={t('Curseurs des autres joueurs')}
            detail={t('En multijoueur, montre où pointent les autres')}
            actif={curseurs}
            onBascule={basculerCurseurs}
          />
          <LigneOption
            libelle={t('Auto-ciblage')}
            detail={t('Sélectionne d\u2019office la cible quand une seule est légale')}
            actif={autoCible}
            onBascule={basculerAutoCible}
          />
          <LigneOption
            libelle={t('Phase du méchant rapide')}
            detail={t('Enchaîne la phase sans « Continue », puis affiche un bilan')}
            actif={phaseRapide}
            onBascule={basculerPhaseRapide}
          />
          <LigneOption
            libelle={t('Validation courte')}
            detail={t('Supprime le « Valider » quand la cible est unique et le coût couvert')}
            actif={validationCourte}
            onBascule={basculerValidationCourte}
          />
          <LigneOption
            libelle={t('Météo')}
            detail={t('Pluie, orage ou neige quand un Soutien météo de Storm est en jeu')}
            actif={meteo}
            onBascule={basculerMeteo}
          />
          <button
            type="button"
            className="ligne-option"
            onClick={cyclerRevelation}
            title={t('Présentation au centre des cartes révélées par la Rencontre')}
          >
            <span className="ligne-option-libelle">{t('Cartes révélées')}</span>
            <span className="ligne-option-etat" aria-hidden="true">
              {revelation === 'off' ? t('Non') : revelation === 'court' ? t('2,6 s') : t('5 s')}
            </span>
          </button>
          <button
            type="button"
            className="ligne-option"
            onClick={cyclerReglageMode}
            title={t('Choix du rendu du plateau : automatique selon l’appareil, ou force mobile/ordinateur')}
          >
            <span className="ligne-option-libelle">{t('Disposition')}</span>
            <span className="ligne-option-etat" aria-hidden="true">
              {reglageMode === 'auto'
                ? t('Automatique')
                : reglageMode === 'mobile'
                  ? t('Mobile')
                  : t('Ordinateur')}
            </span>
          </button>
          <p className="options-raccourcis">
            {t('Raccourcis : E = fin du tour, U = annuler')}
          </p>
        </div>
      ) : null}
    </span>
  )
}

/** Ecran de fin de partie : victoire ou defaite, avec retour au menu. */
function EcranFinPartie({
  gagne,
  raison,
  monde,
  hautsFaits,
  onMenu,
}: {
  gagne: boolean
  raison?: string
  monde?: World
  /** Titres débloqués pendant cette session, accumulés par Moteur. */
  hautsFaits: string[]
  onMenu: () => void
}) {
  const heros = (monde?.players ?? [])
    .map((joueur) => joueur.area_hero?.[0]?.name?.replace(/^\W*/, ''))
    .filter((nom): nom is string => Boolean(nom))
  const rounds = monde?.round_id
  const mechants = (monde?.area_villain ?? []).map((carte) => carte.name).filter(Boolean)
  return (
    <div
      className={`fin-partie ${gagne ? 'est-victoire' : 'est-defaite'}`}
      role="dialog"
      aria-modal="true"
      aria-label={gagne ? t('Victoire') : t('Défaite')}
    >
      {gagne ? (
        <div className="fin-partie-confettis" aria-hidden="true">
          {Array.from({ length: 24 }, (_, i) => (
            <span key={i} style={{ '--i': i } as React.CSSProperties} />
          ))}
        </div>
      ) : null}
      <div className="fin-partie-carte">
        <span className="fin-partie-eyebrow">{gagne ? t('Victoire') : t('Défaite')}</span>
        <strong className="fin-partie-titre">
          {gagne ? t('Les héros l\u2019emportent !') : t('Les héros sont vaincus')}
        </strong>
        {raison ? <span className="fin-partie-raison">{raison}</span> : null}
        {heros.length || mechants.length ? (
          <span className="fin-partie-detail">
            {heros.join(', ')}
            {mechants.length ? ` ${t('contre')} ${[...new Set(mechants)].join(', ')}` : ''}
            {rounds ? ` · ${rounds} ${t('round(s)')}` : ''}
          </span>
        ) : null}
        {hautsFaits.length ? (
          <section className="fin-partie-hauts-faits">
            <span className="fin-partie-eyebrow">
              {t('Hauts faits débloqués')} · {hautsFaits.length}
            </span>
            <ul>
              {hautsFaits.map((titre) => (
                <li key={titre}>
                  <span aria-hidden="true">{'\u{1F396}'}</span>
                  {titre}
                </li>
              ))}
            </ul>
          </section>
        ) : null}
        <button type="button" className="fin-partie-menu" onClick={onMenu}>
          {t('Retour au menu')}
        </button>
      </div>
    </div>
  )
}

function PagePartie({
  playerId,
  catalogue,
  outils,
  modeActions,
}: {
  playerId: number
  catalogue: Catalogue
  outils: React.ReactNode
  modeActions: ModeActions
}) {
  const { etat, repondre, continuer, reconnecter, reglerPhaseRapide } = usePartieEnCours(playerId)
  // Fin de tour SUGGEREE : le moteur nous interroge, mais aucune option n'est
  // reellement jouable (toutes portent une failure_reason). Le bouton End Turn
  // devient vert et pulse — jamais d'auto-pass, le joueur garde la main.
  const finDeTourSuggeree = useMemo(() => {
    const options = etat.demande?.options
    if (!etat.aNous || !options || options.length === 0) return false
    return options.every((option) => option.failure_reason !== '')
  }, [etat.aNous, etat.demande])

  // Mode « revoir » (lecteur de replay) : ouvert par le wizard avec
  // ?revoir=1&pas=<nombre de pas enregistres>.
  const modeRevoir = useMemo(() => {
    const url = new URLSearchParams(window.location.search)
    if (url.get('revoir') !== '1') return undefined
    const pas = Number(url.get('pas') ?? '0')
    return { pas: Number.isFinite(pas) && pas > 0 ? pas : 0 }
  }, [])
  // HOT-SEAT : un seul ecran joue tous les heros. La vue (main affichee,
  // visibilite, interactions) suit le joueur que le moteur interroge...
  // ...sauf si le joueur FORCE la vue sur un heros precis (regarder la main de
  // l'autre). Auto = null.
  const [vueForcee, setVueForcee] = useState<number | null>(null)
  const joueurActif = vueForcee ?? etat.joueurDemande ?? playerId
  const effets = useEffetsCartes(etat.monde)
  // Declare AVANT le useMemo de `plateau` : il en est une dependance, pour
  // que decocher l'option en pleine partie rafraichisse l'affichage sans
  // attendre le prochain evenement du moteur.
  const [scansFr, setScansFr] = useState(scansFrActifs)

  // La table est decoupee AVANT l'interaction : celle-ci a besoin de savoir
  // quelles cartes sont reellement dessinees pour ne rendre cliquable que ce qui
  // se voit, et renvoyer le reste au selecteur.
  const plateau = useMemo(
    () =>
      etat.monde
        ? construirePlateau(etat.monde, { playerId: joueurActif, catalogue })
        : undefined,
    [etat.monde, joueurActif, catalogue, scansFr]
  )
  const interaction = useInteraction(
    etat.monde,
    etat.demande,
    repondre,
    plateau?.idsAffiches ?? AUCUN_ID,
    joueurActif,
    catalogue,
    modeActions
  )
  const groupesRegardes = useMemo(
    () => (etat.monde ? cartesRegardees(etat.monde, joueurActif, catalogue) : []),
    [etat.monde, joueurActif, catalogue]
  )
  const cartesMondeParId = useMemo(() => indexerCartesMonde(etat.monde), [etat.monde])
  const cartesAfficheesParId = useMemo(() => indexerCartesAffichees(plateau), [plateau])
  const [optionSurvolee, setOptionSurvolee] = useState<Option | undefined>(undefined)
  const [pulseTemporaire, setPulseTemporaire] = useState<Set<number>>(() => new Set())
  const [ciblesMenu, setCiblesMenu] = useState<{ titre: string; cartes: ScanCardProps[] } | undefined>(
    undefined
  )
  const minuteurPulse = useRef<number | undefined>(undefined)

  useEffect(
    () => () => {
      window.clearTimeout(minuteurPulse.current)
    },
    []
  )

  const ciblesPulseesSurvol = useMemo(
    () => idsPulsePourOption(optionSurvolee, plateau, interaction.cibleFocus),
    [optionSurvolee, plateau, interaction.cibleFocus]
  )
  const ciblesPulseesPhaseEnnemie = useMemo(
    () => idsPulsePourDemandeEnnemie(etat.monde, etat.demande, plateau),
    [etat.monde, etat.demande, plateau]
  )
  const ciblesPulsees = useMemo(() => {
    const ids = new Set(ciblesPulseesSurvol)
    for (const id of ciblesPulseesPhaseEnnemie) ids.add(id)
    for (const id of pulseTemporaire) ids.add(id)
    return ids
  }, [ciblesPulseesSurvol, ciblesPulseesPhaseEnnemie, pulseTemporaire])
  const interactifsAvecPulse = useMemo(
    () => ajouterPulse(interaction.cartes, ciblesPulsees),
    [interaction.cartes, ciblesPulsees]
  )
  const representantsPulseHorsTable = useMemo(() => {
    const representants = new Set<number>()
    if (!optionAvecCibles(optionSurvolee) || !plateau || interaction.cibleFocus !== undefined) {
      return representants
    }
    for (const cible of new Set(optionSurvolee.all_legal_targets)) {
      if (plateau.idsAffiches.has(cible)) continue
      const representant = plateau.representantsDePile.get(cible)
      if (representant !== undefined) representants.add(representant)
    }
    return representants
  }, [optionSurvolee, plateau, interaction.cibleFocus])

  const choisirOptionDepuisMenu = useCallback(
    (option: Option, ciblesInitiales?: number[]) => {
      const ids = idsPulsePourOption(option, plateau, ciblesInitiales?.[0])
      setPulseTemporaire(ids)
      setOptionSurvolee(undefined)
      window.clearTimeout(minuteurPulse.current)
      minuteurPulse.current = window.setTimeout(() => setPulseTemporaire(new Set()), 1000)
      interaction.choisirOption(option, ciblesInitiales)
    },
    [interaction, plateau]
  )

  const ouvrirCiblesHorsTable = useCallback(
    (option: Option | undefined) => {
      if (!option || !plateau) return false
      const cartes = ciblesHorsTablePourOption(option, cartesMondeParId, plateau, joueurActif, catalogue)
      if (cartes.length === 0) return false
      setCiblesMenu({ titre: nomLisible(option), cartes })
      return true
    },
    [cartesMondeParId, catalogue, plateau, joueurActif]
  )

  const [apercuSelecteur, setApercuSelecteur] = useState<ScanCardProps | undefined>(undefined)

  // Le selecteur se demonte des qu'une cible est choisie. React n'emet aucun
  // onMouseLeave sur un composant demonte : sans ce nettoyage, l'apercu resterait
  // fige sur la derniere carte survolee, par-dessus la table et sans plus jamais
  // se mettre a jour.
  const selecteurOuvert = interaction.ciblesHorsTable.length > 0
  useEffect(() => {
    if (!selecteurOuvert) setApercuSelecteur(undefined)
  }, [selecteurOuvert])

  const { mode: modePlateau, reglage: reglageMode, changer: changerReglageMode } = useModeMobile()
  const cyclerReglageMode = useCallback(() => {
    changerReglageMode(
      reglageMode === 'auto' ? 'mobile' : reglageMode === 'mobile' ? 'pc' : 'auto'
    )
  }, [reglageMode, changerReglageMode])

  const [animations, setAnimations] = useState(lireAnimations)
  const basculerAnimations = useCallback(() => {
    setAnimations((a) => {
      const nouveau = !a
      try {
        window.localStorage.setItem(CLE_ANIMATIONS, nouveau ? 'on' : 'off')
      } catch {
        /* localStorage indisponible : le choix ne survivra pas au rechargement. */
      }
      return nouveau
    })
  }, [])
  const historique = useHistoriquePartie(etat.monde, etat.demande, etat.partieId)

  const [sons, setSons] = useState(lireSons)
  const basculerSons = useCallback(() => {
    setSons((s) => {
      const nouveau = !s
      try {
        window.localStorage.setItem(CLE_SONS, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [meteo, setMeteo] = useState(lireMeteoActive)
  const basculerMeteo = useCallback(() => {
    setMeteo((m) => {
      const nouveau = !m
      try {
        window.localStorage.setItem(CLE_METEO, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [succes, setSucces] = useState(lireSuccesActifs)
  const basculerSucces = useCallback(() => {
    setSucces((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_SUCCES, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [textesCdb, setTextesCdb] = useState(lireTextesCdb)
  const basculerTextesCdb = useCallback(() => {
    setTextesCdb((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_TEXTES_CDB, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const basculerScansFr = useCallback(() => {
    setScansFr((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_SCANS_FR, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [curseurs, setCurseurs] = useState(lireCurseursActifs)
  const basculerCurseurs = useCallback(() => {
    setCurseurs((c) => {
      const nouveau = !c
      try {
        window.localStorage.setItem(CLE_CURSEURS, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [autoCible, setAutoCible] = useState(lireAutoCible)
  const basculerAutoCible = useCallback(() => {
    setAutoCible((a) => {
      const nouveau = !a
      try {
        window.localStorage.setItem(CLE_AUTO_CIBLE, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [validationCourte, setValidationCourte] = useState(lireValidationCourte)
  const basculerValidationCourte = useCallback(() => {
    setValidationCourte((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_VALIDATION_COURTE, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [phaseRapide, setPhaseRapide] = useState(lirePhaseRapide)
  const basculerPhaseRapide = useCallback(() => {
    setPhaseRapide((p) => {
      const nouveau = !p
      try {
        window.localStorage.setItem(CLE_PHASE_RAPIDE, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  // Le reglage vit dans le composant, mais c'est le Moteur qui retient (ou non)
  // l'accuse de reception : il faut le lui redire a chaque changement.
  useEffect(() => {
    reglerPhaseRapide(phaseRapide)
  }, [phaseRapide, reglerPhaseRapide])

  const [musique, setMusique] = useState(lireMusiqueActive)
  const basculerMusique = useCallback(() => {
    setMusique((m) => {
      const nouveau = !m
      try {
        window.localStorage.setItem(CLE_MUSIQUE, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [revelation, setRevelation] = useState<ModeRevelation>(lireRevelation)
  const cyclerRevelation = useCallback(() => {
    setRevelation((r) => {
      const suivant: ModeRevelation = r === 'off' ? 'court' : r === 'court' ? 'long' : 'off'
      try {
        window.localStorage.setItem(CLE_REVELATION, suivant)
      } catch {
        /* preference non critique */
      }
      return suivant
    })
  }, [])

  // Les effets CSS transitoires (secousse d'impact, halo de statut) sont
  // debrayes par une classe sur <body> : ils vivent dans des feuilles de style,
  // pas dans des composants qu'on peut couper par prop.
  useEffect(() => {
    document.body.classList.toggle('plateau-sans-animations', !animations)
    return () => document.body.classList.remove('plateau-sans-animations')
  }, [animations])

  useSons(etat.monde, sons, etat.demande !== undefined)
  useMusique(etat.monde, musique)

  // Raccourcis clavier : E = fin du tour (quand le bouton simple est visible),
  // U = annuler la derniere action. Ignorés pendant une saisie ou avec un
  // modificateur. HOOKS DECLARES ICI, avant le retour anticipe « monde pas
  // charge » : sinon le nombre de hooks change entre deux rendus (React #310).
  // La cible reelle du raccourci E est assignee plus bas, une fois
  // afficherFinTourSimple connu, via ce ref.
  const finTourClavier = useRef<() => void>(() => {})
  useEffect(() => {
    const surTouche = (evenement: KeyboardEvent) => {
      if (evenement.ctrlKey || evenement.metaKey || evenement.altKey) return
      const cible = evenement.target as HTMLElement | null
      if (cible && (cible.tagName === 'INPUT' || cible.tagName === 'TEXTAREA' || cible.isContentEditable)) return
      const touche = evenement.key.toLowerCase()
      if (touche === 'e') {
        finTourClavier.current()
      } else if (touche === 'u') {
        fetch('/debug?/undo auto').catch(() => undefined)
      }
    }
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [])
  useHaloStatut(etat.monde, animations)

  const annulerCoup = useCallback(() => {
    // « /undo auto » remonte au dernier point de decision, comme le bouton Undo
    // du client d'origine. L'espace est encode par fetch, le '/' est conserve.
    fetch('/debug?/undo auto').catch(() => undefined)
  }, [])

  const retourMenu = useCallback(() => {
    window.location.href = '/prepare.html'
  }, [])

  const retourMenuPrincipal = useCallback(() => {
    if (window.confirm('Return to the main menu? Save first if you want to keep this game.')) {
      window.location.href = '/prepare.html'
    }
  }, [])

  const effetCentrale = useMemo(() => {
    const premier = effets.entries().next().value as [number, CardEffectDelta] | undefined
    if (!premier) return undefined
    const [id, effet] = premier
    const carte = cartesMondeParId.get(id)
    if (!carte) return undefined
    const valeur = Math.abs(effet.value)
    if (effet.kind === 'damage') return `${carte.name} takes ${valeur} damage`
    if (effet.kind === 'heal') return `${carte.name} heals ${valeur}`
    return effet.value > 0
      ? `${carte.name} gains ${valeur} threat`
      : `${carte.name} loses ${valeur} threat`
  }, [effets, cartesMondeParId])

  if (!etat.monde || !plateau) {
    return (
      <p className="plateau-message" role={etat.erreur ? 'alert' : undefined}>
        {etat.erreur ?? 'Connecting to the game...'}
      </p>
    )
  }

  const idMenu = interaction.carteFocus ?? interaction.cibleFocus
  const carteMenu = idMenu !== undefined ? cartesAfficheesParId.get(idMenu) : undefined
  const modeMenu = interaction.cibleFocus !== undefined ? 'target' : 'source'
  const identiteJoueurId = etat.monde.players?.[joueurActif]?.area_hero?.[0]?.id
  // Badge « Active » : identite du joueur que le moteur interroge. Sans objet en
  // solo (un seul heros, toujours actif).
  const heroActifId =
    (etat.monde.players?.length ?? 0) > 1 && etat.joueurDemande !== undefined
      ? etat.monde.players?.[etat.joueurDemande]?.area_hero?.[0]?.id
      : undefined
  const menuIdentiteJoueur =
    modeMenu === 'source' &&
    carteMenu !== undefined &&
    identiteJoueurId !== undefined &&
    Number(carteMenu.id) === identiteJoueurId
  const libelleAnnulationMenu =
    etat.demande?.event_name === 'WhenPlayerInTurn' && etat.demande.ability_type === 'Normal'
      ? 'End Turn'
      : 'Pass'
  const afficherDemandeCentrale =
    etat.aNous &&
    etat.connecte &&
    etat.demande !== undefined &&
    effets.size === 0 &&
    !etat.validationRequise &&
    !interaction.option &&
    !carteMenu &&
    demandeDoitApparaitreAuCentre(etat.demande)
  const afficherEvenementCentrale =
    etat.connecte &&
    (etat.validationRequise ||
      effets.size > 0 ||
      (etat.monde.phase === 'Enemy Activation' && evenementNarreImportant(etat.monde))) &&
    !afficherDemandeCentrale &&
    !interaction.option &&
    !carteMenu

  // Mode simple : la barre du bas disparait. Il reste juste un bouton flottant
  // « End Turn » quand on est en phase libre (sinon plus aucun moyen visible de
  // finir son tour ; le clic-sur-heros le permet aussi, mais c'est moins evident).
  const afficherFinTourSimple =
    modeActions === 'simple' &&
    etat.aNous &&
    etat.connecte &&
    etat.demande !== undefined &&
    etat.demande.show_cancel &&
    !demandeDoitApparaitreAuCentre(etat.demande) &&
    !interaction.option &&
    !carteMenu

  finTourClavier.current = () => {
    if (afficherFinTourSimple) interaction.annuler()
  }

  const RenduPartie = modePlateau === 'mobile' ? PlateauMobile : Board

  return (
    <>
      {etat.erreur ? (
        <p className="plateau-message" role="alert">
          {etat.erreur}
        </p>
      ) : null}

      <SplashTour monde={etat.monde} />

      <CoucheCoach monde={etat.monde} />

      <SelecteurCibles
        cibles={interaction.ciblesHorsTable}
        titre={interaction.option ? nomLisible(interaction.option) : ''}
        survoler={setApercuSelecteur}
      />
      {apercuSelecteur ? <CarteApercu carte={apercuSelecteur} /> : null}
      {interaction.ciblesHorsTable.length === 0 && !interaction.option ? (
        <ModaleCartesRegardees groupes={groupesRegardes} />
      ) : null}

      {ciblesMenu ? (
        <ModaleCiblesMenu
          titre={ciblesMenu.titre}
          cartes={ciblesMenu.cartes}
          fermer={() => setCiblesMenu(undefined)}
        />
      ) : null}

      {afficherDemandeCentrale && etat.demande ? (
        <DemandeCentrale
          demande={etat.demande}
          options={interaction.options}
          cartesParId={cartesMondeParId}
          choisirOption={choisirOptionDepuisMenu}
          annuler={interaction.annuler}
          survolerOption={setOptionSurvolee}
        />
      ) : null}

      {afficherEvenementCentrale ? (
        <EvenementCentrale
          prompt={etat.monde.prompt}
          eventName={etat.monde.event_name}
          message={effetCentrale}
          validationRequise={etat.validationRequise}
          continuer={continuer}
        />
      ) : null}

      {carteMenu && !interaction.option ? (
        <MenuActionsCarte
          carte={carteMenu}
          carteMonde={cartesMondeParId.get(Number(carteMenu.id))}
          options={interaction.options}
          toutesOptions={etat.demande?.options ?? []}
          cartesParId={cartesMondeParId}
          catalogue={catalogue}
          choisirOption={choisirOptionDepuisMenu}
          annulerDemande={
            menuIdentiteJoueur && etat.demande?.show_cancel ? interaction.annuler : undefined
          }
          libelleAnnulation={libelleAnnulationMenu}
          fermer={interaction.defocaliser}
          playerId={joueurActif}
          survolerOption={setOptionSurvolee}
          idsAffiches={plateau.idsAffiches}
          ouvrirCiblesHorsTable={ouvrirCiblesHorsTable}
          mode={modeMenu}
          ciblePreselectionnee={interaction.cibleFocus}
          affichage={modeActions}
        />
      ) : null}

      <AssistantAction
        demande={etat.demande}
        interaction={interaction}
        aNous={etat.aNous}
        connecte={etat.connecte}
        cartesParId={cartesMondeParId}
        affichage={modeActions}
      />

      <CoucheMeteo world={etat.monde} active={meteo} />
      <CoucheSucces monde={etat.monde} demande={etat.demande} actif={succes} />
      <CoucheHautsFaits hautsFaits={etat.hautsFaits} />
      <RecapPhaseMechant entrees={historique.entrees} monde={etat.monde} actif={phaseRapide} />
      <CoucheCurseurs
        actif={curseurs && (etat.monde?.players?.length ?? 0) > 1}
        monJoueur={playerId}
        nomsJoueurs={(etat.monde?.players ?? []).map(
          (joueur, i) => joueur.area_hero?.[0]?.name?.replace(/^\W*/, '') ?? `J${i}`
        )}
      />

      <RenduPartie
        world={etat.monde}
        playerId={joueurActif}
        plateau={plateau}
        effets={effets}
        heroActifId={heroActifId}
        // Meme condition que le rendu de MenuActionsCarte ci-dessus : le rendu
        // mobile empile une couche tant que ce menu est affiche, pour que le
        // Retour d'Android le ferme au lieu de sortir de la partie.
        carteFocalisee={carteMenu && !interaction.option ? idMenu : undefined}
        onFermerCarte={interaction.defocaliser}
        // Meme condition que le rendu de SelecteurCibles ci-dessus (il ne
        // dessine rien sans cible). Le Retour abandonne l'option en cours de
        // composition : le menu de la carte revient, on n'a pas quitte la
        // partie au milieu d'un ciblage.
        selecteurOuvert={interaction.ciblesHorsTable.length > 0}
        onFermerSelecteur={interaction.abandonnerOption}
        journal={
          <JournalHeros
            entrees={historique.entrees}
            monde={etat.monde}
            joueur={joueurActif}
            nomHeros={etat.monde.players?.[joueurActif]?.area_hero?.[0]?.name?.replace(/^\W*/, '')}
          />
        }
        source={t('Partie en cours')}
        outils={outils}
        actionsPartie={
          <div className="board-actions">
            <button
              type="button"
              className="bh-bouton bh-undo"
              onClick={annulerCoup}
              title={t('Annuler la dernière action')}
            >
              {/* « Annuler » se traduit ici « Undo » (le dictionnaire réserve
                  « Annuler » -> « Cancel » pour l'assistant d'action). */}
              <span aria-hidden="true">↶</span> {langueActuelle() === 'fr' ? 'Annuler' : 'Undo'}
            </button>
            <PopoverSauvegardes />
            <PanneauOptions
              animations={animations}
              basculerAnimations={basculerAnimations}
              sons={sons}
              basculerSons={basculerSons}
              musique={musique}
              basculerMusique={basculerMusique}
              meteo={meteo}
              basculerMeteo={basculerMeteo}
              revelation={revelation}
              cyclerRevelation={cyclerRevelation}
              autoCible={autoCible}
              basculerAutoCible={basculerAutoCible}
              curseurs={curseurs}
              basculerCurseurs={basculerCurseurs}
              textesCdb={textesCdb}
              basculerTextesCdb={basculerTextesCdb}
              scansFr={scansFr}
              basculerScansFr={basculerScansFr}
              succes={succes}
              basculerSucces={basculerSucces}
              phaseRapide={phaseRapide}
              basculerPhaseRapide={basculerPhaseRapide}
              validationCourte={validationCourte}
              basculerValidationCourte={basculerValidationCourte}
              reglageMode={reglageMode}
              cyclerReglageMode={cyclerReglageMode}
            />
            {(etat.monde?.players?.length ?? 0) > 1 ? (
              <span className="bh-vue" title={t('Quel héros est affiché (plateau et main)')}>
                <span className="bh-vue-label">{t('Vue')}</span>
                <button
                  type="button"
                  className={`bh-bouton${vueForcee === null ? ' est-actif' : ''}`}
                  title={t('Suivre celui qui doit agir')}
                  onClick={() => setVueForcee(null)}
                >
                  Auto
                </button>
                {etat.monde!.players.map((joueur, i) => (
                  <button
                    type="button"
                    key={i}
                    className={`bh-bouton${vueForcee === i ? ' est-actif' : ''}${joueurActif === i ? ' est-joueur-actif' : ''}`}
                    title={joueur.area_hero?.[0]?.name ?? `${t('Joueur')} ${i}`}
                    onClick={() => setVueForcee(i)}
                  >
                    {joueur.area_hero?.[0]?.name?.replace(/^\W*/, '').split(' ')[0] ?? `P${i}`}
                  </button>
                ))}
              </span>
            ) : null}
            <HistoriquePartie entrees={historique.entrees} effacer={historique.effacer} />
            <button
              type="button"
              className="bh-bouton bh-langue"
              onClick={() => void basculerLangue()}
              title={
                langueActuelle() === 'fr'
                  ? 'Interface et narration en français — cliquer pour passer en anglais'
                  : 'Interface and narration in English — click to switch to French'
              }
            >
              <span aria-hidden="true">🌐</span> {langueActuelle() === 'fr' ? 'FR' : 'EN'}
            </button>
            <button
              type="button"
              className="bh-bouton bh-menu"
              onClick={retourMenuPrincipal}
              title={t('Revenir au menu principal')}
            >
              <span aria-hidden="true">⌂</span> Menu
            </button>
          </div>
        }
        interactifs={interactifsAvecPulse}
        bloquerActionsPassives={interaction.option !== undefined}
        mainVisibleForcee={
          interaction.option !== undefined &&
          (interaction.assistant.etape === 'target' || interaction.assistant.etape === 'payment')
        }
        onCardClick={
          etat.aNous && etat.connecte && !interaction.option
            ? (carte) => {
                const id = Number(carte.id)
                if (representantsPulseHorsTable.has(id) && ouvrirCiblesHorsTable(optionSurvolee)) {
                  return
                }
                if (modeActions === 'simple') {
                  const optionsSource = etat.demande?.options.filter((option) => option.bind_id === id) ?? []
                  const identiteId = etat.monde?.players?.[joueurActif]?.area_hero?.[0]?.id
                  const aActionsGenerales =
                    id === identiteId && (etat.demande?.options.some((option) => option.bind_id === 0) ?? false)
                  const peutFinirTour =
                    id === identiteId && etat.demande?.show_cancel === true
                  if (optionsSource.length > 0 || aActionsGenerales || peutFinirTour) {
                    interaction.focaliserCarte(id)
                  }
                  return
                }
                const carteMonde = cartesMondeParId.get(id)
                const actionsVersCible = optionsDisponiblesVersCible(etat.demande?.options ?? [], id)
                if (actionsVersCible.length === 1) {
                  choisirOptionDepuisMenu(actionsVersCible[0]!, [id])
                  return
                }
                if (actionsVersCible.length > 1 || estCibleExpliquee(carteMonde)) {
                  interaction.focaliserCible(id)
                  return
                }
                interaction.focaliserCarte(id)
              }
            : undefined
        }
        bas={
          modeActions === 'detailed' ? (
            <BarreAction
              demande={etat.demande}
              interaction={interaction}
              aNous={etat.aNous}
              connecte={etat.connecte}
              nomPorteur={(bindId) => nomDeCarte(etat.monde, bindId)}
            />
          ) : undefined
        }
      />

      {afficherFinTourSimple ? (
        <button
          type="button"
          className={`bouton-fin-tour${finDeTourSuggeree ? ' est-suggere' : ''}`}
          onClick={interaction.annuler}
          title={
            finDeTourSuggeree
              ? t('Plus rien n\u2019est jouable — termine ton tour')
              : t('Terminer ton tour')
          }
        >
          {t('Fin du tour')}{finDeTourSuggeree ? ' ✓' : ''}
        </button>
      ) : null}

      <BandeauConnexion etat={etat} reconnecter={reconnecter} />
      {modeRevoir ? <BarreRevoir pasTotal={modeRevoir.pas} /> : null}
      <CoucheAnimations renderId={etat.monde.render_id} actif={animations} />
      <CoucheRevelation
        monde={etat.monde}
        duree={DUREES_REVELATION[revelation]}
        joueurId={joueurActif}
      />
      <CoucheCharge
        renderId={etat.monde.render_id}
        eventName={etat.monde.event_name ?? ''}
        activeIds={etat.monde.active_card_ids ?? []}
        actif={animations}
      />

      {etat.monde?.game_over ? (
        <EcranFinPartie
          gagne={Boolean(etat.monde.players_won)}
          raison={etat.monde.game_over_reason}
          monde={etat.monde}
          hautsFaits={etat.hautsFaits}
          onMenu={retourMenu}
        />
      ) : null}
    </>
  )
}

function Page() {
  const { etat, playerId } = parametres()
  // Le catalogue ne fait que completer les pastilles PV (« 1/3 » au lieu de
  // « 1 ») : le plateau ne l'attend pas pour s'afficher.
  const [catalogue, setCatalogue] = useState<Catalogue>(catalogueVide)
  const [catalogueEtats, setCatalogueEtats] = useState<EntreeCatalogue[]>([])
  const [modeActions, setModeActions] = useState<ModeActions>(() => lireModeActions())

  useEffect(() => {
    chargerCatalogue().then(setCatalogue).catch(() => undefined)
    chargerCatalogueEtats().then(setCatalogueEtats).catch(() => setCatalogueEtats([]))
  }, [])

  const changerModeActions = useCallback((mode: ModeActions) => {
    setModeActions(mode)
    try {
      window.localStorage.setItem(CLE_MODE_ACTIONS, mode)
    } catch {
      // Preference non critique : si le navigateur refuse localStorage, le mode
      // simple par defaut reste utilisable.
    }
  }, [])

  const outils = (
    <Outils
      etat={etat}
      playerId={playerId}
      catalogueEtats={catalogueEtats}
      modeActions={modeActions}
      changerModeActions={changerModeActions}
    />
  )

  return etat ? (
    <PageEtat fichier={etat} playerId={playerId} catalogue={catalogue} outils={outils} />
  ) : (
    <PagePartie playerId={playerId} catalogue={catalogue} outils={outils} modeActions={modeActions} />
  )
}

// Le serveur de developpement peut reexecuter ce module sans recharger la page
// (reoptimisation des dependances, mise a jour a chaud). Un second createRoot sur
// le meme noeud casse le rendu : « container that has already been passed to
// createRoot », puis un removeChild qui vide la page. On garde donc la racine.
declare global {
  interface Window {
    racinePlateau?: Root
  }
}

const cible = document.getElementById('plateau')
if (!cible) throw new Error('Element #plateau not found in board.html')
synchroniserLangueServeur()
window.racinePlateau ??= createRoot(cible)
window.racinePlateau.render(<Page />)
