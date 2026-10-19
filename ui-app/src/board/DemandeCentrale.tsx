import { QuestionSurTable, type ChoixSurTable } from './TableSansModale'
import { ligneDefense } from './ligne-attaque'
import { useEffect, useMemo, useRef, useState, type MouseEvent as ReactMouseEvent } from 'react'
import { ScanCard, type ScanCardProps } from '../components/ScanCard'
import { classeTonaliteAction } from './action-style'
import type { Demande, Option } from './ask'
import { CarteApercu } from './Board'
import { nettoyerNarration, nomLisible, sansIdentifiants } from './BarreAction'
import { t } from './langue'
import { avecIcones, marquerRessources } from './icones-ressources'
import { usePlacement } from './placement/usePlacement'
import { useGlisserPanneau, styleAvecDecalage } from './placement/useGlisserPanneau'
import { traduireMoteur, traduireTitreRepetition } from './vocabulaire-moteur'
import type { WorldCard } from './world'
import { nomAffiche } from './noms-cartes-fr'
import { NOMS_FR } from './noms-fr'
import { scansFrActifs } from './scans-fr'
import './boutons-bd.css'

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
   * Le SCAN a montrer en grand quand on SURVOLE le bouton (ou qu'on le
   * focalise au clavier), meme quand l'option ne nomme rien : la carte qui
   * la PORTE (« Spider-Sense » sur une interruption, « Backflip » sous
   * « Jouer »). Sans vignette : seule la carte nommee en a une. Repli :
   * carteDeLOption.
   */
  carteAuSurvol?: (option: Option) => ScanCardProps | undefined
  /** Le nom (francais si connu) de la carte qui porte l'option, comme dans la barre d'action. */
  nomPorteur?: (bindId: number) => string | undefined
  /**
   * Le TEXTE de la capacite que l'option declenche, a lire sous le bouton
   * (texte-capacite.ts). Pour une fenetre de reaction seulement : « I Object!
   * » ne dit rien a un nouveau joueur, le texte dit tout.
   */
  texteCapacite?: (option: Option) => string | undefined
  /** La carte qui porte l'option est-elle EN MAIN (« Ne pas jouer ») plutot qu'en jeu (« Ne pas utiliser ») ? */
  estEnMain?: (bindId: number) => boolean
  /**
   * Ce qui est connu de l'attaque (« ATQ 2 + 3 Charge + 1 carte boost »),
   * jamais un total : entre parentheses DANS « Ne pas défendre » (04/10/2026).
   */
  ligneSansDefense?: string
  /** Le meme detail, sans abreger : l'infobulle de « Ne pas défendre ». */
  survolSansDefense?: string
  /**
   * Loge dans la scene du deroule detaille (DeroulePhase, prop `question`)
   * plutot que pose au centre de la table : plus de placement, plus de
   * position fixe, le panneau coule dans la scene a la place de ses boutons.
   */
  enScene?: boolean
  /** « Sur la table » sans modale : pas de fenêtre, les cartes qui répondent portent leur étiquette. */
  surLaTable?: boolean
  /**
   * Remet la partie avant le choix de la carte (`/undo action`). La croix du
   * coin ne s'affiche que si la question en fait partie (`annuler_action`).
   */
  annulerAction?: () => void
}

/**
 * Les cartes que le moteur cite avec leur code, « [(48,01097b) The Break-In!] »,
 * remises dans la langue du plateau : « L'Effraction ! ». Le moteur ne connait
 * que l'anglais ; le plateau, lui, a le nom francais (noms-fr.ts). « Underground
 * Distribution s'apprête à recevoir 1⚠ » en pleine partie francaise, signale le
 * 12/09/2026.
 */
export function sansIdentifiantsEnFrancais(texte: string): string {
  if (!scansFrActifs()) return sansIdentifiants(texte)
  return texte.replace(/\[+\(\s*\d+\s*,\s*([0-9a-z_]+)\s*\)\s*([^[\]]+?)\]+/g, (_, code: string, nom: string) => NOMS_FR[code] ?? nom)
}

/** Le texte que le moteur a VRAIMENT envoyé, ou rien s'il n'a rien dit. */
function promptDemande(demande: Demande): string {
  const prompt = nettoyerNarration(sansIdentifiantsEnFrancais(demande.prompt_text))
  return prompt ? traduireTitreRepetition(prompt.replace(/^---\s*/, '').replace(/\s*---$/, '')) : ''
}

