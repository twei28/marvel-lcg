// Un fichier PSD « à plat » : une seule image (RVB + transparence), sans calques. Les calques du gabarit ne sont pas rejoués ici :
// c'est l'image finale de la carte, ouvrable dans Photoshop, GIMP, Krita, Affinity.
// Format (Adobe, « Photoshop File Format Specification ») : en-tete, mode couleur, ressources, calques (vide), donnees d'image brutes par canal.
export function construirePsd(toile) {
  const { width: l, height: h } = toile
  const px = toile.getContext('2d').getImageData(0, 0, l, h).data
  const taille = l * h
  const sortie = new Uint8Array(26 + 4 + 4 + 4 + 2 + taille * 4)
  const v = new DataView(sortie.buffer)
  let p = 0
  for (const c of '8BPS') sortie[p++] = c.charCodeAt(0)
  v.setUint16(p, 1); p += 2 // version
  p += 6 // reserve
  v.setUint16(p, 4); p += 2 // canaux : R, V, B, alpha
  v.setUint32(p, h); p += 4
  v.setUint32(p, l); p += 4
  v.setUint16(p, 8); p += 2 // 8 bits par canal
  v.setUint16(p, 3); p += 2 // mode RVB
  v.setUint32(p, 0); p += 4 // donnees du mode couleur : aucune
  v.setUint32(p, 0); p += 4 // ressources d'image : aucune
  v.setUint32(p, 0); p += 4 // calques et masques : aucun
  v.setUint16(p, 0); p += 2 // donnees d'image brutes (sans compression)
  for (let c = 0; c < 4; c++) for (let i = 0; i < taille; i++) sortie[p++] = px[i * 4 + c]
  return sortie
}

// ---------------------------------------------------------------- PSD a calques
/** Compression « PackBits » d'une ligne d'octets (la RLE des PSD). */
function packBits(src) {
  const out = []
  let i = 0
  const n = src.length
  while (i < n) {
    let run = 1
    while (i + run < n && run < 128 && src[i + run] === src[i]) run++
    if (run >= 2) { out.push(257 - run, src[i]); i += run; continue }
    let j = i
    while (j < n && j - i < 128 && !(j + 1 < n && src[j] === src[j + 1])) j++
    out.push(j - i - 1)
    for (let k = i; k < j; k++) out.push(src[k])
    i = j
  }
  return Uint8Array.from(out)
}
/** Les 4 canaux (R, V, B, alpha) d'une toile, chacun compresse ligne par ligne : { comptes: Uint16Array(4 * h), donnees: [Uint8Array] }. */
function canauxRle(toile) {
  const { width: l, height: h } = toile
  const px = toile.getContext('2d').getImageData(0, 0, l, h).data
  const comptes = new Uint16Array(4 * h)
  const morceaux = []
  for (let c = 0; c < 4; c++) {
    const plan = new Uint8Array(l * h)
    for (let i = 0; i < l * h; i++) plan[i] = px[i * 4 + c]
    for (let y = 0; y < h; y++) {
      const ligne = packBits(plan.subarray(y * l, (y + 1) * l))
      comptes[c * h + y] = ligne.length
      morceaux.push(ligne)
    }
  }
  return { comptes, morceaux }
}
/**
 * `couches` : [{ nom, toile, visible }] du BAS vers le HAUT, toutes de la taille de la carte. `fusion` : la carte complete (image affichee par les
 * logiciels qui ne lisent pas les calques). Photoshop, GIMP, Krita et Affinity ouvrent les calques tels quels.
 */
export function construirePsdCalques(couches, fusion) {
  const { width: l, height: h } = fusion
  const octets = (n) => new Uint8Array(n)
  const parts = []
  let total = 0
  const poser = (u8) => { parts.push(u8); total += u8.length }
  const u16 = (v) => { const b = octets(2); new DataView(b.buffer).setUint16(0, v & 0xffff); return b }
  const u32 = (v) => { const b = octets(4); new DataView(b.buffer).setUint32(0, v >>> 0); return b }
  const i32 = (v) => { const b = octets(4); new DataView(b.buffer).setInt32(0, v); return b }
  const texte = (s) => Uint8Array.from([...s].map((c) => c.charCodeAt(0)))
  const concat = (liste) => { const n = liste.reduce((a, x) => a + x.length, 0); const s = octets(n); let p = 0; for (const x of liste) { s.set(x, p); p += x.length }; return s }

  // en-tete
  poser(texte('8BPS')); poser(u16(1)); poser(octets(6)); poser(u16(4)); poser(u32(h)); poser(u32(l)); poser(u16(8)); poser(u16(3))
  poser(u32(0)) // mode couleur
  poser(u32(0)) // ressources d'image

  // calques : les enregistrements, puis les pixels de chaque calque
  const donnees = couches.map((c) => canauxRle(c.toile))
  const enregistrements = []
  const pixels = []
  couches.forEach((c, k) => {
    const d = donnees[k]
    const longueurCanal = 2 + 2 * h + d.morceaux.slice(0, 0).length // calcule ci-dessous canal par canal
    const parCanal = [0, 1, 2, 3].map((ch) => {
      let somme = 0
      for (let y = 0; y < h; y++) somme += d.comptes[ch * h + y]
      return 2 + 2 * h + somme
    })
    const nom = texte(c.nom.slice(0, 31).replace(/[^\x20-\x7e]/g, '?'))
    const nomPascal = concat([Uint8Array.of(nom.length), nom])
    const bourrage = octets((4 - (nomPascal.length % 4)) % 4)
    const extra = concat([u32(0), u32(0), nomPascal, bourrage]) // masque (vide), plages de fusion (vide), nom
    enregistrements.push(concat([
      i32(0), i32(0), i32(h), i32(l), u16(4),
      i16c(0, parCanal[0]), i16c(1, parCanal[1]), i16c(2, parCanal[2]), i16c(-1, parCanal[3]),
      texte('8BIM'), texte('norm'), Uint8Array.of(255, 0, c.visible === false ? 2 : 0, 0), u32(extra.length), extra,
    ]))
    void longueurCanal
    for (let ch = 0; ch < 4; ch++) {
      const liste = [u16(1)]
      const cptes = octets(2 * h)
      for (let y = 0; y < h; y++) new DataView(cptes.buffer).setUint16(2 * y, d.comptes[ch * h + y])
      liste.push(cptes)
      for (let y = 0; y < h; y++) liste.push(d.morceaux[ch * h + y])
      pixels.push(concat(liste))
    }
  })
  function i16c(id, longueur) { return concat([u16(id), u32(longueur)]) }
  let infoCalques = concat([u16(couches.length), ...enregistrements, ...pixels])
  if (infoCalques.length % 2) infoCalques = concat([infoCalques, octets(1)])
  poser(u32(4 + infoCalques.length + 4)) // section « calques et masques »
  poser(u32(infoCalques.length))
  poser(infoCalques)
  poser(u32(0)) // masque global : aucun

  // image fusionnee (RLE)
  const f = canauxRle(fusion)
  poser(u16(1))
  const cptes = octets(2 * 4 * h)
  for (let i = 0; i < 4 * h; i++) new DataView(cptes.buffer).setUint16(2 * i, f.comptes[i])
  poser(cptes)
  for (const m of f.morceaux) poser(m)
  return concat(parts)
}
