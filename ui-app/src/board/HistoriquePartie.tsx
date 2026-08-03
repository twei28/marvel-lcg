import { useCallback, useEffect, useRef, useState } from 'react'
import type { Demande } from './ask'
import { remplacerSymboles, sansIdentifiants } from './BarreAction'
import {
  creerMemoireCauses,
  detailAvecCause,
  lireCause,
  noterCause,
  type MemoireCauses,
} from './causalite'
import { t } from './langue'
import type { World, WorldCard } from './world'

type TypeHistorique = 'phase' | 'text' | 'card' | 'damage' | 'heal' | 'threat'

export type EntreeHistorique = {
  cle: string
  type: TypeHistorique
  renderId: number
  round: number
  phase: string
  titre: string
  detail?: string
  /** Carte concernée. Sert au journal par héros à savoir de qui on parle. */
  cibleId?: number
  /** Joueur dans les zones duquel la carte se trouve, s'il y en a un. */
  joueur?: number
  /** Auteur du fait, tiré de la causalité (le « par X » du détail). */
  acteur?: string
}

/** Ce qu'on sait d'une entrée en plus de son texte, pour la filtrer ensuite. */
type Rattachement = Pick<EntreeHistorique, 'cibleId' | 'joueur' | 'acteur'>

type CarteObservee = {
  id: number
  nom: string
  type: string
  zone: 'hand' | 'player-play' | 'player-discard' | 'encounter-deck' | 'encounter-play' | 'encounter-discard' | 'other'
  joueur?: number
  vie?: number
  menace?: number
}

/**
 * Profondeur du journal, TOUS TYPES CONFONDUS.
 *
 * Le plafond était de 80, ce qui suffisait au panneau « H » : on y lit surtout
 * les dernières lignes. Mais le journal par héros puise dans le MÊME tampon en
 * n'en retenant qu'une petite part (ni les lignes de narration brute, ni ce qui
 * concerne les autres joueurs). Le moteur émettant une entrée de narration à
 * chaque rendu, 80 entrées couvraient à peine une poignée de tours : la colonne
 * du héros se retrouvait avec trois lignes et rien au-dessus à remonter.
 *
 * 400 entrées représentent quelques dizaines de kilo-octets en sessionStorage,
 * ce qui est sans conséquence, et couvrent une partie entière.
 */
const MAX_ENTREES = 400
const UNIT_TYPES = new Set(['Ally', 'Minion', 'EncounterVillain', 'Hero', 'AlterEgo'])
const SCHEME_TYPES = new Set(['MainScheme', 'EncounterSideScheme', 'PlayerSideScheme'])

function nombreInfo(carte: WorldCard, cle: string): number | undefined {
  const valeur = carte.info[cle]
  return typeof valeur === 'number' ? valeur : undefined
}

function nettoyerTexte(texte: string | undefined): string {
  return remplacerSymboles(sansIdentifiants(texte ?? ''))
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/^---\s*/, '')
    .replace(/\s*---$/, '')
}

