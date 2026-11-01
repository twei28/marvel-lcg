import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
import fs from 'node:fs'
const S = process.argv[2]; const ids = process.argv.slice(3)
const types = JSON.parse(fs.readFileSync(S + '/types-options.json', 'utf8')).map((x) => x[0])
const b = await chromium.launch(); const p = await (await b.newContext()).newPage()
const err = []; p.on('pageerror', (e) => err.push(String(e))); p.on('console', (m) => m.type() === 'error' && err.push(m.text()))
await p.goto('http://127.0.0.1:8765/_essai/essai.html'); await p.waitForFunction(() => window.prete, null, { timeout: 20000 })
for (const t of (ids.length ? ids : types)) {
  const url = await p.evaluate((id) => window.rendre(id), t)
  fs.writeFileSync(`${S}/mine/${t}.png`, Buffer.from(url.split(',')[1], 'base64'))
}
console.log('rendus', ids.length || types.length, '| erreurs:', err.join(' | ') || 'aucune')
await b.close()
