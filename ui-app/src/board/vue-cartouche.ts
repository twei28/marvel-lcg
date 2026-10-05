// LE MODELE DE VUE DU CARTOUCHE DU BAS (refonte du 04/10/2026, scene PC,
// mode « Étape par étape »). Decisions : `.planning/todos/2026-10-04-refonte-
// phase-mechant-decisions.md` (D1 a D43).
//
// Une etape du deroule et son contexte entrent ; des DONNEES sortent : quelles
// vignettes dans la rangee, quelle jauge, quels textes, deja en langue. Le
// composant (CartouchePhase) ne fait que les dessiner.
//
// Module PUR, comme deroule-phase.ts et frise-phase.ts : aucun DOM, aucun
// React, AUCUNE CLOSURE dans ce qu'il rend (la vue doit survivre a un
// JSON.stringify : c'est ce qui la rend testable d'un bloc). Les questions du
// moteur n'entrent pas ici : elles passent par `sous-cadre.ts`.
//
// ⚠ RIEN D'INVENTE (piege 40 de la carte du code) : `restant` absent, seuil
// absent, apport nul, degats subis negatifs existent. Une valeur absente se
// tait, une valeur presente s'affiche telle quelle, signe compris.

import type { CardKind, ScanCardProps } from '../components/ScanCard'
import { compteurDeLEtape, type EtapeDeroule, type TempsPhase } from './deroule-phase'
import {
  libelleDeStatut,
  surtitreEtape,
  lignesSonne,
  texteActivationAnnulee,
  texteConsequence,
  texteEffet,
  titreEtape,
} from './deroule-textes'
import { ONGLETS, coupsDe, resumeOnglet } from './frise-phase'
import { t } from './langue'
import type { StatsStade } from './world'

// ------------------------------------------------------------------ PASTILLES

/** Les CINQ pastilles de la scene (D15, D34). Six temps internes, cinq dessinees. */
export type ClePastille = 'menace' | 'mechant' | 'sbires' | 'cartes-rencontre' | 'bilan'

/**
 * Les cinq pastilles, dans l'ordre de la carte de reference. Le point 3
 * (distribution) et le point 4 (revelation) n'en font qu'une, « 3. Cartes
 * rencontre » (D15) ; les temps internes du modele, eux, ne bougent pas
 * (`ORDRE`, `TEMPS_PAR_PHASE`, `ONGLETS` servent encore la table et le
 * telephone, piege 44).
 *
 * ⚠ `libelle` passe par `t()` a travers une variable : la gate du dictionnaire
 * ne le voit pas. `vue-cartouche.test.ts` verifie que chacun a son anglais.
 */
export const PASTILLES: ReadonlyArray<{
  cle: ClePastille
  /** « ① » … « ⑤ » */
  numero: string
  /** Nom complet, affiche au survol (title). Cle t(). */
  libelle: string
  /** Nom court pour « Revenir à 2B ». */
  court: string
  /** Nom de l'étape, écrit à côté du chiffre dans la frise. Clé t(). */
  nom: string
  temps: ReadonlyArray<TempsPhase>
}> = [
  { cle: 'menace', numero: '①', libelle: '1. Placer les menaces', court: '1', nom: 'Menaces', temps: ['menace'] },
  { cle: 'mechant', numero: '②', libelle: '2A. Le méchant s’active', court: '2A', nom: 'Méchant', temps: ['mechant'] },
  { cle: 'sbires', numero: '③', libelle: '2B. Les sbires s’activent', court: '2B', nom: 'Sbires', temps: ['sbires'] },
  { cle: 'cartes-rencontre', numero: '④', libelle: '3. Cartes rencontre', court: '3', nom: 'Cartes rencontre', temps: ['distribution', 'revelation'] },
  { cle: 'bilan', numero: '⑤', libelle: 'Bilan', court: 'Bilan', nom: 'Bilan', temps: ['bilan'] },
]

/** La pastille qui dessine un temps du modele ; aucune pour 'premier-joueur'. */
export function pastilleDuTemps(temps: TempsPhase): ClePastille | undefined {
  return PASTILLES.find((pastille) => pastille.temps.includes(temps))?.cle
}

export type Pastille = {
  cle: ClePastille
  numero: string
  libelle: string
  court: string
  nom: string
  /** Resultat court (resumeOnglet agrege), « 1 carte distribuée » en tete sur ④, '' a venir. */
  resume: string
  etat: 'passe' | 'courant' | 'a-venir'
  relu: boolean
  /** Heros vise (D27), seulement si la table a plus d'un heros. */
  portraitId?: number
  /** « 1 / 2 » (D14, D27). */
  compteur?: string
  /** Un clic relit : passee, et jamais pendant une question. */
  relisible: boolean
}

