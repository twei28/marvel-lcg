// La carte du plateau : un scan, une etiquette de type, et rien d'autre sauf
// les compteurs indispensables.
//
// Ce composant est la seule chose que le plateau sait dessiner. Il a ete extrait
// de la vitrine sans changer son rendu : les regles UX validees avec
// l'utilisateur sont ici, et nulle part ailleurs.
//
//   - pas de panneau pose sur le scan (l'overlay cache la carte) ;
//   - pas de rail lateral de statistiques (trop d'infos) ;
//   - pastilles autorisees : PV, menace, hauteur de pile, stats sur leurs bulles ;
//   - survol / focus clavier = vrai agrandissement, pas de modale.
//
// Il ne connait ni le descripteur du jeu ni les zones : c'est card-model.ts qui
// traduit une carte de partie en props d'ici.
import type { CSSProperties } from 'react'
import { t } from '../board/langue'
import './ScanCard.css'

// Vraies icones de stats (bursts comic) fournies par l'utilisateur. Vite les
// inline en data-URI au build : pas de requete reseau, compatible avec la CSP.
// La couleur ET la forme portent l'info (bleu THW, rouge ATK, vert DEF...), le
// chiffre pose au centre est la valeur COURANTE (deja modifiee par le moteur).
import iconeAtk from './stat-bubbles/attack.png'
import iconeDef from './stat-bubbles/defense.png'
import iconeRec from './stat-bubbles/recover.png'
import iconeThw from './stat-bubbles/thwart.png'
import iconeSch from './stat-bubbles/scheme.png'
import {
  STAT_BUBBLE_POSITIONS,
  type StatBubbleLabel,
  type StatBubblePositions,
} from './stat-bubbles/positions'

const ICONES_STATS: Record<string, string> = {
  ATK: iconeAtk,
  DEF: iconeDef,
  REC: iconeRec,
  THW: iconeThw,
  SCH: iconeSch,
}

const LABELS_BULLES = new Set<string>(['THW', 'ATK', 'DEF', 'REC', 'SCH'])

function estLabelBulle(label: string): label is StatBubbleLabel {
  return LABELS_BULLES.has(label)
}

// Position de CHAQUE stat imprimee, par type de carte, en fractions de la carte
// (x/w = fraction de la largeur, y/h = fraction de la hauteur). Mesures fournies
// par l'utilisateur sur les gabarits. Quand un type est ici, on POSE le badge
// pile sur la stat imprimee (il la recouvre avec la valeur courante). Un type
// absent ne recoit aucune bulle de stat.
const POSITIONS_STATS: Partial<Record<CardKind, StatBubblePositions>> = {
  hero: {
    THW: { x: 0.01, y: 0.15, w: 0.175, h: 0.084 },
    ATK: { x: 0.01, y: 0.295, w: 0.175, h: 0.084 },
    DEF: { x: 0.01, y: 0.442, w: 0.175, h: 0.084 },
  },
  'alter-ego': {
    REC: { x: 0.01, y: 0.15, w: 0.175, h: 0.084 },
  },
  ally: {
    THW: { x: 0.012, y: 0.189, w: 0.19, h: 0.084 },
    ATK: { x: 0.012, y: 0.4, w: 0.19, h: 0.084 },
  },
  minion: {
    SCH: { x: 0.014, y: 0.162, w: 0.17, h: 0.081 },
    ATK: { x: 0.014, y: 0.295, w: 0.17, h: 0.081 },
  },
  // Le vilain varie un peu selon les boites : on part du placement du sbire,
  // a affiner de quelques pixels apres controle visuel si besoin.
  villain: {
    SCH: { x: 0.014, y: 0.162, w: 0.17, h: 0.081 },
    ATK: { x: 0.014, y: 0.295, w: 0.17, h: 0.081 },
  },
}

function positionsStats(kind: CardKind, picId: string | undefined): StatBubblePositions | undefined {
  const generiques = POSITIONS_STATS[kind]
  const calibrees = picId ? STAT_BUBBLE_POSITIONS[picId] : undefined
  if (!generiques && !calibrees) return undefined
  return { ...generiques, ...calibrees }
}

// Vocabulaire d'affichage. Il ne recopie pas les card_type du moteur : plusieurs
// types du moteur partagent la meme grammaire visuelle (un Upgrade et un Support
// se dessinent pareil), et le moteur peut en ajouter sans que l'UI change.
export type CardKind =
  | 'hero'
  | 'alter-ego'
  | 'ally'
  | 'support'
  | 'upgrade'
  | 'event'
  | 'resource'
  | 'villain'
  | 'minion'
  | 'main-scheme'
  | 'side-scheme'
  | 'attachment'
  | 'treachery'
  | 'environment'
  | 'obligation'
  | 'status'
  | 'unknown'

