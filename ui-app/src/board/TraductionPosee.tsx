import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import { GLYPHES, detecterZoneSurFondTeinte, detecterZoneTexte, detecterZoneTextePaysage, elargirPaysage, emDesTraits, encochesGauche, formeDuCache, ligneDeTraits, prolongerLaZone, texteEnParagraphes, zoneDansLeCadre, type ZoneTexte } from './traduction-posee'
import { chargerCatalogue } from './catalogue'
import { TRAITS_FR } from './traits-fr'
import { CADRES_PENCHES, VOILE_UNI, corrigerZone } from './zones-corrections'
import { BANDES_DROITE, effacerTexte, type CadreDuTexte, type OptionsEffacement } from './effacer-texte'
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

const SERIES_ALTERNATIVES = /_(cb|rog|rog2|m3t|mcdc26)$/

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
                return corrigerZone(code, zone ? prolongerLaZone(elargirPaysage(zone, paysage, { pixels, largeur, hauteur }), pixels, largeur, hauteur) : null)
              })()
            : corrigerZone(code, detecterZoneTexte(pixels, largeur, hauteur) ?? detecterZoneSurFondTeinte(pixels, largeur, hauteur))
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

/** Marge autour de la zone détectée : le fond nettoyé est identique au scan hors des lettres, une zone un peu large ne se
    voit pas, une zone trop juste laissait de l'anglais au bord. */
const MARGE = 0.012
/** Hauteur (fraction de la carte) de la bande des icônes de manigance imprimées en bas de la boîte de texte. */
const RESERVE_ICONES = 0.06

export function elargirZone(zone: ZoneTexte, marge = MARGE): ZoneTexte {
  const borne = (v: number) => Math.min(1, Math.max(0, v))
  return {
    ...zone,
    x0: borne(zone.x0 - marge),
    y0: borne(zone.y0 - marge),
    x1: borne(zone.x1 + marge),
    y1: borne(zone.y1 + marge),
    bords: zone.bords.map(([g, d]) => [borne(g - marge), borne(d + marge)]),
  }
}

export type FondNettoye = { image: string; texte: CadreDuTexte | null }

let travailleur: Worker | null | undefined
let numero = 0
const enAttente = new Map<number, (r: { donnees: Uint8ClampedArray; cadre: CadreDuTexte | null }) => void>()

/** effacerTexte dans un Worker (un seul, partagé) ; sur place si le navigateur n'en a pas. */
function effacerAilleurs(donnees: Uint8ClampedArray, largeur: number, hauteur: number, options: OptionsEffacement) {
  if (travailleur === undefined) {
    try {
      travailleur = new Worker(new URL('./effacer-texte.worker.ts', import.meta.url), { type: 'module' })
      travailleur.onmessage = (e: MessageEvent<{ id: number; donnees: Uint8ClampedArray; cadre: CadreDuTexte | null }>) => {
        enAttente.get(e.data.id)?.(e.data)
        enAttente.delete(e.data.id)
      }
    } catch {
      travailleur = null
    }
  }
  if (!travailleur) return Promise.resolve({ donnees, cadre: effacerTexte(donnees, largeur, hauteur, options) })
  const id = (numero += 1)
  const promesse = new Promise<{ donnees: Uint8ClampedArray; cadre: CadreDuTexte | null }>((resoudre) => enAttente.set(id, resoudre))
  travailleur.postMessage({ id, donnees, largeur, hauteur, options }, [donnees.buffer])
  return promesse
}
/**
 * Insère, entre les paragraphes, un bloc vide par icône imprimée au milieu du texte : à la frontière dont la part de
 * texte qui précède est la plus proche de celle de l'anglais au-dessus de l'icône.
 */
