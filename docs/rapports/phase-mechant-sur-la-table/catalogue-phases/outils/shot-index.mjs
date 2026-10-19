import { chromium } from '/home/oem/Desktop/Marvel LCG/ui-check/node_modules/playwright/index.mjs'
const b = await chromium.launch()
const url = 'file:///home/oem/Desktop/Marvel%20LCG/docs/rapports/phase-mechant-sur-la-table/catalogue-phases/index.html'
for (const [n, w, h] of [['pc', 1280, 900], ['mob', 390, 844]]) {
  const p = await b.newPage({ viewport: { width: w, height: h } })
  const errs = []; p.on('pageerror', (e) => errs.push(String(e))); p.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()) })
  await p.goto(url); await p.waitForTimeout(1500)
  await p.screenshot({ path: `out/idx-${n}-top.png` })
  await p.evaluate(() => window.scrollTo({top: document.querySelector('#s04').offsetTop - 70, behavior: 'instant'}))
  await p.waitForTimeout(800)
  await p.screenshot({ path: `out/idx-${n}-s04.png` })
  await p.evaluate(() => window.scrollTo({top: document.querySelector('#ergo').offsetTop - 70, behavior: 'instant'}))
  await p.waitForTimeout(800)
  await p.screenshot({ path: `out/idx-${n}-ergo.png` })
  const hscroll = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)
  console.log(n, 'defilement horizontal:', hscroll, 'erreurs:', errs.slice(0, 3), 'figures', await p.locator('figure').count())
  if (n === 'pc') { await p.click('button[data-f="mobile"]'); console.log('mobile visibles', await p.locator('figure:not(.masque)').count()) ; await p.click('button[data-f="tablette"]'); console.log('tablette visibles', await p.locator('figure:not(.masque)').count()) }
  await p.close()
}
await b.close()
