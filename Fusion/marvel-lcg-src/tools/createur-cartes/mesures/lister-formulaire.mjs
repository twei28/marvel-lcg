import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
import fs from 'node:fs'
const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1700, height: 1100 } })).newPage()
await p.goto('https://champions-card-maker.pages.dev/', { waitUntil: 'networkidle' }); await p.waitForTimeout(3000)
await p.selectOption('#card1selectTypeValue', 'ally'); await p.waitForTimeout(800)
const r = await p.evaluate(() => {
  const out = []
  for (const e of document.querySelectorAll('#card1controls input, #card1controls select, #card1controls textarea, .controls input, .controls select, .controls textarea')) {
    const lab = (e.closest('tr, div, label')?.innerText || '').replace(/\s+/g, ' ').slice(0, 60)
    out.push({ id: e.id, tag: e.tagName, type: e.type, val: (e.value || '').slice(0, 40), cls: String(e.className).slice(0, 50), lab, vis: !!(e.offsetWidth || e.offsetHeight) })
  }
  return out
})
fs.writeFileSync(process.argv[2] + '/form.json', JSON.stringify(r, null, 1))
console.log(r.length, 'controles ;', r.filter((x) => x.vis).length, 'visibles pour ally')
for (const x of r) console.log((x.vis ? '*' : ' '), x.tag, x.type, x.id.padEnd(34), JSON.stringify(x.val).padEnd(20), x.lab)
await b.close()