export type CardState =
  | 'ready'
  | 'exhausted'
  | 'selected'
  | 'source'
  | 'playable'
  | 'targetable'
  | 'disabled'
  | 'hidden'

export type CardEffectDelta = {
  value: number
  kind: 'damage' | 'heal' | 'threat'
}

export type ScanCardProps = {
  id: string
  name: string
  kind: CardKind
  /**
   * Cette carte represente le set NEMESIS du joueur : au lieu de son type
   * (« Minion »), l'etiquette affiche « Nemesis », dans un badge distinct.
   */
  estNemesis?: boolean
  /**
   * Carte PAS ENCORE active (villain en attente dans un scenario multi-villains) :
   * grisee et marquee « Waiting », pour la distinguer nettement des menaces qui
   * agissent deja.
   */
  inactif?: boolean
  /**
   * Identite du joueur ACTIF (hot-seat) : badge vert « Active » sur la carte,
   * pour voir d'un coup d'oeil quel heros a la main.
   */
  estActif?: boolean
  /**
   * Pile representant un DECK SPECIAL du heros (Invocation de Strange...) :
   * etiquette « Special deck » et halo violet, pour le distinguer des piles
   * ordinaires posees a cote du heros.
   */
  deckSpecial?: boolean
  /** Cette pile est une DEFAUSSE : petit badge « Discard » sur le cote. */
  discard?: boolean
  /**
   * Remplace l'etiquette de type imprimee en haut par ce texte (ex. le NOM d'un
   * deck special : « Invocation »). Prioritaire sur le type et sur estNemesis.
   */
  labelType?: string
  state?: CardState
  /**
   * Carte epuisee (is_ready === false). Independant de `state` : une carte peut
   * etre a la fois epuisee ET agissante (le heros porte encore des options meme
   * apres avoir attaque), et doit alors garder son inclinaison d'epuisement.
   */
  exhausted?: boolean
  imageUrl: string
  /**
   * Images des autres faces d'une carte multi-faces (recto-verso, ou 3 formes
   * comme Ant-Man). Portees par les props mais rendues seulement par l'apercu
   * agrandi (CarteApercu), pas par la carte de table.
   */
  autresFaces?: string[]
  /** Identifiant du scan, utilise pour les positions calibrees de bulles. */
  picId?: string
  /** Les complots se posent en paysage. Voir isLandscapeType() dans card-model.ts. */
  isLandscape?: boolean
  /**
   * L'image fournie est en portrait alors que la carte se pose en paysage : il
   * faut la tourner d'un quart de tour.
   *
   * C'est le cas de TOUS les scans servis par le jeu, qui les redresse en
   * portrait avant de les envoyer. Ce n'est PAS le cas d'un fichier importe tel
   * quel dans le bundle, deja dans son orientation d'impression. Sans ce
   * drapeau, un plateau correct et une vitrine correcte s'excluent.
   */
  scanIsPortrait?: boolean
  /** Deja formate, par exemple « 1/3 ». Vide = pas de pastille. */
  allyHp?: string
  /** Deja formate, par exemple « 9/12 » ou « 3 ». Vide = pas de pastille. */
  schemeThreat?: string
  /** Compteurs poses sur la carte (supply, pym...) : pastilles en bas du cadre. */
  counters?: Array<{ label: string; value: number }>
  /**
   * Nom du heros PROPRIETAIRE (multi) : badge en bas de la carte, pour savoir a
   * qui appartient cet allie / avec qui ce sbire est engage.
   */
  proprietaire?: string
  /**
   * Camp de la carte : halo VERT autour des cartes du joueur, ROUGE autour des
   * cartes du mechant. Absent = pas de halo. Jamais montre sur une carte face
   * cachee (ce serait divulguer a quel camp elle appartient).
   */
  camp?: 'player' | 'encounter'
  /**
   * Stats actuelles du personnage, posees sur les bulles imprimees du scan :
   * ATK, THW, DEF, REC et SCH. Les valeurs sont celles du moteur, donc deja
   * MODIFIEES par les ameliorations en jeu.
   */
  stats?: Array<{ label: string; value: number }>
  /** La carte montre son dos : aucun compteur, aucun type ne doit fuiter. */
  facedown?: boolean
  /** Posee face cachee sur la table, mais nous avons le droit de la voir. */
  peeking?: boolean
  /** Hauteur d'une pile representee par cette seule carte. */
  pileCount?: number
  /**
   * Le moteur parle de cette carte en ce moment. Glow externe, jamais un
   * overlay. Independant de `state` : une carte engagee peut etre citee par
   * l'evenement en cours, et les deux doivent se voir.
   */
  highlight?: boolean
  /**
   * Rend la carte agissante : la designer choisit une action, une cible, ou
   * depense une ressource. Absent = la carte est seulement regardee.
   */
  onSelect?: () => void
  /** Nombre de fois que cette carte a ete depensee (paiement). */
  spentCount?: number
  /** Cible possible mise en avant depuis le menu d'action. */
  targetPulse?: boolean
  /** Mots-cles de la carte, affiches (avec definition) par l'apercu seulement. */
  keywords?: Array<{ nom: string; definition: string }>
  /** Identifiant catalogue (ex. 01001a) : liens et textes marvelcdb. */
  codeCarte?: string
  /** Variation temporaire d'un compteur, affichee directement sur la carte. */
  effectDelta?: CardEffectDelta
}

