// Rend le voile FR de chaque carte, pour l'export ZIP des images (27/10/2026).
//
// Lancé par Fusion/marvel-lcg-src/tools/exporter_images_cartes.py, jamais à la
// main en temps normal :
//
//   node ui-app/outils/export-voile/rendre-voile.mjs <travail.json>
//
// travail.json = {
//   "cache": "<dossier>",          // les rendus, gardés d'une génération à l'autre
//   "public": "<moteur>/public",   // les polices de la carte (/public/fonts/...)
//   "catalogues": ["<cards.json>", "<cards_custom.json>"],
//   "paralleles": 3,
//   "cartes": [{ "code", "image", "largeur", "hauteur", "type" }, ...]
// }
//
// Pour chaque carte : le banc (harnais.tsx, servi par un Vite local) donne le
// texte que le site connaît ; sans texte, rien à faire. Sinon la clé du rendu
// (version du code du voile + octets du scan + texte + traits + type) est
// cherchée dans <cache>/index.json : connue, le rendu précédent est gardé ;
// inconnue, la carte est montée dans Chromium et photographiée.
//
// Sortie standard, lue par le script Python : « PROGRES <fait>/<total> » au fil
// de l'eau, puis « FIN <résumé JSON> ».
import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync, createReadStream, statSync } from 'node:fs'
import { createRequire } from 'node:module'
import { dirname, extname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const ICI = dirname(fileURLToPath(import.meta.url))
const UI_APP = resolve(ICI, '../..')
const BOARD = join(UI_APP, 'src/board')

const travail = JSON.parse(readFileSync(process.argv[2], 'utf8'))
const CACHE = travail.cache
mkdirSync(CACHE, { recursive: true })
const INDEX = join(CACHE, 'index.json')
const index = existsSync(INDEX) ? JSON.parse(readFileSync(INDEX, 'utf8')) : {}

// La VERSION du voile : tout fichier dont dépend le rendu. Une retouche de
// l'algorithme invalide donc tous les rendus, et eux seuls.
const SOURCES = [
  'TraductionPosee.tsx', 'traduction-posee.ts', 'traduction-posee.css', 'effacer-texte.ts', 'effacer-texte.worker.ts',
  'zones-corrections.ts', 'zones-arts-alternatifs.ts', 'traits-fr.ts', 'catalogue.ts', 'traduction-carte.tsx', 'marvelcdb.ts',
].map((f) => join(BOARD, f)).concat([join(ICI, 'harnais.tsx'), join(ICI, 'rendre-voile.mjs')])
const empreinte = createHash('sha1')
for (const f of SOURCES) if (existsSync(f)) empreinte.update(readFileSync(f))
const VERSION = empreinte.digest('hex').slice(0, 12)

// Le catalogue fusionné, comme /get_cards_json du moteur (cards.json puis les fichiers custom).
const fusion = {}
for (const chemin of travail.catalogues ?? []) {
  const donnees = JSON.parse(readFileSync(chemin, 'utf8'))
  for (const [paquet, cartes] of Object.entries(donnees)) if (Array.isArray(cartes)) (fusion[paquet] ??= []).push(...cartes)
}
const catalogueJson = JSON.stringify(fusion)

const images = new Map(travail.cartes.map((c) => [c.code, c.image]))
const TYPES = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.ttf': 'font/ttf', '.otf': 'font/otf', '.woff': 'font/woff', '.woff2': 'font/woff2' }

/** Le moteur, réduit à ce que lit le voile : le catalogue, les polices, les scans. */
const routesDuJeu = {
  name: 'routes-du-jeu-export',
  configureServer(serveur) {
    serveur.middlewares.use((req, res, suite) => {
      const chemin = decodeURIComponent((req.url ?? '').split('?')[0])
      let fichier = null
      if (chemin === '/get_cards_json') {
        res.setHeader('Content-Type', 'application/json')
        res.end(catalogueJson)
        return
      }
      if (chemin.startsWith('/export-scan/')) fichier = images.get(chemin.slice('/export-scan/'.length)) ?? null
      else if (chemin.startsWith('/public/fonts/')) {
        const f = resolve(travail.public, 'fonts', chemin.slice('/public/fonts/'.length))
        if (f.startsWith(resolve(travail.public, 'fonts'))) fichier = f
      }
      if (fichier === null) return suite()
      if (!existsSync(fichier)) {
        res.statusCode = 404
        res.end()
        return
      }
      res.setHeader('Content-Type', TYPES[extname(fichier).toLowerCase()] ?? 'application/octet-stream')
      res.setHeader('Content-Length', statSync(fichier).size)
      createReadStream(fichier).pipe(res)
    })
  },
}

/** Playwright : celui de ui-check (déjà installé pour les captures), ou un global. */
async function chargerPlaywright() {
  try {
    return await import('playwright')
  } catch {
    const exiger = createRequire(join(UI_APP, '../ui-check/package.json'))
    return exiger('playwright')
  }
}

const { createServer } = await import('vite')
const react = (await import('@vitejs/plugin-react')).default
const serveur = await createServer({
  configFile: false,
  root: UI_APP,
  base: '/',
  logLevel: 'error',
  plugins: [react(), routesDuJeu],
  server: { host: '127.0.0.1', port: 0, strictPort: false, hmr: false },
  // Le gros dictionnaire (1 Mo) est importé à la demande : on laisse Vite le transformer tel quel.
  optimizeDeps: { include: ['react', 'react-dom', 'react-dom/client', 'react/jsx-runtime', 'react/jsx-dev-runtime'] },
})
await serveur.listen()
const adresse = serveur.resolvedUrls?.local?.[0] ?? `http://127.0.0.1:${serveur.config.server.port}/`

const { chromium } = await chargerPlaywright()
const navigateur = await chromium.launch()
const contexte = await navigateur.newContext({ deviceScaleFactor: 1, viewport: { width: 1200, height: 1200 } })

const resume = { version: VERSION, total: travail.cartes.length, sansTexte: 0, rendues: 0, gardees: 0, nonPosees: 0, erreurs: 0 }
let fait = 0
let depuisSauvegarde = 0

function sauverIndex() {
  const provisoire = INDEX + '.tmp'
  writeFileSync(provisoire, JSON.stringify(index))
  renameSync(provisoire, INDEX)
}

async function nouvellePage() {
  const page = await contexte.newPage()
  // Mesure : EXPORT_VOILE_FONDS=1 écrit aussi, pour chaque carte, le fond nettoyé SANS le français (fond-<code>.webp), pour voir ce qui reste d'anglais.
  if (process.env.EXPORT_VOILE_FONDS) await page.addInitScript(() => { window.exportVoileFonds = true })
  page.on('pageerror', (e) => process.stderr.write(`[page] ${e}\n`))
  await page.goto(new URL('outils/export-voile/index.html', adresse).href)
  await page.waitForFunction(() => window.exportVoile?.pret === true, null, { timeout: 120000 })
  return page
}

async function traiter(page, carte) {
  const connu = await page.evaluate((code) => window.exportVoile.texte(code), carte.code)
  if (!connu) {
    resume.sansTexte += 1
    return
  }
  const octets = readFileSync(carte.image)
  const shaImage = createHash('sha1').update(octets).digest('hex')
  const cle = createHash('sha1')
    .update([VERSION, shaImage, connu.texte, connu.traits.join('|'), carte.type ?? '', carte.largeur, carte.hauteur].join('\u0000'))
    .digest('hex')
  const ancien = index[carte.code]
  if (ancien && ancien.cle === cle && (!ancien.fichier || existsSync(join(CACHE, ancien.fichier)))) {
    resume.gardees += 1
    if (!ancien.fichier) resume.nonPosees += 1
    return
  }
  await page.setViewportSize({ width: Math.max(100, carte.largeur), height: Math.max(100, carte.hauteur) })
  const resultat = await page.evaluate(
    (c) => window.exportVoile.poser(c),
    { code: carte.code, url: `/export-scan/${carte.code}`, largeur: carte.largeur, hauteur: carte.hauteur, type: carte.type, texte: connu.texte, traits: connu.traits }
  )
  if (!resultat.pose) {
    resume.nonPosees += 1
    index[carte.code] = { cle, fichier: null, image_sha: shaImage, raison: resultat.raison ?? 'non-posee' }
    return
  }
  const fichier = `${carte.code}.jpg`
  const urlFond = resultat.fond && /url\("?(data:[^")]+)"?\)/.exec(resultat.fond)
  if (urlFond) writeFileSync(join(CACHE, `fond-${carte.code}.webp`), Buffer.from(urlFond[1].split(',')[1], 'base64'))
  await page.locator('#scene .cadre').screenshot({ path: join(CACHE, fichier), type: 'jpeg', quality: 92 })
  index[carte.code] = { cle, fichier, image_sha: shaImage, fond_nettoye: resultat.fondNettoye, zone: resultat.zone }
  resume.rendues += 1
}

const file = [...travail.cartes]
const paralleles = Math.max(1, Math.min(8, travail.paralleles ?? 3))
async function ouvrier() {
  let page = await nouvellePage()
  for (;;) {
    const carte = file.shift()
    if (!carte) break
    try {
      await traiter(page, carte)
    } catch (e) {
      resume.erreurs += 1
      process.stderr.write(`[erreur] ${carte.code} : ${e}\n`)
      // Une page plantée ne doit pas emporter les cartes suivantes.
      await page.close().catch(() => undefined)
      page = await nouvellePage()
    }
    fait += 1
    depuisSauvegarde += 1
    process.stdout.write(`PROGRES ${fait}/${travail.cartes.length}\n`)
    if (depuisSauvegarde >= 25) {
      depuisSauvegarde = 0
      sauverIndex()
    }
  }
  await page.close().catch(() => undefined)
}

try {
  await Promise.all(Array.from({ length: paralleles }, ouvrier))
} finally {
  sauverIndex()
  await navigateur.close().catch(() => undefined)
  await serveur.close().catch(() => undefined)
}
process.stdout.write(`FIN ${JSON.stringify(resume)}\n`)