/**
 * Le temps que la frise montre COMME COURANT. Pendant une question, il suit
 * la phase REELLE du moteur quand elle a pris de l'avance sur la derniere
 * etape connue (meme regle que le cartouche d'avant, `DeroulePhase.tsx`,
 * `tempsAffiche`) : la question de defense d'un sbire allume ③, pas ②.
 */
export function tempsAfficheDe(
  etape: EtapeDeroule,
  questionAuJoueur: boolean,
  tempsQuestion: TempsPhase | undefined
): TempsPhase {
  const position = (temps: TempsPhase) => ONGLETS.findIndex((onglet) => onglet.cle === temps)
  return questionAuJoueur && tempsQuestion !== undefined && position(tempsQuestion) > position(etape.temps)
    ? tempsQuestion
    : etape.temps
}

/**
 * Le HEROS VISE par une etape (D27), pour le portrait de la pastille : la
 * cible ANNONCEE d'abord, parce qu'une fois la defense jouee `cibleId` est le
 * defenseur (piege 37), et seulement si c'est un heros de la table.
 */
export function herosViseDe(etape: EtapeDeroule, herosIds: ReadonlySet<number>): number | undefined {
  const id = etape.cibleAnnonceeId ?? etape.cibleId
  return id !== undefined && herosIds.has(id) ? id : undefined
}

/** « 1 carte distribuée » (D15), puis ce que les cartes revelees ont fait. */
function resumePastille(cle: ClePastille, etapes: EtapeDeroule[], cartesDistribuees: number): string {
  if (cle !== 'cartes-rencontre') return resumeOnglet(etapes, cle)
  // Les etapes de distribution d'une liste NON fondue (table, telephone, ou un
  // appelant qui ne fond pas) comptent aussi : une liste fondue n'en a plus.
  const distribuees =
    cartesDistribuees +
    etapes.reduce((somme, e) => somme + (e.titre === 'distribution' ? (e.montant ?? 1) : 0), 0)
  const revelation = resumeOnglet(etapes, 'revelation')
  if (distribuees === 0) return revelation
  const tete = (distribuees < 2 ? t('%1 carte distribuée') : t('%1 cartes distribuées')).replace('%1', String(distribuees))
  return revelation === t('aucun') ? tete : `${tete} · ${revelation}`
}

/**
 * LES CINQ PASTILLES de la ligne du haut (D22, D34). Une pastille se juge par
 * rapport a celle du temps affiche : avant elle PASSEE (avec son resultat
 * court), elle COURANTE, apres elle A VENIR (jamais declaree vide : constat en
 * partie, « Sbires (aucun) » pendant que le moteur demandait l'ordre).
 */
export function pastilles(args: {
  etapes: EtapeDeroule[]
  index: number
  tempsAffiche: TempsPhase
  cartesDistribuees: number
  questionAuJoueur: boolean
  relecture?: ClePastille
  herosViseId?: number
  plusieursHeros: boolean
}): Pastille[] {
  const courante = pastilleDuTemps(args.tempsAffiche)
  // Un temps sans pastille compte comme place APRES toutes : elles sont alors
  // toutes passees, ce qui est exactement ce qui vient de se passer.
  const rangCourant = courante === undefined ? PASTILLES.length : PASTILLES.findIndex((p) => p.cle === courante)
  const etapeCourante = args.etapes[args.index]
  const pastilleDeLEtape = etapeCourante ? pastilleDuTemps(etapeCourante.temps) : undefined
  const rang = compteurDeLEtape(args.etapes, args.index)
  return PASTILLES.map((pastille, position) => {
    const etat: Pastille['etat'] =
      position === rangCourant ? 'courant' : position < rangCourant ? 'passe' : 'a-venir'
    // Compteur et portrait parlent de l'etape LUE : seulement sur sa pastille,
    // pas sur celle qu'une question a fait avancer.
    const surLEtape = etat === 'courant' && pastilleDeLEtape === pastille.cle
    // La pastille COURANTE tait « aucun » : son temps n'est pas fini, et
    // « ② aucun » pendant l'annonce de Rhino se lisait comme une attaque sans
    // effet (planche du lot 6). Une pastille passee vide le dit toujours.
    const resume = etat === 'a-venir' ? '' : resumePastille(pastille.cle, args.etapes, args.cartesDistribuees)
    return {
      cle: pastille.cle,
      numero: pastille.numero,
      libelle: t(pastille.libelle),
      court: t(pastille.court),
      nom: t(pastille.nom),
      resume: etat === 'courant' && resume === t('aucun') ? '' : resume,
      etat,
      relu: args.relecture === pastille.cle,
      portraitId: surLEtape && args.plusieursHeros ? args.herosViseId : undefined,
      compteur: surLEtape && rang ? `${rang.rang} / ${rang.total}` : undefined,
      relisible: etat === 'passe' && !args.questionAuJoueur,
    }
  })
}

// ------------------------------------------------------------------ LA VUE

