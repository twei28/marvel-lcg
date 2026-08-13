// Le bilan de la phase du méchant, en une fois.
//
// En mode rapide, la phase s'enchaîne sans s'arrêter : plus de présentation
// plein écran, plus de « Continue » à chaque activation. On ne voit donc plus
// passer ce qu'on a encaissé. Ce panneau le rejoue à la fin, groupé.
//
// Il ne réinvente rien : il relit les entrées que l'historique a déjà produites
// pendant la phase. Chaque entrée porte le round et la phase où elle est née,
// c'est tout ce qu'il faut pour les retrouver.
//
// Il suit LA CARTE DE RÉFÉRENCE du jeu plutôt que ses propres catégories : une
// étape par point de la carte, dans l'ordre où le méchant les joue. C'est ce qui
// rend explicite « quelle carte appartient à quelle étape » — et ça ne coûte
// rien, puisque le moteur découpe déjà sa phase de la même façon et que chaque
// entrée sait de quel découpage elle vient.

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { CarteApercu } from './Board'
import { toScanCard, type ContexteCarte } from './card-model'
import type { Catalogue } from './catalogue'
import type { EntreeHistorique } from './HistoriquePartie'
import { t } from './langue'
import type { ScanCardProps } from '../components/ScanCard'
import type { World, WorldCard } from './world'

/**
 * Les étapes de la phase du méchant, dans l'ordre de la carte de référence.
 *
 * Les clés sont les états que le moteur nomme lui-même (voir game/world/phase.py,
 * Phase.State) : il n'a pas d'état unique pour « phase du méchant », il la
 * découpe exactement comme la carte. On ne re-catégorise donc rien, on affiche
 * son découpage.
 *
 * Le point 5 de la carte (« passer le jeton de premier joueur ») ne produit
 * aucun fait à raconter : il n'a pas d'étape ici.
 */
const ETAPES = [
  { phase: 'Main Scheme Place Threat', numero: 1, titre: 'Menace sur la manigance' },
  { phase: 'Enemy Activation', numero: 2, titre: 'Activations' },
  { phase: 'Deal Encounter Cards', numero: 3, titre: 'Cartes distribuées' },
  { phase: 'Reveal Encounter Cards', numero: 4, titre: 'Cartes révélées' },
] as const

const PHASES_MECHANT = new Set<string>(ETAPES.map((e) => e.phase))

type Etape = {
  numero: number
  titre: string
  entrees: EntreeHistorique[]
  /** Menace posée sur l'étape, retraits déduits. 0 = rien à annoncer. */
  menace: number
  /** Dégâts encaissés sur l'étape, en positif. */
  degats: number
  /** Cartes entrées en jeu sur l'étape. */
  cartes: number
}

type Bilan = { cle: string; round: number; etapes: Etape[] }

/** Les faits d'une étape, et ce qu'ils totalisent. */
function etapeDe(
  entrees: EntreeHistorique[],
  definition: (typeof ETAPES)[number]
): Etape | undefined {
  const dedans = entrees.filter((e) => e.phase === definition.phase && e.type !== 'phase')
  if (dedans.length === 0) return undefined

  let menace = 0
  let degats = 0
  let cartes = 0
  for (const e of dedans) {
    // `valeur` est la variation signée du compteur (voir HistoriquePartie) :
    // une menace retirée se soustrait d'elle-même, sans test de sens ici.
    if (e.type === 'threat') menace += e.valeur ?? 0
    if (e.type === 'damage') degats += Math.abs(e.valeur ?? 0)
    if (e.type === 'card') cartes += 1
  }
  return { numero: definition.numero, titre: definition.titre, entrees: dedans, menace, degats, cartes }
}

export function bilanDeLaPhase(entrees: EntreeHistorique[], round: number): Bilan | undefined {
  const dedans = entrees.filter((e) => e.round === round && PHASES_MECHANT.has(e.phase))
  // Ordre du jeu : l'historique empile les plus récentes en tête.
  const ordonnees = [...dedans].reverse()
  const etapes = ETAPES.map((definition) => etapeDe(ordonnees, definition)).filter(
    (e): e is Etape => e !== undefined
  )
  if (etapes.length === 0) return undefined
  return { cle: `${round}`, round, etapes }
}

/** « +3 → 4/12 », ou « +3 → 4 » quand la manigance n'affiche pas de seuil. */
function menaceLisible(entree: EntreeHistorique): string | undefined {
  const { valeur, restant, plafond } = entree
  if (valeur === undefined || restant === undefined) return undefined
  const signe = valeur > 0 ? `+${valeur}` : `${valeur}`
  return plafond ? `${signe} → ${restant}/${plafond}` : `${signe} → ${restant}`
}

/** Le héros de ce siège, pour dire QUI a reçu la carte. */
function nomDuHeros(monde: World | undefined, joueur: number | undefined): string | undefined {
  if (joueur === undefined) return undefined
  const heros = monde?.players?.[joueur]?.area_hero?.[0]?.name
  return heros ? heros.replace(/^\W*/, '') : `P${joueur + 1}`
}

