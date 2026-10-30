// La sauvegarde sur le serveur du site (comptes « createur »), EN PLUS de celle du navigateur.
//
// - Un projet serveur par DOSSIER (id = `d-<nom>-<empreinte>`), plus un projet `_reglages` (modeles et styles perso).
// - La page detecte l'API au demarrage : 200 = connecte, 401 = pas connecte, autre chose (page ouverte hors du site) = local seulement.
// - Envoi automatique 5 s apres un changement, seulement pour les dossiers modifies.
// - Au demarrage, fusion : par dossier, le plus recent gagne ; ce qui est ecrase est garde dans les versions du navigateur.
//
// Ce qu'on retient dans `projet.sync[id]` (sauvegarde avec le projet dans le navigateur) : `vu` = la date du serveur la derniere fois
// qu'on s'est mis d'accord avec lui, `sale` = des changements pas encore envoyes, `local` = date du dernier changement local.
import { ajouterVersion } from './stockage.js'

const API = '/api/createur/'
const DELAI_ENVOI = 5000
const DELAI_REESSAI = 30000
const REGLAGES = '_reglages'

// ---------------------------------------------------------------- identifiants
function empreinteTexte(texte) {
  let h = 0x811c9dc5
  for (const c of texte) { h ^= c.codePointAt(0); h = Math.imul(h, 0x01000193) >>> 0 }
  return h.toString(16).padStart(8, '0')
}
/** L'id serveur d'un dossier : lettres, chiffres, « - » (<= 64 caracteres), stable, et deux noms differents ne se confondent pas. */
export function idDossier(nom) {
  if (!nom) return 'd-sans-dossier'
  const slug = nom.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40)
  return `d-${slug || 'x'}-${empreinteTexte(nom)}`
}

// ---------------------------------------------------------------- cartes vierges
const TITRES_PAR_DEFAUT = new Set(['Card name', 'Nom de la carte', ''])
/** Une carte jamais touchee (titre par defaut, aucun texte, aucune image) : un navigateur neuf en a une, et elle ne vaut pas d'etre envoyee. */
export function estVierge(c) {
  if (c.dossier) return false // rangee dans un dossier : elle a une intention
  const ct = c.contenu ?? {}
  if (!TITRES_PAR_DEFAUT.has(String(ct.titre ?? '').trim())) return false
  if (['regles', 'citation', 'traits', 'typeTexte'].some((k) => String(ct[k] ?? '').replace(/<[^>]*>/g, '').trim())) return false
  if (c.art?.blob || c.artDevant?.blob || c.tete?.blob || c.verso?.blob || (c.libres?.length ?? 0)) return false
  return true
}

// ---------------------------------------------------------------- empreintes (pour savoir si quelque chose a change)
const idsBlob = new WeakMap()
let compteurBlob = 0
const remplaceur = (k, v) => {
  if (v instanceof Blob) {
    if (!idsBlob.has(v)) idsBlob.set(v, ++compteurBlob)
    return `blob#${idsBlob.get(v)}:${v.size}`
  }
  return v
}
const empreinte = (x) => JSON.stringify(x, remplaceur)

// ---------------------------------------------------------------- appels
async function appeler(chemin, options = {}) {
  const r = await fetch(API + chemin, { credentials: 'same-origin', cache: 'no-store', ...options })
  return r
}
async function erreurDe(r) {
  try { return (await r.json()).erreur || `HTTP ${r.status}` } catch { return `HTTP ${r.status}` }
}

/**
 * `h` : { projet(), serialiser(carte), deserialiser(json), message(texte), sauver(), apres(pullIds) }
 *   - sauver() : demande la sauvegarde du projet dans le navigateur (les marques `sync` y sont)
 *   - apres(ids) : appele quand des cartes ont ete remplacees par celles du serveur (pour rafraichir la page)
 */
