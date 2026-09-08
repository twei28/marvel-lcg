// Le plateau. Il dessine le descripteur /get_world, et rien d'autre : il ne
// depend pas du runtime historique et ne connait pas le moteur Python.
//
// Principe repris de l'ancien plateau, mesure sur le jeu : la table a une taille
// FIXE en pixels de scene, et c'est la table entiere qui est mise a l'echelle de
// la fenetre. Consequence voulue : on voit tout, tout le temps, sans defilement.
// L'original faisait exactement cela (scene 1920x1080, scale(min(vw/1920,
// vh/1080)), voir public/js/marvel/scene.js).

import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type MouseEvent as ReactMouseEvent,
  type PointerEvent as ReactPointerEvent,
  type ReactNode,
} from 'react'
import { createPortal } from 'react-dom'
import { ScanCard, type CardEffectDelta, type ScanCardProps } from '../components/ScanCard'
import { langueActuelle, t } from './langue'
import { codeCarteConnu, codeMarvelcdb, lireTextesCdb, texteMarvelcdb, type TexteCdb } from './marvelcdb'
import { usePlacement } from './placement/usePlacement'
import { CoucheGlisser, BulleRefus } from './glisser/CoucheGlisser'
import { cibleSousLePoint, useGlisser, type CibleSurvolee } from './glisser/useGlisser'
import { aScanFr, scansFrActifs } from './scans-fr'
import { TEXTES_FR } from './textes-fr'
import { TEXTES_FR_FANMADE } from './textes-fr-fanmade'
import { pastilleRedondante, type EmplacementAffiche, type GroupeDePile, type Plateau, type UniteAffichee } from './zones'
import type { World } from './world'
import type { EtatInteractif } from './interaction'
import './board.css'

/**
 * Taille de la table, en pixels de scene. Doit coller a la grille de board.css :
 * 16 de marge + 4 rangees de 216 + 3 ecarts de 14 + 16 de marge = 938.
 */
export const SCENE = { largeur: 1920, hauteur: 940 }

/**
 * Libellé français d'une phase du moteur, pour l'AFFICHAGE seulement : la valeur
 * world.phase reste intacte partout où la logique la compare.
 */
const PHASES_FR: Record<string, string> = {
  'Enemy Activation': 'Activation des ennemis',
  'Place Threat': 'Placer la menace',
  'Deal Encounter Cards': 'Attribuer les cartes Rencontre',
  'Reveals Encounter Cards': 'Révéler les cartes Rencontre',
  'End Phase': 'Fin de phase',
  'End Round': 'Fin du round',
  'Start Round': 'Début du round',
  'Resolve Mulligans': 'Mulligans',
  'Scenario Setup': 'Mise en place',
  Initialize: 'Initialisation',
  'Init Finished': 'Prêt',
}

export function phaseAffichee(phase: string): string {
  // En mode anglais, la valeur du moteur EST déjà le libellé d'origine : on
  // court-circuite le mapping FR au lieu de traduire chaque entrée par t().
  if (langueActuelle() === 'en') return phase
  const tour = phase.match(/^Player (\d+) Turn$/)
  if (tour) return `Tour du Joueur ${tour[1]}`
  return PHASES_FR[phase] ?? phase
}

/**
 * Echelle de la table, et hauteur de scene reellement utilisee.
 *
 * L'echelle est celle de l'ancien plateau : min(largeur/1920, hauteur/940), donc
 * la table tient toujours en entier. Mais l'original s'arrete la et laisse deux
 * bandes noires quand la fenetre est plus large que haute. Ici, la hauteur de
 * scene est etiree pour occuper la place restante : les rangees respirent au lieu
 * de laisser du vide. Elle ne descend jamais sous la hauteur minimale, sinon les
 * cartes ne tiendraient plus dans leur rangee.
 *
 * L'echelle est aussi plafonnee a 1 : au-dela, la scene ne grossit plus, elle
 * s'etire (largeur/hauteur ci-dessous) pour occuper le surplus d'ecran. Plusieurs
 * formules CSS divisent par --echelle pour garder une taille fixe a l'ecran
 * (epaisseur de la jauge de PV dans ScanCard.css, --inspect-scale dans board.css) ;
 * les laisser recevoir une echelle superieure a 1 leur ferait retomber sous leur
 * taille minimale sur un tres grand ecran. Plafonner ici, a la source, les corrige
 * toutes d'un coup plutot que de rajouter un clamp() dans chaque fichier CSS qui
 * consomme la variable.
 */
function useEchelle(cadre: React.RefObject<HTMLDivElement | null>) {
  const [mise, setMise] = useState({
    echelle: 1,
    largeur: SCENE.largeur,
    hauteur: SCENE.hauteur,
  })

  useEffect(() => {
    const element = cadre.current
    if (!element) return

    const recalculer = () => {
      const { width, height } = element.getBoundingClientRect()
      if (width === 0 || height === 0) return
      const echelle = Math.min(1, width / SCENE.largeur, height / SCENE.hauteur)
      setMise({
        echelle,
        largeur: Math.max(SCENE.largeur, width / echelle),
        hauteur: Math.max(SCENE.hauteur, height / echelle),
      })
    }

    recalculer()
    const observateur = new ResizeObserver(recalculer)
    observateur.observe(element)
    return () => observateur.disconnect()
  }, [cadre])

  return mise
}

/** Etats de carte poses par l'interaction, par role. */
const ETAT_PAR_ROLE = {
  porteur: 'playable',
  cible: 'targetable',
  'cible-preview': 'targetable',
  ressource: 'playable',
  source: 'source',
  indisponible: 'disabled',
} as const

