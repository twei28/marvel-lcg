// Releve les NOMBRES des cartes sur le Card Maker de Landstander : remplit TOUS les champs de nombres / etoiles / renforts /
// ressources (valeurs de VAL ci-dessous), capture la carte a 1500 px de large et sort l'arbre complet (boites sans transformation,
// styles) de chaque type. `ETOILE=0` : memes valeurs sans etoiles (pour mesurer l'effet de l'etoile).
//   node mesurer-nombres.mjs <dossier-sortie> [types...]      -> <dossier>/ref-nombres/<type>.png + .json
import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
import fs from 'node:fs'
const [S, ...ids] = process.argv.slice(2)
const ETOILE = process.env.ETOILE !== '0'
const SUF = process.env.SUFFIXE ?? ''
const types = ids.length ? ids : JSON.parse(fs.readFileSync(S + '/types-options.json', 'utf8')).map((x) => x[0])
const VAL = [[/^Cost$/, '3'], [/THW\/SCH value/, '2'], [/ATK value/, '3'], [/DEF value/, '2'], [/REC value/, '4'], [/HP value/, '12'], [/Starting threat\s*$/, '5'], [/Target threat/, '7'], [/Acceleration/, '2'], [/phase number/, '1'], [/Hand size/, '5'], [/Attachment ATK/, '2'], [/Attachment SCH/, '3'], [/Villain stage/, 'II'], [/Overwrite card type/, ''], [/^Subtitle/, '']]
const b = await chromium.launch()
fs.mkdirSync(`${S}/ref-nombres${SUF}`, { recursive: true })
for (const type of types) {
  // une page neuve par type : la rotation des cartes paysage ne se remet pas bien d'un type a l'autre
  const p = await (await b.newContext({ viewport: { width: 1700, height: 1100 }, deviceScaleFactor: 1500 / 676 })).newPage()
  await p.goto('https://champions-card-maker.pages.dev/', { waitUntil: 'networkidle' }); await p.waitForTimeout(2500)
  await p.selectOption('#card1selectTypeValue', type); await p.waitForTimeout(1600)
  // libelle d'un champ = dernier texte non vide qui le precede
  const champs = await p.evaluate(() => [...document.querySelectorAll('input:not([type=checkbox]):not([type=range]):not([type=file]):not([type=number]),select')].map((e, i) => {
    if (!e.offsetWidth) return null
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let last = ''; let n
    while ((n = w.nextNode())) { if (n.compareDocumentPosition(e) & 4 && n.textContent.trim() && n.parentElement.offsetWidth && !n.parentElement.closest('option,select,script,style')) last = n.textContent.trim() }
    return { i, tag: e.tagName, lab: last, star: e.dataset.starfor || '', opts: e.tagName === 'SELECT' ? [...e.options].map((o) => o.text.trim()).join(',') : '' }
  }).filter(Boolean))
  const tous = p.locator('input:not([type=checkbox]):not([type=range]):not([type=file]):not([type=number]),select')
  let res = 0
  for (const c of champs) {
    const el = tous.nth(c.i)
    if (c.tag === 'SELECT') {
      if (c.star && ETOILE) await el.selectOption({ index: 1 })
      else if (/^0,1,2,3,4,5$/.test(c.opts)) await el.selectOption({ index: ETOILE ? 2 : 0 })
      else if (/^0,1$/.test(c.opts)) await el.selectOption({ index: 1 })
      else if (/^none,energy,mental,physical,wild$/.test(c.opts)) await el.selectOption({ index: 1 + (res++ % 3) })
      continue
    }
    const v = VAL.find(([re]) => re.test(c.lab))
    if (v && v[1] !== '') { await el.fill(v[1]); await el.press('Enter') }
  }
  await p.waitForTimeout(900)
  await (await p.$('#card1')).screenshot({ path: `${S}/ref-nombres${SUF}/${type}.png` })
  const rows = await p.evaluate(() => {
    const card = document.querySelector('#card1'); const frame = card.closest('.cardinnerframe')
    const all = [card, ...card.querySelectorAll('*')]
    const neutres = [...all, frame].filter(Boolean)
    const info = all.map((e) => { const cs = getComputedStyle(e); return { rot: cs.rotate, scl: cs.scale, trn: cs.translate, tr: cs.transform, org: cs.transformOrigin } })
    for (const e of neutres) for (const q of ['transform', 'rotate', 'scale', 'translate']) e.style.setProperty(q, 'none', 'important')
    const cr = card.getBoundingClientRect(); const k = 1500 / cr.width
    const props = ['fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'color', 'textAlign', 'lineHeight', 'letterSpacing', 'textShadow', 'webkitTextStroke', 'paintOrder', 'display', 'justifyContent', 'alignItems', 'content', 'backgroundImage', 'backgroundSize', 'backgroundPosition', 'opacity', 'zIndex', 'whiteSpace', 'textTransform', 'marginTop', 'marginLeft', 'top', 'left', 'position']
    return all.map((e, i) => {
      const r = e.getBoundingClientRect(); const cs = getComputedStyle(e)
      const row = { i, parent: e === card ? -1 : all.indexOf(e.parentElement), tag: e.tagName, cls: (typeof e.className === 'string' ? e.className : '').replace(/mce-content-body|editable/g, '').replace(/\s+/g, ' ').trim(),
        x: +((r.left - cr.left) * k).toFixed(1), y: +((r.top - cr.top) * k).toFixed(1), w: +(r.width * k).toFixed(1), h: +(r.height * k).toFixed(1),
        ...info[i], vis: cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0, filtre: /codeshadow/.test(cs.filter) ? 'codeshadow' : cs.filter.slice(0, 60) }
      row.style = {}; for (const pr of props) row.style[pr] = cs[pr]
      const tx = [...e.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join(' ').trim(); if (tx) row.text = tx
      if (e.tagName === 'IMG') row.src = (e.getAttribute('src') || '').slice(0, 80)
      return row
    }).filter((r) => r.vis)
  })
  fs.writeFileSync(`${S}/ref-nombres${SUF}/${type}.json`, JSON.stringify(rows))
  console.log(type, rows.length, 'noeuds')
  await p.close()
}
await b.close()