function texteDemande(demande: Demande): string {
  const prompt = promptDemande(demande)
  if (prompt) return prompt
  if (demande.ability_type) return traduireMoteur(demande.ability_type)
  return t('Choisis une réponse')
}

export function libelleTypeDemande(demande: Demande): string {
  // Le surtitre du panneau vient du moteur, donc de l'anglais : on le repasse
  // par le vocabulaire francais avant de l'afficher. « Normal » n'est pas un
  // mot de joueur, dans aucune langue : « NORMAL » s'affichait en anglais.
  if (demande.ability_type === 'Normal') return t('À toi de jouer')
  if (demande.ability_type) return traduireMoteur(demande.ability_type)
  const depuisEvenement = demande.event_name
    .replace(/^When/, '')
    .replace(/([a-z])([A-Z])/g, '$1 $2')
  return depuisEvenement ? traduireMoteur(depuisEvenement) : t('Décision')
}

function nomSource(
  option: Option,
  cartesParId: Map<number, WorldCard>,
  nomPorteur?: (bindId: number) => string | undefined
): string | undefined {
  if (option.bind_id === 0) return undefined
  // Le monde du moteur ne connait que l'anglais ; le plateau, lui, sait le
  // nom francais (fr.marvelcdb.com, en cache). « Backflip » sous « Jouer »
  // dans une partie en francais, signale le 11/09/2026.
  const porteur = cartesParId.get(option.bind_id)
  return nomPorteur?.(option.bind_id) || (porteur ? nomAffiche(porteur) : undefined)
}

/**
 * « A qui je le fais » : les cibles legales de l'option, en clair sous le
 * bouton. Trois noms maximum, puis « +N ». Une carte inconnue de la table
 * (face cachee) est nommee telle quelle.
 */
function resumeCibles(option: Option, cartesParId: Map<number, WorldCard>): string | undefined {
  if (option.target_num_range[1] === 0 || option.all_legal_targets.length === 0) return undefined
  const uniques = [...new Set(option.all_legal_targets)]
  const noms = uniques.map((id) => {
    const carte = cartesParId.get(id)
    return carte ? nomAffiche(carte) : 'facedown card'
  })
  const tetes = noms.slice(0, 3).join(', ')
  return `→ ${tetes}${noms.length > 3 ? ` +${noms.length - 3}` : ''}`
}

/**
 * Titre du panneau quand le moteur n'envoie AUCUN texte : plutot que « Normal »
 * (le type d'ability, illisible), on nomme la carte qui agit si toutes les
 * options viennent de la meme (« The Pericles — choose an option »).
 */
export function titreDepuisSource(
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
  const source = sources.length === 1 ? cartesParId.get(sources[0]!) : undefined
  const nom = source ? nomAffiche(source) : undefined
  return nom ? `${nom} — ${t('choisis une option')}` : texteDemande(demande)
}

/**
 * UNE FENETRE DE REACTION : le moteur s'arrete avant (ou apres) un evenement
 * pour laisser jouer une interruption ou une reponse, et « Passer » est
 * toujours possible. C'est la ou un nouveau joueur est perdu : le jeu attend,
 * une capacite au nom obscur est proposee, rien ne dit ce qu'elle fait.
 */
export function estFenetreDeReaction(demande: Demande): boolean {
  if (!demande.show_cancel) return false
  if (/interrupt|response/i.test(demande.ability_type)) return true
  return /^(When|After)/.test(demande.event_name) && demande.event_name !== 'WhenPlayerInTurn'
}

/** Une capacité FORCÉE (« Forced Interrupt », « Forced Response ») : rien à refuser. */
export function estForcee(demande: Demande): boolean {
  return /forced/i.test(demande.ability_type)
}

/** « Le Crimson Cowl s’apprête à recevoir 1⚠ (Menace de la phase du Méchant) » -> sans la parenthese technique. */
function sansParentheseTechnique(texte: string): string {
  return texte.replace(/\s*\([^()]*\)\s*$/, '').trim()
}

/**
 * « Jennifer Walters peut réagir » : qui porte les options d'une fenetre de
 * reaction. Plusieurs porteurs : « Tu peux réagir ».
 */
