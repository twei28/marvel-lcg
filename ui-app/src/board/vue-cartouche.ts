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

import type { CardGauge, CardKind, ScanCardProps } from '../components/ScanCard'
import {
  compteurDeLEtape,
  nomNettoye,
  precedenteAnnuleePar,
  type EtapeDeroule,
  type TempsPhase,
} from './deroule-phase'
import {
  libelleDeStatut,
  surtitreEtape,
  lignesSonne,
  texteActivationAnnulee,
  texteConsequence,
  texteEffet,
  texteSortieAnnulation,
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
  /** La bande de la table (PV ou menace), avec les chiffres de l'etape quand elle les donne. */
  jauge?: CardGauge
  /** « PV 7 / 10 · 3 dégâts », « Menace 3 / 5 · +1 menace » : la bande en texte, sous la carte. */
  recap?: string
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
  /**
   * Les chiffres du calcul POSE (essai du 10/10/2026, question 9) : la valeur
   * de l'acteur et la defense, pour ecrire « 1 + 0 + 0 − 0 = 1 » entre les
   * vignettes. Absent : on ne pose rien, plutot qu'un chiffre invente.
   */
  pose?: { base?: number; defense?: number; jauge: 'pv' | 'menace' }
  /** Defenseur retenu, marque « défend · DÉF 3 » (D8, D11). */
  defenseur?: Vignette
  /** Le heros vise, la manigance visee (D13) ; les choix viennent du sous-cadre. */
  cibles: Vignette[]
  /** « 1 dégât subi », jauge 10 → 9 / 14 (D11). */
  /** `note` : « menaces retirées » quand la manigance s'est vidée en atteignant son seuil. */
  /** `tampon` (13/10/2026) : « K.O. » quand le heros tombe, « VAINCU » pour un allie ou un sbire a 0. */
  /**
   * `tampon` (13/10/2026) : « K.O. » quand le heros tombe, « VAINCU » pour un allie ou un sbire a 0.
   * `barre` et `raison` : ce que le coup aurait fait, barre, et pourquoi il a fait moins.
   * `nul` : aucun degat, dit en vert.
   */
  resultat?: { texte: string; jauge?: Jauge; note?: string; tampon?: 'K.O.' | 'VAINCU'; barre?: string; raison?: string; nul?: boolean }
  /** Trait rouge en travers et « ANNULÉE · Étourdi » (D24) ; cause absente toleree (piege 41). */
  annulee?: { cause?: string; par?: Vignette }
  /**
   * LOT 5 (essai, decision 7) : la menace de l'etape 1 decomposee source par
   * source, avec le total, la jauge et « COMPLÉTÉE » quand le seuil est atteint.
   */
  /** `prevu` (13/10/2026) : la somme des sources quand le moteur a posé MOINS (une carte a réduit la menace). */
  menace?: { sources: Array<{ libelle: string; valeur: number; parJoueur?: boolean }>; total: number; jauge?: Jauge; complete: boolean; prevu?: number }
  /** « ★ Charge : … », une ligne par boost etoile (D10). */
  lignesEtoile: string[]
  /** Grisee sous un sous-cadre ou pendant l'attente d'un autre joueur (le composant decide). */
  grisee: boolean
  /** Une carte qui ENTRE en jeu (refonte, lot 4, decision 3) : bandeau « NOUVEAU SBIRE » dans l'essai. */
  entree?: { sbire: boolean }
  /** Lot 5b (decision 40) : une ligne par mot-cle qui a joue sur le coup (Perçant, Robuste, Déferlement). */
  motsCles?: string[]
  /** Lot 5b (decision 39) : l'ecran de la Riposte. */
  riposte?: { vaincu: boolean }
  /** Lot 5c (decision 38) : l'effet ★ differe d'un boost, sur son ecran a part. */
  etoileDifferee?: { texte: string; issue: string }
  /** Lot 5c (decision 45) : un heros elimine. */
  elimine?: boolean
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
  /** La carte revelee A LA PLACE de celle-ci, annulee (Stepford Cuckoos, n72). */
  remplacement?: Vignette
  /** « Révélée par Stepford Cuckoos », au-dessus de la fleche vers `remplacement`. */
  lienRemplacement?: string
  /**
   * Toute la chaine dont la carte fait partie, dans l'ordre (rapport Yarro n72) :
   * Weapons Runner → Renfort → Klaw's Vengeance [annulée] → Sonic Boom. Absente
   * pour une carte seule.
   */
  chaine?: MaillonChaine[]
  /**
   * Ce qu'il faut savoir de la carte d'un coup d'oeil (essai du 10/10/2026) :
   * « Ton obligation », « Nouvelle manigance », « Péril : décide seul ».
   */
  etiquettes?: string[]
}

export type MaillonChaine = {
  vignette: Vignette
  /** Le lien depuis le maillon precedent : « Renfort », « Révélée par X ». */
  lien?: string
  /** « Annulée par X » quand l'effet de cette carte a ete annule. */
  annulee?: string
  /** La carte qui l'a annulee, en vignette (essai du 10/10/2026, tampon « ANNULÉE »). */
  annuleePar?: Vignette
  courante: boolean
}

