// Presentation au centre des cartes revelees.
//
// Quand une traitrise se revele ou qu'une carte boost est retournee, le moteur
// la fait passer par `area_revealing` / `area_boost`. Sur la table physique on
// la lit ; a l'ecran elle ne fait qu'apparaitre dans sa zone, facile a rater.
// Le client original l'affichait en grand au centre (Auto Pause / center_flip).
//
// Ici : on diffe les deux zones d'un rendu a l'autre, et chaque carte qui y
// ENTRE face visible est montree en grand, en pile horizontale sous la barre.
// Auto-dismiss apres `duree` ms, clic pour fermer tout de suite. Purement
// informatif : aucun blocage du jeu, et la couche ne capte que ses vignettes.

import { useEffect, useRef, useState } from 'react'
import { scanUrl } from './card-model'
import { t } from './langue'
import type { World, WorldCard } from './world'
import { estUneCarte } from './world'
import { nomAffiche } from './noms-cartes-fr'

type Revelation = {
  cle: string
  src: string
  nom: string
  etiquette: 'Révélée' | 'Boost'
  paysage: boolean
}

const TYPES_PAYSAGE = ['MainScheme', 'EncounterSideScheme', 'PlayerSideScheme']

/** Memoire module (memes raisons que CoucheAnimations : remontages). */
let dernierRender = -1
let idsVus = new Set<number>()

function idsDe(zone: unknown): Set<number> {
  const ids = new Set<number>()
  if (Array.isArray(zone)) {
    for (const carte of zone) if (estUneCarte(carte)) ids.add(carte.id)
  }
  return ids
}

export function CoucheRevelation({
  monde,
  duree,
  joueurId,
  seulementManigance = false,
}: {
  monde: World | undefined
  /** 0 = desactive. Sinon duree d'affichage en ms. */
  duree: number
  joueurId: number
  /**
   * Pendant la mise en place automatique, seule la manigance principale garde
   * sa presentation en grand : le reste (carte de rencontre initiale, etc.)
   * n'est le geste de personne. Constat de l'utilisateur, 24/09/2026 : « ça
   * fait beaucoup de bruit pour rien ». Les cartes ecartees ici restent
   * marquees VUES (`idsVus`) : elles ne resurgissent pas plus tard si la
   * mise en place se termine avant leur propre disparition de `area_revealing`.
   */
  seulementManigance?: boolean
}) {
  const [revelations, setRevelations] = useState<Revelation[]>([])
  const compteur = useRef(0)

  useEffect(() => {
    if (!monde || monde.render_id === dernierRender) return
    dernierRender = monde.render_id

    const zones: Array<[WorldCard[], 'Révélée' | 'Boost']> = [
      [monde.area_revealing ?? [], 'Révélée'],
      [monde.area_boost ?? [], 'Boost'],
    ]
    const courants = new Set<number>()
    const nouvelles: Revelation[] = []
    for (const [zone, etiquette] of zones) {
      for (const carte of zone) {
        if (!estUneCarte(carte)) continue
        courants.add(carte.id)
        if (idsVus.has(carte.id)) continue
        // Face cachee ou invisible pour nous : rien a montrer (et rien a
        // reveler d'un dos de carte).
        const visible = carte.is_face_up || carte.visible_for_players.includes(joueurId)
        if (!visible || !carte.pic_id) continue
        if (seulementManigance && carte.card_type !== 'MainScheme') continue
        nouvelles.push({
          cle: `r${compteur.current++}`,
          src: scanUrl(carte.pic_id),
          nom: nomAffiche(carte) || t('Carte'),
          etiquette,
          paysage: TYPES_PAYSAGE.includes(carte.card_type),
        })
      }
    }
    idsVus = courants

    if (duree <= 0 || nouvelles.length === 0) return
    setRevelations((r) => [...r, ...nouvelles])
    const cles = new Set(nouvelles.map((n) => n.cle))
    window.setTimeout(() => {
      setRevelations((r) => r.filter((x) => !cles.has(x.cle)))
    }, duree)
  }, [monde, monde?.render_id, duree, joueurId, seulementManigance])

  if (revelations.length === 0) return null
  return (
    <div className="couche-revelation" aria-live="polite">
      {revelations.map((rev) => (
        <figure
          key={rev.cle}
          className={`revelation${rev.paysage ? ' est-paysage' : ''}`}
          onClick={() => setRevelations((r) => r.filter((x) => x.cle !== rev.cle))}
        >
          {/* Le cadre porte le format ; l'image tourne DEDANS quand la carte est
              un complot : le serveur redresse tous ses scans en portrait (meme
              regle que `.scan-a-tourner`, ScanCard.css). Sans ce cadre, un
              complot revele s'affichait debout, texte a la verticale. */}
          <div className="revelation-cadre">
            <img src={rev.src} alt={rev.nom} />
          </div>
          <figcaption>{t(rev.etiquette)}</figcaption>
        </figure>
      ))}
    </div>
  )
}
