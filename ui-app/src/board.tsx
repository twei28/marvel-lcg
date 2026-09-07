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
import { CoucheTriche, useTriche } from './board/CoucheTriche'
import { useSons } from './board/sons'
import { useHaloStatut } from './board/halo-statut'
import { catalogueVide, chargerCatalogue, type Catalogue } from './board/catalogue'
import { kindOf, pvMaximum, toScanCard, type ContexteCarte } from './board/card-model'
import { carteNommeeParOption, indexerCartesMondeParNom } from './board/option-carte'
import {
  DemandeCentrale,
  EvenementCentrale,
  demandeDoitApparaitreAuCentre,
  moteurAttendUneReponse,
} from './board/DemandeCentrale'
import { HistoriquePartie, useHistoriquePartie } from './board/HistoriquePartie'
import { PanneauSalon } from './board/PanneauSalon'
import { peutSuivre } from './board/suivi-vue'
import { traduireMoteur } from './board/vocabulaire-moteur'
import {
  afficherFinDePartie,
  coupFatalLocal,
  DELAI_FILET_FIN_PARTIE_MS,
  finDePartie,
} from './board/fin-partie'
import { installerCollecteErreurs } from './board/erreurs-console'
import { MessageRapport, useRapportBug } from './board/RapportBug'
import { PanneauBug } from './board/PanneauBug'
import { AttenteTable } from './board/AttenteTable'
import { joueurAttendu, joueurEnRetard, useTableSilencieuse } from './board/attente-table'
import { BandeauAbsent } from './board/BandeauAbsent'
import { JournalHeros } from './board/JournalHeros'
import { RecapPhaseMechant } from './board/RecapPhaseMechant'
import { DeroulePhase } from './board/DeroulePhase'
import { BandeauPhase } from './board/BandeauPhase'
import { etapesDeroule, nomNettoye } from './board/deroule-phase'
import { SplashTour } from './board/SplashTour'
import {
  CLE_AUTO_CIBLE,
  CLE_VALIDATION_COURTE,
  lireAutoCible,
  lireValidationCourte,
  useInteraction,
  type EtatInteractif,
} from './board/interaction'
import { MenuActionsCarte } from './board/MenuActionsCarte'
import { FournisseurConfirmation, useConfirmation } from './board/ConfirmationJeu'
import { basculerLangue, langueActuelle, synchroniserLangueServeur, t } from './board/langue'
import { CLE_TEXTES_CDB, lireTextesCdb } from './board/marvelcdb'
import { CLE_SCANS_FR, scansFrActifs } from './board/scans-fr'
import {
  CoucheMeteo,
  CLE_METEO,
  EFFETS_DELAVANTS,
  effetsAffiches,
  type ApercuMeteo,
  lireMeteoActive,
  basculerAmbiance,
  ReglagesApercuAmbiance,
} from './board/CoucheMeteo'
import { ModaleAmbiance } from './board/ModaleAmbiance'
import { CoucheCurseurs, CLE_CURSEURS, lireCurseursActifs } from './board/CoucheCurseurs'
import { PanneauRecompenses } from './board/campagne/PanneauRecompenses'
import { CoucheSucces, CLE_SUCCES, lireSuccesActifs } from './board/CoucheSucces'
import { CLE_MUSIQUE, lireMusiqueActive, useMusique } from './board/musique'
import {
  Moteur,
  PHASES_DU_MECHANT,
  estMultijoueur,
  evenementNarreImportant,
  ecrireAvanceAuto,
  ecrireDelaiPasAPas,
  ecrireModePhaseMechant,
  ecrireReponseAmbiance,
  libelleModePhase,
  lireAvanceAuto,
  lireDelaiPasAPas,
  lireModePhaseMechant,
  lireReponseAmbiance,
  migrerReglagesPhase,
  DELAI_PAS_A_PAS_MAX,
  DELAI_PAS_A_PAS_MIN,
  type EtatMoteur,
  type ModePhaseMechant,
  type ReponseAmbiance,
} from './board/moteur'
// CouchePasAPas et usePasAPas : DEBRANCHES a la demande de l'utilisateur, voir
// les commentaires a leurs points d'appel plus bas pour les rallumer.
import { SelecteurCibles } from './board/SelecteurCibles'
import { nomLisible } from './board/BarreAction'
import { construirePlateau, type Plateau } from './board/zones'
import type { Demande, Option, Reponse } from './board/ask'
import {
  chargerEtat,
} from './board/sources'
import { isScheme, isUnit, isVisibleFor, type World, type WorldCard } from './board/world'

// Migration EXPLICITE des anciens reglages de la phase du mechant (voir
// moteur.ts, `migrerReglagesPhase`), faite UNE FOIS, ici, a l'evaluation du
// module. C'est le plus tot possible : avant meme le montage du composant,
// donc forcement avant les `useState(lireModePhaseMechant)` /
// `useState(lireAvanceAuto)` plus bas, qui n'appellent leur lecteur qu'a
// l'initialisation du premier rendu. Un appel loge dans le corps du composant
// aurait couru un risque inutile (React StrictMode invoque deux fois le corps
// du composant en developpement), alors qu'ici l'evaluation du module n'a
// lieu qu'une fois par chargement de page - et la fonction est de toute facon
// sans effet des la deuxieme fois (elle ne fait rien si la cle porte deja une
// valeur du nouveau schema).
migrerReglagesPhase()

/** L'ancien plateau. Le serveur sert marvel.html des que l'adresse a une query. */

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
    // PAS le deck supplementaire. Cette fenetre annonce une revelation
    // PASSAGERE — « tu regardes les 2 premieres cartes ». Or un deck
    // supplementaire est une zone PERMANENTE dont le proprietaire connait le
    // contenu : les ecureuils de Squirrel Girl sont visibles pour elle tout en
    // restant face cachee, ce qui remplissait la condition en permanence. La
    // fenetre etait donc perpetuellement due, et se rouvrait des qu'un ecureuil
    // etait depense ou rendu, puisqu'elle ne retient que le lot exact qu'on
    // vient de fermer. On consulte ce deck en cliquant la pile, comme les
    // autres.
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
 * Outils de la barre du haut : le mode d'affichage des actions, et rien de plus.
 *
 * Trois autres commandes y vivaient et en sont parties : le selecteur d'etats
 * enregistres, le champ « joueur affiche » et le lien vers l'ancien plateau.
 * Toutes occupaient une place permanente en haut de l'ecran — celle qui manque
 * a la table — pour des usages rares ou deja couverts ailleurs.
 *
 * AUCUNE FONCTION N'A DISPARU, seulement les raccourcis :
 *  - un etat enregistre se charge par `?etat=<fichier>` ;
 *  - le siege regarde se choisit par `?p=<joueur>`, et en hot-seat la vue suit
 *    de toute facon le joueur que le moteur interroge ;
 *  - l'ancien plateau reste servi a la racine, `/?p=<joueur>`.
 * Les trois passent par parametres(), qui lit l'adresse et n'a pas bouge.
 */
function Outils({
  modeActions,
  changerModeActions,
}: {
  modeActions: ModeActions
  changerModeActions: (mode: ModeActions) => void
}) {
  return <ModeActionsBoutons modeActions={modeActions} changerModeActions={changerModeActions} />
}

/**
 * Le choix Simple / Detaille.
 *
 * Compose a part parce qu'il se pose a DEUX endroits selon la vue : dans le
 * groupe des reglages de la barre en partie, et seul dans la barre de la vue
 * « etat enregistre », qui n'a pas d'actions de partie. Une seule definition,
 * deux placements.
 */