export type Vignette = {
  cle: string
  /** data-card-id pour la loupe (piege 8). */
  carteId?: number
  /** undefined : nom seul (carte introuvable dans le monde). */
  scan?: ScanCardProps
  nom: string
  /** « ATQ 2 », « +1 ★ », « défend · DÉF 3 » */
  legende?: string
  etat: 'inerte' | 'cliquable' | 'choisie' | 'grisee' | 'indisponible'
  /** (1)…(9), D37. */
  chiffre?: number
  /** Option du moteur portee par cette vignette (defense, reponse, choix). */
  optionId?: number
  /** failure_reason mise en francais, visible sur « indisponible ». */
  raison?: string
  ordre?: number
  fois?: number
}

export type Jauge = { avant?: number; apres?: number; plafond?: number }

export type VueRangee = {
  genre: 'rangee'
  acteur?: Vignette
  boosts: Array<Vignette & { apport: number; etoile?: boolean }>
  /** « = 3 », en gros au resultat. */
  total?: { texte: string; gros: boolean }
  /** « 1 par joueur + 1 accélération = 2 » (D12). */
  calcul?: string
  /** Defenseur retenu, marque « défend · DÉF 3 » (D8, D11). */
  defenseur?: Vignette
  /** Le heros vise, la manigance visee (D13) ; les choix viennent du sous-cadre. */
  cibles: Vignette[]
  /** « 1 dégât subi », jauge 10 → 9 / 14 (D11). */
  resultat?: { texte: string; jauge?: Jauge }
  /** Trait rouge en travers et « ANNULÉE · Étourdi » (D24) ; cause absente toleree (piege 41). */
  annulee?: { cause?: string }
  /** « ★ Charge : … », une ligne par boost etoile (D10). */
  lignesEtoile: string[]
  /** Grisee sous un sous-cadre ou pendant l'attente d'un autre joueur (le composant decide). */
  grisee: boolean
}

export type QuestionCarte = { intitule: string; choix: Vignette[]; refus?: { libelle: string } }

export type VueRevelee = {
  genre: 'revelee'
  carte: Vignette
  /** « Traîtrise », « Sbire »… depuis le fait (`typeCarte`), sinon le genre de la carte. */
  typeFr?: string
  /** texteEffet / texteConsequence, deja en langue. */
  lignes: string[]
  jauge?: Jauge
  /** La carte suivante de la liste si elle est revelee par Renfort (D17). */
  renfort?: Vignette
  /** La carte a Renfort mais la suivante n'est pas encore revelee : une case vide « ? » (D17). */
  renfortInconnu?: boolean
  /** Question posee par la carte, a droite (D18) : posee par le composant. */
  question?: QuestionCarte
  surtitreRenfort?: string
}

export type VueStade = {
  genre: 'stade'
  avant?: Vignette
  apres: Vignette
  /** « PV 14 → 15 », « ATQ 2 → 3 », « Menace 7 » */
  deltas: string[]
}

/**
 * Une colonne du bilan : une carte touchee pendant la phase. `total` est ce
 * que la phase lui a coute (degats ou menaces), compte par la regle unique
 * (`coupsDe`, frise-phase.ts) : c'est lui qui se compare aux onglets.
 */
export type ColonneJauge = {
  cle: string
  carteId?: number
  nom: string
  total: number
  jauge: Jauge
  statuts?: string[]
}

export type VueBilan = {
  genre: 'bilan'
  menace: ColonneJauge[]
  heros: ColonneJauge[]
  nouveautes: Vignette[]
  vide: boolean
}

export type VueVide = { genre: 'vide'; texte: string }
export type VueAttente = { genre: 'attente'; rangee: VueRangee; texte: string }
export type VueQuestionSeule = { genre: 'question-seule' }

export type VueCorps = VueRangee | VueRevelee | VueStade | VueBilan | VueVide | VueAttente | VueQuestionSeule

export type ContexteVue = {
  /** Les etapes BRUTES de la phase (noms du moteur) : ce qui se cherche par nom anglais. */
  etapes: EtapeDeroule[]
  index: number
  boostsMontres: number
  carteScene?: (id: number, faceVisible: boolean) => ScanCardProps | undefined
  nomFr?: (id: number) => string | undefined
  /** PV maximum par nom ANGLAIS nettoye (board.tsx, comme pour le bilan d'avant). */
  pvMaxParNom?: Map<string, number>
  /** Le texte FR de la capacite Boost (★) d'une carte, quand on le connait. */
  texteEtoile?: (carteId: number) => string | undefined
  /** info.printed_stage, info.target_threat… lus sur le monde par board.tsx. */
  infoCarte?: (id: number) => Partial<Record<string, number>> | undefined
  /** Ce que le catalogue sait d'une carte rencontre revelee : son Renfort, son texte imprime. */
  infoRevelee?: (carteId: number) => InfoRevelee | undefined
}