/**
 * Superpose l'interaction en cours aux props de la carte. Une carte choisie
 * passe en `selected` : c'est un contour, jamais un panneau sur le scan.
 *
 * Exportee, et NON recopiee, parce que le rendu mobile l'applique aussi : deux
 * copies divergeraient, et c'est deja arrive (le mobile ne marquait aucune
 * carte comme jouable, faute d'appeler cette fonction).
 */
export function avecInteraction(
  props: ScanCardProps,
  interactifs: Map<number, EtatInteractif>,
  effets: Map<number, CardEffectDelta>
): ScanCardProps {
  const etat = interactifs.get(Number(props.id))
  if (!etat) return props
  return {
    ...props,
    state: etat.role === 'source' ? 'source' : etat.choisie ? 'selected' : ETAT_PAR_ROLE[etat.role],
    onSelect: etat.agir,
    spentCount: etat.fois,
    targetPulse: etat.pulse,
    effectDelta: effets.get(Number(props.id)),
  }
}

function Unite({
  unite,
  interactifs,
  effets,
  ouvrirPile,
  bloquerActionsPassives,
  heroActifId,
  titreZone,
}: {
  unite: UniteAffichee
  interactifs: Map<number, EtatInteractif>
  effets: Map<number, CardEffectDelta>
  ouvrirPile: (titre: string, cartes: ScanCardProps[], groupes?: GroupeDePile[]) => void
  bloquerActionsPassives: boolean
  heroActifId?: number
  /** Le nom de la zone qui accueille l'unité, pour taire la pastille qui le
   *  répéterait. */
  titreZone?: string
}) {
  // Les statuts (Stunned/Confused/Tough) ne sont PAS des ameliorations : dans le
  // vrai jeu ce sont de petits marqueurs. On les sort de la cascade d'upgrades
  // pour les poser en petit, en bas du personnage.
  const statuts = unite.attachees.filter((a) => a.kind === 'status')
  const upgrades = unite.attachees.filter((a) => a.kind !== 'status')

  // Carte du porteur, avec l'interaction en cours superposee. Si le moteur ne la
  // rend PAS agissante et que c'est une pile publique, un clic l'ouvre pour la
  // regarder (la defausse, la victoire...). L'interaction garde la priorite.
  // La zone dit déjà le type de cette carte ? On tait la pastille, qui le
  // répétait et se posait par-dessus le titre dans les zones étroites.
  const taire = (carte: ScanCardProps): ScanCardProps =>
    titreZone !== undefined && pastilleRedondante(titreZone, carte)
      ? { ...carte, masquerType: true }
      : carte
  const carteNommee = taire(unite.carte)
  const porteurBrut = avecInteraction(carteNommee, interactifs, effets)
  // Badge « Active » sur l'identite du joueur dont c'est le tour (hot-seat).
  const porteur =
    heroActifId !== undefined && Number(unite.carte.id) === heroActifId
      ? { ...porteurBrut, estActif: true }
      : porteurBrut
  const cartePorteur =
    !bloquerActionsPassives && !porteur.onSelect && unite.pileContenu
      ? {
          ...porteur,
          onSelect: () => ouvrirPile(unite.pileTitre ?? unite.carte.name, unite.pileContenu!, unite.pileGroupes),
        }
      : porteur

  return (
    // L'unite garde la largeur de son PORTEUR : les upgrades sont glissees
    // DERRIERE lui et debordent en bas-droite (en absolu), sans pousser les
    // cartes voisines. --i donne le cran de decalage de chaque upgrade.
    <div className="plateau-unite" style={{ '--nb': upgrades.length } as CSSProperties}>
      {/* Phases A VENIR (vilain/complot) : un petit tas DERRIERE la carte, plus
          un bouton loupe qui ouvre la vue de toutes les phases. Purement visuel :
          le clic/survol passe a la carte dessous. */}
      {unite.stagesArriere && unite.stagesArriere.length > 0 ? (
        <>
          {unite.stagesArriere.map((stage, i) => (
            <span
              className="stage-arriere"
              key={stage.id}
              style={{ '--i': i + 1 } as CSSProperties}
              aria-hidden="true"
            >
              <ScanCard
                {...taire(stage)}
                effectDelta={effets.get(Number(stage.id))}
                onSelect={undefined}
                highlight={false}
              />
            </span>
          ))}
          <button
            type="button"
            className="stages-bouton"
            aria-label={`${t('Voir les')} ${unite.stagesTout?.length ?? 0} ${t('stades')}`}
            disabled={bloquerActionsPassives}
            onClick={(evenement) => {
              evenement.stopPropagation()
              if (bloquerActionsPassives) return
              ouvrirPile(unite.stagesTitre ?? t('Stades'), unite.stagesTout ?? [])
            }}
          >
            🔍<b>{unite.stagesTout?.length ?? 0}</b>
          </button>
        </>
      ) : null}

      <ScanCard {...cartePorteur} />
      {upgrades.map((attachee, i) => (
        <span className="est-attachee" key={attachee.id} style={{ '--i': i } as CSSProperties}>
          <ScanCard {...avecInteraction(attachee, interactifs, effets)} />
        </span>
      ))}
      {statuts.length > 0 ? (
        <div className="statuts">
          {statuts.map((statut) => (
            <span className="est-statut" key={statut.id}>
                <ScanCard {...avecInteraction(statut, interactifs, effets)} />
            </span>
          ))}
        </div>
      ) : null}
    </div>
  )
}

