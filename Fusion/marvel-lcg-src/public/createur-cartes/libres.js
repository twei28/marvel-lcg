// Les calques PNG libres : des images posees sur la carte, deplacables, tournables, avec opacite, miroir, teinte, contour et ombre.
//
// Un calque : { id, blob, nom, niveau: 'derriere' | 'devant' | 'dessus', fx, fy (centre, en fraction de la carte), echelle (largeur en
// fraction de la carte), rot (degres), opacite (0-1), miroirH, miroirV, teinte: null | '#rrggbb', contour: null | { couleur, epaisseur },
// ombre: null | { couleur, flou, dx, dy } }.
// `niveau` : derriere = sous le cadre (avec l'illustration), devant = par-dessus le cadre mais sous les textes, dessus = par-dessus tout.
import { ICONES } from './polices.js'

export const NIVEAUX = [
  ['derriere', 'Derrière le cadre'],
  ['devant', 'Devant le cadre'],
  ['dessus', 'Au-dessus du texte'],
]

const cacheTeintes = new WeakMap()

/** L'image du calque, teintee d'une couleur unie (alpha conserve). */
function teintee(image, couleur) {
  let m = cacheTeintes.get(image)
  if (!m) cacheTeintes.set(image, (m = new Map()))
  if (m.has(couleur)) return m.get(couleur)
  const c = document.createElement('canvas')
  c.width = image.naturalWidth
  c.height = image.naturalHeight
  const x = c.getContext('2d')
  x.drawImage(image, 0, 0)
  x.globalCompositeOperation = 'source-in'
  x.fillStyle = couleur
  x.fillRect(0, 0, c.width, c.height)
  if (m.size > 20) m.clear()
  m.set(couleur, c)
  return c
}

/** Le rectangle du calque, en pixels de carte : { cx, cy, w, h, rot }. */
export function boiteLibre(spec, L, image) {
  const w = (L.echelle ?? 0.3) * spec.largeur
  const h = w * (image.naturalHeight / image.naturalWidth)
  return { cx: (L.fx ?? 0.5) * spec.largeur, cy: (L.fy ?? 0.5) * spec.hauteur, w, h, rot: L.rot ?? 0 }
}

/** Dessine un calque libre. `image` : l'image deja chargee. */
export function dessinerLibre(ctx, spec, L, image) {
  if (!image) return
  const { cx, cy, w, h, rot } = boiteLibre(spec, L, image)
  ctx.save()
  ctx.globalAlpha = Math.max(0, Math.min(1, L.opacite ?? 1))
  ctx.translate(cx, cy)
  ctx.rotate((rot * Math.PI) / 180)
  ctx.scale(L.miroirH ? -1 : 1, L.miroirV ? -1 : 1)
  const source = L.teinte ? teintee(image, L.teinte) : image
  if (L.contour && L.contour.epaisseur > 0) {
    const e = L.contour.epaisseur
    const silhouette = teintee(image, L.contour.couleur || '#000000')
    const n = Math.max(12, Math.round(e * 3))
    for (let k = 0; k < n; k++) {
      const a = (k / n) * Math.PI * 2
      ctx.drawImage(silhouette, -w / 2 + Math.cos(a) * e, -h / 2 + Math.sin(a) * e, w, h)
    }
  }
  if (L.ombre) {
    ctx.shadowColor = L.ombre.couleur || '#000000'
    ctx.shadowBlur = L.ombre.flou ?? 10
    // le decalage de l'ombre est en pixels d'ecran : on le ramene dans le repere tourne
    const a = (-rot * Math.PI) / 180
    const dx = L.ombre.dx ?? 8
    const dy = L.ombre.dy ?? 8
    ctx.shadowOffsetX = (dx * Math.cos(a) - dy * Math.sin(a)) * (L.miroirH ? -1 : 1)
    ctx.shadowOffsetY = (dx * Math.sin(a) + dy * Math.cos(a)) * (L.miroirV ? -1 : 1)
  }
  ctx.drawImage(source, -w / 2, -h / 2, w, h)
  ctx.restore()
}

/** Dessine les calques d'un niveau, dans l'ordre de la liste (le dernier est au-dessus). */
export function dessinerNiveau(ctx, spec, etat, niveau) {
  for (const L of etat.libres ?? []) if ((L.niveau ?? 'devant') === niveau && L.visible !== false) dessinerLibre(ctx, spec, L, L.image)
}

/** Le calque sous le point (x, y) (pixels de carte), du dessus au dessous. */
export function calqueSous(spec, libres, x, y) {
  for (let i = libres.length - 1; i >= 0; i--) {
    const L = libres[i]
    if (!L.image || L.visible === false) continue
    const b = boiteLibre(spec, L, L.image)
    const a = (-b.rot * Math.PI) / 180
    const dx = x - b.cx
    const dy = y - b.cy
    const lx = dx * Math.cos(a) - dy * Math.sin(a)
    const ly = dx * Math.sin(a) + dy * Math.cos(a)
    if (Math.abs(lx) <= b.w / 2 && Math.abs(ly) <= b.h / 2) return L
  }
  return null
}