function ModeActionsBoutons({
  modeActions,
  changerModeActions,
}: {
  modeActions: ModeActions
  changerModeActions: (mode: ModeActions) => void
}) {
  return (
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
    siegesAbsents: [],
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

  // STABLES d'un rendu a l'autre, et ce n'est pas un detail de style : le
  // plateau se redessine a chaque trame du moteur, et `reglerModePhase` est
  // la dependance d'un effet (plus bas) qui redit le mode au moteur. Recreee a
  // chaque rendu, elle relancait cet effet a chaque trame — et
  // `setModePhaseMechant` relachait alors la trame retenue. Mesure en partie
  // reelle le 07/09/2026 : la phase du mechant entiere defilait sans un clic.
  const continuer = useCallback(() => moteur.continuer(), [moteur])
  const reconnecter = useCallback(() => moteur.reconnecterMaintenant(), [moteur])
  const reglerModePhase = useCallback(
    (mode: ModePhaseMechant) => moteur.setModePhaseMechant(mode),
    [moteur]
  )
  const avancerPasAPas = useCallback(() => moteur.avancerMaintenant(), [moteur])

  return {
    etat,
    repondre,
    continuer,
    reconnecter,
    reglerModePhase,
    // Branche sur le cartouche du deroule detaille (DeroulePhase, plus bas) :
    // c'est lui qui relache le moteur, etape par etape, et lui seul. La
    // vitesse de l'avance auto ne se regle plus ici : c'est une horloge du
    // cartouche (prop delaiAvanceMs), le moteur n'en a plus.
    avancerPasAPas,
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
  const confirmer = useConfirmation()
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

  const chargerSlot = useCallback(async (slot: number) => {
    const accepte = await confirmer({
      titre: `${t('Charger la sauvegarde')} ${slot} ?`,
      texte: t('La partie en cours sera remplacée.'),
      confirmer: t('Charger'),
      ton: 'danger',
    })
    if (!accepte) return
    setOccupe(`load-${slot}`)
    // `:-1` = reprendre au DERNIER pas enregistre (semantique du client original).
    fetch(`/debug?/load ../replays/save_${slot}.json:-1`)
      .then(() => {
        window.location.href = '/app/board.html?p=0'
      })
      .catch(() => setOccupe(undefined))
  }, [confirmer])

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
      outils={outils}
      bas={
        <footer className="plateau-action plateau-action-attente" role="status">
          <strong>Saved state.</strong>
          <span>
            {t('Aucune partie derrière cette vue : rien à jouer. Retire « ?etat= » de l’adresse pour revenir à la partie.')}
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
  meteo,
  basculerMeteo,
  apercuMeteo,
  reglerApercuMeteo,
  reponseAmbiance,
  cyclerReponseAmbiance,
  revelation,
  cyclerRevelation,
  autoCible,
  basculerAutoCible,
  curseurs,
  basculerCurseurs,
  scansFr,
  basculerScansFr,
  textesCdb,
  basculerTextesCdb,
  succes,
  basculerSucces,
  modePhase,
  changerModePhase,
  avanceAuto,
  basculerAvanceAuto,
  delaiPasAPas,
  reglerDelaiPasAPas,
  validationCourte,
  basculerValidationCourte,
  reglageMode,
  cyclerReglageMode,
  montrerDisposition,
}: {
  animations: boolean
  basculerAnimations: () => void
  sons: boolean
  basculerSons: () => void
  meteo: boolean
  apercuMeteo: ApercuMeteo
  reglerApercuMeteo: (valeur: ApercuMeteo) => void
  basculerMeteo: () => void
  reponseAmbiance: ReponseAmbiance
  cyclerReponseAmbiance: () => void
  revelation: ModeRevelation
  cyclerRevelation: () => void
  autoCible: boolean
  basculerAutoCible: () => void
  curseurs: boolean
  basculerCurseurs: () => void
  scansFr: boolean
  basculerScansFr: () => void
  textesCdb: boolean
  basculerTextesCdb: () => void
  succes: boolean
  basculerSucces: () => void
  modePhase: ModePhaseMechant
  changerModePhase: (mode: ModePhaseMechant) => void
  avanceAuto: boolean
  basculerAvanceAuto: () => void
  delaiPasAPas: number
  reglerDelaiPasAPas: (ms: number) => void
  validationCourte: boolean
  basculerValidationCourte: () => void
  reglageMode: ReglageMode
  cyclerReglageMode: () => void
  montrerDisposition: boolean
}) {
  const [ouvert, setOuvert] = useState(false)
  return (
    <span className="popover-sauvegardes-ancre">
      <button
        type="button"
        className={`bh-bouton bh-options${ouvert ? ' est-actif' : ''}`}
        onClick={() => setOuvert((o) => !o)}
        aria-expanded={ouvert}
        title={t('Tous les réglages du plateau (animations, sons, ambiance, révélation)')}
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
          {/* DEUX positions, sur le modele exact du choix Simple/Detaille du
              mode d'action (ModeActionsBoutons plus haut) : deux boutons cote
              a cote, celui qui est actif porte la classe est-actif. Les
              anciens « Manuel » (un clic par evenement important, sans jamais
              rien montrer) et « Pas a pas » (mode a part entiere) ont
              disparu : le premier n'apportait rien que « Detaille » ne fasse
              deja mieux, le second est devenu le reglage « avance auto »
              ci-dessous, a l'interieur de « Detaille ». */}
          <div className="ligne-option est-etabli">
            <span className="ligne-option-libelle">{t('Phase du méchant')}</span>
          </div>
          <div
            className="mode-actions ligne-option-mode-phase"
            role="group"
            aria-label={t('Phase du méchant')}
          >
            <button
              type="button"
              className={modePhase === 'detaille' ? 'est-actif' : ''}
              onClick={() => changerModePhase('detaille')}
            >
              {t(libelleModePhase('detaille'))}
            </button>
            <button
              type="button"
              className={modePhase === 'instantane' ? 'est-actif' : ''}
              onClick={() => changerModePhase('instantane')}
            >
              {t(libelleModePhase('instantane'))}
            </button>
          </div>
          {modePhase === 'detaille' ? (
            <>
              <LigneOption
                libelle={t('Avance toute seule')}
                detail={t('Chaque étape se termine seule après un délai, sans attendre un clic')}
                actif={avanceAuto}
                onBascule={basculerAvanceAuto}
              />
              {avanceAuto ? (
                <label className="ligne-option ligne-option-curseur">
                  <span className="ligne-option-libelle">{t('Vitesse du déroulé')}</span>
                  <input
                    type="range"
                    min={DELAI_PAS_A_PAS_MIN}
                    max={DELAI_PAS_A_PAS_MAX}
                    step={100}
                    value={delaiPasAPas}
                    onChange={(e) => reglerDelaiPasAPas(Number(e.target.value))}
                    title={t('Temps d’affichage de chaque étape')}
                  />
                  <span className="ligne-option-etat" aria-hidden="true">
                    {(delaiPasAPas / 1000).toFixed(1).replace('.', ',')} s
                  </span>
                </label>
              ) : null}
            </>
          ) : null}
          <LigneOption
            libelle={t('Validation courte')}
            detail={t('Supprime le « Valider » quand la cible est unique et le coût couvert')}
            actif={validationCourte}
            onBascule={basculerValidationCourte}
          />
          <LigneOption
            libelle={t('Ambiance')}
            detail={t('Météo, décor ou traitement de l’image, selon les cartes en jeu')}
            actif={meteo}
            onBascule={basculerMeteo}
          />
          {/* Aperçu d'ambiance et Demande d'ambiance : extraits dans
              CoucheMeteo.tsx (ReglagesApercuAmbiance), grises et inertes tant
              que « Ambiance » est coupee (voir ce composant et
              basculerAmbiance, qui remet deja l'apercu sur Auto au moment de
              la coupure). */}
          <ReglagesApercuAmbiance
            meteo={meteo}
            apercuMeteo={apercuMeteo}
            reglerApercuMeteo={reglerApercuMeteo}
            reponseAmbiance={reponseAmbiance}
            cyclerReponseAmbiance={cyclerReponseAmbiance}
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
          {/* Reglage montre UNIQUEMENT sur un appareil mobile : sur un PC le
              plateau est de toute facon rendu en mode PC, l'option n'aurait
              aucun effet et c'est elle qui a enferme l'utilisateur. */}
          {montrerDisposition ? (
            <button
              type="button"
              className="ligne-option"
              onClick={cyclerReglageMode}
              title={t('Rendu du plateau : automatique selon l’appareil, ou forcer la table complète')}
            >
              <span className="ligne-option-libelle">{t('Disposition')}</span>
              <span className="ligne-option-etat" aria-hidden="true">
                {reglageMode === 'pc' ? t('Ordinateur') : t('Automatique')}
              </span>
            </button>
          ) : null}
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
  bataille,
  monde,
  siege,
  onMenu,
}: {
  gagne: boolean
  raison?: string
  /**
   * Mode Bataille : la partie se gagne PAR UN CAMP, et le meme ecran sert aux
   * deux tables. `gagne` dit alors si c'est NOTRE camp, et `nul` si personne
   * n'a gagne (les deux camps perdus, ou egalite parfaite).
   */
  bataille?: { nul: boolean }
  monde?: World
  /**
   * Siège de CE navigateur (`?p=`), et non la vue affichée : regarder la table
   * d'un autre ne fait pas de nous ce joueur. Le panneau de récompenses s'en
   * sert pour savoir quelles cases nous appartiennent.
   */
  siege: number
  onMenu: () => void
}) {
  const heros = (monde?.players ?? [])
    .map((joueur) => joueur.area_hero?.[0]?.name?.replace(/^\W*/, ''))
    .filter((nom): nom is string => Boolean(nom))
  const eyebrow = bataille
    ? bataille.nul
      ? t('Match nul')
      : gagne
        ? t('Victoire')
        : t('Défaite')
    : gagne
      ? t('Victoire')
      : t('Défaite')
  const titre = bataille
    ? bataille.nul
      ? t('Aucun camp ne l\u2019emporte')
      : gagne
        ? t('Votre camp l\u2019emporte !')
        : t('Le camp adverse l\u2019emporte')
    : gagne
      ? t('Les héros l\u2019emportent !')
      : t('Les héros sont vaincus')
  const rounds = monde?.round_id
  const mechants = (monde?.area_villain ?? []).map((carte) => carte.name).filter(Boolean)
  return (
    <div
      className={`fin-partie ${gagne ? 'est-victoire' : 'est-defaite'}`}
      role="dialog"
      aria-modal="true"
      aria-label={eyebrow}
    >
      {gagne ? (
        <div className="fin-partie-confettis" aria-hidden="true">
          {Array.from({ length: 24 }, (_, i) => (
            <span key={i} style={{ '--i': i } as React.CSSProperties} />
          ))}
        </div>
      ) : null}
      <div className="fin-partie-carte">
        <span className="fin-partie-eyebrow">{eyebrow}</span>
        <strong className="fin-partie-titre">{titre}</strong>
        {raison ? (
          <span className="fin-partie-raison">{traduireMoteur(raison)}</span>
        ) : null}
        {heros.length || mechants.length ? (
          <span className="fin-partie-detail">
            {heros.join(', ')}
            {mechants.length ? ` ${t('contre')} ${[...new Set(mechants)].join(', ')}` : ''}
            {rounds ? ` · ${rounds} ${t('round(s)')}` : ''}
          </span>
        ) : null}
        {/* Liste des hauts faits debloques : DEBRANCHEE, comme la banniere.
            Le style .fin-partie-hauts-faits reste dans board.css. */}
        {/* Campagne : ce que le scenario vient de rapporter. Ne s'affiche qu'a
            la VICTOIRE d'une partie lancee depuis l'ecran des campagnes — le
            livret veut qu'une defaite se rejoue sans rien reporter. */}
        <PanneauRecompenses
          monde={monde}
          gagne={gagne}
          siege={siege}
          onTermine={(retourCampagne) => {
            if (retourCampagne) window.location.href = '/campagne.html'
            else onMenu()
          }}
        />
        <button type="button" className="fin-partie-menu" onClick={onMenu}>
          {t('Retour au menu')}
        </button>
      </div>
    </div>
  )
}

/**
 * Ce qu'un passage de main doit durer pour meriter un changement de vue.
 * Mesure sur le cas signale : les allers-retours du moteur durent environ une
 * demi-seconde.
 */
const DELAI_SUIVI_VUE = 800

function PagePartie({
  playerId,
  catalogue,
  modeActions,
  changerModeActions,
}: {
  playerId: number
  catalogue: Catalogue
  modeActions: ModeActions
  changerModeActions: (mode: ModeActions) => void
}) {
  const confirmer = useConfirmation()
  const {
    etat,
    repondre,
    continuer,
    reconnecter,
    reglerModePhase,
    avancerPasAPas,
  } = usePartieEnCours(playerId)
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

  // La vue ne suit pas TOUS les passages de main.
  //
  // Entre deux cartes jouees, le moteur interroge brievement l'autre joueur —
  // fenetre de reponse ou d'interruption ou il n'a rien de jouable — puis
  // revient. La vue basculait a chaque fois : « entre chaque carte jouee il me
  // remet une demi-seconde sur l'autre perso », signale en jeu a deux heros.
  //
  // Regle : on suit TOUT DE SUITE si le joueur interroge a au moins une option
  // reellement jouable (c'est son tour, il attend la table). Sinon on attend
  // DELAI_SUIVI_VUE : si le moteur repart avant, la bascule n'aura jamais eu
  // lieu. Rien de jouable n'est retarde — la REPONSE part toujours pour le
  // joueur du moteur (`option.bind_player_id`), independamment de la vue.
  // Une vue FORCEE sur un joueur qui vient d'etre elimine ne mene plus nulle
  // part : sa table a disparu. On repasse en Auto plutot que de laisser
  // l'ecran vide avec un bouton qui n'existe plus dans la barre.
  useEffect(() => {
    if (vueForcee === null) return
    if (etat.monde?.players?.[vueForcee]?.is_eliminated) setVueForcee(null)
  }, [vueForcee, etat.monde])

  const [joueurSuivi, setJoueurSuivi] = useState<number | undefined>(undefined)
  const demandeJouable = etat.demande?.options.some((o) => o.failure_reason === '') ?? false

  useEffect(() => {
    const cible = etat.joueurDemande
    if (cible === undefined || cible === joueurSuivi) return
    // On ne suit pas un joueur dont on ne verrait RIEN. Pendant les mulligans,
    // le moteur interroge chaque siege a son tour : la vue partait chez le
    // voisin, dont la main nous est cachee, et l'ecran sans main passait pour
    // une partie bloquee. Voir suivi-vue.ts.
    if (!peutSuivre(etat.monde, cible, playerId)) return
    if (joueurSuivi === undefined || demandeJouable) {
      setJoueurSuivi(cible)
      return
    }
    const attente = window.setTimeout(() => setJoueurSuivi(cible), DELAI_SUIVI_VUE)
    return () => window.clearTimeout(attente)
  }, [etat.joueurDemande, joueurSuivi, demandeJouable, etat.monde, playerId])

  const joueurActif = vueForcee ?? joueurSuivi ?? etat.joueurDemande ?? playerId
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
        ? construirePlateau(etat.monde, {
            playerId: joueurActif,
            catalogue,
            // Vue braquee sur un joueur PAR UN CLIC : on ne pose que sa table.
            // En « Auto » (vueForcee === null), la vue suit celui qui doit agir
            // et la table montre tout le monde, comme une vraie partie a
            // plusieurs.
            seulCeJoueur: vueForcee !== null,
          })
        : undefined,
    [etat.monde, joueurActif, catalogue, scansFr, vueForcee]
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
  const cartesMondeParNom = useMemo(
    () => indexerCartesMondeParNom(cartesMondeParId),
    [cartesMondeParId]
  )
  // Un choix textuel (« quelle chanson ? ») montre le SCAN de la carte nommee.
  const carteDeLOption = useCallback(
    (option: Option) => carteNommeeParOption(option, cartesMondeParNom, joueurActif, catalogue),
    [cartesMondeParNom, joueurActif, catalogue]
  )
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

  const {
    mode: modePlateau,
    reglage: reglageMode,
    surAppareilMobile,
    changer: changerReglageMode,
  } = useModeMobile()
  // Deux etats seulement : automatique, ou forcer le plateau PC. Forcer le mode
  // MOBILE a disparu du cycle — c'est ce choix-la qui enfermait, puisqu'il
  // rendait ensuite l'option elle-meme inatteignable (voir modeEffectif).
  const cyclerReglageMode = useCallback(() => {
    changerReglageMode(reglageMode === 'pc' ? 'auto' : 'pc')
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

  // Les etapes du deroule detaille : `etapesDeroule` parcourt tous les faits
  // et toutes les entrees du journal, donc on ne la relance pas a chaque
  // rendu (meme motif que `cartesMondeParId` plus haut).
  //
  // `etapesDeroule` ne voit pas le monde, seulement les faits et le journal :
  // c'est ici qu'on lui dit qui est le vilain, pour distinguer ses coups de
  // ceux de ses sbires. `cartesMondeParId` porte deja le `card_type` de
  // chaque carte ; `kindOf()` le traduit en famille visuelle, et 'villain'
  // (EncounterVillain) distingue le vilain lui-meme d'un sbire ('minion',
  // Minion). Ajouter `cartesMondeParId` aux dependances ne change rien au
  // rythme de recalcul : `etat.monde` se re-parse en JSON a chaque trame du
  // moteur (meme piege que dans DeroulePhase.tsx), donc `faits_mechant`
  // change deja d'identite a chaque trame et relancait deja ce useMemo aussi
  // souvent.
  const etapesPhaseMechant = useMemo(() => {
    const mechantIds = new Set<number>()
    for (const carte of cartesMondeParId.values()) {
      if (kindOf(carte) === 'villain') mechantIds.add(carte.id)
    }
    // Les heros que le MONDE declare tombes. C'est l'etat que le moteur pose
    // lui-meme (`Player.Eliminate` -> `is_eliminated`), pas une deduction :
    // l'identite d'un joueur elimine reste dans `area_hero` (le moteur exclut
    // le type Identity de la defausse, voir joueur-elimine.test.ts), donc on la
    // retrouve, PV a zero.
    //
    // Il ne dit pas QUEL coup a mis le heros a terre : c'est `etapesDeroule`
    // qui croise cet ensemble avec le `restant` du fait. Les deux ensemble, et
    // jamais l'un sans l'autre.
    const herosVaincusIds = new Set<number>()
    for (const joueur of etat.monde?.players ?? []) {
      if (!joueur.is_eliminated) continue
      for (const carte of joueur.area_hero ?? []) {
        // Les DEUX faces : un heros peut tomber en alter ego (une obligation,
        // une manigance qui frappe). `area_hero` porte aussi ses ameliorations,
        // qui ne sont ni l'une ni l'autre.
        const famille = kindOf(carte)
        if (famille === 'hero' || famille === 'alter-ego') herosVaincusIds.add(carte.id)
      }
    }
    // Le premier joueur du round, pour l'ordre du tour des revelations
    // (regle officielle : chaque joueur revele en commencant par lui).
    //
    // Le monde ne publie pas de champ dedie a l'ordre des joueurs : le jeton
    // de premier joueur vit comme un COMPTEUR generique sur l'identite de son
    // detenteur (`k_first_player_token`, meme convention que `k_threat` sur
    // une manigance), pose par le moteur des `SetActive()`
    // (game/card/face/card_type/identity.py). `findIndex` rend -1 si personne
    // ne le porte (ancien moteur sans le jeton) : on rend alors `undefined`,
    // et `etapesDeroule` garde l'ordre du journal plutot que d'en inventer un.
    const premierJoueurId = (etat.monde?.players ?? []).findIndex(
      (joueur) => ((joueur.area_hero ?? [])[0]?.info['k_first_player_token'] ?? 0) > 0
    )
    // Le heros de chaque joueur, dans le MEME ordre que `World.players` :
    // c'est l'indice que porte deja `EntreeHistorique.joueur`. Brut, prefixe
    // decoratif compris : `etapesDeroule` le nettoie elle-meme, comme elle le
    // fait deja pour les faits du mechant.
    const nomsHerosParJoueur = (etat.monde?.players ?? []).map(
      (joueur) => (joueur.area_hero ?? [])[0]?.name
    )
    return etapesDeroule(
      etat.monde?.faits_mechant ?? [],
      historique.entrees,
      etat.monde?.round_id ?? 0,
      mechantIds,
      herosVaincusIds,
      premierJoueurId === -1 ? undefined : premierJoueurId,
      nomsHerosParJoueur
    )
  }, [
    cartesMondeParId,
    etat.monde?.faits_mechant,
    etat.monde?.players,
    historique.entrees,
    etat.monde?.round_id,
  ])

  // Les PV MAXIMUM des personnages, par nom, pour le bilan de fin de phase du
  // mechant : sans eux il dit « 8 » la ou il pourrait dire « 8/14 ».
  //
  // Par NOM, parce que c'est la cle du bilan : ses lignes regroupent ce qu'UNE
  // cible a encaisse, et le regroupement se fait sur le nom (voir lignesBilan).
  // Le nom passe par `nomNettoye`, la meme fonction que le deroule applique aux
  // noms venus des faits : sans cela, « * Colossus » ne retrouverait jamais
  // « Colossus ».
  //
  // Le plafond vient de `pvMaximum`, exactement comme la pastille de PV des
  // cartes : `info.max_health` du moteur, ameliorations comprises, et le PV
  // imprime du catalogue en secours. Deux regles differentes pour un meme
  // chiffre se contrediraient a l'ecran.
  //
  // Une carte sans maximum sur (PV variables selon le nombre de joueurs, PV
  // infinis, carte hors catalogue) n'entre PAS dans la table : le bilan montre
  // alors le restant seul. Un plafond faux serait pire qu'un chiffre nu.
  const pvMaxParNom = useMemo(() => {
    const parNom = new Map<string, number>()
    for (const carte of cartesMondeParId.values()) {
      if (!isUnit(carte)) continue
      const max = pvMaximum(carte, catalogue)
      if (max === undefined || max <= 0) continue
      const nom = nomNettoye(carte.name)
      if (nom) parNom.set(nom, max)
    }
    return parNom
  }, [cartesMondeParId, catalogue])

  // Le rapport de bug. Il ne capture qu'AU CLIC : il lit le monde et la demande
  // du moment, et le journal ci-dessus pour le passé. Aucun tampon d'états n'est
  // gardé, donc une partie qui ne signale rien n'en porte aucun coût.
  const rapport = useRapportBug(etat.monde, etat.demande, historique.entrees, etat.joueurDemande)

  // Mode Bac à sable. Inerte hors de ce mode : le crochet n'installe aucune
  // écoute et la couche ne rend rien, donc une partie normale n'en porte
  // aucune trace. Déclaré APRÈS l'historique, dont il consomme la porte
  // d'entrée pour y inscrire chaque intervention.
  const triche = useTriche(etat.monde, joueurActif, historique.ajouterTriche)

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
  // Couper « Ambiance » remet l'apercu sur Auto (voir basculerAmbiance) : sinon
  // un apercu fige (pose un jour pour essayer un effet) continue de forcer cet
  // effet a l'ecran malgre l'interrupteur general coupe, sans que rien ne le
  // signale au joueur (voir la ligne « Aperçu d’ambiance », grisee dans ce cas).
  const basculerMeteo = useCallback(() => {
    setMeteo((m) => {
      const { meteo: nouveau, reinitialiserApercu } = basculerAmbiance(m)
      try {
        window.localStorage.setItem(CLE_METEO, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      if (reinitialiserApercu) setApercuMeteo(undefined)
      return nouveau
    })
  }, [])

  // Apercu meteo : force un effet a l'ecran sans partie ni carte. Sert a
  // concevoir de nouveaux effets sans monter une situation de jeu a chaque
  // essai. Volontairement NON persiste : c'est un outil, pas une preference,
  // et le retrouver actif au lancement suivant serait deroutant.
  const [apercuMeteo, setApercuMeteo] = useState<ApercuMeteo>(undefined)
  const reglerApercuMeteo = useCallback((valeur: ApercuMeteo) => setApercuMeteo(valeur), [])

  // La reponse figee a la question « une ambiance s'allume, on la garde ? ».
  // Elle DOIT rester revocable : une case « ne plus me montrer ca » cochee par
  // erreur, sans ligne pour la remettre en marche, serait un piege definitif.
  const [reponseAmbiance, setReponseAmbiance] = useState<ReponseAmbiance>(lireReponseAmbiance)
  const cyclerReponseAmbiance = useCallback(() => {
    setReponseAmbiance((r) => {
      const suivant: ReponseAmbiance =
        r === 'demander' ? 'toujours' : r === 'toujours' ? 'jamais' : 'demander'
      ecrireReponseAmbiance(suivant)
      return suivant
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

  const [modePhase, setModePhase] = useState<ModePhaseMechant>(lireModePhaseMechant)
  const choisirModePhase = useCallback((mode: ModePhaseMechant) => {
    setModePhase(mode)
    ecrireModePhaseMechant(mode)
  }, [])

  // Avance auto : reglage independant (case a cocher du panneau Options), qui
  // ne veut rien dire hors du mode « detaille ». Remplace l'ancien mode a part
  // entiere « pas-a-pas ». Le moteur ne le connait PAS : c'est le cartouche
  // du deroule (DeroulePhase, plus bas) qui s'avance tout seul, et qui
  // relache le moteur par le meme chemin que le clic « Suivant ».
  const [avanceAuto, setAvanceAuto] = useState(lireAvanceAuto)
  const basculerAvanceAuto = useCallback(() => {
    setAvanceAuto((a) => {
      const nouveau = !a
      ecrireAvanceAuto(nouveau)
      return nouveau
    })
  }, [])

  const [delaiPasAPas, setDelaiPasAPas] = useState(lireDelaiPasAPas)
  const choisirDelaiPasAPas = useCallback((ms: number) => {
    setDelaiPasAPas(ms)
    ecrireDelaiPasAPas(ms)
  }, [])

  // Le mode vit dans le composant, mais c'est le Moteur qui retient (ou non)
  // l'accuse de reception : il faut le lui redire a chaque changement. Avance
  // auto et vitesse, eux, ne le regardent pas : ils vont au cartouche.
  useEffect(() => {
    reglerModePhase(modePhase)
  }, [modePhase, reglerModePhase])

  // LE COUP FATAL SE VOIT AVANT L'ECRAN DE FIN.
  //
  // « Defaite en pleine phase : le coup fatal s'affiche normalement et c'est
  // APRES validation que vient l'ecran de fin. On comprend ce qui nous a
  // tues. » Le code faisait l'inverse : le cartouche et l'ecran de fin
  // basculaient sur la MEME trame (`monde.game_over`), et l'etape qui avait tue
  // n'etait jamais lue (constat M5 de l'audit du 06/09/2026).
  //
  // La retenue ne vaut QUE pour le siege dont le heros est tombe, et qu'en
  // mode Detaille : la table des autres joueurs n'attend rien, et le mode
  // Instantane n'a pas d'etape a montrer. La decision elle-meme est pure
  // (`afficherFinDePartie`, board/fin-partie.ts), avec son filet de temps.

  // QUI L'ON ATTEND, quand le plateau ne bouge plus (constat F5).
  //
  // Le moteur n'avance qu'une fois TOUS les clients a jour (`WaitSync`) et
  // n'interroge qu'un joueur a la fois. Trois facons de le savoir, une seule
  // mention a l'ecran. Les regles sont pures et testees dans
  // `board/attente-table.ts` ; ici, on ne fait que les alimenter.
  const phaseMechantEnCours = PHASES_DU_MECHANT.has(etat.monde?.phase ?? '')
  const nomsHerosParJoueur = useMemo(
    () =>
      (etat.monde?.players ?? []).map((joueur) =>
        joueur.area_hero?.[0]?.name?.replace(/^\W*/, '')
      ),
    [etat.monde?.players]
  )
  // Cas 1 : le moteur interroge un AUTRE siege. La seule attente dont il dise
  // le nom (`ask_players[0]`, pousse a tous les clients).
  const autreJoueurInterroge = joueurAttendu({
    joueurDemande: etat.joueurDemande,
    playerId,
    multijoueur: estMultijoueur(),
    nomsHerosParJoueur,
  })
  // Cas 2 : un autre siege n'a pas encore accuse reception de la trame
  // retenue (`sieges_non_acquittes`). Sur un moteur qui le publie, on nomme
  // le retardataire sans attendre le silence ci-dessous.
  const autreJoueurEnRetard = joueurEnRetard({
    siegesNonAcquittes: etat.siegesNonAcquittes,
    playerId,
    multijoueur: estMultijoueur(),
    nomsHerosParJoueur,
  })
  // Cas 3 : plus rien n'arrive, et le moteur ne dit pas encore qui est en
  // retard (`siegesNonAcquittes` absent, moteur ancien). C'est alors tout ce
  // qu'un client peut savoir du retard d'un autre. On ne guette QUE lorsqu'on
  // n'a plus rien a faire de notre cote : trame relachee, aucune question en
  // cours, et aucune des deux reponses precedentes.
  const tableSilencieuse = useTableSilencieuse(
    etat.monde?.render_id,
    estMultijoueur() &&
      etat.connecte &&
      phaseMechantEnCours &&
      etat.trameRetenue === undefined &&
      etat.demande === undefined &&
      autreJoueurInterroge === undefined &&
      etat.siegesNonAcquittes === undefined
  )
  const attendUnAutreJoueur =
    autreJoueurInterroge !== undefined || autreJoueurEnRetard !== undefined || tableSilencieuse

  // Les deux faces du heros de CE navigateur (`?p=`), et non de la vue
  // affichee : regarder la table d'un autre ne fait pas de nous ce joueur.
  // Meme lecture que `herosVaincusIds` plus haut, meme motif : `area_hero`
  // porte aussi les ameliorations, qui ne sont ni l'une ni l'autre.
  const herosLocauxIds = useMemo(() => {
    const ids = new Set<number>()
    for (const carte of etat.monde?.players?.[playerId]?.area_hero ?? []) {
      const famille = kindOf(carte)
      if (famille === 'hero' || famille === 'alter-ego') ids.add(carte.id)
    }
    return ids
  }, [etat.monde?.players, playerId])

  const partieFinieMoteur = Boolean(etat.monde?.game_over)
  const coupFatalAMontrer =
    modePhase === 'detaille' && coupFatalLocal(etapesPhaseMechant, herosLocauxIds)
  // Le joueur a valide l'etape du coup fatal (« Continuer »), et le filet de
  // temps qui laisse paraitre l'ecran de fin quoi qu'il arrive.
  //
  // Les deux se remettent a faux a chaque NOUVELLE PARTIE, et il a fallu le
  // dire : « une nouvelle partie remonte tout le plateau » etait faux.
  // `PagePartie` n'est monte qu'une fois par chargement de page, sans `key`
  // (voir la fin de ce fichier) ; « Rejouer » enchaine donc une seconde partie
  // sur le meme etat. `coupFatalVu` restait vrai, `afficherFinDePartie` rendait
  // vrai des la trame de `game_over`, et le coup fatal n'etait plus jamais
  // montre a partir de la deuxieme partie (relecture A4). Meme motif et meme
  // source que la remise a zero du cartouche : `etat.partieId`.
  const [coupFatalVu, setCoupFatalVu] = useState(false)
  const [filetFinEcoule, setFiletFinEcoule] = useState(false)
  useEffect(() => {
    setCoupFatalVu(false)
    setFiletFinEcoule(false)
  }, [etat.partieId])
  const finPartieAffichee = afficherFinDePartie({
    partieFinie: partieFinieMoteur,
    coupFatalAMontrer,
    coupFatalVu,
    filetEcoule: filetFinEcoule,
  })

  useEffect(() => {
    if (!partieFinieMoteur || !coupFatalAMontrer || coupFatalVu || filetFinEcoule) return
    const minuteur = window.setTimeout(() => setFiletFinEcoule(true), DELAI_FILET_FIN_PARTIE_MS)
    return () => window.clearTimeout(minuteur)
  }, [partieFinieMoteur, coupFatalAMontrer, coupFatalVu, filetFinEcoule])

  // usePasAPas (halo teinte + chiffre flottant sur la carte de l'etape en
  // cours) : DEBRANCHEE a la demande de l'utilisateur - double emploi avec le
  // cartouche du deroule (MENACE / ACTIVATIONS / DISTRIBUTION / RÉVÉLATION),
  // exactement le defaut corrige entre le bandeau et le splash. pas-a-pas.ts
  // reste en place : il suffit de reimporter `usePasAPas` depuis
  // './board/pas-a-pas' et de remettre la ligne suivante pour la rallumer,
  // avec pour second argument « une trame est retenue »
  // (etat.trameRetenue !== undefined).
  // usePasAPas(historique.entrees, etat.trameRetenue !== undefined)

  // Espace n'a plus de role ici : la pause du moteur a disparu avec son
  // minuteur de lecture (le cartouche tient la seule horloge de la phase), et
  // c'est DeroulePhase qui prend Espace pour avancer d'une etape.

  // Le recap de fin de phase ne sert QU'EN INSTANTANE (voir son montage plus
  // bas). En detaille, c'est le cartouche du deroule qui raconte la phase et
  // qui la clot par son propre bilan.

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
  // Même mécanique pour B : l'écoute est installée une fois, sa cible change à
  // chaque monde reçu. Sans le ref, l'effet se réinstallerait à chaque rendu.
  const rapportClavier = useRef<() => void>(() => {})
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
      } else if (touche === 'b') {
        // « B » comme bug : copie les 20 dernières entrées SANS ouvrir le
        // panneau, parce que le symptôme peut disparaître au rendu suivant.
        rapportClavier.current()
      }
    }
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [])
  rapportClavier.current = () => void rapport.copier('recent')

  // Installée une fois pour la vie de la page : une erreur de rendu survenue
  // AVANT l'ouverture du panneau doit quand même figurer au rapport.
  useEffect(() => installerCollecteErreurs(), [])

  useHaloStatut(etat.monde, animations)

  const annulerCoup = useCallback(() => {
    // « /undo auto » remonte au dernier point de decision, comme le bouton Undo
    // du client d'origine. L'espace est encode par fetch, le '/' est conserve.
    fetch('/debug?/undo auto').catch(() => undefined)
  }, [])

  const retourMenu = useCallback(() => {
    window.location.href = '/prepare.html'
  }, [])

  const retourMenuPrincipal = useCallback(async () => {
    const accepte = await confirmer({
      titre: t('Revenir au menu principal ?'),
      texte: t('La partie en cours sera perdue si tu ne l’as pas sauvegardée.'),
      confirmer: t('Quitter'),
      ton: 'danger',
    })
    if (accepte) window.location.href = '/prepare.html'
  }, [confirmer])

  const effetCentrale = useMemo(() => {
    const premier = effets.entries().next().value as [number, CardEffectDelta] | undefined
    if (!premier) return undefined
    const [id, effet] = premier
    const carte = cartesMondeParId.get(id)
    if (!carte) return undefined
    const valeur = Math.abs(effet.value)
    // Narration ecrite ici, pas envoyee par le moteur : elle doit donc suivre
    // la langue du client comme le reste du plateau.
    if (effet.kind === 'damage') return `${carte.name} ${t('subit')} ${valeur} ${t('dégâts')}`
    if (effet.kind === 'heal') return `${carte.name} ${t('récupère')} ${valeur} ${t('PV')}`
    return effet.value > 0
      ? `${carte.name} ${t('gagne')} ${valeur} ${t('menace')}`
      : `${carte.name} ${t('perd')} ${valeur} ${t('menace')}`
  }, [effets, cartesMondeParId])

  if (!etat.monde || !plateau) {
    return (
      <p className="plateau-message" role={etat.erreur ? 'alert' : undefined}>
        {etat.erreur ?? t('Connexion à la partie…')}
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
  // Deux libelles ecrits en dur en ANGLAIS, au milieu d'une interface
  // francaise. Ils datent du portage et personne ne les avait vus : ce bouton
  // n'apparait que sur le menu d'une carte, jamais dans la barre.
  const libelleAnnulationMenu =
    etat.demande?.event_name === 'WhenPlayerInTurn' && etat.demande.ability_type === 'Normal'
      ? t('Fin du tour')
      : t('Passer')
  // Le moteur attend une reponse du joueur LOCAL. Etat du MOTEUR, sans un mot
  // sur la facon dont on repond : c'est ce que le cartouche du deroule doit
  // savoir (voir moteurAttendUneReponse).
  const moteurAttendLeJoueur = moteurAttendUneReponse(etat)
  // Le PANNEAU central, lui, cede la place a toutes les autres facons de
  // repondre a cette meme question : un ciblage sur la table, le menu d'une
  // carte, une animation d'effet en cours.
  const afficherDemandeCentrale =
    moteurAttendLeJoueur && effets.size === 0 && !interaction.option && !carteMenu
  // etat.validationRequise n'entre pas dans la condition ci-dessous : c'est
  // desormais le cartouche du deroule detaille (DeroulePhase) qui garde la
  // validation, ce panneau-la ne fait plus que narrer. Ses deux raisons
  // d'apparaitre (un effet en cours, ou un evenement narre important pendant
  // l'activation ennemie) doivent continuer de marcher telles quelles.
  const afficherEvenementCentrale =
    etat.connecte &&
    (effets.size > 0 ||
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

      {/* En mode detaille, BandeauPhase (plus bas) annonce deja la phase du
          mechant, plus fort : ce splash-ci ne doit pas la doubler. */}
      <SplashTour monde={etat.monde} annonceMechantAilleurs={modePhase === 'detaille'} />


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
          carteDeLOption={carteDeLOption}
        />
      ) : null}

      {afficherEvenementCentrale ? (
        <EvenementCentrale
          prompt={etat.monde.prompt}
          eventName={etat.monde.event_name}
          message={effetCentrale}
          // En mode Détaillé, la validation appartient au cartouche
          // (DeroulePhase) : ce panneau ne doit plus jamais montrer de bouton
          // « Continuer », quelle que soit la valeur de etat.validationRequise.
          validationRequise={modePhase === 'detaille' ? false : etat.validationRequise}
          continuer={continuer}
          // Les cartes citees par l'evenement en cours : le bandeau raconte ce
          // qui leur arrive, il ne doit surtout pas les cacher.
          cartes={etat.monde.active_card_ids}
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

      <CoucheMeteo world={etat.monde} active={meteo} apercu={apercuMeteo} />
      {/* Explique l'ambiance qui s'allume, au lieu de la subir sans un mot.
          Reglage PERSONNEL : elle ne change rien pour les autres joueurs et
          ne retient pas le moteur, la partie continue derriere. */}
      <ModaleAmbiance
        // Change de cle quand le joueur touche au reglage : le composant se
        // remonte, et une question remise en marche depuis les Options se
        // repose des la partie EN COURS, sans attendre la suivante.
        key={reponseAmbiance}
        monde={etat.monde}
        ambianceActive={meteo}
        apercu={apercuMeteo}
        reglerApercu={reglerApercuMeteo}
        onReponseFigee={setReponseAmbiance}
      />
      <CoucheSucces monde={etat.monde} demande={etat.demande} actif={succes} />
      {etat.joueurDemande !== undefined &&
      etat.siegesAbsents.includes(etat.joueurDemande) ? (
        <BandeauAbsent
          numero={etat.joueurDemande + 1}
          nom={etat.monde?.players?.[etat.joueurDemande]?.area_hero?.[0]?.name?.replace(/^\W*/, '')}
          // Le siege est deja ouvert cote serveur (voir allowed_seats) : il
          // suffit de regarder ce joueur pour repondre a sa place.
          onReprendre={() => setVueForcee(etat.joueurDemande ?? null)}
        />
      ) : null}

      {/* CouchePasAPas (barre « où on en est » + Tout passer) : DEBRANCHEE a
          la demande de l'utilisateur - double emploi avec le cartouche du
          deroule juste en dessous, qui porte deja MENACE / ACTIVATIONS /
          DISTRIBUTION / RÉVÉLATION : exactement le defaut corrige entre le
          bandeau et le splash. Le « Tout passer » qu'elle portait est repris
          par DeroulePhase (touche Echap, qui fait defiler le cartouche).
          CouchePasAPas.tsx reste en place, mais deux de ses props n'ont PLUS
          de contrepartie dans le moteur : la pause (`enPause`,
          `onBasculerPause`) et le « Tout passer » moteur (`onToutPasser`) ont
          disparu avec le minuteur de lecture du moteur, le cartouche tenant
          desormais la seule horloge de la phase. La rallumer demanderait de
          lui retirer ces deux commandes ; `actif` vaudrait
          `etat.trameRetenue !== undefined` et `onAvancer` = avancerPasAPas
          (deja destructure plus haut, utilise par DeroulePhase ci-dessous). */}
      {/* Banniere des hauts faits : DEBRANCHEE a la demande de l'utilisateur.
          Moteur.enregistrerHautsFaits() continue de les accumuler dans
          etat.hautsFaits, et CoucheHautsFaits.tsx reste en place : il suffit de
          remettre <CoucheHautsFaits hautsFaits={etat.hautsFaits} /> ici pour la
          rallumer. */}
      {/* Deroule detaille : une etape a la fois, validee avant la suivante.
          Le recap ci-dessous garde son role de bilan de fin, pour les modes
          rapides ou l'on n'a rien vu passer. */}
      {/* Le joueur SANS cartouche (mode Instantane) : une ligne discrete, pas
          un plateau fige et muet. Le reglage est personnel, mais le rythme est
          celui de la table — c'est exactement ce que F5 reprochait. */}
      {modePhase !== 'detaille' && attendUnAutreJoueur && phaseMechantEnCours ? (
        <AttenteTable nom={autreJoueurInterroge?.nom} />
      ) : null}
      {modePhase === 'detaille' ? (
        <>
          <BandeauPhase
            round={etat.monde?.round_id ?? 1}
            actif={etapesPhaseMechant.length > 0}
          />
          <DeroulePhase
            etapes={etapesPhaseMechant}
            // L'identite de la phase en cours, seule chose qui remet le
            // cartouche a zero. Il y a une phase du mechant par round, donc le
            // round suffit a distinguer deux phases ; la liste d'etapes, elle,
            // s'allonge PENDANT la phase (chaque validation relache une trame
            // qui produit l'etape suivante) et ne peut donc pas jouer ce role.
            identitePhase={etat.monde?.round_id ?? 0}
            // La partie, que le moteur renumerote a chaque nouvelle partie :
            // une partie neuve peut commencer SANS rechargement de page, et le
            // round retombe alors a 1 sans que rien d'autre ne le dise au
            // cartouche.
            identitePartie={etat.partieId}
            // Tant que le moteur est dans une des quatre phases du mechant, la
            // liste d'etapes peut encore s'allonger : arriver au bout de
            // celles qu'on connait ne veut pas dire que la phase est finie.
            phaseMechantEnCours={phaseMechantEnCours}
            // La partie est finie ET l'ecran de fin est a l'ecran : le
            // cartouche s'efface. Meme valeur que cet ecran (`EcranFinPartie`,
            // plus bas), pas une seconde inventee pour l'occasion. Constate en
            // partie : l'ecran de defaite etait la et le cartouche annonçait
            // encore « La suite arrive… ». Tant que le coup fatal n'a pas ete
            // valide, `finPartieAffichee` reste faux et le cartouche montre
            // l'etape qui a tue (voir `afficherFinDePartie`).
            partieFinie={finPartieAffichee}
            // Le moteur pose une question au joueur local : le cartouche
            // s'efface devant elle. On lit l'etat du MOTEUR, pas la visibilite
            // du panneau central : pendant un ciblage (choisir les deux sbires
            // a activer), le panneau cede la place au selecteur de cibles et le
            // cartouche se redeployait pour annoncer « La suite arrive… » alors
            // que le moteur attendait le joueur.
            // ...et SEULEMENT quand c'est nous. Sans mot de passe de siege, le
            // serveur laisse ce navigateur lire la question d'un autre joueur
            // (`allowed_seats` rend `None`) : replier le cartouche sur « Le
            // moteur attend ta reponse » serait alors faux. C'est la mention
            // d'attente ci-dessous qui prend le relais dans ce cas.
            questionAuJoueur={moteurAttendLeJoueur && autreJoueurInterroge === undefined}
            // Les deux faces de NOTRE heros : la chute d'un autre joueur ne
            // coupe plus le deroule de ce siege-ci, elle y reste une etape
            // marquee et la phase continue (constat F5).
            herosLocauxIds={herosLocauxIds}
            // La table attend quelqu'un d'AUTRE : le cartouche le dit a la
            // place de « La suite arrive… », qui parle du moteur. Le nom est
            // connu quand le moteur interroge ce siege-la OU quand il publie
            // le retard de son accuse de reception ; sinon la mention reste
            // vraie mais vague (voir board/attente-table.ts).
            attendUnAutreJoueur={attendUnAutreJoueur}
            nomJoueurAttendu={autreJoueurInterroge?.nom ?? autreJoueurEnRetard?.nom}
            // Les PV maximum, que seul le monde connait : le bilan de fin de
            // phase dit alors « 8/14 » plutot que « 8 » tout seul.
            pvMaxParNom={pvMaxParNom}
            // L'identite de la trame que le moteur retient. Elle donne au
            // cartouche de quoi n'acquitter qu'UNE fois par trame, plutot que
            // de se fier a un booleen qui se recalcule sans cesse.
            trameRetenue={etat.trameRetenue}
            // L'echeance du filet anti-blocage de la PHASE (une seule, armee
            // au premier accuse retenu). Le cartouche n'en montre que les
            // quinze dernieres secondes : la phase qui repart toute seule ne
            // doit pas ressembler a un bug.
            echeanceFilet={etat.echeanceFilet}
            // « Avance toute seule » et sa vitesse (panneau Options) : c'est le
            // cartouche qui tient cette horloge, pas le moteur. Il s'avance
            // par la meme fonction que le clic « Suivant », donc l'accuse
            // ci-dessous part par le meme chemin, et le moteur ne peut pas
            // partir devant.
            avanceAuto={avanceAuto}
            delaiAvanceMs={delaiPasAPas}
            // L'accuse de reception. Il ne part plus a chaque « Suivant » : le
            // cartouche le declenche quand il n'a plus rien a montrer, donc
            // quand le joueur a valide tout ce qu'il sait deja. onTerminer
            // rappelle la meme fonction pour ne jamais laisser le moteur
            // bloque une fois la derniere etape validee (elle ne fait rien
            // sans trame en attente, moteur.ts, avancerMaintenant).
            onSuivant={avancerPasAPas}
            onTerminer={avancerPasAPas}
            // Le coup fatal est vu : l'ecran de fin de partie peut paraitre.
            onDefaiteVue={() => setCoupFatalVu(true)}
          />
        </>
      ) : null}
      <RecapPhaseMechant
        entrees={historique.entrees}
        monde={etat.monde}
        // EN INSTANTANE SEULEMENT. En detaille, le cartouche du deroule
        // (DeroulePhase, juste au-dessus) raconte la phase etape par etape et
        // la termine par son propre bilan, valide au clic : le recap disait
        // ensuite la meme chose une seconde plus tard, calculee par un autre
        // chemin. Deux bilans qui se suivent, et qui pouvaient diverger
        // (constat M7 de l'audit du 06/09/2026).
        //
        // Il avait ete remis en detaille « par securite » (c27bb07) a un moment
        // ou le cartouche ne tenait pas le rythme et s'effaçait avant la fin de
        // la phase. Ce n'est plus le cas : la cause racine est corrigee
        // (86d8bd34) et le bilan du cartouche s'affiche vraiment (09e4bfa1).
        actif={modePhase !== 'detaille'}
        // La MEME definition de « la phase du mechant » que le cartouche, et la
        // meme valeur deja calculee : le recap avait son propre detecteur de
        // transition, sur sa propre photo de `monde.phase` (constat F6).
        phaseMechantEnCours={phaseMechantEnCours}
        // De quoi montrer la carte au survol d'une ligne : le même index et le
        // même catalogue que la table, donc le même agrandissement qu'elle.
        cartesMonde={cartesMondeParId}
        catalogue={catalogue}
        playerId={joueurActif}
      />
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
        actionsPartie={
          /* ORDRE : par intention, et il se lit comme une phrase —
              ce que je FAIS, ce que je REGARDE, comment c'est REGLE, je PARS.

              Avant, les reglages etaient eclates en trois endroits : le panneau
              Options, la paire Musique/Langue, et le mode d'affichage exile a
              l'autre bout de la barre. Options, lui, s'etait intercale entre les
              deux actions de partie et les deux boutons de consultation.

              Musique et Langue restent HORS du panneau Options, deliberement :
              couper le son ou changer de langue doit se faire d'un geste (voir
              le commentaire du bouton musique). */
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

            <span className="bh-separateur" aria-hidden="true" />

            <HistoriquePartie
              entrees={historique.entrees}
              effacer={historique.effacer}
              rapport={rapport}
            />
            {/* « Log » : le rapport complet en UN clic, sans ouvrir le panneau
                ni choisir une profondeur. Les mêmes boutons existent au bas du
                panneau Historique depuis le 12/8/2026, mais personne ne les y
                trouvait — et c'est au moment où un bug vient de se produire
                qu'on a le moins envie de chercher. Toute la partie, en texte
                lisible, parce que c'est ce qu'on relit et ce qu'on transmet. */}
            <button
              type="button"
              className="bh-bouton bh-log"
              onClick={() => rapport.telecharger('partie', 'txt')}
              title={t('Télécharger tout le déroulé de la partie en fichier texte')}
            >
              <span aria-hidden="true">🧾</span> {t('Log')}
            </button>
            <MessageRapport message={rapport.message} />
            {/* Signaler un bug : le journal de toute la partie part avec la
                description et la capture. Ne s'affiche que si un site ecoute. */}
            <PanneauBug outils={rapport} />
            {/* Tchat des comptes, le MEME qu'a la preparation : il ne s'affiche
                que la ou il a un sens (siege du titulaire, site derriere). */}
            <PanneauSalon />
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
                {/* Un joueur elimine n'est plus une vue possible : sa table a
                    disparu (voir zones.ts), il n'y aurait rien a regarder. */}
                {etat.monde!.players.map((joueur, i) =>
                  joueur.is_eliminated ? null : (
                    <button
                      type="button"
                      key={i}
                      className={`bh-bouton${vueForcee === i ? ' est-actif' : ''}${joueurActif === i ? ' est-joueur-actif' : ''}`}
                      title={joueur.area_hero?.[0]?.name ?? `${t('Joueur')} ${i}`}
                      onClick={() => setVueForcee(i)}
                    >
                      {joueur.area_hero?.[0]?.name?.replace(/^\W*/, '').split(' ')[0] ?? `P${i}`}
                    </button>
                  )
                )}
              </span>
            ) : null}

            <span className="bh-separateur" aria-hidden="true" />

            <ModeActionsBoutons modeActions={modeActions} changerModeActions={changerModeActions} />
            {/* Couper la musique doit se faire d'UN geste, sans ouvrir les
                réglages : c'est ce qu'on cherche quand quelqu'un entre dans la
                pièce. Le bouton sert aussi à la lancer — un navigateur refuse
                l'autoplay tant que la page n'a pas été cliquée, et ce clic-là
                fait justement office de geste. */}
            <button
              type="button"
              className={`bh-bouton bh-musique${musique ? ' est-actif' : ''}`}
              onClick={basculerMusique}
              aria-pressed={musique}
              title={
                musique
                  ? t('Couper la musique')
                  : t('Remettre la musique (nécessite un fichier dans assets/sounds)')
              }
            >
              <span aria-hidden="true">{musique ? '🔊' : '🔇'}</span>
            </button>
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
            <PanneauOptions
              animations={animations}
              basculerAnimations={basculerAnimations}
              sons={sons}
              basculerSons={basculerSons}
              meteo={meteo}
              apercuMeteo={apercuMeteo}
              reglerApercuMeteo={reglerApercuMeteo}
              reponseAmbiance={reponseAmbiance}
              cyclerReponseAmbiance={cyclerReponseAmbiance}
              basculerMeteo={basculerMeteo}
              revelation={revelation}
              cyclerRevelation={cyclerRevelation}
              autoCible={autoCible}
              basculerAutoCible={basculerAutoCible}
              curseurs={curseurs}
              basculerCurseurs={basculerCurseurs}
              scansFr={scansFr}
              basculerScansFr={basculerScansFr}
              textesCdb={textesCdb}
              basculerTextesCdb={basculerTextesCdb}
              succes={succes}
              basculerSucces={basculerSucces}
              modePhase={modePhase}
              changerModePhase={choisirModePhase}
              avanceAuto={avanceAuto}
              basculerAvanceAuto={basculerAvanceAuto}
              delaiPasAPas={delaiPasAPas}
              reglerDelaiPasAPas={choisirDelaiPasAPas}
              validationCourte={validationCourte}
              basculerValidationCourte={basculerValidationCourte}
              reglageMode={reglageMode}
              cyclerReglageMode={cyclerReglageMode}
              montrerDisposition={surAppareilMobile}
            />

            <span className="bh-separateur" aria-hidden="true" />

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
        delave={effetsAffiches(etat.monde, meteo, apercuMeteo).some((e) => EFFETS_DELAVANTS.includes(e))}
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
      <CoucheTriche actif={triche.actif} couche={triche.couche} />
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

      {/* L'ecran de fin attend que le coup fatal ait ete vu (mode Detaille,
          heros de ce siege), avec un filet de 20 s : voir
          `afficherFinDePartie`. Hors de ce cas, il parait sur la trame meme ou
          le moteur declare la partie finie, comme avant. */}
      {finPartieAffichee && etat.monde ? (
        <EcranFinPartie
          {...finDePartie(etat.monde, playerId)}
          raison={etat.monde.game_over_reason}
          monde={etat.monde}
          siege={playerId}
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
  const [modeActions, setModeActions] = useState<ModeActions>(() => lireModeActions())

  useEffect(() => {
    chargerCatalogue().then(setCatalogue).catch(() => undefined)
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
    <Outils modeActions={modeActions} changerModeActions={changerModeActions} />
  )

  // Le fournisseur enveloppe TOUT : les deux ecrans posent des questions
  // bloquantes, et le dialogue doit exister avant qu'on la pose.
  return (
    <FournisseurConfirmation>
      {etat ? (
        <PageEtat fichier={etat} playerId={playerId} catalogue={catalogue} outils={outils} />
      ) : (
        <PagePartie
          playerId={playerId}
          catalogue={catalogue}
          modeActions={modeActions}
          changerModeActions={changerModeActions}
        />
      )}
    </FournisseurConfirmation>
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