export function RecapPhaseMechant({
  entrees,
  monde,
  actif,
  cartesMonde,
  catalogue,
  playerId,
}: {
  entrees: EntreeHistorique[]
  monde: World | undefined
  actif: boolean
  /** Les cartes du monde par object id, pour retrouver celle d'une ligne. */
  cartesMonde?: Map<number, WorldCard>
  catalogue?: Catalogue
  playerId?: number
}) {
  const [bilan, setBilan] = useState<Bilan | undefined>(undefined)
  const phasePrecedente = useRef<string | undefined>(undefined)

  useEffect(() => {
    const phase = monde?.phase
    const avant = phasePrecedente.current
    phasePrecedente.current = phase

    if (!actif || phase === undefined || avant === undefined) return
    // On ne déclenche qu'à la SORTIE de la phase du méchant.
    if (!PHASES_MECHANT.has(avant) || PHASES_MECHANT.has(phase)) return
    setBilan(bilanDeLaPhase(entrees, monde?.round_id ?? 0))
  }, [monde?.phase, monde?.round_id, actif, entrees])

  // La carte survolée, montrée dans le MÊME agrandissement que sur la table.
  //
  // Délai identique à celui du plateau (200 ms) : sans lui, l'aperçu clignote
  // dès qu'on traverse la liste pour atteindre « Continuer ».
  const [survolId, setSurvolId] = useState<number | undefined>(undefined)
  const minuteur = useRef<number | undefined>(undefined)

  const pointer = useCallback((cibleId: number | undefined) => {
    window.clearTimeout(minuteur.current)
    if (cibleId === undefined) {
      setSurvolId(undefined)
      return
    }
    minuteur.current = window.setTimeout(() => setSurvolId(cibleId), 200)
  }, [])

  // Au doigt, il n'y a pas de survol : l'appui ouvre l'aperçu, un second appui
  // (ou un appui ailleurs) le referme. Le délai n'a plus lieu d'être.
  const appuyer = useCallback((cibleId: number | undefined) => {
    window.clearTimeout(minuteur.current)
    setSurvolId((actuel) => (actuel === cibleId ? undefined : cibleId))
  }, [])

  useEffect(() => () => window.clearTimeout(minuteur.current), [])

  const contexte: ContexteCarte | undefined = useMemo(
    () =>
      catalogue
        ? { playerId: playerId ?? 0, actives: new Set(monde?.active_card_ids ?? []), catalogue }
        : undefined,
    [catalogue, playerId, monde?.active_card_ids]
  )

  const carteSurvolee: ScanCardProps | undefined = useMemo(() => {
    if (survolId === undefined || !contexte) return undefined
    const carte = cartesMonde?.get(survolId)
    // Une carte qui a quitté la table (une carte de boost part à la défausse
    // aussitôt résolue) n'est plus dans le monde : pas d'aperçu pour elle
    // plutôt qu'un aperçu qui mentirait sur son état.
    if (!carte) return undefined
    return toScanCard(carte, contexte)
  }, [survolId, cartesMonde, contexte])

  if (!bilan) return null

  const totaux = (etape: Etape) => {
    const morceaux: string[] = []
    if (etape.menace !== 0)
      morceaux.push(`${etape.menace > 0 ? '+' : ''}${etape.menace} ${t('menace')}`)
    if (etape.degats > 0) morceaux.push(`${etape.degats} ${t('dégâts')}`)
    if (etape.cartes > 0) morceaux.push(`${etape.cartes} ${t('carte(s)')}`)
    return morceaux.join(' · ')
  }

  const ligne = (entree: EntreeHistorique) => {
    const heros = entree.type === 'card' ? nomDuHeros(monde, entree.joueur) : undefined
    const chiffres = entree.type === 'threat' ? menaceLisible(entree) : undefined
    const survolable = entree.cibleId !== undefined
    return (
      <li
        key={entree.cle}
        className={survolable ? 'est-survolable' : undefined}
        onMouseEnter={survolable ? () => pointer(entree.cibleId) : undefined}
        onMouseLeave={survolable ? () => pointer(undefined) : undefined}
        onPointerUp={
          survolable
            ? (evenement) => {
                if (evenement.pointerType === 'mouse') return
                appuyer(entree.cibleId)
              }
            : undefined
        }
      >
        <span className="recap-mechant-fait">
          <b>{entree.titre}</b>
          {heros ? <em className="recap-mechant-heros">{heros}</em> : null}
        </span>
        {chiffres ? <strong className="recap-mechant-chiffre">{chiffres}</strong> : null}
        {entree.detail ? <small>{entree.detail}</small> : null}
      </li>
    )
  }

  return (
    <div
      className="recap-mechant"
      role="dialog"
      aria-label={t('Bilan de la phase du méchant')}
      onPointerUp={(evenement) => {
        // Un appui hors d'une ligne referme l'aperçu (tactile).
        if (evenement.pointerType === 'mouse') return
        if (!(evenement.target as HTMLElement).closest('.est-survolable')) setSurvolId(undefined)
      }}
    >
      <div className="recap-mechant-carte">
        <header>
          <span className="plateau-eyebrow">{t('Phase du méchant')}</span>
          <strong>
            {t('Round')} {bilan.round}
          </strong>
        </header>

        {bilan.etapes.map((etape) => (
          <section className="recap-mechant-groupe" key={etape.numero}>
            <span className="plateau-eyebrow">
              <i>{etape.numero}</i>
              {t(etape.titre)}
              {totaux(etape) ? <b className="recap-mechant-total">{totaux(etape)}</b> : null}
            </span>
            <ul>{etape.entrees.map(ligne)}</ul>
          </section>
        ))}

        <button
          type="button"
          className="recap-mechant-ok"
          onClick={() => {
            setSurvolId(undefined)
            setBilan(undefined)
          }}
          autoFocus
        >
          {t('Continuer')}
        </button>
      </div>

      {carteSurvolee ? <CarteApercu carte={carteSurvolee} classe="au-dessus-du-bilan" /> : null}
    </div>
  )
}
