// Rend tous les types dans une langue : node rendre-langue.mjs <dossier> <fr|en>  -> <dossier>/langue-<l>/<type>.png
import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
import fs from 'node:fs'
const [S, L = 'fr'] = process.argv.slice(2)
const types = JSON.parse(fs.readFileSync(S + '/types-options.json', 'utf8')).map((x) => x[0])
fs.mkdirSync(`${S}/langue-${L}`, { recursive: true })
const b = await chromium.launch(); const p = await (await b.newContext()).newPage()
const err = []; p.on('pageerror', (e) => err.push(String(e)))
await p.goto('http://127.0.0.1:8765/_essai/essai.html'); await p.waitForFunction(() => window.prete)
for (const t of types) {
  const url = await p.evaluate(([id, l]) => window.rendre(id, { langue: l }, { tete: null }), [t, L])
  fs.writeFileSync(`${S}/langue-${L}/${t}.png`, Buffer.from(url.split(',')[1], 'base64'))
}
console.log('ok', err.join('|')); await b.close()
