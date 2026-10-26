// La langue du JEU (tables p<N>.<domaine>, autre origine que le site) suit le site, puis le navigateur (decision du 26/10/2026).
// Ordre : choix fait DANS le jeu (marvel-langue) > cookie nc_langue (pose par le site avec Domain=.<domaine>) > navigator.language > francais.
// Le jeu ecrit aussi le cookie quand le joueur change de langue, pour que le site et les autres tables suivent.
//
// Le module PUR (langue-resolution.js) est teste ici ; son jumeau classique (langue-classique.js, pour les petits scripts
// non-modules de la page de preparation) est evalue dans un bac a sable et compare au module pur sur les memes cas ; le jumeau
// TypeScript (ui-app/src/board/langue-resolution.ts) est compare dans ui-app/src/board/langue-resolution.test.ts.
import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath, pathToFileURL } from 'node:url'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const PREPARE = path.resolve(ICI, '../../public/js/prepare')
const PUBLIC = path.resolve(ICI, '../../public')

const R = await import(pathToFileURL(path.join(PREPARE, 'langue-resolution.js')).href)

const NAV = (language, languages) => ({ language, languages: languages || [language] })

const CAS = [
  // [nom, entrees, attendu]
  ['rien du tout -> francais', { stockage: '', cookie: '', navigateur: null }, 'fr'],
  ['navigateur en-US -> anglais', { stockage: '', cookie: '', navigateur: NAV('en-US') }, 'en'],
  ['navigateur fr-FR -> francais', { stockage: '', cookie: '', navigateur: NAV('fr-FR') }, 'fr'],
  ['navigateur de, rien d\'autre -> francais', { stockage: '', cookie: '', navigateur: NAV('de-DE') }, 'fr'],
  ['cookie fr + navigateur en -> francais', { stockage: '', cookie: 'nc_langue=fr', navigateur: NAV('en-US') }, 'fr'],
  ['cookie en + navigateur fr -> anglais', { stockage: '', cookie: 'a=1; nc_langue=en; b=2', navigateur: NAV('fr-FR') }, 'en'],
  ['stockage en + cookie fr -> anglais (le choix fait dans le jeu gagne)', { stockage: 'en', cookie: 'nc_langue=fr', navigateur: NAV('fr-FR') }, 'en'],
  ['stockage fr + cookie en -> francais (le choix fait dans le jeu gagne)', { stockage: 'fr', cookie: 'nc_langue=en', navigateur: NAV('en-US') }, 'fr'],
  ['cookie invalide ignore -> navigateur', { stockage: '', cookie: 'nc_langue=klingon', navigateur: NAV('en-GB') }, 'en'],
  ['stockage invalide ignore -> cookie', { stockage: 'triangles', cookie: 'nc_langue=en', navigateur: NAV('fr-FR') }, 'en'],
  ['cookie d\'un autre nom ignore', { stockage: '', cookie: 'langue=en', navigateur: NAV('fr-FR') }, 'fr'],
  ['languages[0] quand language manque', { stockage: '', cookie: '', navigateur: { languages: ['en-AU'] } }, 'en'],
]

for (const [nom, entrees, attendu] of CAS) {
  test('resoudreLangue : ' + nom, () => {
    assert.equal(R.resoudreLangue(entrees), attendu)
  })
}

test('lireCookieLangue : seulement fr / en, au bon nom', () => {
  assert.equal(R.lireCookieLangue('nc_langue=en'), 'en')
  assert.equal(R.lireCookieLangue('x=1;nc_langue=fr;y=2'), 'fr')
  assert.equal(R.lireCookieLangue('nc_langue=EN'), '')
  assert.equal(R.lireCookieLangue('xnc_langue=en'), '')
  assert.equal(R.lireCookieLangue(''), '')
  assert.equal(R.lireCookieLangue(undefined), '')
})

test('domaineParentCookie : p<N>, play, www remontent au domaine ; ni IP ni localhost n\'ont de Domain', () => {
  assert.equal(R.domaineParentCookie('p1.narwhalchampions.com'), '.narwhalchampions.com')
  assert.equal(R.domaineParentCookie('p12.narwhalchampions.com:443'), '.narwhalchampions.com')
  assert.equal(R.domaineParentCookie('play.narwhalchampions.com'), '.narwhalchampions.com')
  assert.equal(R.domaineParentCookie('www.narwhalchampions.com'), '.narwhalchampions.com')
  assert.equal(R.domaineParentCookie('narwhalchampions.com'), '.narwhalchampions.com')
  assert.equal(R.domaineParentCookie('localhost'), '')
  assert.equal(R.domaineParentCookie('localhost:2345'), '')
  assert.equal(R.domaineParentCookie('127.0.0.1'), '')
  assert.equal(R.domaineParentCookie('192.168.1.20:8080'), '')
  assert.equal(R.domaineParentCookie('[::1]:2345'), '')
  assert.equal(R.domaineParentCookie(''), '')
  assert.equal(R.domaineParentCookie('machin.exemple.org'), '')
})

