// GARDE : aucune question de la boite de la phase du mechant (essai) ne rogne ses boutons ni ne
// deborde, quelle que soit sa sorte et la taille de la fenetre.
//
//   cd ui-app && npx vitest run src/board/boite-questions.pires-cas.test.tsx   (ecrit les pires cas)
//   cd ui-check && node scripts/garde-boite-questions.mjs                      (code de sortie 1 au moindre ecart)
//
// POURQUOI (13/10/2026) : une question a cinq cibles (Maitres du Chaos) rognait « Annuler » et
// « Confirmer » : la question n'avait que 308 px et les cartes, deja au minimum, ne suffisaient pas.
// Ce garde monte le VRAI HTML de chaque sorte de question (ecrit par le test des pires cas) avec la
// VRAIE feuille construite (ui-app/dist), rejoue le calage des cartes d'`essai-tailles.ts`, puis
// verifie que chaque bouton est entier et visible et que rien ne sort du corps. Les animations
// d'entree sont coupees : on mesure l'ecran au repos, pas en train de glisser.
import { chromium } from '@playwright/test'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const RACINE = path.resolve(ICI, '..', '..')
const ASSETS = path.join(RACINE, 'ui-app/dist/assets')
const POLICES = path.join(RACINE, 'Fusion/marvel-lcg-src/public/fonts')
const CAS = path.join(os.tmpdir(), 'marvel-boite-questions')
// Les zones utiles reelles (fenetre moins la barre du navigateur), pas l'ecran brut.
const TAILLES = [[1366, 657], [1440, 789], [1536, 730], [1920, 969]]

if (!fs.existsSync(CAS) || fs.readdirSync(CAS).length === 0) {
  console.error(`Aucun pire cas dans ${CAS} : lancer d'abord le test boite-questions.pires-cas.`)
  process.exit(1)
}
const css = fs.readdirSync(ASSETS).filter((f) => f.endsWith('.css')).map((f) => fs.readFileSync(path.join(ASSETS, f), 'utf8')).join('\n')
const fichiers = fs.readdirSync(CAS).filter((f) => f.endsWith('.html'))