export type VueStade = {
  genre: 'stade'
  avant?: Vignette
  apres: Vignette
  /** « PV 14 → 15 », « ATQ 2 → 3 », « Menace 7 » */
  deltas: string[]
  /** Lot 5c (decision 11) : ce qui se passe ensuite, dit en une ligne (essai). */
  suite?: string
}

/** Lot 5c (decision 42) : le tableau de la distribution de l'etape 3, une ligne par joueur. */
export type VueDistribution = {
  genre: 'distribution'
  lignes: Array<{ cle: string; nom: string; joueur?: number; cartes: number; raisons: string[] }>
  total: number
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
  /** LOT 5 (essai, decision 12) : la liste courte de la phase, une ligne par etape, survolable. */
  evenements?: Array<{ cle: string; texte: string; carteId?: number }>
}

export type VueVide = { genre: 'vide'; texte: string }
export type VueAttente = { genre: 'attente'; rangee: VueRangee; texte: string }
export type VueQuestionSeule = { genre: 'question-seule' }

export type VueCorps = VueRangee | VueRevelee | VueStade | VueBilan | VueVide | VueAttente | VueQuestionSeule | VueDistribution

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
    case 'EncounterSideScheme':
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
    jauge: scan?.jauge,
    recap: recapDeJauge(scan?.jauge),
  }
}

/** « PV 7 / 10 », « Menace 3 / 5 » : la bande de la table dite en mots, et son changement s'il y en a un. */
export function recapDeJauge(jauge: CardGauge | undefined, changement?: string): string | undefined {
  if (!jauge?.texte) return undefined
  const base = `${jauge.genre === 'menace' ? t('Menace') : t('PV')} ${jauge.texte}`
  return changement ? `${base} · ${changement}` : base
}

/**
 * La vignette avec la bande de L'ETAPE : la table peut etre en avance sur le
 * recit, les chiffres de l'etape priment sur ceux du monde. Sans maximum
 * connu, la bande du monde reste (rien d'invente).
 */
function avecJaugeDeLEtape(
  v: Vignette,
  genre: 'pv' | 'menace',
  jauge: Jauge | undefined,
  changement: string | undefined
): Vignette {
  if (!jauge || !nombre(jauge.apres) || !nombre(jauge.plafond) || jauge.plafond <= 0) return v
  const bande: CardGauge = {
    remplissage: Math.min(1, Math.max(0, jauge.apres / jauge.plafond)),
    genre,
    alarme: v.jauge?.alarme ?? genre === 'pv',
    texte: `${jauge.apres} / ${jauge.plafond}`,
  }
  return { ...v, jauge: bande, recap: recapDeJauge(bande, changement) }
}

