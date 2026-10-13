// LE CARTOUCHE DU BAS DE LA PHASE DU MECHANT (refonte du 04/10/2026, scene PC,
// mode « Étape par étape »). Decisions : `.planning/todos/2026-10-04-refonte-
// phase-mechant-decisions.md` (D1 a D43).
//
// La PRESENTATION seule. `DeroulePhase` reste le controleur : il tient l'index,
// la validation, l'attente et l'accuse de reception, et passe ici ce qu'il a
// decide. Ce composant ne fait que DESSINER l'etape (le modele de vue est dans
// `vue-cartouche.ts`, pur) et rappeler `avancer` au clic.
//
// Un gabarit unique, de la meme hauteur pour tous les etats (D1, D33, D34) :
//  - la ligne du haut (28 px) : cinq pastilles, le titre court en Bangers, le
//    numero de page ; elle sert de poignee pour deplacer le cartouche (D2) ;
//  - le corps : la rangee (acteur, boosts colles, total, defenseur, cible,
//    resultat), la carte revelee en grand, le stade, ou le bilan ;
//  - le pied : « Suivant (espace) », « Terminer », « Continuer », et les
//    mentions qui disent pourquoi rien ne se passe.
// Ce qui ne tient pas passe a la page suivante (D41) : jamais de defilement.
//
// ⚠ LA TABLE ET LE TELEPHONE NE PASSENT JAMAIS ICI (D21, D36) : ils gardent le
// rendu d'avant, dans DeroulePhase.
//
// Le meme gabarit sert trois fois (lot 5) :
//  - la phase, ou une pastille passee se relit sur place (D22, D23) ;
//  - « Pendant ton tour » (`CartoucheHorsPhase`, D26) : un coup du mechant
//    pendant le tour du joueur, defense comprise, ou une carte revelee ;
//  - la relecture depuis le journal (`RelectureJournal`, D38).

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
  type CSSProperties,
  type MouseEvent as ReactMouseEvent,
  type PointerEvent as ReactPointerEvent,
  type ReactNode,
} from 'react'
import type { ScanCardProps } from '../components/ScanCard'
import { useApercuSurvol } from './apercu-survol'
import { CarteApercu } from './Board'
import { avecBilan, nomNettoye, precedenteAnnuleePar, type EtapeDeroule, type TempsPhase } from './deroule-phase'
import { estSpectateur } from './moteur'
import {
  texteArretDefaite,
  texteAttente,
  texteBilanVide,
  texteDefaite,
  texteFenetreReponse,
  texteFiletProche,
  texteTempsParDecision,
  titreEtape,
} from './deroule-textes'
import { etapeEnLangue } from './etape-en-langue'
import { avecTempsVides, fusionnerDistribution } from './frise-phase'
import { t } from './langue'
import { useGlisserPanneau } from './placement/useGlisserPanneau'
import type { CadreDeLEtape } from './couleur-joueur'
import { vueSousCadre, type QuestionDuMoteur, type VueSousCadre } from './sous-cadre'
import { BoutonOption, CarteNue, choixEnTexte, optionDe, SousCadre } from './SousCadre'
import { avecIcones, marquerRessources } from './icones-ressources'
import { NomsSurvolables, Texte, nomsMontrables, type NomDeCarte } from './noms-survolables'
import { ajusterLesCartes, deborde, hauteurPosee } from './essai-tailles'
import {
  compteurDesRevelations,
  rencontreDuJoueur,
  herosViseDe,
  jaugeCritique,
  PASTILLES,
  pastilleDuTemps,
  pastilles,
  tempsAfficheDe,
  titreCourt,
  vueDeLEtape,
  type ClePastille,
  type ColonneJauge,
  type ContexteVue,
  type InfoRevelee,
  type Jauge,
  type MaillonChaine,
  type Pastille,
  type Vignette,
  type VueBilan,
  type VueCorps,
  type VueRangee,
  type VueRevelee,
  type VueDistribution,
  type VueStade,
} from './vue-cartouche'
import './cartouche-phase.css'
import './cartouche-essai.css'
import './cartouche-phase-bis.css'

/** Les gestionnaires de `useGlisserPanneau`, poses sur la ligne du haut. */
export type GestesDeplacer = {
  onPointerDown: (evenement: ReactPointerEvent<HTMLElement>) => void
  onPointerMove: (evenement: ReactPointerEvent<HTMLElement>) => void
  onPointerUp: (evenement: ReactPointerEvent<HTMLElement>) => void
  onPointerCancel: () => void
}

/**
 * Refonte, lot 6 (essai, MULTI) : le pied de la boite quand ce joueur ne donne
 * pas seul le rythme. `choix-hote` : l'hote choisit qui fait avancer (premiere
 * phase) ; `attente-choix` : les autres l'attendent ; `regarde` : un autre joueur
 * donne le rythme, ce joueur voit le meme ecran sans bouton ; `pret` : chacun se
 * dit pret, on avance ensemble.
 */
export type PiedMulti =
  | { genre: 'choix-hote'; choisir: (politique: 'concerne' | 'tous' | 'quiconque') => void }
  | { genre: 'attente-choix' }
  | { genre: 'regarde'; nom: string }
  | {
      genre: 'pret'
      pret: boolean
      pastilles: Array<{ nom: string; couleur?: string; pret: boolean }>
      marquer: () => void
    }

export type CartouchePhaseProps = {
  /** `setElCartouche` du controleur : la section a mesurer. */
  refCartouche: (el: HTMLElement | null) => void
  /** Le decalage pose a la main (`translate`), ou rien. */
  style?: CSSProperties
  gestes: GestesDeplacer
  /** L'etape que le controleur montre ; absente avant la premiere. */
  etape?: EtapeDeroule
  /** Les etapes affichees (brutes, noms du moteur), bilan compris. */
  etapes: EtapeDeroule[]
  index: number
  /**
   * Le cartouche a rendu la main (`termine`) ou la partie est finie : il ne
   * dessine plus rien, meme devant une question.
   */
  efface: boolean
  questionAuJoueur: boolean
  /**
   * La question STRUCTUREE (scene PC, lot 4) : la defense et le choix d'une
   * carte revelee se jouent dans la rangee, le reste dans le sous-cadre.
   */
  questionDuMoteur?: QuestionDuMoteur
  /**
   * La question rendue par le plateau (DemandeCentrale, CiblesScene) quand
   * aucune question structuree n'est donnee : la table, le telephone, la page
   * d'etat, le banc d'essai. Logee dans `.deroule-sous-cadre.est-provisoire`.
   */
  question?: ReactNode
  /**
   * La question posee a un AUTRE siege (D28), en LECTURE SEULE : des
   * identifiants et des noms, aucun gestionnaire. Un bouton actif repondrait
   * a sa place.
   */
  questionDUnAutre?: {
    options: Array<{ id: number; bindId: number; nom: string }>
  }
  tempsQuestion?: TempsPhase
  avancer: () => void
  /** Lot 6 (essai, multi) : le pied quand ce joueur ne donne pas seul le rythme. */
  multi?: PiedMulti
  enAttente: boolean
  attendUnAutreJoueur: boolean
  nomJoueurAttendu?: string
  secondesFilet?: number
  defaiteLocale: boolean
  boostsMontres: number
  tempsParDecision: number
  pvMaxParNom?: Map<string, number>
  carteScene?: (id: number, faceVisible: boolean) => ScanCardProps | undefined
  nomFr?: (id: number) => string | undefined
  texteEtoile?: (carteId: number) => string | undefined
  infoCarte?: (id: number) => Partial<Record<string, number>> | undefined
  infoRevelee?: (carteId: number) => InfoRevelee | undefined
  /** Les cartes rencontre distribuees, retirees de la liste (D15). */
  cartesDistribuees: number
  herosLocauxIds?: ReadonlySet<number>
  herosDesAutresIds?: ReadonlySet<number>
  /**
   * La pastille RELUE (D22, D23), en lecture seule : sa rangee remplace celle
   * de l'etape en cours, qui reste marquee « en cours » dans la frise. Ignoree
   * pendant une question : elle ne doit jamais la cacher.
   */
  relecture?: { temps: ClePastille }
  /** Relire une pastille passee ; `undefined` revient a l'etape en cours. */
  setRelecture?: (relecture: { temps: ClePastille } | undefined) => void
  /**
   * Ce que le cartouche raconte : la phase (defaut) ; un coup du mechant
   * pendant le tour du joueur (D26, bandeau a la place des pastilles) ; la
   * phase precedente rouverte depuis le journal (D38, « Fermer »).
   */
  bandeau?: 'phase' | 'pendant-ton-tour' | 'relecture-journal'
  /** « Fermer » de la relecture depuis le journal. */
  onFermer?: () => void
  /**
   * L'essai « Nouvelle phase du méchant » (10/10/2026) : calcul pose entre les
   * vignettes, tampon « ANNULÉE », etiquettes, compteur de cartes, « Réduire »
   * et « Continuer ». Faux : le rendu d'avant, a l'octet pres.
   */
  essai?: boolean
  /** Presentation « Étape par étape » (l'ancien Bis, seule depuis le
   *  10/10/2026). Vraie par defaut ; faux pour le cartouche pose sur la table. */
  bis?: boolean
  /** Essai : retourner le boost suivant (ils ne s'enchainent plus seuls). */
  montrerBoostSuivant?: () => void
  /**
   * Essai (13/10/2026, encadré ⑫) : la carte révélée arrive face cachée ; le
   * premier clic la retourne (`retournerCarte`), le suivant passe à la suite.
   */
  carteCachee?: boolean
  retournerCarte?: () => void
  /** Essai (13/10/2026) : la couleur de chaque joueur à la table, dans l'ordre des sièges. */
  couleursJoueurs?: readonly string[]
  /**
   * Essai (refonte du 12/10/2026) : le joueur concerne par l'etape, dont la
   * couleur d'aspect fait le bord de la boite (variables posees dans `style`
   * par DeroulePhase), ou « commun » (gris acier).
   */
  cadre?: CadreDeLEtape
  /** Essai, lot 5c (decision 47) : la couleur du joueur a qui appartient une carte (ordre des activations). */
  couleurDeCarte?: (carteId: number) => string | undefined
}

/**
 * LA COLONNE DE GAUCHE (essai, decisions 26 bis et 27) : sur PC, tant que la
 * boite est affichee, la table se decale a droite d'autant
 * (`body.phase-essai-colonne`, cartouche-essai.css). La table se recalcule
 * d'elle-meme (ResizeObserver de Board.tsx) : rien n'est jamais couvert, la
 * main comprise. Le telephone garde sa feuille basse.
 */
function useColonneEssai(actif: boolean) {
  useEffect(() => {
    if (!actif || typeof window.matchMedia !== 'function' || !window.matchMedia('(min-width: 768px)').matches) return
    document.body.classList.add('phase-essai-colonne')
    // Le haut de la colonne : le haut de la table, sous la barre (qui peut
    // passer sur deux lignes en fenetre etroite).
    const caler = () => {
      const haut = document.querySelector('.plateau-cadre')?.getBoundingClientRect().top
      if (haut !== undefined) document.documentElement.style.setProperty('--colonne-haut', `${Math.round(haut)}px`)
    }
    caler()
    window.addEventListener('resize', caler)
    return () => {
      window.removeEventListener('resize', caler)
      document.body.classList.remove('phase-essai-colonne')
      document.documentElement.style.removeProperty('--colonne-haut')
    }
  }, [actif])
}

/** Les temps internes qu'une pastille dessine (④ en couvre deux). */
function tempsDeLaPastille(cle: ClePastille): ReadonlyArray<TempsPhase> {
  return PASTILLES.find((pastille) => pastille.cle === cle)?.temps ?? []
}

/** Une page lue : l'etape (brute), la meme en langue, et ce qu'elle dessine. */
type PageLue = { etape: EtapeDeroule; lue: EtapeDeroule; corps: VueCorps }

/** « 10 → 7 / 14 » ; un morceau absent se tait (rien d'invente, piege 40). */
function texteJauge(jauge: Jauge | undefined): string {
  if (!jauge || jauge.apres === undefined) return ''
  const debut = jauge.avant !== undefined && jauge.avant !== jauge.apres ? `${jauge.avant} → ` : ''
  return `${debut}${jauge.apres}${jauge.plafond !== undefined ? ` / ${jauge.plafond}` : ''}`
}

function VignetteVue({ vignette, grande = false }: { vignette: Vignette; grande?: boolean }) {
  const classes = ['deroule-vignette']
  if (grande) classes.push('deroule-carte-grande')
  if (vignette.etat === 'grisee') classes.push('est-grisee')
  if (vignette.scan && vignette.jauge) classes.push('a-jauge')
  return (
    <figure className={classes.join(' ')} title={vignette.nom || undefined}>
      {vignette.scan ? (
        <CarteNue scan={vignette.scan} jauge={vignette.jauge} />
      ) : (
        <span className="deroule-vignette-nom">{vignette.nom}</span>
      )}
      {vignette.scan && vignette.recap ? <small className="deroule-recap">{vignette.recap}</small> : null}
      {vignette.legende ? <figcaption className="deroule-legende"><Texte>{vignette.legende}</Texte></figcaption> : null}
    </figure>
  )
}