let page = ''
const navigateur = await chromium.launch()
const ecarts = []
for (const [l, h] of TAILLES) {
  const onglet = await navigateur.newPage({ viewport: { width: l, height: h } })
  // Les vraies polices du jeu (Bangers est bien plus etroite que la police de repli) :
  // sans elles, les boutons mesures seraient plus larges qu'en partie.
  await onglet.route('http://garde.local/**', async (route) => {
    const chemin = new URL(route.request().url()).pathname
    if (chemin.startsWith('/public/fonts/')) {
      return route.fulfill({ body: fs.readFileSync(path.join(POLICES, path.basename(chemin))), contentType: 'font/ttf' })
    }
    return route.fulfill({ body: page, contentType: 'text/html' })
  })
  for (const fichier of fichiers) {
    const html = fs.readFileSync(path.join(CAS, fichier), 'utf8')
    page = `<!doctype html><meta charset=utf-8><style>${css}</style><style>*,*::before,*::after{animation:none!important;transition:none!important}</style><body class="phase-essai-colonne" style="margin:0;background:#10131c">${html}</body>`
    await onglet.goto('http://garde.local/')
    await onglet.evaluate(() => document.fonts.ready)
    const m = await onglet.evaluate(() => {
      // Meme calage qu'essai-tailles.ts : la plus grande hauteur de carte qui tient, puis le zoom.
      const section = document.querySelector('.deroule-phase')
      const corps = section.querySelector(':scope > .deroule-corps')
      const excedent = () => {
        let pire = Math.max(0, corps.scrollHeight - corps.clientHeight, corps.scrollWidth - corps.clientWidth)
        const b = corps.getBoundingClientRect()
        for (const el of corps.querySelectorAll('*')) {
          // Le banc n'a pas les images : le nom de secours d'une carte (.scan-fallback) n'existe pas en partie.
          if (el.closest('.scan-fallback')) continue
          const r = el.getBoundingClientRect()
          if (!r.width || !r.height) continue
          pire = Math.max(pire, r.bottom - b.bottom, r.right - b.right, b.top - r.top, b.left - r.left)
        }
        return Math.max(0, Math.round(pire))
      }
      const poser = (v) => section.style.setProperty('--essai-carte-h', `${v}px`)
      let hauteur = 170
      poser(hauteur)
      let meilleure = { hauteur, e: excedent() }
      while (meilleure.e > 2 && hauteur > 56) {
        hauteur = Math.max(56, Math.floor(hauteur * 0.9))
        poser(hauteur)
        const e = excedent()
        if (e < meilleure.e) meilleure = { hauteur, e }
      }
      poser(meilleure.hauteur)
      let zoom = 1
      if (meilleure.e > 2) {
        let mieux = { zoom, e: meilleure.e }
        while (mieux.e > 2 && zoom > 0.8) {
          zoom = Math.max(0.8, Math.round((zoom - 0.05) * 100) / 100)
          section.style.setProperty('--essai-zoom-corps', String(zoom))
          const e = excedent()
          if (e < mieux.e) mieux = { zoom, e }
        }
        section.style.setProperty('--essai-zoom-corps', String(mieux.zoom))
        zoom = mieux.zoom
      }
      const boite = section.getBoundingClientRect()
      const zoneCorps = corps.getBoundingClientRect()
      const rognes = []
      for (const bouton of section.querySelectorAll('button')) {
        const r = bouton.getBoundingClientRect()
        if (!r.width || !r.height) continue
        const dans = (z) => r.top >= z.top - 1 && r.bottom <= z.bottom + 1 && r.left >= z.left - 1 && r.right <= z.right + 1
        if (!dans(boite) || (corps.contains(bouton) && !dans(zoneCorps))) rognes.push((bouton.textContent || '').trim().slice(0, 30))
      }
      // Le pire element, pour savoir quoi corriger sans deviner.
      let pire = { de: 0, quoi: '' }
      const bc = corps.getBoundingClientRect()
      for (const el of corps.querySelectorAll('*')) {
          // Le banc n'a pas les images : le nom de secours d'une carte (.scan-fallback) n'existe pas en partie.
          if (el.closest('.scan-fallback')) continue
        const r = el.getBoundingClientRect()
        if (!r.width || !r.height) continue
        const de = Math.max(r.bottom - bc.bottom, r.right - bc.right, bc.top - r.top, bc.left - r.left)
        if (de > pire.de) pire = { de: Math.round(de), quoi: `${el.parentElement?.className ?? ""} > ${el.tagName.toLowerCase()}.${[...el.classList].join(".")} « ${(el.textContent || "").trim().slice(0, 30)} » ${["bas", "droite", "haut", "gauche"][[r.bottom - bc.bottom, r.right - bc.right, bc.top - r.top, bc.left - r.left].indexOf(de)]}` }
      }
      return { carte: meilleure.hauteur, zoom, excedent: excedent(), rognes, pire }
    })
    const nom = `${fichier.replace('.html', '')} @ ${l}x${h}`
    if (m.excedent > 2 || m.rognes.length > 0) {
      ecarts.push(`${nom} : excedent ${m.excedent} px (${m.pire.quoi}), boutons rognes ${JSON.stringify(m.rognes)}`)
      // Une capture de chaque ecart, a cote des pires cas, pour voir avant de corriger.
      fs.mkdirSync(path.join(CAS, 'ecarts'), { recursive: true })
      await onglet.screenshot({ path: path.join(CAS, 'ecarts', `${fichier.replace('.html', '')}-${l}x${h}.png`), clip: { x: 0, y: 0, width: Math.min(l, 640), height: h } })
    }
    else console.log(`ok  ${nom} : cartes ${m.carte} px, zoom ${m.zoom}`)
  }
  await onglet.close()
}
await navigateur.close()
if (ecarts.length > 0) {
  console.error(`ECARTS (${ecarts.length}) :\n  ${ecarts.join('\n  ')}`)
  process.exit(1)
}
console.log(`OK : ${fichiers.length} questions x ${TAILLES.length} fenetres, aucun bouton rogne, aucun debordement`)
