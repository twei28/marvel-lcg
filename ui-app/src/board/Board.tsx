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
import { ScanCard, type CardEffectDelta, type ScanCardProps } from '../components/ScanCard'
import { nettoyerNarration } from './BarreAction'
import { langueActuelle, t } from './langue'
import { codeMarvelcdb, lireTextesCdb, texteMarvelcdb, type TexteCdb } from './marvelcdb'
import { aScanFr, scansFrActifs } from './scans-fr'
import { TEXTES_FR } from './textes-fr'
import type { EmplacementAffiche, Plateau, UniteAffichee } from './zones'
import type { World } from './world'
import type { EtatInteractif } from './interaction'
import './board.css'

/**
 * Taille de la table, en pixels de scene. Doit coller a la grille de board.css :
 * 16 de marge + 4 rangees de 216 + 3 ecarts de 14 + 16 de marge = 938.
 */
export const SCENE = { largeur: 1920, hauteur: 940 }

/**
 * Le moteur ecrit ses references de carte « [(49,01094) Rhino] ». Sur un
 * plateau on veut lire « Rhino ».
 */
export function lisiblePrompt(brut: string): string {
  return nettoyerNarration(
    brut.replace(/\[\((\d+),[^)]*\)\s*([^\]]*)\]/g, '$2')
  )
}

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
      const echelle = Math.min(width / SCENE.largeur, height / SCENE.hauteur)
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
}: {
  unite: UniteAffichee
  interactifs: Map<number, EtatInteractif>
  effets: Map<number, CardEffectDelta>
  ouvrirPile: (titre: string, cartes: ScanCardProps[]) => void
  bloquerActionsPassives: boolean
  heroActifId?: number
}) {
  // Les statuts (Stunned/Confused/Tough) ne sont PAS des ameliorations : dans le
  // vrai jeu ce sont de petits marqueurs. On les sort de la cascade d'upgrades
  // pour les poser en petit, en bas du personnage.
  const statuts = unite.attachees.filter((a) => a.kind === 'status')
  const upgrades = unite.attachees.filter((a) => a.kind !== 'status')

  // Carte du porteur, avec l'interaction en cours superposee. Si le moteur ne la
  // rend PAS agissante et que c'est une pile publique, un clic l'ouvre pour la
  // regarder (la defausse, la victoire...). L'interaction garde la priorite.
  const porteurBrut = avecInteraction(unite.carte, interactifs, effets)
  // Badge « Active » sur l'identite du joueur dont c'est le tour (hot-seat).
  const porteur =
    heroActifId !== undefined && Number(unite.carte.id) === heroActifId
      ? { ...porteurBrut, estActif: true }
      : porteurBrut
  const cartePorteur =
    !bloquerActionsPassives && !porteur.onSelect && unite.pileContenu
      ? {
          ...porteur,
          onSelect: () => ouvrirPile(unite.pileTitre ?? unite.carte.name, unite.pileContenu!),
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
                {...stage}
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
}: {
  emplacement: EmplacementAffiche
  interactifs: Map<number, EtatInteractif>
  effets: Map<number, CardEffectDelta>
  ouvrirPile: (titre: string, cartes: ScanCardProps[]) => void
  bloquerActionsPassives: boolean
  heroActifId?: number
}) {
  return (
    <section
      className={`plateau-emplacement zone-${emplacement.cle}`}
      style={{ '--n': emplacement.nombreSurLaLigne } as CSSProperties}
      aria-label={emplacement.titre}
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
/** Texte officiel FR de la carte, de deux sources qui ne se marchent pas dessus.
 *
 *  1. Le dictionnaire HORS LIGNE, prioritaire, mais seulement pour les cartes
 *     qui n'ont pas de scan francais : la ou le scan est en francais, le texte
 *     ferait doublon avec l'image.
 *  2. A defaut, le comportement historique : marvelcdb par reseau, sur option,
 *     coupee par defaut. */
export function ApercuMarvelcdb({ codeCarte }: { codeCarte?: string }) {
  const code = codeMarvelcdb(codeCarte)
  const repli = code && scansFrActifs() && !aScanFr(code) ? TEXTES_FR[code] : undefined
  const [texte, setTexte] = useState<TexteCdb | null>(null)
  useEffect(() => {
    setTexte(null)
    if (!code || repli || !lireTextesCdb()) return
    let annule = false
    void texteMarvelcdb(code).then((resultat) => {
      if (!annule) setTexte(resultat)
    })
    return () => {
      annule = true
    }
  }, [code, repli])
  const contenu = repli ?? texte?.text
  if (!contenu) return null
  return (
    <div className="apercu-cdb">
      <span className="apercu-cdb-source">{repli ? t('français') : 'marvelcdb'}</span>
      <p dangerouslySetInnerHTML={{ __html: contenu.replace(/<(?!\/?(b|i|em|strong|br)\b)[^>]*>/g, '') }} />
    </div>
  )
}

export function CarteApercu({
  carte,
  statuts,
}: {
  carte: ScanCardProps
  /** Cartes de statut posees sur ce personnage : montrees comme sur la table. */
  statuts?: ScanCardProps[]
}) {
  const autresFaces = carte.autresFaces ?? []
  const nbFaces = 1 + autresFaces.length
  // Un complot s'agrandit TOUJOURS en paysage, meme si en main il etait montre
  // en portrait pour tenir dans l'eventail (voir card-model : isLandscape).
  const estComplot = carte.kind === 'main-scheme' || carte.kind === 'side-scheme'
  const carteAgrandie = estComplot ? { ...carte, isLandscape: true } : carte
  return (
    <div
      className={`carte-apercu${nbFaces > 1 ? ` a-plusieurs-faces a-faces-${nbFaces}` : ''}`}
      aria-hidden="true"
    >
      {/* Meme composant que sur la table : l'apercu est fidele (cadre, stats,
          pastilles), juste beaucoup plus grand. Jamais agissant. */}
      <div className="apercu-face">
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
    </div>
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
  source: string
  /** Contenu libre de la barre du haut (choix de la source, retour, etc.). */
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
}

const AUCUNE_INTERACTION: Map<number, EtatInteractif> = new Map()

export function Board({
  world,
  playerId,
  plateau,
  source,
  outils,
  actionsPartie,
  bas,
  interactifs = AUCUNE_INTERACTION,
  effets = new Map(),
  onCardClick,
  bloquerActionsPassives = false,
  mainVisibleForcee = false,
  heroActifId,
  journal,
}: BoardProps) {
  const cadre = useRef<HTMLDivElement>(null)
  const { echelle, largeur, hauteur } = useEchelle(cadre)

  const prompt = lisiblePrompt(world.prompt)

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

  const survol = useCallback((evenement: ReactMouseEvent) => {
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

  const carteApercu = apercuId ? cartesParId.get(apercuId) : undefined
  const statutsApercu = apercuId ? statutsParId.get(apercuId) : undefined

  // Pile publique ouverte pour etre regardee (defausse, victoire, retirees...).
  const [pileRegardee, setPileRegardee] = useState<{
    titre: string
    cartes: ScanCardProps[]
  } | null>(null)
  const ouvrirPile = useCallback(
    (titre: string, cartes: ScanCardProps[]) => setPileRegardee({ titre, cartes }),
    []
  )

  return (
    <main className={`plateau${mainVisibleForcee ? ' main-visible-forcee' : ''}`}>
      <header className="plateau-barre">
        {actionsPartie}
        <div className="plateau-etat">
          <span className="plateau-eyebrow">{source}</span>
          <strong>
            Round {world.round_id} · {phaseAffichee(world.phase)}
            {prompt ? ` · ${prompt}` : ''}
          </strong>
        </div>
        <div className="plateau-compte">
          J{playerId} · {plateau.nombreDeCartes} {t('cartes')}
          {plateau.nombreIgnore > 0 ? ` · ${plateau.nombreIgnore} ${t('entrée(s) inattendue(s)')}` : ''}
        </div>
        {outils ? <div className="plateau-outils">{outils}</div> : null}
      </header>

      <div
        className="plateau-cadre"
        ref={cadre}
        onMouseOver={survol}
        onMouseLeave={quitter}
        onPointerUp={cliquerCarte}
      >
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
            if (e.cle === 'deck-special') return null
            if (e.cle === 'terrain-soutien') {
              const deckSpecial = plateau.emplacements.find((x) => x.cle === 'deck-special')
              return (
                <div className="colonne-terrain-soutien" key="colonne-terrain-soutien">
                  {deckSpecial ? (
                    <Emplacement
                      emplacement={deckSpecial}
                      interactifs={interactifs}
                      effets={effets}
                      ouvrirPile={ouvrirPile}
                      bloquerActionsPassives={bloquerActionsPassives}
                      heroActifId={heroActifId}
                    />
                  ) : null}
                  <Emplacement
                    emplacement={e}
                    interactifs={interactifs}
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
                interactifs={interactifs}
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

      {pileRegardee ? (
        <PileRegardee
          titre={pileRegardee.titre}
          cartes={pileRegardee.cartes}
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
  fermer,
}: {
  titre: string
  cartes: ScanCardProps[]
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
          <div className="plateau-regardees-cartes">
            {cartes.map((carte) => (
              <ScanCard {...carte} key={carte.id} />
            ))}
          </div>
        </div>
      </section>
      {apercu ? <CarteApercu carte={apercu} /> : null}
    </div>
  )
}
