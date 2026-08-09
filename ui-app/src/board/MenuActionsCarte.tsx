import { useEffect, useMemo, useRef, useState, type KeyboardEvent as ReactKeyboardEvent } from 'react'
import { kindLabel, type ScanCardProps } from '../components/ScanCard'
import { nombreDeRessources, paiementCourant, type Option } from './ask'
import { classeTonaliteAction } from './action-style'
import { nomLisible } from './BarreAction'
import type { Catalogue } from './catalogue'
import { t } from './langue'
import { usePlacement } from './placement/usePlacement'
import { codeMarvelcdb, urlMarvelcdb } from './marvelcdb'
import { isScheme, isUnit, isVisibleFor, type WorldCard } from './world'

type MenuActionsCarteProps = {
  carte: ScanCardProps
  carteMonde?: WorldCard
  options: Option[]
  /** Toutes les options du moteur, non filtrees : sert a expliquer pourquoi une
   *  cible (complot / ennemi) ne peut pas etre contree ou attaquee. */
  toutesOptions?: Option[]
  cartesParId: Map<number, WorldCard>
  catalogue: Catalogue
  choisirOption: (option: Option, ciblesInitiales?: number[]) => void
  annulerDemande?: () => void
  libelleAnnulation?: string
  fermer: () => void
  playerId: number
  survolerOption?: (option: Option | undefined) => void
  idsAffiches?: ReadonlySet<number>
  ouvrirCiblesHorsTable?: (option: Option) => void
  mode?: 'source' | 'target'
  ciblePreselectionnee?: number
  affichage?: 'simple' | 'detailed'
}

type ActionAffichee = {
  option: Option
  nom: string
  sourceNom?: string
  detailStat?: string
  detailCibles?: string
  cibles: CibleAffichee[]
  schemesNonLegaux: CibleAffichee[]
  cout?: string
  priorite: number
  ordre: number
}

type CibleAffichee = {
  id: number
  nom: string
  fois: number
  horsTable: boolean
  details: string[]
  raisons: string[]
}

const STATS_ACTIONS: Array<{
  mots: string[]
  cle: string
  label: string
}> = [
  { mots: ['attack'], cle: 'attack', label: 'Attaque' },
  { mots: ['thwart'], cle: 'thwart', label: 'Contre' },
  { mots: ['recover'], cle: 'recover', label: 'Récupération' },
  { mots: ['defense', 'defend'], cle: 'defense', label: 'Défense' },
  { mots: ['scheme'], cle: 'scheme', label: 'Manigance' },
]

function prioriteAction(nom: string): number {
  const action = nom.toLowerCase()
  if (action === 'play') return 0
  if (['attack', 'thwart', 'recover', 'defense', 'defend'].includes(action)) return 1
  if (action === 'change form') return 2
  if (action.includes('action')) return 3
  return 4
}

function valeurImprimee(catalogue: Catalogue, carte: WorldCard, label: string): number | undefined {
  const code = label === 'Attaque' ? 'ATK' : label === 'Contre' ? 'THW' : label === 'Récupération' ? 'REC' : label === 'Défense' ? 'DEF' : 'SCH'
  return catalogue.statImprimee(carte.card_id, code)
}

function detailStat(option: Option, carte: WorldCard | undefined, catalogue: Catalogue): string | undefined {
  if (!carte || !isUnit(carte)) return undefined
  const nom = nomLisible(option).toLowerCase()
  const stat = STATS_ACTIONS.find((candidate) => candidate.mots.some((mot) => nom.includes(mot)))
  if (!stat) return undefined
  const courante = carte.info[stat.cle]
  if (typeof courante !== 'number') return undefined
  const imprimee = valeurImprimee(catalogue, carte, stat.label)
  if (imprimee !== undefined && imprimee !== courante) {
    return `${t(stat.label)} ${imprimee} -> ${courante}`
  }
  return `${t(stat.label)} ${courante}`
}