export type InfoRevelee = {
  /** La carte porte le mot-cle Renfort : une autre carte suivra son clic. */
  renfort: boolean
  /** Son texte imprime en langue, sans Renfort ni Boost (`extraireEffetRevele`). */
  texteImprime?: string[]
}

/** Un nombre utilisable : ni absent, ni NaN. */
function nombre(valeur: number | null | undefined): valeur is number {
  return typeof valeur === 'number' && Number.isFinite(valeur)
}

/** Un seuil ou un maximum qui en est un : un 0 ne dit rien (« 0/0 »). */
function seuil(valeur: number | null | undefined): number | undefined {
  return nombre(valeur) && valeur > 0 ? valeur : undefined
}

/** « +2 », et « -1 » tel quel pour un retrait : jamais « +-1 ». */
function signe(n: number): string {
  return n >= 0 ? `+${n}` : `${n}`
}

/** Le numero d'un stade en chiffres romains (« Stade II »), comme sur la carte. */
function romain(n: number): string {
  const valeurs: Array<[number, string]> = [
    [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I'],
  ]
  let reste = Math.floor(n)
  let texte = ''
  for (const [valeur, chiffre] of valeurs) {
    while (reste >= valeur) {
      texte += chiffre
      reste -= valeur
    }
  }
  return texte
}

/**
 * Le type d'une carte rencontre, en langue : d'abord le nom de classe que le
 * fait publie (« Treachery »), sinon le genre de la carte du monde. Une
 * branche par type, pour que chaque traduction reste un litteral visible de la
 * gate du dictionnaire.
 */
function typeFrDe(classe: string | undefined, genre: CardKind | undefined): string | undefined {
  const cle = classe ?? genre
  switch (cle) {
    case 'Treachery':
    case 'treachery':
      return t('Traîtrise')
    case 'Minion':
    case 'minion':
      return t('Sbire')
    case 'Attachment':
    case 'attachment':
      return t('Attachement')
    case 'SideScheme':
    case 'side-scheme':
      return t('Manigance annexe')
    case 'Environment':
    case 'environment':
      return t('Environnement')
    case 'Obligation':
    case 'obligation':
      return t('Obligation')
    default:
      return undefined
  }
}

/**
 * L'etape BRUTE qui correspond a l'etape lue : la vue recoit l'etape en langue
 * (`etapeEnLangue`), mais les PV maximum se cherchent par le nom ANGLAIS.
 */
function etapeBrute(etape: EtapeDeroule, ctx: ContexteVue): EtapeDeroule {
  return ctx.etapes.find((autre) => autre.cle === etape.cle) ?? etape
}

/** Une vignette inerte : la carte du monde si on la connait, son nom sinon. */
function vignette(cle: string, id: number | undefined, nom: string | undefined, ctx: ContexteVue): Vignette {
  const scan = id !== undefined ? ctx.carteScene?.(id, true) : undefined
  return {
    cle,
    carteId: id,
    scan,
    nom: nom || (id !== undefined ? ctx.nomFr?.(id) : undefined) || scan?.name || '',
    etat: 'inerte',
  }
}

/** Le titre court Bangers (D30), en Title Case : la MAJUSCULE vient du CSS (text-transform). */
export function titreCourt(etape: EtapeDeroule, ctx: ContexteVue): string {
  switch (etape.titre) {
    case 'attaque':
      return etape.auteurNom ? t('Attaque de %1').replace('%1', etape.auteurNom) : t('Attaque')
    case 'manigance':
      return t('Manigance')
    case 'menace':
      return t('Menace')
    case 'bilan':
      return t('Bilan')
    case 'distribution':
      return t('Cartes rencontre')
    case 'entree':
      return etape.cibleNom ? t('%1 entre en jeu').replace('%1', etape.cibleNom) : t('Un sbire entre en jeu')
    case 'statut':
      return libelleDeStatut(etape.statut) || titreEtape(etape)
    case 'sonne':
      return t('Sonné')
    case 'stade': {
      const numero = etape.carteId !== undefined ? ctx.infoCarte?.(etape.carteId)?.printed_stage : undefined
      return nombre(numero) && numero > 0 ? t('Stade %1').replace('%1', romain(numero)) : t('Stade suivant')
    }
    case 'revelation': {
      // Une carte enchainee par Renfort se dit par ce qui l'a amenee (D17) :
      // la carte elle-meme est en grand juste dessous.
      if (etape.parSurge) return etape.renfortDe ? t('Renfort de %1').replace('%1', etape.renfortDe) : t('Renfort')
      const nom = etape.cibleNom || t('Carte révélée')
      const genre = etape.carteId !== undefined ? ctx.carteScene?.(etape.carteId, true)?.kind : undefined
      const type = typeFrDe(etape.typeCarte, genre)
      return type ? `${nom} (${type})` : nom
    }
    default:
      return titreEtape(etape)
  }
}

/** Le seuil d'une manigance : le fait, puis l'etape de menace du round, puis le monde. */
function plafondDe(etape: EtapeDeroule, ctx: ContexteVue): number | undefined {
  return (
    seuil(etape.plafond) ??
    seuil(
      ctx.etapes.find(
        (autre) => autre.plafond !== undefined && autre.cibleId !== undefined && autre.cibleId === etape.cibleId
      )?.plafond
    ) ??
    (etape.cibleId !== undefined ? seuil(ctx.infoCarte?.(etape.cibleId)?.target_threat) : undefined)
  )
}

/** « 1 par joueur + 1 accélération = 2 » (D12), seulement si le moteur l'a decompose. */
function calculMenace(etape: EtapeDeroule): string | undefined {
  const { escalade, acceleration, joueurs } = etape
  if (!nombre(escalade) || !nombre(joueurs) || joueurs < 1) return undefined
  // « par joueur » seulement quand c'est vrai : une escalade qui ne se divise
  // pas par le nombre de joueurs ne s'invente pas de part par joueur.
  const morceaux = [
    escalade % joueurs === 0 ? `${escalade / joueurs} ${t('par joueur')}` : `${escalade} ${t('d’escalade')}`,
  ]
  if (nombre(acceleration) && acceleration > 0) morceaux.push(`${acceleration} ${t('accélération')}`)
  return `${morceaux.join(' + ')} = ${etape.montant ?? 0}`
}

function texteMenaces(n: number): string {
  return `${signe(n)} ${Math.abs(n) < 2 ? t('menace') : t('menaces')}`
}

/** La menace du point 1 (D12) : la manigance, le calcul, la jauge. */
function vueMenace(etape: EtapeDeroule, ctx: ContexteVue): VueRangee {
  const montant = etape.montant
  const jauge: Jauge | undefined =
    nombre(etape.restant) && montant !== undefined
      ? { avant: Math.max(0, etape.restant - montant), apres: etape.restant, plafond: seuil(etape.plafond) }
      : undefined
  return {
    genre: 'rangee',
    acteur: vignette(`acteur:${etape.cle}`, etape.cibleId, etape.cibleNom, ctx),
    boosts: [],
    calcul: calculMenace(etape),
    cibles: [],
    resultat: montant !== undefined ? { texte: texteMenaces(montant), jauge } : undefined,
    lignesEtoile: [],
    grisee: false,
  }
}

/**
 * Une ACTIVATION (D7 a D11, D13, D24) : l'acteur a gauche, ses boosts colles,
 * le total, le defenseur, la cible visee, le resultat en gros. LA MEME rangee
 * de l'annonce au resultat : rien ne change de place, elle se complete.
 */
function vueActivation(etape: EtapeDeroule, ctx: ContexteVue): VueRangee {
  const brute = etapeBrute(etape, ctx)
  const attaque = etape.titre === 'attaque'
  const annulee = etape.etat === 'annule'
  const resolue = etape.etat === undefined || etape.etat === 'resolu'
  const montres = etape.boosts.slice(0, Math.max(0, ctx.boostsMontres))

  // « ATQ 2 » : la valeur IMPRIMEE quand le moteur la donne, sinon ce que
  // l'etape porte (la base resolue, ou la valeur annoncee).
  const imprime = etape.baseImprimee ?? (resolue ? etape.base : etape.valeurAnnoncee)
  const sigle = attaque ? t('ATQ') : t('MAN')
  const acteur: Vignette = {
    ...vignette(`acteur:${etape.cle}`, etape.carteId, etape.auteurNom, ctx),
    legende: nombre(imprime) ? `${sigle} ${imprime}` : undefined,
  }

  const boosts = montres.map((boost) => {
    // Un apport nul ne se dit qu'avec l'etoile (« +0 ★ ») : sans elle, il
    // n'apprend rien.
    const apport = boost.apport !== 0 || boost.etoile ? signe(boost.apport) : ''
    const legende = [apport, boost.etoile ? '★' : ''].filter(Boolean).join(' ')
    return {
      ...vignette(`boost:${boost.cle}`, boost.cibleId, boost.nom, ctx),
      legende: legende || undefined,
      apport: boost.apport,
      etoile: boost.etoile,
    }
  })

  // Le SOCLE du total, avant les boosts : la base resolue (qui les exclut
  // deja), ou, sur une annonce enrichie, le total publie moins TOUS ses boosts.
  // Le total suit alors les seuls boosts deja retournes (`boostsMontres`).
  const tousLesApports = etape.boosts.reduce((somme, boost) => somme + boost.apport, 0)
  const socle = resolue
    ? etape.base
    : nombre(etape.totalAvantDefense)
      ? etape.totalAvantDefense - tousLesApports
      : etape.baseImprimee
  const total =
    !annulee && montres.length > 0 && nombre(socle)
      ? { texte: `= ${socle + montres.reduce((somme, boost) => somme + boost.apport, 0)}`, gros: resolue }
      : undefined

  const defenseur: Vignette | undefined =
    !annulee && etape.defenseurId !== undefined
      ? {
          ...vignette(`defenseur:${etape.defenseurId}`, etape.defenseurId, etape.defenseurNom, ctx),
          // Un allie n'a pas de DEF : le moteur publie 0, « DÉF 0 » n'apprend
          // rien (planche du lot 6, Black Widow).
          legende:
            nombre(etape.defense) && etape.defense > 0 ? `${t('défend')} · ${t('DÉF')} ${etape.defense}` : t('défend'),
        }
      : undefined

  // LE HEROS VISE (piege 37) : la cible annoncee d'abord. Il ne fait qu'une
  // vignette avec le defenseur quand il a defendu lui-meme.
  const viseId = etape.cibleAnnonceeId ?? etape.cibleId
  const viseNom = viseId === etape.cibleId ? etape.cibleNom : undefined
  const cibles =
    viseId !== undefined && viseId === defenseur?.carteId ? [] : [vignette(`cible:${viseId ?? ''}`, viseId, viseNom, ctx)]

  let resultat: VueRangee['resultat']
  if (resolue && etape.montant !== undefined) {
    const montant = etape.montant
    if (attaque) {
      const pvMax = seuil(brute.cibleNom ? ctx.pvMaxParNom?.get(brute.cibleNom) : undefined)
      resultat = {
        texte: `${montant} ${Math.abs(montant) < 2 ? t('dégât subi') : t('dégâts subis')}`,
        // L'AVANT se deduit du restant et du subi, borne par le maximum : un
        // coup de 6 sur 4 PV laisse la cible a 0, elle n'avait pas 6 PV.
        // L'APRES s'arrete a 0 : un allie vaincu arrive du moteur avec un
        // restant negatif (planche du lot 5, « 2 → -2 / 2 »).
        jauge: nombre(etape.restant)
          ? {
              avant: pvMax !== undefined ? Math.min(etape.restant + montant, pvMax) : etape.restant + montant,
              apres: Math.max(0, etape.restant),
              plafond: pvMax,
            }
          : undefined,
      }
    } else {
      resultat = {
        texte: texteMenaces(montant),
        jauge: nombre(etape.restant)
          ? { avant: Math.max(0, etape.restant - montant), apres: etape.restant, plafond: plafondDe(etape, ctx) }
          : undefined,
      }
    }
  }

  const lignesEtoile = montres
    .filter((boost) => boost.etoile)
    .map((boost) => `★ ${boost.nom} : ${ctx.texteEtoile?.(boost.cibleId) ?? t('son effet de boost s’applique')}`)

  return {
    genre: 'rangee',
    acteur,
    boosts,
    total,
    defenseur,
    cibles,
    resultat,
    annulee: annulee ? (etape.annuleePar ? { cause: libelleDeStatut(etape.annuleePar) } : {}) : undefined,
    lignesEtoile,
    grisee: false,
  }
}

/** Une carte rencontre revelee (D16, D17) : la carte en grand, son effet resume, le Renfort. */
function vueRevelee(etape: EtapeDeroule, ctx: ContexteVue): VueRevelee {
  const carte = vignette(`carte:${etape.cle}`, etape.carteId, etape.cibleNom, ctx)
  const lignes = [
    ...(etape.effets ?? []).map(texteEffet),
    ...(etape.consequences ?? []).map(texteConsequence),
  ]
  const annulation = texteActivationAnnulee(etape)
  if (annulation) lignes.push(annulation)

  // Aucun resume publie par le moteur : le texte imprime de la carte tient
  // lieu de resume, plutot qu'un cote droit vide (decision du 05/10/2026).
  const infoCarteRevelee = etape.carteId !== undefined ? ctx.infoRevelee?.(etape.carteId) : undefined
  if (lignes.length === 0 && infoCarteRevelee?.texteImprime?.length) lignes.push(...infoCarteRevelee.texteImprime)

  // Une jauge seulement quand la carte n'a fait qu'UNE chose mesuree : avec
  // deux effets, laquelle montrer serait un choix invente.
  const seul = etape.effets?.length === 1 && !etape.consequences?.length ? etape.effets[0] : undefined
  let jauge: Jauge | undefined
  if (seul && seul.genre !== 'entree' && nombre(seul.restant)) {
    jauge =
      seul.genre === 'degats'
        ? { avant: seul.restant + seul.montant, apres: seul.restant }
        : { avant: Math.max(0, seul.restant - seul.montant), apres: seul.restant }
  }

  // LA CARTE SUIVANTE, si un Renfort l'a revelee : la premiere revelation par
  // Renfort qui suit celle-ci dans la liste (`relierLesRenforts`).
  let renfort: Vignette | undefined
  if (etape.suivieDUnRenfort) {
    const position = ctx.etapes.findIndex((autre) => autre.cle === etape.cle)
    const suivante = ctx.etapes
      .slice((position === -1 ? ctx.index : position) + 1)
      .find((autre) => autre.titre === 'revelation' && autre.parSurge)
    if (suivante) {
      const nom = (suivante.carteId !== undefined ? ctx.nomFr?.(suivante.carteId) : undefined) ?? suivante.cibleNom
      renfort = vignette(`renfort:${suivante.cle}`, suivante.carteId, nom, ctx)
    }
  }
  // Le Renfort ne se connait qu'apres le clic : tant que la carte suivante
  // n'est pas revelee, une case vide la tient (la carte a le mot-cle).
  const renfortInconnu = renfort === undefined && infoCarteRevelee?.renfort === true ? true : undefined

  return {
    genre: 'revelee',
    carte,
    typeFr: typeFrDe(etape.typeCarte, carte.scan?.kind),
    lignes,
    jauge,
    renfort,
    renfortInconnu,
    surtitreRenfort: surtitreEtape(etape) || undefined,
  }
}

/**
 * Un ennemi SONNE (etat 04, decision du 05/10/2026) : sa carte en grand et deux
 * lignes, dans le gabarit de la carte revelee (meme hauteur, meme pagination).
 */
function vueSonne(etape: EtapeDeroule, ctx: ContexteVue): VueRevelee {
  const carte = vignette(`carte:${etape.cle}`, etape.carteId, etape.auteurNom, ctx)
  return {
    genre: 'revelee',
    carte,
    typeFr: typeFrDe(undefined, carte.scan?.kind),
    lignes: lignesSonne(etape),
    renfort: undefined,
    renfortInconnu: undefined,
    surtitreRenfort: undefined,
  }
}

/**
 * Le stade (D25) : ancienne carte → nouvelle, les stats qui CHANGENT. Sans le
 * fait enrichi (moteur ancien), la nouvelle carte seule et ses stats du monde,
 * sans fleche : l'ancienne carte n'a plus d'`info` (piege 39).
 */
function vueStade(etape: EtapeDeroule, ctx: ContexteVue): VueStade {
  const stats: Array<[keyof StatsStade, string, string]> = [
    ['pv_max', 'max_health', t('PV')],
    ['atq', 'attack', t('ATQ')],
    ['man', 'scheme', t('MAN')],
    ['seuil', 'target_threat', t('Menace')],
  ]
  const deltas: string[] = []
  if (etape.statsApres) {
    for (const [cle, , sigle] of stats) {
      const avant = etape.statsAvant?.[cle]
      const apres = etape.statsApres[cle]
      if (!nombre(apres)) continue
      if (!nombre(avant)) deltas.push(`${sigle} ${apres}`)
      else if (avant !== apres) deltas.push(`${sigle} ${avant} → ${apres}`)
    }
  } else if (etape.carteId !== undefined) {
    const info = ctx.infoCarte?.(etape.carteId)
    for (const [, cleMonde, sigle] of stats) {
      const valeur = info?.[cleMonde]
      if (nombre(valeur)) deltas.push(`${sigle} ${valeur}`)
    }
  }
  // ⚠ LE MECHANT GARDE SON OBJET d'un stade a l'autre (`SetAsCard`,
  // scenario.py) : `stadeAvantId` vaut alors `carteId`, et le monde ne connait
  // plus que la nouvelle face. La dessiner en « avant » montrerait la nouvelle
  // carte deux fois (planche du lot 3, etat 7) : on se tait plutot.
  const avantDessinable = etape.stadeAvantId !== undefined && etape.stadeAvantId !== etape.carteId
  return {
    genre: 'stade',
    avant: avantDessinable
      ? vignette(`avant:${etape.stadeAvantId}`, etape.stadeAvantId, etape.auteurNom, ctx)
      : undefined,
    apres: vignette(`apres:${etape.carteId ?? ''}`, etape.carteId, etape.cibleNom, ctx),
    deltas,
  }
}

/**
 * LE CORPS DE LA VUE pour une etape. `etape` est l'etape LUE (en langue,
 * `etapeEnLangue`) ; `ctx.etapes` la liste brute de la phase.
 */
export function vueDeLEtape(etape: EtapeDeroule, ctx: ContexteVue): VueCorps {
  switch (etape.titre) {
    case 'bilan':
      return bilanTroisColonnes(ctx.etapes, ctx)
    case 'attaque':
    case 'manigance':
      return vueActivation(etape, ctx)
    case 'menace':
      return vueMenace(etape, ctx)
    case 'revelation':
      return vueRevelee(etape, ctx)
    case 'sonne':
      return vueSonne(etape, ctx)
    case 'stade':
      return vueStade(etape, ctx)
    case 'statut':
      return {
        genre: 'rangee',
        acteur: vignette(`acteur:${etape.cle}`, etape.cibleId, etape.cibleNom, ctx),
        boosts: [],
        cibles: [],
        resultat: { texte: libelleDeStatut(etape.statut) },
        lignesEtoile: [],
        grisee: false,
      }
    case 'entree':
      return {
        genre: 'rangee',
        acteur: vignette(`acteur:${etape.cle}`, etape.carteId, etape.cibleNom, ctx),
        boosts: [],
        cibles: [],
        lignesEtoile: [],
        grisee: false,
      }
    default:
      // Un temps vide, une distribution d'une liste non fondue, un titre libre :
      // une phrase.
      return { genre: 'vide', texte: titreEtape(etape) }
  }
}

// ------------------------------------------------------------------ LE BILAN

type Groupe = {
  cle: string
  carteId?: number
  nomBrut?: string
  total: number
  restant?: number
  plafond?: number
  statuts: string[]
}

/**
 * LE BILAN EN TROIS COLONNES (D19) : la menace (une jauge par manigance), les
 * heros et allies touches (avant → apres), les cartes entrees en jeu.
 *
 * ⚠ UNE SEULE REGLE DE COMPTAGE (piege 43) : les coups viennent de `coupsDe`
 * (frise-phase.ts), la meme source que le resultat court des onglets. Les
 * totaux des deux se comparent dans `frise-phase.test.ts`.
 */
export function bilanTroisColonnes(etapes: EtapeDeroule[], ctx: ContexteVue): VueBilan {
  const menace = new Map<string, Groupe>()
  const heros = new Map<string, Groupe>()
  const nouveautes: Vignette[] = []
  const groupe = (table: Map<string, Groupe>, prefixe: string, carteId: number | undefined, nom: string | undefined) => {
    const cle = `${prefixe}:${carteId ?? nom ?? ''}`
    let deja = table.get(cle)
    if (!deja) {
      deja = { cle, carteId, nomBrut: nom, total: 0, statuts: [] }
      table.set(cle, deja)
    }
    return deja
  }

  for (const etape of etapes) {
    if (etape.titre === 'vide' || etape.temps === 'bilan') continue
    for (const coup of coupsDe(etape)) {
      if (coup.genre === 'degats' || coup.genre === 'menaces') {
        const g = groupe(coup.genre === 'degats' ? heros : menace, coup.genre, coup.cibleId, coup.cibleNom)
        g.total += coup.montant
        // Un compteur connu n'est remplace que par un compteur connu : le
        // dernier coup connu donne l'etat le plus recent.
        if (nombre(coup.restant)) g.restant = coup.restant
        if (seuil(coup.plafond) !== undefined) g.plafond = coup.plafond
      } else if (coup.genre === 'statut') {
        const g = groupe(heros, 'degats', coup.cibleId, coup.cibleNom)
        if (!g.statuts.includes(coup.statut)) g.statuts.push(coup.statut)
      } else if (coup.genre === 'sbire' || coup.genre === 'autre') {
        const { carteId, carteNom } = coup
        if (carteId !== undefined && nouveautes.some((v) => v.carteId === carteId)) continue
        const nom = (carteId !== undefined ? ctx.nomFr?.(carteId) : undefined) ?? carteNom
        nouveautes.push(vignette(`nouveaute:${carteId ?? carteNom ?? ''}`, carteId, nom, ctx))
      }
    }
  }

  const nomDe = (g: Groupe) => (g.carteId !== undefined ? ctx.nomFr?.(g.carteId) : undefined) ?? g.nomBrut ?? ''
  const colonne = (g: Groupe, jauge: Jauge): ColonneJauge => ({
    cle: g.cle,
    carteId: g.carteId,
    nom: nomDe(g),
    total: g.total,
    jauge,
    statuts: g.statuts.length > 0 ? g.statuts : undefined,
  })

  const colonnesMenace = [...menace.values()].map((g) => {
    const plafond = seuil(g.plafond) ?? (g.carteId !== undefined ? seuil(ctx.infoCarte?.(g.carteId)?.target_threat) : undefined)
    return colonne(
      g,
      nombre(g.restant) ? { avant: Math.max(0, g.restant - g.total), apres: g.restant, plafond } : { plafond }
    )
  })
  const colonnesHeros = [...heros.values()].map((g) => {
    // Les PV maximum par nom ANGLAIS : les etapes du bilan sont brutes.
    const pvMax = seuil(g.nomBrut ? ctx.pvMaxParNom?.get(g.nomBrut) : undefined)
    return colonne(
      g,
      nombre(g.restant)
        ? {
            avant: pvMax !== undefined ? Math.min(g.restant + g.total, pvMax) : g.restant + g.total,
            apres: g.restant,
            plafond: pvMax,
          }
        : { plafond: pvMax }
    )
  })

  return {
    genre: 'bilan',
    menace: colonnesMenace,
    heros: colonnesHeros,
    nouveautes,
    vide: colonnesMenace.length === 0 && colonnesHeros.length === 0 && nouveautes.length === 0,
  }
}
