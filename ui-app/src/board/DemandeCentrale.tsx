import { useEffect, useMemo, useRef, useState, type MouseEvent as ReactMouseEvent } from 'react'
import { ScanCard, type ScanCardProps } from '../components/ScanCard'
import { classeTonaliteAction } from './action-style'
import type { Demande, Option } from './ask'
import { CarteApercu } from './Board'
import { nettoyerNarration, nomLisible, sansIdentifiants } from './BarreAction'
import { t } from './langue'
import { avecIcones, marquerRessources } from './icones-ressources'
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
  /**
   * Le SCAN de la carte qu'une option nomme, quand elle en nomme une.
   *
   * Le moteur ne sait proposer qu'un nom quand il fait choisir entre des cartes
   * qui ne sont pas sur la table (« quelle chanson prends-tu ? »). Un nom seul
   * ne dit pas ce que fait la carte : signale en jeu sur Alison Blaire, dont le
   * joueur devait choisir a l'aveugle entre deux titres. Voir
   * carteNommeeParOption dans board.tsx.
   */
  carteDeLOption?: (option: Option) => ScanCardProps | undefined
  /**
   * Loge dans la scene du deroule detaille (DeroulePhase, prop `question`)
   * plutot que pose au centre de la table : plus de placement, plus de
   * position fixe, le panneau coule dans la scene a la place de ses boutons.
   */
  enScene?: boolean
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

/**
 * LE MOTEUR ATTEND-IL UNE REPONSE DU JOUEUR LOCAL ?
 *
 * A ne pas confondre avec « le panneau central est affiche ». Le panneau cede
 * la place a d'autres facons de repondre a la MEME question : un ciblage
 * (`interaction.option`, ou le joueur clique les cartes sur la table puis
 * « Valider »), le menu d'une carte, une animation d'effet en cours. Constate
 * en partie reelle : pendant le choix des deux sbires a activer, le panneau
 * disparaissait et le cartouche du deroule se redeployait pour annoncer « La
 * suite arrive… » alors que le moteur attendait le joueur. Le signal vient donc
 * de l'etat du MOTEUR, pas de la visibilite d'un panneau.
 *
 * `validationRequise` N'EST PLUS DEDANS, et c'est le correctif d'A6. Il y etait
 * comme filet : un cartouche replie n'a plus de bouton, et le replier pendant
 * qu'une trame est retenue ne laisserait plus personne la relacher. Mais la
 * garde mentait sur tout le reste du temps : le moteur pose ses questions de la
 * phase du mechant PENDANT qu'une trame est retenue (« Black Widow is being
 * attacked by Ultron · Defendre / Passer », `WhenUnitBeingAttack`, releve
 * plusieurs fois en partie), le panneau central ne paraissait pas, la question
 * tombait dans la barre du bas et le cartouche annoncait « La suite arrive… »
 * par-dessus. Le filet est desormais porte la ou il doit l'etre : dans
 * `cartoucheAJour` (DeroulePhase.tsx), ou une question posee au joueur est une
 * RAISON D'ACQUITTER. Cartouche replie implique donc cartouche a jour, donc
 * trame relachee, et le blocage est ferme par construction.
 *
 * `demandeDoitApparaitreAuCentre` reste dedans, lui, et ce n'est pas un oubli :
 * la question du TOUR LIBRE (`WhenPlayerInTurn` + `Normal`, « Passer » /
 * « Jouer X ») arrive quand la phase du mechant est finie et que le cartouche
 * montre son bilan, qu'il doit garder deploye jusqu'a « A toi de jouer ». Les
 * questions de la phase du mechant, elles, ont toutes leur propre evenement.
 */
