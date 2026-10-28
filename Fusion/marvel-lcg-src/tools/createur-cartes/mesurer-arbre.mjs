// Releve en arbre : boite SANS transformation de chaque element de #card1 + sa propre matrice et son origine.
import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
import fs from 'node:fs'
const S = process.argv[2]
const types = JSON.parse(fs.readFileSync(S + '/types-options.json', 'utf8')).map((x) => x[0])
const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1700, height: 1100 } })).newPage()
await p.goto('https://champions-card-maker.pages.dev/', { waitUntil: 'networkidle' }); await p.waitForTimeout(3000)
const out = {}
for (const t of types) {
  await p.selectOption('#card1selectTypeValue', t); await p.waitForTimeout(1100)
  out[t] = await p.evaluate(() => {
    const card = document.querySelector('#card1')
    const props = ['fontFamily','fontSize','fontWeight','fontStyle','color','textAlign','lineHeight','letterSpacing','textShadow','webkitTextStroke','textTransform','fontVariant','opacity','mixBlendMode','whiteSpace','justifyContent','alignItems','flexDirection','display','writingMode','textOrientation','paddingTop','paddingRight','paddingBottom','paddingLeft','backgroundColor','zIndex','textIndent','wordSpacing','overflow','clipPath','content','filter','backgroundImage']
    const all = [card, ...card.querySelectorAll('*')]
    // 1. etat d'origine : matrice propre + origine
    const info = all.map((e) => { const cs = getComputedStyle(e); return { tr: cs.transform, org: cs.transformOrigin, rot: cs.rotate, scl: cs.scale, trn: cs.translate } })
    // 2. neutralise les transformations de tout l'arbre ET du cadre (la rotation des cartes paysage)
    const frame = card.closest('.cardinnerframe')
    const neutres = [...all, frame].filter(Boolean)
    for (const e of neutres) for (const q of ['transform', 'rotate', 'scale', 'translate']) e.style.setProperty(q, 'none', 'important')
    const cr = card.getBoundingClientRect(); const k = 1500 / cr.width
    const rows = all.map((e, i) => {
      const r = e.getBoundingClientRect(); const cs = getComputedStyle(e)
      const row = { i, parent: e === card ? -1 : all.indexOf(e.parentElement), tag: e.tagName, cls: (typeof e.className === 'string' ? e.className : '').replace(/mce-content-body|editable/g, '').replace(/\s+/g, ' ').trim(),
        x: +((r.left - cr.left) * k).toFixed(1), y: +((r.top - cr.top) * k).toFixed(1), w: +(r.width * k).toFixed(1), h: +(r.height * k).toFixed(1),
        tr: info[i].tr, org: info[i].org, rot: info[i].rot, scl: info[i].scl, trn: info[i].trn, vis: cs.display !== 'none' && cs.visibility !== 'hidden' }
      row.style = {}; for (const pr of props) row.style[pr] = cs[pr]
      const tx = [...e.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join(' ').trim(); if (tx) row.text = tx
      if (e.tagName === 'IMG') row.src = (e.getAttribute('src') || '').startsWith('data:') ? 'data' : e.getAttribute('src')
      return row
    })
    for (const e of neutres) for (const q of ['transform', 'rotate', 'scale', 'translate']) e.style.removeProperty(q)
    return { attrs: Object.fromEntries([...card.attributes].map((a) => [a.name, a.value])), rows, paysage: !!frame?.classList.contains('rotate') }
  })
  console.log(t, out[t].rows.length, 'noeuds', out[t].paysage ? '(paysage)' : '')
}
fs.writeFileSync(S + '/arbre.json', JSON.stringify(out))
await b.close()
