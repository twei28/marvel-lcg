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
  useEffect,
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
import { avecBilan, type EtapeDeroule, type TempsPhase } from './deroule-phase'
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
import { vueSousCadre, type QuestionDuMoteur, type VueSousCadre } from './sous-cadre'
import { BoutonOption, CarteNue, choixEnTexte, optionDe, SousCadre } from './SousCadre'
import { avecIcones, marquerRessources } from './icones-ressources'
import {
  compteurDesRevelations,
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
      {vignette.legende ? <figcaption className="deroule-legende">{vignette.legende}</figcaption> : null}
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
            <strong className="deroule-resultat-texte">{rangee.resultat.texte}</strong>
            {jauge ? <span className="deroule-jauge">{jauge}</span> : null}
            {rangee.resultat.note ? <small className="deroule-resultat-note">{rangee.resultat.note}</small> : null}
          </span>
        ) : null}
        {rangee.annulee ? (
          <strong className="deroule-annulee-cause">
            {rangee.annulee.cause ? `${t('Annulée')} · ${rangee.annulee.cause}` : t('Annulée')}
          </strong>
        ) : null}
        {fin}
      </div>
      {rangee.lignesEtoile.map((ligne) => (
        <p key={ligne} className="deroule-etoile">
          {ligne}
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
export function PictoBoost({ nombre, etoile = false }: { nombre: number; etoile?: boolean }) {
  const valeur = `${nombre < 0 ? '−' : '+'}${Math.abs(nombre)}`
  const sigle = `${t('BOOST')}${etoile ? ' ★' : ''}`
  return (
    <span className="essai-stat est-boost" role="img" aria-label={`${valeur} ${sigle}`}>
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
        <strong className="deroule-resultat-texte">{rangee.resultat.texte}</strong>
        {jauge ? <span className="deroule-jauge">{jauge}</span> : null}
        {rangee.resultat.note ? <small className="deroule-resultat-note">{rangee.resultat.note}</small> : null}
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
function RangeeEssai({ rangee, grisee }: { rangee: VueRangee; grisee: boolean }) {
  const pose = rangee.pose
  const classes = ['deroule-rangee', 'essai-calcul']
  if (rangee.annulee) classes.push('est-annulee')
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
              <span className="essai-terme">
                <VignetteVue vignette={nue(boost)} />
                <PictoBoost nombre={boost.apport} etoile={boost.etoile} />
                {boost.etoile ? <small className="essai-etoile">{ligne ?? '★'}</small> : null}
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
              {resultat}
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
                {cible === c ? resultat : null}
              </span>
            ))}
          </span>
        ) : null}
        {!cible ? <span className="essai-groupe essai-resultat">{resultat}</span> : null}
        {rangee.annulee ? (
          <strong className="deroule-annulee-cause">
            {rangee.annulee.cause ? `${t('Annulée')} · ${rangee.annulee.cause}` : t('Annulée')}
          </strong>
        ) : null}
      </div>
      {etoiles.map((ligne) => (
        <p key={ligne} className="deroule-etoile">
          {ligne}
        </p>
      ))}
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
          {revelee.surtitreRenfort ? <p className="deroule-surtitre-renfort">{revelee.surtitreRenfort}</p> : null}
          {revelee.typeFr ? <p className="deroule-type">{revelee.typeFr}</p> : null}
          {revelee.lignes.length > 0 ? (
            <ul className="deroule-lignes">
              {revelee.lignes.map((ligne, rang) => (
                <li key={rang}>{ligne}</li>
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
            {maillon.lien ? <span className="deroule-chaine-lien">{`→ ${maillon.lien}`}</span> : null}
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
              {maillon.annulee ? <span className="deroule-chaine-annulee">{maillon.annulee}</span> : null}
            </span>
          </li>
        )
      })}
    </ol>
  )
}