function Emplacement({
  emplacement,
  interactifs,
  effets,
  ouvrirPile,
  bloquerActionsPassives,
  heroActifId,
  accueilleLeGlisser = false,
}: {
  emplacement: EmplacementAffiche
  interactifs: Map<number, EtatInteractif>
  effets: Map<number, CardEffectDelta>
  ouvrirPile: (titre: string, cartes: ScanCardProps[], groupes?: GroupeDePile[]) => void
  bloquerActionsPassives: boolean
  heroActifId?: number
  /** Cette zone attend la carte qu'on est en train de glisser. */
  accueilleLeGlisser?: boolean
}) {
  const vide = emplacement.groupes.every((groupe) => groupe.length === 0)
  return (
    <section
      className={`plateau-emplacement zone-${emplacement.cle}${vide ? ' est-vide' : ''}`}
      style={{ '--n': emplacement.nombreSurLaLigne } as CSSProperties}
      aria-label={emplacement.titre}
      // ⚠ `data-zone` EST LA CIBLE DE DEPOT D'UNE CARTE SANS CIBLE : un allie
      // se lache chez les allies, un soutien dans l'aire du heros. Meme
      // convention que `data-tactile` : un attribut, lisible par le geste comme
      // par les tests, plutot qu'un nom de classe a decouper.
      data-zone={emplacement.cle}
      data-zone-accueille={accueilleLeGlisser ? '' : undefined}
    >
      <h2 className="plateau-emplacement-titre">{emplacement.titre}</h2>
      <div className="plateau-cartes">
        {emplacement.groupes.map((groupe, index) => (
          <div className="plateau-groupe" key={groupe[0]?.cle ?? index}>
            {groupe.map((unite) => (
              <Unite
                unite={unite}
                interactifs={interactifs}
                effets={effets}
                ouvrirPile={ouvrirPile}
                bloquerActionsPassives={bloquerActionsPassives}
                heroActifId={heroActifId}
                titreZone={emplacement.titre}
                key={unite.cle}
              />
            ))}
          </div>
        ))}
      </div>
    </section>
  )
}

/**
 * Aperçu au survol : la carte pointée s'affiche EN GRAND dans un panneau fixe,
 * toujours au même endroit, pendant que le plateau ne bouge pas. On peut ainsi
 * balayer les cartes du regard sans qu'un agrandissement sur place n'en cache
 * les voisines. Le panneau ne capte pas la souris (pointer-events: none en CSS)
 * pour ne pas se re-survoler lui-meme.
 */
/** Texte officiel FR de la carte, de trois sources qui ne se marchent pas dessus.
 *
 *  1. Le dictionnaire HORS LIGNE des cartes officielles, mais seulement pour
 *     celles qui n'ont pas de scan francais : la ou le scan est en francais, le
 *     texte ferait doublon avec l'image.
 *  2. Le dictionnaire des packs FAN-MADE, traduit a la main. Ces cartes
 *     n'auront JAMAIS de scan francais ni de page marvelcdb : ce texte est le
 *     seul francais que le joueur verra dessus, et c'est pour elles que ce bloc
 *     compte le plus.
 *  3. A defaut, le comportement historique : marvelcdb par reseau, sur option,
 *     coupee par defaut. */
export function ApercuMarvelcdb({ codeCarte }: { codeCarte?: string }) {
  // Deux codes, deux rôles. `code` sert de CLÉ aux dictionnaires français et
  // accepte le fan-made ; `codeCdb` désigne une page marvelcdb, que seules les
  // cartes officielles possèdent. Les confondre revenait à n'afficher aucun
  // texte français sur le contenu fan-made.
  const code = codeCarteConnu(codeCarte)
  const codeCdb = codeMarvelcdb(codeCarte)
  const repli =
    code && scansFrActifs() && !aScanFr(code)
      ? (TEXTES_FR[code] ?? TEXTES_FR_FANMADE[code])
      : undefined
  const [texte, setTexte] = useState<TexteCdb | null>(null)
  useEffect(() => {
    setTexte(null)
    if (!codeCdb || repli || !lireTextesCdb()) return
    let annule = false
    void texteMarvelcdb(codeCdb).then((resultat) => {
      if (!annule) setTexte(resultat)
    })
    return () => {
      annule = true
    }
  }, [codeCdb, repli])
  const contenu = repli ?? texte?.text
  if (!contenu) return null
  return (
    <div className="apercu-cdb">
      <span className="apercu-cdb-source">{repli ? t('français') : 'marvelcdb'}</span>
      {/* Les sauts de ligne portent la structure de la carte : une capacite par
          ligne. Sans cette conversion, tout se colle en un pave illisible. Ils
          deviennent des <br> APRES le nettoyage, sinon le nettoyage les
          effacerait avec le reste. */}
      <p
        dangerouslySetInnerHTML={{
          __html: contenu.replace(/<(?!\/?(b|i|em|strong|br)\b)[^>]*>/g, '').replace(/\n/g, '<br />'),
        }}
      />
    </div>
  )
}

