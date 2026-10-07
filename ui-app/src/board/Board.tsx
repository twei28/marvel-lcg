// Le plateau. Il dessine le descripteur /get_world, et rien d'autre : il ne
// depend pas du runtime historique et ne connait pas le moteur Python.
//
// Principe repris de l'ancien plateau, mesure sur le jeu : la table a une taille
// FIXE en pixels de scene, et c'est la table entiere qui est mise a l'echelle de
// la fenetre. Consequence voulue : on voit tout, tout le temps, sans defilement.
// L'original faisait exactement cela (scene 1920x1080, scale(min(vw/1920,
// vh/1080)), voir public/js/marvel/scene.js).

import { DISPOSITION_ORIGINE, styleDeGrille, styleDeZone as tailleDeZone, type Disposition } from './table-briques'
import { ACCOMPAGNEMENT, assemblerZones } from './table-rendu'
import { useNomsZones } from './noms-zones'
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
import { JetonsCarte, ScanCard, type CardEffectDelta, type ScanCardProps } from '../components/ScanCard'
import { langueActuelle, t } from './langue'
import { codeCarteConnu, codeMarvelcdb, lireTextesCdb, texteMarvelcdb, type TexteCdb } from './marvelcdb'
import { usePlacement } from './placement/usePlacement'
import { transformDecalage, useGlisserPanneau } from './placement/useGlisserPanneau'
import { CoucheGlisser, BulleRefus } from './glisser/CoucheGlisser'
import { CoucheOrdre } from './ordre/CoucheOrdre'
import { cleDePile, cleDeRangee, ranger, type Ordres } from './ordre/ordre-cartes'
import { useReordonner } from './ordre/useReordonner'
import { cibleSousLePoint, useGlisser, type CibleSurvolee } from './glisser/useGlisser'
import { aScanFr, scansFrActifs } from './scans-fr'
import { TEXTES_FR } from './textes-fr'
import { TEXTES_FR_FANMADE } from './textes-fr-fanmade'
import { pastilleRedondante, type EmplacementAffiche, type GroupeDePile, type Plateau, type UniteAffichee } from './zones'
import type { World } from './world'
import type { EtatInteractif } from './interaction'
import './board.css'
import './bande-manigances.css'

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
 * La LARGEUR DE LA VIGNETTE servie par le moteur, en pixels.
 *
 * `tools/generer_vignettes.py` reduit chaque scan a 246 px sur le petit cote.
 * C'est elle qui borne l'agrandissement de la table : au-dela, le navigateur
 * etire une image trop petite et le texte devient flou. Mesure, pas suppose.
 */
const LARGEUR_VIGNETTE = 246

/** La largeur d'une carte de table a l'echelle 1 (`--card-w`, board.css). */
const LARGEUR_CARTE = 127

/**
 * Jusqu'ou la table peut grandir, sur CET ecran.
 *
 * ⚠ LA BORNE VIENT DE L'IMAGE, PAS D'UN GOUT. Une carte occupe
 * `LARGEUR_CARTE * echelle` pixels CSS, donc `* devicePixelRatio` pixels REELS.
 * Des que ce nombre depasse `LARGEUR_VIGNETTE`, on demande au navigateur
 * d'agrandir une image qu'il n'a pas : les cartes grandissent et deviennent
 * MOINS nettes, ce qui est exactement l'inverse du but.
 *
 * ⚠ ET ELLE NE DESCEND JAMAIS SOUS 1 : sur un ecran a forte densite (dpr 2), la
 * formule donnerait 0,97 et RETRECIRAIT la table par rapport a aujourd'hui. On
 * ne degrade pas l'existant pour appliquer une regle. Le prix a payer est dit
 * franchement : sur un tel ecran, la table ne grandit pas, et le seul levier
 * restant serait de regenerer les vignettes plus grandes.
 */
