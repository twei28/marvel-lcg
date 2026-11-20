// Rend chaque type avec les MEMES nombres que le releve de reference (`mesurer-nombres.mjs`) : le contenu est relu dans le .json.
//   node rendre-nombres.mjs <dossier avec ref-nombres/> [types...]   -> <dossier>/mine-nombres/<type>.png
import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
import fs from 'node:fs'
const S = process.argv[2]; const ids = process.argv.slice(3)
const types = JSON.parse(fs.readFileSync(S + '/types-options.json', 'utf8')).map((x) => x[0])
const CHAMP = { 'attachmentatknums cost': 'atkAttache', 'attachmentschnums cost': 'schAttache', startingthreatwrap: 'menaceDepart', 'paycost cost': 'cout', 'thw sch cost': 'thw', 'atk cost': 'atk', 'def cost': 'def', 'rec cost': 'rec', 'hp cost': 'pv', 'targetthreat cost': 'menaceCible' }
function contenuDe(rows) {
  const c = {}
  for (const r of rows) {
    const champ = CHAMP[r.cls]; if (!champ || r.y < -5000) continue
    const fils = rows.filter((x) => x.parent === r.i)
    const num = fils.find((x) => x.tag === 'SPAN' || x.cls === 'startingthreat')
    c[champ] = (num?.text ?? r.text ?? '')
    c[champ + 'Etoile'] = fils.some((x) => x.tag === 'CODE')
  }
  const vis = (cls) => rows.find((x) => x.cls === cls && x.y > -5000)
  c.tailleMain = rows.find((x) => x.cls === 'handsize' && x.y > -5000)?.text ?? ''
  c.etape = vis('villainstagenew')?.text ?? ''
  c.acceleration = vis('acceleration')?.text ?? ''
  c.phaseNumero = vis('mainschemephasenumber')?.text ?? ''
  c.phaseLettre = vis('mainschemephaseletter')?.text ?? ''
  c.renforts = rows.filter((x) => /^boost\d boosticon/.test(x.cls) && x.y > -5000).length
  c.renfortEtoile = !!vis('booststar on')
  c.ressources = [1, 2, 3].map((k) => (vis('resource' + k)?.style.backgroundImage.match(/resource-(\w+)\.png/) ?? [])[1] ?? '')
  for (const [cls, champ] of [['thwconsequential', 'thwConseq'], ['atkconsequential', 'atkConseq']]) {
    const r = rows.find((x) => x.cls === cls && x.y > -5000)
    c[champ] = r ? (rows.find((x) => x.parent === r.i && x.tag === 'CODE')?.text ?? '').length : 0
  }
  return c
}
fs.mkdirSync(S + '/mine-nombres', { recursive: true })
const b = await chromium.launch(); const p = await (await b.newContext()).newPage()
const err = []; p.on('pageerror', (e) => err.push(String(e))); p.on('console', (m) => m.type() === 'error' && err.push(m.text()))
await p.goto('http://127.0.0.1:8765/_essai/essai.html'); await p.waitForFunction(() => window.prete, null, { timeout: 20000 })
for (const t of (ids.length ? ids : types)) {
  const rows = JSON.parse(fs.readFileSync(`${S}/ref-nombres/${t}.json`, 'utf8'))
  const TETE = ['ally', 'alter-ego', 'event', 'identity', 'alter-ego-promo', 'identity-promo', 'generic-promo-vert'] // tete visible par defaut sur la reference
  const url = await p.evaluate(([id, extra, opts]) => window.rendre(id, extra, opts), [t, contenuDe(rows), { tete: TETE.includes(t) ? {} : null }])
  fs.writeFileSync(`${S}/mine-nombres/${t}.png`, Buffer.from(url.split(',')[1], 'base64'))
}
console.log('rendus', ids.length || types.length, '| erreurs:', err.join(' | ') || 'aucune')
await b.close()