export function CarteApercu({
  carte,
  statuts,
  classe,
}: {
  carte: ScanCardProps
  /** Cartes de statut posees sur ce personnage : montrees comme sur la table. */
  statuts?: ScanCardProps[]
  /**
   * Classe en plus sur l'apercu. Sert a un appelant qui vit PLUS HAUT que la
   * table : l'apercu est monte dans <body> avec un z-index taille pour passer
   * devant le plateau (400), pas devant un panneau plein ecran. Le bilan de la
   * phase du mechant (540) le recouvrirait sans cela.
   */
  classe?: string
}) {
  const autresFaces = carte.autresFaces ?? []
  const nbFaces = 1 + autresFaces.length
  // Un complot s'agrandit TOUJOURS en paysage, meme si en main il etait montre
  // en portrait pour tenir dans l'eventail (voir card-model : isLandscape).
  const estComplot = carte.kind === 'main-scheme' || carte.kind === 'side-scheme'
  const carteAgrandie = estComplot ? { ...carte, isLandscape: true } : carte

  // L'apercu est le DERNIER servi : il cede la place a tout panneau de decision
  // deja ouvert. Sur une carte recto-verso paysage il fait pres de 930 px de
  // large — sans cette regle il mangeait le centre de la table pendant qu'on
  // choisissait. Il reste ancre a droite tant que la place y est libre.
  // L'aperçu NE BOUGE PAS. Une seule position candidate, donc toujours la même
  // place, quoi qu'il y ait dessous.
  //
  // C'est l'inverse de la règle des panneaux de décision, et c'est voulu. Une
  // décision est rare et il faut lire la carte qu'elle recouvre : elle esquive.
  // Un agrandissement, lui, s'ouvre à CHAQUE survol : s'il change de coin selon
  // ce qui est libre, l'œil doit le rechercher à chaque fois. Essayé, et c'est
  // franchement désagréable — la prévisibilité vaut plus ici que la place
  // gagnée. Il passe simplement devant (z-index 400) : il est transitoire et
  // voulu, alors que le panneau, lui, reste.
  //
  // On garde le hook malgré tout, pour la seule chose qu'il apporte encore ici :
  // l'aperçu est borné à la fenêtre et re-mesuré quand elle change ou quand les
  // images finissent de charger. Il sortait de l'écran par la droite sur une
  // carte recto-verso paysage, qui fait près de 930 px de large.
  const apercu = useRef<HTMLDivElement | null>(null)
  const { style: stylePlacement } = usePlacement(apercu, {
    preferee: 'droite',
    candidats: ['droite'],
    // Une carte SEULE est étroite (~345 px) : elle se range à gauche de la
    // colonne des manigances, qu'elle n'a aucune raison de recouvrir. Une carte
    // recto-verso fait près de 930 px : la borner la pousserait jusqu'au centre,
    // sur le panneau de décision — pour elle, mieux vaut la colonne.
    borneDroite: nbFaces === 1 ? ['.zone-complot-principal'] : undefined,
    signature: `${carte.id}|${nbFaces}`,
  })

  // L'agrandissement est monte DANS <body>, pas dans la table, et c'est ce qui
  // le fait passer DEVANT les boutons de decision.
  //
  // Sans ce portail il vivait a l'interieur de `.plateau`, qui est un contexte
  // d'empilement a `z-index: 1`. Son propre `z-index: 400` ne valait alors que
  // DANS ce contexte : compare aux panneaux, c'est le 1 du parent qui comptait,
  // et 1 perd contre 92. La carte agrandie passait donc sous les boutons quoi
  // qu'on ecrive comme z-index — signale en jeu, et c'est bien ce qu'on voyait.
  return createPortal(
    <div
      ref={apercu}
      className={`carte-apercu${nbFaces > 1 ? ` a-plusieurs-faces a-faces-${nbFaces}` : ''}${classe ? ` ${classe}` : ''}`}
      style={stylePlacement}
      aria-hidden="true"
    >
      {/* Meme composant que sur la table : l'apercu est fidele (cadre, stats,
          pastilles), juste beaucoup plus grand. Jamais agissant.
          `est-paysage` sert au CSS a caler les blocs de texte sous la carte sur
          la LARGEUR de cette carte : l'orientation ne se lit que sur la carte
          elle-meme, qui est leur soeur, pas leur ancetre. */}
      <div className={`apercu-face${carteAgrandie.isLandscape ? ' est-paysage' : ''}`}>
        <ScanCard {...carteAgrandie} onSelect={undefined} highlight={false} />
        {statuts && statuts.length > 0 ? (
          <div className="statuts">
            {statuts.map((statut) => (
              <span className="est-statut" key={statut.id}>
                <ScanCard {...statut} onSelect={undefined} />
              </span>
            ))}
          </div>
        ) : null}
        {/* Mots-cles de la carte avec leur definition : le rappel de regles
            au survol, sans quitter la table. */}
        {!carte.facedown && carte.keywords && carte.keywords.length > 0 ? (
          <dl className="apercu-mots-cles">
            {carte.keywords.map((mot) => (
              <div key={mot.nom}>
                <dt>{mot.nom}</dt>
                <dd>{mot.definition}</dd>
              </div>
            ))}
          </dl>
        ) : null}
        {!carte.facedown ? <ApercuMarvelcdb codeCarte={carte.codeCarte} /> : null}
      </div>
      {/* Carte multi-faces (recto-verso, ou 3 formes comme Ant-Man) : on montre
          AUSSI les autres faces (image seule, badges masques par le CSS car ils
          ne valent pas pour ces faces-la). */}
      {autresFaces.map((face) => (
        <div className="apercu-face apercu-face-autre" key={face}>
          <span className="apercu-face-label">{t('Autre face')}</span>
          <ScanCard
            {...carte}
            imageUrl={face}
            stats={undefined}
            allyHp={undefined}
            schemeThreat={undefined}
            exhausted={false}
            onSelect={undefined}
            highlight={false}
          />
        </div>
      ))}
    </div>,
    document.body
  )
}

