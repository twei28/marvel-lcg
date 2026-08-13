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
// DEUX RÈGLES DE LECTURE, apprises en le voyant tourner :
//
// 1. Il suit LA CARTE DE RÉFÉRENCE du jeu, une étape par point de la carte. Le
//    moteur découpe déjà sa phase de la même façon et chaque entrée sait de quel
//    découpage elle vient : on affiche son découpage, on ne re-catégorise rien.
//
// 2. Il RÉSUME au lieu de dérouler. Poser une menace coûte six lignes au moteur
//    (début de phase, intention, pose du jeton, gain, fin de phase) dont une
//    seule dit quelque chose à un joueur. Le déroulé complet reste accessible
//    sous le repli de chaque étape — mais il ne s'impose plus.

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
 * découpe exactement comme la carte.
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

/**
 * Les seuls types qui racontent un FAIT de jeu.
 *
 * Tout le reste (`text`) est la narration interne du moteur — « Main scheme
 * phase start », « Underground Distribution would place 1 », « moved to
 * BoostCardsDeck<1> ». Elle a sa place dans le journal, où l'on vient chercher
 * le détail ; elle n'en a pas dans un bilan qu'on lit en trois secondes.
 */
const TYPES_FAITS = new Set(['damage', 'heal', 'threat', 'card'])

type Boost = { cle: string; nom: string; cibleId?: number }

/** Une ligne du bilan : un fait, déjà mis en phrase. */
type Ligne = {
  cle: string
  /** Colore et choisit le verbe. */
  genre: 'menace' | 'attaque' | 'manigance' | 'carte'
  titre: string
  /** Le chiffre du fait, à droite : « +1 → 1/6 », « 3 dégâts → 8 PV ». */
  chiffre?: string
  /** Cartes de boost retournées pour cette activation. */
  boosts?: Boost[]
  /** Héros qui a reçu la carte. */
  heros?: string
  /** Ce que la carte a produit ensuite, dans ses propres mots. */
  effets?: string[]
  cibleId?: number
}

type Etape = {
  numero: number
  titre: string
  lignes: Ligne[]
  /** Le déroulé complet du moteur, pour le repli. */
  brut: EntreeHistorique[]
  /** Menace posée sur l'étape, retraits déduits. */
  menace: number
  /** Dégâts encaissés sur l'étape, en positif. */
  degats: number
  /** Cartes entrées en jeu sur l'étape, boosts non compris. */
  cartes: number
}

type Bilan = { cle: string; round: number; etapes: Etape[] }

/** De quoi nommer une carte et un héros sans que le bilan lise le monde. */
export type Noms = {
  carte: (id: number | undefined) => string | undefined
  heros: (joueur: number | undefined) => string | undefined
}

/** « +1 → 1/6 », ou « +1 → 4 » quand la manigance n'affiche pas de seuil. */
function chiffreMenace(entree: EntreeHistorique): string | undefined {
  const { valeur, restant, plafond } = entree
  if (valeur === undefined) return undefined
  const signe = valeur > 0 ? `+${valeur}` : `${valeur}`
  if (restant === undefined) return signe
  return plafond ? `${signe} → ${restant}/${plafond}` : `${signe} → ${restant}`
}

/** « 3 dégâts → 8 PV ». */
function chiffreDegats(entree: EntreeHistorique): string {
  const subis = Math.abs(entree.valeur ?? 0)
  const texte = `${subis} ${t('dégâts')}`
  return entree.restant === undefined ? texte : `${texte} → ${entree.restant} ${t('PV')}`
}

/**
 * Les lignes d'une étape, résumées.
 *
 * Le rattachement des boosts suit L'ORDRE DU MOTEUR, qui retourne les cartes de
 * boost AVANT de résoudre l'attaque qu'elles gonflent : on accumule les boosts
 * rencontrés et on les verse sur le premier fait qui suit. C'est ce que montre
 * le déroulé réel (« Sonic Boom revealed », « T'Challa's Shadow revealed »,
 * « Black Panther is being attacked by Klaw »), et ça n'invente aucun lien que
 * la chronologie ne porte pas déjà.
 *
 * Même principe pour les cartes de rencontre, dans l'autre sens : ce qu'une
 * carte révélée a produit la SUIT, jusqu'à la révélation suivante.
 */