function libelleTypeCible(cibles: WorldCard[]): string {
  if (cibles.length === 0) return 'cible'
  if (cibles.every((carte) => ['EncounterVillain', 'Minion'].includes(carte.card_type))) return 'ennemi'
  if (cibles.every(isScheme)) return 'manigance'
  if (cibles.every(isUnit)) return 'personnage'
  if (cibles.every((carte) => carte.card_type === cibles[0]?.card_type)) {
    return kindLabel[
      cibles[0]?.card_type === 'MainScheme' ||
      cibles[0]?.card_type === 'EncounterSideScheme' ||
      cibles[0]?.card_type === 'PlayerSideScheme'
        ? 'side-scheme'
        : 'unknown'
    ].toLowerCase()
  }
  return 'cible'
}

function detailCibles(option: Option, cartesParId: Map<number, WorldCard>): string | undefined {
  const [min, max] = option.target_num_range
  if (max === 0 || option.all_legal_targets.length === 0) return undefined
  const idsUniques = [...new Set(option.all_legal_targets)]
  const cartes = idsUniques.map((id) => cartesParId.get(id)).filter((c): c is WorldCard => c !== undefined)
  const nombre = min === max ? String(max) : `${min}-${max}`
  return `${nombre} ${t(libelleTypeCible(cartes))} · ${idsUniques.length} ${idsUniques.length > 1 ? t('possibles') : t('possible')}`
}

function detailCiblePreselectionnee(
  cible: number | undefined,
  cartesParId: Map<number, WorldCard>
): string | undefined {
  if (cible === undefined) return undefined
  const carte = cartesParId.get(cible)
  return carte ? `${t('Cible :')} ${carte.name}` : `${t('Cible :')} ${cible}`
}

function ciblesAffichees(
  option: Option,
  cartesParId: Map<number, WorldCard>,
  playerId: number,
  idsAffiches: ReadonlySet<number> | undefined,
  cibleFiltre?: number
): CibleAffichee[] {
  if (option.target_num_range[1] === 0) return []
  const occurrences = new Map<number, number>()
  for (const id of option.all_legal_targets) {
    occurrences.set(id, (occurrences.get(id) ?? 0) + 1)
  }
  const entrees =
    cibleFiltre !== undefined && occurrences.has(cibleFiltre)
      ? ([[cibleFiltre, occurrences.get(cibleFiltre)!]] as Array<[number, number]>)
      : [...occurrences.entries()]
  return entrees.map(([id, fois]) => {
    const carte = cartesParId.get(id)
    const visible = carte ? isVisibleFor(carte, playerId) || option.is_search : false
    const nom = carte
      ? visible
        ? carte.name
        : t('Carte face cachée')
      : `${t('Cible')} ${id}`
    return {
      id,
      nom,
      fois,
      horsTable: idsAffiches !== undefined && !idsAffiches.has(id),
      details: carte && visible ? detailsCible(carte) : [],
      raisons: [],
    }
  })
}

function actionRetireMenace(nom: string): boolean {
  return nom.toLowerCase().includes('thwart')
}

function estVisibleSurTable(
  carte: WorldCard,
  playerId: number,
  idsAffiches: ReadonlySet<number> | undefined
): boolean {
  if (idsAffiches !== undefined && !idsAffiches.has(carte.id)) return false
  return carte.is_face_up || isVisibleFor(carte, playerId)
}

function cartesVisiblesSurTable(
  cartesParId: Map<number, WorldCard>,
  playerId: number,
  idsAffiches: ReadonlySet<number> | undefined
): WorldCard[] {
  return [...cartesParId.values()].filter((carte) =>
    estVisibleSurTable(carte, playerId, idsAffiches)
  )
}

function nombreInfo(carte: WorldCard, cle: string): number | undefined {
  const valeur = carte.info[cle]
  return typeof valeur === 'number' ? valeur : undefined
}

function traitLisible(trait: string): string {
  return trait.startsWith('t_') ? trait.slice(2).replace(/_/g, ' ') : trait
}

