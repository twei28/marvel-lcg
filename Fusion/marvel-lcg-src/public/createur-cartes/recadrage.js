// Le recadrage assiste : retirer le fond d'une image (surtout pour la tete d'angle et les calques PNG), rogner sur le sujet, cadrer en carre.
// Tout se fait dans le navigateur, sans envoyer l'image nulle part.
import { dialogue, el } from './commun.js'

const MAX = 1800 // les images plus grandes sont reduites avant le travail (la tete et les calques n'ont pas besoin de plus)

async function chargerCanvas(blob) {
  const bmp = await createImageBitmap(blob)
  const k = Math.min(1, MAX / Math.max(bmp.width, bmp.height))
  const c = document.createElement('canvas')
  c.width = Math.round(bmp.width * k)
  c.height = Math.round(bmp.height * k)
  c.getContext('2d').drawImage(bmp, 0, 0, c.width, c.height)
  return c
}
const versBlob = (c) => new Promise((ok) => c.toBlob(ok, 'image/png'))

/** La couleur de fond estimee : la moyenne des quatre coins (carres de 6 px). */
export function couleurDesCoins(canvas) {
  const x = canvas.getContext('2d')
  const n = 6
  const pts = [[0, 0], [canvas.width - n, 0], [0, canvas.height - n], [canvas.width - n, canvas.height - n]]
  const somme = [0, 0, 0]
  let k = 0
  for (const [px, py] of pts) {
    const d = x.getImageData(px, py, n, n).data
    for (let i = 0; i < d.length; i += 4) { somme[0] += d[i]; somme[1] += d[i + 1]; somme[2] += d[i + 2]; k++ }
  }
  return somme.map((v) => Math.round(v / k))
}

/**
 * Retire le fond : on part des bords et on gagne de proche en proche tous les pixels proches de `fond` (distance en RGB <= tolerance) ;
 * un liseré de 25 % de tolerance devient semi-transparent pour adoucir le contour. Rend un nouveau canvas.
 */
export function retirerFond(source, fond, tolerance) {
  const w = source.width
  const h = source.height
  const sortie = document.createElement('canvas')
  sortie.width = w
  sortie.height = h
  const x = sortie.getContext('2d')
  x.drawImage(source, 0, 0)
  const img = x.getImageData(0, 0, w, h)
  const d = img.data
  const dist = (i) => Math.hypot(d[i] - fond[0], d[i + 1] - fond[1], d[i + 2] - fond[2])
  const vu = new Uint8Array(w * h)
  const pile = []
  const pousser = (px, py) => {
    const p = py * w + px
    if (vu[p]) return
    if (d[p * 4 + 3] < 8 || dist(p * 4) <= tolerance) { vu[p] = 1; pile.push(p) }
  }
  for (let i = 0; i < w; i++) { pousser(i, 0); pousser(i, h - 1) }
  for (let j = 0; j < h; j++) { pousser(0, j); pousser(w - 1, j) }
  while (pile.length) {
    const p = pile.pop()
    const px = p % w
    const py = (p - px) / w
    if (px > 0) pousser(px - 1, py)
    if (px < w - 1) pousser(px + 1, py)
    if (py > 0) pousser(px, py - 1)
    if (py < h - 1) pousser(px, py + 1)
  }
  const liseré = tolerance * 1.25
  for (let p = 0; p < w * h; p++) {
    if (vu[p]) { d[p * 4 + 3] = 0; continue }
    // un pixel de contour (voisin d'un pixel retire) proche du fond : on l'adoucit
    const px = p % w
    const py = (p - px) / w
    const voisin = (px > 0 && vu[p - 1]) || (px < w - 1 && vu[p + 1]) || (py > 0 && vu[p - w]) || (py < h - 1 && vu[p + w])
    if (voisin) {
      const dd = dist(p * 4)
      if (dd < liseré) d[p * 4 + 3] = Math.round(d[p * 4 + 3] * Math.max(0, (dd - tolerance) / (liseré - tolerance)))
    }
  }
  x.putImageData(img, 0, 0)
  return sortie
}

