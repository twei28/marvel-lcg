// Le niveau 1 : la vue d'etat. Elle tient TOUJOURS a l'ecran, en entier, et ne
// defile jamais. Ce n'est pas le plateau en petit, c'est l'etat de la partie en
// objets condenses.
//
// Elle accepte exactement les BoardProps du plateau PC : c'est ce qui permet a
// board.tsx de choisir l'un ou l'autre sans rien adapter.

import { useLayoutEffect, useMemo, useRef, useState } from 'react'
import { avecInteraction, phaseAffichee, type BoardProps } from '../Board'
import { t } from '../langue'
import type { CardEffectDelta, ScanCardProps } from '../../components/ScanCard'
import type { EtatInteractif } from '../interaction'
import type { EmplacementAffiche, UniteAffichee } from '../zones'
import { BandeHeros, hauteurBandeauxReplies } from './BandeHeros'
import { BandeMobile, BandeResume } from './BandeMobile'
import { repartir, type BandeAffichee, type CleBande } from './bandes'
import { TUILE_PLANCHER } from './condensation'
import { useCouches, useCouchesBoard } from './couches'
import { groupesParJoueur } from './joueurs'
import {
  MESURES_PAR_DEFAUT,
  planifier,
  plancherTuiles,
  type MesuresBande,
} from './degradation'
import { ZoneFocus } from './ZoneFocus'
import './mobile.css'

/**
 * Poids RELATIFS des bandes : pas des pixels absolus. L'espace vertical
 * reellement disponible (mesure sur .pm-bandes, voir useHauteurCadre) est
 * reparti entre les bandes affichees au prorata de ces poids, une fois que
 * chacune a recu son plancher (voir degradation.ts). Ces valeurs viennent des
 * hauteurs de repos de la spec ; ce qui a change (task 11) c'est qu'elles ne
 * sont plus prises pour argent comptant, seulement pour LEURS PROPORTIONS
 * relatives.
 */
const BUDGETS: Record<CleBande, number> = {
  vilain: 140,
  complots: 110,
  terrain: 120,
  rencontre: 64,
  heros: 200,
  main: 76,
}

/** Largeur utile d'une bande : la fenetre moins les marges laterales de mobile.css. */
const MARGES_LATERALES = 20

const AUCUNE_INTERACTION: Map<number, EtatInteractif> = new Map()
const AUCUN_EFFET: Map<number, CardEffectDelta> = new Map()

/**
 * Largeur reelle du cadre, tenue a jour par un ResizeObserver.
 *
 * Meme motif que useEchelle dans Board.tsx : window.resize ne voit pas les
 * changements de mise en page qui ne sont pas des redimensionnements de fenetre
 * (barre d'URL de Chrome mobile qui apparait ou disparait), donc seul un
 * ResizeObserver sur le cadre lui-meme est fiable.
 */
function useLargeurCadre(cadre: React.RefObject<HTMLDivElement | null>) {
  const [largeur, setLargeur] = useState(() => window.innerWidth)

  // useLayoutEffect et non useEffect : la premiere image peinte doit deja
  // etre calculee sur la mesure reelle, pas sur window.innerWidth.
  useLayoutEffect(() => {
    const element = cadre.current
    if (!element) return

    const recalculer = () => {
      const { width } = element.getBoundingClientRect()
      if (width === 0) return
      setLargeur(width)
    }

    recalculer()
    const observateur = new ResizeObserver(recalculer)
    observateur.observe(element)
    return () => observateur.disconnect()
  }, [cadre])

  return largeur
}

/**
 * Hauteur reelle de .pm-bandes (la ligne 1fr entre le HUD et la barre
 * d'action), tenue a jour par un ResizeObserver. Independante du CONTENU de
 * .pm-bandes : min-height:0 dans mobile.css la laisse epouser exactement sa
 * part de grille, quel que soit ce qui est dedans (voir le commentaire sur
 * .pm-bandes dans mobile.css). Mesurer cet element ne boucle donc pas sur
 * lui-meme.
 *
 * C'est la piece qui manquait avant task 11 : BUDGETS etait fixe, sans lien
 * avec l'espace REEL restant apres le HUD et la barre d'action (qui varient
 * avec le contenu). Une bande pouvait donc recevoir un budget que la grille
 * CSS ne lui donnait pas vraiment, et le surplus etait invisible, avale par
 * l'overflow:hidden de .bande-tuiles, sans jamais faire deborder
 * .plateau-mobile ni .pm-bandes eux-memes.
 *
 * useLayoutEffect et non useEffect : avec useEffect, la premiere image peinte
 * de chaque montage et de chaque rotation calculait ses budgets contre
 * window.innerHeight et sur-rendait visiblement pendant une image.
 */
function useHauteurCadre(cadre: React.RefObject<HTMLDivElement | null>) {
  const [hauteur, setHauteur] = useState(() => window.innerHeight)

  useLayoutEffect(() => {
    const element = cadre.current
    if (!element) return

    const recalculer = () => {
      const { height } = element.getBoundingClientRect()
      if (height === 0) return
      setHauteur(height)
    }

    recalculer()
    const observateur = new ResizeObserver(recalculer)
    observateur.observe(element)
    return () => observateur.disconnect()
  }, [cadre])

  return hauteur
}

