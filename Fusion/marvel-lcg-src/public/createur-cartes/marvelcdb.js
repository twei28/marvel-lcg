// Importer des cartes depuis MarvelCDB (marvelcdb.com) : le TEXTE et les chiffres seulement, jamais les images (elles appartiennent a leurs auteurs).
// L'API publique de MarvelCDB repond avec « Access-Control-Allow-Origin: * » : le navigateur peut l'appeler directement.
const API = 'https://marvelcdb.com/api/public/'

/** Les codes de carte (« 01004 », « 01001a ») ou adresses (marvelcdb.com/card/01004) dans un texte ; un code de paquet (« core ») vaut tout le paquet. */
export function codesDepuisTexte(texte) {
  const cartes = []
  const paquets = []
  for (const m of String(texte).split(/[\s,;]+/).filter(Boolean)) {
    const u = /marvelcdb\.com\/(?:[a-z]{2}\/)?card\/([0-9]{5}[a-z]?)/i.exec(m)
    const code = u ? u[1] : /^[0-9]{5}[a-z]?$/i.test(m) ? m : null
    if (code) cartes.push(code.toLowerCase())
    else if (/^[a-z][a-z0-9_]{1,30}$/i.test(m)) paquets.push(m.toLowerCase())
  }
  return { cartes, paquets }
}

async function json(url) {
  const r = await fetch(url)
  if (!r.ok) throw new Error(`MarvelCDB a répondu ${r.status} pour ${url.replace(API, '')}`)
  return r.json()
}

/** Va chercher les cartes (JSON brut de MarvelCDB), dans l'ordre demandé. */
export async function chargerCartesMarvelCDB({ cartes, paquets }) {
  const sortie = []
  for (const code of cartes) sortie.push(await json(`${API}card/${code}`))
  for (const p of paquets) sortie.push(...(await json(`${API}cards/${p}`)))
  return sortie
}

const TYPES = {
  hero: 'identity', alter_ego: 'alter-ego', ally: 'ally', event: 'event', resource: 'resource', support: 'support', upgrade: 'upgrade',
  minion: 'minion', treachery: 'treachery', villain: 'villain', environment: 'environment', attachment: 'attachment',
  side_scheme: 'sidescheme', main_scheme: 'main_scheme_a', player_side_scheme: 'playersidescheme',
}

/** Le texte de MarvelCDB (<b>, <i>, [energy]…) est deja celui de notre mise en page : on le garde, sauf les balises inconnues. */
const nettoyer = (t) => String(t ?? '').replace(/<\/?(?:p|div|span)[^>]*>/gi, '').replace(/\\n|\r/g, '').replace(/\n/g, '\n').trim()

/**
 * Le JSON d'une carte MarvelCDB -> { type, contenu } (les champs de contenu de notre modele). Retourne null pour un type qu'on ne sait pas faire.
 */
export function champsDepuisMarvelCDB(j) {
  let type = TYPES[j.type_code]
  if (j.type_code === 'obligation') type = j.faction_code === 'encounter' || j.set_code ? 'obligation-villain' : 'obligation'
  if (!type) return null
  const n = (v) => (v == null ? '' : String(v))
  const ct = {
    titre: j.name ?? '', unique: !!j.is_unique, traits: String(j.traits ?? '').replace(/\.\s*$/, ''), regles: nettoyer(j.text), citation: nettoyer(j.flavor),
    ligneEnsemble: j.card_set_name ?? '', createur: '',
  }
  const champ = (cle, v, etoile) => { if (v != null && v !== '') ct[cle] = n(v); if (etoile) ct[cle + 'Etoile'] = true }
  champ('cout', j.cost, j.cost_star)
  champ('atk', j.attack, j.attack_star)
  champ('thw', j.thwart ?? j.scheme, j.thwart_star ?? j.scheme_star)
  champ('def', j.defense, j.defense_star)
  champ('rec', j.recover, j.recover_star)
  champ('pv', j.health, j.health_star)
  if (j.hand_size != null) ct.tailleMain = n(j.hand_size)
  if (j.base_threat != null) { ct.menaceDepart = n(j.base_threat); ct.menaceDepartEtoile = !!j.base_threat_star; ct.menaceDepartParJoueur = !!j.base_threat_per_group }
  if (j.target_threat != null) { ct.menaceCible = n(j.target_threat); ct.menaceCibleParJoueur = !!j.target_threat_per_group }
  if (j.escalation_threat != null) { ct.acceleration = n(j.escalation_threat); ct.accelerationParJoueur = !!j.escalation_threat_per_group }
  if (j.boost != null) { ct.renforts = Number(j.boost) || 0; ct.renfortEtoile = !!j.boost_star }
  if (j.stage != null && type === 'villain') ct.etape = n(j.stage)
  if (type.startsWith('main_scheme')) {
    const m = /^(\d+)([a-z]?)$/i.exec(String(j.stage ?? j.code ?? '').replace(/^.*?(\d+[a-z]?)$/i, '$1'))
    if (j.stage != null) ct.phaseNumero = n(j.stage)
    ct.phaseLettre = (m?.[2] || 'A').toUpperCase()
  }
  const res = []
  for (const k of ['energy', 'mental', 'physical', 'wild']) for (let i = 0; i < (j['resource_' + k] ?? 0); i++) res.push(k)
  if (res.length) ct.ressources = [res[0] ?? '', res[1] ?? '', res[2] ?? '']
  return { type, contenu: ct, code: j.code }
}