function detailsCible(carte: WorldCard): string[] {
  const details: string[] = []

  if (isScheme(carte)) {
    const menace = nombreInfo(carte, 'k_threat')
    const cible = nombreInfo(carte, 'target_threat')
    if (menace !== undefined) {
      details.push(cible !== undefined && cible > 0 ? `${menace}/${cible} ${t('menace')}` : `${menace} ${t('menace')}`)
    }
    if (nombreInfo(carte, 'permanent')) details.push('Permanent')
    if (nombreInfo(carte, 'crisis')) details.push(t('Crise'))
    if (nombreInfo(carte, 'hazard')) details.push(t('Aléa'))
    if (nombreInfo(carte, 'amplify')) details.push(t('Amplification'))
    const acceleration = nombreInfo(carte, 'acceleration_icon')
    if (acceleration) details.push(`${acceleration} ${t('accélération')}`)
  } else if (isUnit(carte)) {
    const vie = nombreInfo(carte, 'health')
    if (vie !== undefined) details.push(`${vie} ${t('PV')}`)
    const scheme = nombreInfo(carte, 'scheme')
    if (scheme !== undefined) details.push(`${t('MNG')} ${scheme}`)
    const attack = nombreInfo(carte, 'attack')
    if (attack !== undefined) details.push(`${t('ATQ')} ${attack}`)
    const thwart = nombreInfo(carte, 'thwart')
    if (thwart !== undefined) details.push(`${t('CTR')} ${thwart}`)
  }

  const traits = Object.entries(carte.traits ?? {})
    .filter(([, actif]) => Boolean(actif))
    .map(([trait]) => traitLisible(trait))
  return [...details, ...traits]
}

function nomAvecPorteur(source: WorldCard, cartesParId: Map<number, WorldCard>): string {
  const porteur = source.bind_object_id ? cartesParId.get(source.bind_object_id) : undefined
  return porteur ? `${source.name} ${t('sur')} ${porteur.name}` : source.name
}

function raisonsSchemeNonLegal(
  scheme: WorldCard,
  cartesSurTable: WorldCard[],
  cartesParId: Map<number, WorldCard>
): string[] {
  const raisons: string[] = []

  if (scheme.name === 'Light at the End') {
    for (const source of cartesSurTable.filter((carte) => carte.name === 'Taunting Presence')) {
      raisons.push(`${t('Bloquée par')} ${nomAvecPorteur(source, cartesParId)}`)
    }
  }

  if (scheme.name !== 'Brute Force Barricade') {
    for (const source of cartesSurTable.filter((carte) => carte.name === 'Brute Force Barricade')) {
      raisons.push(`${t('Bloquée par')} ${source.name}`)
    }
  }

  // CRISE. Tant qu'une manigance annexe portant l'icone est en jeu, les joueurs
  // ne peuvent pas retirer de menace de la manigance PRINCIPALE. Le moteur
  // applique la regle correctement, mais sans un mot : on jouait une carte de
  // contre, rien ne se passait, et rien n'expliquait pourquoi. On nomme donc la
  // carte responsable — c'est elle qu'il faut vaincre pour se debloquer.
  if (scheme.card_type === 'MainScheme') {
    for (const source of cartesSurTable) {
      if (source.id !== scheme.id && (nombreInfo(source, 'crisis') ?? 0) > 0) {
        raisons.push(`${t('Bloquée par')} ${source.name} (${t('Crise')})`)
      }
    }
  }

  return raisons.length > 0 ? raisons : [t('Pas légale dans l\'état actuel de la partie')]
}

function schemesNonLegaux(
  option: Option,
  nom: string,
  cartesParId: Map<number, WorldCard>,
  playerId: number,
  idsAffiches: ReadonlySet<number> | undefined
): CibleAffichee[] {
  if (option.failure_reason || !actionRetireMenace(nom) || option.target_num_range[1] === 0) {
    return []
  }

  const legales = new Set(option.all_legal_targets)
  const ciblesLegales = [...legales].map((id) => cartesParId.get(id)).filter((c): c is WorldCard => c !== undefined)
  if (ciblesLegales.length > 0 && !ciblesLegales.every(isScheme)) return []

  const cartesSurTable = cartesVisiblesSurTable(cartesParId, playerId, idsAffiches)

  return [...cartesParId.values()]
    .filter((carte) => isScheme(carte))
    .filter((carte) => !legales.has(carte.id))
    .filter((carte) => estVisibleSurTable(carte, playerId, idsAffiches))
    .map((carte) => ({
      id: carte.id,
      nom: carte.name,
      fois: 1,
      horsTable: false,
      details: detailsCible(carte),
      raisons: raisonsSchemeNonLegal(carte, cartesSurTable, cartesParId),
    }))
}

function estEnnemi(carte: WorldCard): boolean {
  return carte.card_type === 'EncounterVillain' || carte.card_type === 'Minion'
}

