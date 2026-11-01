// Un ecrivain de .zip minimal (sans compression : les images sont deja compressees). Rend un Blob.
let TABLE = null
function crc32(octets) {
  if (!TABLE) {
    TABLE = new Uint32Array(256)
    for (let n = 0; n < 256; n++) {
      let c = n
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1
      TABLE[n] = c >>> 0
    }
  }
  let c = 0xffffffff
  for (let i = 0; i < octets.length; i++) c = TABLE[(c ^ octets[i]) & 0xff] ^ (c >>> 8)
  return (c ^ 0xffffffff) >>> 0
}

/** `fichiers` : [{ nom, octets: Uint8Array }]. Les noms sont en UTF-8 (drapeau 0x0800). */
export function creerZip(fichiers) {
  const enc = new TextEncoder()
  const morceaux = []
  const centrale = []
  let decalage = 0
  const maintenant = new Date()
  const heure = (maintenant.getHours() << 11) | (maintenant.getMinutes() << 5) | (maintenant.getSeconds() >> 1)
  const jour = ((maintenant.getFullYear() - 1980) << 9) | ((maintenant.getMonth() + 1) << 5) | maintenant.getDate()
  for (const f of fichiers) {
    const nom = enc.encode(f.nom)
    const crc = crc32(f.octets)
    const local = new DataView(new ArrayBuffer(30))
    local.setUint32(0, 0x04034b50, true)
    local.setUint16(4, 20, true)
    local.setUint16(6, 0x0800, true)
    local.setUint16(8, 0, true)
    local.setUint16(10, heure, true)
    local.setUint16(12, jour, true)
    local.setUint32(14, crc, true)
    local.setUint32(18, f.octets.length, true)
    local.setUint32(22, f.octets.length, true)
    local.setUint16(26, nom.length, true)
    morceaux.push(new Uint8Array(local.buffer), nom, f.octets)
    const c = new DataView(new ArrayBuffer(46))
    c.setUint32(0, 0x02014b50, true)
    c.setUint16(4, 20, true)
    c.setUint16(6, 20, true)
    c.setUint16(8, 0x0800, true)
    c.setUint16(12, heure, true)
    c.setUint16(14, jour, true)
    c.setUint32(16, crc, true)
    c.setUint32(20, f.octets.length, true)
    c.setUint32(24, f.octets.length, true)
    c.setUint16(28, nom.length, true)
    c.setUint32(42, decalage, true)
    centrale.push(new Uint8Array(c.buffer), nom)
    decalage += 30 + nom.length + f.octets.length
  }
  const tailleCentrale = centrale.reduce((a, m) => a + m.length, 0)
  const fin = new DataView(new ArrayBuffer(22))
  fin.setUint32(0, 0x06054b50, true)
  fin.setUint16(8, fichiers.length, true)
  fin.setUint16(10, fichiers.length, true)
  fin.setUint32(12, tailleCentrale, true)
  fin.setUint32(16, decalage, true)
  return new Blob([...morceaux, ...centrale, new Uint8Array(fin.buffer)], { type: 'application/zip' })
}
