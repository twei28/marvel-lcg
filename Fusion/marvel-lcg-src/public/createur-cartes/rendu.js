// Le rendu d'une carte : une pile de calques (teintes par role) + l'illustration + les textes.
//
// Tout se dessine en pixels de carte : 1500 x 2150 en portrait, 2150 x 1500 pour les cartes qui se posent en paysage
// (manigances, plus la manigance annexe de joueur). Les calques du gabarit sont TOUS fournis en portrait ; une carte paysage
// les fait pivoter d'un quart de tour (sens horaire), l'illustration, elle, se place dans le repere paysage.
//
// Un calque teinte est une forme pleine : seul son ALPHA compte, il est rempli d'une couleur unie (role = nom du calque :
// `left_color`, `middle`...). Le calque `gradient` est un degrade bas -> haut decoupe par son masque.

import { dessinerNiveau } from './libres.js'

const cacheImages = new Map()

export function chargerImage(url) {
  if (!cacheImages.has(url)) {
    cacheImages.set(
      url,
      new Promise((ok, ko) => {
        const im = new Image()
        im.onload = () => ok(im)
        im.onerror = () => ko(new Error('image introuvable : ' + url))
        im.src = url
      })
    )
  }
  return cacheImages.get(url)
}

const cacheTeintes = new Map()

/** La forme du calque remplie d'une couleur unie (alpha conserve). */
function teinter(image, couleur) {
  const cle = image.src + '|' + couleur
  let c = cacheTeintes.get(cle)
  if (c) return c
  c = document.createElement('canvas')
  c.width = image.naturalWidth
  c.height = image.naturalHeight
  const x = c.getContext('2d')
  x.drawImage(image, 0, 0)
  x.globalCompositeOperation = 'source-in'
  x.fillStyle = couleur
  x.fillRect(0, 0, c.width, c.height)
  if (cacheTeintes.size > 120) cacheTeintes.clear()
  cacheTeintes.set(cle, c)
  return c
}

/** Le degrade CSS « to right top » d'une boite L x H : la ligne du degrade est perpendiculaire a la diagonale. */
function degradeVersHautDroite(ctx, L, H, bas, haut) {
  const n = Math.hypot(L, H)
  const dx = H / n
  const dy = -L / n
  const demi = (Math.abs(L * dx) + Math.abs(H * dy)) / 2
  const g = ctx.createLinearGradient(L / 2 - dx * demi, H / 2 - dy * demi, L / 2 + dx * demi, H / 2 + dy * demi)
  g.addColorStop(0, bas)
  g.addColorStop(1, haut)
  return g
}

/** Les dimensions du gabarit (toujours portrait) d'une carte, avant rotation. */
export const PORTRAIT = { l: 1500, h: 2150 }

/** Pose le repere d'une carte paysage : un point du gabarit portrait (x, y) arrive en (largeur - y, x). */
function repereGabarit(ctx, spec) {
  if (spec.paysage) ctx.transform(0, 1, -1, 0, spec.largeur, 0)
}

/**
 * Dessine l'illustration (ou le premier plan) : `art` = { image, x, y, zoom, rotation }. Sans reglage, elle remplit la carte
 * (comme `object-fit: cover`) ; `zoom` agrandit, x / y decalent, `rotation` en degres autour du centre.
 */
export function dessinerArt(ctx, spec, art) {
  if (!art || !art.image) return
  const im = art.image
  const base = Math.max(spec.largeur / im.naturalWidth, spec.hauteur / im.naturalHeight) * (art.zoom ?? 1)
  const w = im.naturalWidth * base
  const h = im.naturalHeight * base
  ctx.save()
  ctx.translate(spec.largeur / 2 + (art.x ?? 0), spec.hauteur / 2 + (art.y ?? 0))
  ctx.rotate(((art.rotation ?? 0) * Math.PI) / 180)
  ctx.drawImage(im, -w / 2, -h / 2, w, h)
  ctx.restore()
}

const ROLES_FISSURES = new Set(['base', 'shading', 'light_boxes', 'cracks'])
const ECLAT = [
  { role: 'splash', src: 'general/splash' },
  { role: 'splash_color', src: 'general/splash_color', teinte: 'splash_color' },
  { role: 'splash_dots', src: 'general/splash_dots' },
]