test('cookieLangue : memes attributs que le site (Path=/, un an, SameSite=Lax, Domain parent, Secure en https)', () => {
  assert.equal(
    R.cookieLangue('en', 'p3.narwhalchampions.com', 'https:'),
    'nc_langue=en; Path=/; Max-Age=31536000; SameSite=Lax; Domain=.narwhalchampions.com; Secure'
  )
  assert.equal(R.cookieLangue('fr', 'localhost:2345', 'http:'), 'nc_langue=fr; Path=/; Max-Age=31536000; SameSite=Lax')
  assert.equal(R.cookieLangue('klingon', '127.0.0.1', 'http:'), 'nc_langue=fr; Path=/; Max-Age=31536000; SameSite=Lax')
})

// ---- le jumeau classique (petits scripts de la page de preparation) -------------------------------------------------------
function chargerClassique({ stockage, cookie, navigateur, hote = 'p1.narwhalchampions.com', protocole = 'https:', stockageBloque = false }) {
  const ecrits = []
  const fenetre = {}
  const contexte = {
    window: fenetre,
    navigator: navigateur,
    location: { hostname: hote.replace(/:\d+$/, ''), host: hote, protocol: protocole },
    localStorage: stockageBloque
      ? { getItem() { throw new Error('bloque') }, setItem() { throw new Error('bloque') } }
      : { getItem: (k) => (k === 'marvel-langue' && stockage ? stockage : null), setItem() {} },
    document: {
      get cookie() { return cookie },
      set cookie(v) { ecrits.push(v) },
    },
  }
  contexte.window.localStorage = contexte.localStorage
  contexte.window.document = contexte.document
  vm.createContext(contexte)
  vm.runInContext(fs.readFileSync(path.join(PREPARE, 'langue-classique.js'), 'utf8'), contexte)
  return { M: fenetre.MarvelLangue, ecrits }
}

for (const [nom, entrees, attendu] of CAS) {
  test('langue-classique.js = langue-resolution.js : ' + nom, () => {
    const { M } = chargerClassique({ stockage: entrees.stockage, cookie: entrees.cookie, navigateur: entrees.navigateur })
    assert.ok(M && typeof M.actuelle === 'function', 'window.MarvelLangue.actuelle doit exister')
    assert.equal(M.actuelle(), attendu)
  })
}

test('langue-classique.js : stockage bloque (navigation privee) -> cookie, puis navigateur', () => {
  assert.equal(chargerClassique({ stockageBloque: true, cookie: 'nc_langue=en', navigateur: NAV('fr-FR') }).M.actuelle(), 'en')
  assert.equal(chargerClassique({ stockageBloque: true, cookie: '', navigateur: NAV('en-US') }).M.actuelle(), 'en')
})

test('langue-classique.js : ecrire() pose le meme cookie que le module pur', () => {
  const { M, ecrits } = chargerClassique({ stockage: '', cookie: '', navigateur: NAV('fr-FR'), hote: 'p2.narwhalchampions.com', protocole: 'https:' })
  M.ecrire('en')
  assert.deepEqual(ecrits, [R.cookieLangue('en', 'p2.narwhalchampions.com', 'https:')])
})

// ---- branchements (controle de texte : ces fichiers ne s'importent pas en node) ---------------------------------------------
const lire = (f) => fs.readFileSync(f, 'utf8')

test('langue.js : langueActuelle suit la resolution commune, et les changements de langue ecrivent le cookie', () => {
  const src = lire(path.join(PREPARE, 'langue.js'))
  assert.match(src, /from "\/public\/js\/prepare\/langue-resolution\.js"/)
  assert.match(src, /resoudreLangue\(/)
  const basc = src.slice(src.indexOf('export async function basculerLangue'), src.indexOf('/* --- LE CHOIX DE LA LANGUE'))
  assert.match(basc, /poserCookieLangue\(/, 'basculerLangue doit ecrire le cookie nc_langue')
  const ret = src.slice(src.indexOf('export async function retenirLangue'), src.indexOf('/** Bouton FR/EN'))
  assert.match(ret, /poserCookieLangue\(/, 'retenirLangue doit ecrire le cookie nc_langue (changement ou non)')
})

test('langue.js : la question de langue ne se pose plus quand le site a deja fixe la langue (cookie present)', () => {
  const src = lire(path.join(PREPARE, 'langue.js'))
  const corps = src.slice(src.indexOf('export function langueDejaChoisie'), src.indexOf('/** Retient la réponse'))
  assert.match(corps, /lireCookieLangue\(/)
})

const MINI = ['annonce.js', 'invitations.js', 'maj.js', 'messages.js', 'reprise.js', 'lien-admin.js', 'lien-signalements.js', 'lien-galerie.js']
for (const f of MINI) {
  test('petit script ' + f + ' : lit la langue par MarvelLangue (plus de lecture directe de marvel-langue)', () => {
    const src = lire(path.join(PREPARE, f))
    assert.match(src, /window\.MarvelLangue\s*\?/, f + ' doit passer par window.MarvelLangue (le stockage direct ne sert que de repli)')
  })
}

for (const page of ['prepare.html', 'campagne.html', 'deck-builder.html']) {
  test(page + ' : langue-classique.js est charge AVANT les petits scripts qui en dependent', () => {
    const html = lire(path.join(PUBLIC, page))
    const i = html.indexOf('langue-classique.js')
    assert.ok(i > 0, page + ' doit charger langue-classique.js')
    for (const f of MINI) {
      const j = html.indexOf('/' + f + '?')
      if (j > 0) assert.ok(i < j, page + ' : langue-classique.js doit preceder ' + f)
    }
  })
}