export function creerSynchro(h) {
  const synchro = {
    etat: 'local', // 'local' | 'deconnecte' | 'connecte'
    activite: 'repos', // 'repos' | 'attente' | 'envoi' | 'erreur'
    detail: '',
    quota: null,
    onEtat: () => {},
  }
  const base = {} // id -> empreinte au dernier accord (en memoire seulement)
  const trop = new Set() // dossiers refuses (taille, quota) : on ne reessaie qu'apres un nouveau changement
  let minuteur = 0
  let enCours = false
  let relancer = false

  const sync = () => (h.projet().sync ??= {})
  const majEtat = (activite, detail = '') => { synchro.activite = activite; synchro.detail = detail; synchro.onEtat() }

  // ------------------------------------------------ ce que la page contient
  function dossiersLocaux() {
    const m = new Map()
    for (const c of h.projet().cartes) {
      if (estVierge(c)) continue // jamais envoyee (et si elle est modifiee, elle ne l'est plus)
      const nom = c.dossier || ''
      const id = idDossier(nom)
      if (!m.has(id)) m.set(id, { id, nom, cartes: [] })
      m.get(id).cartes.push(c)
    }
    return m
  }
  const empreinteDossier = (d) => empreinte(d.cartes)
  const empreinteReglages = () => empreinte({ m: h.projet().modeles ?? [], s: h.projet().styles ?? [], g: h.projet().gabarits ?? {} })

  /** Repere les dossiers dont le contenu a change depuis le dernier accord : ils sont « sales » (a envoyer). */
  function marquerSales() {
    const s = sync()
    const locaux = dossiersLocaux()
    for (const [id, d] of locaux) {
      const fp = empreinteDossier(d)
      if (base[id] !== fp) {
        s[id] = { ...s[id], sale: true, supprime: false, local: Date.now() }
        base[id] = fp
        trop.delete(id)
      }
    }
    for (const id of Object.keys(s)) if (id !== REGLAGES && !locaux.has(id) && !s[id].supprime) { s[id].supprime = true; s[id].local = Date.now(); delete base[id] }
    const fr = empreinteReglages()
    if (base[REGLAGES] !== fr) {
      s[REGLAGES] = { ...s[REGLAGES], sale: true, local: Date.now() }
      base[REGLAGES] = fr
      trop.delete(REGLAGES)
    }
  }
  const aEnvoyer = () => Object.entries(sync()).filter(([id, e]) => (e.sale || e.supprime) && !trop.has(id))

  // ------------------------------------------------ envoi
  async function serialiserDossier(d) {
    const cartes = []
    for (const c of d.cartes) cartes.push(await h.serialiser(c))
    return { format: 'createur-cartes-dossier', version: 1, nom: d.nom || 'Sans dossier', dossier: d.nom, modifie: Date.now(), cartes }
  }
  async function serialiserReglages() {
    const p = h.projet()
    const modeles = []
    for (const m of p.modeles ?? []) modeles.push({ id: m.id, nom: m.nom, dossier: m.dossier, carte: await h.serialiser(m.carte) })
    return { format: 'createur-cartes-reglages', version: 1, nom: REGLAGES, dossier: '', modifie: Date.now(), modeles, styles: p.styles ?? [], gabarits: p.gabarits ?? {} }
  }

  async function envoyer(id) {
    const s = sync()
    if (s[id]?.supprime) {
      const r = await appeler('projet/' + id, { method: 'DELETE' })
      if (r.ok || r.status === 404) { delete s[id]; delete base[id] } else throw await echec(r, id)
      return
    }
    let doc, fp
    if (id === REGLAGES) { fp = empreinteReglages(); doc = await serialiserReglages() } else {
      const d = dossiersLocaux().get(id)
      if (!d) return // le dossier a disparu entre-temps : marquerSales() le notera
      fp = empreinteDossier(d)
      doc = await serialiserDossier(d)
    }
    const r = await appeler('projet/' + id, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(doc) })
    if (!r.ok) throw await echec(r, id)
    const meta = await r.json()
    const encore = (id === REGLAGES ? empreinteReglages() : (dossiersLocaux().get(id) && empreinteDossier(dossiersLocaux().get(id)))) !== fp
    s[id] = { ...s[id], vu: meta.modifie, sale: encore }
    h.sauver()
  }
  async function echec(r, id) {
    const e = new Error(await erreurDe(r))
    e.statut = r.status
    e.id = id
    return e
  }

  async function envoyerTout() {
    if (synchro.etat !== 'connecte') return
    if (enCours) { relancer = true; return }
    enCours = true
    try {
      marquerSales()
      for (const [id] of aEnvoyer()) {
        majEtat('envoi')
        try {
          await envoyer(id)
        } catch (e) {
          if (e.statut === 401) { synchro.etat = 'deconnecte'; majEtat('repos'); return }
          if (e.statut === 413 || e.statut === 507) {
            trop.add(id)
            h.message(e.statut === 413 ? `Dossier trop volumineux pour le serveur : ${e.message}` : e.message)
            continue
          }
          throw e
        }
      }
      await actualiserQuota()
      majEtat(trop.size ? 'erreur' : 'repos', trop.size ? 'trop' : '')
    } catch (e) {
      majEtat('erreur', e.message)
      clearTimeout(minuteur)
      minuteur = setTimeout(envoyerTout, DELAI_REESSAI)
    } finally {
      enCours = false
      if (relancer) { relancer = false; planifier() }
    }
  }

  /** A appeler JUSTE AVANT de ranger le projet dans le navigateur : note ce qui a change (les marques partent avec le projet). */
  synchro.avantSauvegarde = marquerSales
  /** Le point de depart : l'etat de la page tel qu'elle vient de le charger. A appeler une fois, avant toute modification. */
  synchro.baseline = () => {
    for (const [id, d] of dossiersLocaux()) base[id] = empreinteDossier(d)
    base[REGLAGES] = empreinteReglages()
  }
  /** A appeler APRES avoir range le projet dans le navigateur : envoi sur le serveur dans 5 s. */
  function planifier() {
    if (synchro.etat !== 'connecte') return
    if (!aEnvoyer().length) return
    majEtat('attente')
    if (minuteur) return // une echeance est deja posee : elle emportera aussi ce changement
    minuteur = setTimeout(() => { minuteur = 0; envoyerTout() }, DELAI_ENVOI)
  }
  synchro.planifier = planifier

  async function actualiserQuota() {
    try {
      const r = await appeler('projets')
      if (r.ok) { const j = await r.json(); synchro.quota = { utilise: j.utilise, quota: j.quota } }
    } catch {}
  }

  // ------------------------------------------------ rapatriement
  async function lireDoc(id) {
    const r = await appeler('projet/' + id)
    if (!r.ok) throw await echec(r, id)
    return r.json()
  }
  /** Remplace les cartes d'un dossier de la page par celles du document serveur. */
  async function appliquerDossier(doc) {
    const p = h.projet()
    const nom = doc.dossier ?? ''
    const neuves = []
    for (const j of doc.cartes ?? []) {
      const c = await h.deserialiser(j)
      c.dossier = nom
      neuves.push(c)
    }
    const ids = new Set(neuves.map((c) => c.id))
    p.cartes = p.cartes.filter((c) => (c.dossier || '') !== nom && !ids.has(c.id)).concat(neuves)
    return neuves
  }
  async function appliquerReglages(doc, fusion) {
    const p = h.projet()
    const modeles = []
    for (const m of doc.modeles ?? []) modeles.push({ id: m.id, nom: m.nom, dossier: m.dossier, carte: await h.deserialiser(m.carte) })
    if (!fusion) { p.modeles = modeles; p.styles = doc.styles ?? []; p.gabarits = doc.gabarits ?? p.gabarits ?? {}; return }
    // les deux cotes ont change : on garde tout (par id ; le local passe en premier)
    const idsM = new Set((p.modeles ?? []).map((x) => x.id))
    const idsS = new Set((p.styles ?? []).map((x) => x.id))
    p.modeles = [...(p.modeles ?? []), ...modeles.filter((x) => !idsM.has(x.id))]
    p.styles = [...(p.styles ?? []), ...(doc.styles ?? []).filter((x) => !idsS.has(x.id))]
    // templates des dossiers : par nom de dossier, le local l'emporte
    p.gabarits = { ...(doc.gabarits ?? {}), ...(p.gabarits ?? {}) }
  }

  /** Fusion au demarrage. Rend le nombre de dossiers rapatries. */
  async function fusionner(liste) {
    const s = sync()
    const distants = new Map(liste.map((m) => [m.id, m]))
    const locaux = dossiersLocaux()
    const ids = new Set([...locaux.keys(), ...[...distants.keys()], ...Object.keys(s)])
    ids.delete(REGLAGES)
    const rapatries = []
    let versionGardee = false
    const garder = async () => { if (!versionGardee) { versionGardee = true; await ajouterVersion(h.projet(), 'avant fusion avec le serveur').catch(() => {}) } }

    for (const id of ids) {
      const r = distants.get(id)
      const l = locaux.get(id)
      const e = s[id]
      if (r && l) {
        const change = !e || e.vu !== r.modifie
        if (!change) continue // le serveur n'a pas bouge : s'il y a du neuf chez nous, il part avec les envois
        const saleChezNous = e ? !!e.sale : true
        const gagneLeServeur = !saleChezNous || Date.parse(r.modifie) > (e?.local ?? 0)
        if (gagneLeServeur) {
          if (saleChezNous) await garder()
          const doc = await lireDoc(id)
          // touche depuis le debut de la fusion (pendant le telechargement) : le local gagne, rien n'est ecrase
          if (!saleChezNous && s[id]?.sale) continue
          await appliquerDossier(doc)
          s[id] = { vu: r.modifie, sale: false, local: Date.now() }
          base[id] = empreinteDossier(dossiersLocaux().get(id) ?? { cartes: [] })
          rapatries.push(id)
        } else s[id] = { ...e, sale: true, local: e?.local ?? Date.now() } // le local gagne : il sera envoye (le serveur garde l'ancien en version)
      } else if (r && !l) {
        if (e && e.vu === r.modifie) { // supprime chez nous, inchange sur le serveur
          s[id] = { ...e, supprime: true, local: e.local ?? Date.now() }
        } else {
          const doc = await lireDoc(id)
          await appliquerDossier(doc)
          s[id] = { vu: r.modifie, sale: false, local: Date.now() }
          base[id] = empreinteDossier(dossiersLocaux().get(id) ?? { cartes: [] })
          rapatries.push(id)
        }
      } else if (!r && l) {
        if (e?.vu && !e.sale) { // supprime ou renomme ailleurs, et rien de neuf chez nous : on le retire aussi (garde dans les versions locales)
          await garder()
          const p = h.projet()
          p.cartes = p.cartes.filter((c) => idDossier(c.dossier || '') !== id)
          delete s[id]; delete base[id]
          rapatries.push(id)
        } else s[id] = { ...e, vu: undefined, sale: true, local: e?.local ?? Date.now() } // absent du serveur : on l'envoie
      } else if (e) delete s[id]
    }

    // reglages (modeles, styles)
    const r = distants.get(REGLAGES)
    const e = s[REGLAGES]
    if (r && (!e || e.vu !== r.modifie)) {
      const saleChezNous = e ? !!e.sale : (h.projet().modeles?.length || h.projet().styles?.length)
      if (saleChezNous) await garder()
      await appliquerReglages(await lireDoc(REGLAGES), !!saleChezNous)
      s[REGLAGES] = { vu: r.modifie, sale: !!saleChezNous, local: Date.now() }
      base[REGLAGES] = empreinteReglages()
      if (!saleChezNous) rapatries.push(REGLAGES)
    } else if (!r && (h.projet().modeles?.length || h.projet().styles?.length)) s[REGLAGES] = { ...e, sale: true, local: e?.local ?? Date.now() }
    return rapatries
  }

  // ------------------------------------------------ demarrage
  /** Detecte l'API, puis fusionne. Ne leve jamais : au pire on reste en mode local. */
  synchro.demarrer = async () => {
    let liste
    try {
      const r = await appeler('projets', { signal: AbortSignal.timeout(5000) })
      if (r.status === 401) { synchro.etat = 'deconnecte'; synchro.onEtat(); return }
      if (!r.ok) { synchro.etat = 'local'; synchro.onEtat(); return }
      const j = await r.json()
      if (!Array.isArray(j?.projets)) { synchro.etat = 'local'; synchro.onEtat(); return }
      liste = j.projets
      synchro.quota = { utilise: j.utilise, quota: j.quota }
    } catch {
      synchro.etat = 'local'
      synchro.onEtat()
      return
    }
    synchro.etat = 'connecte'
    majEtat('envoi')
    try {
      const rapatries = await fusionner(liste)
      h.sauver()
      if (rapatries.length) h.apres(rapatries)
      majEtat('repos')
      marquerSales()
      if (aEnvoyer().length) envoyerTout() // l'arriere de la derniere fois part tout de suite
    } catch (e) {
      majEtat('erreur', e.message)
      clearTimeout(minuteur)
      minuteur = setTimeout(envoyerTout, DELAI_REESSAI)
    }
  }

  // ------------------------------------------------ versions du serveur (fenetre « Versions »)
  synchro.versions = async (nomDossier) => {
    const id = idDossier(nomDossier || '')
    const r = await appeler(`projet/${id}/versions`)
    if (r.status === 404) return []
    if (!r.ok) throw await echec(r, id)
    return (await r.json()).versions ?? []
  }
  /** Remplace le dossier par une ancienne version du serveur. Rend les cartes rapatriees. */
  synchro.restaurerVersion = async (nomDossier, numero) => {
    const id = idDossier(nomDossier || '')
    const r = await appeler(`projet/${id}/versions/${numero}`)
    if (!r.ok) throw await echec(r, id)
    const neuves = await appliquerDossier(await r.json())
    marquerSales() // la version restauree devient le courant : elle repart sur le serveur (qui garde l'actuelle comme version)
    h.sauver()
    return neuves
  }
  return synchro
}
