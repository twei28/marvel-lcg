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
import { BoutonsRapportBug, type OutilsRapport } from './RapportBug'
import type { World, WorldCard } from './world'

type TypeHistorique = 'phase' | 'text' | 'card' | 'damage' | 'heal' | 'threat' | 'triche'

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
  /**
   * Le texte du moteur AVANT sansIdentifiants(), quand l'entrée vient d'une
   * narration. C'est la seule trace des identifiants « [(50,01113) Klaw] »,
   * que texteSignificatif() efface à la création : l'affichage lit `titre`,
   * le rapport de bug lit `brut`. Absent sur les autres types d'entrée, qui
   * portent déjà leur object id dans `cibleId`.
   */
  brut?: string
  /**
   * Les mêmes nombres que le titre, mais en nombres.
   *
   * Le titre est une PHRASE (« Klaw subit 3 dégât(s) »), traduite, où le chiffre
   * est noyé. Tout lecteur qui veut additionner — le bilan de la phase du
   * méchant et ses totaux par étape — devrait le ré-extraire à coups
   * d'expression régulière, dans deux langues. On le publie donc ici, à
   * l'endroit où on le connaît déjà.
   *
   * `valeur` est la VARIATION SIGNÉE du compteur, une seule règle pour tous les
   * types : -3 quand les PV tombent de 8 à 5, +2 quand la menace monte, -1
   * quand on en retire. Un lecteur additionne sans se demander de quel côté
   * penche la ligne, et affiche `Math.abs` quand le titre dit déjà le sens.
   *
   * L'ampleur seule ne suffisait pas : « menace » est le seul type qui serve
   * les deux sens, un total en valeur absolue y compterait un retrait comme
   * une pose.
   */
  valeur?: number
  /** Ce qu'il reste après coup : PV restants, ou menace sur la manigance. */
  restant?: number
  /** Le seuil, quand la cible en a un : la menace maximale d'une manigance. */
  plafond?: number
}

/**
 * Ce qu'on sait d'une entrée en plus de son texte : de quoi la filtrer ensuite
 * (cible, joueur, auteur) et de quoi l'additionner (les nombres du titre).
 */
type Rattachement = Pick<
  EntreeHistorique,
  'cibleId' | 'joueur' | 'acteur' | 'valeur' | 'restant' | 'plafond'
>

type CarteObservee = {
  id: number
  nom: string
  type: string
  zone: 'hand' | 'player-play' | 'player-discard' | 'encounter-deck' | 'encounter-play' | 'encounter-discard' | 'other'
  joueur?: number
  vie?: number
  menace?: number
  /** Seuil de la manigance (`target_threat`), quand elle en affiche un. */
  menaceCible?: number
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
export const MAX_ENTREES = 400
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
    // Même source que le badge « 4/12 » des complots sur la table
    // (card-model : menaceAffichee). Une manigance sans seuil vaut 0 : on ne
    // retient alors rien, pour ne pas annoncer « 3/0 ».
    menaceCible: SCHEME_TYPES.has(carte.card_type)
      ? nombreInfo(carte, 'target_threat') || undefined
      : undefined,
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
      const nombres = { valeur: ecart, restant: courante.vie }
      sorties.push(
        ecart < 0
          ? entree(
              apres,
              'damage',
              `${courante.nom} ${t('subit')} ${Math.abs(ecart)} ${t('dégât(s)')}`,
              detailAvecCause(`${courante.vie} ${t('PV restants')}`, cause),
              `${id}:hp:${courante.vie}`,
              { ...rattachement, ...nombres, acteur: cause?.source }
            )
          : entree(apres, 'heal', `${courante.nom} ${t('soigne')} ${ecart}`, `${courante.vie} ${t('PV')}`, `${id}:hp:${courante.vie}`, { ...rattachement, ...nombres })
      )
    }

    if (
      precedente.menace !== undefined &&
      courante.menace !== undefined &&
      precedente.menace !== courante.menace
    ) {
      const ecart = courante.menace - precedente.menace
      const cause = lireCause(causes, 'menace', courante.nom, apres.render_id)
      const attache = {
        ...rattachement,
        acteur: cause?.source,
        valeur: ecart,
        restant: courante.menace,
        plafond: courante.menaceCible,
      }
      sorties.push(
        ecart < 0
          ? entree(apres, 'threat', `${Math.abs(ecart)} ${t('menace retirée de')} ${courante.nom}`, detailAvecCause(`${courante.menace} ${t('menace restante')}`, cause), `${id}:threat:${courante.menace}`, attache)
          : entree(apres, 'threat', `${courante.nom} ${t('gagne')} ${ecart} ${t('menace')}`, detailAvecCause(`${courante.menace} ${t('menace')}`, cause), `${id}:threat:${courante.menace}`, attache)
      )
    }
  }

  return sorties
}