function Rangee({
  rangee,
  grisee,
  choix,
  fin,
  attente = false,
  nbChoix = 0,
}: {
  rangee: VueRangee
  grisee: boolean
  /** Les choix de la question posee DANS la rangee (D7, D8), a la suite. */
  choix?: ReactNode
  /** Ce qui ferme la rangee : « Black Panther choisit… » (D28). */
  fin?: ReactNode
  attente?: boolean
  /** Le nombre de cartes que `choix` pose (la taille des vignettes en depend). */
  nbChoix?: number
}) {
  const jauge = texteJauge(rangee.resultat?.jauge)
  const classes = ['deroule-rangee']
  if (rangee.annulee) classes.push('est-annulee')
  if (grisee) classes.push('est-grisee')
  if (attente) classes.push('est-attente')
  const vise = rangee.defenseur !== undefined || rangee.cibles.length > 0
  return (
    <div
      className={classes.join(' ')}
      aria-hidden={grisee || undefined}
      style={{ '--nb-cartes': Math.max(1, nombreDeCartes(rangee) + nbChoix), '--poids-cartes': poidsDesCartes(rangee, nbChoix) } as CSSProperties}
    >
      <div className="deroule-rangee-cartes">
        {rangee.acteur ? <VignetteVue vignette={rangee.acteur} /> : null}
        {rangee.boosts.map((boost) => (
          <VignetteVue key={boost.cle} vignette={boost} />
        ))}
        {rangee.total ? (
          <span className={rangee.total.gros ? 'deroule-total est-gros' : 'deroule-total'}>{rangee.total.texte}</span>
        ) : null}
        {rangee.calcul ? <span className="deroule-calcul">{rangee.calcul}</span> : null}
        {vise ? (
          <span className="deroule-vers" aria-hidden="true">
            →
          </span>
        ) : null}
        {rangee.defenseur ? <VignetteVue vignette={rangee.defenseur} /> : null}
        {rangee.cibles.map((cible) => (
          <VignetteVue key={cible.cle} vignette={cible} />
        ))}
        {choix}
        {rangee.resultat ? (
          <span className="deroule-resultat-gros">
            <strong className="deroule-resultat-texte"><Texte>{rangee.resultat.texte}</Texte></strong>
            {jauge ? <span className="deroule-jauge">{jauge}</span> : null}
            {rangee.resultat.note ? <small className="deroule-resultat-note"><Texte>{rangee.resultat.note}</Texte></small> : null}
          </span>
        ) : null}
        {rangee.annulee ? (
          <strong className="deroule-annulee-cause">
            <Texte>{rangee.annulee.cause ? `${t('Annulée')} · ${rangee.annulee.cause}` : t('Annulée')}</Texte>
          </strong>
        ) : null}
        {fin}
      </div>
      {rangee.lignesEtoile.map((ligne) => (
        <p key={ligne} className="deroule-etoile">
          <Texte>{ligne}</Texte>
        </p>
      ))}
    </div>
  )
}

/** Les cartes qu'une rangee pose cote a cote (la taille des vignettes en depend). */
/** La largeur de la rangée en « cartes portrait » : un complot (paysage) pèse 176/127. */
function poidsDesCartes(rangee: VueRangee, nbChoix = 0): number {
  const vignettes = [
    ...(rangee.acteur ? [rangee.acteur] : []),
    ...rangee.boosts,
    ...(rangee.defenseur ? [rangee.defenseur] : rangee.cibles),
  ]
  const poids = vignettes.reduce((somme, v) => somme + (v.scan?.isLandscape ? 176 / 127 : 1), 0)
  return Math.max(1, poids + nbChoix)
}

function nombreDeCartes(rangee: VueRangee): number {
  return (
    (rangee.acteur ? 1 : 0) + rangee.boosts.length + (rangee.defenseur ? 1 : 0) + (rangee.defenseur ? 0 : rangee.cibles.length)
  )
}

/**
 * LE PICTO D'UNE CARACTERISTIQUE (essai, decisions du 10/10/2026) : ATQ et MEN
 * de l'acteur, DEF du defenseur, le chiffre en grand dedans. Les couleurs sont
 * celles des cartes : rouge pour l'attaque, bleu pour la manigance, vert pour
 * la defense.
 */
export function PictoStat({ genre, valeur }: { genre: 'atq' | 'men' | 'def'; valeur: number | undefined }) {
  if (valeur === undefined) return null
  const sigle = genre === 'atq' ? t('ATQ') : genre === 'men' ? t('MEN') : t('DÉF')
  return (
    <span className={`essai-stat est-${genre}`} role="img" aria-label={`${sigle} ${valeur}`}>
      <b>{valeur}</b>
      <small>{sigle}</small>
    </span>
  )
}

/** La pastille d'un boost, de la forme de « 2 MEN » : « +1 BOOST », « +0 BOOST ★ ». */
export function PictoBoost({ nombre, etoile = false, stat }: { nombre: number; etoile?: boolean; stat?: 'atq' | 'men' }) {
  const valeur = `${nombre < 0 ? '−' : '+'}${Math.abs(nombre)}`
  // LOT 5 (decision 36) : « +2 ATQ » plutot que « +2 BOOST » : ce que le boost ajoute.
  const base = stat === 'atq' ? t('ATQ') : stat === 'men' ? t('MEN') : t('BOOST')
  const sigle = `${base}${etoile ? ' ★' : ''}`
  return (
    // 13/10/2026 : un boost a 0 (sans ★) se dit en gris, il n'a rien apporte.
    <span className={`essai-stat est-boost${nombre === 0 && !etoile ? ' est-nul' : ''}`} role="img" aria-label={`${valeur} ${sigle}`}>
      <b>{valeur}</b>
      <small>{sigle}</small>
    </span>
  )
}

/** Le resultat (« 2 dégâts subis », jauge avant → apres), sous la carte qui le subit. */
function ResultatEssai({ rangee }: { rangee: VueRangee }) {
  const pose = rangee.pose
  if (rangee.resultat) {
    const jauge = texteJauge(rangee.resultat.jauge)
    const critique = pose ? jaugeCritique(rangee.resultat.jauge, pose.jauge) : false
    return (
      <span className={`essai-boite${critique ? ' est-critique' : ''}`}>
        {rangee.resultat.tampon ? (
          <span className={`essai-tampon essai-tampon-${rangee.resultat.tampon === 'K.O.' ? 'ko' : 'vaincu'}`}>{t(rangee.resultat.tampon)}</span>
        ) : null}
        <strong className={`deroule-resultat-texte${rangee.resultat.nul ? ' est-nul' : ''}`}>
          {rangee.resultat.barre ? (
            <>
              <s className="essai-barre">{rangee.resultat.barre}</s>
              {' → '}
            </>
          ) : null}
          <Texte>{rangee.resultat.texte}</Texte>
        </strong>
        {rangee.resultat.raison ? <small className="essai-raison">{rangee.resultat.raison}</small> : null}
        {jauge ? <span className="deroule-jauge">{jauge}</span> : null}
        {rangee.resultat.note ? <small className="deroule-resultat-note"><Texte>{rangee.resultat.note}</Texte></small> : null}
        {pose?.jauge === 'menace' ? <AlerteSeuil jauge={rangee.resultat.jauge} /> : null}
      </span>
    )
  }
  if (rangee.total)
    return (
      <span className="essai-boite">
        <strong className="deroule-resultat-texte">{rangee.total.texte}</strong>
      </span>
    )
  return null
}

/**
 * LE CALCUL POSE DE L'ESSAI (decisions du 10/10/2026) : sous l'acteur le picto
 * de la caracteristique utilisee (ATQ ou MEN), sous chaque boost ses icones,
 * sous le defenseur son picto DEF ; le resultat sous la carte qui le subit.
 * Le calcul se lit sans un mot : [ATQ] + [boosts] − [DEF].
 */
function RangeeEssai({ rangee, grisee, encadre = false }: { rangee: VueRangee; grisee: boolean; encadre?: boolean }) {
  const pose = rangee.pose
  const classes = ['deroule-rangee', 'essai-calcul']
  if (rangee.annulee) classes.push('est-annulee')
  if (rangee.riposte) classes.push('est-riposte')
  if (grisee) classes.push('est-grisee')
  // La legende (« ATQ 1 », « +0 ★ ») ferait doublon avec les pictos.
  const nue = (vignette: Vignette): Vignette => ({ ...vignette, legende: undefined })
  const operateur = (signe: string) => (
    <span className="essai-operateur" aria-hidden="true">
      {signe}
    </span>
  )
  // Une ligne « ★ » par boost etoile, dans l'ordre : chacune sous SON boost.
  const etoiles = [...rangee.lignesEtoile]
  const statActeur = pose?.jauge === 'menace' ? 'men' : 'atq'
  const resultat = <ResultatEssai rangee={rangee} />
  const cible = rangee.defenseur ?? (rangee.cibles.length === 1 ? rangee.cibles[0] : undefined)
  return (
    <div
      className={classes.join(' ')}
      aria-hidden={grisee || undefined}
      style={{ '--nb-cartes': Math.max(1, nombreDeCartes(rangee)), '--poids-cartes': poidsDesCartes(rangee) } as CSSProperties}
    >
      {rangee.riposte ? (
        // LOT 5b (decision 39) : la Riposte, son ecran a part, la fleche part de la carte touchee.
        <span className="essai-tampon-riposte">{t('RIPOSTE')}</span>
      ) : null}
      <div className="deroule-rangee-cartes">
        {rangee.acteur ? (
          <span className="essai-terme">
            <VignetteVue vignette={nue(rangee.acteur)} />
            <PictoStat genre={statActeur} valeur={pose?.base} />
          </span>
        ) : null}
        {rangee.boosts.map((boost) => {
          const ligne = boost.etoile ? etoiles.shift() : undefined
          return (
            <span key={boost.cle} className="essai-groupe">
              {operateur('+')}
              <span className={`essai-terme${boost.apport === 0 && !boost.etoile ? ' est-nul' : ''}`}>
                <VignetteVue vignette={nue(boost)} />
                <PictoBoost nombre={boost.apport} etoile={boost.etoile} stat={statActeur} />
                {boost.etoile && !encadre ? <small className="essai-etoile"><Texte>{ligne ?? '★'}</Texte></small> : null}
              </span>
            </span>
          )
        })}
        {rangee.defenseur ? (
          <span className="essai-groupe">
            {operateur('−')}
            <span className="essai-terme">
              <VignetteVue vignette={nue(rangee.defenseur)} />
              <PictoStat genre="def" valeur={pose?.defense} />
              {encadre ? null : resultat}
            </span>
          </span>
        ) : rangee.cibles.length > 0 ? (
          <span className="essai-groupe">
            <span className="deroule-vers" aria-hidden="true">
              →
            </span>
            {rangee.cibles.map((c) => (
              <span key={c.cle} className="essai-terme">
                <VignetteVue vignette={nue(c)} />
                {cible === c && !encadre ? resultat : null}
              </span>
            ))}
          </span>
        ) : null}
        {!cible && !encadre ? <span className="essai-groupe essai-resultat">{resultat}</span> : null}
        {rangee.annulee ? (
          <strong className="deroule-annulee-cause">
            <Texte>{rangee.annulee.cause ? `${t('Annulée')} · ${rangee.annulee.cause}` : t('Annulée')}</Texte>
          </strong>
        ) : null}
        {encadre && rangee.annulee ? (
          // LOT 5 (decision 6) : le tampon, et la carte qui annule a cote.
          <span className="essai-annulation">
            <span className="essai-tampon essai-tampon-rangee" aria-hidden="true">
              {t('ANNULÉE')}
            </span>
            {rangee.annulee.par ? (
              <span className="essai-annuleur">
                <VignetteVue vignette={rangee.annulee.par} />
              </span>
            ) : null}
          </span>
        ) : null}
      </div>
      {encadre && (rangee.resultat || rangee.total) ? (
        // LOT 5 (decision 8) : le resultat sur sa ligne, sous le calcul pose,
        // plutot que coince sous une carte que l'ecran a pu reduire.
        <div className="essai-resultat-ligne">{resultat}</div>
      ) : null}
      {encadre && rangee.motsCles && rangee.motsCles.length > 0 ? (
        // LOT 5b (decision 40) : une ligne par mot-cle qui a joue (Perçant, Robuste, Déferlement).
        <ul className="essai-mots-cles">
          {rangee.motsCles.map((ligne) => (
            <li key={ligne}>
              <Texte>{ligne}</Texte>
            </li>
          ))}
        </ul>
      ) : null}
      {encadre
        ? rangee.lignesEtoile.length > 0 ? (
            // LOT 5 (decision 37) : les lignes ★ recopiees en clair, dans un seul encadre.
            <div className="essai-encadre-etoile">
              {rangee.lignesEtoile.map((ligne) => (
                <p key={ligne}>
                  <b>{t('★ BOOST')}</b> <Texte>{ligne.replace(/^★\s*/, '')}</Texte>
                </p>
              ))}
            </div>
          ) : null
        : etoiles.map((ligne) => (
            <p key={ligne} className="deroule-etoile">
              <Texte>{ligne}</Texte>
            </p>
          ))}
    </div>
  )
}

