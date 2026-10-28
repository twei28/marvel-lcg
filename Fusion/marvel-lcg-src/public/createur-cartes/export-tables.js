// Les exports pour les tables de jeu en ligne : un set OCTGN (GameDatabase + ImageDataBase) et des cartes pour DragnCards (.tsv + images).
//
// SOURCES (pas de devinette) :
//  - OCTGN : la structure et les proprietes viennent d'un VRAI set de la communaute (« She-Hulk - Why Not », par Merlin, dans le dossier
//    She-Hulk Release EN) : set.xml (<set> / <card> / <alternate>, proprietes CardNumber, Position, Quantity, Type, Owner, HP, HandSize,
//    BaseThreat, BaseThreatFixed, DefaultSetupPile), images <id>.jpg et <id>.b.jpg sous ImageDataBase. Recoupe avec le code source de MCdeck
//    (github.com/lcgtools/MCdeck, mcdeck/octgn.py : generateur ET lecteur de sets OCTGN pour Marvel Champions) : liste exacte des Type
//    (ally, alter_ego, attachment, environment, event, hero, main_scheme, minion, obligation, resource, side_scheme, support, treachery,
//    upgrade, villain), des proprietes (Unique, Cost, Attack, Thwart, Defense, Recovery, Scheme, AttackCost, ThwartCost, HandSize, HP,
//    Boost, Threat, BaseThreat(+Fixed), EscalationThreat(+Fixed), Resource_*), de `size` (SchemeCard pour manigances, EncounterCard pour
//    attachment / environment / minion / obligation / treachery, VillainCard pour villain, rien pour les cartes joueur), et de la regle
//    « Text » et « Quote » = texte de l'element (pas un attribut value). OCTGN n'a pas de Type « player_side_scheme » : side_scheme.
//    Le suffixe Owner `_nemesis` (nemesis d'un heros) n'est PAS pose : on ne sait pas quelles cartes en sont.
//  - DragnCards : wiki officiel (TSV Documentation, Custom Content) : fichier .tsv separe par des tabulations, colonnes obligatoires
//    databaseId, name, imageUrl (.jpg / .png, URL complete), cardBack, type ; une carte a plusieurs faces = plusieurs lignes de meme
//    databaseId avec cardBack = multi_sided. Les valeurs de type / cardBack doivent exister dans le plugin : A VERIFIER avec le modele
//    « Download Example Template » de la salle (Builder -> Custom Content).
import { S } from './commun.js'

const JEU_OCTGN = '055c536f-adba-4bc2-acbf-9aefb9756046' // Marvel Champions dans OCTGN (id du jeu relevé dans le set d'exemple)

