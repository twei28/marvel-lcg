import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import { GLYPHES, detecterZoneTexte, detecterZoneTextePaysage, elargirPaysage, formeDuCache, ligneDeTraits, texteEnHtml, type ZoneTexte } from './traduction-posee'
import { chargerCatalogue } from './catalogue'
import { TRAITS_FR } from './traits-fr'
import './traduction-posee.css'

const LARGEUR = 300
const HAUTEUR = 420
const zones = new Map<string, Promise<ZoneTexte | null>>()

/** Côté de la boîte de texte d'une carte paysage (manigance principale : gauche, annexe : droite). */
export type CotePaysage = 'gauche' | 'droite'

/**
 * La zone de texte d'un scan, lue une fois par image (cache par adresse).
 *
 * Paysage : le serveur sert les scans paysage REDRESSÉS en portrait, et le
 * plateau les tourne de 90° dans le sens horaire (ScanCard.css,
 * `.scan-a-tourner`). On fait la même rotation sur la toile, pour lire la
 * carte telle qu'elle est affichée. Une image déjà paysage est lue telle quelle.
 */
/** Code d'image d'une adresse de scan (« /scan/fr_01001a_cb » -> « 01001a_cb »). */
export function codeImage(url: string): string {
  const segment = url.split('?')[0]!.split('/').pop() ?? ''
  return segment.replace(/\.(jpe?g|png|webp)$/i, '').replace(/^fr_/, '')
}

const SERIES_ALTERNATIVES = /_(cb|rog|rog2|m3t)$/

export function zoneDuScan(url: string, paysage?: CotePaysage): Promise<ZoneTexte | null> {
  const cle = paysage ? `${url}|${paysage}` : url
  const connue = zones.get(cle)
  if (connue) return connue
  // Les arts alternatifs de héros ont leur propre mise en page : leur zone est
  // relevée une fois pour toutes, image par image (zones-arts-alternatifs.ts).
  const code = codeImage(url)
  if (!paysage && SERIES_ALTERNATIVES.test(code)) {
    const promesse = import('./zones-arts-alternatifs')
      .then((module) => module.ZONES_ARTS_ALTERNATIFS[code] ?? null)
      .catch(() => null)
    zones.set(cle, promesse)
    return promesse
  }
  const promesse = new Promise<ZoneTexte | null>((resoudre) => {
    const image = new Image()
    image.onload = () => {
      try {
        const imagePaysage = image.naturalWidth > image.naturalHeight
        if (!paysage && imagePaysage) return resoudre(null)
        const [largeur, hauteur] = paysage ? [HAUTEUR, LARGEUR] : [LARGEUR, HAUTEUR]
        const toile = document.createElement('canvas')
        toile.width = largeur
        toile.height = hauteur
        const contexte = toile.getContext('2d', { willReadFrequently: true })
        if (!contexte) return resoudre(null)
        if (paysage && !imagePaysage) {
          contexte.translate(largeur, 0)
          contexte.rotate(Math.PI / 2)
          contexte.drawImage(image, 0, 0, hauteur, largeur)
        } else {
          contexte.drawImage(image, 0, 0, largeur, hauteur)
        }
        const pixels = contexte.getImageData(0, 0, largeur, hauteur).data
        resoudre(
          paysage
            ? (() => {
                const zone = detecterZoneTextePaysage(pixels, largeur, hauteur, paysage)
                return zone ? elargirPaysage(zone, paysage, { pixels, largeur, hauteur }) : null
              })()
            : detecterZoneTexte(pixels, largeur, hauteur)
        )
      } catch {
        resoudre(null)
      }
    }
    image.onerror = () => resoudre(null)
    image.src = url
  })
  zones.set(cle, promesse)
  return promesse
}

function fondSombre([r, g, b]: [number, number, number]): boolean {
  return 0.299 * r + 0.587 * g + 0.114 * b < 128
}

/**
 * Le français posé sur la zone de texte du scan anglais. `onPose(true)` dès que
 * la pose a réussi : l'appelant retire alors l'encadré de traduction.
 */
