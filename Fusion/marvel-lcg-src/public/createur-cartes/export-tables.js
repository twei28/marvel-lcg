// Les exports pour les tables de jeu en ligne : un set OCTGN (GameDatabase + ImageDataBase) et des cartes pour DragnCards (.tsv + images).
//
// SOURCES (pas de devinette) :
//  - OCTGN : la structure et les proprietes viennent d'un VRAI set de la communaute (« She-Hulk - Why Not », par Merlin, dans le dossier
//    She-Hulk Release EN) : set.xml (<set> / <card> / <alternate>, proprietes CardNumber, Position, Quantity, Type, Owner, HP, HandSize,
//    BaseThreat, BaseThreatFixed, DefaultSetupPile), images <id>.jpg et <id>.b.jpg sous ImageDataBase. Les noms de Type de ce set (hero,
//    alter_ego, ally, event, support, upgrade, obligation, minion, attachment, treachery, side_scheme) sont repris tels quels ; ceux qu'il
//    n'illustre pas (villain, main_scheme, environment, resource, player_side_scheme) suivent le meme usage : A VERIFIER dans OCTGN.
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
const texteBrut = (html) => String(html ?? '').replace(/<hr[^>]*>/gi, '\n').replace(/<[^>]*>/g, '').replace(/&mdash;/g, '—').replace(/&nbsp;/g, ' ').replace(/[ \t]+/g, ' ').trim()

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
  event: 'event', upgrade: 'upgrade', support: 'support', resource: 'resource', obligation: 'obligation', playersidescheme: 'player_side_scheme',
  villain: 'villain', minion: 'minion', treachery: 'treachery', environment: 'environment', attachment: 'attachment', sidescheme: 'side_scheme',
  main_scheme_a: 'main_scheme', main_scheme_b: 'main_scheme', 'obligation-villain': 'obligation', 'starter-deck': 'resource',
}
const RENCONTRE = new Set(['villain', 'minion', 'treachery', 'environment', 'attachment', 'side_scheme', 'main_scheme', 'obligation'])
const estRencontre = (c) => RENCONTRE.has(TYPE_TABLE[c.type]) && c.type !== 'obligation'

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
  const proprietes = (c, numero, pos, suffixe = '') => {
    const ct = c.contenu
    const p = [['CardNumber', numero + suffixe], ['Position', pos], ['Quantity', 1], ['Type', TYPE_TABLE[c.type]], ['Owner', proprietaire + (estRencontre(c) ? '_encounter' : '')]]
    if (ct.tailleMain && montre(c, 'handsize')) p.push(['HandSize', ct.tailleMain])
    if (ct.pv !== '' && ct.pv != null && montre(c, 'hp cost')) p.push(['HP', ct.pv])
    if (c.type === 'sidescheme' && ct.menaceDepart !== '') { p.push(['BaseThreat', ct.menaceDepart]); p.push(['BaseThreatFixed', 'True']) }
    return p
  }
  const ligne = (marge, [k, v]) => `${marge}<property name="${k}" value="${echapper(v)}"/>`
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
    const taille = ['sidescheme', 'main_scheme_a'].includes(a.type) ? ' size="SchemeCard"' : (['minion', 'treachery', 'attachment', 'obligation', 'obligation-villain'].includes(a.type) ? ' size="EncounterCard"' : '')
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

Structure reprise d'un set de la communaute (She-Hulk par Merlin). A VERIFIER dans OCTGN :
  - les Type utilises pour villain, main_scheme, environment, resource et player_side_scheme (non illustres par ce set d'exemple) ;
  - Owner : "fm_<set>" pour les cartes joueur, "fm_<set>_encounter" pour les cartes rencontre (a ajuster selon ton plugin) ;
  - la carte "fm_hero_setup" (point d'entree du constructeur de deck) n'est creee que s'il y a un heros ;
  - Quantity vaut 1 partout : change-la dans set.xml pour les cartes en plusieurs exemplaires.
`

// ---------------------------------------------------------------- DragnCards
const COLONNES = ['databaseId', 'name', 'imageUrl', 'cardBack', 'type', 'cardSet', 'traits', 'cost', 'thw', 'atk', 'def', 'rec', 'hp', 'handSize', 'text']
const tsv = (v) => String(v ?? '').replace(/[\t\r\n]+/g, ' ').trim()

/** Le .tsv et les images : [{ nom, octets }]. `prefixe` : l'adresse (finie par « / ») ou seront hebergees les images. */
export async function genererDragncards(cartes, { nomSet, rendre, prefixe = '' }) {
  const lignes = [COLONNES.join('\t')]
  const fichiers = []
  const pris = new Set()
  const unique = (base) => { let n = base; let k = 2; while (pris.has(n)) n = `${base}_${k++}`; pris.add(n); return n }
  for (const e of regrouper(cartes)) {
    const multi = e.faces.length > 1
    const id = 'custom-' + slug(nomSet) + '-' + unique(slug(e.faces[0].contenu.titre))
    for (const [i, c] of e.faces.entries()) {
      const ct = c.contenu
      const fichier = `${id}${multi ? '-' + 'ab'[i] : ''}.jpg`
      fichiers.push({ nom: `images/${fichier}`, octets: await jpeg(await rendre(c, c.langue), 1050) })
      const valeurs = {
        databaseId: id, name: ct.titre, imageUrl: prefixe + fichier, cardBack: multi ? 'multi_sided' : (estRencontre(c) ? 'encounter' : 'player'),
        type: TYPE_TABLE[c.type], cardSet: nomSet, traits: ct.traits, cost: montre(c, 'paycost cost') ? ct.cout : '', thw: montre(c, 'thw sch cost') ? ct.thw : '',
        atk: montre(c, 'atk cost') ? ct.atk : '', def: montre(c, 'def cost') ? ct.def : '', rec: montre(c, 'rec cost') ? ct.rec : '', hp: montre(c, 'hp cost') ? ct.pv : '',
        handSize: montre(c, 'handsize') ? ct.tailleMain : '', text: texteBrut(ct.regles),
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
  2. Dans une salle du plugin Marvel Champions : Builder -> Custom Content -> « Download Example Template » : compare les colonnes et les
     valeurs de cardBack et de type avec celles de cards.tsv.
  3. Menu « Upload Public Cards » : choisis cards.tsv. Chaque ligne doit montrer une petite image.

Colonnes obligatoires : databaseId, name, imageUrl, cardBack, type. Une carte a deux faces (heros + alter-ego, manigance A + B) = deux lignes
de meme databaseId avec cardBack = multi_sided.

A VERIFIER avec le modele du plugin : les valeurs de type (hero, alter_ego, ally, event, upgrade, support, resource, obligation, villain,
minion, treachery, environment, attachment, side_scheme, main_scheme, player_side_scheme) et de cardBack (player, encounter) doivent exister
dans ce plugin. Les colonnes en plus (cardSet, traits, cost, thw, atk, def, rec, hp, handSize, text) deviennent des proprietes de carte.
`
