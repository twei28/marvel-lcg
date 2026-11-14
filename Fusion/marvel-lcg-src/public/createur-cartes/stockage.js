// Le stockage dans le navigateur (IndexedDB) : le projet courant, et les versions gardees automatiquement.
const NOM = 'createur-cartes'
const MAX_VERSIONS = 10

function ouvrir() {
  return new Promise((ok, ko) => {
    const r = indexedDB.open(NOM, 2)
    r.onupgradeneeded = () => {
      const db = r.result
      if (!db.objectStoreNames.contains('kv')) db.createObjectStore('kv')
      if (!db.objectStoreNames.contains('versions')) db.createObjectStore('versions', { autoIncrement: true })
    }
    r.onsuccess = () => ok(r.result)
    r.onerror = () => ko(r.error)
  })
}
const promesse = (req) => new Promise((ok, ko) => { req.onsuccess = () => ok(req.result); req.onerror = () => ko(req.error) })

export async function lireProjet() {
  try {
    const db = await ouvrir()
    return (await promesse(db.transaction('kv').objectStore('kv').get('projet'))) ?? null
  } catch {
    return null
  }
}
export async function ecrireProjet(projet) {
  const db = await ouvrir()
  await promesse(db.transaction('kv', 'readwrite').objectStore('kv').put(projet, 'projet'))
}

/** Garde une version (les plus anciennes au-dela de MAX_VERSIONS disparaissent). */
export async function ajouterVersion(projet, raison = 'auto') {
  const db = await ouvrir()
  const tx = db.transaction('versions', 'readwrite')
  const st = tx.objectStore('versions')
  st.add({ date: Date.now(), raison, nb: projet.cartes.length, projet })
  const cles = await promesse(st.getAllKeys())
  for (const k of cles.slice(0, Math.max(0, cles.length - MAX_VERSIONS))) st.delete(k)
  await new Promise((ok) => { tx.oncomplete = ok })
}
export async function listerVersions() {
  const db = await ouvrir()
  const st = db.transaction('versions').objectStore('versions')
  const [cles, vals] = await Promise.all([promesse(st.getAllKeys()), promesse(st.getAll())])
  return cles.map((k, i) => ({ cle: k, date: vals[i].date, raison: vals[i].raison, nb: vals[i].nb, projet: vals[i].projet })).reverse()
}