export type VerdictCiblage = {
  /** thwart pour un complot, attack pour un ennemi. */
  type: 'thwart' | 'attack'
  possible: boolean
  raisons: string[]
}

/**
 * Pour une carte-CIBLE (complot ou ennemi) cliquee : peut-on la contrer / l'attaquer
 * maintenant, et sinon pourquoi ? Le verdict « possible » vient du moteur (la cible est
 * dans les all_legal_targets d'une action utilisable). La raison est, dans l'ordre :
 * l'etat de la carte (menace nulle), le failure_reason du moteur si l'action est
 * bloquee, un blocage connu (Taunting Presence...), sinon une explication generique.
 */
function verdictCiblage(
  carte: WorldCard,
  toutesOptions: Option[],
  cartesSurTable: WorldCard[],
  cartesParId: Map<number, WorldCard>
): VerdictCiblage | undefined {
  const scheme = isScheme(carte)
  const ennemi = estEnnemi(carte)
  if (!scheme && !ennemi) return undefined

  const type: 'thwart' | 'attack' = scheme ? 'thwart' : 'attack'
  const options = toutesOptions.filter((o) => nomLisible(o).toLowerCase().includes(type))
  const utilisables = options.filter((o) => !o.failure_reason && o.target_num_range[1] > 0)
  const possible = utilisables.some((o) => o.all_legal_targets.includes(carte.id))
  if (possible) return { type, possible: true, raisons: [] }

  // Complot sans menace : rien a retirer, c'est LA raison, inutile d'en dire plus.
  if (scheme && nombreInfo(carte, 'k_threat') === 0) {
    return { type, possible: false, raisons: [t('Aucune menace à retirer pour le moment')] }
  }

  const raisons: string[] = []
  if (utilisables.length > 0) {
    // L'action existe et est utilisable, mais cette carte n'est pas une cible legale.
    if (scheme) raisons.push(...raisonsSchemeNonLegal(carte, cartesSurTable, cartesParId))
    else raisons.push(t('Pas une cible légale dans l\'état actuel de la partie'))
  } else if (options.length > 0) {
    // L'action existe mais est bloquee : le moteur en donne souvent la raison.
    const duMoteur = [...new Set(options.map((o) => o.failure_reason).filter(Boolean))]
    raisons.push(
      ...(duMoteur.length > 0
        ? duMoteur
        : [
            scheme
              ? t('Aucune action de contre utilisable pour le moment')
              : t('Aucune action d\'attaque utilisable pour le moment'),
          ])
    )
  } else {
    raisons.push(
      scheme
        ? t('Aucun personnage redressé ne peut contrer pour le moment (mauvaise phase, incliné, ou désorienté)')
        : t('Aucun personnage redressé ne peut attaquer pour le moment (mauvaise phase, incliné, sonné, ou non engagé)')
    )
  }
  if (raisons.length === 0) raisons.push(t('Pas disponible dans l\'état actuel de la partie'))
  return { type, possible: false, raisons: [...new Set(raisons)] }
}

function coutAction(option: Option): string | undefined {
  const paiement = paiementCourant(option, [])
  const ressources = nombreDeRessources(paiement)
  if (ressources === 0) return undefined
  if (ressources !== undefined) return String(ressources)
  return paiement?.cost && paiement.cost !== '0' ? paiement.cost : undefined
}

function PipsCout({ cout }: { cout: string }) {
  const nombre = Number(cout)
  if (!Number.isInteger(nombre) || nombre < 0 || nombre > 6) {
    return <span className="ma-cout-texte">{cout}</span>
  }
  if (nombre === 0) return <span className="ma-cout-zero">0</span>
  return (
    <span className="ma-cout-pips" aria-label={`${t('Coût')} ${nombre}`}>
      {Array.from({ length: nombre }, (_, index) => (
        <span key={index} />
      ))}
    </span>
  )
}

function ContenuCible({ target }: { target: CibleAffichee }) {
  return (
    <>
      <span className="ma-cible-texte">
        <span className="ma-cible-nom">{target.nom}</span>
        {target.details.length > 0 ? (
          <span className="ma-cible-meta">{target.details.join(' - ')}</span>
        ) : null}
        {target.raisons.map((raison) => (
          <span className="ma-cible-raison" key={raison}>
            {raison}
          </span>
        ))}
      </span>
      {target.fois > 1 ? <b>{target.fois}x</b> : null}
    </>
  )
}