function echelleMaximale(): number {
  const dpr = typeof window === 'undefined' ? 1 : window.devicePixelRatio || 1
  return Math.max(1, LARGEUR_VIGNETTE / (LARGEUR_CARTE * dpr))
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
 * ⚠ ELLE PEUT DEPASSER 1 DEPUIS LE 14/09/2026, et c'etait tout le probleme.
 * Elle etait plafonnee a 1 : sur un ecran 2560x1440, le plateau disposait de
 * 2560x1316 et dessinait quand meme des cartes de 127 px, toute la place en plus
 * perdue. Constat de l'utilisateur : les cartes sont trop petites pour etre
 * lues. Mesure a l'ecran : sans le plafond, la meme carte passe a 169 px et son
 * texte devient lisible.
 *
 * ⚠ CE QUE LE PLAFOND PROTEGEAIT, ET QUI EST TRAITE AILLEURS. Douze formules CSS
 * divisent par --echelle pour garder une taille FIXE A L'ECRAN quand la table
 * retrecit (epaisseur de la jauge de PV, --inspect-scale, ombres d'un pixel).
 * Leur diviseur est desormais `--echelle-fixe`, qui vaut `min(1, --echelle)` :
 * en dessous de 1 rien ne change, au-dessus ces details grandissent avec le
 * reste de la table, ce qui est le comportement voulu. Voir board.css.
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
      const echelle = Math.min(
        echelleMaximale(),
        width / SCENE.largeur,
        height / SCENE.hauteur
      )
      setMise({
        echelle,
        largeur: Math.max(SCENE.largeur, width / echelle),
        hauteur: Math.max(SCENE.hauteur, height / echelle),
      })
      // Recopiee sur la RACINE pour ce qui vit hors de la scene : le cartouche
      // du bas (cartouche-phase.css) se dimensionne sur la rangee de la main,
      // a l'echelle de la table.
      document.documentElement.style.setProperty('--echelle', String(echelle))
    }

    recalculer()
    const observateur = new ResizeObserver(recalculer)
    observateur.observe(element)
    return () => {
      observateur.disconnect()
      document.documentElement.style.removeProperty('--echelle')
    }
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
    orderNumber: etat.ordre,
    onOrdreReculer: etat.ordreReculer,
    onOrdreAvancer: etat.ordreAvancer,
    onAssignerReste: etat.assignerReste,
    assignerResteQuantite: etat.assignerResteQuantite,
    targetPulse: etat.pulse,
    effectDelta: effets.get(Number(props.id)),
  }
}

/**
 * Les statuts identiques repliés en un seul, avec leur nombre.
 *
 * ⚠ 14/09/2026. `.statuts` est un `flex` sans repli ni limite : chaque statut
 * ajoutait 65 px à une rangée centrée sous une carte de 106. MESURÉ sur le
 * plateau réel : 2 statuts débordent déjà de la carte, 3 font 192 px, 10 font
 * 647 px, soit 270 px de débord de CHAQUE côté, par-dessus les zones voisines.
 * Luke Cage n'a aucune limite de Tenaces (`ThisCanHaveAdditionalTough("Any")`,
 * `62001a.py`) : le cas n'est pas théorique.
 *
 * Dix cartes identiques côte à côte n'apprennent d'ailleurs rien de plus
 * qu'une seule : ce qui compte, c'est le NOMBRE. Le jeu de table empile les
 * mêmes marqueurs, il ne les étale pas.
 *
 * ⚠ ON NE REPLIE PAS UN GROUPE OÙ QUELQU'UN EST CLIQUABLE. Le moteur peut
 * demander de choisir UNE carte de statut (la défausser, la déplacer) : replier
 * mettrait les autres hors d'atteinte et bloquerait le joueur. Même chose pour
 * un statut qui porte un delta (+N/-N) : il a quelque chose à montrer de son
 * propre chef. Dans ces cas-là on les remontre tous, débord compris — un
 * affichage large vaut mieux qu'un coup impossible.
 */
export function grouperStatuts(
  statuts: ScanCardProps[],
  interactifs: Map<number, EtatInteractif>,
  effets: Map<number, CardEffectDelta>
): { carte: ScanCardProps; nombre: number }[] {
  const singulier = statuts.some(
    (s) => interactifs.has(Number(s.id)) || effets.has(Number(s.id))
  )
  if (singulier) return statuts.map((carte) => ({ carte, nombre: 1 }))

  const groupes: { carte: ScanCardProps; nombre: number }[] = []
  for (const statut of statuts) {
    // La CLÉ est le nom, pas l'identifiant d'objet : deux Tenaces sont deux
    // cartes différentes pour le moteur, la même chose pour le joueur.
    const meme = groupes.find((g) => g.carte.name === statut.name)
    if (meme) meme.nombre += 1
    else groupes.push({ carte: statut, nombre: 1 })
  }
  return groupes
}