export type BoardProps = {
  world: World
  playerId: number
  /**
   * Table deja decoupee. C'est la PAGE qui la construit, parce que l'interaction
   * a besoin de savoir quelles cartes sont reellement dessinees avant de decider
   * lesquelles sont cliquables (voir Plateau.idsAffiches).
   */
  plateau: Plateau
  /** Affiche d'ou vient l'etat regarde (etat enregistre ou partie en cours). */
  /** Contenu libre de la barre du haut (mode d'affichage, joueur regarde). */
  outils?: ReactNode
  /** Actions de partie dans la barre du haut : Undo / Save / Menu. */
  actionsPartie?: ReactNode
  /** Barre du bas : actions du moteur, ou rappel de lecture seule. */
  bas?: ReactNode
  /** Cartes rendues agissantes par l'interaction en cours. */
  interactifs?: Map<number, EtatInteractif>
  /** Variations de compteurs visibles pendant un court instant. */
  effets?: Map<number, CardEffectDelta>
  /** Clic sur une carte qui n'a pas deja une action directe. */
  onCardClick?: (carte: ScanCardProps) => void
  /** Identite du joueur ACTIF (hot-seat) : badge « Active » sur sa carte. */
  heroActifId?: number
  /**
   * Carte dont le MENU D'ACTIONS est ouvert. Le menu appartient a la page, pas
   * au plateau ; le rendu mobile a seulement besoin de savoir qu'il est la pour
   * l'inscrire dans sa pile de couches (le Retour d'Android doit le fermer, pas
   * quitter la partie). Le rendu PC l'ignore.
   */
  carteFocalisee?: number
  /** Ferme ce menu. Appele par le rendu mobile quand le Retour retire sa couche. */
  onFermerCarte?: () => void
  /**
   * Vrai quand le SELECTEUR DE CIBLES hors table est affiche. Meme raison que
   * carteFocalisee : il appartient a la page, mais le rendu mobile doit
   * l'inscrire dans sa pile de couches, sinon le Retour d'Android quitte la
   * partie en plein ciblage. Le rendu PC l'ignore.
   */
  selecteurOuvert?: boolean
  /** Abandonne le ciblage en cours. Appele quand le Retour retire cette couche. */
  onFermerSelecteur?: () => void
  /**
   * Journal du héros affiché. Il occupe une case de la grille de la scène
   * (rangée du bas, colonne de droite) : ce n'est pas un emplacement de cartes,
   * il ne passe donc pas par zones.ts.
   */
  journal?: ReactNode
  /** Pendant l'assistant pas-a-pas, seules les cartes de l'etape active agissent. */
  bloquerActionsPassives?: boolean
  /** Force la main a rester deployee pendant une selection/paiement. */
  mainVisibleForcee?: boolean
  /**
   * Un effet d'ambiance efface les couleurs (le noir et blanc). Le plateau
   * desature alors les SCANS et rend l'aspect par un lisere colore, qui, lui,
   * n'est pas desature parce qu'il est dessine hors de l'image.
   */
  delave?: boolean
  /**
   * Le glisser-deposer. Absent, le plateau se comporte exactement comme avant :
   * c'est ce qui garantit que le geste s'AJOUTE au clic sans rien lui prendre.
   *
   * Le plateau tient le geste et le dessin ; la page, elle, tient les REGLES
   * (quelles cartes se soulevent, ou elles peuvent aller, ce que le lacher
   * declenche). Elle seule connait les options du moteur.
   */
  glisser?: ReglagesGlisser
}

export type ReglagesGlisser = {
  /** Cette carte peut-elle etre soulevee ? */
  estSource: (id: number) => boolean
  /** Les cartes qu'elle peut viser, deja restreintes a ce qui est dessine. */
  ciblesLegales: (sourceId: number) => Set<number>
  /** Les zones du plateau qui l'accueillent quand elle ne vise personne. */
  zonesLegales: (sourceId: number) => Set<string>
  /** Ce qui va se passer, en une ligne, pour l'etiquette qui suit le pointeur. */
  libelle: (sourceId: number, cible: CibleSurvolee) => string | undefined
  /**
   * Le lacher. Rend `undefined` quand l'action est partie, ou la raison du
   * refus, que le plateau affiche en bulle a l'endroit du lacher.
   */
  onDepot: (sourceId: number, cible: CibleSurvolee) => string | undefined
}

const AUCUNE_INTERACTION: Map<number, EtatInteractif> = new Map()