export function avecBandes(html: string, bandes: readonly { avant: number }[]): string {
  if (!bandes.length) return html
  const paragraphes = html.split(/(?=<div class="tp-)/)
  if (paragraphes.length < 2) return html
  const longueurs = paragraphes.map((p) => p.replace(/<[^>]*>/g, '').length || 1)
  const total = longueurs.reduce((a, b) => a + b, 0)
  const parts: number[] = []
  let cumul = 0
  for (let i = 0; i < paragraphes.length - 1; i += 1) {
    cumul += longueurs[i]
    parts.push(cumul / total)
  }
  const apres = new Map<number, number>()
  for (const b of bandes) {
    let meilleur = 0
    parts.forEach((p, i) => {
      if (Math.abs(p - b.avant) < Math.abs(parts[meilleur] - b.avant)) meilleur = i
    })
    apres.set(meilleur, (apres.get(meilleur) ?? 0) + 1)
  }
  return paragraphes.map((p, i) => p + '<div class="tp-bande"></div>'.repeat(apres.get(i) ?? 0)).join('')
}

const fondsNettoyes = new Map<string, Promise<FondNettoye | null>>()

/**
 * La zone du scan SANS ses lettres anglaises (effacer-texte.ts), en image (adresse de données) : c'est le fond du voile.
 * Coordonnées de la zone : celles de l'image (portrait) ou de la carte couchée (paysage), comme `zoneDuScan`.
 */
export function fondNettoye(url: string, zone: ZoneTexte, paysage?: CotePaysage, reserveBas = 0): Promise<FondNettoye | null> {
  const cle = `${url}|${paysage ?? ''}|${reserveBas}|${zone.x0},${zone.y0},${zone.x1},${zone.y1}`
  const connu = fondsNettoyes.get(cle)
  if (connu) return connu
  const promesse = new Promise<FondNettoye | null>((resoudre) => {
    const image = new Image()
    image.onload = () => {
      try {
        const imagePaysage = image.naturalWidth > image.naturalHeight
        const tourner = paysage !== undefined && !imagePaysage
        // Résolution d'origine, plafonnée : au-delà, le calcul coûte sans rien montrer de plus.
        const reduction = Math.min(1, 850 / Math.max(image.naturalWidth, image.naturalHeight))
        const [largeurImage, hauteurImage] = [Math.round(image.naturalWidth * reduction), Math.round(image.naturalHeight * reduction)]
        const [largeur, hauteur] = tourner ? [hauteurImage, largeurImage] : [largeurImage, hauteurImage]
        const toile = document.createElement('canvas')
        toile.width = largeur
        toile.height = hauteur
        const contexte = toile.getContext('2d', { willReadFrequently: true })
        if (!contexte) return resoudre(null)
        if (tourner) {
          contexte.translate(largeur, 0)
          contexte.rotate(Math.PI / 2)
          contexte.drawImage(image, 0, 0, hauteur, largeur)
        } else {
          contexte.drawImage(image, 0, 0, largeur, hauteur)
        }
        const x = Math.floor(zone.x0 * largeur)
        const y = Math.floor(zone.y0 * hauteur)
        const l = Math.max(1, Math.ceil(zone.x1 * largeur) - x)
        const h = Math.max(1, Math.ceil(zone.y1 * hauteur) - y)
        const region = contexte.getImageData(x, y, l, h)
        void effacerAilleurs(region.data, l, h, {
          largeurCarte: Math.min(largeur, hauteur),
          hauteurCarte: Math.max(largeur, hauteur),
          sombre: fondSombre(zone.fond),
          reserveBas,
          margeHaut: Math.round(MARGE * hauteur),
          margeBas: Math.round(MARGE * hauteur),
          margeCote: Math.round((MARGE + 0.012) * Math.min(largeur, hauteur)),
        })
          .then(({ donnees, cadre }) => {
            const sortie = document.createElement('canvas')
            sortie.width = l
            sortie.height = h
            sortie.getContext('2d')?.putImageData(new ImageData(new Uint8ClampedArray(donnees), l, h), 0, 0)
            resoudre({ image: sortie.toDataURL('image/webp', 0.92), texte: cadre })
          })
          .catch(() => resoudre(null))
      } catch {
        resoudre(null)
      }
    }
    image.onerror = () => resoudre(null)
    image.src = url
  })
  fondsNettoyes.set(cle, promesse)
  return promesse
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
  const [zoneImage, setZone] = useState<ZoneTexte | null>(null)
  // La même zone, ramenée au CADRE : le scan y est posé en `object-fit: cover`, donc rogné (voir `zoneDansLeCadre`).
  const [zoneCadre, setZoneCadre] = useState<ZoneTexte | null>(null)
  const zone = zoneImage && !paysage ? (zoneCadre ?? zoneImage) : zoneImage
  const boite = useRef<HTMLDivElement | null>(null)
  const contour = useRef<HTMLSpanElement | null>(null)
  const contourGauche = useRef<HTMLSpanElement | null>(null)
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
  const [fond, setFond] = useState<FondNettoye | null>(null)
  useEffect(() => {
    setFond(null)
    if (!zoneImage || VOILE_UNI.has(codeImage(url))) return
    let vivant = true
    // Icônes imprimées sous le texte : leur bande n'est pas effacée (elles restent celles du scan).
    void fondNettoye(url, zoneImage, paysage, icones.length > 0 ? RESERVE_ICONES + MARGE : 0).then((image) => {
      if (vivant) setFond(image)
    })
    return () => {
      vivant = false
    }
  }, [zoneImage, url, paysage, icones])

  useEffect(() => {
    let vivant = true
    setZone(null)
    onPose?.(false)
    void zoneDuScan(url, paysage).then((trouvee) => {
      if (!vivant) return
      setZone(trouvee ? elargirZone(trouvee) : null)
      onPose?.(trouvee !== null)
    })
    return () => {
      vivant = false
    }
    // onPose est un rappel de l'appelant : seule l'image compte.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url, paysage])

  useLayoutEffect(() => {
    setZoneCadre(null)
    const cadre = boite.current?.parentElement
    const image = cadre?.querySelector('img')
    if (!zoneImage || paysage || !cadre || !image) return
    const poser = () => {
      if (!image.naturalWidth || !cadre.clientWidth || !cadre.clientHeight) return
      setZoneCadre(
        zoneDansLeCadre(
          zoneImage,
          { largeur: image.naturalWidth, hauteur: image.naturalHeight },
          { largeur: cadre.clientWidth, hauteur: cadre.clientHeight }
        )
      )
    }
    poser()
    image.addEventListener('load', poser)
    return () => image.removeEventListener('load', poser)
  }, [zoneImage, paysage, url])

  // Le français est plus long que l'anglais : la police baisse jusqu'à ce que
  // le texte tienne, sans descendre sous un plancher lisible.
  //
  // ⚠ CALCUL À TAILLE DE RÉFÉRENCE (25/10/2026, signalé sur téléphone) : la boîte est mise en page pour une carte de
  // 300 px de large puis RÉDUITE par `transform: scale()`. Sur une petite carte (téléphone), la police voulue tombait
  // sous la taille minimale du navigateur (et le zoom de texte de l'appli) : le texte ne rétrécissait plus, ne tenait
  // pas, et la boîte montait sur l'illustration, hors du cadre de la carte. Une réduction par transformation, elle, n'est
  // bornée par rien.
  useLayoutEffect(() => {
    const element = boite.current
    if (!zone || !element) return
    const ajuster = () => {
      // La largeur d'une carte PORTRAIT de même taille : en paysage, la carte
      // est plus large que haute, mais ses lettres gardent la même taille.
      const parent = element.parentElement
      const largeurParent = parent?.clientWidth ?? LARGEUR
      const hauteurParent = parent?.clientHeight ?? HAUTEUR
      // Paysage : une carte portrait de même taille a pour LARGEUR la hauteur de la carte couchée (le texte imprimé a la
      // même taille absolue) ; la formule portrait la prenait 1,4 fois trop étroite et le français sortait 30 % trop petit.
      const carte = parent
        ? largeurParent > hauteurParent
          ? hauteurParent
          : Math.min(largeurParent, (hauteurParent * LARGEUR) / HAUTEUR)
        : LARGEUR
      const echelle = carte > 0 ? carte / LARGEUR : 1
      // Dimensions de la boîte À LA TAILLE DE RÉFÉRENCE (avant réduction).
      const largeurRef = ((zone.x1 - zone.x0) * largeurParent) / echelle
      const hauteurRef = ((zone.y1 - zone.y0) * hauteurParent) / echelle
      element.style.transformOrigin = '0 0'
      element.style.transform = `scale(${echelle})`
      element.style.width = `${largeurRef}px`
      // Départ à la taille du texte IMPRIMÉ (≈ 4,3 % de la largeur de la carte, mesuré sur les scans) : le français ne
      // doit pas paraître plus gros que l'anglais qu'il recouvre ; il ne fait ensuite que rétrécir pour tenir.
      // Départ : la taille de l'anglais imprimé, lue à son interligne quand on l'a mesuré (le corps fait ≈ 1/1,18 de
      // l'interligne, celui de la boîte), sinon 4,3 % de la largeur de la carte.
      const interligne = fond?.texte?.interligne ?? 0
      let taille = interligne > 0 ? Math.min(LARGEUR * 0.06, Math.max(LARGEUR * 0.03, (interligne * HAUTEUR) / 1.18)) : LARGEUR * 0.043
      // Le fond est le scan nettoyé de SA zone : la boîte ne peut plus déborder sur l'illustration. Un texte long
      // rétrécit donc davantage (le plancher reste lisible une fois la carte agrandie).
      const plancher = LARGEUR * 0.017
      element.style.fontSize = `${taille}px`
      element.style.top = `${zone.y0 * 100}%`
      element.style.height = `${hauteurRef}px`
      // Le français se pose là où était l'anglais : mêmes marges gauche, droite et haut que les lettres effacées ; il
      // peut descendre jusqu'au bas de la zone (il est souvent plus long).
      const cadreTexte = fond?.texte
      if (cadreTexte) {
        element.style.paddingLeft = `${cadreTexte.x0 * largeurRef}px`
        // À droite, la fin des lignes anglaises : le français ne s'étend pas plus loin (le cadre peut avoir un dessin pâle à
        // droite, sur lequel l'anglais ne mord qu'à peine). Une seule ligne anglaise courte (« Max 1 per deck. ») ne dit
        // rien de la colonne : marge symétrique de la gauche.
        element.style.paddingRight = `${(cadreTexte.lignes > 1 ? 1 - cadreTexte.x1 : Math.min(1 - cadreTexte.x1, cadreTexte.x0)) * largeurRef}px`
        element.style.paddingTop = `${Math.max(0, cadreTexte.y0 * hauteurRef - 1)}px`
        // En bas, le français s'arrête là où le fond du texte s'arrête (bandeau, icônes, liseré du cadre), et jamais
        // au-delà du bas de la zone détectée.
        const basDetecte = 1 - (MARGE + 0.006) * ((hauteurParent / echelle) / hauteurRef)
        element.style.paddingBottom = `${(1 - Math.min(cadreTexte.bas, basDetecte)) * hauteurRef + 1}px`
        // Une illustration qui entre dans le cadre par la droite (une main, un dessin pâle) : le français la contourne,
        // bande par bande, par un flottant dont la forme suit le bord du fond libre.
        // Icône imprimée entre deux paragraphes : un bloc vide de sa hauteur, posé entre les paragraphes français (voir
        // le rendu), le texte reprend dessous.
        const contourDroit = contour.current
        if (contourDroit) {
          const haut = Math.max(0, cadreTexte.y0 * hauteurRef - 1)
          const hauteurContenu = Math.max(0, element.clientHeight - haut - parseFloat(element.style.paddingBottom))
          const finDesLignes = (cadreTexte.lignes > 1 ? cadreTexte.x1 : Math.max(cadreTexte.x1, 1 - cadreTexte.x0)) * largeurRef
          const ecart = largeurRef * 0.012
          const encoches = cadreTexte.droite.map((x) => Math.max(0, finDesLignes - x * largeurRef + ecart))
          const largeurContour = Math.max(...encoches, 0)
          // (Pas de contour avec une bande d'icône : la forme du contour suit les lignes anglaises, plus en face des françaises.)
          if (largeurContour > ecart * 1.5 && hauteurContenu > 0 && !cadreTexte.entre.length) {
            const points = [`${largeurContour}px 0px`]
            encoches.forEach((w, b) => {
              const ya = (b * hauteurRef) / BANDES_DROITE - haut
              const yb = ((b + 1) * hauteurRef) / BANDES_DROITE - haut
              if (yb <= 0 || ya >= hauteurContenu) return
              points.push(`${largeurContour - w}px ${Math.max(0, ya)}px`, `${largeurContour - w}px ${Math.min(hauteurContenu, yb)}px`)
            })
            points.push(`${largeurContour}px ${hauteurContenu}px`)
            contourDroit.style.display = 'block'
            contourDroit.style.width = `${largeurContour}px`
            contourDroit.style.height = `${hauteurContenu}px`
            contourDroit.style.shapeOutside = `polygon(${points.join(', ')})`
          } else {
            contourDroit.style.display = 'none'
          }
        }
        // Un cadre qui penche à gauche (le bord noir s'écarte vers le bas) : les lignes anglaises du haut commencent plus à droite
        // que celles du bas, et le français commençait sur le bord noir (premières lettres perdues). Même procédé qu'à droite :
        // un flottant dont la forme suit le départ des lignes anglaises, bande par bande.
        const flottantGauche = contourGauche.current
        if (flottantGauche) {
          const encochesG = CADRES_PENCHES.has(codeImage(url)) ? encochesGauche(cadreTexte.gauche ?? [], cadreTexte.x0, largeurRef) : null
          const haut = Math.max(0, cadreTexte.y0 * hauteurRef - 1)
          const hauteurContenu = Math.max(0, element.clientHeight - haut - parseFloat(element.style.paddingBottom))
          if (encochesG && hauteurContenu > 0 && !cadreTexte.entre.length) {
            const largeurMax = Math.max(...encochesG)
            const points = ['0px 0px']
            encochesG.forEach((w, b) => {
              const ya = (b * hauteurRef) / BANDES_DROITE - haut
              const yb = ((b + 1) * hauteurRef) / BANDES_DROITE - haut
              if (yb <= 0 || ya >= hauteurContenu) return
              points.push(`${w}px ${Math.max(0, ya)}px`, `${w}px ${Math.min(hauteurContenu, yb)}px`)
            })
            points.push(`0px ${hauteurContenu}px`)
            flottantGauche.style.display = 'block'
            flottantGauche.style.width = `${largeurMax}px`
            flottantGauche.style.height = `${hauteurContenu}px`
            flottantGauche.style.shapeOutside = `polygon(${points.join(', ')})`
          } else {
            flottantGauche.style.display = 'none'
          }
        }
      } else {
        element.style.padding = ''
        if (contour.current) contour.current.style.display = 'none'
        if (contourGauche.current) contourGauche.current.style.display = 'none'
      }
      // Icônes imprimées au milieu du texte : chaque bloc vide est posé après le dernier paragraphe qui tient au-dessus
      // de l'icône, et s'allonge jusqu'à elle ; le texte reprend dessous. Si le français déborde sur l'icône, la police
      // baisse comme pour un débordement.
      const bandes = cadreTexte ? cadreTexte.entre : []
      const blocs = [...element.querySelectorAll<HTMLElement>('.tp-bande')]
      const placerLesBandes = (): boolean => {
        let chevauche = false
        blocs.forEach((bloc, i) => {
          const bande = bandes[i]
          if (!bande) return
          bloc.style.height = '0'
          const parent = bloc.parentElement
          if (!parent) return
          const haut = bande.y0 * hauteurRef
          const paragraphes = [...parent.querySelectorAll<HTMLElement>(':scope > .tp-par')]
          const tiennent = paragraphes.filter((p) => p.offsetTop + p.offsetHeight <= haut + 2)
          const apres = tiennent[tiennent.length - 1] ?? null
          if (apres && apres.nextSibling !== bloc) apres.after(bloc)
          if (!apres && parent.firstChild !== bloc) parent.prepend(bloc)
          const debut = bloc.offsetTop
          bloc.style.height = `${Math.max(0, haut - debut) + (bande.y1 - bande.y0) * hauteurRef}px`
          if (debut > haut + 2) chevauche = true
        })
        return chevauche
      }
      const deborde = () => placerLesBandes() || element.scrollHeight > element.clientHeight + 1
      while (deborde() && taille > plancher) {
        taille -= LARGEUR * 0.001
        element.style.fontSize = `${taille}px`
      }
      // La ligne des traits tient sur UNE ligne : elle déborde un peu dans les marges (symétriquement : elle reste centrée sur
      // la colonne) et rétrécit si elle est encore trop longue, au lieu de se couper au tiret (« SUPER- / POUVOIR. »).
      const traitsEl = element.querySelector<HTMLElement>('.tp-traits')
      const traitsTexte = traitsEl?.querySelector<HTMLElement>('.tp-traits-texte')
      if (traitsEl && traitsTexte) {
        // Une illustration qui entre par la droite (flottant) réduit la ligne : elle reste centrée dans ce qui reste, sans déborder.
        const flottantDroit = contour.current && contour.current.style.display === 'block' ? contour.current.offsetWidth : 0
        const marge = flottantDroit > 0 ? 0 : Math.min(parseFloat(element.style.paddingLeft) || 0, parseFloat(element.style.paddingRight) || 0) * 0.9
        traitsEl.style.marginLeft = `${-marge}px`
        traitsEl.style.marginRight = `${-marge}px`
        traitsEl.style.fontSize = ''
        const base = parseFloat(getComputedStyle(traitsEl).fontSize) / (taille || 1)
        traitsEl.style.fontSize = `${emDesTraits(traitsEl.clientWidth - flottantDroit, traitsTexte.offsetWidth, base)}em`
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
  }, [zone, texte, fond, icones])

  if (!zone) return null
  const forme = formeDuCache(zone)
  const ligneTraits = ligneDeTraits(traits, TRAITS_FR)
  return (
    <div
      ref={boite}
      className={`traduction-posee${icones.length > 0 && !fond ? ' tp-avec-icones' : ''}`}
      lang="fr"
      style={{
        left: `${zone.x0 * 100}%`,
        top: `${zone.y0 * 100}%`,
        width: `${(zone.x1 - zone.x0) * 100}%`,
        height: `${(zone.y1 - zone.y0) * 100}%`,
        // Le scan sans ses lettres anglaises ; la couleur unie le temps du calcul.
        background: fond ? `url(${fond.image}) 0 0 / 100% 100% no-repeat` : `rgb(${zone.fond.join(',')})`,
        // Fond sombre (certains arts alternatifs) : le texte passe en clair.
        color: fondSombre(zone.fond) ? '#f4f4f4' : undefined,
        // Fond = le scan nettoyé : hors des lettres, ses pixels sont ceux de l'image ; ni découpe ni encoche à dessiner.
        clipPath: fond ? undefined : forme.clipPath,
      }}
    >
      <span ref={contour} className="tp-contour-droit" />
      <span ref={contourGauche} className="tp-contour-gauche" />
      {forme.gauche && !fond ? (
        <span className="tp-encoche tp-encoche-gauche" style={{ height: `${forme.gauche.hauteur}%`, width: `${forme.gauche.largeur}%` }} />
      ) : null}
      {forme.droite && !fond ? (
        <span className="tp-encoche tp-encoche-droite" style={{ height: `${forme.droite.hauteur}%`, width: `${forme.droite.largeur}%` }} />
      ) : null}
      {ligneTraits ? (
        <div className="tp-traits">
          <span className="tp-traits-texte">{ligneTraits}</span>
        </div>
      ) : null}
      <div dangerouslySetInnerHTML={{ __html: avecBandes(texteEnParagraphes(texte), fond?.texte?.entre ?? []) }} />
      {icones.length > 0 && !fond ? (
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
