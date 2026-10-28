// Rend nos cartes dans les variantes de la reference (cases a cocher) pour les comparer aux captures de `sonde10.mjs`.
//   node rendre-variantes.mjs <dossier>  -> <dossier>/bas/mine-<type>-<variante>.png
import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
import fs from 'node:fs'
const S = process.argv[2]
const V = [['ally', 'etoile', { tete: { etoile: true } }], ['ally', 'sanstete', { tete: null }], ['minion', 'fissures', { fissures: false }], ['ally', 'hpstar', { tete: {}, hpStar: true }]]
const b = await chromium.launch(); const p = await (await b.newContext()).newPage()
const err = []; p.on('pageerror', (e) => err.push(String(e)))
await p.goto('http://127.0.0.1:8765/_essai/essai.html'); await p.waitForFunction(() => window.prete)
for (const [t, nom, o] of V) {
  const url = await p.evaluate(([id, extra, opts]) => window.rendre(id, extra, opts), [t, o.hpStar ? { pvEtoile: true } : {}, o])
  fs.writeFileSync(`${S}/bas/mine-${t}-${nom}.png`, Buffer.from(url.split(',')[1], 'base64'))
}
console.log('ok', err.join('|'))
await b.close()