export function Board({
  world,
  playerId,
  plateau,
  outils,
  actionsPartie,
  bas,
  interactifs = AUCUNE_INTERACTION,
  effets = new Map(),
  onCardClick,
  bloquerActionsPassives = false,
  mainVisibleForcee = false,
  delave = false,
  heroActifId,
  journal,
  glisser,
}: BoardProps) {
  const cadre = useRef<HTMLDivElement>(null)
  const { echelle, largeur, hauteur } = useEchelle(cadre)


  // Index id -> carte, pour retrouver la carte survolee (porteurs ET upgrades).
  const cartesParId = useMemo(() => {
    const index = new Map<string, ScanCardProps>()
    for (const emplacement of plateau.emplacements) {
      for (const groupe of emplacement.groupes) {
        for (const unite of groupe) {
          index.set(unite.carte.id, unite.carte)
          for (const attachee of unite.attachees) index.set(attachee.id, attachee)
        }
      }
    }
    return index
  }, [plateau])

  // Index id du personnage -> ses cartes de STATUT, pour les remontrer dans
  // l'aperçu agrandi (comme sur la table).
  const statutsParId = useMemo(() => {
    const index = new Map<string, ScanCardProps[]>()
    for (const emplacement of plateau.emplacements) {
      for (const groupe of emplacement.groupes) {
        for (const unite of groupe) {
          const statuts = unite.attachees.filter((a) => a.kind === 'status')
          if (statuts.length > 0) index.set(unite.carte.id, statuts)
        }
      }
    }
    return index
  }, [plateau])

  // Survol avec petit delai : la carte pointee est mise en aperçu apres ~0,2s,
  // pour que l'aperçu ne clignote pas quand la souris traverse le plateau. On se
  // vide des qu'on ne pointe plus aucune carte.
  const [apercuId, setApercuId] = useState<string | null>(null)
  const minuteur = useRef<number | undefined>(undefined)
  const pointee = useRef<string | null>(null)

  // Pendant un glisser, l'apercu au survol se tait : la carte tenue en main
  // suffit, et un panneau geant en plein geste cacherait la table qu'on vise.
  const enGlisserRef = useRef(false)

  const survol = useCallback((evenement: ReactMouseEvent) => {
    if (enGlisserRef.current) return
    const carte = (evenement.target as HTMLElement).closest<HTMLElement>('.scan-card')
    const id = carte?.dataset.cardId ?? null
    if (id === pointee.current) return
    pointee.current = id
    window.clearTimeout(minuteur.current)
    if (!id) {
      setApercuId(null)
      return
    }
    minuteur.current = window.setTimeout(() => setApercuId(id), 200)
  }, [])

  const quitter = useCallback(() => {
    pointee.current = null
    window.clearTimeout(minuteur.current)
    setApercuId(null)
  }, [])

  const cliquerCarte = useCallback(
    (evenement: ReactPointerEvent<HTMLDivElement>) => {
      if (!onCardClick) return
      const cible = evenement.target
      if (!(cible instanceof HTMLElement)) return
      if (cible.closest('button, a, input, select, textarea')) return
      const element = cible.closest<HTMLElement>('.scan-card')
      const id = element?.dataset.cardId
      if (!id) return
      if (element.classList.contains('est-agissante')) return
      const carte = cartesParId.get(id)
      if (carte) onCardClick(carte)
    },
    [cartesParId, onCardClick]
  )

  useEffect(() => () => window.clearTimeout(minuteur.current), [])

  /* ---- Le glisser-deposer (8 septembre 2026) ------------------------------
     Le plateau tient le GESTE et le DESSIN ; les regles restent a la page, qui
     seule connait les options du moteur. Sans la prop `glisser`, tout ce bloc
     est inerte et le plateau se comporte exactement comme avant. */
  const [refus, setRefus] = useState<{ x: number; y: number; texte: string } | null>(null)
  const minuteurRefus = useRef(0)
  useEffect(() => () => window.clearTimeout(minuteurRefus.current), [])

  const estSourceGlisser = useCallback((id: number) => glisser?.estSource(id) ?? false, [glisser])
  const surDepot = useCallback(
    (sourceId: number, cible: CibleSurvolee, point: { x: number; y: number }) => {
      const raison = glisser?.onDepot(sourceId, cible)
      window.clearTimeout(minuteurRefus.current)
      if (!raison) {
        setRefus(null)
        return
      }
      setRefus({ x: point.x, y: point.y, texte: raison })
      minuteurRefus.current = window.setTimeout(() => setRefus(null), 2600)
    },
    [glisser]
  )
  const { glisse, gestes } = useGlisser({
    estSource: estSourceGlisser,
    cibleSous: cibleSousLePoint,
    onDepot: surDepot,
  })

  const enGlisser = glisse !== null
  enGlisserRef.current = enGlisser
  // L'apercu DEJA ouvert quand le geste commence resterait par-dessus la table.
  useEffect(() => {
    if (!enGlisser) return
    window.clearTimeout(minuteur.current)
    pointee.current = null
    setApercuId(null)
  }, [enGlisser])

  const ciblesDuGlisser = useMemo(
    () => (glisse && glisser ? glisser.ciblesLegales(glisse.sourceId) : undefined),
    [glisse, glisser]
  )
  const zonesDuGlisser = useMemo(
    () => (glisse && glisser ? glisser.zonesLegales(glisse.sourceId) : undefined),
    [glisse, glisser]
  )
  // Les cibles legales s'allument comme le fait deja le menu d'action : meme
  // halo, meme classe CSS, aucune apparence nouvelle a inventer.
  //
  // ⚠ ET TOUTES LA MEME, QUOI QU'ELLES PORTAIENT AVANT. On gardait le role
  // courant de la carte en n'ajoutant que la pulsation : une carte deja
  // marquee `choisie` restait donc en `selected`, dont le halo est BLEU
  // (`--state-glow: rgba(67, 180, 255, .56)`, ScanCard.css). Pendant un geste
  // ca donnait des cibles bleues au milieu de cibles dorees, signale deux fois
  // le 08/09/2026 (« ce halo bleu degueulasse »). Une cible de geste est une
  // cible, un point : meme role, meme couleur, pour toutes.
  //
  // On garde `agir` et les autres champs du role courant : seul l'habillage
  // change, et seulement le temps du geste (ce calcul ne sert que quand
  // `ciblesDuGlisser` n'est pas vide).
  const interactifsEffectifs = useMemo(() => {
    if (!ciblesDuGlisser || ciblesDuGlisser.size === 0) return interactifs
    const avecHalo = new Map(interactifs)
    for (const id of ciblesDuGlisser) {
      const courant = avecHalo.get(id)
      avecHalo.set(id, { ...courant, role: 'cible-preview', choisie: false, pulse: true })
    }
    return avecHalo
  }, [interactifs, ciblesDuGlisser])

  const cibleSurvoleeId = glisse?.cible.carteId
  const zoneSurvolee = glisse?.cible.zone
  const depotRefuse =
    glisse !== null &&
    !(
      (cibleSurvoleeId !== undefined && (ciblesDuGlisser?.has(cibleSurvoleeId) ?? false)) ||
      (cibleSurvoleeId === undefined &&
        zoneSurvolee !== undefined &&
        (zonesDuGlisser?.has(zoneSurvolee) ?? false))
    )
  const libelleGlisser = glisse && glisser ? glisser.libelle(glisse.sourceId, glisse.cible) : undefined

  const carteApercu = apercuId ? cartesParId.get(apercuId) : undefined
  const statutsApercu = apercuId ? statutsParId.get(apercuId) : undefined

  // Pile publique ouverte pour etre regardee (defausse, victoire, retirees...).
  const [pileRegardee, setPileRegardee] = useState<{
    titre: string
    cartes: ScanCardProps[]
    groupes?: GroupeDePile[]
  } | null>(null)
  const ouvrirPile = useCallback(
    (titre: string, cartes: ScanCardProps[], groupes?: GroupeDePile[]) =>
      setPileRegardee({ titre, cartes, groupes }),
    []
  )

  return (
    <main
      className={`plateau${mainVisibleForcee ? ' main-visible-forcee' : ''}${delave ? ' est-delave' : ''}`}
    >
      <header className="plateau-barre">
        {actionsPartie}
        {/* Plus d'etat de partie ni de compteur de cartes ici : le round, la
            phase et l'evenement en cours sont deja dans le Journal, en clair et
            avec leur historique. Les repeter en permanence prenait de la place
            en haut de l'ecran — celle-la meme qui manque a la table.

            SEULE EXCEPTION : l'avertissement ci-dessous. Il ne s'affiche que
            si le descripteur du moteur contient des entrees que le plateau n'a
            pas su lire ; c'est un signal d'anomalie, pas une information de
            jeu, et le perdre reviendrait a dessiner une table incomplete sans
            que personne ne le sache. */}
        {plateau.nombreIgnore > 0 ? (
          <div className="plateau-anomalie" role="status">
            {plateau.nombreIgnore} {t('entrée(s) inattendue(s)')}
          </div>
        ) : null}
        {outils ? <div className="plateau-outils">{outils}</div> : null}
      </header>

      <div
        className={`plateau-cadre${enGlisser ? ' est-en-glisser' : ''}`}
        ref={cadre}
        // Le geste est-il offert en ce moment ? Lisible depuis la page, donc
        // depuis les tests : sans ce temoin, un glisser qui ne demarre pas ne
        // dit pas s'il est refuse (pas notre tour, action deja engagee) ou
        // casse. Cherche pendant une demi-heure le 08/09/2026, faute de l'avoir.
        data-glisser={glisser ? 'offert' : 'absent'}
        onMouseOver={survol}
        onMouseLeave={quitter}
        onPointerDown={gestes.onPointerDown}
        onPointerMove={gestes.onPointerMove}
        // ⚠ LE CLIC PASSE APRES, ET SEULEMENT SI AUCUN GLISSER NE S'ACHEVE.
        // `gestes.onPointerUp` rend `true` quand il vient de lacher une carte :
        // sans cette garde, un lacher declencherait AUSSI le clic sous le
        // pointeur, donc deux actions pour un seul geste.
        onPointerUp={(evenement) => {
          if (gestes.onPointerUp(evenement)) return
          cliquerCarte(evenement)
        }}
        onPointerCancel={gestes.onPointerCancel}
      >
        {/* L'ACCENTUATION DE NETTETE DES SCANS. Une carte mesure 615 px de
            large a la source et 123 px sur la table : une reduction de 5 pour
            1, que le navigateur fait en une passe et qui rend le texte
            cotonneux (« on peut pas faire en sorte que ce soit moins flou ? »,
            08/09/2026). On ne peut pas inventer des pixels, mais on peut
            rendre au resultat le contraste de bord que la reduction lui a
            pris : c'est un masque flou, le meme geste qu'en photo.

            ⚠ `color-interpolation-filters="sRGB"` N'EST PAS FACULTATIF : par
            defaut un filtre SVG travaille en lumiere lineaire, et le meme
            noyau assombrit alors visiblement les cartes.

            ⚠ Le noyau est a somme 1 (2.6 au centre, quatre bras a -0.4) :
            la luminosite moyenne ne bouge pas, seuls les bords se durcissent.
            Plus fort, les lettres blanches prennent un halo noir. */}
        <svg className="plateau-filtres" aria-hidden="true" focusable="false">
          <filter
            id="nettete-scan"
            colorInterpolationFilters="sRGB"
            x="0"
            y="0"
            width="100%"
            height="100%"
          >
            <feConvolveMatrix
              order="3"
              preserveAlpha="true"
              divisor="1"
              kernelMatrix="0 -0.4 0  -0.4 2.6 -0.4  0 -0.4 0"
            />
          </filter>
        </svg>
        <div
          className="plateau-scene"
          style={
            {
              '--echelle': echelle,
              width: `${largeur}px`,
              height: `${hauteur}px`,
            } as CSSProperties
          }
        >
          {plateau.emplacements.map((e) => {
            // Le deck special partage la case « terrain-soutien » : il occupe un
            // slot dedie a GAUCHE, le heros et les soutiens sont a sa droite.
            // La RESERVE de Brawn prend exactement la meme place : c'est la zone
            // personnelle du personnage, comme l'Invocation de Strange. Aucun
            // heros n'a les deux, l'autre slot est donc simplement absent.
            if (e.cle === 'deck-special' || e.cle === 'reserve') return null
            if (e.cle === 'terrain-soutien') {
              const deckSpecial = plateau.emplacements.find((x) => x.cle === 'deck-special')
              const reserve = plateau.emplacements.find((x) => x.cle === 'reserve')
              return (
                <div className="colonne-terrain-soutien" key="colonne-terrain-soutien">
                  {deckSpecial ? (
                    <Emplacement
                      emplacement={deckSpecial}
                      accueilleLeGlisser={zonesDuGlisser?.has(deckSpecial.cle)}
                      interactifs={interactifsEffectifs}
                      effets={effets}
                      ouvrirPile={ouvrirPile}
                      bloquerActionsPassives={bloquerActionsPassives}
                      heroActifId={heroActifId}
                    />
                  ) : null}
                  {reserve ? (
                    <Emplacement
                      emplacement={reserve}
                      accueilleLeGlisser={zonesDuGlisser?.has(reserve.cle)}
                      interactifs={interactifsEffectifs}
                      effets={effets}
                      ouvrirPile={ouvrirPile}
                      bloquerActionsPassives={bloquerActionsPassives}
                      heroActifId={heroActifId}
                    />
                  ) : null}
                  <Emplacement
                    emplacement={e}
                    accueilleLeGlisser={zonesDuGlisser?.has(e.cle)}
                    interactifs={interactifsEffectifs}
                    effets={effets}
                    ouvrirPile={ouvrirPile}
                    bloquerActionsPassives={bloquerActionsPassives}
                    heroActifId={heroActifId}
                  />
                </div>
              )
            }
            return (
              <Emplacement
                emplacement={e}
                accueilleLeGlisser={zonesDuGlisser?.has(e.cle)}
                interactifs={interactifsEffectifs}
                effets={effets}
                ouvrirPile={ouvrirPile}
                bloquerActionsPassives={bloquerActionsPassives}
                heroActifId={heroActifId}
                key={e.cle}
              />
            )
          })}
          {journal}
        </div>
      </div>

      {carteApercu ? <CarteApercu carte={carteApercu} statuts={statutsApercu} /> : null}

      {glisse ? (
        <CoucheGlisser
          glisse={glisse}
          carte={cartesParId.get(String(glisse.sourceId))}
          libelle={libelleGlisser}
          refuse={depotRefuse}
        />
      ) : null}
      {refus ? <BulleRefus x={refus.x} y={refus.y} texte={refus.texte} /> : null}

      {pileRegardee ? (
        <PileRegardee
          titre={pileRegardee.titre}
          cartes={pileRegardee.cartes}
          groupes={pileRegardee.groupes}
          fermer={() => setPileRegardee(null)}
        />
      ) : null}

      {bas}
    </main>
  )
}

