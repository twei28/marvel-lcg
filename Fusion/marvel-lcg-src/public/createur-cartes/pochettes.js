// Les pochettes (couvertures de pack : heros, scenario, modulaire, boite d'extension). Moteur de rendu repris de l'atelier de couvertures
// (tools/atelier-couvertures/modele.html), integre a MC Creator le 30/10/2026 : memes calques (extraits du PSD « Pack Template »),
// meme recoloration (on garde la luminosite et les blancs, on remplace la teinte), memes dimensions.
//
// Une pochette = un objet simple (les images sont des Blob, comme celles des cartes) :
//   { id, mode, nom, dossier, art: { blob, x, y, zoom }, titre: { texte, blob, police, haut, bas, contour, epaisseur, taille, x, y, ombre },
//     couleurBoite, couleurEtiquette, textes: [...], policeBlob }
import { nouvelId } from './commun.js'

export const DIMENSIONS = { heros: [938, 1538], scenario: [938, 1538], modulaire: [938, 1538], boite: [1000, 1000] }
export const MODES = [
  ['heros', 'Pochette héros', 'Hero Pack'],
  ['scenario', 'Pochette scénario', 'Scenario Pack'],
  ['modulaire', 'Pochette modulaire', 'Modular Set'],
  ['boite', 'Pochette extension', 'Expansion'],
]
export const NOMS_ETIQUETTE = Object.fromEntries(MODES.map(([m, , e]) => [m, e]))
// Ou tombe le titre, et sa taille, selon le gabarit.
const TITRE = {
  heros: { cx: 938 / 2, cy: 200, taille: 230, largeur: 860, apresBoite: false },
  scenario: { cx: 938 / 2, cy: 1330, taille: 120, largeur: 760, apresBoite: true },
  modulaire: { cx: 938 / 2, cy: 1330, taille: 120, largeur: 760, apresBoite: true },
  boite: { cx: 500, cy: 858, taille: 72, largeur: 760, apresBoite: true },
}
const COUCHES = {
  heros: { boite: 'heros-boite', logos: 'heros-logos', etiquette: 'heros-etiquette' },
  scenario: { boite: 'scenario-boite', logos: 'scenario-logos', etiquette: 'scenario-etiquette' },
  modulaire: { boite: 'scenario-boite', logos: 'scenario-logos', etiquette: 'modulaire-etiquette' },
  boite: { boite: 'boite-boite', logos: 'boite-logos', etiquette: 'boite-etiquette' },
}
export const POLICES = [
  ["'BangersUI', Impact, sans-serif", 'Bangers'],
  ["Impact, 'Arial Narrow Bold', sans-serif", 'Impact'],
  ["'Arial Black', Arial, sans-serif", 'Arial Black'],
  ['Georgia, serif', 'Georgia gras'],
  ["'Trebuchet MS', sans-serif", 'Trebuchet gras'],
  ["'Courier New', monospace", 'Courier gras'],
]
export const POLICE_PERSO = '__perso'

// ---- les calques (PNG du PSD)
let images = null
let prets = null
export function chargerCalques(base) {
  if (prets) return prets
  const noms = ['boite-boite', 'boite-etiquette', 'boite-logos', 'heros-boite', 'heros-etiquette', 'heros-logos', 'modulaire-etiquette', 'scenario-boite', 'scenario-etiquette', 'scenario-logos']
  images = {}
  prets = Promise.all(noms.map((n) => new Promise((ok) => {
    const im = new Image()
    im.onload = () => { images[n] = im; ok() }
    im.onerror = () => ok()
    im.src = `${base}${n}.png`
  })))
  return prets
}

