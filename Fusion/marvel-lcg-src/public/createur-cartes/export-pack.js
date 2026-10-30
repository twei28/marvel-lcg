// L'export d'un pack (un dossier, ou toutes les cartes) en un seul .zip : images (une ou deux langues), dos, planche-contact, fichier de
// projet, et un « kit pour le jeu » (les cartes au format de data/cards_custom.json, avec leurs images).
import { dialogue, el, S } from './commun.js'
import { creerZip } from './zip.js'
import { genererDragncards, genererOctgn, genererCardtable, LISEZ_MOI_CARDTABLE, LISEZ_MOI_DRAGNCARDS, LISEZ_MOI_OCTGN } from './export-tables.js'

const aBlob = (toile, type = 'image/png', q = 0.95) => new Promise((ok) => toile.toBlob(ok, type, q))
const octets = async (blob) => new Uint8Array(await blob.arrayBuffer())
const slug = (t) => String(t || 'carte').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^\w]+/g, '_').replace(/^_|_$/g, '').slice(0, 48) || 'carte'

// ---------------------------------------------------------------- kit pour le jeu
const TYPE_JEU = {
  ally: 'Ally', event: 'Event', upgrade: 'Upgrade', support: 'Support', resource: 'Resource', 'alter-ego': 'AlterEgo', identity: 'Hero', obligation: 'Obligation',
  playersidescheme: 'PlayerSideScheme', villain: 'Villain', minion: 'Minion', treachery: 'Treachery', environment: 'Environment', attachment: 'Attachment',
  sidescheme: 'SideScheme', main_scheme_a: 'MainScheme', main_scheme_b: 'MainScheme', 'obligation-villain': 'Obligation',
  'generic-promo': 'Ally', 'generic-promo-vert': 'Ally', 'alter-ego-promo': 'AlterEgo', 'identity-promo': 'Hero',
}
const avecEtoile = (v, etoile) => (v === '' || v == null ? '' : String(v) + (etoile ? '*' : ''))

/** Le texte de regles de la carte -> celui du jeu (gras, italique, icones gardes ; styles de taille / couleur retires). */
export function texteJeu(html) {
  return String(html ?? '')
    .replace(/<\/?span\b[^>]*>/gi, '')
    .replace(/<\/?em>/gi, '')
    .replace(/<hr[^>]*\/?>/gi, '\n')
    .replace(/&mdash;/g, '—')
    .trim()
}

/** Une carte -> une entree de cards_custom.json (a completer : numero, ressources, script). */
export function carteVersJeu(c, id, nomDossier) {
  const ct = c.contenu
  const type = TYPE_JEU[c.type]
  const desc = {}
  const spec = S.types[c.type]
  const a = (cls) => spec.elements.some((e) => e.cls === cls) // la carte montre-t-elle ce nombre ? (les autres champs gardent des valeurs par defaut sans effet)
  const poser = (cls, cle, v, etoile = false) => { if (!a(cls)) return; const x = avecEtoile(v, etoile); if (x !== '') desc[cle] = x }
  poser('paycost cost', 'Cost', ct.cout, ct.coutEtoile)
  poser('thw sch cost', ['villain', 'minion'].includes(c.type) ? 'SCH' : 'THW', ct.thw, ct.thwEtoile)
  poser('atk cost', 'ATK', ct.atk, ct.atkEtoile)
  poser('def cost', 'DEF', ct.def, ct.defEtoile)
  poser('rec cost', 'REC', ct.rec, ct.recEtoile)
  poser('hp cost', 'HP', ct.pv, ct.pvEtoile)
  poser('handsize', 'HS', ct.tailleMain)
  poser('startingthreatwrap', 'StartingThreat', ct.menaceDepart, ct.menaceDepartEtoile)
  poser('targetthreat cost', 'TargetThreat', ct.menaceCible)
  poser('acceleration', 'EscalationThreat', ct.acceleration)
  poser('villainstagenew', 'Stage', ct.etape)
  poser('mainschemephase cost', 'Stage', ct.phaseNumero)
  if (ct.renforts && spec.renforts) desc.Boost = String(ct.renforts)
  const traits = (ct.traits || '').split('.').map((t) => t.trim().toUpperCase()).filter(Boolean)
  return {
    card_id: id, type, name: (ct.unique ? '* ' : '') + (ct.titre || ''), subtitle: '', desc, traits, set_name: nomDossier || '', text: texteJeu(ct.regles),
    // ce que le createur sait mais que le format ne porte pas tel quel : a verifier a la main avant integration
    _a_verifier: {
      ressources: (ct.ressources || []).filter(Boolean), citation: ct.citation || '', faceB: c.type === 'main_scheme_b' || c.type === 'alter-ego' || undefined,
      dossier: nomDossier || '',
    },
  }
}