// Etiquettes courtes : les cartes sont petites. Ce sont les termes du jeu,
// ceux imprimes sur les cartes et employes par le moteur (card_type).
export const kindLabel: Record<CardKind, string> = {
  hero: 'Héros',
  ally: 'Allié',
  minion: 'Sbire',
  'side-scheme': 'Manigance annexe',
  attachment: 'Attachement',
  treachery: 'Traîtrise',
  'alter-ego': 'Alter ego',
  support: 'Soutien',
  upgrade: 'Amélioration',
  event: 'Événement',
  resource: 'Ressource',
  villain: 'Méchant',
  'main-scheme': 'Manigance principale',
  environment: 'Environnement',
  obligation: 'Obligation',
  status: 'État',
  unknown: 'Carte',
}

export function ScanCard({
  id,
  name,
  kind,
  estNemesis = false,
  inactif = false,
  estActif = false,
  deckSpecial = false,
  discard = false,
  labelType,
  state = 'ready',
  exhausted = false,
  imageUrl,
  picId,
  isLandscape = false,
  scanIsPortrait = false,
  allyHp,
  schemeThreat,
  counters,
  proprietaire,
  camp,
  stats,
  facedown = false,
  peeking = false,
  pileCount,
  highlight = false,
  onSelect,
  spentCount,
  targetPulse = false,
  effectDelta,
}: ScanCardProps) {
  // Une carte qui montre son dos n'annonce ni son type ni ses compteurs :
  // ce serait donner au joueur une information que le moteur lui cache. Le set
  // nemesis, lui, s'annonce « Nemesis » plutot que par le type de sa carte.
  // deckSpecial ne change PLUS l'etiquette (le nom du deck est porte par la
   // zone) : il ne fait que le style violet. L'etiquette reste le type de carte.
  const label = facedown
    ? t(kindLabel.unknown)
    : labelType
      ? labelType
      : estNemesis
        ? t('Némésis')
        : t(kindLabel[kind])
  const hp = facedown ? undefined : allyHp
  const threat = facedown ? undefined : schemeThreat
  const compteurs = facedown ? [] : (counters ?? [])
  // Ce type de carte a-t-il des positions de stats mesurees ? Sinon, aucune stat
  // n'est ajoutee : les autres types de cartes ne portent pas ces bulles.
  const statsCalees = facedown ? undefined : positionsStats(kind, picId)
  const aDesStats = !facedown && stats !== undefined && stats.length > 0

  const classes = [
    'scan-card',
    `kind-${facedown ? 'unknown' : kind}`,
    `state-${state}`,
    exhausted ? 'est-epuise' : '',
    isLandscape ? 'is-landscape' : 'is-portrait',
    isLandscape && scanIsPortrait ? 'scan-a-tourner' : '',
    facedown ? 'is-facedown' : '',
    peeking ? 'is-peeking' : '',
    highlight ? 'is-highlighted' : '',
    targetPulse ? 'is-target-pulse' : '',
    // Secousse/flash a l'impact : la classe suit le badge +N/-N (meme cycle de
    // vie), le CSS ne s'anime que si les animations sont actives.
    effectDelta ? `a-delta-${effectDelta.kind}` : '',
    onSelect ? 'est-agissante' : '',
    // Halo de camp, jamais sur une carte face cachee (n'en revele pas le camp).
    !facedown && camp ? `camp-${camp}` : '',
    !facedown && estNemesis ? 'est-nemesis' : '',
    inactif ? 'est-inactif' : '',
    !facedown && deckSpecial ? 'est-deck-special' : '',
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <article
      className={classes}
      data-card-id={id}
      aria-label={`${name}, ${label}`}
      tabIndex={0}
      role={onSelect ? 'button' : undefined}
      aria-pressed={onSelect ? state === 'selected' : undefined}
      onClick={
        onSelect
          ? (evenement) => {
              evenement.stopPropagation()
              onSelect()
            }
          : undefined
      }
      onKeyDown={
        onSelect
          ? (evenement) => {
              // Une carte agissante se declenche au clavier comme un bouton.
              if (evenement.key === 'Enter' || evenement.key === ' ') {
                evenement.preventDefault()
                onSelect()
              }
            }
          : undefined
      }
    >
      {/* Couche visuelle. C'est ELLE qui grandit au survol, pas la carte, et
          elle ne recoit aucun evenement : sans cela, une carte agrandie
          recouvrirait ses voisines et volerait leurs clics, ce qui rend le
          paiement d'un cout impraticable. La zone sensible reste donc la taille
          normale de la carte. */}
      <div className="scan-visuel">
        <div className="top-strip">
          <span className="kind-pill">{label}</span>
          {inactif ? <span className="pastille-inactif">{t('En attente')}</span> : null}
          {estActif && !facedown ? <span className="pastille-actif">{t('Actif')}</span> : null}
        </div>

        <div className="scan-frame">
          {/* Sans imageUrl, un <img src=""> fait recharger la PAGE au
              navigateur et fait crier React. Le rendu ne change pas pour
              autant : l'image vide etait de toute facon masquee par
              data-missing, et .scan-fallback reste dessous. */}
          {imageUrl ? (
            <img
              src={imageUrl}
              alt=""
              draggable="false"
              onError={(event) => {
                event.currentTarget.dataset.missing = 'true'
              }}
            />
          ) : null}
          <div className="scan-fallback" aria-hidden="true">
            <span>{facedown ? '?' : name}</span>
          </div>

          {pileCount !== undefined ? (
            <span className="pile-count-badge" aria-label={`${pileCount} ${t('cartes dans la pile')}`}>
              <b>{pileCount}</b>
            </span>
          ) : null}

          {discard ? <span className="pastille-discard">{t('Défausse')}</span> : null}

          {spentCount ? (
            <span className="spent-badge" aria-label={`${t('Dépensée')} ${spentCount} ${t('fois')}`}>
              <b>{spentCount > 1 ? `${spentCount}x` : '✓'}</b>
            </span>
          ) : null}

          {hp ? (
            <span className="ally-hp-badge" aria-label={`${t('Points de vie :')} ${hp}`}>
              <b>{hp}</b>
              <span>{t('PV')}</span>
            </span>
          ) : null}

          {threat ? (
            <span className="scheme-threat-badge" aria-label={`${t('Menace :')} ${threat}`}>
              <b>{threat}</b>
              <span>{t('MEN')}</span>
            </span>
          ) : null}

          {compteurs.length > 0 ? (
            <span className="counter-badges" aria-label={t('Compteurs')}>
              {compteurs.map((compteur) => (
                <span className="counter-badge" key={compteur.label}>
                  <b>{compteur.value}</b>
                  <span>{compteur.label}</span>
                </span>
              ))}
            </span>
          ) : null}

          {proprietaire && !facedown ? (
            <span className="proprio-badge" aria-label={`${t('Appartient à')} ${proprietaire}`}>
              {proprietaire}
            </span>
          ) : null}

          {effectDelta ? (
            <span
              className={`card-effect-delta card-effect-${effectDelta.kind}`}
              aria-label={`${effectDelta.value > 0 ? 'Increased' : 'Decreased'} by ${Math.abs(effectDelta.value)}`}
            >
              {effectDelta.value > 0 ? '+' : ''}{effectDelta.value}
            </span>
          ) : null}

          {/* Badges CALES : poses pile sur les stats imprimees, dans le cadre (qui
              rogne), donc entierement sur la carte. La valeur courante recouvre la
              valeur de base. Position et taille en fractions de la carte. */}
          {aDesStats && statsCalees ? (
            <div className="scan-stats-calee" aria-hidden="true">
              {stats!.map((s) => {
                if (!estLabelBulle(s.label)) return null
                const icone = ICONES_STATS[s.label]
                const pos = statsCalees[s.label]
                if (!icone || !pos) return null
                const style: CSSProperties = {}
                style.backgroundImage = `url(${icone})`
                style.left = `${pos.x * 100}%`
                style.top = `${pos.y * 100}%`
                style.width = `${pos.w * 100}%`
                style.height = `${pos.h * 100}%`
                return (
                  <span
                    className={`scan-stat scan-stat-${s.label.toLowerCase()} a-icone a-calee`}
                    key={s.label}
                    style={style}
                  >
                    <b>{s.value}</b>
                  </span>
                )
              })}
            </div>
          ) : null}
        </div>
      </div>
    </article>
  )
}
