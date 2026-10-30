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
