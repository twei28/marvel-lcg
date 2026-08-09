import { useEffect, useMemo, useRef, useState } from 'react'
import { classeTonaliteAction } from './action-style'
import type { Demande, Option } from './ask'
import { nettoyerNarration, nomLisible, sansIdentifiants } from './BarreAction'
import { t } from './langue'
import { usePlacement } from './placement/usePlacement'
import { traduireMoteur } from './vocabulaire-moteur'
import type { WorldCard } from './world'

type DemandeCentraleProps = {
  demande: Demande
  options: Option[]
  cartesParId: Map<number, WorldCard>
  choisirOption: (option: Option) => void
  annuler: () => void
  survolerOption?: (option: Option | undefined) => void
}

/** Le texte que le moteur a VRAIMENT envoyé, ou rien s'il n'a rien dit. */
function promptDemande(demande: Demande): string {
  const prompt = nettoyerNarration(sansIdentifiants(demande.prompt_text))
  return prompt ? prompt.replace(/^---\s*/, '').replace(/\s*---$/, '') : ''
}

function texteDemande(demande: Demande): string {
  const prompt = promptDemande(demande)
  if (prompt) return prompt
  if (demande.ability_type) return traduireMoteur(demande.ability_type)
  return t('Choisis une réponse')
}

function libelleTypeDemande(demande: Demande): string {
  // Le surtitre du panneau vient du moteur, donc de l'anglais : on le repasse
  // par le vocabulaire francais avant de l'afficher.
  if (demande.ability_type) return traduireMoteur(demande.ability_type)
  const depuisEvenement = demande.event_name
    .replace(/^When/, '')
    .replace(/([a-z])([A-Z])/g, '$1 $2')
  return depuisEvenement ? traduireMoteur(depuisEvenement) : t('Décision')
}

function nomSource(option: Option, cartesParId: Map<number, WorldCard>): string | undefined {
  if (option.bind_id === 0) return undefined
  return cartesParId.get(option.bind_id)?.name
}

/**
 * « A qui je le fais » : les cibles legales de l'option, en clair sous le
 * bouton. Trois noms maximum, puis « +N ». Une carte inconnue de la table
 * (face cachee) est nommee telle quelle.
 */
function resumeCibles(option: Option, cartesParId: Map<number, WorldCard>): string | undefined {
  if (option.target_num_range[1] === 0 || option.all_legal_targets.length === 0) return undefined
  const uniques = [...new Set(option.all_legal_targets)]
  const noms = uniques.map((id) => cartesParId.get(id)?.name ?? 'facedown card')
  const tetes = noms.slice(0, 3).join(', ')
  return `→ ${tetes}${noms.length > 3 ? ` +${noms.length - 3}` : ''}`
}

/**
 * Titre du panneau quand le moteur n'envoie AUCUN texte : plutot que « Normal »
 * (le type d'ability, illisible), on nomme la carte qui agit si toutes les
 * options viennent de la meme (« The Pericles — choose an option »).
 */
function titreDepuisSource(
  demande: Demande,
  options: Option[],
  cartesParId: Map<number, WorldCard>
): string {
  // On teste l'ABSENCE de prompt, pas l'égalité du texte rendu avec
  // `ability_type` : depuis que ce dernier est traduit, les deux ne peuvent
  // plus coïncider en français, et la comparaison laissait passer « Normal »
  // au lieu de nommer la carte.
  if (promptDemande(demande)) return texteDemande(demande)
  const sources = [...new Set(options.map((o) => o.bind_id).filter((id) => id !== 0))]
  const nom = sources.length === 1 ? cartesParId.get(sources[0]!)?.name : undefined
  return nom ? `${nom} — ${t('choisis une option')}` : texteDemande(demande)
}

export function demandeDoitApparaitreAuCentre(demande: Demande | undefined): boolean {
  if (!demande) return false
  return demande.event_name !== 'WhenPlayerInTurn' || demande.ability_type !== 'Normal'
}

function libelleEvenement(eventName: string): string {
  const decoupe = eventName
    .replace(/^When/, '')
    .replace(/([a-z])([A-Z])/g, '$1 $2')
    .replace(/^After /, '')
    .trim()
  return decoupe ? traduireMoteur(decoupe) : t('Événement de jeu')
}