export function TraductionPosee({
  url,
  texte,
  traits = [],
  paysage,
  onPose,
}: {
  url: string
  texte: string
  /** Carte affichée en paysage : côté attendu de sa boîte de texte. */
  paysage?: CotePaysage
  /** Traits imprimés : leur ligne est sous le cache, on la réécrit en tête. */
  traits?: readonly string[]
  onPose?: (pose: boolean) => void
}) {
  const [zone, setZone] = useState<ZoneTexte | null>(null)
  const boite = useRef<HTMLDivElement | null>(null)
  // Les icônes imprimées sous le cache (Accélération, Crise...) : on les redessine.
  const [icones, setIcones] = useState<readonly string[]>([])
  const code = codeImage(url)
  useEffect(() => {
    let vivant = true
    void chargerCatalogue().then((catalogue) => {
      if (vivant) setIcones(catalogue.iconesManigance?.(code) ?? [])
    })
    return () => {
      vivant = false
    }
  }, [code])

  useEffect(() => {
    let vivant = true
    setZone(null)
    onPose?.(false)
    void zoneDuScan(url, paysage).then((trouvee) => {
      if (!vivant) return
      setZone(trouvee)
      onPose?.(trouvee !== null)
    })
    return () => {
      vivant = false
    }
    // onPose est un rappel de l'appelant : seule l'image compte.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url, paysage])

  // Le français est plus long que l'anglais : la police baisse jusqu'à ce que
  // le texte tienne, sans descendre sous un plancher lisible.
  useLayoutEffect(() => {
    const element = boite.current
    if (!zone || !element) return
    const ajuster = () => {
      // La largeur d'une carte PORTRAIT de même taille : en paysage, la carte
      // est plus large que haute, mais ses lettres gardent la même taille.
      const parent = element.parentElement
      const carte = parent ? Math.min(parent.clientWidth, (parent.clientHeight * LARGEUR) / HAUTEUR) : 300
      let taille = carte * 0.05
      const plancher = carte * 0.026
      element.style.fontSize = `${taille}px`
      element.style.top = `${zone.y0 * 100}%`
      element.style.height = `${(zone.y1 - zone.y0) * 100}%`
      while (element.scrollHeight > element.clientHeight + 1 && taille > plancher) {
        taille -= carte * 0.0015
        element.style.fontSize = `${taille}px`
      }
      // Toujours trop long au plancher (petits encadrés de certains arts) : le
      // cache monte sur l'illustration plutôt que de couper le texte.
      const hauteurCarte = parent?.clientHeight ?? 0
      if (hauteurCarte && element.scrollHeight > element.clientHeight + 1) {
        const voulue = Math.min(element.scrollHeight, zone.y1 * hauteurCarte)
        element.style.top = `${zone.y1 * hauteurCarte - voulue}px`
        element.style.height = `${voulue}px`
      }
    }
    ajuster()
    let vivant = true
    void document.fonts?.ready.then(() => {
      if (vivant) ajuster()
    })
    return () => {
      vivant = false
    }
  }, [zone, texte])

  if (!zone) return null
  const forme = formeDuCache(zone)
  const ligneTraits = ligneDeTraits(traits, TRAITS_FR)
  return (
    <div
      ref={boite}
      className={`traduction-posee${icones.length > 0 ? ' tp-avec-icones' : ''}`}
      lang="fr"
      style={{
        left: `${zone.x0 * 100}%`,
        top: `${zone.y0 * 100}%`,
        width: `${(zone.x1 - zone.x0) * 100}%`,
        height: `${(zone.y1 - zone.y0) * 100}%`,
        background: `rgb(${zone.fond.join(',')})`,
        // Fond sombre (certains arts alternatifs) : le texte passe en clair.
        color: fondSombre(zone.fond) ? '#f4f4f4' : undefined,
        clipPath: forme.clipPath,
      }}
    >
      {forme.gauche ? (
        <span className="tp-encoche tp-encoche-gauche" style={{ height: `${forme.gauche.hauteur}%`, width: `${forme.gauche.largeur}%` }} />
      ) : null}
      {forme.droite ? (
        <span className="tp-encoche tp-encoche-droite" style={{ height: `${forme.droite.hauteur}%`, width: `${forme.droite.largeur}%` }} />
      ) : null}
      {ligneTraits ? <div className="tp-traits">{ligneTraits}</div> : null}
      <div dangerouslySetInnerHTML={{ __html: texteEnHtml(texte) }} />
      {icones.length > 0 ? (
        <div className="tp-icones-manigance">
          {icones.map((jeton) => (
            <span key={jeton} className={`tp-icone tp-icone-${jeton}`}>
              {GLYPHES[jeton]}
            </span>
          ))}
        </div>
      ) : null}
    </div>
  )
}