export function Unite({
  unite,
  interactifs,
  effets,
  ouvrirPile,
  bloquerActionsPassives,
  heroActifId,
  titreZone,
  pilesAccueillantes,
  ordreAmeliorations,
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
  /** Les piles qui accueillent la carte qu'on glisse (mode manuel, question 12). */
  pilesAccueillantes?: Set<string>
  /** Ordre d'affichage choisi par le joueur pour les ameliorations de cette carte. */
  ordreAmeliorations?: number[]
}) {
  const pileAccueille = unite.pile !== undefined && (pilesAccueillantes?.has(unite.pile) ?? false)
  if (unite.pileVide) {
    return (
      <div
        className="plateau-unite pile-vide"
        data-pile={unite.pile}
        data-pile-accueille={pileAccueille ? '' : undefined}
        aria-label={unite.carte.name}
      >
        <span>{unite.carte.name}</span>
      </div>
    )
  }

  // Les statuts (Stunned/Confused/Tough) ne sont PAS des ameliorations : dans le
  // vrai jeu ce sont de petits marqueurs. On les sort de la cascade d'upgrades
  // pour les poser en petit, en bas du personnage.
  const statuts = unite.attachees.filter((a) => a.kind === 'status')
  const upgrades = ranger(
    unite.attachees.filter((a) => a.kind !== 'status'),
    (a) => Number(a.id),
    ordreAmeliorations
  )

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
    <div
      className="plateau-unite"
      style={{ '--nb': upgrades.length } as CSSProperties}
      // ⚠ `data-pile` NE VISE QUE LES VRAIES PILES (tache 5, glisser-depose du
      // mode manuel) : `unite.pile` n'est pose par zones.ts QUE sur un deck,
      // une defausse... jamais sur une carte posee (allie, heros, sbire) ni
      // sur une pile FONDUE de plusieurs origines. Une carte ordinaire n'a
      // donc jamais cet attribut sur SA PROPRE unite, ce qui permet au
      // glisser de distinguer « je lache sur cette pile » de « je lache sur
      // cette carte, j'attache » (`useGlisser.ts`, `cibleSousLePoint`).
      data-pile={unite.pile}
      data-pile-accueille={pileAccueille ? '' : undefined}
    >
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
            data-tactile="stades"
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
        // `--nb-statuts` : le nombre de mini-cartes REELLEMENT dessinees (apres
        // repli). La CSS s'en sert pour serrer la rangee jusqu'a la largeur du
        // porteur : quatre statuts DIFFERENTS (Tenace + Sonne + Desoriente +
        // Exposé) sont possibles sur n'importe quel personnage, et debordaient.
        <div
          className="statuts"
          style={{ '--nb-statuts': grouperStatuts(statuts, interactifs, effets).length } as CSSProperties}
        >
          {grouperStatuts(statuts, interactifs, effets).map(({ carte, nombre }) => (
            <span className="est-statut" key={carte.id}>
              <ScanCard {...avecInteraction(carte, interactifs, effets)} />
              {nombre > 1 ? (
                <span className="statut-nombre" aria-label={`${carte.name} ×${nombre}`}>
                  ×{nombre}
                </span>
              ) : null}
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
  pilesAccueillantes,
  styleDeZone,
  aire,
  ordres,
}: {
  emplacement: EmplacementAffiche
  interactifs: Map<number, EtatInteractif>
  effets: Map<number, CardEffectDelta>
  ouvrirPile: (titre: string, cartes: ScanCardProps[], groupes?: GroupeDePile[]) => void
  bloquerActionsPassives: boolean
  heroActifId?: number
  /** Cette zone attend la carte qu'on est en train de glisser. */
  accueilleLeGlisser?: boolean
  /** Les piles fines qui l'attendent aussi (deck, défausse : question 12). */
  pilesAccueillantes?: Set<string>
  /** La taille des cartes de la zone (`--taille-zone`), table-briques.ts. */
  styleDeZone?: CSSProperties
  /** L'aire de grille de la zone (table-briques.ts), qui prend le pas sur celle de board.css. */
  aire?: string
  /** L'ordre des cartes choisi par le joueur (Alt + glisser), local. */
  ordres?: Ordres
}) {
  const vide = emplacement.groupes.every((groupe) => groupe.length === 0)
  // Une zone ASSEMBLEE (table-rendu.ts) reprend la classe de chaque emplacement
  // d'origine, pour garder leur apparence.
  const origines = emplacement.emplacementsDOrigine ?? [emplacement.cle]
  const classesDOrigine = origines.map((cle) => `zone-${cle}`).join(' ')
  return (
    <section
      className={`plateau-emplacement ${classesDOrigine}${vide ? ' est-vide' : ''}`}
      style={{ '--n': emplacement.nombreSurLaLigne, ...(aire ? { gridArea: aire } : {}), ...styleDeZone } as CSSProperties}
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
        {emplacement.groupes.map((groupeBrut, index) => {
          const rangee = cleDeRangee(
            emplacement.cle,
            index,
            emplacement.proprietaires?.[index],
            emplacement.groupesPiles?.[index]
          )
          const groupe = ranger(groupeBrut, (u) => Number(u.carte.id), ordres?.[rangee])
          return (
          <div
            className="plateau-groupe"
            data-rangee={rangee}
            key={groupeBrut[0]?.cle ?? index}
            // Le SECTEUR de ce groupe (tache 5, glisser-depose) : un
            // emplacement qui melange plusieurs secteurs (`terrain-combat` :
            // allies, ennemis engages, environnement) a besoin de distinguer
            // le groupe vise, pas seulement l'emplacement entier. Absent pour
            // tous les autres emplacements (`groupesPiles` n'est fourni que
            // par `terrain-combat`, zones.ts).
            data-pile={emplacement.groupesPiles?.[index]}
            // Le siege du joueur a qui est ce groupe (lot 5 du 06/10/2026) :
            // une carte lachee dedans, en mode manuel, arrive chez lui.
            data-joueur={emplacement.proprietaires?.[index]}
            // Une zone assemblee de plusieurs origines : chaque groupe garde la
            // cible de depot de SON emplacement d'origine.
            data-zone={origines.length > 1 ? emplacement.groupesDOrigine?.[index] : undefined}
          >
            {groupe.map((unite) => (
              <Unite
                unite={unite}
                interactifs={interactifs}
                effets={effets}
                ouvrirPile={ouvrirPile}
                bloquerActionsPassives={bloquerActionsPassives}
                heroActifId={heroActifId}
                titreZone={emplacement.titre}
                pilesAccueillantes={pilesAccueillantes}
                ordreAmeliorations={ordres?.[cleDePile(Number(unite.carte.id))]}
                key={unite.cle}
              />
            ))}
          </div>
          )
        })}
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
export function ApercuMarvelcdb({ codeCarte, artAlternatif = false }: { codeCarte?: string; artAlternatif?: boolean }) {
  // Deux codes, deux rôles. `code` sert de CLÉ aux dictionnaires français et
  // accepte le fan-made ; `codeCdb` désigne une page marvelcdb, que seules les
  // cartes officielles possèdent. Les confondre revenait à n'afficher aucun
  // texte français sur le contenu fan-made.
  const code = codeCarteConnu(codeCarte)
  const codeCdb = codeMarvelcdb(codeCarte)
  // Un ART ALTERNATIF est un scan anglais, meme sur une carte qui a son scan
  // francais : il faut alors le texte francais de TOUTES les cartes
  // (textes-fr-complets.ts, 700 Ko), charge une fois a la demande.
  const scanAnglais = code !== undefined && scansFrActifs() && (artAlternatif || !aScanFr(code))
  const [textesComplets, setTextesComplets] = useState<Readonly<Record<string, string | undefined>>>()
  useEffect(() => {
    if (!scanAnglais || !artAlternatif || textesComplets) return
    let vivant = true
    import('./textes-fr-complets')
      .then((module) => {
        if (vivant) setTextesComplets(module.TEXTES_FR_COMPLETS)
      })
      .catch(() => undefined)
    return () => {
      vivant = false
    }
  }, [scanAnglais, artAlternatif, textesComplets])
  const repli =
    code && scanAnglais
      ? (TEXTES_FR[code] ?? TEXTES_FR_FANMADE[code] ?? textesComplets?.[code])
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
  raisons,
  classe,
  borneDroite,
}: {
  carte: ScanCardProps
  /** Cartes de statut posees sur ce personnage : montrees comme sur la table. */
  statuts?: ScanCardProps[]
  /**
   * Pourquoi cette carte est injouable, une ligne par action refusee.
   * Deja mises en phrase (voir `raisons-refus.ts`) : l'apercu ne fait que les
   * poser. Vide ou absent quand la carte est jouable, ou quand le moteur n'a
   * rien a dire.
   */
  raisons?: string[]
  /**
   * Classe en plus sur l'apercu. Sert a un appelant qui vit PLUS HAUT que la
   * table : l'apercu est monte dans <body> avec un z-index taille pour passer
   * devant le plateau (400), pas devant un panneau plein ecran. Le bilan de la
   * phase du mechant (540) le recouvrirait sans cela.
   */
  classe?: string
  /** Panneaux a ne pas recouvrir, a la place de la colonne des manigances (le volet du journal). */
  borneDroite?: readonly string[]
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
  // Rien sous la carte quand elle n'a ni jeton ni statut : le bloc vide
  // decalerait l'apercu sans rien dire.
  const aQuelqueChoseDessous =
    (statuts?.length ?? 0) > 0 ||
    !!carte.jetonMenace ||
    !!carte.jetonDegats ||
    (carte.counters?.length ?? 0) > 0

  const apercu = useRef<HTMLDivElement | null>(null)
  const { style: stylePlacement } = usePlacement(apercu, {
    preferee: 'droite',
    candidats: ['droite'],
    // Une carte SEULE est étroite (~345 px) : elle se range à gauche de la
    // colonne des manigances, qu'elle n'a aucune raison de recouvrir. Une carte
    // recto-verso fait près de 930 px : la borner la pousserait jusqu'au centre,
    // sur le panneau de décision — pour elle, mieux vaut la colonne.
    //
    // ⚠ SANS LA BANDE DES MANIGANCES SEULEMENT (signalement du 04/10/2026,
    // « avant c'etait a droite »). Avec la bande, la manigance principale est
    // EN HAUT A GAUCHE : la borner a son bord gauche rejetait l'apercu a
    // gauche de l'ecran. Le selecteur ne trouve alors rien, et l'apercu reste
    // ancre a droite comme avant.
    borneDroite: borneDroite ?? (nbFaces === 1 ? ['.plateau-scene:not(.avec-bande) .zone-complot-principal'] : undefined),
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
        {/* En GRAND, les jetons quittent l'illustration : ils cachaient le
            texte de la carte, qui est justement ce qu'on vient y lire. Ils se
            rangent sous la carte, avec les cartes de statut. Demande de
            l'utilisateur, 09/09/2026. */}
        <ScanCard
          {...carteAgrandie}
          jetonMenace={undefined}
          jetonDegats={undefined}
          counters={undefined}
          onSelect={undefined}
          highlight={false}
          taille="grande"
        />
        {/* POURQUOI ON NE PEUT PAS LA JOUER, juste sous la carte : place apres
            les mots-cles, en petit, on ne le voyait pas (30/09/2026). Une ligne
            par action refusee : le joueur doit savoir LAQUELLE il peut
            debloquer. Rien du tout quand la carte est jouable. */}
        {raisons && raisons.length > 0 ? (
          <div className="apercu-refus" role="note">
            <p className="apercu-refus-titre">
              <span className="apercu-refus-icone" aria-hidden="true">⊘</span>
              {t('Injouable')}
            </p>
            <ul>
              {raisons.map((raison) => (
                <li key={raison}>{raison}</li>
              ))}
            </ul>
          </div>
        ) : null}
        {aQuelqueChoseDessous ? (
          <div className="apercu-dessous">
            <JetonsCarte
              menace={carte.jetonMenace}
              degats={carte.jetonDegats}
              compteurs={carte.counters ?? []}
              dessous
            />
            {/* Repliés comme sur la table (voir `grouperStatuts`). L'aperçu
                est plus large, mais dix Tenaces y déborderaient tout autant,
                et le nombre reste l'information utile. Ici rien n'est
                cliquable (`onSelect: undefined`) : on peut toujours replier. */}
            {grouperStatuts(statuts ?? [], new Map(), new Map()).map(({ carte: statut, nombre }) => (
              <span className="est-statut" key={statut.id}>
                <ScanCard {...statut} onSelect={undefined} />
                {nombre > 1 ? (
                  <span className="statut-nombre" aria-label={`${statut.name} ×${nombre}`}>
                    ×{nombre}
                  </span>
                ) : null}
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
        {/* CRISE : le complot principal est verrouille par une manigance
            annexe. Un contre qui le vise part sans effet ; on le dit AVANT que
            le joueur ne joue sa carte (rapport joueur du 11/09/2026). */}
        {/* Le picto est sur la carte (filigrane, ScanCard) ; ici, la seule
            chose qu'il ne dit pas : QUELLE carte verrouille. Une ligne sobre,
            pas un pave rouge. */}
        {carte.crise && !carte.facedown ? (
          <p
            className="apercu-crise-ligne"
            title={`${t('Crise : la menace ne peut pas être retirée d’ici tant que')} ${carte.crise} ${t('est en jeu.')}`}
          >
            {t('Crise')} · <b>{carte.crise}</b>
          </p>
        ) : null}
        {!carte.facedown ? <ApercuMarvelcdb codeCarte={carte.codeCarte} artAlternatif={carte.artAlternatif} /> : null}
      </div>
      {/* Carte multi-faces (recto-verso, ou 3 formes comme Ant-Man) : on montre
          AUSSI les autres faces (image seule, badges masques par le CSS car ils
          ne valent pas pour ces faces-la). */}
      {autresFaces.map((face) => (
        <div
          className={`apercu-face apercu-face-autre${(face.isLandscape ?? carteAgrandie.isLandscape) ? ' est-paysage' : ''}`}
          key={face.url}
        >
          <span className="apercu-face-label">{t('Autre face')}</span>
          {/* CHAQUE face porte son orientation : le verso portrait d'un complot
              ne doit pas heriter du cadre paysage de la face visible. Sans type
              connu, on garde celle de la face visible, comme avant. */}
          <ScanCard
            {...carte}
            imageUrl={face.url}
            isLandscape={face.isLandscape ?? carteAgrandie.isLandscape}
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
  /** La partie en cours : l'ordre rangé à la main n'est gardé que pour elle. */
  identitePartie?: string
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
  /**
   * POURQUOI telle carte est injouable, par identifiant d'objet, deja mis en
   * phrase (`raisons-refus.ts`). C'est la PAGE qui les construit depuis
   * `demande.refus`, comme elle construit `interactifs` : le plateau ne parle
   * pas au moteur.
   */
  raisonsRefus?: Map<number, string[]>
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
   * Le bouton d'action principal du telephone (Fin du tour, et sa variante
   * suggeree) : le portrait le pose dans son bandeau (spec du 12/09/2026).
   * Le plateau PC l'ignore, il garde son bouton flottant.
   */
  actionPrincipale?: { libelle: string; suggere?: boolean; agir: () => void }
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
  /**
   * La BANDE DES MANIGANCES (plateau PC) : le mechant colle au deck rencontre,
   * puis la manigance principale et les annexes sur toute la largeur du haut.
   * Voir `bande-manigances.css`.
   */
  bandeManigances?: boolean
  /**
   * LA DISPOSITION DE LA TABLE (table personnalisable, 04/10/2026), lue avec
   * la bande des manigances seulement (plateau PC). Absente : celle d'origine.
   */
  disposition?: Disposition
  /**
   * Une couche posee DANS la scene, sur sa grille (l'editeur de la table,
   * EditeurTable). Plateau PC seulement.
   */
  superposition?: ReactNode
  /**
   * « À toi de jouer », « Le méchant agit »... Déjà calculé par board.tsx pour
   * sa propre barre (libelleQuiAgit a besoin de aNous/connecte/demande, que ce
   * plateau ne connaît pas) : le rendu portrait n'a qu'à l'afficher tel quel.
   */
  quiAgit?: string
  /**
   * Onglets du multijoueur sur telephone (tache 10) : PAS un nouvel etat, la
   * MEME bascule que les boutons « Vue » de la barre PC (`vueForcee` dans
   * board.tsx). `construirePlateau` braque deja toute la table — heros,
   * allies/engages, reserve, nemesis, main comprise — sur un seul joueur
   * (zones.ts : « notre = joueurs[options.playerId] ») : changer CE joueur
   * suffit, aucun filtrage a faire dans le rendu portrait lui-meme.
   *
   * Les trois props ci-dessous sont optionnelles : le plateau PC/paysage garde
   * son propre bouton « Vue » et continue de fonctionner sans elles.
   */
  /** Les joueurs qu'on peut aller regarder (elimines deja exclus). */
  joueursAffichables?: Array<{ id: number; nom: string }>
  /** Le joueur actuellement regarde : c'est deja `playerId` ci-dessus (la
   *  table et la main recues sont les siennes), redonne ici explicitement
   *  pour que l'onglet actif ne depende pas de le deviner depuis `playerId`. */
  joueurRegarde?: number
  /** Force la vue sur cet id (memes id que `joueursAffichables`). */
  choisirJoueurRegarde?: (id: number) => void
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
   * Le lacher sera-t-il accepte ? Optionnel (lot 2 du 06/10/2026, mode
   * manuel) : absent, le plateau le deduit des cibles et zones legales comme
   * avant. Present, il decide seul du rouge : un lacher qui ne fait rien (une
   * carte deja en jeu relachee sur la table) n'est pas un refus.
   */
  accepte?: (sourceId: number, cible: CibleSurvolee) => boolean
  /**
   * Mode manuel, au doigt (question 11) : la carte se glisse au lieu de faire
   * defiler la page, et l'appui long appartient au menu du clic droit
   * (CoucheTriche), plus a l'action du portrait.
   */
  auDoigt?: boolean
  /** La table entiere accueille-t-elle cette carte ? Un seul cadre autour du plateau (question 12). */
  accueilleLaTable?: (sourceId: number) => boolean
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
  raisonsRefus,
  onCardClick,
  bloquerActionsPassives = false,
  mainVisibleForcee = false,
  delave = false,
  heroActifId,
  journal,
  glisser,
  bandeManigances = false,
  disposition = DISPOSITION_ORIGINE,
  superposition,
  identitePartie,
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

  // Alt : l'aperçu tout de suite, sans le délai du survol. Convention
  // Tabletop Simulator, et le seul raccourci qui ne change pas l'état de la
  // partie — il n'est donc pas réservé au mode manuel, contrairement au
  // clavier d'action (voir `manuel/clavier.ts`, `CoucheTriche.tsx`).
  useEffect(() => {
    const surAlt = (evenement: KeyboardEvent) => {
      if (evenement.key !== 'Alt') return
      window.clearTimeout(minuteur.current)
      if (evenement.type === 'keydown') setApercuId(pointee.current)
      else setApercuId(null)
    }
    document.addEventListener('keydown', surAlt)
    document.addEventListener('keyup', surAlt)
    return () => {
      document.removeEventListener('keydown', surAlt)
      document.removeEventListener('keyup', surAlt)
    }
  }, [])

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

  const reordre = useReordonner(identitePartie)
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
  // Le secteur fin (C1) : distinct de `zone`, il ne sert qu'au mode manuel
  // (l'engagement d'un sbire lâché dans l'espace vide des ennemis engagés).
  // Le mode ordinaire ne pose jamais de secteur dans `zonesLegales`, donc ce
  // second essai ne change rien pour lui.
  const secteurSurvole = glisse?.cible.secteur
  const depotRefuse =
    glisse !== null &&
    (glisser?.accepte
      ? !glisser.accepte(glisse.sourceId, glisse.cible)
      : !(
          (cibleSurvoleeId !== undefined && (ciblesDuGlisser?.has(cibleSurvoleeId) ?? false)) ||
          (cibleSurvoleeId === undefined &&
            ((zoneSurvolee !== undefined && (zonesDuGlisser?.has(zoneSurvolee) ?? false)) ||
              (secteurSurvole !== undefined && (zonesDuGlisser?.has(secteurSurvole) ?? false))))
        ))
  const tableAccueille = glisse !== null && (glisser?.accueilleLaTable?.(glisse.sourceId) ?? false)
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

  // Le nom donne par le joueur (Modifier la table, double-clic) remplace le titre automatique.
  const nomsZones = useNomsZones()
  const zonesRendues = useMemo(
    () =>
      (bandeManigances ? assemblerZones(plateau, disposition) : []).map((rendue) => {
        const nom = nomsZones[rendue.aire]
        return nom && rendue.emplacement ? { ...rendue, emplacement: { ...rendue.emplacement, titre: nom } } : rendue
      }),
    [bandeManigances, plateau, disposition, nomsZones]
  )
  const unEmplacement = (e: EmplacementAffiche, styleDeZone?: CSSProperties, aire?: string) => (
    <Emplacement
      emplacement={e}
      aire={aire}
      styleDeZone={styleDeZone}
      accueilleLeGlisser={[e.cle, ...(e.emplacementsDOrigine ?? [])].some((cle) => zonesDuGlisser?.has(cle))}
      pilesAccueillantes={zonesDuGlisser}
      ordres={reordre.ordres}
      interactifs={interactifsEffectifs}
      effets={effets}
      ouvrirPile={ouvrirPile}
      bloquerActionsPassives={bloquerActionsPassives}
      heroActifId={heroActifId}
      key={e.cle}
    />
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
        // Mode manuel (lot 2, question 12) : la table entiere accueille la
        // carte tenue, un seul cadre autour du plateau.
        data-table-accueille={tableAccueille ? '' : undefined}
        data-glisser-doigt={glisser?.auDoigt ? '' : undefined}
        onMouseOver={survol}
        onMouseLeave={quitter}
        onPointerDown={(evenement) => {
          if (reordre.gestes.surAppui(evenement)) return
          gestes.onPointerDown(evenement)
        }}
        onPointerMove={(evenement) => {
          if (reordre.gestes.surDeplacement(evenement)) return
          gestes.onPointerMove(evenement)
        }}
        // ⚠ LE CLIC PASSE APRES, ET SEULEMENT SI AUCUN GLISSER NE S'ACHEVE.
        // `gestes.onPointerUp` rend `true` quand il vient de lacher une carte :
        // sans cette garde, un lacher declencherait AUSSI le clic sous le
        // pointeur, donc deux actions pour un seul geste.
        onPointerUp={(evenement) => {
          if (reordre.gestes.surRelache(evenement)) return
          if (gestes.onPointerUp(evenement)) return
          cliquerCarte(evenement)
        }}
        onPointerCancel={() => {
          reordre.gestes.annuler()
          gestes.onPointerCancel()
        }}
      >
        <div
          className={`plateau-scene${bandeManigances ? ' avec-bande' : ''}`}
          style={
            {
              '--echelle': echelle,
              // ⚠ LE DIVISEUR DES DETAILS QUI DOIVENT RESTER FINS, jamais
              // au-dessus de 1. Douze formules CSS divisent par lui pour garder
              // une taille fixe a l'ecran quand la table RETRECIT ; au-dessus
              // de 1 la table GRANDIT, et ces details doivent grandir avec elle.
              // `min()` en CSS aurait fait la meme chose, mais la regle se lit
              // mieux ici, a cote de l'echelle dont elle derive.
              '--echelle-fixe': Math.min(1, echelle),
              width: `${largeur}px`,
              height: `${hauteur}px`,
              // La grille vient des DONNEES (disposition.ts) : a l'origine, la
              // meme que bande-manigances.css.
              ...(bandeManigances ? styleDeGrille(disposition) : {}),
            } as CSSProperties
          }
        >
          {bandeManigances
            ? zonesRendues.map((z) => {
                const taille = tailleDeZone(z.zone) as CSSProperties
                // La brique Heros emmene ses zones personnelles (deck special,
                // reserve, maree montante) a sa GAUCHE, comme avant.
                if (z.avecHeros) {
                  return (
                    <div className="colonne-terrain-soutien" key={`colonne-${z.aire}`} style={{ gridArea: z.aire }}>
                      {z.accompagnement.map((a) => unEmplacement(a))}
                      {z.emplacement ? unEmplacement(z.emplacement, taille) : null}
                    </div>
                  )
                }
                return z.emplacement ? unEmplacement(z.emplacement, taille, z.aire) : null
              })
            : plateau.emplacements.map((e) => {
                // Le deck special partage la case « terrain-soutien » : il occupe un
                // slot dedie a GAUCHE, le heros et les soutiens sont a sa droite.
                // La RESERVE de Brawn et la RISING TIDE AREA de Wave prennent
                // exactement la meme place : ce sont les zones personnelles du
                // personnage, comme l'Invocation de Strange. Aucun heros n'a deux
                // de ces trois zones a la fois, les autres slots sont donc
                // simplement absents.
                if (ACCOMPAGNEMENT.includes(e.cle)) return null
                if (e.cle === 'terrain-soutien') {
                  return (
                    <div className="colonne-terrain-soutien" key="colonne-terrain-soutien">
                      {plateau.emplacements.filter((x) => ACCOMPAGNEMENT.includes(x.cle)).map((a) => unEmplacement(a))}
                      {unEmplacement(e)}
                    </div>
                  )
                }
                return unEmplacement(e)
              })}
          {journal}
          {superposition}
        </div>
      </div>

      {carteApercu ? (
        <CarteApercu
          carte={carteApercu}
          statuts={statutsApercu}
          // `apercuId` vient de `data-card-id`, donc une CHAINE ; les cartes
          // sont indexees par leur identifiant d'objet NUMERIQUE partout
          // ailleurs (`interactifs`, `effets`). On convertit ici, une fois.
          raisons={apercuId === null ? undefined : raisonsRefus?.get(Number(apercuId))}
        />
      ) : null}

      {glisse ? (
        <CoucheGlisser
          glisse={glisse}
          carte={cartesParId.get(String(glisse.sourceId))}
          libelle={libelleGlisser}
          refuse={depotRefuse}
        />
      ) : null}
      {reordre.geste ? (
        <CoucheOrdre geste={reordre.geste} carte={cartesParId.get(String(reordre.geste.sourceId))} />
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
export function PileRegardee({
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
  const masque = groupes?.some((groupe) => groupe.masque !== undefined) === true
  const total = masque
    ? (groupes ?? []).reduce((somme, groupe) => somme + (groupe.masque?.nombre ?? 0), 0)
    : cartes.length
  const survol = useCallback((evenement: ReactMouseEvent) => {
    const carte = (evenement.target as HTMLElement).closest<HTMLElement>('.scan-card')
    setApercuId(carte?.dataset.cardId ?? null)
  }, [])
  const apercu = apercuId ? parId.get(apercuId) : undefined
  // Deplacement volontaire, a la poignee -- meme mecanisme que
  // `DemandeCentrale`/`AssistantAction` (demande de l'utilisateur, 28/09/2026,
  // « toutes les fenetres, tous les panneaux »). Pas de `usePlacement` ici
  // (centre par le voile en CSS), le decalage se pose donc en `transform`.
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(`${titre}|${cartes.length}`)

  return (
    <div className="plateau-regardees-voile" onClick={fermer}>
      <section
        className="plateau-regardees"
        role="dialog"
        aria-label={titre}
        style={transformDecalage(decalage)}
        onClick={(evenement) => evenement.stopPropagation()}
        onMouseOver={survol}
        onMouseLeave={() => setApercuId(null)}
      >
        <header className="plateau-regardees-entete">
          <div
            className="poignee-glisser"
            onPointerDown={gestesGlisser.onPointerDown}
            onPointerMove={gestesGlisser.onPointerMove}
            onPointerUp={gestesGlisser.onPointerUp}
            onPointerCancel={gestesGlisser.onPointerCancel}
          >
            <span className="plateau-eyebrow">{titre}</span>
            <strong>
              {total} {total > 1 ? t('cartes') : t('carte')}
            </strong>
          </div>
          <button type="button" onClick={fermer}>
            {t('Fermer')}
          </button>
        </header>

        <div className="plateau-regardees-corps">
          {masque ? (
            <>
              <p className="plateau-regardees-masque">{t('Masqué, mais il contient :')}</p>
              <ul className="plateau-regardees-masque-liste">
                {(groupes ?? []).map((groupe) => (
                  <li key={groupe.cle}>
                    {groupe.titre} · {groupe.masque?.nombre ?? 0}{' '}
                    {(groupe.masque?.nombre ?? 0) > 1 ? t('cartes') : t('carte')}
                  </li>
                ))}
              </ul>
            </>
          ) : groupes && groupes.length > 0 ? (
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