function nombreFini(valeur: string, defaut: number): number {
  const lu = Number.parseFloat(valeur)
  return Number.isFinite(lu) ? lu : defaut
}

/**
 * Les hauteurs de la boite d'une bande, RELEVEES sur le DOM plutot que
 * recopiees dans une constante. La sonde est une vraie .bande contenant un
 * vrai .bande-titre, posee en absolu et invisible : elle est mesurable des la
 * premiere passe de mise en page, avant meme que les bandes soient dessinees,
 * et elle suit automatiquement mobile.css si ses valeurs changent.
 *
 * MESURES_PAR_DEFAUT ne sert que quand il n'y a rien a mesurer : avant le
 * montage, et sous jsdom qui ne fait aucune mise en page.
 */
function useMesuresBande(sonde: React.RefObject<HTMLDivElement | null>): MesuresBande {
  const [mesures, setMesures] = useState<MesuresBande>(MESURES_PAR_DEFAUT)

  useLayoutEffect(() => {
    const bande = sonde.current
    const titre = bande?.querySelector('.bande-titre')
    if (!bande || !titre) return

    const relever = () => {
      const style = window.getComputedStyle(bande)
      const hauteurTitre = titre.getBoundingClientRect().height
      const relevees: MesuresBande = {
        titre: hauteurTitre > 0 ? hauteurTitre : MESURES_PAR_DEFAUT.titre,
        remplissage:
          nombreFini(style.paddingTop, 0) + nombreFini(style.paddingBottom, 0),
        bordure:
          nombreFini(style.borderTopWidth, 0) + nombreFini(style.borderBottomWidth, 0),
        ecart: nombreFini(style.rowGap, 0),
      }
      setMesures((precedentes) =>
        precedentes.titre === relevees.titre &&
        precedentes.remplissage === relevees.remplissage &&
        precedentes.bordure === relevees.bordure &&
        precedentes.ecart === relevees.ecart
          ? precedentes
          : relevees
      )
    }

    relever()
    const observateur = new ResizeObserver(relever)
    observateur.observe(bande)
    return () => observateur.disconnect()
  }, [sonde])

  return mesures
}

/** Toutes les unites d'une bande, tous emplacements confondus. */
function unitesDe(bande: BandeAffichee): UniteAffichee[] {
  return bande.emplacements.flatMap((emplacement) => emplacement.groupes.flat())
}

/**
 * Combien de bandeaux joueurs REPLIES la bande Heros va empiler : ils prennent
 * de la hauteur EN PLUS des tuiles, le plancher de la bande doit donc les
 * couvrir. Un seul joueur est deplie a la fois, donc tous les autres se
 * replient ; si le siege regarde n'apparait pas parmi les proprietaires (etat
 * degenere), aucun n'est deplie et ils se replient tous.
 */
function nombreDeBandeauxReplies(bande: BandeAffichee, playerId: number): number {
  const soutien = bande.emplacements.find(
    (emplacement: EmplacementAffiche) => emplacement.cle === 'terrain-soutien'
  )
  if (!soutien) return 0
  const joueurs = [...groupesParJoueur(soutien).keys()]
  return joueurs.includes(playerId) ? Math.max(0, joueurs.length - 1) : joueurs.length
}

