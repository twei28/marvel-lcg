// Position des icones de renfort (boosts) selon leur nombre (0-3) et l'etoile, sur un type donne.
//   node mesurer-renforts.mjs <type>  -> JSON sur la sortie standard
import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
const type = process.argv[2] ?? 'sidescheme'
const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1700, height: 1100 } })).newPage()
await p.goto('https://champions-card-maker.pages.dev/', { waitUntil: 'networkidle' }); await p.waitForTimeout(2500)
await p.selectOption('#card1selectTypeValue', type); await p.waitForTimeout(1600)
// les listes 0..3 et le bouton etoile des renforts : on les repere par leurs options
const listes = await p.evaluate(() => [...document.querySelectorAll('select')].map((s, i) => ({ i, vis: !!s.offsetWidth, opts: [...s.options].map((o) => o.text.trim()).join(','), ds: JSON.stringify(s.dataset) })).filter((x) => x.vis))
console.error(JSON.stringify(listes))
const out = []
const idx = listes.find((l) => /^0,1,2,3,4,5$/.test(l.opts))
const etoile = listes.filter((l) => /^0,1$/.test(l.opts))
console.error('boost select', idx?.i, 'etoiles', etoile.map((e) => e.i))
for (const n of [0, 1, 2, 3, 4, 5]) for (const star of [0, 1]) {
  if (idx) await p.locator('select').nth(idx.i).selectOption({ index: n })
  for (const e of etoile) await p.locator('select').nth(e.i).selectOption({ index: star })
  await p.waitForTimeout(400)
  const rows = await p.evaluate(() => {
    const card = document.querySelector('#card1'); const frame = card.closest('.cardinnerframe')
    const els = [frame, ...card.querySelectorAll('*')].filter(Boolean)
    for (const e of els) for (const q of ['transform', 'rotate', 'scale', 'translate']) e.style.setProperty(q, 'none', 'important')
    const cr = card.getBoundingClientRect(); const k = 1500 / cr.width
    const r = [...card.querySelectorAll('.boosts, .boosts *')].map((e) => { const b = e.getBoundingClientRect(); const cs = getComputedStyle(e); return { cls: String(e.className), x: +((b.left - cr.left) * k).toFixed(1), y: +((b.top - cr.top) * k).toFixed(1), w: +(b.width * k).toFixed(1), h: +(b.height * k).toFixed(1), vis: cs.display !== 'none' && b.width > 0 } })
    for (const e of els) for (const q of ['transform', 'rotate', 'scale', 'translate']) e.style.removeProperty(q)
    return r.filter((x) => x.vis)
  })
  out.push({ n, star, rows })
}
console.log(JSON.stringify(out))
await b.close()