// ---- le modele
export function titreDefaut(mode) {
  return { texte: '', blob: null, police: POLICES[0][0], haut: '#e23a6a', bas: '#a3123a', contour: '#ffffff', epaisseur: 0, taille: TITRE[mode].taille, x: 0, y: 0, ombre: true }
}
export function nouvellePochette(mode = 'heros', dossier = '') {
  return {
    id: nouvelId(), mode, nom: '', dossier,
    art: { blob: null, x: 0, y: 0, zoom: 1 }, titre: titreDefaut(mode),
    couleurBoite: null, couleurEtiquette: null, textes: [], policeBlob: null,
  }
}
export function texteLibre(mode, langue = 'en') {
  const [L, H] = DIMENSIONS[mode]
  return { texte: langue === 'fr' ? 'Créé par …' : 'Created by …', police: POLICES[0][0], taille: 44, couleur: '#ffffff', contour: '#000000', epaisseur: 6, x: L / 2, y: H - 40, ombre: true, gras: true }
}
/** Change le gabarit d'une pochette : le titre reprend la taille et la position du nouveau gabarit. */
export function changerMode(p, mode) {
  p.mode = mode
  p.titre.taille = TITRE[mode].taille
  p.titre.x = 0
  p.titre.y = 0
  for (const t of p.textes) { const [L, H] = DIMENSIONS[mode]; t.x = Math.min(t.x, L); t.y = Math.min(t.y, H) }
}

// ---- recoloration
function rgbVersHsl(r, g, b) {
  r /= 255; g /= 255; b /= 255
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2
  if (mx === mn) return [0, 0, l]
  const d = mx - mn
  const s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn)
  const h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4
  return [h / 6, s, l]
}
function hslVersRgb(h, s, l) {
  if (s === 0) return [l * 255, l * 255, l * 255]
  const q = l < 0.5 ? l * (1 + s) : l + s - l * s, p = 2 * l - q
  const f = (t) => { t = (t + 1) % 1; return t < 1 / 6 ? p + (q - p) * 6 * t : t < 0.5 ? q : t < 2 / 3 ? p + (q - p) * (2 / 3 - t) * 6 : p }
  return [f(h + 1 / 3) * 255, f(h) * 255, f(h - 1 / 3) * 255]
}
const hexVersHsl = (hex) => rgbVersHsl(parseInt(hex.slice(1, 3), 16), parseInt(hex.slice(3, 5), 16), parseInt(hex.slice(5, 7), 16))
const hslVersHex = (h, s, l) => '#' + hslVersRgb(h, s, l).map((v) => Math.round(v).toString(16).padStart(2, '0')).join('')
const referenceCache = {}
function referenceDe(nom) {
  if (referenceCache[nom]) return referenceCache[nom]
  const im = images[nom]
  const c = document.createElement('canvas'); c.width = im.width; c.height = im.height
  const x = c.getContext('2d', { willReadFrequently: true }); x.drawImage(im, 0, 0)
  const d = x.getImageData(0, 0, im.width, im.height).data
  let sx = 0, sy = 0, ss = 0, sl = 0, n = 0
  for (let i = 0; i < d.length; i += 4) {
    if (d[i + 3] < 200) continue
    const [h, s, l] = rgbVersHsl(d[i], d[i + 1], d[i + 2])
    if (s < 0.25 || l < 0.08 || l > 0.92) continue
    sx += Math.cos(h * 2 * Math.PI); sy += Math.sin(h * 2 * Math.PI); ss += s; sl += l; n++
  }
  const h = n ? (Math.atan2(sy, sx) / (2 * Math.PI) + 1) % 1 : 0
  return (referenceCache[nom] = { h, s: n ? ss / n : 0.7, l: n ? sl / n : 0.4 })
}
/** La couleur d'origine (hex) d'un calque (la boite ou l'etiquette) : celle du PSD. */
export function couleurOrigine(mode, quoi) {
  const nom = COUCHES[mode][quoi]
  if (!images?.[nom]) return '#c0392b'
  const r = referenceDe(nom)
  return hslVersHex(r.h, r.s, r.l)
}
const recolorees = new Map()
function recolorer(nom, hex) {
  const cle = nom + hex
  if (recolorees.has(cle)) return recolorees.get(cle)
  const im = images[nom]
  const ref = referenceDe(nom), [th, ts, tl] = hexVersHsl(hex)
  const c = document.createElement('canvas'); c.width = im.width; c.height = im.height
  const x = c.getContext('2d', { willReadFrequently: true }); x.drawImage(im, 0, 0)
  const img = x.getImageData(0, 0, im.width, im.height), d = img.data
  for (let i = 0; i < d.length; i += 4) {
    if (!d[i + 3]) continue
    const [h, s, l] = rgbVersHsl(d[i], d[i + 1], d[i + 2])
    if (s < 0.12) continue // blancs et gris : le trait blanc de la boite reste blanc
    const poids = Math.min(1, s / 0.25)
    const ns = Math.min(1, s * (ts / Math.max(ref.s, 0.05)))
    const nl = Math.min(0.98, Math.max(0.02, l + (tl - ref.l)))
    const [r, g, b] = hslVersRgb(th, ns, nl)
    d[i] = d[i] + (r - d[i]) * poids; d[i + 1] = d[i + 1] + (g - d[i + 1]) * poids; d[i + 2] = d[i + 2] + (b - d[i + 2]) * poids
  }
  x.putImageData(img, 0, 0)
  if (recolorees.size > 24) recolorees.clear()
  recolorees.set(cle, c)
  return c
}
const couche = (nom, choisi, origine) => (choisi && choisi.toLowerCase() !== origine.toLowerCase() ? recolorer(nom, choisi) : images[nom])