/**
 * Une pile publique etalee : toutes ses cartes en grille, par-dessus le plateau.
 * On clique le voile (ou « Close ») pour fermer. Reutilise l'habillage de la
 * modale « cartes regardees ».
 */
function PileRegardee({
  titre,
  cartes,
  groupes,
  fermer,
}: {
  titre: string
  cartes: ScanCardProps[]
  /** Une pile faite de plusieurs : un titre par origine (voir pileFondue). */
  groupes?: GroupeDePile[]
  fermer: () => void
}) {
  // Survol -> aperçu dans le panneau fixe habituel (a droite), comme sur le
  // plateau : les cartes de l'overlay ne grandissent pas sur place.
  const [apercuId, setApercuId] = useState<string | null>(null)
  const parId = useMemo(() => new Map(cartes.map((c) => [c.id, c])), [cartes])
  const survol = useCallback((evenement: ReactMouseEvent) => {
    const carte = (evenement.target as HTMLElement).closest<HTMLElement>('.scan-card')
    setApercuId(carte?.dataset.cardId ?? null)
  }, [])
  const apercu = apercuId ? parId.get(apercuId) : undefined

  return (
    <div className="plateau-regardees-voile" onClick={fermer}>
      <section
        className="plateau-regardees"
        role="dialog"
        aria-label={titre}
        onClick={(evenement) => evenement.stopPropagation()}
        onMouseOver={survol}
        onMouseLeave={() => setApercuId(null)}
      >
        <header className="plateau-regardees-entete">
          <div>
            <span className="plateau-eyebrow">{titre}</span>
            <strong>
              {cartes.length} {cartes.length > 1 ? t('cartes') : t('carte')}
            </strong>
          </div>
          <button type="button" onClick={fermer}>
            {t('Fermer')}
          </button>
        </header>

        <div className="plateau-regardees-corps">
          {groupes && groupes.length > 0 ? (
            groupes.map((groupe) => (
              <section className="plateau-regardees-groupe" key={groupe.cle}>
                <h2>
                  {groupe.titre} · {groupe.cartes.length}
                </h2>
                <div className="plateau-regardees-cartes">
                  {groupe.cartes.map((carte) => (
                    <ScanCard {...carte} key={carte.id} />
                  ))}
                </div>
              </section>
            ))
          ) : (
            <div className="plateau-regardees-cartes">
              {cartes.map((carte) => (
                <ScanCard {...carte} key={carte.id} />
              ))}
            </div>
          )}
        </div>
      </section>
      {apercu ? <CarteApercu carte={apercu} /> : null}
    </div>
  )
}
