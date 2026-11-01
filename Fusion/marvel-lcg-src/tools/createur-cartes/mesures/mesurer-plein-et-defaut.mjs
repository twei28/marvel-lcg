import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
import fs from 'node:fs'
const S = process.argv[2]; const PLEIN = process.argv[3] === 'plein'; const SUF = PLEIN ? '-plein' : ''
const types = JSON.parse(fs.readFileSync(S + '/types-options.json', 'utf8')).map((x) => x[0])
const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1700, height: 1100 } })).newPage()
await p.goto('https://champions-card-maker.pages.dev/', { waitUntil: 'networkidle' }); await p.waitForTimeout(3000)
const out = {}
for (const t of types) {
  await p.selectOption('#card1selectTypeValue', t); await p.waitForTimeout(1200)
  if (PLEIN) {
    await p.evaluate(() => {
      const VAL = [[/^Cost$/, '3'], [/THW\/SCH value/, '2'], [/ATK value/, '3'], [/DEF value/, '2'], [/REC value/, '3'], [/HP value/, '12'], [/Starting threat\s*$/, '5'], [/Target threat/, '7'], [/Acceleration/, '2'], [/phase number/, '1'], [/Hand size/, '5'], [/Attachment ATK value/, '2'], [/Attachment SCH value/, '3'], [/^Subtitle/, 'Sous-titre'], [/^Overwrite card type/, 'ALLIE']]
      const fire = (e) => { for (const t of ['input', 'change', 'keyup']) e.dispatchEvent(new Event(t, { bubbles: true })) }
      for (const e of document.querySelectorAll('#card1controls input[type=text], #card1controls select')) {
        if (!(e.offsetWidth || e.offsetHeight)) continue
        if (e.id === 'card1selectTypeValue' || e.id === 'colorscheme') continue
        const lab = (e.closest('tr, div, label')?.innerText || '').replace(/\s+/g, ' ').trim()
        if (e.tagName === 'SELECT') {
          if (/Resource|Boost icons|Boost star|star|conseq/i.test(lab) && e.options.length > 1) { e.selectedIndex = /Boost icons/.test(lab) ? 3 : /conseq/i.test(lab) ? 2 : /Resource/.test(lab) ? Math.min(e.options.length - 1, 1 + ((lab.match(/Resource (\d)/)?.[1] | 0) % 3)) : 1; fire(e) }
          if (/Villain stage/.test(lab) && e.options.length > 1) { e.selectedIndex = 1; fire(e) }
          continue
        }
        for (const [re, v] of VAL) if (re.test(lab)) { e.value = v; fire(e); break }
      }
    })
    await p.waitForTimeout(800)
  }
  { const el0 = await p.$('#card1'); await el0.screenshot({ path: `${S}/ref${SUF}/${t}.png` }) }
  const data = await p.evaluate(() => {
    const fr = document.querySelector('#card1innerframe'); const tournee = fr.classList.contains('rotate');     const card = document.querySelector('#card1'); const cr = card.getBoundingClientRect(); const k = (tournee ? 2150 : 1500) / cr.width
    const props = ['content','backgroundImage','backgroundSize','backgroundPosition','objectFit','objectPosition','textIndent','textDecoration','textRendering','top','left','right','bottom','width','height','marginTop','marginLeft','maxWidth','position','fontStretch','wordSpacing','paintOrder','webkitTextFillColor','fontFamily','fontSize','fontWeight','fontStyle','color','textAlign','lineHeight','letterSpacing','textShadow','webkitTextStroke','textTransform','opacity','filter','mixBlendMode','transform','zIndex','clipPath','display','fontVariant','whiteSpace','padding','backgroundColor','border','borderRadius','overflow','justifyContent','alignItems','flexDirection']
    const rows = []
    const walk = (el, depth) => {
      if (depth > 4) return
      for (const c of el.children) {
        const r = c.getBoundingClientRect(); const cs = getComputedStyle(c)
        const row = { tag: c.tagName, cls: c.className && c.className.baseVal === undefined ? String(c.className).replace(/mce-content-body|editable/g, '').trim() : '', depth,
          x: Math.round((r.left - cr.left) * k), y: Math.round((r.top - cr.top) * k), w: Math.round(r.width * k), h: Math.round(r.height * k), vis: cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0 }
        if (!row.vis) { rows.push(row); continue }
        row.style = {}; for (const pr of props) row.style[pr] = cs[pr]
        if (c.tagName === 'IMG') row.src = c.getAttribute('src')?.startsWith('data:') ? 'data' : c.getAttribute('src')
        const tx = [...c.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join(' ').trim(); if (tx) row.text = tx
        rows.push(row); walk(c, depth + 1)
      }
    }
    walk(card, 0)
    const res = { tournee, w: card.offsetWidth, h: card.offsetHeight, rows, cls: card.className, attrs: Object.fromEntries([...card.attributes].map((a) => [a.name, a.value])) }
    return res
  })
  out[t] = data
  console.log(t, data.w, 'x', data.h, data.rows.filter((r) => r.vis).length, 'elements visibles')
}
fs.writeFileSync(S + '/mesures' + SUF + '.json', JSON.stringify(out))
await b.close()