const LISEZ_MOI = `Kit pour le jeu — fabrique par le Createur de cartes
====================================================

Contenu
  cards_custom.json   les cartes au format de data/cards_custom.json (type, nom, valeurs, traits, texte)
  images/             une image par carte (<card_id>.png), dans la langue choisie
  projet.json         le projet complet (rouvrable dans le Createur)

Ce que ce kit N'EST PAS : une carte jouable. Une carte du jeu a besoin d'un script (ses capacites) ; il se fait carte par carte
avec docs/reference/PROCESSUS-CARTE.md (puis PROCESSUS-HEROS.md pour un heros complet).

A verifier a la main avant d'integrer
  - card_id : les numeros sont des identifiants de travail (custom_<nom>), a remplacer par les vrais.
  - desc.RES (symboles de ressources) n'est pas rempli : voir "_a_verifier.ressources" de chaque carte.
  - les cartes a deux faces (heros / alter-ego, manigance A / B) : a relier avec le meme set_name et les suffixes a / b.
  - le champ _a_verifier est un memo : le retirer avant d'ajouter la carte a cards_custom.json.
`

// ---------------------------------------------------------------- planche-contact
async function planche(toiles, colonnes = 5, largeur = 360) {
  const hauteur = Math.round(largeur * 1.4333)
  const lignes = Math.ceil(toiles.length / colonnes)
  const o = document.createElement('canvas')
  o.width = colonnes * largeur
  o.height = lignes * hauteur
  const x = o.getContext('2d')
  x.fillStyle = '#222'
  x.fillRect(0, 0, o.width, o.height)
  x.imageSmoothingQuality = 'high'
  toiles.forEach((t, i) => {
    const portrait = t.width <= t.height
    const k = Math.min(largeur / (portrait ? t.width : t.height), hauteur / (portrait ? t.height : t.width))
    x.save()
    x.translate((i % colonnes) * largeur + largeur / 2, Math.floor(i / colonnes) * hauteur + hauteur / 2)
    if (!portrait) x.rotate(Math.PI / 2)
    x.drawImage(t, (-t.width * k) / 2, (-t.height * k) / 2, t.width * k, t.height * k)
    x.restore()
  })
  return o
}