/** La carte montre-t-elle ce nombre ? (les autres champs gardent des valeurs par defaut sans effet : on ne les exporte pas) */
const IDENTITES = new Set(['identity', 'identity-promo', 'alter-ego', 'alter-ego-promo']) // leur taille de main et leurs PV sont dans la ligne « Hand size / Hit points »
const montre = (c, cls) => !!S.types[c.type]?.elements?.some((e) => e.cls === cls) || (IDENTITES.has(c.type) && ['handsize', 'hp cost'].includes(cls))
const slug = (t) => String(t || 'cartes').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^\w]+/g, '_').replace(/^_|_$/g, '').toLowerCase().slice(0, 40) || 'cartes'
const echapper = (t) => String(t ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
const texteBrut = (html) => String(html ?? '').replace(/<hr[^>]*>/gi, '\n').replace(/<[^>]*>/g, '').replace(/&mdash;/g, '—').replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#0?39;/g, "'").replace(/&amp;/g, '&').replace(/[ \t]+/g, ' ').trim()

function hachage(texte, graine) {
  let h = (0x811c9dc5 ^ graine) >>> 0
  for (const c of texte) { h ^= c.codePointAt(0); h = Math.imul(h, 0x01000193) >>> 0 }
  return h.toString(16).padStart(8, '0')
}
/** Un identifiant au format GUID, stable pour un nom donne (le meme set garde le meme id d'une exportation a l'autre). */
export function guidStable(nom) {
  const h = [1, 2, 3, 4].map((g) => hachage(nom, g * 7919)).join('')
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-4${h.slice(13, 16)}-a${h.slice(17, 20)}-${h.slice(20, 32)}`
}

// type du createur -> type de la table
const TYPE_TABLE = {
  identity: 'hero', 'identity-promo': 'hero', 'alter-ego': 'alter_ego', 'alter-ego-promo': 'alter_ego', ally: 'ally', 'generic-promo': 'ally', 'generic-promo-vert': 'ally',
  event: 'event', upgrade: 'upgrade', support: 'support', resource: 'resource', obligation: 'obligation', playersidescheme: 'side_scheme',
  villain: 'villain', minion: 'minion', treachery: 'treachery', environment: 'environment', attachment: 'attachment', sidescheme: 'side_scheme',
  main_scheme_a: 'main_scheme', main_scheme_b: 'main_scheme', 'obligation-villain': 'obligation', 'starter-deck': 'resource',
}

/** Regroupe les cartes en « entrees » : heros + alter-ego, manigance A + B, ou une carte seule. Rend [{ faces: [carte, carte?] }]. */
export function regrouper(cartes) {
  const seconde = new Map() // face A -> face B
  for (const [premier, second] of [['identity', 'alter-ego'], ['main_scheme_a', 'main_scheme_b']]) {
    const libres = cartes.filter((c) => c.type === second)
    for (const c of cartes.filter((x) => x.type === premier)) { const b = libres.shift(); if (b) seconde.set(c, b) }
  }
  const rangees = new Set(seconde.values())
  const sorties = []
  for (const c of cartes) {
    if (rangees.has(c)) continue
    sorties.push({ faces: seconde.has(c) ? [c, seconde.get(c)] : [c] })
  }
  return sorties
}

/** Une image reduite a `hauteur` pixels (la plus grande dimension si la carte est paysage), en JPEG. */
async function jpeg(toile, hauteur, qualite = 0.9) {
  const k = Math.min(1, hauteur / Math.max(toile.width, toile.height))
  const o = document.createElement('canvas')
  o.width = Math.round(toile.width * k)
  o.height = Math.round(toile.height * k)
  const x = o.getContext('2d')
  x.fillStyle = '#ffffff'
  x.fillRect(0, 0, o.width, o.height)
  x.imageSmoothingQuality = 'high'
  x.drawImage(toile, 0, 0, o.width, o.height)
  const blob = await new Promise((ok) => o.toBlob(ok, 'image/jpeg', qualite))
  return new Uint8Array(await blob.arrayBuffer())
}

// ---------------------------------------------------------------- OCTGN
/** Les fichiers d'un set OCTGN : [{ nom, octets }] (a ranger dans le dossier de donnees d'OCTGN). `rendre(carte, langue)` -> canvas. */
export async function genererOctgn(cartes, { nomSet, rendre }) {
  const idSet = guidStable('octgn:' + nomSet)
  const racineId = idSet.slice(0, 29) // « …-4adb7 » : on y colle 3 + le numero de carte, comme dans les sets de la communaute
  const idCarte = (numero) => racineId + '3' + String(numero).padStart(6, '0')
  const proprietaire = 'fm_' + slug(nomSet)
  const entrees = regrouper(cartes)
  const fichiers = []
  const base = `GameDatabase/${JEU_OCTGN}/Sets/${idSet}`
  const images = `ImageDataBase/${JEU_OCTGN}/Sets/${idSet}/Cards`
  const xml = []
  let position = 0
  const heros = entrees.find((e) => e.faces[0].type === 'identity' || e.faces[0].type === 'identity-promo')
  const entier = (v) => (/^\d+$/.test(String(v ?? '').trim()) ? String(parseInt(v, 10)) : null)
  const proprietes = (c, numero, pos, suffixe = '') => {
    const ct = c.contenu
    const p = [['CardNumber', numero + suffixe], ['Position', pos], ['Quantity', 1], ['Type', TYPE_TABLE[c.type]], ['Owner', proprietaire]]
    const nombre = (cle, cls, v) => { const n = entier(v); if (n !== null && montre(c, cls)) p.push([cle, n]) }
    if (ct.unique) p.push(['Unique', 'True'])
    nombre('Cost', 'paycost cost', ct.cout)
    nombre(['villain', 'minion'].includes(c.type) ? 'Scheme' : 'Thwart', 'thw sch cost', ct.thw)
    nombre('Attack', 'atk cost', ct.atk)
    nombre('Defense', 'def cost', ct.def)
    nombre('Recovery', 'rec cost', ct.rec)
    nombre('HandSize', 'handsize', ct.tailleMain)
    nombre('HP', 'hp cost', ct.pv)
    if (c.type === 'ally') { if (ct.atkConseq > 0) p.push(['AttackCost', ct.atkConseq]); if (ct.thwConseq > 0) p.push(['ThwartCost', ct.thwConseq]) }
    const ress = { Resource_Physical: 'physical', Resource_Mental: 'mental', Resource_Energy: 'energy', Resource_Wild: 'wild' }
    for (const [cle, genre] of Object.entries(ress)) { const n = (ct.ressources || []).filter((r) => r === genre).length; if (n) p.push([cle, n]) }
    if (ct.renforts > 0) p.push(['Boost', ct.renforts])
    // manigances : un nombre imprime tel quel (sans icone « par joueur ») est FIXE
    if (['sidescheme', 'playersidescheme'].includes(c.type) || c.type.startsWith('main_scheme')) {
      nombre('Threat', 'targetthreat cost', ct.menaceCible)
      const base = entier(ct.menaceDepart)
      if (base !== null && montre(c, 'startingthreatwrap')) { p.push(['BaseThreat', base]); p.push(['BaseThreatFixed', 'True']) }
      const esc = entier(ct.acceleration)
      if (esc !== null && montre(c, 'acceleration')) { p.push(['EscalationThreat', esc]); p.push(['EscalationThreatFixed', 'True']) }
    }
    const texte = texteBrut(ct.regles), citation = texteBrut(ct.citation)
    if (texte) p.push(['Text', texte])
    if (citation) p.push(['Quote', citation])
    return p
  }
  const ligne = (marge, [k, v]) => (k === 'Text' || k === 'Quote' ? `${marge}<property name="${k}">${echapper(v)}</property>` : `${marge}<property name="${k}" value="${echapper(v)}"/>`)
  if (heros) {
    // la carte de « mise en place » du heros, comme dans les sets de la communaute : un point d'entree pour le constructeur de deck
    const c = heros.faces[0]
    xml.push(`    <card id="${idCarte(900001)}" name="${echapper((c.contenu.titre || 'Hero') + ' (' + nomSet + ')')}">`,
      '      <property name="Type" value="fm_hero_setup"/>', `      <property name="Owner" value="${echapper(proprietaire)}"/>`, '    </card>')
    fichiers.push({ nom: `${images}/${idCarte(900001)}.jpg`, octets: await jpeg(await rendre(c, c.langue), 880) })
  }
  for (const e of entrees) {
    position++
    const numero = 999000 + position
    const [a, b] = e.faces
    const taille = ['sidescheme', 'main_scheme_a', 'playersidescheme'].includes(a.type) ? ' size="SchemeCard"' : (['minion', 'treachery', 'attachment', 'environment', 'obligation', 'obligation-villain'].includes(a.type) ? ' size="EncounterCard"' : (a.type === 'villain' ? ' size="VillainCard"' : ''))
    const lignes = [`    <card name="${echapper(a.contenu.titre)}" id="${idCarte(numero)}"${taille}>`, ...proprietes(a, numero, position, b ? 'a' : '').map((p) => ligne('      ', p))]
    if (b) {
      lignes.push(`      <alternate name="${echapper(b.contenu.titre)}" type="b">`, ...proprietes(b, numero, position, 'b').filter(([k]) => k !== 'Quantity').map((p) => ligne('        ', p)), '      </alternate>')
      fichiers.push({ nom: `${images}/${idCarte(numero)}.b.jpg`, octets: await jpeg(await rendre(b, b.langue), 880) })
    }
    lignes.push('    </card>')
    xml.push(...lignes)
    fichiers.push({ nom: `${images}/${idCarte(numero)}.jpg`, octets: await jpeg(await rendre(a, a.langue), 880) })
  }
  const doc = '﻿<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n'
    + `<set name="${echapper(nomSet)}" id="${idSet}" gameId="${JEU_OCTGN}" gameVersion="0.0.0.0" version="1.0.0.0">\n <cards>\n${xml.join('\n')}\n </cards>\n</set>\n`
  fichiers.push({ nom: `${base}/set.xml`, octets: new TextEncoder().encode(doc) })
  return fichiers
}

export const LISEZ_MOI_OCTGN = `Set OCTGN — fabrique par le Createur de cartes
================================================

Contenu : GameDatabase/ (set.xml) et ImageDataBase/ (une image par carte, <id>.jpg ; la face B d'un heros ou d'une manigance : <id>.b.jpg).

Installer : copie GameDatabase et ImageDataBase dans le dossier de donnees d'OCTGN (sous Windows : Documents\\OCTGN\\), en gardant l'arborescence,
puis relance OCTGN. Le jeu est Marvel Champions (id ${JEU_OCTGN}).

Structure reprise d'un set de la communaute (She-Hulk par Merlin) et recoupee avec le code de MCdeck (outil qui lit et ecrit les sets OCTGN
de Marvel Champions) : types, proprietes, tailles (SchemeCard / EncounterCard / VillainCard). A savoir :
  - OCTGN n'a pas de type « manigance annexe de joueur » : elle est exportee en side_scheme ;
  - seuls les nombres entiers sont exportes (pas les X ni les etoiles) ; la menace de depart et l'acceleration sont marquees « fixes » ;
  - Owner : "fm_<set>" pour toutes les cartes (le suffixe _nemesis, qui range des cartes rencontre dans le nemesis d'un heros, n'est pas pose) ;
  - la carte "fm_hero_setup" (point d'entree du constructeur de deck) n'est creee que s'il y a un heros ;
  - Quantity vaut 1 partout : change-la dans set.xml pour les cartes en plusieurs exemplaires.
`

// ---------------------------------------------------------------- DragnCards
// Colonnes du plugin Marvel Champions de DragnCards (github.com/hone/dragncards-mc-plugin : src/dragncards/database.rs, json/cardTypes.json,
// json/cardBacks.json, json/faceProperties.json) : databaseId, name, subname, type, classification, imageUrl, cardBack, traits, handSize,
// hitPointsFixed, set, stage, startingThreatFixed, accelerationFixed. Les valeurs de `type` y portent des majuscules et des espaces
// (« Alter-Ego », « Main Scheme », « Side Scheme »...) et `cardBack` vaut encounter / player / villain (ou multi_sided pour les deux faces).
const COLONNES = ['databaseId', 'name', 'subname', 'type', 'classification', 'imageUrl', 'cardBack', 'traits', 'handSize', 'hitPointsFixed', 'set', 'stage', 'startingThreatFixed', 'accelerationFixed']
const TYPE_DRAGN = {
  identity: 'Hero', 'identity-promo': 'Hero', 'alter-ego': 'Alter-Ego', 'alter-ego-promo': 'Alter-Ego', ally: 'Ally', 'generic-promo': 'Ally', 'generic-promo-vert': 'Ally',
  event: 'Event', upgrade: 'Upgrade', support: 'Support', resource: 'Resource', 'starter-deck': 'Resource', obligation: 'Obligation', 'obligation-villain': 'Obligation',
  playersidescheme: 'Player Side Scheme', villain: 'Villain', minion: 'Minion', treachery: 'Treachery', environment: 'Environment', attachment: 'Attachment',
  sidescheme: 'Side Scheme', main_scheme_a: 'Main Scheme', main_scheme_b: 'Main Scheme',
}
const DOS_ENCOUNTER = new Set(['Attachment', 'Environment', 'Minion', 'Obligation', 'Side Scheme', 'Treachery'])
const CLASSIFICATION_RENCONTRE = new Set(['Attachment', 'Environment', 'Minion', 'Obligation', 'Side Scheme', 'Treachery', 'Villain', 'Main Scheme'])
const tsv = (v) => String(v ?? '').replace(/[\t\r\n]+/g, ' ').trim()
/** « Asgard. Avenger. » -> « Asgard,Avenger » (le format des traits du plugin). */
const traitsDragn = (t) => String(t ?? '').split('.').map((x) => x.trim()).filter(Boolean).join(',')

/** Le .tsv et les images : [{ nom, octets }]. `prefixe` : l'adresse (finie par « / ») ou seront hebergees les images. */
export async function genererDragncards(cartes, { nomSet, rendre, prefixe = '' }) {
  const lignes = [COLONNES.join('\t')]
  const fichiers = []
  const pris = new Set()
  const unique = (base) => { let n = base; let k = 2; while (pris.has(n)) n = `${base}_${k++}`; pris.add(n); return n }
  const entier = (v) => (/^\d+$/.test(String(v ?? '').trim()) ? String(parseInt(v, 10)) : '')
  for (const e of regrouper(cartes)) {
    const multi = e.faces.length > 1
    const base = unique(slug(e.faces[0].contenu.titre))
    const id = guidStable(`dragncards:${nomSet}:${base}`)
    for (const [i, c] of e.faces.entries()) {
      const ct = c.contenu
      const type = TYPE_DRAGN[c.type]
      const fichier = `custom-${slug(nomSet)}-${base}${multi ? '-' + 'ab'[i] : ''}.jpg`
      fichiers.push({ nom: `images/${fichier}`, octets: await jpeg(await rendre(c, c.langue), 1050) })
      const stage = c.type === 'villain' ? ct.etape : (c.type.startsWith('main_scheme') ? ct.phaseNumero : '')
      const valeurs = {
        databaseId: id, name: ct.titre, subname: '', type,
        classification: CLASSIFICATION_RENCONTRE.has(type) ? 'Encounter' : (type === 'Resource' || type === 'Event' || type === 'Support' || type === 'Upgrade' || type === 'Ally' ? '' : 'Hero'),
        imageUrl: prefixe + fichier,
        cardBack: multi ? 'multi_sided' : (type === 'Villain' ? 'villain' : (DOS_ENCOUNTER.has(type) ? 'encounter' : 'player')),
        traits: traitsDragn(ct.traits), handSize: montre(c, 'handsize') ? entier(ct.tailleMain) : '', hitPointsFixed: montre(c, 'hp cost') ? entier(ct.pv) : '',
        set: nomSet, stage, startingThreatFixed: montre(c, 'startingthreatwrap') ? entier(ct.menaceDepart) : '', accelerationFixed: montre(c, 'acceleration') ? entier(ct.acceleration) : '',
      }
      lignes.push(COLONNES.map((k) => tsv(valeurs[k])).join('\t'))
    }
  }
  fichiers.push({ nom: 'cards.tsv', octets: new TextEncoder().encode(lignes.join('\n') + '\n') })
  return fichiers
}

export const LISEZ_MOI_DRAGNCARDS = `Cartes pour DragnCards — fabrique par le Createur de cartes
==========================================================

Contenu : cards.tsv (separe par des tabulations) et images/ (une image par face).

Utiliser (wiki officiel de DragnCards, page « Custom Content ») :
  1. Heberge les images : DragnCards n'en heberge aucune. Chaque imageUrl doit etre une adresse complete finissant par .jpg ou .png
     (Google Drive ne marche pas). Si tu n'as pas donne d'adresse dans l'export, imageUrl ne contient que le nom du fichier : remplace-le
     par l'adresse complete (ou ajoute-la devant dans un tableur).
  2. Dans une salle du plugin Marvel Champions : Builder -> Custom Content -> « Download Example Template » pour comparer les colonnes.
  3. Menu « Upload Public Cards » : choisis cards.tsv. Chaque ligne doit montrer une petite image.

Colonnes obligatoires de DragnCards : databaseId, name, imageUrl, cardBack, type. Les autres colonnes (celles du plugin Marvel Champions :
subname, classification, traits, handSize, hitPointsFixed, set, stage, startingThreatFixed, accelerationFixed) deviennent des proprietes.
Une carte a deux faces (heros + alter-ego, manigance A + B) = deux lignes de meme databaseId avec cardBack = multi_sided.

Valeurs reprises du plugin (github.com/hone/dragncards-mc-plugin) : type = Hero, Alter-Ego, Ally, Event, Upgrade, Support, Resource, Obligation,
Villain, Minion, Treachery, Environment, Attachment, Side Scheme, Player Side Scheme, Main Scheme ; cardBack = player, encounter, villain.
A savoir : les nombres ne sont exportes que s'ils sont entiers (pas les X ni les etoiles) ; un nombre de PV ou de menace est exporte comme
« fixe » (le createur ne dessine pas l'icone « par joueur »), a corriger a la main dans le tableur si besoin.
`