export function moteurAttendUneReponse(etat: {
  aNous: boolean
  connecte: boolean
  demande?: Demande
}): boolean {
  return etat.aNous && etat.connecte && demandeDoitApparaitreAuCentre(etat.demande)
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
      <strong>{avecIcones(texte)}</strong>
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
  carteDeLOption,
  enScene = false,
}: DemandeCentraleProps) {
  const [raisonVisible, setRaisonVisible] = useState<number | undefined>(undefined)
  // Carte regardee : l'agrandissement s'ouvre au survol du bouton, comme au
  // survol d'une carte de la table, et avec le meme panneau (texte francais
  // compris). C'est LUI qui repond a « je ne sais pas ce que fait la carte » :
  // la vignette du bouton ne fait que la reconnaitre.
  const [carteRegardee, setCarteRegardee] = useState<ScanCardProps | undefined>(undefined)
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
  const { style } = usePlacement(panneau, { candidats: ['centre'], signature, actif: !enScene })

  useEffect(() => {
    setRaisonVisible(undefined)
    setCarteRegardee(undefined)
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

  // ⚠ LE SURVOL EST ECOUTE SUR LE CONTENEUR, pas sur chaque option (regle
  // commune, `apercu-survol.ts`). Pose sur chaque option, `mouseleave` n'est
  // jamais emis quand l'option disparait sous le pointeur, et l'agrandissement
  // reste ouvert sur une carte qui n'est plus la. Ici le declencheur n'est pas
  // la carte mais L'OPTION ENTIERE, vignette et bouton compris : c'est voulu,
  // on doit pouvoir lire la carte en visant le libelle.
  const survolerZone = (evenement: ReactMouseEvent) => {
    const zone = (evenement.target as HTMLElement).closest<HTMLElement>('.af-action-wrap')
    const vise = options.find((option) => String(option.id) === zone?.dataset.optionId)
    if (!vise) {
      setCarteRegardee(undefined)
      survolerOption?.(undefined)
      return
    }
    activerOption(vise, carteDeLOption?.(vise))
  }

  const quitterZone = () => {
    setCarteRegardee(undefined)
    survolerOption?.(undefined)
  }

  const activerOption = (option: Option, carte?: ScanCardProps) => {
    // L'agrandissement s'ouvre MEME sur une option indisponible : savoir
    // pourquoi on ne peut pas la prendre demande de lire la carte.
    setCarteRegardee(carte)
    if (!option.failure_reason) survolerOption?.(option)
  }

  const desactiverOption = (option: Option) => {
    setCarteRegardee(undefined)
    if (!option.failure_reason) survolerOption?.(undefined)
  }

  return (
    <section
      ref={panneau}
      className={`demande-centrale${enScene ? ' est-en-scene' : ''}`}
      style={enScene ? undefined : style}
      role="dialog"
      aria-label="Game decision"
      aria-live="polite"
    >
      <div className="dc-texte">
        <span className="plateau-eyebrow">{libelleTypeDemande(demande)}</span>
        <strong>{avecIcones(marquerRessources(titreDepuisSource(demande, options, cartesParId)))}</strong>
      </div>

      <div className="af-boutons dc-boutons" onMouseOver={survolerZone} onMouseLeave={quitterZone}>
        {options.map((option) => {
          const nom = nomLisible(option)
          const source = nomSource(option, cartesParId)
          const cibles = resumeCibles(option, cartesParId)
          const indisponible = option.failure_reason !== ''
          const montrerRaison = indisponible && raisonVisible === option.id
          const carte = carteDeLOption?.(option)
          return (
            <span
              className={`af-action-wrap${carte ? ' a-vignette' : ''}`}
              key={option.id}
              data-option-id={option.id}
            >
              {/* La carte que l'option nomme, en petit au-dessus du bouton.
                  Elle est CLIQUABLE : viser la carte plutot que son nom est le
                  geste naturel, et c'est celui de toutes les autres cartes de
                  l'ecran. Le survol, lui, ouvre le grand apercu. */}
              {carte ? (
                <span className="dc-vignette">
                  <ScanCard
                    {...carte}
                    state={indisponible ? 'disabled' : 'targetable'}
                    highlight={false}
                    onSelect={() => choisirOuInformer(option)}
                  />
                </span>
              ) : null}
              <button
                type="button"
                className={`af-action ${classeTonaliteAction(`${nom} ${demande.ability_type}`)}${
                  indisponible ? ' est-indisponible' : ''
                }`}
                aria-disabled={indisponible || undefined}
                title={indisponible ? option.failure_reason : undefined}
                onFocus={() => activerOption(option, carte)}
                onBlur={() => desactiverOption(option)}
                onClick={() => choisirOuInformer(option)}
              >
                <span>{avecIcones(marquerRessources(nom))}</span>
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

      {/* Le meme agrandissement que sur la table : scan en grand, mots-cles et
          texte francais. Il se monte dans <body> (portail) et passe devant ce
          panneau, comme il passe devant la table. */}
      {carteRegardee ? <CarteApercu carte={carteRegardee} /> : null}
    </section>
  )
}