export function phraseDeReaction(
  options: Option[],
  cartesParId: Map<number, WorldCard>,
  nomPorteur?: (bindId: number) => string | undefined,
  forcee = false
): string {
  const porteurs = [...new Set(options.map((o) => o.bind_id).filter((id) => id !== 0))]
  if (porteurs.length === 1) {
    const nom = nomSourceParId(porteurs[0]!, cartesParId, nomPorteur)
    // Une capacité FORCÉE n'est pas facultative : « peut réagir » mentait.
    if (nom) return forcee ? `${nom} : ${t('choisis un effet')}` : `${nom} ${t('peut réagir')}`
  }
  return forcee ? t('Choisis un effet') : t('Tu peux réagir')
}

function nomSourceParId(
  bindId: number,
  cartesParId: Map<number, WorldCard>,
  nomPorteur?: (bindId: number) => string | undefined
): string | undefined {
  const porteur = cartesParId.get(bindId)
  return nomPorteur?.(bindId) || (porteur ? nomAffiche(porteur) : undefined)
}

/**
 * Le nom a ecrire sur le bouton d'une capacite NOMMEE (« "I Object!" »,
 * « Spider-Sense ») : celui que porte le texte dans la langue du plateau
 * (« "Objection !" — Interruption : ... »), sinon celui du moteur. Le moteur
 * ne connait que l'anglais ; le texte francais officiel, lui, commence par le
 * nom traduit, avant le tiret.
 */