export function MenuActionsCarte({
  carte,
  carteMonde,
  options,
  toutesOptions,
  cartesParId,
  catalogue,
  choisirOption,
  annulerDemande,
  libelleAnnulation = t('Passer'),
  fermer,
  playerId,
  survolerOption,
  idsAffiches,
  ouvrirCiblesHorsTable,
  mode = 'source',
  ciblePreselectionnee,
  affichage = 'detailed',
}: MenuActionsCarteProps) {
  const ref = useRef<HTMLElement>(null)
  const [raisonVisible, setRaisonVisible] = useState<number | undefined>(undefined)
  const [optionActive, setOptionActive] = useState<number | undefined>(undefined)

  useEffect(() => {
    setRaisonVisible(undefined)
    setOptionActive(undefined)
    survolerOption?.(undefined)
  }, [carte.id])

  useEffect(() => () => survolerOption?.(undefined), [survolerOption])

  // Fixe, comme les autres panneaux de decision : il s'ouvre toujours au meme
  // endroit. Une carte agrandie passe devant lui, pas l'inverse.
  const { style: stylePlacement } = usePlacement(ref, {
    candidats: ['centre'],
    signature: `${carte.id}|${mode}|${options.map((o) => o.id).join(',')}`,
  })

  const activerOption = (option: Option) => {
    if (option.failure_reason) return
    setOptionActive(option.id)
    survolerOption?.(option)
  }

  const desactiverOption = (option: Option) => {
    if (option.failure_reason) return
    setOptionActive(undefined)
    survolerOption?.(undefined)
  }

  const choisirOuInformer = (option: Option) => {
    if (option.failure_reason) {
      setRaisonVisible(option.id)
      return
    }
    choisirOption(
      option,
      ciblePreselectionnee !== undefined && option.all_legal_targets.includes(ciblePreselectionnee)
        ? [ciblePreselectionnee]
        : undefined
    )
  }

  const clavierAction = (evenement: ReactKeyboardEvent, option: Option) => {
    if (evenement.key !== 'Enter' && evenement.key !== ' ') return
    evenement.preventDefault()
    choisirOuInformer(option)
  }

  const boutonAnnulationSimple = annulerDemande ? (
    <span className="af-action-wrap">
      <button
        type="button"
        className="af-action tonalite-general af-annulation"
        onClick={annulerDemande}
      >
        {libelleAnnulation}
      </button>
    </span>
  ) : null

  const boutonAnnulationDetaille = annulerDemande ? (
    <button
      type="button"
      className="ma-action ma-action-annulation"
      onClick={annulerDemande}
    >
      <span className="ma-action-principal">
        <b>{libelleAnnulation}</b>
      </span>
    </button>
  ) : null

  useEffect(() => {
    const fermerClavier = (evenement: KeyboardEvent) => {
      if (evenement.key === 'Escape') fermer()
    }
    const fermerClic = (evenement: PointerEvent) => {
      const cible = evenement.target
      if (!(cible instanceof HTMLElement)) return
      if (ref.current?.contains(cible)) return
      if (cible.closest('.scan-card')) return
      if (cible.closest('.plateau-action')) return
      fermer()
    }
    document.addEventListener('keydown', fermerClavier)
    document.addEventListener('pointerdown', fermerClic)
    return () => {
      document.removeEventListener('keydown', fermerClavier)
      document.removeEventListener('pointerdown', fermerClic)
    }
  }, [fermer])

  const actions = useMemo<ActionAffichee[]>(
    () =>
      options
        .map((option, ordre) => {
          const nom = nomLisible(option)
          const source = option.bind_id ? cartesParId.get(option.bind_id) : undefined
          const cartePourStat = mode === 'target' ? source : carteMonde
          return {
            option,
            nom,
            sourceNom: source?.name,
            detailStat: detailStat(option, cartePourStat, catalogue),
            detailCibles:
              detailCiblePreselectionnee(ciblePreselectionnee, cartesParId) ??
              detailCibles(option, cartesParId),
            cibles: ciblesAffichees(
              option,
              cartesParId,
              playerId,
              idsAffiches,
              ciblePreselectionnee
            ),
            schemesNonLegaux: schemesNonLegaux(option, nom, cartesParId, playerId, idsAffiches),
            cout: coutAction(option),
            priorite: prioriteAction(nom),
            ordre,
          }
        })
        .sort((a, b) => {
          const disabled = Number(Boolean(a.option.failure_reason)) - Number(Boolean(b.option.failure_reason))
          if (disabled !== 0) return disabled
          if (a.priorite !== b.priorite) return a.priorite - b.priorite
          return a.ordre - b.ordre
        }),
    [options, carteMonde, catalogue, cartesParId, idsAffiches, playerId, ciblePreselectionnee, mode]
  )

  const groupesActions = useMemo(() => {
    if (mode !== 'target') return [{ cle: 'actions', titre: undefined, actions }]
    const groupes = new Map<string, { cle: string; titre: string; actions: ActionAffichee[] }>()
    for (const action of actions) {
      const titre =
        action.option.bind_id === 0
          ? t('Actions générales')
          : action.sourceNom ?? `${t('Carte')} ${action.option.bind_id}`
      const cle = `${action.option.bind_id}:${titre}`
      const groupe = groupes.get(cle) ?? { cle, titre, actions: [] }
      groupe.actions.push(action)
      groupes.set(cle, groupe)
    }
    return [...groupes.values()]
  }, [actions, mode])

  // Carte-cible cliquee (complot / ennemi) : peut-elle etre contree / attaquee, sinon pourquoi ?
  const verdict = useMemo(
    () =>
      carteMonde
        ? verdictCiblage(
            carteMonde,
            toutesOptions ?? [],
            cartesVisiblesSurTable(cartesParId, playerId, idsAffiches),
            cartesParId
          )
        : undefined,
    [carteMonde, toutesOptions, cartesParId, playerId, idsAffiches]
  )

  if (affichage === 'simple') {
    return (
      <section
        className="actions-flottantes"
        style={stylePlacement}
        ref={ref}
        role="dialog"
        aria-label={`${t('Actions de')} ${carte.name}`}
      >
        <button type="button" className="af-fermer" aria-label={t('Fermer')} onClick={fermer}>
          X
        </button>
        <div className="af-boutons">
          {actions.length === 0 && !boutonAnnulationSimple ? (
            <span className="af-vide">{t('Aucune action')}</span>
          ) : (
            actions.map(({ option, nom }) => {
              const disabled = option.failure_reason !== ''
              const montrerRaison = disabled && raisonVisible === option.id
              return (
                <span className="af-action-wrap" key={option.id}>
                  <button
                    type="button"
                    className={`af-action ${classeTonaliteAction(nom)}${disabled ? ' est-indisponible' : ''}`}
                    aria-disabled={disabled || undefined}
                    title={disabled ? option.failure_reason : undefined}
                    onMouseEnter={() => activerOption(option)}
                    onMouseLeave={() => desactiverOption(option)}
                    onFocus={() => activerOption(option)}
                    onBlur={() => desactiverOption(option)}
                    onClick={() => choisirOuInformer(option)}
                    onKeyDown={(evenement) => clavierAction(evenement, option)}
                  >
                    {nom}
                  </button>
                  {montrerRaison ? (
                    <span className="af-raison">{option.failure_reason}</span>
                  ) : null}
                </span>
              )
            })
          )}
          {boutonAnnulationSimple}
        </div>
      </section>
    )
  }

  const codeCdb = carte.facedown ? undefined : codeMarvelcdb(carte.codeCarte)
  return (
    <section
      className={`menu-actions-carte${mode === 'target' ? ' mode-cible-focus' : ''}`}
      style={stylePlacement}
      ref={ref}
      role="dialog"
      aria-label={`${t('Actions de')} ${carte.name}`}
    >
      <header className="ma-entete">
        <div>
          <span className="plateau-eyebrow">
            {mode === 'target' ? t('Cible') : t(kindLabel[carte.kind])}
          </span>
          <strong>{carte.name}</strong>
        </div>
        <button type="button" className="ma-fermer" aria-label={t('Fermer')} onClick={fermer}>
          X
        </button>
      </header>

      {verdict ? (
        <div className={`ma-ciblage ${verdict.possible ? 'est-possible' : 'est-bloque'}`}>
          <span className="ma-ciblage-titre">
            {verdict.type === 'thwart'
              ? verdict.possible
                ? t('Peut être contrée')
                : t('Ne peut pas être contrée')
              : verdict.possible
                ? t('Peut être attaqué')
                : t('Ne peut pas être attaqué')}
          </span>
          {verdict.raisons.map((raison) => (
            <span className="ma-ciblage-raison" key={raison}>
              {raison}
            </span>
          ))}
        </div>
      ) : null}

      {actions.length === 0 ? (
        verdict || boutonAnnulationDetaille ? null : <p className="ma-vide">{t('Aucune action disponible')}</p>
      ) : (
        <div className="ma-actions">
          {groupesActions.map((groupe) => (
            <div className="ma-groupe" key={groupe.cle}>
              {groupe.titre ? <span className="ma-groupe-titre">{groupe.titre}</span> : null}
              {groupe.actions.map(({ option, nom, detailStat: stat, detailCibles: cible, cibles, schemesNonLegaux, cout }) => {
                const disabled = option.failure_reason !== ''
                const montrerRaison = disabled && raisonVisible === option.id
                const ciblesActives = !disabled && optionActive === option.id && cibles.length > 0
                return (
                  <div
                    key={option.id}
                    role="button"
                    tabIndex={0}
                    className={`ma-action${disabled ? ' est-indisponible' : ''}${montrerRaison ? ' a-raison-visible' : ''}${ciblesActives ? ' a-cibles-actives' : ''}`}
                    aria-disabled={disabled || undefined}
                    title={disabled ? option.failure_reason : undefined}
                    onMouseEnter={() => activerOption(option)}
                    onMouseLeave={() => desactiverOption(option)}
                    onFocus={() => activerOption(option)}
                    onBlur={() => desactiverOption(option)}
                    onClick={() => choisirOuInformer(option)}
                    onKeyDown={(evenement) => clavierAction(evenement, option)}
                  >
                    <span className="ma-action-principal">
                      <b>{nom}</b>
                      {cout ? (
                        <span className="ma-cout">
                          <PipsCout cout={cout} />
                        </span>
                      ) : null}
                    </span>
                    {stat || cible ? (
                      <span className="ma-details">
                        {stat ? <span>{stat}</span> : null}
                        {cible ? <span>{cible}</span> : null}
                      </span>
                    ) : null}
                    {cibles.length > 0 ? (
                      <span className="ma-cibles" aria-label={t('Cibles possibles')}>
                        {cibles.map((target) => {
                          const contenu = <ContenuCible target={target} />
                          return target.horsTable && ouvrirCiblesHorsTable ? (
                            <button
                              type="button"
                              className="ma-cible est-hors-table"
                              key={target.id}
                              onClick={(evenement) => {
                                evenement.stopPropagation()
                                ouvrirCiblesHorsTable(option)
                              }}
                              onKeyDown={(evenement) => evenement.stopPropagation()}
                            >
                              {contenu}
                            </button>
                          ) : (
                            <span className="ma-cible" key={target.id}>
                              {contenu}
                            </span>
                          )
                        })}
                      </span>
                    ) : null}
                    {schemesNonLegaux.length > 0 ? (
                      <span className="ma-cibles ma-cibles-verrouillees" aria-label={t('Manigances pas légales maintenant')}>
                        <span className="ma-cibles-libelle">{t('Pas légal maintenant')}</span>
                        {schemesNonLegaux.map((target) => (
                          <span className="ma-cible est-non-legale" key={target.id}>
                            <ContenuCible target={target} />
                          </span>
                        ))}
                      </span>
                    ) : null}
                    {disabled ? <span className="ma-action-raison">{option.failure_reason}</span> : null}
                  </div>
                )
              })}
            </div>
          ))}
        </div>
      )}
      {boutonAnnulationDetaille ? <div className="ma-actions">{boutonAnnulationDetaille}</div> : null}
      {codeCdb ? (
        <a
          className="ma-lien-cdb"
          href={urlMarvelcdb(codeCdb)}
          target="_blank"
          rel="noreferrer"
          onClick={(evenement) => evenement.stopPropagation()}
        >
          {t('Voir sur marvelcdb')} {'\u2197'}
        </a>
      ) : null}
    </section>
  )
}