export function PlateauMobile({
  world,
  playerId,
  plateau,
  outils,
  actionsPartie,
  bas,
  interactifs = AUCUNE_INTERACTION,
  effets = AUCUN_EFFET,
  heroActifId,
  carteFocalisee,
  onFermerCarte,
  selecteurOuvert = false,
  onFermerSelecteur,
  onCardClick,
}: BoardProps) {
  const cadre = useRef<HTMLDivElement>(null)
  const cadreBandes = useRef<HTMLDivElement>(null)
  const sonde = useRef<HTMLDivElement>(null)
  const largeur = useLargeurCadre(cadre)
  const hauteurBandes = useHauteurCadre(cadreBandes)
  const mesures = useMesuresBande(sonde)
  const couches = useCouches()
  const { pile, ouvrir, fermer } = couches
  // Le menu d'actions d'une carte et le selecteur de cibles vivent dans
  // board.tsx : ce pont les inscrit tout de meme dans la pile, pour que le
  // Retour d'Android les ferme au lieu de sortir de la partie (spec S6).
  useCouchesBoard(carteFocalisee, selecteurOuvert, couches, onFermerCarte, onFermerSelecteur)

  // Les memes props d'interaction que sur le plateau PC : sans cela, aucune
  // carte jouable, aucune cible, aucun badge « Actif » et aucune variation de
  // compteur n'etait visible sur mobile. avecInteraction vient de Board.tsx et
  // n'est pas recopie ici : les deux rendus ne peuvent donc pas diverger.
  const bandes = useMemo(() => {
    const brutes = repartir(plateau)
    if (interactifs.size === 0 && effets.size === 0 && heroActifId === undefined) return brutes
    const decorer = (carte: ScanCardProps): ScanCardProps => {
      const avec = avecInteraction(carte, interactifs, effets)
      return heroActifId !== undefined && Number(carte.id) === heroActifId
        ? { ...avec, estActif: true }
        : avec
    }
    return brutes.map((bande) => ({
      ...bande,
      emplacements: bande.emplacements.map((emplacement) => ({
        ...emplacement,
        groupes: emplacement.groupes.map((groupe) =>
          groupe.map((unite) => ({ ...unite, carte: decorer(unite.carte) }))
        ),
      })),
    }))
  }, [plateau, interactifs, effets, heroActifId])

  // Combien de cibles legales chaque bande contient, pendant un ciblage
  // (spec S5 : le niveau 1 marque les bandes qui en portent).
  const ciblesParBande = useMemo(() => {
    const compte = new Map<CleBande, number>()
    for (const bande of bandes) {
      const nombre = unitesDe(bande).filter(
        (unite) => unite.carte.state === 'targetable'
      ).length
      if (nombre > 0) compte.set(bande.cle, nombre)
    }
    return compte
  }, [bandes])

  // Ce que chaque bande exige AU MINIMUM pour ne rien couper, et le poids avec
  // lequel elle se partage ce qui reste. Une bande sans aucune unite n'exige
  // rien : elle ne dessinera ni tuile ni pastille.
  const exigences = useMemo(
    () =>
      bandes.map((bande) => {
        const vide = unitesDe(bande).length === 0
        const replies = bande.cle === 'heros' ? nombreDeBandeauxReplies(bande, playerId) : 0
        const supplement = hauteurBandeauxReplies(replies, mesures.ecart)
        return {
          cle: bande.cle,
          poids: vide ? 0 : BUDGETS[bande.cle],
          plancher: vide ? 0 : plancherTuiles(supplement),
        }
      }),
    [bandes, mesures.ecart, playerId]
  )

  const plan = useMemo(
    () => planifier(exigences, hauteurBandes, mesures),
    [exigences, hauteurBandes, mesures]
  )

  // La feuille de focus la plus recente, meme si un menu de carte est empile
  // PAR-DESSUS elle : le menu recouvre la feuille, il ne la remplace pas, et
  // le Retour doit la retrouver telle quelle.
  const coucheFocus = [...pile].reverse().find((couche) => couche.sorte === 'focus')
  const bandeEnFocus = coucheFocus
    ? bandes.find((bande) => bande.cle === coucheFocus.bande)
    : undefined

  const ouvrirCarte = (carte: ScanCardProps) => {
    if (carte.onSelect) carte.onSelect()
    else onCardClick?.(carte)
  }

  return (
    <div className="plateau-mobile" ref={cadre}>
      {/* Sonde de mesure : une vraie bande, hors flux et invisible, dont
          useMesuresBande releve les hauteurs. Elle remplace la constante
          OVERHEAD_BANDE, qui affirmait 60 px la ou le rendu en vaut 61. */}
      <div className="pm-sonde" aria-hidden="true">
        <div className="bande" ref={sonde}>
          <span className="bande-titre" />
        </div>
      </div>

      <header className="pm-hud">
        <span className="pm-etat">
          <strong>{phaseAffichee(world.phase)}</strong>
          <span className="pm-tour">
            {t('Tour')} {world.round_id}
          </span>
        </span>
        <span className="pm-outils">
          {actionsPartie}
          {outils}
        </span>
      </header>

      <div
        className={`pm-bandes${plan.colonnes === 2 ? ' pm-bandes-deux' : ''}${
          plan.defilement ? ' pm-bandes-defilantes' : ''
        }`}
        ref={cadreBandes}
      >
        {bandes.map((bande) => {
          const onOuvrirBande = () => ouvrir({ sorte: 'focus', bande: bande.cle })
          const cibles = ciblesParBande.get(bande.cle)

          if (plan.modes.get(bande.cle) !== 'tuiles') {
            return (
              <BandeResume
                key={bande.cle}
                bande={bande}
                cibles={cibles}
                onOuvrirBande={onOuvrirBande}
              />
            )
          }

          const budget = {
            largeur: Math.max(0, largeur - MARGES_LATERALES),
            hauteur: plan.hauteurs.get(bande.cle) ?? TUILE_PLANCHER.hauteur,
          }

          return bande.cle === 'heros' ? (
            <BandeHeros
              key={bande.cle}
              bande={bande}
              budget={budget}
              playerId={playerId}
              cibles={cibles}
              ecartGrille={mesures.ecart}
              onOuvrirBande={onOuvrirBande}
              onOuvrirCarte={ouvrirCarte}
            />
          ) : (
            <BandeMobile
              key={bande.cle}
              bande={bande}
              budget={budget}
              cibles={cibles}
              onOuvrirBande={onOuvrirBande}
              onOuvrirCarte={ouvrirCarte}
            />
          )
        })}
      </div>

      {bas ? <div className="pm-barre-action">{bas}</div> : null}

      {bandeEnFocus ? (
        <ZoneFocus
          bande={bandeEnFocus}
          playerId={playerId}
          onFermer={fermer}
          onOuvrirCarte={ouvrirCarte}
        />
      ) : null}
    </div>
  )
}