/**
 * LA MENACE DE L'ETAPE 1 (lot 5, decision 7) : le calcul pose, une ligne par
 * source, le total, la jauge avant → apres sur le seuil, « COMPLÉTÉE ».
 */
/**
 * 13/10/2026 (decision ① seuil proche) : « Encore N avant la défaite » en rouge,
 * des qu'il reste 2 menaces ou moins avant le seuil. Seule une manigance a seuil
 * (la principale) en a un : une annexe n'en a pas.
 */
export function texteAlerteSeuil(jauge: { apres?: number; plafond?: number } | undefined): string | undefined {
  if (!jauge || jauge.apres === undefined || !jauge.plafond) return undefined
  const reste = jauge.plafond - jauge.apres
  if (reste <= 0 || reste > 2) return undefined
  return t('Encore %1 avant la défaite').replace('%1', String(reste))
}

function AlerteSeuil({ jauge }: { jauge: { apres?: number; plafond?: number } | undefined }) {
  const texte = texteAlerteSeuil(jauge)
  return texte ? <p className="essai-alerte-seuil">{texte}</p> : null
}

/** Les couleurs des joueurs à la table (essai, 13/10/2026), pour les pastilles du calcul de menace. */
const AUCUNE_COULEUR: readonly string[] = []
const CouleursJoueurs = createContext<readonly string[]>(AUCUNE_COULEUR)

function MenaceEssai({ rangee, grisee }: { rangee: VueRangee; grisee: boolean }) {
  const couleursJoueurs = useContext(CouleursJoueurs)
  const menace = rangee.menace
  if (!menace) return null
  const jauge = menace.jauge
  const pct = (v: number | undefined) =>
    jauge && v !== undefined && jauge.plafond ? `${Math.min(100, Math.max(0, (v / jauge.plafond) * 100))}%` : '0%'
  return (
    <div className={grisee ? 'essai-menace est-grisee' : 'essai-menace'} aria-hidden={grisee || undefined}>
      {rangee.acteur ? <VignetteVue vignette={{ ...rangee.acteur, legende: undefined }} /> : null}
      <div className="essai-menace-calcul">
        <table className="essai-menace-sources">
          <tbody>
            {menace.sources.map((source) => (
              <tr key={source.libelle}>
                <td>
                  <Texte>{source.libelle}</Texte>
                  {/* 13/10/2026 (encadré ①) : en multijoueur, les pastilles des joueurs comptés. */}
                  {source.parJoueur && couleursJoueurs.length >= 2 ? (
                    <span className="essai-pastilles-joueurs" aria-hidden="true">
                      {couleursJoueurs.map((couleur, rang) => (
                        <span key={rang} className="essai-pastille-joueur-mini" style={{ background: couleur }} />
                      ))}
                    </span>
                  ) : null}
                </td>
                <td className={`essai-menace-valeur${source.valeur < 0 ? ' est-reduction' : ''}`}>
                  {source.valeur < 0 ? `−${-source.valeur}` : `+${source.valeur}`}
                </td>
              </tr>
            ))}
            <tr className="essai-menace-total">
              <td>=</td>
              <td className="essai-menace-valeur">
                {/* 13/10/2026 : moins que prévu, la somme barrée puis la vraie pose. */}
                {menace.prevu !== undefined ? (
                  <>
                    <s className="essai-barre">+{menace.prevu}</s>{' '}
                  </>
                ) : null}
                +{menace.total}
              </td>
            </tr>
          </tbody>
        </table>
        {jauge && jauge.apres !== undefined ? (
          <div className="essai-menace-jauge" role="img" aria-label={`${jauge.avant ?? 0} → ${jauge.apres}${jauge.plafond ? ` / ${jauge.plafond}` : ''}`}>
            <span className="essai-menace-barre">
              <span className="essai-menace-avant" style={{ width: pct(jauge.avant) }} />
              <span className="essai-menace-ajout" style={{ left: pct(jauge.avant), width: `calc(${pct(jauge.apres)} - ${pct(jauge.avant)})` }} />
            </span>
            <span className="essai-menace-chiffres">
              {jauge.avant ?? 0} → <b>{jauge.apres}</b>
              {jauge.plafond ? ` / ${jauge.plafond}` : ''}
            </span>
          </div>
        ) : null}
        <AlerteSeuil jauge={menace.complete ? undefined : jauge} />
        {menace.complete ? (
          <span className="essai-tampon essai-tampon-complete" aria-hidden="true">
            {t('COMPLÉTÉE')}
          </span>
        ) : null}
      </div>
    </div>
  )
}

function CarteRevelee({
  revelee,
  grisee = false,
  question,
  essai = false,
}: {
  revelee: VueRevelee
  grisee?: boolean
  essai?: boolean
  /** La question posee par la carte, a la place du resume (D18). */
  question?: ReactNode
}) {
  const jauge = texteJauge(revelee.jauge)
  const classes = ['deroule-revelee']
  if (revelee.renfort || revelee.renfortInconnu || revelee.remplacement) classes.push('a-renfort')
  if (revelee.chaine) classes.push('a-chaine')
  if (grisee) classes.push('est-grisee')
  return (
    <div className={classes.join(' ')} aria-hidden={grisee || undefined}>
      {revelee.chaine ? <ChaineRevelee chaine={revelee.chaine} essai={essai} /> : null}
      <VignetteVue vignette={revelee.carte} grande />
      {question ?? (
        <div className="deroule-revelee-texte">
          {essai && revelee.etiquettes ? (
            <p className="essai-etiquettes">
              {revelee.etiquettes.map((etiquette) => (
                <span key={etiquette} className="essai-etiquette">
                  {etiquette}
                </span>
              ))}
            </p>
          ) : null}
          {revelee.surtitreRenfort ? <p className="deroule-surtitre-renfort"><Texte>{revelee.surtitreRenfort}</Texte></p> : null}
          {revelee.typeFr ? <p className="deroule-type">{revelee.typeFr}</p> : null}
          {revelee.lignes.length > 0 ? (
            <ul className="deroule-lignes">
              {revelee.lignes.map((ligne, rang) => (
                <li key={rang}>
                  <Texte>{ligne}</Texte>
                </li>
              ))}
            </ul>
          ) : null}
          {jauge ? <span className="deroule-jauge">{jauge}</span> : null}
        </div>
      )}
      {revelee.renfort ? (
        <>
          <span className="deroule-renfort-fleche">{`→ ${t('Renfort')}`}</span>
          <VignetteVue vignette={revelee.renfort} grande />
        </>
      ) : revelee.renfortInconnu ? (
        <>
          <span className="deroule-renfort-fleche">{`→ ${t('Renfort')}`}</span>
          <span className="deroule-renfort-vide" aria-hidden="true">
            ?
          </span>
        </>
      ) : null}
      {revelee.remplacement ? (
        <>
          <span className="deroule-renfort-fleche">{`→ ${revelee.lienRemplacement ?? ''}`}</span>
          <VignetteVue vignette={revelee.remplacement} grande />
        </>
      ) : null}
    </div>
  )
}

/** La chaine Renfort / annulation / remplacement, en petites vignettes (n72). */
function ChaineRevelee({ chaine, essai = false }: { chaine: MaillonChaine[]; essai?: boolean }) {
  return (
    <ol className="deroule-chaine" aria-label={t('Enchaînement des cartes')}>
      {chaine.map((maillon) => {
        const classes = ['deroule-chaine-maillon']
        if (maillon.courante) classes.push('est-courante')
        if (maillon.annulee) classes.push('est-annulee')
        return (
          <li key={maillon.vignette.cle} className={classes.join(' ')}>
            {maillon.lien ? (
              <span className="deroule-chaine-lien">
                {'→ '}
                <Texte>{maillon.lien}</Texte>
              </span>
            ) : null}
            <span className="deroule-chaine-carte">
              <VignetteVue vignette={maillon.vignette} />
              {essai && maillon.annulee ? (
                <span className="essai-tampon" aria-hidden="true">
                  {t('ANNULÉE')}
                </span>
              ) : null}
              {essai && maillon.annuleePar ? (
                <span className="essai-annuleur">
                  <VignetteVue vignette={maillon.annuleePar} />
                </span>
              ) : null}
              {maillon.annulee ? (
                <span className="deroule-chaine-annulee">
                  <Texte>{maillon.annulee}</Texte>
                </span>
              ) : null}
            </span>
          </li>
        )
      })}
    </ol>
  )
}

/** LOT 5c (decision 38) : l'effet ★ differe d'un boost, sur son ecran a part. */
function EtoileDiffereeEssai({ rangee, grisee }: { rangee: VueRangee; grisee: boolean }) {
  const differee = rangee.etoileDifferee
  return (
    <div className={grisee ? 'deroule-rangee essai-etoile-differee est-grisee' : 'deroule-rangee essai-etoile-differee'} aria-hidden={grisee || undefined}>
      <div className="deroule-rangee-cartes" style={{ '--nb-cartes': 1 + rangee.cibles.length } as CSSProperties}>
        {rangee.acteur ? <VignetteVue vignette={{ ...rangee.acteur, legende: undefined }} /> : null}
        {rangee.cibles.length > 0 ? (
          <span className="deroule-vers" aria-hidden="true">
            →
          </span>
        ) : null}
        {rangee.cibles.map((cible) => (
          <VignetteVue key={cible.cle} vignette={cible} />
        ))}
      </div>
      {differee ? (
        <div className="essai-encadre-etoile">
          <p>
            <b>{t('★ BOOST')}</b> <Texte>{differee.texte.replace(/^★\s*/, '')}</Texte>
          </p>
          <p className="essai-etoile-issue">
            <Texte>{differee.issue}</Texte>
          </p>
        </div>
      ) : null}
    </div>
  )
}

/** LOT 5c (decision 45) : un heros elimine en pleine phase. */
function EliminationEssai({ rangee, grisee }: { rangee: VueRangee; grisee: boolean }) {
  return (
    <div className={grisee ? 'deroule-rangee essai-elimination est-grisee' : 'deroule-rangee essai-elimination'} aria-hidden={grisee || undefined}>
      <div className="deroule-rangee-cartes" style={{ '--nb-cartes': 1 } as CSSProperties}>
        {rangee.acteur ? <VignetteVue vignette={{ ...rangee.acteur, legende: undefined }} /> : null}
        <span className="essai-tampon essai-tampon-rangee" aria-hidden="true">
          {t('ÉLIMINÉ')}
        </span>
      </div>
      {rangee.resultat ? (
        <p className="essai-resultat-ligne">
          <Texte>{rangee.resultat.texte}</Texte>
        </p>
      ) : null}
    </div>
  )
}