function lignesDeLEtape(faits: EntreeHistorique[], noms: Noms): Ligne[] {
  const lignes: Ligne[] = []
  let boostsEnAttente: Boost[] = []
  /** Dernière carte révélée, à qui rattacher ce qui arrive ensuite. */
  let derniereCarte: Ligne | undefined

  const verser = () => {
    const boosts = boostsEnAttente
    boostsEnAttente = []
    return boosts.length > 0 ? boosts : undefined
  }

  for (const fait of faits) {
    if (fait.type === 'card') {
      if (fait.boost) {
        boostsEnAttente.push({
          cle: fait.cle,
          nom: fait.nomCarte ?? fait.titre,
          cibleId: fait.cibleId,
        })
        continue
      }
      derniereCarte = {
        cle: fait.cle,
        genre: 'carte',
        titre: fait.nomCarte ?? fait.titre,
        heros: noms.heros(fait.joueur),
        cibleId: fait.cibleId,
      }
      lignes.push(derniereCarte)
      continue
    }

    if (fait.type === 'damage' || fait.type === 'heal') {
      const cible = noms.carte(fait.cibleId)
      const chiffre = chiffreDegats(fait)
      // Une carte révélée en cours d'étape s'attribue ses conséquences ; hors
      // de ce cas, les dégâts sont ceux d'une activation ennemie.
      if (derniereCarte) {
        derniereCarte.effets = [...(derniereCarte.effets ?? []), `${cible ?? fait.titre} : ${chiffre}`]
        continue
      }
      lignes.push({
        cle: fait.cle,
        genre: 'attaque',
        // Sans auteur connu, on garde la phrase du moteur plutôt que d'inventer
        // un attaquant : « untel subit 3 dégâts » reste vrai.
        titre: fait.acteur && cible ? `${fait.acteur} ${t('attaque')} ${cible}` : fait.titre,
        chiffre,
        boosts: verser(),
        cibleId: fait.cibleId,
      })
      continue
    }

    if (fait.type === 'threat') {
      const cible = noms.carte(fait.cibleId)
      const chiffre = chiffreMenace(fait)
      if (derniereCarte) {
        derniereCarte.effets = [
          ...(derniereCarte.effets ?? []),
          `${cible ?? fait.titre}${chiffre ? ` : ${chiffre}` : ''}`,
        ]
        continue
      }
      // Une menace posée PENDANT une activation est une manigance d'ennemi ;
      // la même à l'étape 1 est la menace de phase, qui n'a pas d'auteur.
      const manigance = fait.acteur !== undefined
      lignes.push({
        cle: fait.cle,
        genre: manigance ? 'manigance' : 'menace',
        titre:
          manigance && cible
            ? `${fait.acteur} ${t('manigance sur')} ${cible}`
            : (cible ?? fait.titre),
        chiffre,
        boosts: verser(),
        cibleId: fait.cibleId,
      })
    }
  }

  return lignes
}

function etapeDe(
  entrees: EntreeHistorique[],
  definition: (typeof ETAPES)[number],
  noms: Noms
): Etape | undefined {
  const brut = entrees.filter((e) => e.phase === definition.phase && e.type !== 'phase')
  if (brut.length === 0) return undefined

  const faits = brut.filter((e) => TYPES_FAITS.has(e.type))

  let menace = 0
  let degats = 0
  let cartes = 0
  for (const e of faits) {
    // `valeur` est la variation signée du compteur (voir HistoriquePartie) :
    // une menace retirée se soustrait d'elle-même, sans test de sens ici.
    if (e.type === 'threat') menace += e.valeur ?? 0
    if (e.type === 'damage') degats += Math.abs(e.valeur ?? 0)
    // Une carte de boost n'est pas une carte de plus : elle appartient à
    // l'activation, et le total la compterait deux fois.
    if (e.type === 'card' && !e.boost) cartes += 1
  }

  const lignes = lignesDeLEtape(faits, noms)
  // Une étape qui n'a produit QUE de la narration n'a rien à montrer, mais son
  // déroulé reste consultable : on la garde, repliée.
  return { numero: definition.numero, titre: definition.titre, lignes, brut, menace, degats, cartes }
}