/** Narration courte des resolutions automatiques, au meme endroit que les choix. */
export function EvenementCentrale({
  prompt,
  eventName,
  message,
  validationRequise = false,
  continuer,
  cartes,
}: {
  prompt: string
  eventName: string
  message?: string
  validationRequise?: boolean
  continuer?: () => void
  /** Cartes citées par l'événement : c'est d'elles qu'on parle, on les laisse voir. */
  cartes?: readonly number[]
}) {
  const [texte, setTexte] = useState('')
  const [visible, setVisible] = useState(false)
  const signature = `${eventName}|${prompt}|${message ?? ''}`
  const panneau = useRef<HTMLElement | null>(null)
  // Fixe, comme les autres panneaux : les quatre sont mutuellement exclusifs
  // (voir les conditions d'affichage dans board.tsx), donc partager une ancre
  // ne les fait jamais se recouvrir entre eux.
  const { style } = usePlacement(panneau, {
    candidats: ['centre'],
    signature,
    actif: visible,
  })

  useEffect(() => {
    const propre =
      nettoyerNarration(sansIdentifiants(message ?? prompt)) || libelleEvenement(eventName)
    setTexte(propre.replace(/^---\s*/, '').replace(/\s*---$/, ''))
    setVisible(true)
    const minuterie = validationRequise
      ? undefined
      : window.setTimeout(() => setVisible(false), 2400)
    return () => {
      if (minuterie !== undefined) window.clearTimeout(minuterie)
    }
  }, [signature, eventName, message, prompt, validationRequise])

  if (!visible || !texte) return null
  return (
    <section
      ref={panneau}
      className="evenement-centrale"
      style={style}
      aria-live="polite"
      aria-label={t('Événement de jeu')}
    >
      <span className="plateau-eyebrow">{libelleEvenement(eventName)}</span>
      <strong>{texte}</strong>
      {validationRequise && continuer ? (
        <button type="button" className="dc-continue" onClick={continuer}>
          {t('Continuer')}
        </button>
      ) : null}
    </section>
  )
}

export function DemandeCentrale({
  demande,
  options,
  cartesParId,
  choisirOption,
  annuler,
  survolerOption,
}: DemandeCentraleProps) {
  const [raisonVisible, setRaisonVisible] = useState<number | undefined>(undefined)
  const signature = useMemo(
    () => `${demande.event_name}|${demande.ability_type}|${options.map((option) => option.id).join(',')}`,
    [demande.ability_type, demande.event_name, options]
  )

  // Le panneau NE BOUGE PAS : une seule position candidate, toujours la même.
  //
  // Il a d'abord esquivé les cartes qu'il concerne. À l'usage c'est pire : on
  // le voyait sauter en haut de l'écran d'une décision à l'autre, et il fallait
  // le chercher du regard à chaque fois. Une décision doit être là où on
  // l'attend. Quand une carte agrandie le recouvre, c'est ELLE qui passe devant
  // (z-index 400 contre 92) — le panneau est permanent, l'agrandissement non.
  const panneau = useRef<HTMLElement | null>(null)
  const { style } = usePlacement(panneau, { candidats: ['centre'], signature })

  useEffect(() => {
    setRaisonVisible(undefined)
    survolerOption?.(undefined)
  }, [signature, survolerOption])

  useEffect(() => () => survolerOption?.(undefined), [survolerOption])

  const choisirOuInformer = (option: Option) => {
    if (option.failure_reason) {
      setRaisonVisible(option.id)
      return
    }
    choisirOption(option)
  }

  const activerOption = (option: Option) => {
    if (!option.failure_reason) survolerOption?.(option)
  }

  const desactiverOption = (option: Option) => {
    if (!option.failure_reason) survolerOption?.(undefined)
  }

  return (
    <section
      ref={panneau}
      className="demande-centrale"
      style={style}
      role="dialog"
      aria-label="Game decision"
      aria-live="polite"
    >
      <div className="dc-texte">
        <span className="plateau-eyebrow">{libelleTypeDemande(demande)}</span>
        <strong>{titreDepuisSource(demande, options, cartesParId)}</strong>
      </div>

      <div className="af-boutons dc-boutons">
        {options.map((option) => {
          const nom = nomLisible(option)
          const source = nomSource(option, cartesParId)
          const cibles = resumeCibles(option, cartesParId)
          const indisponible = option.failure_reason !== ''
          const montrerRaison = indisponible && raisonVisible === option.id
          return (
            <span className="af-action-wrap" key={option.id}>
              <button
                type="button"
                className={`af-action ${classeTonaliteAction(`${nom} ${demande.ability_type}`)}${
                  indisponible ? ' est-indisponible' : ''
                }`}
                aria-disabled={indisponible || undefined}
                title={indisponible ? option.failure_reason : undefined}
                onMouseEnter={() => activerOption(option)}
                onMouseLeave={() => desactiverOption(option)}
                onFocus={() => activerOption(option)}
                onBlur={() => desactiverOption(option)}
                onClick={() => choisirOuInformer(option)}
              >
                <span>{nom}</span>
                {source ? <small>{source}</small> : null}
                {cibles ? <small className="af-cibles">{cibles}</small> : null}
              </button>
              {montrerRaison ? <span className="af-raison">{option.failure_reason}</span> : null}
            </span>
          )
        })}
        {demande.show_cancel ? (
          <span className="af-action-wrap">
            <button type="button" className="af-action tonalite-general dc-pass" onClick={annuler}>
              {t('Passer')}
            </button>
          </span>
        ) : null}
      </div>
    </section>
  )
}
