// Un PDF minimal : des pages A4 portant des images JPEG (la planche d'impression : 3 x 3 cartes de 63 x 88 mm).
// Pas de bibliotheque : un PDF est un texte avec des objets numerotes, un index (xref) et une fin.

const MM = 72 / 25.4 // millimetres -> points PDF
const A4 = [210, 297]

/** `pages` : liste de pages, chacune une liste de { jpeg: Uint8Array, px: [largeur, hauteur], mm: [x, y, largeur, hauteur] } (y compte depuis le haut). */
export function construirePdf(pages) {
  const morceaux = []
  const decalages = []
  let taille = 0
  const enc = new TextEncoder()
  const poser = (x) => { const o = typeof x === 'string' ? enc.encode(x) : x; morceaux.push(o); taille += o.length }
  const objet = (n, corps) => { decalages[n] = taille; poser(`${n} 0 obj\n`); for (const c of corps) poser(c); poser('\nendobj\n') }

  // numerotation : 1 catalogue, 2 liste des pages, puis pour chaque page : page, contenu, puis ses images
  let suivant = 3
  const modele = pages.map((cellules) => {
    const page = suivant++
    const contenu = suivant++
    const images = cellules.map(() => suivant++)
    return { page, contenu, images, cellules }
  })
  poser('%PDF-1.4\n%\xE2\xE3\xCF\xD3\n')
  objet(1, ['<< /Type /Catalog /Pages 2 0 R >>'])
  objet(2, [`<< /Type /Pages /Kids [${modele.map((m) => `${m.page} 0 R`).join(' ')}] /Count ${modele.length} >>`])
  const h = A4[1] * MM
  for (const m of modele) {
    const xobjets = m.images.map((n, i) => `/Im${i} ${n} 0 R`).join(' ')
    objet(m.page, [`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${(A4[0] * MM).toFixed(2)} ${h.toFixed(2)}] /Resources << /XObject << ${xobjets} >> >> /Contents ${m.contenu} 0 R >>`])
    const flux = m.cellules.map((c, i) => {
      const [x, y, w, hh] = c.mm
      return `q ${(w * MM).toFixed(3)} 0 0 ${(hh * MM).toFixed(3)} ${(x * MM).toFixed(3)} ${(h - (y + hh) * MM).toFixed(3)} cm /Im${i} Do Q\n`
    }).join('')
    objet(m.contenu, [`<< /Length ${flux.length} >>\nstream\n${flux}endstream`])
    m.cellules.forEach((c, i) => {
      objet(m.images[i], [`<< /Type /XObject /Subtype /Image /Width ${c.px[0]} /Height ${c.px[1]} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${c.jpeg.length} >>\nstream\n`, c.jpeg, '\nendstream'])
    })
  }
  const debutXref = taille
  const n = suivant
  poser(`xref\n0 ${n}\n0000000000 65535 f \n`)
  for (let i = 1; i < n; i++) poser(`${String(decalages[i]).padStart(10, '0')} 00000 n \n`)
  poser(`trailer\n<< /Size ${n} /Root 1 0 R >>\nstartxref\n${debutXref}\n%%EOF\n`)
  const sortie = new Uint8Array(taille)
  let p = 0
  for (const o of morceaux) { sortie.set(o, p); p += o.length }
  return sortie
}

/** Les cellules d'une feuille de 9 cartes, 3 colonnes, centrees avec 10 mm de marge haute comme la planche a l'ecran. */
export function cellulesPlanche(images) {
  const [cw, ch] = [63, 88]
  const x0 = (A4[0] - 3 * cw) / 2
  const y0 = (A4[1] - 3 * ch) / 2
  return images.map((im, i) => (im ? { ...im, mm: [x0 + (i % 3) * cw, y0 + Math.floor(i / 3) * ch, cw, ch] } : null))
}
