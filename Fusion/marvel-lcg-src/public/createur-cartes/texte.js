// Le texte riche d'une carte : un mini-HTML (gras, italique, traits, icones, filets) mis en page sur un canvas.
//
// Balises : <b> gras, <i> italique, <em> style « traits », <u> souligne, <code>e</code> ou [energy] icone, <br> retour a la ligne,
// <hr class="br"/> saut de paragraphe, <hr/> filet horizontal. Une ligne vide = un saut de paragraphe, un retour simple = une ligne.
// <span style="font-size:1.3em; color:#c00"> : taille relative (em ou %) et couleur d'un morceau de texte (ce que fait l'editeur de la page).
import { ICONES } from './polices.js'

const ENTITES = { '&mdash;': '—', '&ndash;': '–', '&amp;': '&', '&nbsp;': ' ', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&rsquo;': '’', '&hellip;': '…' }

/** Analyse la source en une suite de « jetons » : mot, espace, icone, saut (ligne), para (paragraphe), filet. */
export function analyser(source) {
  const jetons = []
  const pile = { b: 0, i: 0, em: 0, u: 0, code: 0 }
  const spans = [{ ech: 1, col: null }] // taille relative et couleur courantes (pile des <span style>)
  let tampon = ''
  const style = () => ({ b: pile.b > 0, i: pile.i > 0, em: pile.em > 0, u: pile.u > 0, ech: spans[spans.length - 1].ech, col: spans[spans.length - 1].col })
  const vider = () => {
    if (!tampon) return
    const t = tampon.replace(/&[a-z]+;/g, (e) => ENTITES[e] ?? e)
    tampon = ''
    if (pile.code > 0) {
      for (const c of t) jetons.push({ t: 'icone', s: c, ...style() })
      return
    }
    for (const morceau of t.split(/(\s+)/)) {
      if (!morceau) continue
      if (/^\s+$/.test(morceau)) {
        const n = (morceau.match(/\n/g) || []).length
        if (n >= 2) jetons.push({ t: 'para' })
        else if (n === 1) jetons.push({ t: 'saut' })
        else jetons.push({ t: 'espace', ...style() })
      } else jetons.push({ t: 'mot', s: morceau, ...style() })
    }
  }
  for (let k = 0; k < source.length; ) {
    const c = source[k]
    if (c === '<') {
      const fin = source.indexOf('>', k)
      if (fin > 0) {
        const balise = source.slice(k + 1, fin).trim().toLowerCase()
        vider()
        const nom = balise.replace(/^\//, '').split(/[\s/]/)[0]
        const ferme = balise.startsWith('/')
        if (nom === 'span') {
          if (ferme) { if (spans.length > 1) spans.pop() } else {
            const cur = spans[spans.length - 1]
            const css = /style\s*=\s*["']([^"']*)["']/i.exec(balise)?.[1] ?? ''
            const tailleCss = /font-size\s*:\s*([\d.]+)\s*(em|%)/i.exec(css)
            const coul = /(?:^|;|\s)color\s*:\s*([^;]+)/i.exec(css)?.[1]?.trim()
            spans.push({ ech: tailleCss ? cur.ech * (tailleCss[2] === '%' ? tailleCss[1] / 100 : Number(tailleCss[1])) : cur.ech, col: coul ?? cur.col })
          }
        } else if (nom in pile) pile[nom] = Math.max(0, pile[nom] + (ferme ? -1 : 1))
        else if (nom === 'br') jetons.push({ t: 'saut' })
        else if (nom === 'hr') jetons.push(/class=["']?br/.test(balise) ? { t: 'para' } : { t: 'filet' })
        k = fin + 1
        continue
      }
    }
    if (c === '[') {
      const fin = source.indexOf(']', k)
      const nom = fin > 0 ? source.slice(k + 1, fin).trim().toLowerCase() : ''
      if (fin > 0 && nom in ICONES) {
        vider()
        jetons.push({ t: 'icone', s: ICONES[nom], ...style() })
        k = fin + 1
        continue
      }
    }
    tampon += c
    k++
  }
  vider()
  return jetons
}

/** La police CSS d'un jeton, a partir de la police de base du champ. */
export function policeDe(base, jeton, facteur = 1) {
  const taille = base.taille * facteur * (jeton.ech ?? 1)
  if (jeton.t === 'icone') return `${taille}px ChampionsIcons`
  if (jeton.em) return `${taille}px ${base.familleTraits ?? 'KomikaTitle'}`
  const gras = jeton.b ? (base.familleGras ?? base.poidsGras ?? 'bold') : base.poids ?? 'normal'
  const italique = jeton.i || base.style === 'italic' ? 'italic' : 'normal'
  return `${italique} ${gras} ${taille}px ${base.famille}`
}

/**
 * Met le texte en page dans une largeur donnee. Rend { lignes, hauteur } ; chaque ligne = { x, largeur, items, filet, y }.
 * `base` : { famille, taille, poids, style, interligne (px), alignement, ecartParagraphe (px) }.
 * `contrainte(y0, y1)` (facultatif) rend { g, d } : ce que les formes voisines (coins coupes) retirent a gauche et a droite
 * d'une ligne qui occupe la hauteur [y0, y1] du bloc ; chaque ligne se coupe donc dans SA largeur disponible.
 */
export function mettreEnPage(ctx, jetons, base, largeur, facteur = 1, contrainte = null) {
  const interligne = (base.interligne ?? base.taille * 1.2) * facteur
  const ecart = (base.ecartParagraphe ?? 0) * facteur
  const lignes = []
  let y = 0
  const dispo = () => {
    const c = contrainte ? contrainte(y, y + interligne) : { g: 0, d: 0 }
    return { g: c.g, largeur: Math.max(40, largeur - c.g - c.d) }
  }
  let d = dispo()
  let courante = { items: [], largeur: 0, apresPara: false, g: d.g, dispo: d.largeur }
  const pousser = (filet = false) => {
    while (courante.items.length && courante.items[courante.items.length - 1].t === 'espace') courante.largeur -= courante.items.pop().w
    courante.y = y
    lignes.push({ ...courante, filet })
    y += filet ? interligne * 0.5 : interligne
    d = dispo()
    courante = { items: [], largeur: 0, apresPara: false, g: d.g, dispo: d.largeur }
  }
  let aDuTexte = false
  for (const j of jetons) {
    if (j.t === 'saut') {
      pousser()
      continue
    }
    if (j.t === 'para') {
      pousser()
      y += ecart
      d = dispo()
      courante = { items: [], largeur: 0, apresPara: true, g: d.g, dispo: d.largeur }
      continue
    }
    if (j.t === 'filet') {
      if (courante.items.length) pousser()
      y += ecart
      pousser(true)
      continue
    }
    ctx.font = policeDe(base, j, facteur)
    ctx.fontVariantCaps = base.capsPetites && j.t !== 'icone' ? 'small-caps' : 'normal'
    const letter = (base.espacement ?? 0) * facteur
    ctx.letterSpacing = letter ? letter + 'px' : '0px'
    const largeurJeton = ctx.measureText(j.t === 'espace' ? ' ' : j.s).width
    if (j.t === 'espace' && !courante.items.length) continue
    if (courante.items.length && j.t !== 'espace' && courante.largeur + largeurJeton > courante.dispo) pousser()
    courante.items.push({ ...j, w: largeurJeton })
    courante.largeur += largeurJeton
    aDuTexte = true
  }
  if (courante.items.length || !lignes.length) pousser()
  ctx.letterSpacing = '0px'
  ctx.fontVariantCaps = 'normal'
  return { lignes, hauteur: y, aDuTexte, interligne }
}

/** Reduit le texte (par pas de 3 %) jusqu'a ce qu'il tienne dans `hauteurMax`. Rend le facteur retenu et la mise en page. */
export function ajuster(ctx, jetons, base, largeur, hauteurMax, minimum = 0.55, contrainte = null) {
  let facteur = 1
  let page = mettreEnPage(ctx, jetons, base, largeur, facteur, contrainte)
  while (page.hauteur > hauteurMax && facteur > minimum) {
    facteur = Math.max(minimum, facteur * 0.97)
    page = mettreEnPage(ctx, jetons, base, largeur, facteur, contrainte)
  }
  return { facteur, page }
}

/**
 * Dessine une mise en page dont le coin haut-gauche est (0, 0) du repere courant.
 * `alignement` : left | center | right, sur la largeur donnee.
 */
export function dessinerPage(ctx, page, base, largeur, facteur = 1, couleur = '#000', alignement = 'left') {
  ctx.textBaseline = 'alphabetic'
  ctx.fillStyle = couleur
  for (const l of page.lignes) {
    if (l.filet) {
      ctx.save()
      ctx.fillStyle = couleur
      ctx.fillRect(0, l.y + page.interligne * 0.22, largeur, Math.max(2, 3 * facteur))
      ctx.restore()
      continue
    }
    const zone = l.dispo ?? largeur
    let x = (l.g ?? 0) + (alignement === 'center' ? (zone - l.largeur) / 2 : alignement === 'right' ? zone - l.largeur : 0)
    const lettre = (base.espacement ?? 0) * facteur
    ctx.letterSpacing = lettre ? lettre + 'px' : '0px'
    // une seule ligne de base par ligne : le plus grand morceau la fixe, les autres s'y alignent
    let baseline = 0
    for (const it of l.items) {
      if (it.t === 'espace') continue
      ctx.font = policeDe(base, it, facteur)
      const m = ctx.measureText(it.s)
      baseline = Math.max(baseline, l.y + (page.interligne - (m.fontBoundingBoxAscent + m.fontBoundingBoxDescent)) / 2 + m.fontBoundingBoxAscent)
    }
    for (const it of l.items) {
      if (it.t !== 'espace') {
        ctx.font = policeDe(base, it, facteur)
        ctx.fontVariantCaps = base.capsPetites && it.t !== 'icone' ? 'small-caps' : 'normal'
        ctx.fillStyle = it.col ?? couleur
        ctx.fillText(it.s, x, baseline)
        if (it.u) ctx.fillRect(x, baseline + 4 * facteur * (it.ech ?? 1), it.w, Math.max(2, 3 * facteur * (it.ech ?? 1)))
      }
      x += it.w
    }
  }
  ctx.letterSpacing = '0px'
  ctx.fontVariantCaps = 'normal'
}