// ---- images (Blob -> Image) et polices personnelles
const lues = new WeakMap()
function lire(blob) {
  if (!blob) return Promise.resolve(null)
  if (!lues.has(blob)) lues.set(blob, new Promise((ok) => { const im = new Image(); im.onload = () => ok(im); im.onerror = () => ok(null); im.src = URL.createObjectURL(blob) }))
  return lues.get(blob)
}
const policesChargees = new WeakMap()
async function policePerso(p) {
  if (!p.policeBlob) return 'sans-serif'
  if (!policesChargees.has(p.policeBlob)) {
    const famille = 'PochettePerso' + p.id
    policesChargees.set(p.policeBlob, (async () => { const f = new FontFace(famille, await p.policeBlob.arrayBuffer()); await f.load(); document.fonts.add(f); return `'${famille}'` })().catch(() => 'sans-serif'))
  }
  return policesChargees.get(p.policeBlob)
}

// ---- dessin
/** Dessine une pochette sur un canvas neuf. `canvas.boites` : les zones des textes libres (pour les pointer a la souris). */
export async function rendrePochette(p, { choisi = -1, apercu = true } = {}) {
  await chargerCalques('/createur-cartes/img/pochettes/')
  try { await document.fonts.load("40px 'BangersUI'") } catch {}
  const [L, H] = DIMENSIONS[p.mode]
  const toile = document.createElement('canvas'); toile.width = L; toile.height = H
  const ctx = toile.getContext('2d')
  const cfg = TITRE[p.mode], c = COUCHES[p.mode]
  const [art, titreImg, perso] = await Promise.all([lire(p.art.blob), lire(p.titre.blob), policePerso(p)])
  const police = (v) => (v === POLICE_PERSO ? perso : v)
  // l'illustration
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, L, H)
  if (!art) {
    if (apercu) {
      ctx.fillStyle = '#2a2d36'; ctx.fillRect(0, 0, L, H)
      ctx.fillStyle = '#9aa1ad'; ctx.font = '600 44px system-ui, sans-serif'; ctx.textAlign = 'center'
      ctx.fillText(p.mode === 'boite' ? 'Illustration' : 'Illustration', L / 2, H / 2 - (p.mode === 'boite' ? 300 : 600))
    }
  } else {
    const base = Math.max(L / art.width, H / art.height) * p.art.zoom
    const w = art.width * base, h = art.height * base
    ctx.drawImage(art, (L - w) / 2 + p.art.x, (H - h) / 2 + p.art.y, w, h)
  }
  const titre = () => {
    const t = p.titre
    if (titreImg) {
      const k = Math.min(cfg.largeur / titreImg.width, 1.5) * (t.taille / cfg.taille)
      const w = titreImg.width * k, h = titreImg.height * k
      ctx.drawImage(titreImg, cfg.cx + t.x - w / 2, cfg.cy + t.y - h / 2, w, h)
      return
    }
    const texte = (t.texte || '').replace(/\s+$/, '')
    if (!texte) return
    const lignes = texte.split('\n')
    let taille = t.taille
    ctx.save()
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round'
    const fam = police(t.police)
    const mesure = () => { ctx.font = `${taille}px ${fam}`; return Math.max(...lignes.map((l) => ctx.measureText(l).width)) }
    const large = mesure()
    if (large > cfg.largeur) { taille *= cfg.largeur / large; mesure() }
    const inter = taille * 0.92, hauteur = inter * lignes.length
    const y0 = cfg.cy + t.y - hauteur / 2 + inter / 2
    const grad = ctx.createLinearGradient(0, y0 - inter / 2, 0, y0 - inter / 2 + hauteur)
    grad.addColorStop(0, t.haut); grad.addColorStop(1, t.bas)
    lignes.forEach((ligne, i) => {
      const x = cfg.cx + t.x, y = y0 + i * inter
      if (t.ombre) { ctx.shadowColor = 'rgba(0,0,0,.55)'; ctx.shadowBlur = taille * 0.06; ctx.shadowOffsetY = taille * 0.04 }
      if (t.epaisseur > 0) { ctx.strokeStyle = t.contour; ctx.lineWidth = t.epaisseur; ctx.strokeText(ligne, x, y) }
      ctx.fillStyle = grad; ctx.fillText(ligne, x, y)
      ctx.shadowColor = 'transparent'
    })
    ctx.restore()
  }
  if (!cfg.apresBoite) titre()
  ctx.drawImage(couche(c.boite, p.couleurBoite, couleurOrigine(p.mode, 'boite')), 0, 0)
  if (cfg.apresBoite) titre()
  ctx.drawImage(images[c.logos], 0, 0)
  ctx.drawImage(couche(c.etiquette, p.couleurEtiquette, couleurOrigine(p.mode, 'etiquette')), 0, 0)
  // les textes libres (mentions, nom du createur...)
  toile.boites = []
  p.textes.forEach((t, i) => {
    const lignes = (t.texte || '').split('\n')
    if (!lignes.join('').trim()) { toile.boites[i] = null; return }
    ctx.save()
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round'
    ctx.font = `${t.gras ? 'bold ' : ''}${t.taille}px ${police(t.police)}`
    const inter = t.taille * 1.15, haut = inter * lignes.length
    const large = Math.max(...lignes.map((l) => ctx.measureText(l).width))
    const y0 = t.y - haut / 2 + inter / 2
    lignes.forEach((ligne, k) => {
      const y = y0 + k * inter
      if (t.ombre) { ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = t.taille * 0.08; ctx.shadowOffsetY = t.taille * 0.04 }
      if (t.epaisseur > 0) { ctx.strokeStyle = t.contour; ctx.lineWidth = t.epaisseur; ctx.strokeText(ligne, t.x, y) }
      ctx.fillStyle = t.couleur; ctx.fillText(ligne, t.x, y)
      ctx.shadowColor = 'transparent'
    })
    toile.boites[i] = { x: t.x - large / 2 - 8, y: t.y - haut / 2 - 8, l: large + 16, h: haut + 16 }
    if (apercu && i === choisi) { ctx.setLineDash([10, 8]); ctx.lineWidth = 3; ctx.strokeStyle = '#3f86e0'; ctx.strokeRect(toile.boites[i].x, toile.boites[i].y, toile.boites[i].l, toile.boites[i].h) }
    ctx.restore()
  })
  return toile
}

/** Un nom de fichier propre pour l'export. */
export function nomFichierPochette(p) {
  const base = (p.nom || p.titre.texte.split('\n')[0] || 'pochette').toLowerCase().normalize('NFD').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')
  return `${base || 'pochette'}-${p.mode}`
}
