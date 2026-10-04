// Animations de DEPLACEMENT des cartes.
//
// Principe : le plateau se redessine a chaque rendu du moteur (render_id). Entre
// deux rendus, une carte peut changer de zone (deck -> main, main -> table,
// -> defausse, deck rencontre -> vilain...). On DIFFE les positions ecran des
// cartes d'un rendu a l'autre, et pour chaque mouvement on fait voler une
// « carte fantome » (une image) du point de depart au point d'arrivee, PENDANT
// que la vraie carte est masquee. La vraie carte reapparait a l'atterrissage.
//
// Decouple du reste : on lit le DOM (`.scan-card[data-card-id]`, `.zone-*`), on
// ne touche pas au rendu de Board. Si quoi que ce soit manque, on n'anime pas —
// la carte apparait directement, aucun blocage.

import { useEffect, useLayoutEffect, useRef, useState } from 'react'
// Meme mesure que le placement des panneaux : une seule definition de boite
// d'ecran pour tout le plateau (voir placement/boites.ts).
import { boiteDe, type Boite } from './placement/boites'
import { mouvementReduit } from './affichage'

/**
 * LA DUREE SUIT LA DISTANCE, et c'est le coeur du poids.
 *
 * ⚠ C'ETAIT UNE CONSTANTE : 250 ms, qu'une carte traverse l'ecran ou bouge de
 * trois centimetres. Rien ne pesait, rien ne prenait son elan. Constat de
 * l'utilisateur le 14/09/2026 : « au niveau animation on est tres mauvais,
 * je trouve ca tres mou ». C'est la premiere des six causes relevees
 * (.planning/todos/2026-09-14-animations-molles.md).
 *
 * ⚠ RACINE CARREE, PAS PROPORTIONNEL. Une duree proportionnelle rendrait les
 * petits deplacements quasi instantanes (invisibles) et les grands
 * interminables. La racine resserre les ecarts : un trajet 9 fois plus long
 * dure 3 fois plus longtemps, ce qui est la sensation juste.
 */
const DUREE_MIN = 130
const DUREE_MAX = 400
/** Au-dela de cette distance, on ne ralentit plus : c'est deja la traversee. */
const DISTANCE_PLEINE = 900

export function dureeDe(depart: Boite, arrivee: Boite): number {
  const d = Math.hypot(arrivee.x - depart.x, arrivee.y - depart.y)
  const part = Math.sqrt(Math.min(1, d / DISTANCE_PLEINE))
  return Math.round(DUREE_MIN + (DUREE_MAX - DUREE_MIN) * part)
}

/**
 * L'inclinaison pendant le vol, dans le sens du deplacement.
 *
 * ⚠ BORNEE A 3 DEGRES, et c'est voulu : au-dela on ne lit plus une carte
 * lancee mais une carte qui tourne, ce que l'utilisateur a explicitement
 * exclu (« sans que ce soit trop charge »).
 */
const ANGLE_MAX = 3

export function inclinaisonDe(depart: Boite, arrivee: Boite): number {
  const dx = arrivee.x - depart.x
  return Math.max(-ANGLE_MAX, Math.min(ANGLE_MAX, dx / 120))
}

const CASCADE = 60
/** Pause entre deux GROUPES (types de deck) enchaines l'un apres l'autre. */
const GAP = 70
/**
 * Au-dela de ce nombre de cartes en mouvement d'un coup, ce n'est pas un vrai
 * coup (pioche = quelques cartes) mais une resynchronisation massive : chargement,
 * undo, remelange, changement de forme qui re-trie tout le plateau... On n'anime
 * PAS (sinon « 40 cartes » volent en meme temps), on met juste l'etat a jour.
 */
const MAX_VOLS = 10

/** Ordre d'enchainement des groupes (par type de source). */
const GROUPE_RENCONTRE = 0
const GROUPE_PIOCHE = 1
const GROUPE_JEU = 2
const GROUPE_DEFAUSSE = 3

type Mesure = { rect: Boite; zone: string; src: string; el: HTMLElement }
type Vol = {
  cle: string
  src: string
  depart: Boite
  arrivee: Boite
  delai: number
  /** Calculee sur la DISTANCE de ce vol-la : voir `dureeDe`. */
  duree: number
  /** Inclinaison pendant le trajet, en degres : voir `inclinaisonDe`. */
  angle: number
  /**
   * Le « clac » a l'arrivee.
   *
   * ⚠ SEULEMENT QUAND LA CARTE EST SEULE. Le depassement avait ete retire du
   * plateau parce qu'il rendait « fouillis » l'arrivee groupee de plusieurs
   * cartes (commentaire de `.vol-carte` dans board.css). Le probleme n'etait
   * donc pas le rebond, mais le rebond A PLUSIEURS : on le rend au coup
   * unique, la ou il se lit, et on le refuse au reste.
   */
  clac: boolean
}