/** Rogne sur le sujet (pixels non transparents) avec une marge ; `carre` : le cadre devient carre, sujet centre. */
export function rognerSurSujet(source, { marge = 0.04, carre = false } = {}) {
  const w = source.width
  const h = source.height
  const d = source.getContext('2d').getImageData(0, 0, w, h).data
  let x0 = w, y0 = h, x1 = -1, y1 = -1
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (d[(y * w + x) * 4 + 3] > 12) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y }
  if (x1 < 0) return source
  const m = Math.round(Math.max(x1 - x0, y1 - y0) * marge)
  let bw = x1 - x0 + 1 + 2 * m
  let bh = y1 - y0 + 1 + 2 * m
  if (carre) bw = bh = Math.max(bw, bh)
  const sortie = document.createElement('canvas')
  sortie.width = bw
  sortie.height = bh
  sortie.getContext('2d').drawImage(source, x0 - m - (bw - (x1 - x0 + 1 + 2 * m)) / 2, y0 - m - (bh - (y1 - y0 + 1 + 2 * m)) / 2)
  return sortie
}

/**
 * La fenetre de recadrage. `blob` : l'image actuelle ; `appliquer(blobNeuf)` : appelee si l'utilisateur valide ; `carre` : proposer le
 * cadrage carre (tete d'angle). Les reglages se font sur un apercu, l'image n'est remplacee qu'a la validation.
 */
export async function ouvrirRecadrage(blob, appliquer, { carre = false } = {}) {
  const base = await chargerCanvas(blob)
  let fond = couleurDesCoins(base)
  let courant = base
  const apercu = el('canvas', { class: 'apercu-recadrage' })
  const tol = el('input', { type: 'range', min: 5, max: 160, value: 40 })
  const valTol = el('span', { class: 'aide' }, '40')
  const pastille = el('span', { class: 'pastille-fond', style: `background:rgb(${fond.join(',')})` })
  const cFond = el('input', { type: 'checkbox', checked: true })
  const cRogner = el('input', { type: 'checkbox', checked: true })
  const cCarre = el('input', { type: 'checkbox', checked: carre })
  let minuteur = 0
  const maj = () => {
    let c = base
    if (cFond.checked) c = retirerFond(c, fond, Number(tol.value))
    if (cRogner.checked || cCarre.checked) c = rognerSurSujet(c, { carre: cCarre.checked })
    courant = c
    const k = Math.min(1, 420 / Math.max(c.width, c.height))
    apercu.width = Math.round(c.width * k)
    apercu.height = Math.round(c.height * k)
    apercu.getContext('2d').drawImage(c, 0, 0, apercu.width, apercu.height)
  }
  const planifier = () => { clearTimeout(minuteur); minuteur = setTimeout(maj, 60) }
  tol.addEventListener('input', () => { valTol.textContent = tol.value; planifier() })
  for (const c of [cFond, cRogner, cCarre]) c.addEventListener('change', planifier)
  // pour choisir la couleur sur l'image d'origine : un bouton qui montre l'original
  const original = el('canvas', { class: 'apercu-recadrage', title: 'Clique pour choisir la couleur du fond à retirer' })
  const kO = Math.min(1, 260 / Math.max(base.width, base.height))
  original.width = Math.round(base.width * kO)
  original.height = Math.round(base.height * kO)
  original.getContext('2d').drawImage(base, 0, 0, original.width, original.height)
  original.addEventListener('click', (e) => {
    const r = original.getBoundingClientRect()
    const p = base.getContext('2d').getImageData(Math.round(((e.clientX - r.left) / r.width) * base.width), Math.round(((e.clientY - r.top) / r.height) * base.height), 1, 1).data
    fond = [p[0], p[1], p[2]]
    pastille.style.background = `rgb(${fond.join(',')})`
    planifier()
  })
  maj()
  dialogue('Détourer et recadrer',
    el('div', { class: 'recadrage' },
      el('div', { class: 'rang', style: 'align-items:flex-start' },
        el('div', { style: 'flex:1' }, el('div', { class: 'aide' }, 'Original (clique sur le fond pour le choisir)'), original),
        el('div', { style: 'flex:1.3' }, el('div', { class: 'aide' }, 'Résultat'), el('div', { class: 'damier' }, apercu))),
      el('label', { class: 'ligne' }, cFond, 'Retirer le fond', pastille),
      el('label', {}, el('span', { class: 'rang' }, 'Tolérance', valTol), tol),
      el('label', { class: 'ligne' }, cRogner, 'Rogner sur le sujet'),
      el('label', { class: 'ligne' }, cCarre, 'Cadrer en carré (tête d’angle)')),
    [{ texte: 'Annuler' }, { texte: 'Appliquer', principal: true, action: async () => { appliquer(await versBlob(courant)) } }])
}