/**
 * La tete d'angle : retiree du createur le 29/10/2026 (reglage casse, jamais corrige). La fonction reste
 * pour ne pas toucher au modele de donnees (projets/versions deja enregistres avec un `tete.blob`) ; elle
 * ne rend plus jamais rien, et le formulaire n'offre plus aucun moyen d'en poser une nouvelle.
 */
export function teteVisible() {
  return false
}

/**
 * La pile effective : l'eclat de la tete (3 calques, variante etoile) n'y est que si la tete est visible, les calques a fissures
 * prennent leur variante `-nocracks` quand `etat.fissures === false`.
 */
export function pileDeCalques(spec, etat) {
  // « pleine illustration » : plus de cadre, l'image seule (les panneaux de texte sont poses par carte.js)
  if (etat.cadre === 'illustration') return spec.calques.filter((c) => c.role === 'photo' || c.role === 'photofront')
  let pile = spec.calques.filter((c) => !c.role.startsWith('splash'))
  // la promo generique prend un autre fond des qu'une valeur THW apparait (encarts de stats)
  if (spec.id === 'generic-promo' && etat.avecStats) pile = pile.map((c) => (c.role === 'base' ? { ...c, src: 'generic-promo/base-ally.webp' } : c))
  if (teteVisible(spec, etat) && spec.tete.splash) {
    const i = pile.findIndex((c) => c.role === 'photofront')
    const eclat = ECLAT.map((c) => ({ ...c, src: `${c.src}${etat.tete.etoile ? '-star' : ''}.webp` }))
    pile = [...pile.slice(0, i < 0 ? pile.length : i), ...eclat, ...pile.slice(i < 0 ? pile.length : i)]
  }
  return pile
}

/**
 * La pile de calques d'une carte, dans l'ordre du gabarit. `etat.couleurs` donne la couleur de chaque role teinte ;
 * `etat.art` / `etat.artDevant` : l'illustration derriere le gabarit et le premier plan par-dessus.
 */
export async function dessinerCalques(ctx, spec, etat, dossierImages = 'img/') {
  for (const calque of pileDeCalques(spec, etat)) {
    if (calque.role === 'photo') {
      dessinerArt(ctx, spec, etat.art)
      dessinerNiveau(ctx, spec, etat, 'derriere')
      continue
    }
    if (calque.role === 'photofront') {
      dessinerArt(ctx, spec, etat.artDevant)
      dessinerNiveau(ctx, spec, etat, 'devant')
      continue
    }
    let image
    if (etat.fissures === false && ROLES_FISSURES.has(calque.role)) {
      image = await chargerImage(dossierImages + calque.src.replace(/\.webp$/, '-nocracks.webp')).catch(() => null)
    }
    image ??= await chargerImage(dossierImages + calque.src)
    ctx.save()
    repereGabarit(ctx, spec)
    if (calque.melange) ctx.globalCompositeOperation = calque.melange
    if (calque.role === 'gradient') {
      const [bas, haut] = [etat.couleurs.background_lower ?? calque.degrade?.[0], etat.couleurs.background_upper ?? calque.degrade?.[1]]
      const c = document.createElement('canvas')
      c.width = PORTRAIT.l
      c.height = PORTRAIT.h
      const x = c.getContext('2d')
      x.fillStyle = degradeVersHautDroite(x, PORTRAIT.l, PORTRAIT.h, bas ?? '#888', haut ?? '#888')
      x.fillRect(0, 0, c.width, c.height)
      x.globalCompositeOperation = 'destination-out' // le degrade se voit HORS de la fenetre du masque (mask-composite: exclude)
      x.drawImage(image, 0, 0)
      ctx.drawImage(c, 0, 0)
    } else if (calque.teinte) {
      const couleur = etat.couleurs[calque.teinte] ?? spec.couleursParDefaut[calque.teinte] ?? (calque.teinte === 'splash_color' ? '#e0ca22' : '#888888')
      ctx.drawImage(teinter(image, couleur), 0, 0)
    } else {
      ctx.drawImage(image, ...(calque.pos ?? [0, 0]))
    }
    ctx.restore()
  }
}