function zoneDe(el: Element): string {
  const z = el.closest('[class*="zone-"]')
  if (!z) return ''
  return [...z.classList].find((c) => c.startsWith('zone-')) ?? ''
}

/**
 * L'URL du scan de la carte, ou '' quand elle n'en a pas : ScanCard ne pose
 * plus d'<img> du tout dans ce cas (un src vide fait recharger la PAGE).
 *
 * '' veut donc dire « pas d'image a faire voler », PAS « pas une carte » : le
 * mouvement s'anime quand meme, c'est le fantome qui s'adapte (voir VolCarte).
 */
function imageDe(el: Element): string {
  const img = el.querySelector('img')
  return img instanceof HTMLImageElement ? img.src : ''
}

/**
 * Memoire des positions du rendu PRECEDENT, au niveau MODULE (pas dans un ref de
 * composant). Raison : le composant peut etre demonte/remonte (retour momentane
 * a « Connecting », re-rendu de la page...), ce qui reinitialiserait un ref et
 * ferait apparaitre TOUTES les cartes deja en place comme « nouvelles ». Il n'y a
 * qu'UN plateau par page, donc une memoire de module est sure et survit aux
 * remontages. Repartie a zero au vrai rechargement de page (module re-execute).
 */
let memoire = new Map<string, Mesure>()
/** Dernier render_id DEJA traite : l'effet est parfois invoque 2x pour le meme
 *  rendu (remontage/StrictMode) ; on ne diffe qu'une fois par rendu. */
let dernierRender = -1

/**
 * Une carte fantome qui glisse de `depart` a `arrivee`, taille comprise.
 *
 * ⚠ DEUX COUCHES, ET C'EST LA CLE DU MONTAGE. La couche du dessus porte la
 * TRANSLATION, celle du dessous le GESTE (inclinaison, leger agrandissement,
 * ombre). Tout mettre dans un seul `transform` casserait le vol : changer
 * l'inclinaison a mi-chemin relancerait la transition de `transform`, donc le
 * deplacement lui-meme, et la carte repartirait de la ou elle en etait.
 * Separees, les deux s'animent sur leurs propres durees sans se gener.
 */
function VolCarte({ vol }: { vol: Vol }) {
  const [pose, setPose] = useState(false)
  const [atterri, setAtterri] = useState(false)
  useEffect(() => {
    const decolle = window.setTimeout(() => setPose(true), 20)
    // Le geste se resorbe AVANT la fin du trajet : la carte se remet a plat en
    // approchant, elle ne se pose pas de travers.
    const pose_ = window.setTimeout(
      () => setAtterri(true),
      20 + vol.delai + Math.round(vol.duree * 0.62)
    )
    return () => {
      window.clearTimeout(decolle)
      window.clearTimeout(pose_)
    }
  }, [vol.delai, vol.duree])

  const b = pose ? vol.arrivee : vol.depart
  // On dimensionne le fantome a la taille d'ARRIVEE et on met le depart a
  // l'echelle : le mouvement direct opaque « physique » demande, sans fondu.
  const echelle = vol.arrivee.w > 0 ? b.w / vol.arrivee.w : 1
  const style = {
    width: `${vol.arrivee.w}px`,
    height: `${vol.arrivee.h}px`,
    transform: `translate(${b.x}px, ${b.y}px) scale(${echelle})`,
    transitionDelay: `${vol.delai}ms`,
    transitionDuration: `${vol.duree}ms`,
    // Le « clac » vit dans la COURBE, pas dans une animation de plus.
    transitionTimingFunction: vol.clac
      ? 'cubic-bezier(0.2, 0.9, 0.24, 1.06)'
      : 'cubic-bezier(0.22, 0.75, 0.3, 1)',
  } as const

  const geste = {
    // `--angle` sert la CSS, qui compose l'inclinaison et l'agrandissement.
    '--angle': `${vol.angle}deg`,
  } as Record<string, string>

  // Carte sans scan : c'est sa BOITE qui vole, pas une image. Un <img src="">
  // ferait recharger la page (meme raison que la garde de ScanCard), et une
  // image cassee ne montrait de toute facon rien de plus qu'un rectangle.
  return (
    <div className="vol-carte" style={style}>
      <div className={`vol-carte-geste${atterri ? ' est-pose' : ''}`} style={geste}>
        {vol.src ? <img className="vol-carte-image" src={vol.src} alt="" /> : null}
      </div>
    </div>
  )
}

/** L'ancienne duree, gardee pour tout le monde sauf les essais. */
const DUREE_AVANT_ESSAIS = 250

