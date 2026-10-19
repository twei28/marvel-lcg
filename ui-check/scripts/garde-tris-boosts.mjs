// TRIS_CAPTURE=1 vitest run src/board/CartouchePhase.test.tsx dans ui-app,
// puis node scripts/garde-tris-boosts.mjs dans ui-check, après le build.
// Mesure le contenu réel : cacher un débordement ne fait pas passer ce garde.
import { chromium } from '@playwright/test'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
const assets = path.join(root, 'ui-app/dist/assets')
const css = fs.readdirSync(assets).filter(f => f.endsWith('.css')).map(f => fs.readFileSync(path.join(assets, f), 'utf8')).join('\n')
const browser = await chromium.launch()
try {
  const page = await browser.newPage()
  await page.route('**/*', r => r.fulfill({ status: 404, body: '' }))
  await page.route('**/public/fonts/**', r => r.fulfill({ body: fs.readFileSync(path.join(root, 'Fusion/marvel-lcg-src/public/fonts', path.basename(new URL(r.request().url()).pathname))), contentType: 'font/ttf' }))
  let count = 0
  for (const [width, height] of [[1000, 600], [1280, 720], [1920, 1080]]) {
    await page.setViewportSize({ width, height })
    for (const theme of ['normal', 'epure']) {
      for (const scene of ['boost-premier', 'boost-second', 'attaque']) {
        const html = fs.readFileSync(path.join(os.tmpdir(), `tris-${scene}.html`), 'utf8')
        await page.setContent(`<html class="phase-tris" data-affichage="${theme === 'epure' ? 'sobre' : 'normal'}" ${theme === 'epure' ? 'data-epure' : ''}><base href="http://tris.local/"><style>${css}</style><style>*,*::before,*::after{animation:none!important;transition:none!important}</style><body class="phase-essai-colonne">${html}</body></html>`)
        await page.evaluate(() => document.fonts.ready)
        const measure = await page.evaluate(() => {
          const section = document.querySelector('.deroule-phase')
          const body = section.querySelector('.deroule-corps')
          const b = body.getBoundingClientRect(), s = section.getBoundingClientRect()
          const cut = [...body.querySelectorAll('*')].filter(e => !e.closest('.scan-fallback')).some(e => {
            const r = e.getBoundingClientRect()
            return r.width && r.height && (r.top < b.top - 2 || r.bottom > b.bottom + 2 || r.left < b.left - 2 || r.right > b.right + 2)
          })
          const buttonsOutside = [...section.querySelectorAll('button')].some(e => {
            const r = e.getBoundingClientRect()
            return r.width && r.height && (r.top < 0 || r.bottom > innerHeight || r.left < 0 || r.right > innerWidth)
          })
          return { overflow: body.scrollHeight - body.clientHeight, overflowX: body.scrollWidth - body.clientWidth, cut, buttonsOutside, outside: s.top < 0 || s.bottom > innerHeight }
        })
        if (measure.overflow > 2 || measure.overflowX > 2 || measure.cut || measure.buttonsOutside || measure.outside) {
          const capture = path.join(os.tmpdir(), `tris-debordement-${scene}-${theme}-${width}.png`)
          await page.screenshot({ path: capture })
          throw Error(`${scene} ${theme} ${width}×${height}: ${JSON.stringify(measure)} — ${capture}`)
        }
        count++
      }
    }
  }
  console.log(`OK : ${count} écrans de deux boosts, aucun défilement ni contenu coupé.`)
} finally { await browser.close() }