export function bilanDeLaPhase(
  entrees: EntreeHistorique[],
  round: number,
  noms: Noms = { carte: () => undefined, heros: () => undefined }
): Bilan | undefined {
  const dedans = entrees.filter((e) => e.round === round && PHASES_MECHANT.has(e.phase))
  // Ordre du jeu : l'historique empile les plus récentes en tête.
  const ordonnees = [...dedans].reverse()
  const etapes = ETAPES.map((definition) => etapeDe(ordonnees, definition, noms)).filter(
    (e): e is Etape => e !== undefined
  )
  if (etapes.length === 0) return undefined
  return { cle: `${round}`, round, etapes }
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
  const [depliees, setDepliees] = useState<Set<number>>(() => new Set())
  const phasePrecedente = useRef<string | undefined>(undefined)

  // Les noms sont lus au moment du bilan, sur le monde tel qu'il est alors. Une
  // carte partie (toute carte de boost l'est) n'y répond plus : les entrées
  // portent donc leur propre `nomCarte`, qui, lui, ne s'efface pas.
  const noms: Noms = useMemo(
    () => ({
      carte: (id) => (id === undefined ? undefined : cartesMonde?.get(id)?.name),
      heros: (joueur) => {
        if (joueur === undefined) return undefined
        const heros = monde?.players?.[joueur]?.area_hero?.[0]?.name
        return heros ? heros.replace(/^\W*/, '') : `P${joueur + 1}`
      },
    }),
    [cartesMonde, monde]
  )
  const nomsRef = useRef(noms)
  nomsRef.current = noms

  useEffect(() => {
    const phase = monde?.phase
    const avant = phasePrecedente.current
    phasePrecedente.current = phase

    if (!actif || phase === undefined || avant === undefined) return
    // On ne déclenche qu'à la SORTIE de la phase du méchant.
    if (!PHASES_MECHANT.has(avant) || PHASES_MECHANT.has(phase)) return
    setDepliees(new Set())
    setBilan(bilanDeLaPhase(entrees, monde?.round_id ?? 0, nomsRef.current))
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

  const survolProps = (cibleId: number | undefined) =>
    cibleId === undefined
      ? {}
      : {
          className: 'est-survolable',
          onMouseEnter: () => pointer(cibleId),
          onMouseLeave: () => pointer(undefined),
          onPointerUp: (evenement: React.PointerEvent) => {
            if (evenement.pointerType === 'mouse') return
            appuyer(cibleId)
          },
        }

  const ligne = (ligne: Ligne) => (
    <li key={ligne.cle} className={`recap-ligne est-${ligne.genre}`}>
      <span className="recap-mechant-fait" {...survolProps(ligne.cibleId)}>
        <b>{ligne.titre}</b>
        {ligne.heros ? <em className="recap-mechant-heros">{ligne.heros}</em> : null}
      </span>
      {ligne.chiffre ? <strong className="recap-mechant-chiffre">{ligne.chiffre}</strong> : null}
      {ligne.boosts ? (
        <span className="recap-mechant-boosts">
          {t('boost')} :{' '}
          {ligne.boosts.map((boost, index) => (
            <span key={boost.cle}>
              {index > 0 ? ', ' : ''}
              <span {...survolProps(boost.cibleId)}>{boost.nom}</span>
            </span>
          ))}
        </span>
      ) : null}
      {ligne.effets?.map((effet) => (
        <small key={effet}>{effet}</small>
      ))}
    </li>
  )

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

        {bilan.etapes.map((etape) => {
          const depliee = depliees.has(etape.numero)
          return (
            <section className="recap-mechant-groupe" key={etape.numero}>
              <span className="plateau-eyebrow">
                <i>{etape.numero}</i>
                {t(etape.titre)}
                {totaux(etape) ? <b className="recap-mechant-total">{totaux(etape)}</b> : null}
                <button
                  type="button"
                  className="recap-mechant-repli"
                  aria-expanded={depliee}
                  title={t('Voir le déroulé complet du moteur')}
                  onClick={() =>
                    setDepliees((avant) => {
                      const apres = new Set(avant)
                      if (!apres.delete(etape.numero)) apres.add(etape.numero)
                      return apres
                    })
                  }
                >
                  {depliee ? '▾' : '▸'}
                </button>
              </span>

              {etape.lignes.length > 0 ? <ul>{etape.lignes.map(ligne)}</ul> : null}

              {depliee ? (
                <ul className="recap-mechant-deroule">
                  {etape.brut.map((entree) => (
                    <li key={entree.cle}>{entree.titre}</li>
                  ))}
                </ul>
              ) : null}
            </section>
          )
        })}

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