export function CoucheAnimations({
  renderId,
  actif,
  essais = false,
}: {
  renderId: number
  actif: boolean
  /**
   * Le poids, le geste et le « clac » (14/09/2026).
   *
   * ⚠ RESERVES A UN SEUL COMPTE tant qu'ils ne sont pas valides a l'usage
   * (voir `board/essais.ts`). Faux = comportement d'avant, a l'identique :
   * 250 ms fixes, aucune inclinaison, aucun depassement, aucun tressaillement.
   * C'est du code TEMPORAIRE : le jour ou l'utilisateur valide, ce drapeau et
   * les deux branches disparaissent.
   */
  essais?: boolean
}) {
  const [vols, setVols] = useState<Vol[]>([])
  const compteur = useRef(0)

  useLayoutEffect(() => {
    if (renderId === dernierRender) return
    dernierRender = renderId

    const scene = document.querySelector('.plateau-scene')
    if (!scene) {
      memoire = new Map()
      return
    }

    const courant = new Map<string, Mesure>()
    for (const el of scene.querySelectorAll<HTMLElement>('.scan-card[data-card-id]')) {
      const id = el.dataset.cardId
      if (!id) continue
      courant.set(id, { rect: boiteDe(el), zone: zoneDe(el), src: imageDe(el), el })
    }

    // Ancres de pile : dans piles-joueur = [deck, defausse] ; idem rencontre.
    // On garde l'ELEMENT et pas seulement sa boite : la pile qui recoit une
    // carte tressaille a l'atterrissage, et pour cela il faut pouvoir la
    // toucher.
    const ancreEl = (zone: string, index: number): HTMLElement | undefined =>
      scene.querySelectorAll<HTMLElement>(`.${zone} .scan-card[data-card-id]`)[index]
    const boiteOuRien = (el: HTMLElement | undefined): Boite | undefined =>
      el ? boiteDe(el) : undefined

    /**
     * LA PLACE DE LA DEFAUSSE, MEME QUAND ELLE EST VIDE.
     *
     * ⚠ UNE PILE VIDE N'EXISTE PAS DANS LE DOM. `zones.ts` fait `if (!carte)
     * return []` : sans carte, aucune unite n'est produite, donc aucun element
     * a viser. Le repli envoyait alors la carte defaussee voler vers le DECK,
     * c'est-a-dire vers la pioche — exactement le contraire de ce qui se passe.
     * Signale par l'utilisateur le 14/09/2026 : « le vrai point de depart et le
     * vrai point d'arrivee ».
     *
     * On DEDUIT donc sa place : elle se pose a la droite du deck, meme taille,
     * meme hauteur, a une gouttiere d'ecart. C'est ou elle apparaitra des
     * qu'elle aura sa premiere carte.
     */
    const placeDeLaDefausse = (zone: string, deck: Boite | undefined): Boite | undefined => {
      if (!deck) return undefined
      const conteneur = scene.querySelector<HTMLElement>(`.${zone}`)
      const gouttiere = conteneur
        ? Number.parseFloat(getComputedStyle(conteneur).columnGap || '0') || 8
        : 8
      return { ...deck, x: deck.x + deck.w + gouttiere }
    }

    const deckJoueurEl = ancreEl('zone-piles-joueur', 0)
    const defausseJoueurEl = ancreEl('zone-piles-joueur', 1)
    const deckRencontreEl = ancreEl('zone-piles-rencontre', 0)
    const defausseRencontreEl = ancreEl('zone-piles-rencontre', 1)

    const deckJoueur = boiteOuRien(deckJoueurEl)
    const deckRencontre = boiteOuRien(deckRencontreEl)
    const defausseJoueur =
      boiteOuRien(defausseJoueurEl) ?? placeDeLaDefausse('zone-piles-joueur', deckJoueur)
    const defausseRencontre =
      boiteOuRien(defausseRencontreEl) ?? placeDeLaDefausse('zone-piles-rencontre', deckRencontre)

    // Respect du reglage systeme : si l'OS demande de reduire les animations, on
    // ne masque meme pas les vraies cartes (sinon elles clignoteraient sans
    // fantome). On met quand meme `precedent` a jour pour repartir proprement.
    const reduit = mouvementReduit()

    const prev = memoire
    if (actif && !reduit && prev.size > 0) {
      type Brouillon = {
        groupe: number
        src: string
        depart: Boite
        arrivee: Boite
        /** La vraie carte a masquer pendant que son fantome vole. */
        el?: HTMLElement
        /** La PILE qui recoit, quand il y en a une : elle tressaille. */
        elArrivee?: HTMLElement
      }
      const brouillons: Brouillon[] = []

      // On n'anime QUE les mouvements qui touchent la MAIN du joueur (pioche,
      // mise en jeu, defausse depuis la main). Raison : le client ne recoit que
      // des instantanes ESPACES du moteur (le render_id saute de ~100 a chaque
      // mise a jour), donc entre deux instantanes tout le plateau peut avoir
      // bouge. Animer tout ferait « apparaitre » les cartes deja en place. En se
      // limitant a la main, les cartes du plateau (vilain, complots, allies deja
      // poses) ne volent JAMAIS, meme quand la memoire repart de zero.
      for (const [id, m] of courant) {
        const avant = prev.get(id)
        if (!avant) {
          // Carte APPARUE dans la main = pioche. On ne conditionne PAS a la
          // presence d'une image : une carte sans scan se deplace comme les
          // autres, elle vole juste sans visuel.
          if (m.zone === 'zone-main' && deckJoueur) {
            brouillons.push({ groupe: GROUPE_PIOCHE, src: m.src, depart: deckJoueur, arrivee: m.rect, el: m.el })
          }
        } else if (avant.zone === 'zone-main' && m.zone !== 'zone-main') {
          // Carte qui QUITTE la main vers la table = mise en jeu.
          brouillons.push({ groupe: GROUPE_JEU, src: m.src || avant.src, depart: avant.rect, arrivee: m.rect, el: m.el })
        }
      }

      // Carte qui QUITTE la main et disparait (event joue, defausse fin de tour).
      for (const [id, avant] of prev) {
        if (courant.has(id)) continue
        if (avant.zone === 'zone-main' && defausseJoueur) {
          brouillons.push({
            groupe: GROUPE_DEFAUSSE,
            src: avant.src,
            depart: avant.rect,
            arrivee: defausseJoueur,
            elArrivee: defausseJoueurEl,
          })
        }
      }

      if (brouillons.length > MAX_VOLS) {
        // Resynchronisation massive : on saute l'animation pour ce rendu.
        console.warn(`[anim] ${brouillons.length} mouvements d'un coup -> saute (resync)`)
      } else if (brouillons.length > 0) {
        // Enchainer par GROUPE (type de deck) : chaque groupe demarre apres
        // l'atterrissage du precedent, plutot que tout en meme temps.
        const parGroupe = new Map<number, Brouillon[]>()
        for (const b of brouillons) {
          const liste = parGroupe.get(b.groupe) ?? []
          liste.push(b)
          parGroupe.set(b.groupe, liste)
        }
        const masquer = (el: HTMLElement, delai: number, duree: number) => {
          el.style.visibility = 'hidden'
          window.setTimeout(() => {
            el.style.visibility = ''
          }, 20 + delai + duree + 30)
        }

        /**
         * La pile qui RECOIT tressaille de deux pixels a l'atterrissage.
         *
         * ⚠ Elle dit « c'est arrive LA ». Sans elle, une carte defaussee
         * disparaissait au bord de l'ecran sans que rien ne signale ou : la
         * defausse est l'endroit du plateau qu'on ne regarde jamais.
         */
        const tressaillir = (el: HTMLElement | undefined, quand: number) => {
          if (!el) return
          window.setTimeout(() => {
            el.classList.add('a-recu')
            window.setTimeout(() => el.classList.remove('a-recu'), 260)
          }, quand)
        }

        const nouveaux: Vol[] = []
        let base = 0
        let dureeMax = 0
        for (const groupe of [...parGroupe.keys()].sort((a, b) => a - b)) {
          const liste = parGroupe.get(groupe)!
          // ⚠ Le « clac » ne part QUE si ce rendu ne fait voler qu'une seule
          // carte, tous groupes confondus. Voir `Vol.clac`.
          const seule = brouillons.length === 1
          dureeMax = 0
          liste.forEach((b, i) => {
            const delai = base + i * CASCADE
            const duree = essais ? dureeDe(b.depart, b.arrivee) : DUREE_AVANT_ESSAIS
            dureeMax = Math.max(dureeMax, duree)
            nouveaux.push({
              cle: `v${compteur.current++}`,
              src: b.src,
              depart: b.depart,
              arrivee: b.arrivee,
              delai,
              duree,
              angle: essais ? inclinaisonDe(b.depart, b.arrivee) : 0,
              clac: essais && seule,
            })
            if (b.el) masquer(b.el, delai, duree)
            if (essais) tressaillir(b.elArrivee, 20 + delai + duree)
          })
          base += (liste.length - 1) * CASCADE + dureeMax + GAP
        }

        setVols((v) => [...v, ...nouveaux])
        const finMax = base + 200
        window.setTimeout(() => {
          const cles = new Set(nouveaux.map((n) => n.cle))
          setVols((v) => v.filter((x) => !cles.has(x.cle)))
        }, finMax)
      }
    }

    memoire = courant
  }, [renderId, actif, essais])

  if (vols.length === 0) return null
  return (
    <div className={`couche-animations${essais ? ' est-essai' : ''}`} aria-hidden="true">
      {vols.map((vol) => (
        <VolCarte key={vol.cle} vol={vol} />
      ))}
    </div>
  )
}
