// Le panneau et la poignee des calques PNG libres : liste, reglages, bibliotheque, et deplacement / zoom / rotation sur l'apercu.
import { el, S } from './commun.js'
import { ouvrirRecadrage } from './recadrage.js'
import { NIVEAUX, bibliotheque, boiteLibre, calqueSous, nouveauLibre } from './libres.js'

let selectionnee = null // id du calque choisi
export const calqueChoisi = () => (S.carte()?.libres ?? []).find((L) => L.id === selectionnee) ?? null
export function choisirCalque(id) {
  selectionnee = id
  dessinerSurcouche()
}

/** Ajoute des fichiers image comme calques. */
export async function ajouterFichiers(fichiers) {
  const c = S.carte()
  let dernier = null
  for (const f of fichiers) {
    if (!f.type.startsWith('image/')) continue
    const L = nouveauLibre(f, f.name.replace(/\.[^.]+$/, ''))
    // les images tres larges ne depassent pas la carte
    c.libres.push(L)
    dernier = L
  }
  if (dernier) selectionnee = dernier.id
  S.changement()
  S.reconstruire()
}

function curseurLibre(label, L, cle, min, max, pas, defaut, fmt = (v) => v) {
  const r = el('input', { type: 'range', min, max, step: pas })
  r.value = L[cle] ?? defaut
  const val = el('span', { class: 'aide' }, fmt(Number(r.value)))
  r.addEventListener('input', () => { L[cle] = Number(r.value); val.textContent = fmt(L[cle]); S.changement(); dessinerSurcouche() })
  r.addEventListener('dblclick', () => { r.value = defaut; L[cle] = defaut; val.textContent = fmt(defaut); S.changement(); dessinerSurcouche() })
  return el('label', {}, el('span', { class: 'rang' }, label, val), r)
}
function caseLibre(label, valeur, quand) {
  const i = el('input', { type: 'checkbox' })
  i.checked = !!valeur
  i.addEventListener('change', () => quand(i.checked))
  return el('label', { class: 'ligne' }, i, label)
}
function couleurLibre(valeur, quand, titre) {
  const i = el('input', { type: 'color', value: valeur || '#000000', title: titre })
  i.addEventListener('input', () => quand(i.value))
  return i
}

function reglages(L) {
  const maj = () => { S.changement(); dessinerSurcouche() }
  const niveau = el('select', {}, NIVEAUX.map(([v, n]) => el('option', { value: v }, n)))
  niveau.value = L.niveau
  niveau.addEventListener('change', () => { L.niveau = niveau.value; maj() })
  const nom = el('input', { type: 'text', value: L.nom ?? '' })
  nom.addEventListener('input', () => { L.nom = nom.value; S.changement() })
  const contourOn = !!L.contour
  const ombreOn = !!L.ombre
  return el('div', { class: 'contenu', style: 'gap:6px' },
    el('label', {}, 'Nom', nom),
    el('label', {}, 'Position', niveau),
    curseurLibre('Taille', L, 'echelle', 0.02, 2, 0.005, 0.3, (v) => Math.round(v * 100) + ' %'),
    curseurLibre('Rotation', L, 'rot', -180, 180, 1, 0, (v) => v + '°'),
    curseurLibre('Opacité', L, 'opacite', 0, 1, 0.01, 1, (v) => Math.round(v * 100) + ' %'),
    el('div', { class: 'rang' },
      caseLibre('Miroir ↔', L.miroirH, (v) => { L.miroirH = v; maj() }),
      caseLibre('Miroir ↕', L.miroirV, (v) => { L.miroirV = v; maj() })),
    el('div', { class: 'rang' },
      caseLibre('Teinte', L.teinte, (v) => { L.teinte = v ? L.teinte || '#ffffff' : null; maj(); S.reconstruire() }),
      L.teinte ? couleurLibre(L.teinte, (v) => { L.teinte = v; maj() }, 'Couleur de la teinte') : null),
    el('div', { class: 'rang' },
      caseLibre('Contour', contourOn, (v) => { L.contour = v ? L.contour || { couleur: '#000000', epaisseur: 6 } : null; maj(); S.reconstruire() }),
      L.contour ? couleurLibre(L.contour.couleur, (v) => { L.contour.couleur = v; maj() }, 'Couleur du contour') : null),
    L.contour ? curseurLibre('Épaisseur du contour', L.contour, 'epaisseur', 1, 40, 1, 6, (v) => v + ' px') : null,
    el('div', { class: 'rang' },
      caseLibre('Ombre', ombreOn, (v) => { L.ombre = v ? L.ombre || { couleur: '#000000', flou: 12, dx: 8, dy: 10 } : null; maj(); S.reconstruire() }),
      L.ombre ? couleurLibre(L.ombre.couleur, (v) => { L.ombre.couleur = v; maj() }, 'Couleur de l’ombre') : null),
    L.ombre ? curseurLibre('Flou de l’ombre', L.ombre, 'flou', 0, 60, 1, 12, (v) => v + ' px') : null,
    el('div', { class: 'rang' },
      el('button', { class: 'btn petit', type: 'button', onclick: () => { L.fx = 0.5; L.fy = 0.5; maj() } }, 'Centrer'),
      el('button', { class: 'btn petit', type: 'button', onclick: () => ouvrirRecadrage(L.blob, (nb) => { L.blob = nb; S.changement(); S.reconstruire() }) }, 'Détourer / recadrer…'),
      el('button', { class: 'btn petit', type: 'button', onclick: () => { L.rot = 0; L.miroirH = false; L.miroirV = false; maj(); S.reconstruire() } }, 'Remettre droit')))
}