/** Le titre court Bangers (D30), en Title Case : la MAJUSCULE vient du CSS (text-transform). */
export function titreCourt(etape: EtapeDeroule, ctx: ContexteVue): string {
  switch (etape.titre) {
    case 'attaque':
      return etape.auteurNom ? t('Attaque de %1').replace('%1', etape.auteurNom) : t('Attaque')
    case 'manigance':
      return t('Manigance')
    case 'riposte':
      return etape.auteurNom ? t('Riposte de %1').replace('%1', etape.auteurNom) : t('Riposte')
    case 'etoile-differe':
      return etape.auteurNom ? t('Effet ★ de %1').replace('%1', etape.auteurNom) : t('Effet ★')
    case 'elimination':
      return etape.cibleNom ? t('%1 est éliminé').replace('%1', etape.cibleNom) : t('Un héros est éliminé')
    case 'distribution-tableau':
      // 13/10/2026 (encadré ⑪) : « Distribution : 3 cartes rencontre ».
      return etape.montant !== undefined
        ? t('Distribution : %1').replace('%1', `${etape.montant} ${etape.montant < 2 ? t('carte rencontre') : t('cartes rencontre')}`)
        : t('Cartes rencontre distribuées')
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
    case 'paquet-vide':
      return t('Paquet rencontre vide')
    case 'stade-revele':
      return etape.cibleNom ? t('%1 : une fois révélé').replace('%1', etape.cibleNom) : t('Une fois révélé')
    case 'stade': {
      const numero = etape.carteId !== undefined ? ctx.infoCarte?.(etape.carteId)?.printed_stage : undefined
      return nombre(numero) && numero > 0 ? t('Stade %1').replace('%1', romain(numero)) : t('Stade suivant')
    }
    case 'revelation': {
      // Une carte enchainee par Renfort se dit par ce qui l'a amenee (D17) :
      // la carte elle-meme est en grand juste dessous. Meme regle pour une
      // carte de remplacement (« Révélée par Stepford Cuckoos », n72).
      if (etape.reveleePar) return surtitreEtape(etape)
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

/** « (Cloak) » : les cartes dont l'icône d'accélération est comptée (rapport BL-Stark n°104). Vide quand le moteur ne les donne pas. */
function sourcesAcceleration(etape: EtapeDeroule): string {
  const noms = [...new Set((etape.sourcesAcceleration ?? []).map((nom) => nomNettoye(nom) ?? nom))]
  return noms.length > 0 ? ` (${noms.join(', ')})` : ''
}

/** « 1 par joueur + 1 accélération (Cloak) = 2 » (D12), seulement si le moteur l'a decompose. */
export function calculMenace(etape: EtapeDeroule): string | undefined {
  const { escalade, acceleration, joueurs } = etape
  if (!nombre(escalade) || !nombre(joueurs) || joueurs < 1) return undefined
  // « par joueur » seulement quand c'est vrai : une escalade qui ne se divise
  // pas par le nombre de joueurs ne s'invente pas de part par joueur.
  const morceaux = [
    escalade % joueurs === 0 ? `${escalade / joueurs} ${t('par joueur')}` : `${escalade} ${t('d’escalade')}`,
  ]
  if (nombre(acceleration) && acceleration > 0) morceaux.push(`${acceleration} ${t('accélération')}${sourcesAcceleration(etape)}`)
  return `${morceaux.join(' + ')} = ${etape.montant ?? 0}`
}

function texteMenaces(n: number): string {
  return `${signe(n)} ${Math.abs(n) < 2 ? t('menace') : t('menaces')}`
}

/**
 * LA MENACE DECOMPOSEE (lot 5, decision 7) : une ligne par source, comme le
 * joueur la refait a la main. Seulement ce que le moteur publie : l'escalade
 * (par joueur quand elle se divise) et les icones d'acceleration.
 */
function decompositionMenace(
  etape: EtapeDeroule,
  montant: number,
  jauge: Jauge | undefined,
  ctx: ContexteVue
): NonNullable<VueRangee['menace']> {
  const sources: Array<{ libelle: string; valeur: number; parJoueur?: boolean }> = []
  const { escalade, acceleration, joueurs } = etape
  if (nombre(escalade) && nombre(joueurs) && joueurs >= 1) {
    sources.push({
      libelle:
        escalade % joueurs === 0
          ? t('Manigance : %1 par joueur × %2').replace('%1', String(escalade / joueurs)).replace('%2', String(joueurs))
          : t('Manigance'),
      valeur: escalade,
      // 13/10/2026 (encadré ①) : la ligne qui compte les joueurs porte leurs pastilles.
      parJoueur: escalade % joueurs === 0,
    })
  }
  if (nombre(acceleration) && acceleration > 0) sources.push({ libelle: `${t('Accélération')}${sourcesAcceleration(etape)}`, valeur: acceleration })
  // Sans decomposition publiee, une seule ligne : le total tel quel.
  if (sources.length === 0) sources.push({ libelle: t('Manigance'), valeur: montant })
  // 13/10/2026 : la somme prévue, puis chaque carte qui a réduit la pose (« Surveillance −1 »).
  const prevuAvantReductions = sources.reduce((acc, source) => acc + source.valeur, 0)
  for (const r of etape.reductions ?? []) sources.push({ libelle: nomNettoye(r.source) ?? r.source, valeur: -r.valeur })
  const plafond = plafondDe(etape, ctx)
  const avecSeuil = jauge ? { ...jauge, plafond: jauge.plafond ?? plafond } : undefined
  const complete = !!avecSeuil && nombre(avecSeuil.apres) && nombre(avecSeuil.plafond) && avecSeuil.plafond > 0 && avecSeuil.apres >= avecSeuil.plafond
  return {
    sources,
    total: montant,
    jauge: avecSeuil,
    complete,
    prevu: prevuAvantReductions > montant ? prevuAvantReductions : undefined,
  }
}

/** La menace du point 1 (D12) : la manigance, le calcul, la jauge. */
function vueMenace(etape: EtapeDeroule, ctx: ContexteVue): VueRangee {
  const montant = etape.montant
  const jauge: Jauge | undefined =
    nombre(etape.restant) && montant !== undefined
      ? { avant: Math.max(0, etape.restant - montant), apres: etape.restant, plafond: seuil(etape.plafond) }
      : undefined
  return {
    menace: montant !== undefined ? decompositionMenace(etape, montant, jauge, ctx) : undefined,
    genre: 'rangee',
    acteur: avecJaugeDeLEtape(
      vignette(`acteur:${etape.cle}`, etape.cibleId, etape.cibleNom, ctx),
      'menace',
      jauge,
      montant !== undefined ? texteMenaces(montant) : undefined
    ),
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
      // 13/10/2026 (encadré ④) : le coup a fait moins que prévu (Robuste, réduction) :
      // la valeur prévue barrée, et la raison. Rien d'inventé : `inflige` et `subi` viennent du moteur.
      const inflige = etape.inflige
      const reduit = nombre(inflige) && inflige > montant
      resultat = {
        texte:
          montant === 0
            ? t('AUCUN DÉGÂT')
            : `${montant} ${Math.abs(montant) < 2 ? t('dégât subi') : t('dégâts subis')}`,
        barre: reduit ? `${inflige} ${inflige < 2 ? t('dégât') : t('dégâts')}` : undefined,
        // 13/10/2026 (encadré ⑥) : un ★ sans effet, dit en une ligne sous le résultat.
        note: etape.etoilesSansEffet?.length
          ? etape.etoilesSansEffet
              .map((nom) => `★ ${nomNettoye(nom) ?? nom} : ${t('sans effet (aucun dégât)')}`)
              .join(' · ')
          : undefined,
        // La carte responsable quand le moteur la publie (« Bouclier −2 »), sinon Robuste ou « réduit ».
        raison: reduit
          ? etape.reductions?.length
            ? etape.reductions.map((r) => `${nomNettoye(r.source) ?? r.source} −${r.valeur}`).join(' · ')
            : etape.motsCles?.robuste
              ? t('Robuste')
              : t('réduit')
          : undefined,
        nul: montant === 0 || undefined,
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
        tampon: etape.defaite ? 'K.O.' : nombre(etape.restant) && etape.restant <= 0 ? 'VAINCU' : undefined,
      }
    } else {
      // La manigance a pu atteindre son seuil puis se vider (21099b) : on montre
      // la montee reelle (« 3 → 6 / 6 ») et on dit qu'elle s'est videe.
      const pic = nombre(etape.menaceAvant) ? etape.menaceAvant + montant : undefined
      const videe = pic !== undefined && nombre(etape.restant) && etape.restant < pic
      resultat = {
        texte: texteMenaces(montant),
        jauge: nombre(etape.restant)
          ? {
              avant: etape.menaceAvant ?? Math.max(0, etape.restant - montant),
              apres: videe ? pic : etape.restant,
              plafond: plafondDe(etape, ctx),
            }
          : undefined,
        note: videe ? t('menaces retirées') : undefined,
        // 13/10/2026 : des cartes ont réduit la menace posée : la valeur prévue barrée, et elles.
        ...(etape.reductions?.length
          ? {
              barre: texteMenaces(montant + etape.reductions.reduce((acc, r) => acc + r.valeur, 0)),
              raison: etape.reductions.map((r) => `${nomNettoye(r.source) ?? r.source} −${r.valeur}`).join(' · '),
            }
          : {}),
      }
    }
  }

  // La bande de l'etape resolue va sur la carte qui l'a ENCAISSEE (`cibleId`) :
  // l'allie defenseur quand il a defendu, jamais le heros vise (capture k2-25).
  let defenseurFinal = defenseur
  if (resultat?.jauge && etape.montant !== undefined) {
    const montant = etape.montant
    const avecBande = (v: Vignette) =>
      avecJaugeDeLEtape(
        v,
        attaque ? 'pv' : 'menace',
        resultat.jauge,
        attaque ? `${montant} ${Math.abs(montant) < 2 ? t('dégât') : t('dégâts')}` : texteMenaces(montant)
      )
    if (defenseur && etape.cibleId !== undefined && defenseur.carteId === etape.cibleId) {
      defenseurFinal = avecBande(defenseur)
    } else if (cibles[0]) {
      cibles[0] = avecBande(cibles[0])
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
    pose: annulee
      ? undefined
      : {
          base: nombre(socle) ? socle : nombre(imprime) ? imprime : undefined,
          defense: defenseur && nombre(etape.defense) ? etape.defense : undefined,
          jauge: attaque ? 'pv' : 'menace',
        },
    defenseur: defenseurFinal,
    cibles,
    resultat,
    annulee: annulee
      ? {
          ...(etape.annuleePar ? { cause: libelleDeStatut(etape.annuleePar) } : {}),
          // LOT 5 (decision 6) : la carte qui annule, a cote du tampon.
          ...(etape.annuleeParId !== undefined
            ? {
                par: vignette(
                  `annuleur:${etape.cle}`,
                  etape.annuleeParId,
                  etape.annuleePar ? libelleDeStatut(etape.annuleePar) : undefined,
                  ctx
                ),
              }
            : {}),
        }
      : undefined,
    lignesEtoile,
    grisee: false,
    motsCles: resolue && !annulee ? lignesMotsCles(etape) : undefined,
  }
}

/** Lot 5b (decision 40) : ce que Perçant, Robuste et Déferlement ont fait, une ligne chacun. */
export function lignesMotsCles(etape: EtapeDeroule): string[] | undefined {
  const mots = etape.motsCles
  if (!mots) return undefined
  const lignes: string[] = []
  if (mots.percant) lignes.push(t('Perçant : la carte Robuste est défaussée avant les dégâts'))
  if (mots.robuste) lignes.push(t('Robuste : la carte Robuste absorbe tout le coup'))
  if (mots.overkill)
    lignes.push(
      t('Déferlement : %1 en trop sur %2')
        .replace('%1', `${mots.overkill.degats} ${mots.overkill.degats < 2 ? t('dégât') : t('dégâts')}`)
        .replace('%2', nomNettoye(mots.overkill.cible) ?? mots.overkill.cible)
    )
  return lignes.length > 0 ? lignes : undefined
}

/** Lot 5b (decision 39) : la Riposte, un ecran a part, la carte touchee frappe l'attaquant. */
/** Lot 5c (decision 38) : l'effet ★ differe, au moment ou il s'applique. */
function vueEtoileDifferee(etape: EtapeDeroule, ctx: ContexteVue): VueRangee {
  const texte = (etape.carteId !== undefined ? ctx.texteEtoile?.(etape.carteId) : undefined) ?? t('son effet de boost s’applique')
  const degats = /\b(deals? damage|inflige[nt]? des dégâts)\b/i.test(texte)
  const sansDefense = /\b(undefended|n.est pas défendue)\b/i.test(texte)
  let issue = t('S’applique maintenant, à la fin de l’activation.')
  if (degats) {
    issue =
      (etape.montant ?? 0) > 0
        ? t('Condition remplie : %1 subis, l’effet s’applique.').replace('%1', `${etape.montant} ${(etape.montant ?? 0) < 2 ? t('dégât') : t('dégâts')}`)
        : t('Sans effet : aucun dégât subi.')
  } else if (sansDefense) {
    issue = etape.defenseurId === undefined ? t('Condition remplie : l’attaque n’était pas défendue.') : t('Sans effet : l’attaque était défendue.')
  }
  return {
    genre: 'rangee',
    acteur: { ...vignette(`etoile:${etape.cle}`, etape.carteId, etape.auteurNom, ctx), legende: '★' },
    boosts: [],
    cibles: etape.cibleId !== undefined ? [vignette(`cible:${etape.cibleId}`, etape.cibleId, etape.cibleNom, ctx)] : [],
    lignesEtoile: [],
    grisee: false,
    etoileDifferee: { texte: `★ ${texte}`, issue },
  }
}

const LIBELLE_RAISON: Record<string, string> = {
  base: 'la règle (1 par joueur)',
  danger: 'Danger',
  renfort: 'Renfort',
  carte: 'effet de carte',
}

/** Lot 5c (decision 42) : le tableau de la distribution, la raison de chaque carte en clair. */
function vueDistribution(etape: EtapeDeroule): VueDistribution {
  const lignes = (etape.lignesDistribution ?? []).map((ligne, rang) => ({
    cle: `${etape.cle}:${ligne.joueur ?? rang}`,
    nom: ligne.nom ?? `${t('Joueur')} ${(ligne.joueur ?? rang) + 1}`,
    joueur: ligne.joueur,
    cartes: ligne.cartes,
    raisons: ligne.raisons.map((r) => {
      const libelle = t(LIBELLE_RAISON[r.raison] ?? 'effet de carte')
      return r.source && r.raison !== 'base' ? `${libelle} : ${r.source}` : libelle
    }),
  }))
  return { genre: 'distribution', lignes, total: etape.montant ?? lignes.reduce((s, l) => s + l.cartes, 0) }
}

function vueRiposte(etape: EtapeDeroule, ctx: ContexteVue): VueRangee {
  const montant = etape.montant ?? 0
  const pvMax = seuil(etape.cibleNom ? ctx.pvMaxParNom?.get(etape.cibleNom) : undefined)
  const jauge: Jauge | undefined = nombre(etape.restant)
    ? {
        avant: pvMax !== undefined ? Math.min(etape.restant + montant, pvMax) : etape.restant + montant,
        apres: Math.max(0, etape.restant),
        plafond: pvMax,
      }
    : undefined
  const texteDegats = `${montant} ${montant < 2 ? t('dégât') : t('dégâts')}`
  const cible = vignette(`cible:${etape.cibleId ?? ''}`, etape.cibleId, etape.cibleNom, ctx)
  return {
    genre: 'rangee',
    acteur: { ...vignette(`acteur:${etape.cle}`, etape.carteId, etape.auteurNom, ctx), legende: t('Riposte') },
    boosts: [],
    cibles: [jauge ? avecJaugeDeLEtape(cible, 'pv', jauge, texteDegats) : cible],
    resultat: { texte: etape.riposte?.vaincu ? `${texteDegats} · ${t('VAINCU')}` : texteDegats, jauge },
    lignesEtoile: [],
    grisee: false,
    riposte: { vaincu: Boolean(etape.riposte?.vaincu) },
  }
}

/** Le resultat d'une etape en trois mots, pour la liste du bilan : « 3 dégâts », « +2 menaces », « annulée ». */
function resultatCourt(etape: EtapeDeroule): string | undefined {
  if (etape.etat === 'annule') return t('annulée')
  if (etape.montant === undefined || etape.temps === 'revelation' || etape.temps === 'distribution') return undefined
  if (etape.titre === 'attaque') return `${etape.montant} ${Math.abs(etape.montant) < 2 ? t('dégât') : t('dégâts')}`
  if (etape.titre === 'manigance' || etape.titre === 'menace') return texteMenaces(etape.montant)
  return undefined
}

/**
 * Les recherches d'une carte révélée (13/10/2026, encadré ⑫) : « Recherche :
 * rien trouvé » ou « Défaussé : A » puis « Trouvé : X », puis « Paquet rencontre mélangé » si le
 * paquet a été fouillé. Rien d'inventé : tout vient du fait du moteur.
 */
export function textesRecherches(recherches: EtapeDeroule['recherches']): string[] {
  const lignes: string[] = []
  for (const recherche of recherches ?? []) {
    // « Défausser jusqu'à trouver » (Piller l'Armurerie, rapport BL-Stark n°102) : ce qui a été défaussé en chemin, avant ce qui est trouvé.
    if (recherche.defausse && recherche.defausse.length > 0) {
      lignes.push(t('Défaussé : %1').replace('%1', recherche.defausse.map((nom) => nomNettoye(nom) ?? nom).join(', ')))
    }
    lignes.push(
      recherche.trouve.length === 0
        ? t('Recherche : rien trouvé')
        : t('Trouvé : %1').replace('%1', recherche.trouve.map((nom) => nomNettoye(nom) ?? nom).join(', '))
    )
    if (recherche.paquet) lignes.push(t('Paquet rencontre mélangé'))
  }
  return lignes
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
  // 13/10/2026 (encadré ⑫) : ce qu'une recherche a donné, trouvé ou non, après le texte.
  lignes.push(...textesRecherches(etape.recherches))
  const sorties = sortiesDeLEtape(ctx.etapes, etape)
  if (etape.reveleePar) lignes.unshift(...sorties)
  else lignes.push(...sorties)

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

  const position = ctx.etapes.findIndex((autre) => autre.cle === etape.cle)
  const suivanteRemplacement = position === -1 ? undefined : remplacementDe(ctx.etapes, position)
  const remplacement = suivanteRemplacement
    ? vignette(`remplacement:${suivanteRemplacement.cle}`, suivanteRemplacement.carteId, nomDe(suivanteRemplacement, ctx), ctx)
    : undefined

  const typeFr = typeFrDe(etape.typeCarte, carte.scan?.kind)
  return {
    genre: 'revelee',
    carte,
    typeFr,
    etiquettes: etiquettesDeLaCarte(etape, typeFr, infoCarteRevelee, jauge, etape.carteId !== undefined ? ctx.infoCarte?.(etape.carteId) : undefined),
    lignes,
    jauge,
    renfort,
    renfortInconnu,
    surtitreRenfort: surtitreEtape(etape) || undefined,
    remplacement,
    lienRemplacement: suivanteRemplacement ? surtitreEtape(suivanteRemplacement) || undefined : undefined,
    chaine: position === -1 ? undefined : chaineDe(ctx.etapes, position, ctx),
  }
}

/**
 * LES ETIQUETTES DE LA CARTE REVELEE (essai du 10/10/2026, questions 26, 28 et
 * 45) : ce qui doit sauter aux yeux avant meme de lire la carte.
 */
function etiquettesDeLaCarte(
  etape: EtapeDeroule,
  typeFr: string | undefined,
  info: InfoRevelee | undefined,
  jauge: Jauge | undefined,
  nombres?: Partial<Record<string, number>>
): string[] | undefined {
  const etiquettes: string[] = []
  const genre = etape.typeCarte ?? ''
  if (/obligation/i.test(genre) || typeFr === t('Obligation')) etiquettes.push(t('Ton obligation'))
  if (/sidescheme/i.test(genre) || typeFr === t('Manigance annexe')) {
    const menace = jauge?.apres
    etiquettes.push(
      nombre(menace) ? t('Nouvelle manigance : %1').replace('%1', texteMenaces(menace).replace(/^\+/, '')) : t('Nouvelle manigance')
    )
  }
  if ((info?.texteImprime ?? []).some((ligne) => /\bp[ée]ril\b/i.test(ligne))) etiquettes.push(t('Péril : décide seul'))
  // LOT 5 (decision 9) : les icones de la carte, expliquees en une ligne chacune.
  const icone = (cle: string) => (nombres && nombre(nombres[cle]) ? (nombres[cle] as number) : 0)
  if (icone('crisis') > 0) etiquettes.push(t('Crise : plus de menace retirée de la manigance principale'))
  if (icone('acceleration_icon') > 0) etiquettes.push(t('Accélération : +%1 menace à chaque étape 1').replace('%1', String(icone('acceleration_icon'))))
  if (icone('hazard') > 0) etiquettes.push(t('Danger : +%1 carte rencontre à chaque distribution').replace('%1', String(icone('hazard'))))
  if (icone('incite') > 0) etiquettes.push(t('Incite %1 : +%1 menace sur la manigance principale').split('%1').join(String(icone('incite'))))
  return etiquettes.length > 0 ? etiquettes : undefined
}

/**
 * UN ETAT CRITIQUE (essai du 10/10/2026, question 44) : un heros a 3 PV ou
 * moins (ou au quart de ses PV), une manigance a un pas de son seuil.
 */
export function jaugeCritique(jauge: Jauge | undefined, genre: 'pv' | 'menace'): boolean {
  if (!jauge || !nombre(jauge.apres)) return false
  if (genre === 'pv') {
    if (jauge.apres <= 0) return false
    return jauge.apres <= 3 || (nombre(jauge.plafond) && jauge.apres <= jauge.plafond / 4)
  }
  return nombre(jauge.plafond) && jauge.plafond > 0 && jauge.apres >= jauge.plafond * 0.75
}

/**
 * « Carte 3 / 3 · +1 Renfort (Weapons Runner) » (essai du 10/10/2026, question
 * 22) : la place de la carte revelee parmi celles de la phase, et ce qui en a
 * ajoute en route. Rien hors d'une revelation.
 */
export function compteurDesRevelations(
  etapes: EtapeDeroule[],
  cle: string,
  cartesDistribuees: number
): { rang: number; total: number; ajouts: string[] } | undefined {
  const revelations = etapes.filter((e) => e.titre === 'revelation' && !e.horsPhase)
  const rang = revelations.findIndex((e) => e.cle === cle)
  if (rang === -1) return undefined
  const ajouts = revelations
    .filter((e) => e.parSurge || e.reveleePar)
    .map((e) =>
      e.reveleePar
        ? `+1 ${nomNettoye(e.reveleePar) ?? e.reveleePar}`
        : `+1 ${t('Renfort')}${e.renfortDe ? ` (${e.renfortDe})` : ''}`
    )
  const total = Math.max(revelations.length, cartesDistribuees + ajouts.length)
  return { rang: rang + 1, total, ajouts }
}

/**
 * L'etape 3 dite par joueur (essai, demande de l'utilisateur du 13/10/2026) :
 * « Carte rencontre 2/2 · Captain America ». Le rang et le total comptent les
 * cartes de CE joueur (son choix), le nom est son heros ou son alter ego.
 * Le total prend ce qu'il a recu a la distribution, plus les Renforts et les
 * cartes revelees en remplacement : il est connu des sa premiere carte.
 */
export function rencontreDuJoueur(
  etapes: EtapeDeroule[],
  cle: string
): { rang: number; total: number; nom?: string } | undefined {
  const revelations = etapes.filter((e) => e.titre === 'revelation' && !e.horsPhase)
  const etape = revelations.find((e) => e.cle === cle)
  if (!etape) return undefined
  const duJoueur = revelations.filter((e) => e.joueur === etape.joueur)
  let distribuees = 0
  let enTableau = 0
  for (const e of etapes) {
    if (e.titre === 'distribution' && e.joueur === etape.joueur) distribuees += e.montant ?? 1
    for (const ligne of e.lignesDistribution ?? []) if (ligne.joueur === etape.joueur) enTableau += ligne.cartes
  }
  const ajouts = duJoueur.filter((e) => e.parSurge || e.reveleePar).length
  return {
    rang: duJoueur.findIndex((e) => e.cle === cle) + 1,
    total: Math.max(duJoueur.length, Math.max(distribuees, enTableau) + ajouts),
    nom: nomNettoye(etape.auteurNom),
  }
}

/**
 * « Stepford Cuckoos : défaussée » (n72) : sur la carte annulee, et aussi sur sa
 * remplacante. Le panneau retient le moteur jusqu'au « Suivant » : l'annulation
 * n'arrive a l'ecran qu'avec la carte de remplacement.
 */
export function sortiesDeLEtape(etapes: EtapeDeroule[], etape: EtapeDeroule): string[] {
  const propre = texteSortieAnnulation(etape)
  if (propre) return [propre]
  const rang = etapes.findIndex((autre) => autre.cle === etape.cle)
  if (!etape.reveleePar || rang === -1) return []
  const annulee = precedenteAnnuleePar(etapes, rang, etapes[rang])
  const sortie = annulee ? texteSortieAnnulation(annulee) : ''
  return sortie ? [sortie] : []
}

function nomDe(etape: EtapeDeroule, ctx: ContexteVue): string | undefined {
  return (etape.carteId !== undefined ? ctx.nomFr?.(etape.carteId) : undefined) ?? etape.cibleNom
}

/** La revelation qui REMPLACE celle du rang donne (`reveleePar`), si elle existe. */
function remplacementDe(etapes: EtapeDeroule[], rang: number): EtapeDeroule | undefined {
  if (!etapes[rang]?.annuleePar) return undefined
  for (let apres = rang + 1; apres < etapes.length; apres++) {
    const suivante = etapes[apres]
    if (suivante.titre === 'revelation' && suivante.reveleePar && precedenteAnnuleePar(etapes, apres, suivante) === etapes[rang]) {
      return suivante
    }
  }
  return undefined
}

/** La revelation que suit celle du rang donne par Renfort (`relierLesRenforts`). */
function renfortDe(etapes: EtapeDeroule[], rang: number): EtapeDeroule | undefined {
  if (!etapes[rang]?.suivieDUnRenfort) return undefined
  return etapes.slice(rang + 1).find((autre) => autre.titre === 'revelation' && autre.parSurge)
}

/** La revelation dont celle du rang donne est la suite (Renfort ou remplacement). */
function maillonPrecedent(etapes: EtapeDeroule[], rang: number): number {
  const etape = etapes[rang]
  if (etape.titre !== 'revelation') return -1
  if (etape.reveleePar) {
    const annulee = precedenteAnnuleePar(etapes, rang, etape)
    return annulee ? etapes.indexOf(annulee) : -1
  }
  if (!etape.parSurge) return -1
  for (let avant = rang - 1; avant >= 0; avant--) {
    const precedente = etapes[avant]
    if (precedente.titre !== 'revelation') continue
    return renfortDe(etapes, avant) === etape ? avant : -1
  }
  return -1
}

function maillonSuivant(etapes: EtapeDeroule[], rang: number): number {
  const suivante = remplacementDe(etapes, rang) ?? renfortDe(etapes, rang)
  return suivante ? etapes.indexOf(suivante) : -1
}

/**
 * LA CHAINE EN DIRECT (rapport Yarro n72, 09/10/2026) : la carte et celles
 * qu'elle a amenees ou qui l'ont amenee, une vignette chacune. Une carte
 * seule, ou un Renfort simple a deux cartes, n'a pas de chaine.
 */
function chaineDe(etapes: EtapeDeroule[], rang: number, ctx: ContexteVue): MaillonChaine[] | undefined {
  const rangs = rangsDeLaChaine(etapes, rang)
  if (!rangs) return undefined
  return rangs.map((r, i) => {
    const maillon = etapes[r]
    return {
      vignette: vignette(`chaine:${maillon.cle}`, maillon.carteId, nomDe(maillon, ctx), ctx),
      lien: i === 0 ? undefined : lienDuMaillon(maillon),
      annulee: annuleeDuMaillon(maillon),
      annuleePar:
        maillon.annuleePar && maillon.annuleeParId !== undefined
          ? vignette(`annuleur:${maillon.cle}`, maillon.annuleeParId, nomNettoye(maillon.annuleePar), ctx)
          : undefined,
      courante: r === rang,
    }
  })
}

function lienDuMaillon(maillon: EtapeDeroule): string | undefined {
  return (maillon.reveleePar ? surtitreEtape(maillon) : t('Renfort')) || undefined
}

function annuleeDuMaillon(maillon: EtapeDeroule): string | undefined {
  return maillon.annuleePar
    ? t('Annulée par %1').replace('%1', nomNettoye(maillon.annuleePar) ?? maillon.annuleePar)
    : undefined
}

/**
 * La chaine en une ligne, pour l'ancien rendu du telephone (D36) : « Weapons
 * Runner → Renfort → Klaw's Vengeance (Annulée par Stepford Cuckoos) →
 * Révélée par Stepford Cuckoos → Sonic Boom ». Vide sans chaine.
 */
export function texteDeLaChaine(etapes: EtapeDeroule[], cle: string, nom: (etape: EtapeDeroule) => string | undefined): string {
  const rang = etapes.findIndex((autre) => autre.cle === cle)
  const rangs = rang === -1 ? undefined : rangsDeLaChaine(etapes, rang)
  if (!rangs) return ''
  return rangs
    .map((r, i) => {
      const maillon = etapes[r]
      const annulee = annuleeDuMaillon(maillon)
      const carte = `${nom(maillon) ?? maillon.cibleNom ?? '?'}${annulee ? ` (${annulee})` : ''}`
      return i === 0 ? carte : `→ ${lienDuMaillon(maillon) ?? ''} → ${carte}`
    })
    .join(' ')
}

/** Les rangs de la chaine dont la carte du rang donne fait partie, dans l'ordre. */
function rangsDeLaChaine(etapes: EtapeDeroule[], rang: number): number[] | undefined {
  let debut = rang
  for (let garde = 0; garde < etapes.length; garde++) {
    const precedent = maillonPrecedent(etapes, debut)
    if (precedent === -1 || precedent >= debut) break
    debut = precedent
  }
  const rangs: number[] = [debut]
  for (let garde = 0; garde < etapes.length; garde++) {
    const suivant = maillonSuivant(etapes, rangs[rangs.length - 1])
    if (suivant === -1 || rangs.includes(suivant)) break
    rangs.push(suivant)
  }
  // Un Renfort simple (deux cartes) se dit deja par la fleche a droite.
  const avecRemplacement = rangs.some((r) => etapes[r].annuleePar || etapes[r].reveleePar)
  if (rangs.length < 2 || (rangs.length < 3 && !avecRemplacement)) return undefined
  return rangs
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
    suite:
      etape.stade === 'mechant'
        ? t('Le méchant continue avec ce nouveau stade. La phase continue.')
        : t('La nouvelle manigance entre en jeu avec sa menace de départ. La phase continue.'),
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
    case 'riposte':
      return vueRiposte(etape, ctx)
    case 'etoile-differe':
      return vueEtoileDifferee(etape, ctx)
    case 'elimination':
      return {
        genre: 'rangee',
        acteur: { ...vignette(`elimine:${etape.cle}`, etape.carteId, etape.cibleNom, ctx), legende: t('ÉLIMINÉ') },
        boosts: [],
        cibles: [],
        // 13/10/2026 (encadré ⑧, Rules Reference « PLAYER ELIMINATION ») : il gagne ou perd avec le groupe.
        resultat: { texte: t('Ses sbires passent au joueur suivant. La phase continue.'), note: t('Il reste dans la partie : il gagne ou perd avec son équipe.') },
        lignesEtoile: [],
        grisee: false,
        elimine: true,
      }
    case 'distribution-tableau':
      return vueDistribution(etape)
    case 'menace':
      return vueMenace(etape, ctx)
    case 'revelation':
    case 'stade-revele':
      return vueRevelee(etape, ctx)
    case 'sonne':
      return vueSonne(etape, ctx)
    case 'stade':
      return vueStade(etape, ctx)
    case 'paquet-vide':
      // 13/10/2026 (encadré ②) : la manigance qui reçoit le jeton, et ce que ça change.
      return {
        genre: 'rangee',
        acteur: vignette(`acteur:${etape.cle}`, etape.cibleId, etape.cibleNom, ctx),
        boosts: [],
        cibles: [],
        resultat: {
          texte: t('Défausse remélangée : un nouveau paquet'),
          note: t('+1 jeton d’accélération : +1 menace à chaque étape 1'),
        },
        lignesEtoile: [],
        grisee: false,
      }
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
        entree: { sbire: true },
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

  // LOT 5 (decision 12) : la liste courte, une ligne par etape racontee.
  const evenements = etapes
    .filter((etape) => etape.titre !== 'vide' && etape.temps !== 'bilan')
    .map((etape) => ({
      cle: etape.cle,
      texte: [titreCourt(etape, ctx), resultatCourt(etape)].filter(Boolean).join(' · '),
      carteId: etape.carteId ?? etape.cibleId,
    }))
  return {
    evenements: evenements.length > 0 ? evenements : undefined,
    genre: 'bilan',
    menace: colonnesMenace,
    heros: colonnesHeros,
    nouveautes,
    vide: colonnesMenace.length === 0 && colonnesHeros.length === 0 && nouveautes.length === 0,
  }
}