function texteSignificatif(texte: string | undefined): string | undefined {
  const propre = nettoyerTexte(texte)
  if (!propre) return undefined
  // Bilingue : narration moteur en anglais, ou en francais via translate_fr.json.
  if (/ on event "WhenPlayerInTurn"$| sur l(?:'|’)[eé]v[eé]nement "WhenPlayerInTurn"$/.test(propre)) return undefined
  if (/^[^-]+ Turn(?: \(\d+\))?$|^Tour de [^-]+(?: \(\d+\))?$/.test(propre)) return undefined
  return propre
}

function entree(
  monde: World,
  type: TypeHistorique,
  titre: string,
  detail?: string,
  cleDetail = detail ?? '',
  rattachement: Rattachement = {}
): EntreeHistorique {
  return {
    cle: `${monde.render_id}:${type}:${titre}:${cleDetail}`,
    type,
    renderId: monde.render_id,
    round: monde.round_id,
    phase: monde.phase,
    titre,
    detail,
    ...rattachement,
  }
}

function observerCarte(
  carte: WorldCard,
  zone: CarteObservee['zone'],
  joueur?: number
): CarteObservee {
  return {
    id: carte.id,
    nom: carte.name,
    type: carte.card_type,
    zone,
    joueur,
    vie: UNIT_TYPES.has(carte.card_type) ? nombreInfo(carte, 'health') : undefined,
    menace: SCHEME_TYPES.has(carte.card_type) ? nombreInfo(carte, 'k_threat') : undefined,
  }
}

function ajouterCartes(
  index: Map<number, CarteObservee>,
  cartes: readonly WorldCard[] | undefined,
  zone: CarteObservee['zone'],
  joueur?: number
) {
  if (!Array.isArray(cartes)) return
  for (const carte of cartes) index.set(carte.id, observerCarte(carte, zone, joueur))
}

function indexerMonde(monde: World): Map<number, CarteObservee> {
  const index = new Map<number, CarteObservee>()

  ajouterCartes(index, monde.area_schemes_main, 'encounter-play')
  ajouterCartes(index, monde.area_schemes_side, 'encounter-play')
  ajouterCartes(index, monde.area_villain, 'encounter-play')
  ajouterCartes(index, monde.area_environment, 'encounter-play')
  ajouterCartes(index, monde.area_revealing, 'encounter-play')
  ajouterCartes(index, monde.area_processing, 'encounter-play')
  ajouterCartes(index, monde.area_boost, 'encounter-play')
  ajouterCartes(index, monde.area_removed, 'other')
  ajouterCartes(index, monde.victory_display, 'other')
  ajouterCartes(index, monde.encounter_deck, 'encounter-deck')
  ajouterCartes(index, monde.encounter_discard_pile, 'encounter-discard')

  for (const [joueur, zone] of (monde.players ?? []).entries()) {
    ajouterCartes(index, zone.hand_cards, 'hand', joueur)
    ajouterCartes(index, zone.player_deck, 'other', joueur)
    ajouterCartes(index, zone.player_discard_pile, 'player-discard', joueur)
    ajouterCartes(index, zone.area_hero, 'player-play', joueur)
    ajouterCartes(index, zone.allies, 'player-play', joueur)
    ajouterCartes(index, zone.supports, 'player-play', joueur)
    ajouterCartes(index, zone.engaged_enemies, 'encounter-play', joueur)
    ajouterCartes(index, zone.environment_area, 'player-play', joueur)
    ajouterCartes(index, zone.obligations_area, 'player-play', joueur)
    ajouterCartes(index, zone.additional_deck, 'other', joueur)
    ajouterCartes(index, zone.additional_discard_pile, 'player-discard', joueur)
    ajouterCartes(index, zone.dealt_encounter_cards, 'encounter-play', joueur)
  }

  return index
}

function entreeCarteJouee(monde: World, avant: CarteObservee, apres: CarteObservee): EntreeHistorique | undefined {
  if (avant.zone !== 'hand') return undefined
  const rattachement = { cibleId: apres.id, joueur: apres.joueur }
  if (apres.zone === 'player-play') {
    return entree(monde, 'card', `${apres.nom} ${t('joué')}`, `P${(apres.joueur ?? 0) + 1}`, `${apres.id}:play`, rattachement)
  }
  if (apres.zone === 'player-discard') {
    const verbe = apres.type === 'Resource' ? t('payé') : apres.type === 'Event' ? t('joué') : t('défaussé')
    return entree(monde, 'card', `${apres.nom} ${verbe}`, `P${(apres.joueur ?? 0) + 1}`, `${apres.id}:discard`, rattachement)
  }
  return undefined
}

function analyserDelta(avant: World, apres: World, causes: MemoireCauses): EntreeHistorique[] {
  const precedentes = indexerMonde(avant)
  const courantes = indexerMonde(apres)
  const sorties: EntreeHistorique[] = []

  if (avant.round_id !== apres.round_id || avant.phase !== apres.phase) {
    sorties.push(entree(apres, 'phase', `Round ${apres.round_id}`, apres.phase, 'phase'))
  }

  for (const [id, courante] of courantes) {
    const precedente = precedentes.get(id)
    const rattachement = { cibleId: id, joueur: courante.joueur }
    if (!precedente) {
      if (courante.zone === 'encounter-play') {
        sorties.push(entree(apres, 'card', `${courante.nom} ${t('révélée')}`, undefined, `${id}:revealed`, rattachement))
      }
      continue
    }

    const jouee = entreeCarteJouee(apres, precedente, courante)
    if (jouee) sorties.push(jouee)

    if (precedente.zone === 'encounter-deck' && courante.zone !== 'encounter-deck') {
      sorties.push(entree(apres, 'card', `${courante.nom} ${t('révélée')}`, undefined, `${id}:revealed`, rattachement))
    }

    if (precedente.vie !== undefined && courante.vie !== undefined && precedente.vie !== courante.vie) {
      const ecart = courante.vie - precedente.vie
      // Les soins ne sont pas attribues : le moteur ne narre pas de gabarit
      // « soigne X via Y », et reutiliser la cause des degats designerait
      // l'attaquant precedent comme soigneur.
      const cause = lireCause(causes, 'degats', courante.nom, apres.render_id)
      sorties.push(
        ecart < 0
          ? entree(
              apres,
              'damage',
              `${courante.nom} ${t('subit')} ${Math.abs(ecart)} ${t('dégât(s)')}`,
              detailAvecCause(`${courante.vie} ${t('PV restants')}`, cause),
              `${id}:hp:${courante.vie}`,
              { ...rattachement, acteur: cause?.source }
            )
          : entree(apres, 'heal', `${courante.nom} ${t('soigne')} ${ecart}`, `${courante.vie} ${t('PV')}`, `${id}:hp:${courante.vie}`, rattachement)
      )
    }

    if (
      precedente.menace !== undefined &&
      courante.menace !== undefined &&
      precedente.menace !== courante.menace
    ) {
      const ecart = courante.menace - precedente.menace
      const cause = lireCause(causes, 'menace', courante.nom, apres.render_id)
      const attache = { ...rattachement, acteur: cause?.source }
      sorties.push(
        ecart < 0
          ? entree(apres, 'threat', `${Math.abs(ecart)} ${t('menace retirée de')} ${courante.nom}`, detailAvecCause(`${courante.menace} ${t('menace restante')}`, cause), `${id}:threat:${courante.menace}`, attache)
          : entree(apres, 'threat', `${courante.nom} ${t('gagne')} ${ecart} ${t('menace')}`, detailAvecCause(`${courante.menace} ${t('menace')}`, cause), `${id}:threat:${courante.menace}`, attache)
      )
    }
  }

  return sorties
}

function narrationsDuRendu(monde: World, demande: Demande | undefined): string[] {
  return [
    texteSignificatif(monde.prompt),
    texteSignificatif(monde.prompt_last_text),
    texteSignificatif(demande?.prompt_text),
  ].filter((texte, index, liste): texte is string => texte !== undefined && liste.indexOf(texte) === index)
}

function ajouterNouvellesEntrees(
  courantes: EntreeHistorique[],
  nouvelles: EntreeHistorique[]
): EntreeHistorique[] {
  if (nouvelles.length === 0) return courantes
  const vues = new Set(courantes.map((entree) => entree.cle))
  const aAjouter = nouvelles.filter((entree) => {
    if (vues.has(entree.cle)) return false
    vues.add(entree.cle)
    return true
  })
  return [...aAjouter.reverse(), ...courantes].slice(0, MAX_ENTREES)
}

// L'historique SURVIT aux rechargements de page (bascule de langue, F5,
// reconnexion) via sessionStorage : meme onglet = meme partie en pratique.
// Un nouveau round_id inferieur (nouvelle partie) remet le journal a zero.
const CLE_HISTORIQUE = 'marvel-historique-partie'

function lireHistoriquePersiste(): EntreeHistorique[] {
  try {
    const brut = window.sessionStorage.getItem(CLE_HISTORIQUE)
    if (!brut) return []
    const donnees = JSON.parse(brut) as EntreeHistorique[]
    return Array.isArray(donnees) ? donnees.slice(0, MAX_ENTREES) : []
  } catch {
    return []
  }
}

function persisterHistorique(entrees: EntreeHistorique[]): void {
  try {
    window.sessionStorage.setItem(CLE_HISTORIQUE, JSON.stringify(entrees))
  } catch {
    /* stockage plein ou indisponible : l'historique reste en memoire */
  }
}

export function useHistoriquePartie(
  monde: World | undefined,
  demande: Demande | undefined,
  partieId?: number
) {
  const [entrees, setEntrees] = useState<EntreeHistorique[]>(lireHistoriquePersiste)
  const precedent = useRef<World | undefined>(undefined)
  const causes = useRef<MemoireCauses>(creerMemoireCauses())
  const partieNotee = useRef<number | undefined>(undefined)

  // Remise à zéro sur NOUVELLE PARTIE seulement.
  //
  // Le critère était « le round est reparti en arrière ». C'était faux : le
  // bouton « Annuler la dernière action » fait reculer le monde, et un seul
  // undo effaçait tout le journal, plusieurs rounds compris. Le game_id du
  // moteur, lui, ne change qu'à une vraie nouvelle partie.
  useEffect(() => {
    if (partieId === undefined) return
    const premiere = partieNotee.current === undefined
    partieNotee.current = partieId
    // Au tout premier rendu on ADOPTE la partie en cours sans rien effacer :
    // sinon un simple F5 jetterait l'historique restauré depuis sessionStorage.
    if (premiere) return
    setEntrees([])
    persisterHistorique([])
  }, [partieId])

  useEffect(() => {
    if (!monde) return

    // Les causes sont relevees AVANT le diff : une attaque se narre au rendu
    // precedent (« would deal 2 damage to X »), le total de PV ne bouge qu'ici.
    const narrations = narrationsDuRendu(monde, demande)
    for (const texte of narrations) noterCause(causes.current, texte, monde.render_id)

    const nouvelles = [
      ...(precedent.current
        ? analyserDelta(precedent.current, monde, causes.current)
        : [entree(monde, 'phase', `Round ${monde.round_id}`, monde.phase, 'initial')]),
      ...narrations.map((texte) => entree(monde, 'text', texte, undefined, `text:${texte}`)),
    ]
    setEntrees((courantes) => {
      const suivantes = ajouterNouvellesEntrees(courantes, nouvelles)
      persisterHistorique(suivantes)
      return suivantes
    })
    precedent.current = monde
  }, [monde, monde?.render_id, demande?.event_name, demande?.prompt_text, demande?.ability_type])

  const effacer = useCallback(() => {
    setEntrees([])
    persisterHistorique([])
  }, [])
  return { entrees, effacer }
}

function libelleType(type: TypeHistorique): string {
  if (type === 'card') return t('Carte')
  if (type === 'damage') return t('Dégâts')
  if (type === 'heal') return t('Soin')
  if (type === 'threat') return t('Menace')
  if (type === 'phase') return 'Phase'
  return t('Événement')
}

export function HistoriquePartie({
  entrees,
  effacer,
}: {
  entrees: EntreeHistorique[]
  effacer: () => void
}) {
  const [ouvert, setOuvert] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!ouvert) return
    const fermer = (evenement: PointerEvent) => {
      const cible = evenement.target
      if (cible instanceof Node && ref.current?.contains(cible)) return
      setOuvert(false)
    }
    const fermerClavier = (evenement: KeyboardEvent) => {
      if (evenement.key === 'Escape') setOuvert(false)
    }
    document.addEventListener('pointerdown', fermer)
    document.addEventListener('keydown', fermerClavier)
    return () => {
      document.removeEventListener('pointerdown', fermer)
      document.removeEventListener('keydown', fermerClavier)
    }
  }, [ouvert])

  return (
    <div className="historique-partie" ref={ref}>
      <button
        type="button"
        className={`bh-bouton bh-history${ouvert ? ' est-ouvert' : ''}`}
        aria-expanded={ouvert}
        onClick={() => setOuvert((actuel) => !actuel)}
        title={t('Historique de la partie')}
      >
        <span aria-hidden="true">H</span> {t('Historique')} <em>{entrees.length}</em>
      </button>

      {ouvert ? (
        <section className="historique-panneau" role="dialog" aria-label="Game history">
          <header className="hp-entete">
            <div>
              <span className="plateau-eyebrow">Game history</span>
              <strong>{entrees[0]?.titre ?? t('Aucune entrée pour le moment')}</strong>
            </div>
            <button type="button" onClick={effacer} disabled={entrees.length === 0}>
              {t('Effacer')}
            </button>
          </header>

          {entrees.length === 0 ? (
            <p className="hp-vide">The log will fill as the board changes.</p>
          ) : (
            <ol className="hp-liste">
              {entrees.map((entree) => (
                <li className={`hp-entree type-${entree.type}`} key={entree.cle}>
                  <span className="hp-round">R{entree.round}</span>
                  <span className="hp-type">{libelleType(entree.type)}</span>
                  <span className="hp-texte">
                    <b>{entree.titre}</b>
                    {entree.detail ? <small>{entree.detail}</small> : null}
                  </span>
                </li>
              ))}
            </ol>
          )}
        </section>
      ) : null}
    </div>
  )
}