// ---------------------------------------------------------------- bibliotheque d'icones pretes
/** Un canvas -> Blob PNG. */
const versBlob = (c) => new Promise((ok) => c.toBlob(ok, 'image/png'))

/** Une icone de la police du jeu, en blanc sur fond transparent (on la teinte ensuite). */
async function iconePolice(lettre, taille = 400) {
  const c = document.createElement('canvas')
  c.width = c.height = taille
  const x = c.getContext('2d')
  x.fillStyle = '#ffffff'
  x.font = `${taille * 0.8}px ChampionsIcons`
  x.textAlign = 'center'
  x.textBaseline = 'middle'
  x.fillText(lettre, taille / 2, taille / 2 + taille * 0.04)
  return versBlob(c)
}

function forme(nom, taille = 400) {
  const c = document.createElement('canvas')
  c.width = c.height = taille
  const x = c.getContext('2d')
  x.fillStyle = '#ffffff'
  const m = taille * 0.06
  x.beginPath()
  if (nom === 'rond') x.arc(taille / 2, taille / 2, taille / 2 - m, 0, Math.PI * 2)
  else if (nom === 'carre') x.roundRect(m, m, taille - 2 * m, taille - 2 * m, taille * 0.16)
  else if (nom === 'bandeau') { c.height = taille / 3; x.roundRect(m, m, taille - 2 * m, taille / 3 - 2 * m, taille * 0.05) }
  else if (nom === 'losange') { x.moveTo(taille / 2, m); x.lineTo(taille - m, taille / 2); x.lineTo(taille / 2, taille - m); x.lineTo(m, taille / 2); x.closePath() }
  else if (nom === 'bulle') {
    x.ellipse(taille / 2, taille * 0.45, taille / 2 - m, taille * 0.34, 0, 0, Math.PI * 2)
    x.moveTo(taille * 0.3, taille * 0.74); x.lineTo(taille * 0.2, taille - m); x.lineTo(taille * 0.5, taille * 0.78); x.closePath()
  } else if (nom === 'explosion') {
    const n = 12
    for (let i = 0; i < n * 2; i++) {
      const r = (i % 2 ? 0.28 : 0.48) * taille
      const a = (i / (n * 2)) * Math.PI * 2 - Math.PI / 2
      x[i ? 'lineTo' : 'moveTo'](taille / 2 + Math.cos(a) * r, taille / 2 + Math.sin(a) * r)
    }
    x.closePath()
  }
  x.fill()
  return c
}

const NOMS_ICONES = {
  energy: 'Énergie', mental: 'Mental', physical: 'Physique', wild: 'Joker', star: 'Étoile', acceleration: 'Accélération', crisis: 'Crise', hazard: 'Aléas',
  boost: 'Boost', per_hero: 'Par joueur', consequential: 'Dégâts conséquents', unique: 'Unique', amplify: 'Amplification', infinity: 'Infini',
}
const FORMES = [['rond', 'Rond'], ['carre', 'Carré arrondi'], ['bandeau', 'Bandeau'], ['losange', 'Losange'], ['bulle', 'Bulle'], ['explosion', 'Explosion']]
const IMAGES_JEU = [['general/resource-energy', 'Ressource énergie'], ['general/resource-mental', 'Ressource mental'], ['general/resource-physical', 'Ressource physique'], ['general/resource-wild', 'Ressource joker'], ['general/boost_icon', 'Icône de boost'], ['general/boost_star', 'Icône d’étoile']]

/** Le catalogue : [{ groupe, id, nom, fabriquer: async () => Blob, teintable }]. */
export function bibliotheque(dossierImages = 'img/') {
  const liste = []
  for (const [nom, titre] of Object.entries(NOMS_ICONES)) liste.push({ groupe: 'Icônes du jeu', id: 'icone-' + nom, nom: titre, teintable: true, lettre: ICONES[nom], fabriquer: () => iconePolice(ICONES[nom]) })
  for (const [nom, titre] of FORMES) liste.push({ groupe: 'Formes (teintables)', id: 'forme-' + nom, nom: titre, teintable: true, fabriquer: () => versBlob(forme(nom)) })
  for (const [src, titre] of IMAGES_JEU) liste.push({ groupe: 'Images du jeu', id: src, nom: titre, teintable: false, fabriquer: async () => (await fetch(`${dossierImages}${src}.webp`)).blob() })
  return liste
}

/** Un calque neuf pour une image : au centre, un tiers de la largeur, devant le cadre. */
export function nouveauLibre(blob, nom, extra = {}) {
  return {
    id: Math.random().toString(36).slice(2, 9), blob, nom, niveau: 'devant', fx: 0.5, fy: 0.5, echelle: 0.3, rot: 0, opacite: 1,
    miroirH: false, miroirV: false, teinte: null, contour: null, ombre: null, visible: true, ...extra,
  }
}