function Stade({ stade, grisee = false }: { stade: VueStade; grisee?: boolean }) {
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
            <li key={delta}>{delta}</li>
          ))}
        </ul>
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
      <span className="deroule-colonne-nom">{colonne.nom}</span> <span className="deroule-jauge">{jauge || cout}</span>
      {colonne.statuts?.map((statut) => (
        <small key={statut} className="deroule-statut">
          {statut}
        </small>
      ))}
    </li>
  )
}

function Bilan({ bilan, grisee = false }: { bilan: VueBilan; grisee?: boolean }) {
  // La phase n'a rien coute : on le dit, plutot que trois colonnes vides.
  if (bilan.vide) return <p className="deroule-vide">{texteBilanVide()}</p>
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
    </div>
  )
}

function Corps({ corps, grisee, essai = false }: { corps: VueCorps; grisee: boolean; essai?: boolean }) {
  switch (corps.genre) {
    case 'rangee':
      return essai && corps.pose ? <RangeeEssai rangee={corps} grisee={grisee} /> : <Rangee rangee={corps} grisee={grisee} />
    case 'revelee':
      return <CarteRevelee revelee={corps} grisee={grisee} essai={essai} />
    case 'stade':
      return <Stade stade={corps} grisee={grisee} />
    case 'bilan':
      return <Bilan bilan={corps} grisee={grisee} />
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
                  <span className="deroule-pastille-nom">{pastille.nom}</span>
                  {pastille.resume ? <small className="deroule-pastille-resume">{pastille.resume}</small> : null}
                  {pastille.compteur ? <small className="deroule-pastille-compteur">{pastille.compteur}</small> : null}
                </>
              )
              return (
                <li
                  key={pastille.cle}
                  className={`deroule-pastille est-${pastille.etat}${pastille.relu ? ' est-relu' : ''}`}
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
          <h2 className="deroule-titre-court">{titre}</h2>
          {outils}
        </div>
      ) : (
        <h2 className="deroule-titre-court">{titre}</h2>
      )}
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
function scansDe(corps: VueCorps | undefined, question: VueSousCadre | undefined, autres: Vignette[]): ScanCardProps[] {
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
        ...(corps.chaine ?? []).map((maillon) => maillon.vignette),
        ...(corps.question?.choix ?? []),
      ])
      break
    case 'stade':
      vignettes([corps.avant, corps.apres])
      break
    case 'bilan':
      vignettes(corps.nouveautes)
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
  const questionSansEtape =
    etape === undefined && questionAuJoueur && (question !== undefined || props.questionDuMoteur !== undefined)
  const montre = !efface && (etape !== undefined || questionSansEtape)
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
  const scans = scansDe(vuePage?.corps, vueQ, [...vignettesAttente, ...(defenseVue?.acteur ? [defenseVue.acteur] : [])])
  const { regardee, survol, quitter } = useApercuSurvol(scans)
  const optionSurvolee = useRef<number | undefined>(undefined)

  if (!montre) return null

  const survolerSection = (evenement: ReactMouseEvent<HTMLElement>) => {
    survol(evenement)
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
    corps = (
      <Rangee
        rangee={defenseVue}
        grisee={false}
        nbChoix={vueQ.defenseurs.length + vueQ.autres.length}
        choix={
          <>
            <span className="deroule-vers" aria-hidden="true">
              →
            </span>
            {[...vueQ.defenseurs, ...vueQ.autres].map((choix) => (
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
            <p className="deroule-question-intitule">{vueQ.intitule}</p>
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
            <span>{choix.defense ? `${t('Défendre avec')} ${choix.defense.source}` : avecIcones(marquerRessources(choix.nom))}</span>
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
  const titre =
    defenseVue && nomAttaquant && etapeLue?.titre !== 'attaque'
      ? t('Attaque de %1').replace('%1', nomAttaquant)
      : etapeLue && vuePage
        ? titreCourt(etapeLue, relu ? contexteRelu(vuePage.etape) : ctx)
        : ''

  // ESSAI : les boosts se retournent au clic, un par un (questions 3 et 10).
  const boostsRestants =
    essai && !relu && etape && props.montrerBoostSuivant ? Math.max(0, etape.boosts.length - props.boostsMontres) : 0
  const compteur =
    essai && etape && !relu && !horsPhase ? compteurDesRevelations(etapes, etape.cle, props.cartesDistribuees) : undefined

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
  const gestesDuFond = {
    ...props.gestes,
    onPointerDown: (evenement: ReactPointerEvent<HTMLElement>) => {
      if ((evenement.target as HTMLElement).closest('button, [data-card-id], a, input, select, textarea')) return
      props.gestes.onPointerDown(evenement)
    },
  }

  const classes = ['deroule-phase', 'est-scene', 'poignee-glisser']
  if (relu || depuisLeJournal) classes.push('est-relecture')
  if (horsPhase) classes.push('est-hors-phase')
  if (essai) classes.push('est-essai')
  if (props.bis ?? true) classes.push('est-bis')
  if (essai && reduit) classes.push('est-reduit')
  const outils = essai ? (
    <span className="essai-outils">
      {compteur ? (
        <span className="essai-compteur">
          <b>{t('Carte %1 / %2').replace('%1', String(compteur.rang)).replace('%2', String(compteur.total))}</b>
          {compteur.ajouts.length > 0 ? <small>{compteur.ajouts.join(' · ')}</small> : null}
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
    <section
      ref={props.refCartouche}
      className={classes.join(' ')}
      style={props.style}
      {...gestesDuFond}
      role="dialog"
      aria-label={horsPhase ? t('Pendant ton tour') : t('Phase du méchant')}
      onMouseOver={survolerSection}
      onMouseLeave={quitterSection}
    >
      <LigneDuHaut
        liste={horsPhase ? [] : liste}
        bandeau={horsPhase ? t('Pendant ton tour') : relu || depuisLeJournal ? t('Relecture') : undefined}
        relire={relire ? (cle) => relire({ temps: cle }) : undefined}
        titre={titre}
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
        {q && vueDuSousCadre ? <SousCadre vue={vueDuSousCadre} q={q} /> : null}
        {/* Le repli de la table, du telephone et du banc d'essai : la
            question rendue par le plateau. Jamais a cote d'une question
            structuree, qui a deja ses boutons. */}
        {questionAuJoueur && !q && question !== undefined ? (
          <div className="deroule-sous-cadre est-provisoire">{question}</div>
        ) : null}
      </div>
      {choixDefense}
      <div className="deroule-boutons">
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
          {essai && etape && etape.boosts.length > 0 && !relu ? (
            <span className="essai-boosts">
              {t('Boost %1 / %2 retourné')
                .replace('%1', String(Math.min(props.boostsMontres, etape.boosts.length)))
                .replace('%2', String(etape.boosts.length))}
            </span>
          ) : null}
          {props.defaiteLocale ? <span className="deroule-arret">{texteArretDefaite()}</span> : null}
          {props.tempsParDecision > 0 ? <span className="deroule-timeout">{texteTempsParDecision()}</span> : null}
        </span>
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
        {boostsRestants > 0 && !questionAuJoueur && !attenteSurPlace ? (
          <button
            type="button"
            className="bh-bouton deroule-suivant essai-continuer"
            data-boost-suivant=""
            data-page-suivante=""
            onClick={() => props.montrerBoostSuivant?.()}
          >
            {t('Continuer')} <kbd>{t('Espace')}</kbd>
          </button>
        ) : null}
        {boostsRestants === 0 && etape && !relu && !questionAuJoueur && !annonceEnCours && !attenteSurPlace ? (
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
      {regardee ? <CarteApercu carte={regardee} classe="au-dessus-du-deroule" /> : null}
    </section>
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
