// Le stockage (IndexedDB) de l'outil « Traduction » : une base A PART de celle du createur de cartes (stockage.js,
// base 'createur-cartes') — cet outil est AUTONOME (pas de projet, pas de carte du catalogue), sa file d'attente de
// scans ne doit jamais se mélanger avec un projet de carte. Même patron que stockage.js : IndexedDB, un magasin
// cle/valeur, un objet par scan (id = cle).
const NOM = 'createur-cartes-traduction'

function ouvrir() {
  return new Promise((ok, ko) => {
    const r = indexedDB.open(NOM, 1)
    r.onupgradeneeded = () => {
      const db = r.result
      if (!db.objectStoreNames.contains('cartes')) db.createObjectStore('cartes', { keyPath: 'id' })
      if (!db.objectStoreNames.contains('kv')) db.createObjectStore('kv')
    }
    r.onsuccess = () => ok(r.result)
    r.onerror = () => ko(r.error)
  })
}
const promesse = (req) => new Promise((ok, ko) => { req.onsuccess = () => ok(req.result); req.onerror = () => ko(req.error) })

/** Toutes les cartes de la file, dans l'ordre enregistre (voir lireOrdre). */
export async function listerCartes() {
  const db = await ouvrir()
  const cartes = (await promesse(db.transaction('cartes').objectStore('cartes').getAll())) ?? []
  const ordre = await lireOrdre()
  if (!ordre.length) return cartes
  const parId = new Map(cartes.map((c) => [c.id, c]))
  const triees = ordre.map((id) => parId.get(id)).filter(Boolean)
  for (const c of cartes) if (!ordre.includes(c.id)) triees.push(c)
  return triees
}
export async function sauvegarderCarte(carte) {
  const db = await ouvrir()
  await promesse(db.transaction('cartes', 'readwrite').objectStore('cartes').put(carte))
}
export async function supprimerCarte(id) {
  const db = await ouvrir()
  await promesse(db.transaction('cartes', 'readwrite').objectStore('cartes').delete(id))
  await sauvegarderOrdre((await lireOrdre()).filter((i) => i !== id))
}
export async function lireOrdre() {
  try {
    const db = await ouvrir()
    return (await promesse(db.transaction('kv').objectStore('kv').get('ordre'))) ?? []
  } catch {
    return []
  }
}
export async function sauvegarderOrdre(ordre) {
  const db = await ouvrir()
  await promesse(db.transaction('kv', 'readwrite').objectStore('kv').put(ordre, 'ordre'))
}