type Narration = { texte: string; brut: string }

function narrationsDuRendu(monde: World, demande: Demande | undefined): Narration[] {
  const sources = [monde.prompt, monde.prompt_last_text, demande?.prompt_text]
  const sorties: Narration[] = []
  const vus = new Set<string>()
  for (const source of sources) {
    const texte = texteSignificatif(source)
    if (texte === undefined || vus.has(texte)) continue
    vus.add(texte)
    sorties.push({ texte, brut: (source ?? '').trim() })
  }
  return sorties
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
//
// Il porte donc le `game_id` DE LA PARTIE qui l'a produit. Sans cette
// etiquette, l'onglet gardait le journal d'une partie finie et le deroulait
// au-dessus de la suivante : signale en jeu, « l'historique garde tout ».
// La cause exacte est plus bas, dans l'effet de remise a zero — au premier
// montage il adoptait la partie en cours SANS rien verifier, precisement pour
// qu'un F5 ne jette pas le journal restaure. Il faut les deux : garder sur F5,
// jeter sur nouvelle partie. C'est ce que l'etiquette permet de distinguer.
const CLE_HISTORIQUE = 'marvel-historique-partie'

type HistoriquePersiste = { partieId?: number; entrees: EntreeHistorique[] }

function lireHistoriquePersiste(): HistoriquePersiste {
  try {
    const brut = window.sessionStorage.getItem(CLE_HISTORIQUE)
    if (!brut) return { entrees: [] }
    const donnees = JSON.parse(brut) as unknown
    // Ancien format : un simple tableau, sans etiquette de partie. On le relit
    // pour ne pas perdre le journal d'une partie en cours au moment de la mise
    // a jour, mais sans partieId il sera jete des que le moteur en annoncera
    // une — on ne peut pas savoir a quelle partie il appartenait.
    if (Array.isArray(donnees)) {
      return { entrees: (donnees as EntreeHistorique[]).slice(0, MAX_ENTREES) }
    }
    const objet = donnees as Partial<HistoriquePersiste>
    return {
      partieId: typeof objet?.partieId === 'number' ? objet.partieId : undefined,
      entrees: Array.isArray(objet?.entrees) ? objet.entrees.slice(0, MAX_ENTREES) : [],
    }
  } catch {
    return { entrees: [] }
  }
}

function persisterHistorique(entrees: EntreeHistorique[], partieId?: number): void {
  try {
    const charge: HistoriquePersiste = { partieId, entrees }
    window.sessionStorage.setItem(CLE_HISTORIQUE, JSON.stringify(charge))
  } catch {
    /* stockage plein ou indisponible : l'historique reste en memoire */
  }
}

export function useHistoriquePartie(
  monde: World | undefined,
  demande: Demande | undefined,
  partieId?: number
) {
  // Lu UNE fois : la partie a laquelle appartient le journal restaure.
  const restaure = useRef(lireHistoriquePersiste())
  const [entrees, setEntrees] = useState<EntreeHistorique[]>(() => restaure.current.entrees)
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

    if (premiere) {
      // Au premier montage on ne peut pas effacer aveuglément : un simple F5
      // jetterait le journal restauré de la partie EN COURS. On compare donc
      // son étiquette. Égales -> c'est bien la même partie, on la reprend.
      // Différentes, ou absente (ancien format) -> le journal vient d'une
      // partie finie, il n'a rien à faire au-dessus de celle-ci.
      if (restaure.current.partieId === partieId) {
        persisterHistorique(restaure.current.entrees, partieId)
        return
      }
      setEntrees([])
      persisterHistorique([], partieId)
      return
    }

    // Nouvelle partie sans rechargement de page : on repart de zéro.
    setEntrees([])
    persisterHistorique([], partieId)
  }, [partieId])

  useEffect(() => {
    if (!monde) return

    // Les causes sont relevees AVANT le diff : une attaque se narre au rendu
    // precedent (« would deal 2 damage to X »), le total de PV ne bouge qu'ici.
    const narrations = narrationsDuRendu(monde, demande)
    for (const { texte } of narrations) noterCause(causes.current, texte, monde.render_id)

    const nouvelles = [
      ...(precedent.current
        ? analyserDelta(precedent.current, monde, causes.current)
        : [entree(monde, 'phase', `Round ${monde.round_id}`, monde.phase, 'initial')]),
      ...narrations.map(({ texte, brut }) => ({
        ...entree(monde, 'text', texte, undefined, `text:${texte}`),
        brut,
      })),
    ]
    setEntrees((courantes) => {
      const suivantes = ajouterNouvellesEntrees(courantes, nouvelles)
      persisterHistorique(suivantes, partieNotee.current)
      return suivantes
    })
    precedent.current = monde
  }, [monde, monde?.render_id, demande?.event_name, demande?.prompt_text, demande?.ability_type])

  const effacer = useCallback(() => {
    setEntrees([])
    persisterHistorique([], partieNotee.current)
  }, [])
  /**
   * Inscrit une intervention du mode Bac à sable dans le journal.
   *
   * Elle se mêle aux événements du jeu, dans l'ordre où tout s'est produit,
   * mais garde son type propre : en relisant une situation étrange, on
   * distingue immédiatement ce qui vient d'une carte de ce qui vient du joueur.
   * C'est exactement ce qui manquait pour diagnostiquer Kamala's Room.
   *
   * La clé porte un compteur : deux soins identiques au même rendu sont deux
   * faits distincts, et sans lui React n'en afficherait qu'un.
   */
  const compteurTriche = useRef(0)
  const ajouterTriche = useCallback(
    (libelle: string) => {
      compteurTriche.current += 1
      const monde = precedent.current
      const entree: EntreeHistorique = {
        cle: `triche:${compteurTriche.current}`,
        type: 'triche',
        renderId: monde?.render_id ?? 0,
        round: monde?.round_id ?? 0,
        phase: monde?.phase ?? '',
        titre: libelle,
      }
      setEntrees((liste) => {
        const suite = [...liste, entree].slice(-MAX_ENTREES)
        persisterHistorique(suite, partieNotee.current)
        return suite
      })
    },
    []
  )

  return { entrees, effacer, ajouterTriche }
}

function libelleType(type: TypeHistorique): string {
  if (type === 'card') return t('Carte')
  if (type === 'damage') return t('Dégâts')
  if (type === 'heal') return t('Soin')
  if (type === 'threat') return t('Menace')
  if (type === 'triche') return t('Triche')
  if (type === 'phase') return 'Phase'
  return t('Événement')
}

export function HistoriquePartie({
  entrees,
  effacer,
  rapport,
}: {
  entrees: EntreeHistorique[]
  effacer: () => void
  /** Absent hors partie : le panneau se contente alors du bouton « Effacer ». */
  rapport?: OutilsRapport
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
            <div className="hp-entete-actions">
              {rapport ? <BoutonsRapportBug outils={rapport} /> : null}
              <button type="button" onClick={effacer} disabled={entrees.length === 0}>
                {t('Effacer')}
              </button>
            </div>
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