/** LOT 5c (decision 42) : la distribution de l'etape 3 en tableau, une ligne par joueur. */
function DistributionEssai({ distribution, grisee }: { distribution: VueDistribution; grisee: boolean }) {
  return (
    <div className={grisee ? 'essai-distribution est-grisee' : 'essai-distribution'} aria-hidden={grisee || undefined}>
      <table>
        <thead>
          <tr>
            <th scope="col">{t('Joueur')}</th>
            <th scope="col">{t('Cartes')}</th>
            <th scope="col">{t('Pourquoi')}</th>
          </tr>
        </thead>
        <tbody>
          {distribution.lignes.map((ligne) => (
            <tr key={ligne.cle} data-siege={ligne.joueur}>
              <td>
                <Texte>{ligne.nom}</Texte>
              </td>
              <td className="essai-distribution-dos" aria-label={`${ligne.cartes}`}>
                {Array.from({ length: Math.max(ligne.raisons.length, ligne.cartes) }, (_, i) => (
                  <span key={i} className="essai-dos-mini" aria-hidden="true" />
                ))}
                <b>{ligne.raisons.length > ligne.cartes ? ligne.raisons.length : ligne.cartes}</b>
              </td>
              <td>
                {ligne.raisons.length > 0 ? <Texte>{ligne.raisons.join(' · ')}</Texte> : <span>{t('la règle (1 par joueur)')}</span>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function Stade({ stade, grisee = false, essai = false }: { stade: VueStade; grisee?: boolean; essai?: boolean }) {
  return (
    <div className={grisee ? 'deroule-stade est-grisee' : 'deroule-stade'} aria-hidden={grisee || undefined}>
      {stade.avant ? (
        <>
          <VignetteVue vignette={stade.avant} />
          <span className="deroule-vers" aria-hidden="true">
            →
          </span>
        </>
      ) : null}
      <VignetteVue vignette={stade.apres} />
      {stade.deltas.length > 0 ? (
        <ul className="deroule-lignes">
          {stade.deltas.map((delta) => (
            <li key={delta}>
              <Texte>{delta}</Texte>
            </li>
          ))}
        </ul>
      ) : null}
      {essai && stade.suite ? (
        // LOT 5c (decision 11) : ce qui se passe ensuite.
        <p className="essai-stade-suite">
          <Texte>{stade.suite}</Texte>
        </p>
      ) : null}
    </div>
  )
}

/** Une ligne du bilan : le nom, puis la jauge, ou ce que la phase a coute. */
function LigneColonne({ colonne, unite }: { colonne: ColonneJauge; unite: 'degats' | 'menaces' }) {
  const jauge = texteJauge(colonne.jauge)
  const cout =
    unite === 'degats'
      ? `${colonne.total} ${colonne.total < 2 ? t('dégât') : t('dégâts')}`
      : `+${colonne.total} ${colonne.total < 2 ? t('menace') : t('menaces')}`
  return (
    <li>
      <span className="deroule-colonne-nom">
        <Texte>{colonne.nom}</Texte>
      </span> <span className="deroule-jauge">{jauge || cout}</span>
      {colonne.statuts?.map((statut) => (
        <small key={statut} className="deroule-statut">
          {statut}
        </small>
      ))}
    </li>
  )
}

/** La liste courte du bilan tient dans la boite fixe : au-dela, « et N autres ». */
const LIGNES_BILAN_MAX = 10

function Bilan({ bilan, grisee = false, essai = false }: { bilan: VueBilan; grisee?: boolean; essai?: boolean }) {
  // La phase n'a rien coute : on le dit, plutot que trois colonnes vides.
  if (bilan.vide)
    // 13/10/2026 (encadré ⑱) : dans l'essai, en grand et en vert.
    return essai ? (
      <p className="deroule-vide essai-bilan-calme">{t('Rien de grave cette phase')}</p>
    ) : (
      <p className="deroule-vide">{texteBilanVide()}</p>
    )
  const rien = <li className="deroule-rien">{t('aucun')}</li>
  return (
    <div className={grisee ? 'deroule-bilan est-grisee' : 'deroule-bilan'} aria-hidden={grisee || undefined}>
      <section className="deroule-colonne">
        <h3 className="deroule-colonne-titre">{t('Menace')}</h3>
        <ul className="deroule-lignes">
          {bilan.menace.length > 0
            ? bilan.menace.map((colonne) => <LigneColonne key={colonne.cle} colonne={colonne} unite="menaces" />)
            : rien}
        </ul>
      </section>
      <section className="deroule-colonne">
        <h3 className="deroule-colonne-titre">{t('Héros et alliés')}</h3>
        <ul className="deroule-lignes">
          {bilan.heros.length > 0
            ? bilan.heros.map((colonne) => <LigneColonne key={colonne.cle} colonne={colonne} unite="degats" />)
            : rien}
        </ul>
      </section>
      <section className="deroule-colonne">
        <h3 className="deroule-colonne-titre">{t('Nouveautés sur la table')}</h3>
        {bilan.nouveautes.length > 0 ? (
          <div className="deroule-nouveautes">
            {bilan.nouveautes.map((vignette) => (
              <VignetteVue key={vignette.cle} vignette={vignette} />
            ))}
          </div>
        ) : (
          <p className="deroule-vide">{t('Rien de nouveau sur la table')}</p>
        )}
      </section>
      {essai && bilan.evenements ? (
        // LOT 5 (decision 12) : la liste courte de la phase ; survoler une ligne
        // montre sa carte dans l'apercu habituel (meme `data-card-id` qu'une carte).
        <section className="deroule-colonne essai-bilan-liste">
          <h3 className="deroule-colonne-titre">{t('La phase en bref')}</h3>
          <ol className="deroule-lignes">
            {bilan.evenements.slice(0, LIGNES_BILAN_MAX).map((evenement) => (
              <li
                key={evenement.cle}
                className={evenement.carteId !== undefined ? 'essai-bilan-ligne est-survolable' : 'essai-bilan-ligne'}
                data-card-id={evenement.carteId !== undefined ? String(evenement.carteId) : undefined}
                tabIndex={evenement.carteId !== undefined ? 0 : undefined}
              >
                {evenement.texte}
              </li>
            ))}
          </ol>
          {bilan.evenements.length > LIGNES_BILAN_MAX ? (
            <p className="deroule-vide">
              {t('et %1 autres').replace('%1', String(bilan.evenements.length - LIGNES_BILAN_MAX))}
            </p>
          ) : null}
        </section>
      ) : null}
    </div>
  )
}

function Corps({ corps, grisee, essai = false }: { corps: VueCorps; grisee: boolean; essai?: boolean }) {
  switch (corps.genre) {
    case 'rangee':
      if (essai && corps.menace) return <MenaceEssai rangee={corps} grisee={grisee} />
      if (essai && corps.etoileDifferee) return <EtoileDiffereeEssai rangee={corps} grisee={grisee} />
      if (essai && corps.elimine) return <EliminationEssai rangee={corps} grisee={grisee} />
      if (essai && (corps.pose || corps.annulee || corps.riposte)) return <RangeeEssai rangee={corps} grisee={grisee} encadre />
      // LOT 4 (decision 3) : une carte qui entre en jeu se dit d'un bandeau, puis vole vers la table (TrajetsPhase).
      if (essai && corps.entree)
        return (
          <div className="essai-entree">
            <Rangee rangee={corps} grisee={grisee} />
            <strong className="essai-bandeau-nouveau">{corps.entree.sbire ? t('Nouveau sbire') : t('Entre en jeu')}</strong>
          </div>
        )
      return <Rangee rangee={corps} grisee={grisee} />
    case 'revelee':
      return <CarteRevelee revelee={corps} grisee={grisee} essai={essai} />
    case 'stade':
      return <Stade stade={corps} grisee={grisee} essai={essai} />
    case 'distribution':
      return <DistributionEssai distribution={corps} grisee={grisee} />
    case 'bilan':
      return <Bilan bilan={corps} grisee={grisee} essai={essai} />
    case 'vide':
      return <p className="deroule-vide">{corps.texte}</p>
    case 'attente':
      return <Rangee rangee={corps.rangee} grisee />
    case 'question-seule':
      return null
  }
}

function LigneDuHaut({
  liste,
  bandeau,
  relire,
  titre,
  sousTitre,
  page,
  outils,
  numerosCarres = false,
}: {
  /** Vide : pas de pastilles (« Pendant ton tour », D26). */
  liste: Pastille[]
  /** « Relecture » (D23, D38) ou « Pendant ton tour » (D26). */
  bandeau?: string
  /** Relire une pastille passee (D22) ; absent, aucune ne se clique. */
  relire?: (cle: ClePastille) => void
  titre: string
  /** Sous le titre : la carte revelee, quand le titre dit « Carte rencontre 2/2 · X ». */
  sousTitre?: string
  page?: string
  /** Essai : ce qui se pose a droite du titre (compteur de cartes, « Réduire »). */
  outils?: ReactNode
  /** Bis : chiffres simples, la police embarquee ne dessine pas bien ①…⑤. */
  numerosCarres?: boolean
}) {
  return (
    <header className="deroule-ligne-haut">
      <div className="deroule-frise">
        {liste.length > 0 ? (
          <ol className="deroule-pastilles">
            {liste.map((pastille) => {
              // 13/10/2026 (encadré ⑩) : une étape passée sans rien (2B sans sbire)
              // reste grisée, son nom remplacé par « — ».
              const vide = numerosCarres && pastille.etat === 'passe' && pastille.resume === t('aucun')
              const contenu = (
                <>
                  <span className="deroule-pastille-numero">
                    {numerosCarres
                      ? pastille.cle === 'mechant'
                        ? '2A'
                        : pastille.cle === 'sbires'
                          ? '2B'
                          : pastille.cle === 'cartes-rencontre'
                            ? '3'
                            : pastille.cle === 'bilan'
                              ? '✓'
                              : '1'
                      : pastille.numero}
                  </span>
                  <span className="deroule-pastille-nom">{vide ? '—' : pastille.nom}</span>
                  {pastille.resume && !vide ? <small className="deroule-pastille-resume">{pastille.resume}</small> : null}
                  {pastille.compteur ? <small className="deroule-pastille-compteur">{pastille.compteur}</small> : null}
                </>
              )
              return (
                <li
                  key={pastille.cle}
                  className={`deroule-pastille est-${pastille.etat}${pastille.relu ? ' est-relu' : ''}${vide ? ' est-vide' : ''}`}
                  title={pastille.libelle}
                >
                  {/* Une pastille passee se relit d'un clic (D22) : un bouton,
                    pour le clavier et le lecteur d'ecran. Le seuil de
                    `useGlisserPanneau` laisse passer le clic sans deplacer. */}
                  {pastille.relisible && relire ? (
                    <button
                      type="button"
                      className="deroule-pastille-bouton"
                      aria-label={pastille.libelle}
                      aria-pressed={pastille.relu}
                      onClick={() => relire(pastille.cle)}
                    >
                      {contenu}
                    </button>
                  ) : (
                    contenu
                  )}
                </li>
              )
            })}
          </ol>
        ) : null}
        {bandeau ? <p className="deroule-bandeau">{bandeau}</p> : null}
        {page ? <small className="deroule-page">{page}</small> : null}
      </div>
      {outils ? (
        <div className="essai-titre-ligne">
          <h2 className="deroule-titre-court">
            <Texte>{titre}</Texte>
          </h2>
          {outils}
        </div>
      ) : (
        <h2 className="deroule-titre-court">
          <Texte>{titre}</Texte>
        </h2>
      )}
      {sousTitre ? (
        <p className="deroule-sous-titre">
          <Texte>{sousTitre}</Texte>
        </p>
      ) : null}
    </header>
  )
}

/** Les questions qui se jouent DANS la rangee : la defense, et pendant elle (D7, D8). */
type VueDefense = Extract<VueSousCadre, { genre: 'defense' }>

/**
 * LA RANGEE DE DEFENSE (D7) : l'attaquant a gauche, avec ce qu'on sait de son
 * attaque au moment de choisir (« ATQ 2 + 1 carte boost », jamais un total :
 * le boost se retourne APRES la defense). Les defenseurs viennent ensuite, en
 * vignettes cliquables (`choix`).
 */
function rangeeDeDefense(vue: VueDefense, q: QuestionDuMoteur): VueRangee {
  const id = vue.attaquantId
  const scan = id !== undefined ? q.carteScene(id, true) : undefined
  return {
    genre: 'rangee',
    acteur:
      id !== undefined
        ? {
            cle: `attaquant:${id}`,
            carteId: id,
            scan,
            nom: q.nomPorteur(id) || scan?.name || '',
            legende: q.ligneSansDefense,
            etat: 'inerte',
          }
        : undefined,
    boosts: [],
    cibles: [],
    lignesEtoile: [],
    grisee: false,
  }
}

/**
 * Les cartes de la question d'un AUTRE siege (D28), grisees : les cartes que
 * ses options designent, une fois chacune. Lecture seule : des figures, jamais
 * des boutons.
 */
function vignettesDUnAutre(
  options: Array<{ id: number; bindId: number; nom: string }>,
  carteScene: CartouchePhaseProps['carteScene']
): Vignette[] {
  const vues = new Set<number>()
  const vignettes: Vignette[] = []
  for (const option of options) {
    if (option.bindId === 0 || vues.has(option.bindId)) continue
    vues.add(option.bindId)
    vignettes.push({
      cle: `attente:${option.bindId}`,
      carteId: option.bindId,
      scan: carteScene?.(option.bindId, true),
      nom: option.nom,
      legende: option.nom,
      etat: 'grisee',
    })
  }
  return vignettes
}

/** Toutes les cartes que le cartouche dessine : la loupe les retrouve par `data-card-id` (piege 8). */
/** Au doigt : au-dela, l'appui est un appui long (ouvre la carte en grand). */
const DELAI_APPUI_LONG = 450

/**
 * Les noms ecrits dans la boite, avec leur carte : ceux de l'etape (auteur,
 * cible, defenseur, boosts) et ceux des vignettes dessinees. `nomsMontrables`
 * ne garde que ceux que la loupe sait montrer.
 */
function candidatsDesNoms(
  lue: EtapeDeroule | undefined,
  corps: VueCorps | undefined,
  autres: Array<Vignette | undefined>
): Array<{ nom?: string; carteId?: number }> {
  const candidats: Array<{ nom?: string; carteId?: number }> = []
  const vignettes = (liste: Array<Vignette | undefined>) => {
    for (const v of liste) if (v) candidats.push({ nom: v.nom, carteId: v.carteId })
  }
  if (lue) {
    candidats.push(
      { nom: lue.auteurNom, carteId: lue.carteId },
      { nom: lue.cibleNom, carteId: lue.cibleId },
      { nom: lue.defenseurNom, carteId: lue.defenseurId },
      ...lue.boosts.map((boost) => ({ nom: boost.nom, carteId: boost.cibleId }))
    )
  }
  vignettes(autres)
  const rangee = (r: VueRangee) => vignettes([r.acteur, ...r.boosts, r.defenseur, ...r.cibles])
  switch (corps?.genre) {
    case 'rangee':
      rangee(corps)
      break
    case 'attente':
      rangee(corps.rangee)
      break
    case 'revelee':
      vignettes([corps.carte, corps.renfort, corps.remplacement, ...(corps.chaine ?? []).flatMap((m) => [m.vignette, m.annuleePar])])
      break
    case 'stade':
      vignettes([corps.avant, corps.apres])
      break
    case 'bilan':
      vignettes(corps.nouveautes)
      for (const colonne of [...corps.menace, ...corps.heros]) candidats.push({ nom: colonne.nom, carteId: colonne.carteId })
      break
    default:
      break
  }
  return candidats
}

function scansDe(
  corps: VueCorps | undefined,
  question: VueSousCadre | undefined,
  autres: Vignette[],
  /** Essai : les noms du bilan (heros, allies, manigances) ouvrent aussi leur carte. */
  carteScene?: (id: number, faceVisible: boolean) => ScanCardProps | undefined
): ScanCardProps[] {
  const scans: Array<ScanCardProps | undefined> = autres.map((v) => v.scan)
  const vignettes = (liste: Array<Vignette | undefined>) => {
    for (const v of liste) scans.push(v?.scan)
  }
  const rangee = (r: VueRangee) => vignettes([r.acteur, ...r.boosts, r.defenseur, ...r.cibles])
  switch (corps?.genre) {
    case 'rangee':
      rangee(corps)
      break
    case 'attente':
      rangee(corps.rangee)
      break
    case 'revelee':
      vignettes([
        corps.carte,
        corps.renfort,
        corps.remplacement,
        ...(corps.chaine ?? []).flatMap((maillon) => [maillon.vignette, maillon.annuleePar]),
        ...(corps.question?.choix ?? []),
      ])
      break
    case 'stade':
      vignettes([corps.avant, corps.apres])
      break
    case 'bilan':
      vignettes(corps.nouveautes)
      if (carteScene) {
        for (const colonne of [...corps.menace, ...corps.heros]) {
          if (colonne.carteId !== undefined) scans.push(carteScene(colonne.carteId, true))
        }
      }
      break
    default:
      break
  }
  switch (question?.genre) {
    case 'defense':
      for (const v of [...question.defenseurs, ...question.autres]) scans.push(v.scan)
      break
    case 'pendant-defense':
      for (const v of question.options) scans.push(v.scan)
      break
    case 'reponses':
    case 'choix-carte':
      for (const v of question.choix) scans.push(v.scan)
      break
    case 'cibles':
    case 'ordre':
      for (const c of question.cibles) scans.push(c.scan)
      break
    case 'paiement':
      for (const c of question.cartesMain) scans.push(c.scan)
      break
    default:
      break
  }
  return scans.filter((scan): scan is ScanCardProps => scan !== undefined)
}

export function CartouchePhase(props: CartouchePhaseProps) {
  const { etape, etapes, index, efface, questionAuJoueur, question, tempsQuestion, avancer } = props

  const horsPhase = props.bandeau === 'pendant-ton-tour'
  const depuisLeJournal = props.bandeau === 'relecture-journal'
  const essai = props.essai === true
  // « Réduire » (essai, question 33) : une barre garde la carte en cours, le
  // plateau redevient visible. Une nouvelle etape le laisse replie : c'est le
  // joueur qui l'a voulu.
  const [reduit, setReduit] = useState(false)

  // Une question posee AVANT toute etape (la fenetre d'interruption qui
  // precede la menace) s'affiche quand meme : sans elle, plus aucun bouton
  // nulle part (constat du 12/09/2026, DeroulePhase).
  // Celle d'un AUTRE siege aussi (multi, 11/10/2026) : sans elle, les autres
  // joueurs ne voyaient rien tant que l'hote n'avait pas repondu.
  const questionSansEtape =
    etape === undefined &&
    (questionAuJoueur
      ? question !== undefined || props.questionDuMoteur !== undefined
      : props.questionDUnAutre !== undefined)
  const montre = !efface && (etape !== undefined || questionSansEtape)
  // La colonne n'est reservee que si la boite est REELLEMENT affichee : le
  // composant reste monte, vide, hors de la phase (mise en place, tour du joueur).
  useColonneEssai(essai && montre)
  // LA RELECTURE (D22, D23) : jamais devant une question, qui a besoin de
  // l'etape en cours sous les yeux et de ses boutons.
  const relu = questionAuJoueur || horsPhase ? undefined : props.relecture

  // LA PAGE LUE (D41), retenue pour UNE etape dans UN etat : une autre etape,
  // ou la meme qui se complete (annonce puis resolu), repart de la premiere.
  // En relecture, les coups de la pastille relue se suivent en pages.
  const identite = relu ? `relecture|${relu.temps}` : etape ? `${etape.cle}|${etape.etat ?? ''}` : ''
  const [pageLue, setPageLue] = useState<{ identite: string; page: number }>()

  const ctx: ContexteVue = {
    etapes,
    index,
    boostsMontres: props.boostsMontres,
    carteScene: props.carteScene,
    nomFr: props.nomFr,
    pvMaxParNom: props.pvMaxParNom,
    texteEtoile: props.texteEtoile,
    infoCarte: props.infoCarte,
    infoRevelee: props.infoRevelee,
  }
  const pagesDeLEtape = (e: EtapeDeroule, contexte: ContexteVue): PageLue[] => {
    const lue = etapeEnLangue(e, props.nomFr)
    return [{ etape: e, lue, corps: vueDeLEtape(lue, contexte) }]
  }
  // Une etape relue est PASSEE : ses boosts sont tous retournes.
  const contexteRelu = (e: EtapeDeroule): ContexteVue => ({
    ...ctx,
    index: etapes.indexOf(e),
    boostsMontres: e.boosts.length,
  })
  const sequence: PageLue[] = relu
    ? etapes
        .filter((e) => tempsDeLaPastille(relu.temps).includes(e.temps))
        .flatMap((e) => pagesDeLEtape(e, contexteRelu(e)))
    : etape
      ? pagesDeLEtape(etape, ctx)
      : []
  const page = Math.min(pageLue?.identite === identite ? pageLue.page : 0, Math.max(0, sequence.length - 1))
  const vuePage: PageLue | undefined = sequence[page]
  const etapeLue = vuePage?.lue
  const dernierePage = page >= sequence.length - 1
  const tournerLaPage = () => setPageLue({ identite, page: page + 1 })

  // LA QUESTION DU MOTEUR, EN DONNEES (lot 4). Elle ne vaut que pour le
  // joueur local : celle d'un autre siege se lit, ne se joue pas (D28).
  const q = questionAuJoueur ? props.questionDuMoteur : undefined
  const vueQ = q ? vueSousCadre(q, { etape, tempsQuestion }) : undefined
  const corpsRangee = vuePage?.corps.genre === 'rangee' ? vuePage.corps : undefined
  const corpsRevele = vuePage?.corps.genre === 'revelee' ? vuePage.corps : undefined
  // Ou se joue-t-elle ? La defense et ce qui se joue pendant elle : dans la
  // rangee (D7, D8). Le choix pose par la carte revelee : a sa droite (D18).
  // Tout le reste : le sous-cadre, par-dessus l'etape grisee (D4 a D6).
  const aDroiteDeLaCarte = vueQ?.genre === 'choix-carte' && corpsRevele !== undefined
  const vueDuSousCadre =
    vueQ && !aDroiteDeLaCarte && vueQ.genre !== 'defense' && vueQ.genre !== 'pendant-defense' ? vueQ : undefined

  // L'ATTENTE D'UN AUTRE JOUEUR (D28) : la rangee reste, ses cartes grisees,
  // et « Black Panther choisit… » pulse a la place des boutons.
  // En relecture, on lit une etape passee : l'attente se dit au pied.
  const attente = !questionAuJoueur && props.questionDUnAutre !== undefined
  const attenteDansLEtape = attente && !relu
  // Un autre joueur choisit sur la DERNIERE etape connue : rien a valider ici
  // tant qu'il n'a pas repondu, et c'est elle que sa question complete. En
  // retard sur la table, l'etape lue est une etape passee : elle reste la
  // sienne (« X choisit… » passe au pied) et le joueur garde son « Suivant »
  // pour la rattraper.
  const attenteSurPlace = attenteDansLEtape && (etape === undefined || index === etapes.length - 1)
  const vignettesAttente = attenteSurPlace
    ? vignettesDUnAutre(props.questionDUnAutre?.options ?? [], props.carteScene)
    : []
  const texteAttenteNommee = props.nomJoueurAttendu
    ? t('%1 choisit…').replace('%1', props.nomJoueurAttendu)
    : t('Un autre joueur choisit…')
  const defenseVue = vueQ?.genre === 'defense' && q ? rangeeDeDefense(vueQ, q) : undefined

  // LA LOUPE (D29) : un seul ecouteur, sur la section ; la carte regardee est
  // retrouvee dans la liste COURANTE (`apercu-survol.ts`) : une carte qui
  // quitte le cartouche emporte son agrandissement. Il s'ouvre juste
  // au-dessus du cartouche, centre sur la vignette survolee.
  const scans = scansDe(
    vuePage?.corps,
    vueQ,
    [...vignettesAttente, ...(defenseVue?.acteur ? [defenseVue.acteur] : [])],
    essai ? props.carteScene : undefined
  )
  const { regardee, survol, quitter, viser } = useApercuSurvol(scans)
  // Finition (12/10/2026) : la question « de repli » dessine ses propres cartes,
  // absentes de `scans` ; l'appui long retombe alors sur la carte de la table.
  const [idAppui, setIdAppui] = useState<string | undefined>(undefined)
  const apercu =
    regardee ??
    (essai && idAppui !== undefined && /^\d+$/.test(idAppui) ? props.carteScene?.(Number(idAppui), true) : undefined)
  const optionSurvolee = useRef<number | undefined>(undefined)

  // LOT 2 (essai, decision 55) : les noms de cartes ecrits dans la boite
  // ouvrent la carte a droite, comme les cartes elles-memes.
  const nomsDeLaBoite: NomDeCarte[] = essai
    ? nomsMontrables(candidatsDesNoms(vuePage?.lue, vuePage?.corps, [...vignettesAttente, ...(defenseVue ? [defenseVue.acteur, ...defenseVue.cibles] : [])]), scans)
    : []

  // LOT 2 (essai, decisions 29, 48, 54) : une seule taille de carte par ecran,
  // qui rapetisse toute ensemble si l'ecran ne tient pas (`essai-tailles.ts`).
  // L'ecran est la page lue dans son etat : etape, page, boosts retournes,
  // question posee ou non. Un nouvel ecran repart de la plus grande taille ;
  // le meme ecran qui grandit (une question qui s'ajoute) ne fait que descendre.
  const refSection = useRef<HTMLElement | null>(null)
  const refCartouche = props.refCartouche
  const poserSection = useCallback(
    (el: HTMLElement | null) => {
      refSection.current = el
      refCartouche(el)
    },
    [refCartouche]
  )
  const ecranDesCartes = [
    vuePage?.etape.cle ?? 'sans-etape',
    vuePage?.etape.etat ?? '',
    page,
    props.boostsMontres,
    questionAuJoueur ? 'question' : '',
    vueQ?.genre ?? '',
    attenteSurPlace ? 'attente' : '',
    relu?.temps ?? '',
  ].join('|')
  const ecranAjuste = useRef('')
  const [, setRecalage] = useState(0)
  useLayoutEffect(() => {
    const section = refSection.current
    if (!section) return
    if (!essai || reduit) {
      section.style.removeProperty('--essai-carte-h')
      ecranAjuste.current = ''
      return
    }
    const corps = section.querySelector<HTMLElement>(':scope > .deroule-corps')
    if (!corps) return
    if (ecranAjuste.current !== ecranDesCartes) {
      ecranAjuste.current = ecranDesCartes
      ajusterLesCartes(section, corps)
    } else if (deborde(corps)) {
      ajusterLesCartes(section, corps, hauteurPosee(section))
    }
  })
  // Une mesure prise pendant une animation (le glissement d'entree du corps,
  // le bandeau de phase) lit des positions decalees : on remesure, depuis la
  // plus grande taille, a la fin de chaque animation et a chaque redimension.
  useEffect(() => {
    if (!essai) return
    const section = refSection.current
    const recaler = () => {
      ecranAjuste.current = ''
      setRecalage((n) => n + 1)
    }
    window.addEventListener('resize', recaler)
    section?.addEventListener('animationend', recaler)
    section?.addEventListener('transitionend', recaler)
    return () => {
      window.removeEventListener('resize', recaler)
      section?.removeEventListener('animationend', recaler)
      section?.removeEventListener('transitionend', recaler)
    }
  }, [essai, montre])

  // LOT 2 (essai, decision 56) : au doigt, un APPUI LONG sur une carte ou un
  // nom ouvre la carte en grand, relacher la ferme. L'appui court ne fait
  // rien : le survol emule qui suit un appui ne doit pas l'ouvrir, et le clic
  // qui suit un appui long ne doit pas choisir la carte.
  const appui = useRef<{ minuteur?: number; ouvert: boolean; doigt: boolean }>({ ouvert: false, doigt: false })
  useEffect(() => () => window.clearTimeout(appui.current.minuteur), [])

  if (!montre) return null

  const survolerSection = (evenement: ReactMouseEvent<HTMLElement>) => {
    if (!(essai && appui.current.doigt)) survol(evenement)
    const cible = evenement.target as HTMLElement
    // Le survol d'une option la signale a la table (pulse des cibles), comme
    // dans le panneau d'avant ; une option indisponible ne pulse pas.
    if (!q) return
    const zone = cible.closest<HTMLElement>('[data-option-id]')
    const id = zone ? Number(zone.dataset.optionId) : undefined
    if (id === optionSurvolee.current) return
    optionSurvolee.current = id
    const option = id !== undefined ? optionDe(q, id) : undefined
    q.survolerOption(option && !option.failure_reason ? option : undefined)
  }
  const quitterSection = () => {
    quitter()
    if (q && optionSurvolee.current !== undefined) {
      optionSurvolee.current = undefined
      q.survolerOption(undefined)
    }
  }

  const herosIds = new Set([...(props.herosLocauxIds ?? []), ...(props.herosDesAutresIds ?? [])])
  const liste = pastilles({
    etapes,
    index,
    // Depuis le journal, la phase est finie : toutes les pastilles sont
    // passees, donc toutes se relisent (D38).
    tempsAffiche: depuisLeJournal
      ? 'premier-joueur'
      : etape
        ? tempsAfficheDe(etape, questionAuJoueur, tempsQuestion)
        : (tempsQuestion ?? 'menace'),
    cartesDistribuees: props.cartesDistribuees,
    questionAuJoueur,
    relecture: relu?.temps,
    herosViseId: etape ? herosViseDe(etape, herosIds) : undefined,
    plusieursHeros: (props.herosDesAutresIds?.size ?? 0) > 0,
  })
  const relire = props.setRelecture
  // « Revenir à 2B » : le nom court de la pastille en cours (D23).
  const courante = liste.find((pastille) => pastille.etat === 'courant')
  const libelleRevenir = courante ? t('Revenir à %1').replace('%1', courante.court) : t('Revenir à l’étape en cours')

  // Pendant une question, l'etape reste sous les yeux, grisee, derriere le
  // sous-cadre (D4). Sans question structuree (table, banc d'essai), toute
  // question grise l'etape, comme avant.
  // Le CHOIX d'un effet d'une carte laisse les cartes en couleur (10/10/2026) :
  // grisées, on ne voyait plus qui attaque qui au moment de choisir.
  const choixEnCours = vueDuSousCadre?.genre === 'choix-carte'
  const grisee = q ? vueDuSousCadre !== undefined && !choixEnCours : questionAuJoueur
  const etapeEstAnnonce = etape?.etat === 'annonce'
  // Une annonce se complete SUR PLACE tant qu'elle est la derniere etape
  // connue (le cartouche est alors « a jour » et le moteur la resout). Une
  // annonce DEPASSEE (une etape la suit deja : l'activation n'a jamais ete
  // close, un changement de stade en pleine attaque) ne se completera plus :
  // elle doit pouvoir se valider, sinon plus rien ne bouge.
  const annonceEnCours = etapeEstAnnonce && index === etapes.length - 1
  // L'attente d'un autre joueur se dessine DANS la rangee seulement sur
  // l'etape que sa question complete (`attenteSurPlace`) ; sinon, au pied.
  const attenteDansLaRangee = attenteSurPlace && corpsRangee !== undefined

  const choisir = (optionId: number) => {
    const option = q ? optionDe(q, optionId) : undefined
    if (q && option) q.choisirOption(option)
  }

  // LE CORPS, selon ce que la question demande.
  let corps: ReactNode = null
  if (defenseVue && vueQ?.genre === 'defense') {
    // Essai (13/10/2026) : « Demander à X de défendre » a son bouton bleu en bas ;
    // la rangee ne montre que l'attaquant et TES defenseurs (choix de l'utilisateur).
    const autresEnCarte = essai ? vueQ.autres.filter((choix) => !choix.demande) : vueQ.autres
    corps = (
      <Rangee
        rangee={defenseVue}
        grisee={false}
        nbChoix={vueQ.defenseurs.length + autresEnCarte.length}
        choix={
          <>
            <span className="deroule-vers" aria-hidden="true">
              →
            </span>
            {[...vueQ.defenseurs, ...autresEnCarte].map((choix) => (
              <BoutonOption key={choix.optionId} vignette={choix} choisir={() => choisir(choix.optionId)} />
            ))}
          </>
        }
      />
    )
  } else if (vueQ?.genre === 'pendant-defense') {
    // Le defenseur n'est connu que par le fait `boosts` d'une ATTAQUE annoncee
    // (`vueSousCadre`) : sa rangee est la. La rangee vide n'est qu'un garde-fou.
    corps = (
      <Rangee
        rangee={
          corpsRangee ?? {
            genre: 'rangee',
            boosts: [],
            cibles: [],
            lignesEtoile: [],
            grisee: false,
          }
        }
        grisee={false}
        choix={vueQ.options.map((choix) => (
          <BoutonOption key={choix.optionId} vignette={choix} choisir={() => choisir(choix.optionId)} />
        ))}
      />
    )
  } else if (vueQ?.genre === 'choix-carte' && corpsRevele) {
    corps = (
      <CarteRevelee
        revelee={corpsRevele}
        essai={essai}
        question={
          <div className="deroule-question-carte">
            <p className="deroule-question-intitule" title={vueQ.intitule}>
              {vueQ.intitule}
            </p>
            <div className={choixEnTexte(vueQ) ? 'deroule-question-choix est-textes' : 'deroule-question-choix'}>
              {vueQ.choix.map((choix) => (
                <BoutonOption key={choix.optionId} vignette={choix} choisir={() => choisir(choix.optionId)} />
              ))}
            </div>
          </div>
        }
      />
    )
  } else if (attenteDansLaRangee && corpsRangee) {
    corps = (
      <Rangee
        rangee={vignettesAttente.length > 0 ? { ...corpsRangee, cibles: vignettesAttente } : corpsRangee}
        grisee={false}
        attente
        fin={<span className="deroule-pulse">{texteAttenteNommee}</span>}
      />
    )
  } else if (vuePage) {
    corps = <Corps corps={vuePage.corps} grisee={grisee} essai={essai} />
  }

  // LE REFUS d'une question jouee dans la rangee : a droite, sous les
  // vignettes (D7, D34). Celui du sous-cadre vit dans le sous-cadre.
  let refus: { libelle: string; titre?: string } | undefined
  if (q && vueQ?.genre === 'defense' && q.demande.show_cancel) {
    refus = {
      libelle: vueQ.refus,
      titre: q.survolSansDefense ?? q.ligneSansDefense,
    }
  } else if (vueQ?.genre === 'pendant-defense') {
    refus = { libelle: vueQ.refus }
  } else if (vueQ?.genre === 'choix-carte' && corpsRevele && vueQ.refus) {
    refus = { libelle: vueQ.refus }
  }

  // 13/10/2026 (encadré ⑫) : tant qu'elle n'est pas retournée, la carte révélée
  // n'est qu'un dos ; une question du moteur la montre toujours.
  // Un joueur qui regarde sans bouton (multi) ne pourrait jamais la retourner : chez lui, elle arrive retournée.
  const regardeSansBouton = props.multi?.genre === 'regarde' || props.multi?.genre === 'attente-choix' || props.multi?.genre === 'choix-hote'
  const carteCacheeIci = Boolean(essai && !relu && props.carteCachee && etapeLue?.titre === 'revelation' && !questionAuJoueur && !regardeSansBouton)
  if (carteCacheeIci) {
    corps = (
      <div className="essai-revelation-cachee">
        <span className="essai-dos-rencontre" aria-hidden="true" />
        <p>{t('Clique sur Continuer pour la retourner.')}</p>
      </div>
    )
  }

  // L'ESSAI (decisions du 10/10/2026) : pendant le choix du defenseur, une
  // rangee de boutons de meme taille en bas du panneau, un « Défendre avec X »
  // vert par defenseur (son picto DEF en tete) et « Ne pas défendre » gris.
  const choixDefense =
    essai && q && vueQ?.genre === 'defense' ? (
      <div className="essai-choix-defense" role="group" aria-label={t('Défendre ?')}>
        {vueQ.defenseurs.map((choix) => (
          <button
            key={choix.optionId}
            type="button"
            className="essai-choix est-defendre"
            data-option-id={choix.optionId}
            aria-disabled={choix.indisponible ? true : undefined}
            title={choix.indisponible ?? choix.nom}
            onClick={() => {
              if (!choix.indisponible) choisir(choix.optionId)
            }}
          >
            {choix.defense ? <PictoStat genre="def" valeur={choix.defense.valeur} /> : null}
            <span>
              {choix.defense ? `${t('Défendre avec')} ${choix.defense.source}` : avecIcones(marquerRessources(choix.nom))}
              {/* 13/10/2026 : grisé AVEC la raison, dite dans le bouton. */}
              {choix.indisponible ? ` · ${choix.indisponible}` : null}
            </span>
          </button>
        ))}
        {/* 13/10/2026 : ce qu'on peut jouer AVANT de défendre (Interruptions), à part, en doré. */}
        {vueQ.autres.some((choix) => !choix.demande) ? (
          <div className="essai-avant-defendre" role="group" aria-label={t('Avant de défendre, tu peux jouer :')}>
            <p>{t('Avant de défendre, tu peux jouer :')}</p>
            {vueQ.autres
              .filter((choix) => !choix.demande)
              .map((choix) => (
                <button
                  key={choix.optionId}
                  type="button"
                  className="essai-choix est-jouer"
                  data-option-id={choix.optionId}
                  aria-disabled={choix.indisponible ? true : undefined}
                  title={choix.sousTexte ?? choix.indisponible ?? choix.nom}
                  onClick={() => {
                    if (!choix.indisponible) choisir(choix.optionId)
                  }}
                >
                  <span>{avecIcones(marquerRessources(choix.nom))}</span>
                </button>
              ))}
          </div>
        ) : null}
        {vueQ.autres
          .filter((choix) => choix.demande)
          .map((choix) => (
            <button
              key={choix.optionId}
              type="button"
              className="essai-choix est-demande"
              data-option-id={choix.optionId}
              aria-disabled={choix.indisponible ? true : undefined}
              title={choix.indisponible ?? choix.nom}
              onClick={() => {
                if (!choix.indisponible) choisir(choix.optionId)
              }}
            >
              <span>{choix.nom}</span>
            </button>
          ))}
        {refus ? (
          <button
            type="button"
            className="essai-choix est-refus"
            data-refus=""
            title={refus.titre}
            onClick={q.interaction.annuler}
          >
            <span>{refus.libelle}</span>
          </button>
        ) : null}
      </div>
    ) : null

  // Le titre court dit l'attaque meme quand l'etape lue est en retard sur la
  // question de defense (elle arrive avant que l'annonce soit lue).
  const nomAttaquant = defenseVue?.acteur?.nom
  const titreBrut =
    defenseVue && nomAttaquant && etapeLue?.titre !== 'attaque'
      ? t('Attaque de %1').replace('%1', nomAttaquant)
      : etapeLue && vuePage
        ? titreCourt(etapeLue, relu ? contexteRelu(vuePage.etape) : ctx)
        : ''
  // LOT 5 (essai, decision 5) : une activation inseree par une carte se dit
  // dans le titre (« Attaque de Rhino (Hydra Jet-Trooper) ») ; d'habitude, le
  // moteur ne remplit `cause` que dans ce cas.
  // LOT 5b (essai, decision 43) : une attaque Rapide se dit comme telle, de l'annonce au resultat.
  const titreRapide =
    essai && etapeLue?.rapide && etapeLue.titre === 'attaque'
      ? etapeLue.auteurNom
        ? t('Attaque Rapide de %1').replace('%1', etapeLue.auteurNom)
        : t('Attaque Rapide')
      : undefined
  // 13/10/2026 (encadré ⑨) : une 2e activation du même ennemi se numérote,
  // « Attaque de Klaw (2e, Hydra Jet-Trooper) ».
  const rangActivation =
    essai && etapeLue?.cause && etapeLue.carteId !== undefined
      ? etapes.filter(
          (e, i) =>
            i <= etapes.findIndex((x) => x.cle === etapeLue.cle) &&
            e.carteId === etapeLue.carteId &&
            (e.titre === 'attaque' || e.titre === 'manigance')
        ).length
      : 0
  const titreSansRang =
    titreRapide ??
    (essai && etapeLue?.cause && (etapeLue.titre === 'attaque' || etapeLue.titre === 'manigance')
      ? `${titreBrut} (${rangActivation >= 2 ? `${t('%1e').replace('%1', String(rangActivation))}, ` : ''}${etapeLue.cause})`
      : titreBrut)
  // 13/10/2026 (encadré ⑩) : « Attaque du Fondeur (sbire 2/3) », seulement à partir de deux sbires.
  const titre =
    essai && etapeLue?.temps === 'sbires' && etapeLue.rangSbire !== undefined && (etapeLue.totalSbires ?? 0) >= 2
      ? `${titreSansRang} (${t('sbire %1/%2').replace('%1', String(etapeLue.rangSbire)).replace('%2', String(etapeLue.totalSbires))})`
      : titreSansRang

  // ESSAI : les boosts se retournent au clic, un par un (questions 3 et 10).
  const boostsRestants =
    (essai && !relu && etape && props.montrerBoostSuivant ? Math.max(0, etape.boosts.length - props.boostsMontres) : 0) +
    (carteCacheeIci ? 1 : 0)
  const compteur =
    essai && etape && !relu && !horsPhase ? compteurDesRevelations(etapes, etape.cle, props.cartesDistribuees) : undefined
  // Essai (13/10/2026) : « Carte rencontre 2/2 · Captain America » en titre, la
  // carte revelee dessous. Le compteur de droite ne garde que les Renforts.
  const rencontre = essai && etapeLue && !relu && !horsPhase ? rencontreDuJoueur(etapes, etapeLue.cle) : undefined
  // 13/10/2026 (encadrés ⑯ ⑰) : la carte de Renfort le dit dans le titre, une
  // remplaçante dit quelle carte elle remplace sous le titre.
  const remplacee =
    rencontre && etapeLue?.reveleePar
      ? precedenteAnnuleePar(etapes, etapes.findIndex((e) => e.cle === etapeLue.cle), etapeLue)
      : undefined
  const titreAffiche = rencontre
    ? `${t('Carte rencontre %1/%2').replace('%1', String(rencontre.rang)).replace('%2', String(rencontre.total))}${rencontre.nom ? ` · ${rencontre.nom}` : ''}${etapeLue?.parSurge ? ` (${t('Renfort')})` : ''}`
    : titre
  const sousTitre = rencontre
    ? remplacee?.cibleNom
      ? `${titre} · ${t('remplace %1').replace('%1', nomNettoye(remplacee.cibleNom) ?? remplacee.cibleNom)}`
      : titre
    : undefined
  // Lot 6 (essai, multi) : ce joueur ne donne pas le rythme, son pied dit qui le donne.
  const multiSansBouton =
    props.multi?.genre === 'regarde' || props.multi?.genre === 'attente-choix' || props.multi?.genre === 'choix-hote'

  // Hors phase, la touche Espace n'est pas a nous (le tour du joueur pose
  // ses propres questions) : « Suivant » tourne la page, « Continuer » ferme.
  const libelleBouton = horsPhase
    ? dernierePage
      ? t('Continuer')
      : t('Suivant')
    : props.defaiteLocale
      ? t('Continuer')
      : etape?.temps === 'bilan'
        ? t('Terminer')
        : t('Suivant (espace)')

  // On attrape le carre sur tout fond libre : jamais sur une carte, un bouton
  // ou un champ, qui gardent leur clic.
  const debutAppui = (evenement: ReactPointerEvent<HTMLElement>) => {
    if (!essai) return
    appui.current.doigt = evenement.pointerType !== 'mouse'
    appui.current.ouvert = false
    window.clearTimeout(appui.current.minuteur)
    if (!appui.current.doigt) return
    const id = (evenement.target as HTMLElement).closest<HTMLElement>('[data-card-id]')?.dataset.cardId
    if (!id) return
    appui.current.minuteur = window.setTimeout(() => {
      appui.current.ouvert = true
      viser(id)
      setIdAppui(id)
    }, DELAI_APPUI_LONG)
  }
  const finAppui = () => {
    if (!essai) return
    window.clearTimeout(appui.current.minuteur)
    if (appui.current.ouvert) {
      viser(undefined)
      setIdAppui(undefined)
    }
  }
  const gestesDuFond = {
    ...props.gestes,
    onPointerDown: (evenement: ReactPointerEvent<HTMLElement>) => {
      debutAppui(evenement)
      if ((evenement.target as HTMLElement).closest('button, [data-card-id], a, input, select, textarea')) return
      props.gestes.onPointerDown(evenement)
    },
    onPointerUp: (evenement: ReactPointerEvent<HTMLElement>) => {
      finAppui()
      props.gestes.onPointerUp(evenement)
    },
    onPointerCancel: () => {
      finAppui()
      props.gestes.onPointerCancel()
    },
  }
  const avalerApresAppuiLong = (evenement: ReactMouseEvent<HTMLElement>) => {
    if (!essai || !appui.current.ouvert) return
    appui.current.ouvert = false
    evenement.preventDefault()
    evenement.stopPropagation()
  }

  // Essai (13/10/2026, decision « pied = Continuer seul ») : les mentions passent
  // en bas du corps ; « Boost N / N retourné » disparait, on voit les cartes.
  const mentions = (
      <span className="deroule-mentions">
        {/* Le joueur a la main : on le dit, et JAMAIS « La suite arrive… »,
            qui parlerait du moteur (piege 3). Une question structuree n'a
            pas besoin qu'on la dise : elle est a l'ecran. */}
        {questionAuJoueur && question === undefined && !q ? (
          <span className="deroule-fenetre" aria-live="polite">
            {etapeEstAnnonce ? texteFenetreReponse() : t('Le moteur attend ta réponse')}
          </span>
        ) : null}
        {attente && !attenteDansLaRangee ? <span className="deroule-pulse">{texteAttenteNommee}</span> : null}
        {props.enAttente && !questionAuJoueur && !attente ? (
          <span className="deroule-attente" aria-live="polite">
            {texteAttente({
              autreJoueur: props.attendUnAutreJoueur,
              nom: props.nomJoueurAttendu,
            })}
          </span>
        ) : null}
        {props.secondesFilet !== undefined ? (
          <span className="deroule-filet" aria-live="polite">
            {texteFiletProche(props.secondesFilet)}
          </span>
        ) : null}
        {props.defaiteLocale ? <span className="deroule-arret">{texteArretDefaite()}</span> : null}
        {props.multi?.genre === 'pret' ? (
          <span className="essai-prets" aria-live="polite">
            {props.multi.pastilles.map((pastille) => (
              <span
                key={pastille.nom}
                className={`essai-pret${pastille.pret ? ' est-pret' : ''}`}
                style={pastille.couleur ? ({ '--couleur-pret': pastille.couleur } as CSSProperties) : undefined}
              >
                {pastille.nom}
                {pastille.pret ? ' ✓' : ''}
              </span>
            ))}
          </span>
        ) : null}
        {props.tempsParDecision > 0 ? <span className="deroule-timeout">{texteTempsParDecision()}</span> : null}
      </span>
  )
  const classes = ['deroule-phase', 'est-scene', 'poignee-glisser']
  if (relu || depuisLeJournal) classes.push('est-relecture')
  if (horsPhase) classes.push('est-hors-phase')
  if (essai) classes.push('est-essai')
  if (props.bis ?? true) classes.push('est-bis')
  if (essai && reduit) classes.push('est-reduit')
  // 13/10/2026 (encadré ②) : un changement de stade secoue la boîte (rien en sobre ni en mouvement réduit).
  if (essai && etapeLue?.titre === 'stade') classes.push('est-secousse')
  if (essai && props.cadre) classes.push(props.cadre.genre === 'commun' ? 'est-cadre-commun' : 'est-cadre-joueur')
  if (essai && props.cadre?.genre === 'joueur' && props.cadre.raye) classes.push('est-cadre-raye')
  // Finition : au telephone, la feuille basse s'agrandit seulement le temps d'une question.
  if (essai && questionAuJoueur) classes.push('a-question')
  const outils = essai ? (
    <span className="essai-outils">
      {props.cadre ? (
        <span
          className="essai-pastille-joueur"
          data-cadre={props.cadre.genre}
          title={props.cadre.genre === 'commun' ? undefined : `${t('Joueur')} ${props.cadre.siege}`}
          aria-hidden={props.cadre.genre === 'commun' ? true : undefined}
        >
          {props.cadre.genre === 'commun' ? null : <b>{`J${props.cadre.siege}`}</b>}
        </span>
      ) : null}
      {compteur && (!rencontre || compteur.ajouts.length > 0) ? (
        <span className="essai-compteur">
          {rencontre ? null : <b>{t('Carte %1 / %2').replace('%1', String(compteur.rang)).replace('%2', String(compteur.total))}</b>}
          {compteur.ajouts.length > 0 ? (
            <small>
              <Texte>{compteur.ajouts.join(' · ')}</Texte>
            </small>
          ) : null}
        </span>
      ) : null}
      <button
        type="button"
        className="essai-reduire"
        aria-pressed={reduit}
        aria-label={reduit ? t('Agrandir le panneau') : t('Réduire le panneau')}
        title={reduit ? t('Agrandir le panneau') : t('Réduire le panneau')}
        onClick={() => setReduit((r) => !r)}
      >
        {reduit ? '▢' : '–'}
      </button>
    </span>
  ) : undefined

  return (
    <CouleursJoueurs.Provider value={props.couleursJoueurs ?? AUCUNE_COULEUR}>
    <NomsSurvolables value={nomsDeLaBoite}>
    <section
      ref={poserSection}
      className={classes.join(' ')}
      style={props.style}
      {...gestesDuFond}
      role="dialog"
      aria-label={horsPhase ? t('Pendant ton tour') : t('Phase du méchant')}
      onMouseOver={survolerSection}
      onMouseLeave={quitterSection}
      onClickCapture={essai ? avalerApresAppuiLong : undefined}
      onContextMenu={
        essai
          ? (evenement) => {
              if ((evenement.target as HTMLElement).closest('[data-card-id]')) evenement.preventDefault()
            }
          : undefined
      }
    >
      <LigneDuHaut
        liste={horsPhase ? [] : liste}
        bandeau={horsPhase ? t('Pendant ton tour') : relu || depuisLeJournal ? t('Relecture') : undefined}
        relire={relire ? (cle) => relire({ temps: cle }) : undefined}
        titre={titreAffiche}
        sousTitre={sousTitre}
        page={sequence.length > 1 ? `${page + 1} / ${sequence.length}` : undefined}
        outils={outils}
        numerosCarres={props.bis ?? true}
      />
      {/* La cle `etape|page` remonte le corps a chaque page : c'est ce qui
          rejoue le glissement d'entree (D35). Entrer en relecture aussi. */}
      <div
        key={`${relu ? 'relu|' : ''}${vuePage?.etape.cle ?? etape?.cle ?? 'sans-etape'}|${page}`}
        className="deroule-corps"
        aria-label={etapeLue ? titreEtape(etapeLue) : undefined}
      >
        {corps}
        {etapeLue?.defaite ? (
          <p className="deroule-defaite">
            <span aria-hidden="true">☠</span> {texteDefaite(etapeLue)}
          </p>
        ) : null}
        {q && vueDuSousCadre ? (
          <SousCadre vue={vueDuSousCadre} q={q} essai={essai} couleurDeCarte={essai ? props.couleurDeCarte : undefined} />
        ) : null}
        {/* Le repli de la table, du telephone et du banc d'essai : la
            question rendue par le plateau. Jamais a cote d'une question
            structuree, qui a deja ses boutons. */}
        {questionAuJoueur && !q && question !== undefined ? (
          <div className="deroule-sous-cadre est-provisoire">{question}</div>
        ) : null}
        {essai ? mentions : null}
      </div>
      {choixDefense}
      {props.multi?.genre === 'choix-hote' ? (
        <div className="essai-choix-avance" role="group" aria-label={t('Qui fait avancer la phase du méchant ?')}>
          <strong>{t('Qui fait avancer la phase du méchant ?')}</strong>
          <span>{t('Ton choix vaut pour toute la partie. Tu pourras le changer dans les réglages.')}</span>
          {(
            [
              ['concerne', t('Le joueur concerné'), t('Celui que l’ennemi vise ou qui révèle ; le premier joueur pour la menace et le bilan.')],
              ['tous', t('Tout le monde valide'), t('Chacun clique « Prêt » ; on avance quand tout le monde l’est.')],
              ['quiconque', t('N’importe qui'), t('Le premier qui clique fait avancer tout le monde.')],
            ] as const
          ).map(([valeur, titre, detail]) => (
            <button
              key={valeur}
              type="button"
              className="bh-bouton essai-choix-avance-option"
              data-politique={valeur}
              onClick={() => (props.multi?.genre === 'choix-hote' ? props.multi.choisir(valeur) : undefined)}
            >
              <b>{titre}</b>
              <small>{detail}</small>
            </button>
          ))}
        </div>
      ) : null}
      <div className="deroule-boutons">
        {essai ? null : mentions}
        {refus && !choixDefense ? (
          <button
            type="button"
            className="bh-bouton"
            data-refus=""
            title={refus.titre}
            onClick={q?.interaction.annuler}
          >
            {refus.libelle}
          </button>
        ) : null}
        {/* EN RELECTURE (D23, D38) : rien ne se valide. « Suivant » montre la
            page ou le coup suivant de la pastille relue ; « Revenir à 2B »
            rend l'etape en cours, « Fermer » referme la relecture du journal. */}
        {relu && !dernierePage ? (
          <button type="button" className="bh-bouton" data-page-suivante="" onClick={tournerLaPage}>
            {t('Suivant')}
          </button>
        ) : null}
        {relu && depuisLeJournal ? (
          <button type="button" className="bh-bouton deroule-suivant" onClick={props.onFermer}>
            {t('Fermer')}
          </button>
        ) : null}
        {relu && !depuisLeJournal ? (
          <button type="button" className="bh-bouton deroule-suivant" onClick={() => relire?.(undefined)}>
            {libelleRevenir}
          </button>
        ) : null}
        {/* Pas de bouton pendant une question : elle a ses propres boutons.
            Ni sur une ANNONCE en cours (piege 2) : elle se complete sur place,
            sans clic ; la rangee resolue, elle, porte toujours « Suivant ».
            Ni pendant qu'un autre joueur choisit sur l'etape en cours (D28). */}
        {/* Un spectateur (ou une relecture) ne valide rien : il tourne les
            pages d'une etape, mais l'etape suit le joueur (etape-partagee.ts). */}
        {multiSansBouton && etape && !relu && !questionAuJoueur ? (
          <button type="button" disabled className="bh-bouton deroule-suivant essai-continuer essai-multi-attente" aria-live="polite">
            {props.multi?.genre === 'regarde'
              ? t('%1 regarde…').replace('%1', props.multi.nom)
              : props.multi?.genre === 'choix-hote'
                ? t('Choisis d’abord qui fait avancer')
                : t('L’hôte choisit qui fait avancer…')}
          </button>
        ) : null}
        {boostsRestants > 0 && !questionAuJoueur && !attenteSurPlace && !multiSansBouton ? (
          <button
            type="button"
            className="bh-bouton deroule-suivant essai-continuer"
            data-boost-suivant=""
            data-page-suivante=""
            onClick={() => (carteCacheeIci ? props.retournerCarte?.() : props.montrerBoostSuivant?.())}
          >
            {t('Continuer')} <kbd>{t('Espace')}</kbd>
          </button>
        ) : null}
        {props.multi?.genre === 'pret' && boostsRestants === 0 && etape && dernierePage && !relu && !questionAuJoueur && !annonceEnCours && !attenteSurPlace ? (
          <button
            type="button"
            disabled={props.multi.pret}
            className="bh-bouton deroule-suivant essai-continuer"
            data-pret=""
            data-page-suivante=""
            onClick={props.multi.marquer}
          >
            {props.multi.pret ? (
              t('Prêt ✓ %1 / %2')
                .replace('%1', String(props.multi.pastilles.filter((p) => p.pret).length))
                .replace('%2', String(props.multi.pastilles.length))
            ) : (
              <>
                {t('Prêt')} <kbd>{t('Espace')}</kbd>
              </>
            )}
          </button>
        ) : null}
        {boostsRestants === 0 && etape && !relu && !questionAuJoueur && !annonceEnCours && !attenteSurPlace && !multiSansBouton && !(props.multi?.genre === 'pret' && dernierePage) ? (
          <button
            type="button"
            // Spectateur : visible, grise et inactif sur la derniere page ; il
            // s'allume quand le joueur passe a l'etape suivante (cle).
            key={dernierePage && estSpectateur() ? `suivant-${etape.cle}` : 'suivant'}
            disabled={dernierePage && estSpectateur()}
            className={`bh-bouton deroule-suivant${essai ? ' essai-continuer' : ''}${
              dernierePage && estSpectateur() ? ' suivant-spectateur' : ''
            }`}
            data-page-suivante={dernierePage ? undefined : ''}
            onClick={() => {
              if (dernierePage) {
                avancer()
                return
              }
              tournerLaPage()
            }}
          >
            {essai && !horsPhase && !props.defaiteLocale && etape.temps !== 'bilan' ? (
              <>
                {t('Continuer')} <kbd>{t('Espace')}</kbd>
              </>
            ) : (
              libelleBouton
            )}
          </button>
        ) : null}
      </div>
      {apercu ? <CarteApercu carte={apercu} classe="au-dessus-du-deroule" /> : null}
    </section>
    </NomsSurvolables>
    </CouleursJoueurs.Provider>
  )
}

/** Ce que les deux cartouches hors du controleur passent au gabarit. */
type CartesDuCartouche = {
  pvMaxParNom?: Map<string, number>
  carteScene?: (id: number, faceVisible: boolean) => ScanCardProps | undefined
  nomFr?: (id: number) => string | undefined
  texteEtoile?: (carteId: number) => string | undefined
  infoCarte?: (id: number) => Partial<Record<string, number>> | undefined
  infoRevelee?: (carteId: number) => InfoRevelee | undefined
}

/** Le decalage pose a la main, en `translate` comme le cartouche de la phase. */
function styleDuDecalage(decalage: { dx: number; dy: number }): CSSProperties | undefined {
  return decalage.dx !== 0 || decalage.dy !== 0 ? { translate: `${decalage.dx}px ${decalage.dy}px` } : undefined
}

export type CartoucheHorsPhaseProps = CartesDuCartouche & {
  /** Les coups du mechant pendant le tour (`etapesHorsPhase`, revelations comprises). */
  coups: EtapeDeroule[]
  /** La question de defense d'un coup annonce, quand c'est le cartouche qui la porte. */
  questionDuMoteur?: QuestionDuMoteur
  questionAuJoueur: boolean
  /**
   * La relecture du journal occupe le bas de l'ecran : rien a dessiner, mais
   * les coups vus restent retenus (demonter les oublierait).
   */
  masque?: boolean
  /** Le cartouche parait ou disparait : board.tsx fait taire la narration du centre. */
  onAffiche?: (affiche: boolean) => void
}

/**
 * « PENDANT TON TOUR » (D26) : le meme cartouche du bas, sans frise, pour un
 * coup du mechant pendant le tour du joueur (attaque, manigance, carte
 * revelee). « Continuer » le referme ; le moteur ne l'attend pas.
 *
 * Reprend la regle de `CoupHorsPhase` (qui sert toujours la table) : un coup a
 * la fois ; ceux deja la au chargement de la page ont ete vus avant. Une
 * ANNONCE ne se montre que quand le cartouche porte sa question de defense
 * (`coupHorsPhaseEnScene`, board.tsx) : sans elle, l'attaque n'a pas encore eu
 * lieu. Et elle se montre alors meme presente au chargement, sans quoi la
 * question n'aurait plus aucun bouton.
 */
export function CartoucheHorsPhase(props: CartoucheHorsPhaseProps) {
  const vus = useRef<Set<string> | undefined>(undefined)
  if (vus.current === undefined) {
    // Une annonce n'est pas « vue » : son resultat, qui garde sa cle, doit
    // encore se montrer.
    vus.current = new Set(props.coups.filter((e) => e.etat !== 'annonce').map((e) => e.cle))
  }
  const [, redessiner] = useState(0)
  const q = props.questionAuJoueur ? props.questionDuMoteur : undefined
  // La defense d'abord : c'est elle qui attend le joueur.
  const enDefense = q ? props.coups.filter((e) => e.etat === 'annonce').pop() : undefined
  const aMontrer = (e: EtapeDeroule) => e.etat !== 'annonce' && !vus.current?.has(e.cle)
  // Le coup a l'ecran y reste jusqu'a « Continuer » : la liste est rangee par
  // temps, et un coup arrive apres lui (Advance revelee fait manigancer Rhino,
  // planche du lot 5) se rangerait devant et prendrait sa place sans un clic.
  const courant = useRef<string | undefined>(undefined)
  const coup =
    enDefense ?? props.coups.find((e) => e.cle === courant.current && aMontrer(e)) ?? props.coups.find(aMontrer)
  courant.current = coup && coup !== enDefense ? coup.cle : courant.current
  const { decalage, gestes } = useGlisserPanneau(`hors-phase|${coup?.cle ?? ''}`)
  const affiche = !props.masque && coup !== undefined
  const { onAffiche } = props
  useEffect(() => {
    onAffiche?.(affiche)
  }, [affiche, onAffiche])
  // Demonte (la phase du mechant commence), il n'est plus a l'ecran.
  useEffect(() => () => onAffiche?.(false), [onAffiche])
  if (props.masque || !coup) return null
  const marquerVu = () => {
    vus.current?.add(coup.cle)
    redessiner((n) => n + 1)
  }
  return (
    <CartouchePhase
      refCartouche={() => {}}
      style={styleDuDecalage(decalage)}
      gestes={gestes}
      etape={coup}
      etapes={[coup]}
      index={0}
      efface={false}
      // La question n'est la sienne que sur l'annonce qu'elle defend : pendant
      // le tour, le moteur interroge sans cesse le joueur (son action), et le
      // coup resolu doit garder son « Continuer ».
      questionAuJoueur={coup === enDefense}
      questionDuMoteur={coup === enDefense ? q : undefined}
      avancer={marquerVu}
      enAttente={false}
      attendUnAutreJoueur={false}
      defaiteLocale={false}
      boostsMontres={coup.boosts.length}
      tempsParDecision={0}
      cartesDistribuees={0}
      pvMaxParNom={props.pvMaxParNom}
      carteScene={props.carteScene}
      nomFr={props.nomFr}
      texteEtoile={props.texteEtoile}
      infoCarte={props.infoCarte}
      infoRevelee={props.infoRevelee}
      bandeau="pendant-ton-tour"
    />
  )
}

/**
 * « REVOIR LA PHASE DU MÉCHANT » depuis le journal (D38) : la phase finie,
 * rouverte dans le cartouche du bas en relecture. Meme rendu que pendant la
 * phase : la distribution fondue dans ④ (D15), les temps vides dits, le bilan
 * en dernier ; les cinq pastilles se relisent, « Fermer » referme.
 */
export function RelectureJournal(props: CartesDuCartouche & { etapes: EtapeDeroule[]; onFermer: () => void }) {
  const { etapes: fondues, cartesDistribuees } = fusionnerDistribution(props.etapes)
  const liste = avecBilan(avecTempsVides(fondues, true), props.pvMaxParNom)
  const [relecture, setRelecture] = useState<{ temps: ClePastille }>()
  const { decalage, gestes } = useGlisserPanneau('relecture-journal')
  // On ouvre sur le premier temps raconte.
  const premiere = liste.map((e) => pastilleDuTemps(e.temps)).find((cle): cle is ClePastille => cle !== undefined)
  const lue = relecture ?? (premiere ? { temps: premiere } : undefined)
  return (
    <CartouchePhase
      refCartouche={() => {}}
      style={styleDuDecalage(decalage)}
      gestes={gestes}
      etape={liste[liste.length - 1]}
      etapes={liste}
      index={liste.length - 1}
      efface={false}
      questionAuJoueur={false}
      avancer={() => {}}
      enAttente={false}
      attendUnAutreJoueur={false}
      defaiteLocale={false}
      boostsMontres={0}
      tempsParDecision={0}
      cartesDistribuees={cartesDistribuees}
      pvMaxParNom={props.pvMaxParNom}
      carteScene={props.carteScene}
      nomFr={props.nomFr}
      texteEtoile={props.texteEtoile}
      infoCarte={props.infoCarte}
      infoRevelee={props.infoRevelee}
      relecture={lue}
      setRelecture={(r) => {
        if (r) setRelecture(r)
      }}
      bandeau="relecture-journal"
      onFermer={props.onFermer}
    />
  )
}