/** La section « Calques PNG » du formulaire. */
export function sectionLibres() {
  const c = S.carte()
  const liste = el('div', { class: 'liste-libres' })
  const bouge = (L, d) => {
    const i = c.libres.indexOf(L)
    const j = i + d
    if (j < 0 || j >= c.libres.length) return
    c.libres.splice(i, 1)
    c.libres.splice(j, 0, L)
    S.changement()
    S.reconstruire()
  }
  for (const L of [...c.libres].reverse()) {
    const ligne = el('div', { class: 'ligne-libre' + (L.id === selectionnee ? ' choisie' : '') },
      el('button', { class: 'btn petit nom-libre', type: 'button', onclick: () => { selectionnee = L.id; S.reconstruire(); dessinerSurcouche() } }, (L.visible === false ? '🚫 ' : '') + (L.nom || 'image')),
      el('button', { class: 'btn petit', type: 'button', title: 'Monter', onclick: () => bouge(L, 1) }, '↑'),
      el('button', { class: 'btn petit', type: 'button', title: 'Descendre', onclick: () => bouge(L, -1) }, '↓'),
      el('button', { class: 'btn petit', type: 'button', title: 'Afficher / masquer', onclick: () => { L.visible = L.visible === false; S.changement(); S.reconstruire() } }, '👁'),
      el('button', { class: 'btn petit', type: 'button', title: 'Dupliquer', onclick: () => { const d = { ...structuredClone({ ...L, blob: null }), blob: L.blob, id: Math.random().toString(36).slice(2, 9), fx: Math.min(1, L.fx + 0.04), fy: Math.min(1, L.fy + 0.04) }; c.libres.splice(c.libres.indexOf(L) + 1, 0, d); selectionnee = d.id; S.changement(); S.reconstruire() } }, '⧉'),
      el('button', { class: 'btn petit', type: 'button', title: 'Supprimer', onclick: () => { c.libres.splice(c.libres.indexOf(L), 1); if (selectionnee === L.id) selectionnee = null; S.changement(); S.reconstruire() } }, '✕'))
    liste.append(ligne)
  }
  if (!c.libres.length) liste.append(el('div', { class: 'aide' }, 'Aucun calque. Ajoute un PNG (ou glisse-le sur l’aperçu) ou prends une icône dans la bibliothèque.'))

  const fichier = el('input', { type: 'file', accept: 'image/*', multiple: true })
  fichier.addEventListener('change', () => ajouterFichiers([...fichier.files]))

  const biblio = el('details', {}, el('summary', {}, 'Bibliothèque (icônes, formes, images du jeu)'))
  const grille = el('div', { class: 'contenu' })
  let groupe = null
  let rang = null
  for (const item of bibliotheque('/createur-cartes/img/')) {
    if (item.groupe !== groupe) {
      groupe = item.groupe
      grille.append(el('h2', {}, groupe))
      rang = el('div', { class: 'outils' })
      grille.append(rang)
    }
    rang.append(el('button', {
      class: 'btn petit', type: 'button', title: item.nom, style: item.lettre ? 'font-family:ChampionsIcons;font-size:16px;min-width:32px' : '',
      onclick: async () => {
        const L = nouveauLibre(await item.fabriquer(), item.nom, { echelle: item.lettre ? 0.12 : item.groupe.startsWith('Formes') ? 0.2 : 0.14, teinte: item.teintable ? '#ffffff' : null })
        c.libres.push(L)
        selectionnee = L.id
        S.changement()
        S.reconstruire()
      },
    }, item.lettre ?? item.nom))
  }
  biblio.append(grille)

  const L = calqueChoisi()
  return el('details', { open: c.libres.length > 0 }, el('summary', {}, 'Calques PNG'),
    el('div', { class: 'contenu' },
      el('label', {}, 'Ajouter des PNG (ou glisse-les sur l’aperçu)', fichier),
      biblio, liste,
      L ? reglages(L) : null))
}

