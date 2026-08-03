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

const DUREE = 250
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

type Boite = { x: number; y: number; w: number; h: number }
type Mesure = { rect: Boite; zone: string; src: string; el: HTMLElement }
type Vol = {
  cle: string
  src: string
  depart: Boite
  arrivee: Boite
  delai: number
}

function boiteDe(el: Element): Boite {
  const r = el.getBoundingClientRect()
  return { x: r.left, y: r.top, w: r.width, h: r.height }
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

/** Une carte fantome qui glisse de `depart` a `arrivee`, taille comprise. */
function VolCarte({ vol }: { vol: Vol }) {
  const [pose, setPose] = useState(false)
  useEffect(() => {
    const t = window.setTimeout(() => setPose(true), 20)
    return () => window.clearTimeout(t)
  }, [])

  const b = pose ? vol.arrivee : vol.depart
  // On dimensionne le fantome a la taille d'ARRIVEE et on met le depart a
  // l'echelle : le mouvement direct opaque « physique » demande, sans fondu.
  const echelle = vol.arrivee.w > 0 ? b.w / vol.arrivee.w : 1
  const style = {
    width: `${vol.arrivee.w}px`,
    height: `${vol.arrivee.h}px`,
    transform: `translate(${b.x}px, ${b.y}px) scale(${echelle})`,
    transitionDelay: `${vol.delai}ms`,
  }

  // Carte sans scan : c'est sa BOITE qui vole, pas une image. Un <img src="">
  // ferait recharger la page (meme raison que la garde de ScanCard), et une
  // image cassee ne montrait de toute facon rien de plus qu'un rectangle.
  if (!vol.src) return <div className="vol-carte" style={style} />

  return <img className="vol-carte" src={vol.src} alt="" style={style} />
}

export function CoucheAnimations({ renderId, actif }: { renderId: number; actif: boolean }) {
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
    const ancre = (zone: string, index: number): Boite | undefined => {
      const els = scene.querySelectorAll<HTMLElement>(`.${zone} .scan-card[data-card-id]`)
      const el = els[index]
      return el ? boiteDe(el) : undefined
    }
    const deckJoueur = ancre('zone-piles-joueur', 0)
    const defausseJoueur = ancre('zone-piles-joueur', 1) ?? deckJoueur
    const deckRencontre = ancre('zone-piles-rencontre', 0)
    const defausseRencontre = ancre('zone-piles-rencontre', 1) ?? deckRencontre

    // Respect du reglage systeme : si l'OS demande de reduire les animations, on
    // ne masque meme pas les vraies cartes (sinon elles clignoteraient sans
    // fantome). On met quand meme `precedent` a jour pour repartir proprement.
    const reduit = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    const prev = memoire
    if (actif && !reduit && prev.size > 0) {
      type Brouillon = { groupe: number; src: string; depart: Boite; arrivee: Boite; el?: HTMLElement }
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
          brouillons.push({ groupe: GROUPE_DEFAUSSE, src: avant.src, depart: avant.rect, arrivee: defausseJoueur })
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
        const masquer = (el: HTMLElement, delai: number) => {
          el.style.visibility = 'hidden'
          window.setTimeout(() => {
            el.style.visibility = ''
          }, 20 + delai + DUREE + 30)
        }

        const nouveaux: Vol[] = []
        let base = 0
        for (const groupe of [...parGroupe.keys()].sort((a, b) => a - b)) {
          const liste = parGroupe.get(groupe)!
          liste.forEach((b, i) => {
            const delai = base + i * CASCADE
            nouveaux.push({ cle: `v${compteur.current++}`, src: b.src, depart: b.depart, arrivee: b.arrivee, delai })
            if (b.el) masquer(b.el, delai)
          })
          base += (liste.length - 1) * CASCADE + DUREE + GAP
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
  }, [renderId, actif])

  if (vols.length === 0) return null
  return (
    <div className="couche-animations" aria-hidden="true">
      {vols.map((vol) => (
        <VolCarte key={vol.cle} vol={vol} />
      ))}
    </div>
  )
}