export function nomDeCapacite(option: Option, texteCapacite: string | undefined): string {
  const nom = nomLisible(option)
  if (!texteCapacite) return nom
  const entete = texteCapacite.match(/^[«"]?\s*([^«»"—]{2,60}?)\s*[»"]?\s+—\s/)
  if (!entete) return nom
  // Seulement si le moteur nomme lui aussi une capacite, jamais pour un simple
  // « Interrupt » ni pour un nom technique (« Generate_Energy »). Les noms SANS
  // guillemets comptent : « Spider-Sense » restait en anglais au lieu de
  // « Sens d'Araignée » (signale par l'utilisateur, 04/10/2026).
  const moteurNomme =
    /^["«]/.test(option.name) || /—/.test(option.name) || estNomDeCapacite(option.name)
  // 19/10/2026 (Garde du Corps, Yōjimbō se011) : le moteur ne nomme pas cette capacité, son
  // option ne porte que le TYPE (« Hero Interrupt »), mais le texte de la carte lui donne un
  // nom imprimé (« Garde du Corps — Interruption de héros : … »). Choix de l'utilisateur :
  // le bouton dit ce nom. Seulement si l'en-tête est suivi d'un vrai type de capacité.
  const nomImprime = /—\s*(interrupt|interruption|response|réponse|action)/i.test(texteCapacite)
  return moteurNomme || nomImprime ? entete[1]!.trim() : nom
}

/** Un vrai nom de capacite (« Spider-Sense »), pas un TYPE ni un nom technique. */
function estNomDeCapacite(nomMoteur: string): boolean {
  if (nomMoteur.includes('_')) return false
  return !TYPES_DE_CAPACITE.test(nomMoteur.trim())
}

/** Les noms d'option qui ne sont qu'un TYPE de capacite, pas un nom propre. */
const TYPES_DE_CAPACITE =
  /^(forced |hero |alter-?ego )?(interrupt|response|action|resource|special|play|when revealed|defen[cs]e|attack|thwart|recover|scheme|activate|basic.*)$/i

/**
 * Le libelle du bouton de refus, a la place de « Passer » qui ne disait pas ce
 * qu'il fait. Choix de l'utilisateur, questions une a une (04/10/2026) :
 *  - une question de defense : « Ne pas défendre » ;
 *  - une reaction a UNE carte en main : « Ne pas jouer Contre-attaque » ;
 *  - une reaction a UNE capacite en jeu : « Ne pas utiliser Sens d'Araignée » ;
 *  - plusieurs reactions proposees : « Ne rien jouer » ;
 *  - tout le reste garde « Passer ».
 */
export function libelleRefus(
  options: Option[],
  reaction: boolean,
  cartesParId: Map<number, WorldCard>,
  nomPorteur?: (bindId: number) => string | undefined,
  texteCapacite?: (option: Option) => string | undefined,
  estEnMain?: (bindId: number) => boolean
): string {
  if (options.some((option) => option.name === 'Defense')) return t('Ne pas défendre')
  if (!reaction) return t('Passer')
  if (options.length !== 1) return t('Ne rien jouer')
  const option = options[0]!
  const carte = nomSource(option, cartesParId, nomPorteur)
  if (estEnMain?.(option.bind_id)) return carte ? `${t('Ne pas jouer')} ${carte}` : t('Ne rien jouer')
  // Capacite en jeu : le MEME nom que son bouton (« Spider-Sense », « Objection
  // ! »), sinon celui de la carte quand le moteur ne donne qu'un TYPE de
  // capacite : « Ne pas utiliser Interruption » ne voudrait rien dire. Vu en
  // capture le 04/10/2026 : la premiere version ne reconnaissait que les noms
  // entre guillemets, et ecrivait « Ne pas utiliser Spider-Man ».
  const nommee = /^["«]/.test(option.name) || /—/.test(option.name) || estNomDeCapacite(option.name)
  // Une capacité qui n'a que son TYPE pour nom (« Réponse », « Interruption ») : le refus reprend ce type,
  // comme le bouton d'à côté (« Réponse » / « Ne pas utiliser la Réponse »). Avec le nom de la carte
  // (« Ne pas utiliser Squirrel Girl »), on croyait annuler la mise en jeu de la carte (17/10/2026).
  if (!nommee) {
    const type = typeDeCapaciteAvecArticle(nomLisible(option))
    if (type) return `${t('Ne pas utiliser')} ${type}`
  }
  const nom = nommee ? nomDeCapacite(option, texteCapacite?.(option)) : carte
  return nom ? `${t('Ne pas utiliser')} ${nom}` : t('Passer')
}

/** « Réponse » -> « la Réponse », « Interruption » -> « l'Interruption » ; rien si ce n'est pas un type connu. */
function typeDeCapaciteAvecArticle(nom: string | undefined): string | undefined {
  const cle = (nom ?? '').trim().toLowerCase()
  const types: Record<string, string> = {
    'réponse': 'la Réponse', response: 'la Réponse',
    'réponse forcée': 'la Réponse forcée', 'forced response': 'la Réponse forcée',
    'interruption': "l'Interruption", interrupt: "l'Interruption",
    'interruption forcée': "l'Interruption forcée", 'forced interrupt': "l'Interruption forcée",
  }
  const phrase = types[cle]
  return phrase ? t(phrase) : undefined
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
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(signature)
  const styleDeplace = styleAvecDecalage(style, decalage)

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
      style={styleDeplace}
      aria-live="polite"
      aria-label={t('Événement de jeu')}
    >
      <div
        className="poignee-glisser"
        onPointerDown={gestesGlisser.onPointerDown}
        onPointerMove={gestesGlisser.onPointerMove}
        onPointerUp={gestesGlisser.onPointerUp}
        onPointerCancel={gestesGlisser.onPointerCancel}
      >
        <span className="plateau-eyebrow">{libelleEvenement(eventName)}</span>
        <strong>{avecIcones(texte)}</strong>
      </div>
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
  carteAuSurvol,
  nomPorteur,
  texteCapacite,
  estEnMain,
  ligneSansDefense,
  survolSansDefense,
  enScene = false,
  surLaTable = false,
  annulerAction,
}: DemandeCentraleProps) {
  const reaction = estFenetreDeReaction(demande)
  // UN SEUL CHOIX, SANS « Passer » : le titre recopiait le bouton (« Fin de
  // phase pour Domino » au-dessus de « FIN DE PHASE / Domino »). Demande de
  // l'utilisateur, 03/10/2026 : garder seulement le bouton. Le bandeau reste en
  // fine barre, parce que c'est lui qui sert de poignee pour deplacer le panneau.
  // Sauf l'option imposee « au maximum » : son titre explique pourquoi elle est seule (Sonic Boom, 11/10/2026).
  const choixUnique = options.length === 1 && !demande.show_cancel && !enScene && !options[0]?.au_maximum
  // BEAUCOUP DE CHOIX (07/10/2026) : les vignettes rapetissent, puis la liste
  // devient une colonne de lignes (mini-vignette a gauche, bouton a droite). Le
  // refus reste epingle en bas ; seule la liste defile. Voir board.css.
  const tailleDesChoix = enScene ? '' : options.length >= 7 ? ' dc-liste' : options.length >= 4 ? ' dc-compact' : ''
  /**
   * Les images de vignette deja posees dans CE rendu, pour n'en poser qu'une
   * par carte. Volontairement recree a chaque rendu : c'est un compteur de
   * boucle, pas un etat.
   */
  const vignettesPosees = new Set<string>()
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
  // Deplacement volontaire, a la poignee (le bandeau `.dc-texte`), par-dessus
  // le placement automatique : deux decisions qui s'enchainent posent deux
  // panneaux l'un sur l'autre, rien ne permettait d'ecarter celui du dessus.
  // Remis a zero a chaque nouvelle decision (`signature`) : une position
  // gardee par-dessus une decision qui n'existe plus deroute plus qu'elle
  // n'aide. Inactif en scene (`enScene`), ou le panneau ne flotte pas.
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(signature)
  const styleDeplace: typeof style = enScene ? style : styleAvecDecalage(style, decalage)

  // EPURE (16/10/2026) : devant le cartouche « Pendant ton tour » / de la phase du
  // mechant, la question n'a plus de bandeau a elle ; ses boutons SUIVENT le
  // cartouche (on deplace la fenetre par son bandeau jaune, les boutons partent
  // avec elle). Les variables `--ep-ancre-*` sont lues par affichage-epure.css.
  useEffect(() => {
    if (enScene) return
    const element = panneau.current
    if (!element) return
    let image = 0
    const suivre = () => {
      const racine = document.documentElement
      const cartouche = document.querySelector('.deroule-phase.est-scene:not(.est-question)')
      if (racine.dataset.epure && cartouche) {
        const c = cartouche.getBoundingClientRect()
        element.style.setProperty('--ep-ancre-x', `${Math.round(c.left + 232)}px`)
        element.style.setProperty('--ep-ancre-y', `${Math.round(c.top + 118)}px`)
        element.dataset.surCartouche = 'oui'
      } else if (element.dataset.surCartouche) {
        delete element.dataset.surCartouche
        element.style.removeProperty('--ep-ancre-x')
        element.style.removeProperty('--ep-ancre-y')
      }
      image = requestAnimationFrame(suivre)
    }
    image = requestAnimationFrame(suivre)
    return () => cancelAnimationFrame(image)
  }, [enScene, panneau])

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
    activerOption(vise, carteAuSurvol?.(vise) ?? carteDeLOption?.(vise))
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

  // SANS MODALE : une question à UNE seule option qui demande des cibles (« ordre d'activation des
  // sbires ») ne vaut pas un clic de plus : on entre directement dans le ciblage, sur la table.
  const optionSeule = options.length === 1 && !demande.show_cancel ? options[0] : undefined
  const entrerDansLeCiblage = surLaTable && optionSeule !== undefined && optionSeule.target_num_range[1] > 0 && !optionSeule.failure_reason
  const idOptionSeule = optionSeule?.id
  useEffect(() => {
    if (entrerDansLeCiblage && optionSeule) choisirOuInformer(optionSeule)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- une seule fois par question
  }, [entrerDansLeCiblage, idOptionSeule, demande.event_name])

  if (surLaTable) {
    const phrase = options.some((option) => option.name === 'Defense')
      ? t('Qui défend contre cette attaque ?')
      : titreDepuisSource(demande, options, cartesParId).replace(/\s*\(\+0\)\s*$/, '')
    const posees = new Set<number>()
    const choix: ChoixSurTable[] = options.map((option) => {
      const nomBrut = reaction ? nomDeCapacite(option, texteCapacite?.(option)) : nomLisible(option)
      const source = nomSource(option, cartesParId, nomPorteur)
      const defense = option.name === 'Defense' && source !== undefined
      const nom = defense ? `${t('Défendre avec')} ${source}` : nomBrut
      const carte = carteDeLOption?.(option) ?? (reaction ? carteAuSurvol?.(option) : undefined)
      const carteId = carte && !posees.has(Number(carte.id)) ? Number(carte.id) : undefined
      if (carteId !== undefined) posees.add(carteId)
      return {
        id: option.id,
        nom: carte?.kind === 'upgrade' && source && !String(nom).includes(source) ? `${source} — ${nom}` : String(nom),
        carteId,
        enLigne: carte?.kind === 'upgrade',
        carte: carte?.kind === 'upgrade' ? carte : undefined,
        indisponible: option.failure_reason || undefined,
        choisir: () => choisirOuInformer(option),
        survoler: (actif: boolean) => (actif ? activerOption(option, carteAuSurvol?.(option) ?? carte) : desactiverOption(option)),
      }
    })
    const attaque = ligneSansDefense && options.some((option) => option.name === 'Defense')
    return (
      <>
      <QuestionSurTable
        phrase={phrase}
        choix={choix}
        refus={
          demande.show_cancel
            ? {
                libelle: `${libelleRefus(options, reaction, cartesParId, nomPorteur, texteCapacite, estEnMain)}${attaque ? ` (${ligneSansDefense})` : ''}`,
                agir: annuler,
              }
            : undefined
        }
      />
      {carteRegardee ? <CarteApercu carte={carteRegardee} /> : null}
      </>
    )
  }

  return (
    <section
      ref={panneau}
      className={`demande-centrale${enScene ? ' est-en-scene' : ''}${tailleDesChoix}`}
      style={enScene ? undefined : styleDeplace}
      role="dialog"
      aria-label="Game decision"
      aria-live="polite"
    >
      {/* Poignee de deplacement : le bandeau du haut, deja sans bouton ni
          contenu cliquable. Un simple clic (sans franchir le seuil de
          glisser) ne fait rien, donc rien ne casse pour qui ne glisse pas. */}
      <div
        className={enScene ? 'dc-texte' : `dc-texte poignee-glisser${choixUnique ? ' est-poignee-seule' : ''}`}
        onPointerDown={enScene ? undefined : gestesGlisser.onPointerDown}
        onPointerMove={enScene ? undefined : gestesGlisser.onPointerMove}
        onPointerUp={enScene ? undefined : gestesGlisser.onPointerUp}
        onPointerCancel={enScene ? undefined : gestesGlisser.onPointerCancel}
      >
        {demande.annuler_action && annulerAction ? (
          <button
            type="button"
            className="dc-croix"
            onClick={annulerAction}
            // Le bandeau est la poignee de deplacement : la croix ne glisse pas.
            onPointerDown={(evenement) => evenement.stopPropagation()}
            aria-label={t('Annuler l’action')}
            title={t('Annuler l’action (Échap)')}
          >
            ×
          </button>
        ) : null}
        {/* Dans le cartouche du mechant, ni « À toi de jouer » ni « Tu peux
            réagir » (retires le 03/10/2026, demande de l'utilisateur) : la
            phrase et les boutons disent tout. */}
        {enScene || choixUnique ? null : <span className="plateau-eyebrow">{libelleTypeDemande(demande)}</span>}
        {choixUnique ? null : <strong>
          {avecIcones(
            marquerRessources(
              reaction
                ? sansParentheseTechnique(titreDepuisSource(demande, options, cartesParId))
                : titreDepuisSource(demande, options, cartesParId)
            )
          )}
        </strong>}
        {/* Qui peut reagir, en clair : le nom de la capacite seul (« I Object! »)
            ne le dit pas a un nouveau joueur. */}
        {reaction && !enScene ? (
          <span className="dc-reagit">{phraseDeReaction(options, cartesParId, nomPorteur, estForcee(demande))}</span>
        ) : null}
      </div>

      {/* Le TEXTE de l'effet, sous le titre (Épuré, 17/10/2026 : « Réponse : après que Squirrel Girl entre
          en jeu… »). Masqué hors Épuré (board.css) : les autres affichages gardent leur fenêtre. */}
      {reaction && !enScene
        ? (() => {
            const textes = [...new Set(options.map((option) => texteCapacite?.(option)).filter((x): x is string => Boolean(x)))]
            if (textes.length === 0) return null
            // « Réponse : après que… » : le nom de la capacité en gras, le reste en clair.
            const brut = textes.join(' ')
            const m = brut.match(/^([^:]{2,30}?) : ([\s\S]*)$/)
            return <span className="dc-effet">{m ? <><b>{m[1]}</b> : {m[2]}</> : brut}</span>
          })()
        : null}

      <div className={`af-boutons dc-boutons${choixUnique ? ' est-choix-unique' : ''}`} onMouseOver={survolerZone} onMouseLeave={quitterZone}>
        {/*
          ⚠ UNE SEULE VIGNETTE PAR IMAGE, ET PAS UNE PAR BOUTON.
          Signale en jeu le 15/09/2026, capture a l'appui : « pourquoi il montre
          l'image de mon perso deux fois ? ». Ironheart portait DEUX options de
          la meme fenetre de reaction (Defense et Ask) et chaque bouton posait
          SA vignette : deux fois la meme carte cote a cote, plus la vraie sur
          la table. La deuxieme n'apprenait rien.

          ⚠ ON REGROUPE SUR L'IMAGE, PAS SUR LE PORTEUR. Une recherche dans le
          deck propose plusieurs cartes DIFFERENTES sous un meme `bind_id` (ou
          sous `bind_id === 0`) : regrouper par porteur les fondrait en une
          seule vignette et on ne saurait plus ce qu'on choisit.
        */}
        {options.map((option) => {
          const nomBrut = reaction ? nomDeCapacite(option, texteCapacite?.(option)) : nomLisible(option)
          const source = nomSource(option, cartesParId, nomPorteur)
          // « Défendre avec Domino » plutôt que « DÉFENDRE / Domino » : le bouton
          // dit d'un trait QUI défend (demande de l'utilisateur, 03/10/2026).
          const defense = option.name === 'Defense' && source !== undefined
          // Sa DÉF entre parentheses (04/10/2026) : on compare d'un coup d'oeil
          // avec « Ne pas défendre (ATQ …) ».
          const defenseur = defense ? cartesParId.get(option.bind_id) : undefined
          const def = defense ? ligneDefense(defenseur, nomPorteur) : undefined
          const nom = defense ? `${t('Défendre avec')} ${source}${def ? ` (${def})` : ''}` : nomBrut
          const cibles = resumeCibles(option, cartesParId)
          const indisponible = option.failure_reason !== ''
          const montrerRaison = indisponible && raisonVisible === option.id
          // La vignette : la carte nommee, sinon, sur une fenetre de reaction,
          // la carte PORTEUSE (elle n'apparaissait qu'au survol). Reconnaitre
          // la carte est la moitie de la comprehension.
          const carteBrute = carteDeLOption?.(option) ?? (reaction ? carteAuSurvol?.(option) : undefined)
          const dejaMontree = carteBrute !== undefined && vignettesPosees.has(carteBrute.id)
          if (carteBrute) vignettesPosees.add(carteBrute.id)
          const carte = dejaMontree ? undefined : carteBrute
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
                }${defense ? ' est-defense' : ''}${option.au_maximum ? ' est-au-maximum' : ''}`}
                aria-disabled={indisponible || undefined}
                title={indisponible ? option.failure_reason : undefined}
                onFocus={() => activerOption(option, carteAuSurvol?.(option) ?? carteBrute)}
                onBlur={() => desactiverOption(option)}
                onClick={() => choisirOuInformer(option)}
              >
                <span>{avecIcones(marquerRessources(nom))}</span>
                {source && !defense ? <small>{source}</small> : null}
                {cibles && !defense ? <small className="af-cibles">{cibles}</small> : null}
              </button>
              {montrerRaison ? <span className="af-raison">{option.failure_reason}</span> : null}
            </span>
          )
        })}
        {demande.show_cancel ? (
          <span className="af-action-wrap dc-refus">
            {(() => {
              const attaque = ligneSansDefense && options.some((option) => option.name === 'Defense')
              return (
                <button
                  type="button"
                  className={`af-action tonalite-general dc-pass${attaque ? ' est-defense' : ''}`}
                  onClick={annuler}
                  title={attaque ? (survolSansDefense ?? ligneSansDefense) : undefined}
                >
                  {libelleRefus(options, reaction, cartesParId, nomPorteur, texteCapacite, estEnMain)}
                  {attaque ? ` (${ligneSansDefense})` : null}
                </button>
              )
            })()}
          </span>
        ) : null}
      </div>

      {/* Plus de texte de capacite sous les boutons (retire le 03/10/2026, demande
          de l'utilisateur) : la carte, au-dessus de son bouton, se lit en grand
          au survol. */}
      {/* Le meme agrandissement que sur la table : scan en grand, mots-cles et
          texte francais. Il se monte dans <body> (portail) et passe devant ce
          panneau, comme il passe devant la table. */}
      {carteRegardee ? <CarteApercu carte={carteRegardee} /> : null}
    </section>
  )
}