// ---------------------------------------------------------------- surcouche (selection, poignees)
let surcouche = null
let toileRef = null
export function brancherSurcouche(sur, toile) {
  surcouche = sur
  toileRef = toile
}
const rayon = () => (toileRef ? toileRef.width / toileRef.getBoundingClientRect().width : 1)

/** Trace le cadre de selection du calque choisi (sur la surcouche, jamais dans l'image). */
export function dessinerSurcouche() {
  if (!surcouche || !toileRef) return
  surcouche.width = toileRef.width
  surcouche.height = toileRef.height
  const x = surcouche.getContext('2d')
  x.clearRect(0, 0, surcouche.width, surcouche.height)
  const c = S.carte()
  const L = calqueChoisi()
  if (!c || !L || L.visible === false) return
  const im = S.imageSync(L.blob)
  if (!im) return
  const spec = S.types[c.type]
  const b = boiteLibre(spec, L, im)
  const k = rayon()
  x.save()
  x.translate(b.cx, b.cy)
  x.rotate((b.rot * Math.PI) / 180)
  x.lineWidth = 2 * k
  x.strokeStyle = '#ff3b3b'
  x.setLineDash([8 * k, 5 * k])
  x.strokeRect(-b.w / 2, -b.h / 2, b.w, b.h)
  x.setLineDash([])
  x.fillStyle = '#fff'
  const p = 7 * k
  for (const [px, py] of [[b.w / 2, b.h / 2], [-b.w / 2, b.h / 2], [b.w / 2, -b.h / 2], [-b.w / 2, -b.h / 2]]) { x.fillRect(px - p, py - p, 2 * p, 2 * p); x.strokeRect(px - p, py - p, 2 * p, 2 * p) }
  x.beginPath()
  x.moveTo(0, -b.h / 2)
  x.lineTo(0, -b.h / 2 - 38 * k)
  x.stroke()
  x.beginPath()
  x.arc(0, -b.h / 2 - 38 * k, 8 * k, 0, Math.PI * 2)
  x.fill()
  x.stroke()
  x.restore()
}

/** Le point de la souris en pixels de carte. */
function pointCarte(e) {
  const r = toileRef.getBoundingClientRect()
  return [((e.clientX - r.left) / r.width) * toileRef.width, ((e.clientY - r.top) / r.height) * toileRef.height]
}

/**
 * Appele au debut d'un glisser sur l'apercu. Rend une fonction « deplacer(e) » si un calque libre (ou l'une de ses poignees)
 * est touche, sinon null (l'appelant laisse alors l'illustration prendre la main).
 */