/** Ouvre la fenetre d'export d'un pack. `api` : { cartes, carte, rendre(c, langue), rendreVerso(c, langue), serialiser(c), nomDossier }. */
export function ouvrirExportPack(api) {
  const c0 = api.carte()
  const portee = el('select', {}, el('option', { value: 'dossier' }, 'Le dossier de la carte choisie'), el('option', { value: 'tout' }, 'Toutes les cartes'))
  portee.value = c0?.dossier ? 'dossier' : 'tout'
  const format = el('select', {}, ['png', 'jpeg', 'webp'].map((v) => el('option', { value: v }, v.toUpperCase())))
  const casesLangue = [['carte', 'Dans la langue de chaque carte'], ['les-deux', 'Dans les deux langues (EN et FR)']]
  const langue = el('select', {}, casesLangue.map(([v, n]) => el('option', { value: v }, n)))
  const opt = (n, coche = false) => ({ i: el('input', { type: 'checkbox', checked: coche }), n })
  const dos = opt('Les dos (quand une carte en a un)', true)
  const contact = opt('Une planche-contact de toutes les cartes', true)
  const projet = opt('Le fichier de projet (.json)', true)
  const kit = opt('Un kit pour le jeu (cartes au format du jeu + images)')
  const octgn = opt('Un set pour OCTGN (GameDatabase + ImageDataBase)')
  const dragn = opt('Des cartes pour DragnCards (.tsv + images)')
  const cardtable = opt('Un fichier CSV pour CardTable (images dedans)')
  const adresse = el('input', { type: 'text', placeholder: 'https://mon-site.example/images/' })
  const bilan = el('div', { class: 'aide', 'aria-live': 'polite' })
  const visees = () => (portee.value === 'tout' ? api.cartes() : api.cartes().filter((c) => (c.dossier || '') === (c0?.dossier || '')))
  const maj = () => { bilan.textContent = `${visees().length} carte(s).` }
  portee.addEventListener('change', maj)
  maj()
  dialogue('Exporter un pack (.zip)', el('div', { class: 'contenu', style: 'display:flex;flex-direction:column;gap:8px' },
    el('label', {}, 'Cartes', portee), el('label', {}, 'Format des images', format), el('label', {}, 'Langues', langue),
    ...[dos, contact, projet, kit, octgn, dragn, cardtable].map((o) => el('label', { class: 'ligne' }, o.i, o.n)),
    el('label', {}, 'DragnCards : adresse où seront hébergées les images (facultatif, finie par « / »)', adresse), bilan),
  [{ texte: 'Annuler' }, {
    texte: 'Exporter', principal: true, action: async () => {
      const cartes = visees()
      if (!cartes.length) return false
      S.message(`Export de ${cartes.length} carte(s)…`)
      const ext = format.value === 'jpeg' ? 'jpg' : format.value
      const mime = 'image/' + format.value
      const fichiers = []
      const toilesContact = []
      const pris = new Set()
      const nomUnique = (base) => { let n = base; let k = 2; while (pris.has(n)) n = `${base}_${k++}`; pris.add(n); return n }
      for (const c of cartes) {
        const base = nomUnique(slug(c.contenu.titre))
        const langues = langue.value === 'les-deux' ? ['en', 'fr'] : [c.langue]
        for (const l of langues) {
          const t = await api.rendre(c, l)
          if (l === c.langue || langue.value !== 'les-deux') toilesContact.push(t)
          const suffixe = langue.value === 'les-deux' ? '_' + l : ''
          fichiers.push({ nom: `cartes/${base}${suffixe}.${ext}`, octets: await octets(await aBlob(t, mime)) })
          if (dos.i.checked) {
            const d = await api.rendreVerso(c, l)
            if (d) fichiers.push({ nom: `cartes/${base}${suffixe}_back.${ext}`, octets: await octets(await aBlob(d, mime)) })
          }
        }
      }
      // les pochettes du pack (30/10/2026) : en PNG, dans « pochettes/ »
      if (api.pochettes) for (const f of await api.pochettes(c0?.dossier || '', portee.value)) fichiers.push(f)
      if (contact.i.checked) fichiers.push({ nom: 'planche-contact.jpg', octets: await octets(await aBlob(await planche(toilesContact), 'image/jpeg', 0.9)) })
      if (projet.i.checked) {
        const j = { format: 'createur-cartes', version: 2, cartes: [] }
        for (const c of cartes) j.cartes.push(await api.serialiser(c))
        fichiers.push({ nom: 'projet.json', octets: new TextEncoder().encode(JSON.stringify(j)) })
      }
      if (kit.i.checked) {
        const jeu = []
        pris.clear()
        for (const c of cartes) {
          if (!TYPE_JEU[c.type]) continue
          const id = 'custom_' + nomUnique(slug(c.contenu.titre)).toLowerCase() + (c.type === 'main_scheme_b' || c.type === 'alter-ego' ? 'b' : c.type === 'main_scheme_a' || c.type === 'identity' ? 'a' : '')
          jeu.push(carteVersJeu(c, id, c.dossier))
          fichiers.push({ nom: `kit-jeu/images/${id}.png`, octets: await octets(await aBlob(await api.rendre(c, c.langue))) })
        }
        fichiers.push({ nom: 'kit-jeu/cards_custom.json', octets: new TextEncoder().encode(JSON.stringify({ '': jeu }, null, 1)) })
        fichiers.push({ nom: 'kit-jeu/LISEZ-MOI.txt', octets: new TextEncoder().encode(LISEZ_MOI) })
      }
      const nomSet = c0?.dossier || 'Cartes'
      if (octgn.i.checked) {
        for (const f of await genererOctgn(cartes, { nomSet, rendre: api.rendre })) fichiers.push({ nom: 'octgn/' + f.nom, octets: f.octets })
        fichiers.push({ nom: 'octgn/LISEZ-MOI.txt', octets: new TextEncoder().encode(LISEZ_MOI_OCTGN) })
      }
      if (dragn.i.checked) {
        for (const f of await genererDragncards(cartes, { nomSet, rendre: api.rendre, prefixe: adresse.value.trim() })) fichiers.push({ nom: 'dragncards/' + f.nom, octets: f.octets })
        fichiers.push({ nom: 'dragncards/LISEZ-MOI.txt', octets: new TextEncoder().encode(LISEZ_MOI_DRAGNCARDS) })
      }
      if (cardtable.i.checked) {
        const url = async (n) => { const b = await (await fetch(new URL(`img/general/${n}.webp`, import.meta.url))).blob(); return new Promise((ok) => { const r = new FileReader(); r.onload = () => ok(r.result); r.readAsDataURL(b) }) }
        const dos = { joueur: await url('dos-joueur'), rencontre: await url('dos-rencontre') }
        for (const f of await genererCardtable(cartes, { nomSet, rendre: api.rendre, dos })) fichiers.push({ nom: 'cardtable/' + f.nom, octets: f.octets })
        fichiers.push({ nom: 'cardtable/LISEZ-MOI.txt', octets: new TextEncoder().encode(LISEZ_MOI_CARDTABLE) })
      }
      const zip = creerZip(fichiers)
      const a = el('a', { href: URL.createObjectURL(zip), download: slug(c0?.dossier || 'cartes') + '.zip' })
      document.body.append(a)
      a.click()
      setTimeout(() => { URL.revokeObjectURL(a.href); a.remove() }, 1500)
      S.message(`Pack exporté : ${cartes.length} carte(s), ${fichiers.length} fichier(s).`)
    },
  }])
}