export function commencerGlisser(e) {
  const c = S.carte()
  if (!c?.libres?.length) return null
  const spec = S.types[c.type]
  const images = c.libres.map((L) => ({ ...L, image: S.imageSync(L.blob) }))
  const [x, y] = pointCarte(e)
  const k = rayon()
  const L0 = calqueChoisi()
  let cible = null
  let mode = 'deplacer'
  if (L0 && L0.visible !== false && S.imageSync(L0.blob)) {
    const b = boiteLibre(spec, L0, S.imageSync(L0.blob))
    const a = (-b.rot * Math.PI) / 180
    const lx = (x - b.cx) * Math.cos(a) - (y - b.cy) * Math.sin(a)
    const ly = (x - b.cx) * Math.sin(a) + (y - b.cy) * Math.cos(a)
    if (Math.hypot(lx, ly + b.h / 2 + 38 * k) < 16 * k) { cible = L0; mode = 'tourner' }
    else if (Math.hypot(Math.abs(lx) - b.w / 2, Math.abs(ly) - b.h / 2) < 16 * k) { cible = L0; mode = 'taille' }
  }
  if (!cible) {
    const touche = calqueSous(spec, images, x, y)
    if (!touche) return null
    cible = c.libres.find((L) => L.id === touche.id)
    selectionnee = cible.id
    S.reconstruire()
  }
  const depart = { x, y, fx: cible.fx, fy: cible.fy }
  return {
    deplacer(ev) {
      const [mx, my] = pointCarte(ev)
      if (mode === 'deplacer') {
        cible.fx = depart.fx + (mx - depart.x) / spec.largeur
        cible.fy = depart.fy + (my - depart.y) / spec.hauteur
      } else if (mode === 'tourner') {
        const cx = cible.fx * spec.largeur
        const cy = cible.fy * spec.hauteur
        let r = (Math.atan2(my - cy, mx - cx) * 180) / Math.PI + 90
        if (ev.shiftKey) r = Math.round(r / 15) * 15
        cible.rot = Math.round(((r + 540) % 360) - 180)
      } else {
        const im = S.imageSync(cible.blob)
        const b = boiteLibre(spec, cible, im)
        const a = (-b.rot * Math.PI) / 180
        const lx = (mx - b.cx) * Math.cos(a) - (my - b.cy) * Math.sin(a)
        cible.echelle = Math.max(0.02, Math.min(3, (2 * Math.abs(lx)) / spec.largeur))
      }
      S.changement()
      dessinerSurcouche()
    },
    fin() { S.reconstruire() },
  }
}

/** Molette sur le calque choisi : zoom. Rend vrai si l'evenement est pris. */
export function molette(e) {
  const L = calqueChoisi()
  const c = S.carte()
  if (!L || !c) return false
  const spec = S.types[c.type]
  const [x, y] = pointCarte(e)
  const touche = calqueSous(spec, c.libres.map((l) => ({ ...l, image: S.imageSync(l.blob) })), x, y)
  if (touche?.id !== L.id) return false
  L.echelle = Math.max(0.02, Math.min(3, L.echelle * (e.deltaY < 0 ? 1.05 : 1 / 1.05)))
  S.changement()
  dessinerSurcouche()
  return true
}

/** Touches : Suppr efface le calque choisi, les fleches le poussent (Maj : plus vite). */
export function touche(e) {
  const L = calqueChoisi()
  const c = S.carte()
  if (!L || !c) return false
  if (/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) || e.target.isContentEditable) return false
  if (e.key === 'Delete' || e.key === 'Backspace') {
    c.libres.splice(c.libres.indexOf(L), 1)
    selectionnee = null
    S.changement()
    S.reconstruire()
    dessinerSurcouche()
    return true
  }
  const d = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] }[e.key]
  if (!d) return false
  const pas = e.shiftKey ? 0.01 : 0.002
  L.fx += d[0] * pas
  L.fy += d[1] * pas
  S.changement()
  dessinerSurcouche()
  return true
}
