import { chromium } from '/home/oem/Desktop/Marvel LCG/ui-check/node_modules/playwright/index.mjs'
import fs from 'fs'
export const BASE = process.env.BASE || 'http://127.0.0.1:2494'
export const OUT = process.env.OUT || '/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/2ed3e66d-9fcf-45e1-aa7f-2debf9a42af0/scratchpad/cat/out'
const contrat = JSON.parse(fs.readFileSync('/home/oem/Desktop/Marvel LCG/ui-check/contrat-nouvelle-partie.json', 'utf8'))
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms))
const J = async (url) => (await fetch(BASE + url)).json()
export const monde = async (p = 0) => J(`/get_world?hot_seat&p=${p}`)
export async function nouvellePartie({ scenario = 'klaw', heros = ['spider_man'], seed = 4321, extraSets = [], cmdsApres = [] } = {}) {
  const s = await J('/get_scenario_json?' + scenario)
  const charge = {
    campaign_json: JSON.stringify(s), campaign_log: {}, challenges: s.challenges ?? [],
    encounter_set_names: [...new Set([...(s.encounter_sets ?? []), ...(s.modular_sets ?? []), ...extraSets])],
    hero_json: await Promise.all(heros.map(async (h) => JSON.stringify(await J('/get_hero_json?' + h)))),
    rules: [...contrat.regles_partie_standard, 'mode_sandbox'], seed, timeout: 0,
  }
  const r = await fetch(BASE + '/new?data=' + encodeURIComponent(JSON.stringify(charge)))
  if (!r.ok) throw new Error('new ' + r.status)
}
export async function cmd(cmds, p = 0) {
  const r = await fetch(BASE + `/sandbox_command?p=${p}`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ commands: cmds }) })
  if (!r.ok) throw new Error('cmd ' + r.status + ' ' + await r.text())
  await sleep(500)
}
export async function contexte({ w = 1280, h = 720, reduit = false, tactile = false, affichage = 'epure' } = {}) {
  const browser = await chromium.launch()
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: reduit ? 'reduce' : 'no-preference', hasTouch: tactile, isMobile: tactile, deviceScaleFactor: 1 })
  await ctx.addInitScript((aff) => {
    localStorage.setItem('mc_phase_presentation', 'bis')
    localStorage.setItem('marvel-langue-choisie', '1')
    localStorage.setItem('marvel-langue', 'fr')
    localStorage.setItem('marvel-board-mode-phase-mechant', 'sur-table')
    localStorage.setItem('mc_aide_bulle_table', 'vue')
    if (aff) localStorage.setItem('mc_affichage_v1', aff)
  }, affichage)
  await ctx.addInitScript(() => { const st = document.createElement('style'); st.textContent = '.bandeau-triche{display:none!important}'; document.addEventListener('DOMContentLoaded', () => document.head.appendChild(st)) })
  return { browser, ctx }
}
const ign = (e) => { if (!/Timeout/.test(String(e))) throw e }
async function boutonVisible(page, re) {
  for (const b of await page.getByRole('button', { name: re }).all()) if (await b.isVisible() && await b.isEnabled()) return b
}
export async function prepa(page, finTour = false) {
  const mull = page.getByRole('dialog', { name: 'Résoudre les mulligans' })
  if (await mull.count()) { await mull.getByRole('button', { name: 'Annuler', exact: true }).click({ timeout: 1500 }).catch(ign); return }
  const def = page.getByRole('button', { name: /^Défausser \d/ }).first()
  if (await def.isVisible().catch(() => false) && await def.isDisabled()) {
    const main = page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/, pressed: false }).first()
    if (await main.count()) { await main.click({ timeout: 1500 }).catch(ign); return }
  }
  const val = page.locator('.plateau-selecteur-valider:not([disabled]), .tsm-bandeau .tsm-bouton:not([disabled])').filter({ hasText: /^Valider/ }).first()
  if (await val.isVisible().catch(() => false)) { await val.click({ timeout: 1500 }).catch(ign); return }
  for (const re of [/^Garder ma main/, /^Oui, garder/, /^Ne pas (défendre|utiliser|jouer)/, /(^|— )Ne pas/, /^Aucune réponse/, /^Continuer sans rien jouer/, /^Passer/, /^Confirmer$/, /(^|— )Continuer/, /^OK$/, /^Défausser \d/, /^Fin de phase/, /^Action$/]) {
    const b = await boutonVisible(page, re)
    if (b) { await b.click({ timeout: 1500 }).catch(ign); return }
  }
  const af = page.locator('.demande-centrale .af-action:visible').first()
  if (await af.count()) { await af.click({ timeout: 1500 }).catch(ign); return }
  const carte = page.locator('.plateau-selecteur.est-fenetre .plateau-selecteur-carte:not(.est-choisie)').first()
  if (await carte.isVisible().catch(() => false)) { await carte.click({ timeout: 1500 }).catch(ign); return }
  const unique = page.locator('[data-choix-unique]:visible').first()
  if (await unique.count()) { await unique.click({ timeout: 1500 }).catch(ign); return }
  if (finTour) { const fin = await boutonVisible(page, /Fin du tour/); if (fin) { await fin.click({ timeout: 1500 }).catch(ign); return } }
  const premier = page.locator('[data-choix]:visible, .tsm-utilisable:not(.est-choisie):not([disabled])').first()
  if (await premier.count()) await premier.click({ timeout: 1500 }).catch(ign)
}
export async function attendreTourJoueur(pages, max = 200) {
  for (let i = 0; i < max; i++) {
    const w = await monde()
    if (/^Player(?: \d+)? Turn$/.test(w.phase)) return w
    for (const p of pages) await prepa(p)
    await sleep(150)
  }
  throw new Error('tour joueur non atteint')
}
export async function ouvrir(ctx, p = 0, multi = false) {
  const page = await ctx.newPage()
  page.on('pageerror', (e) => console.log('PAGEERROR', String(e).slice(0, 200)))
  await page.goto(`/app/board.html?${multi ? `p=${p}&multi=1` : 'phase=sur-table'}`.replace(/^/, BASE + ''))
  return page
}
export async function signature(page) {
  return page.evaluate(() => ({
    bandeau: Array.from(document.querySelectorAll('.tsm-bandeau')).map((e) => e.textContent.trim().replace(/\s+/g, ' ')).join(' | '),
    phrase: document.querySelector('.tsm-phrase')?.textContent ?? '',
    lecture: Array.from(document.querySelectorAll('.rencontre-sur-table')).map((e) => e.getAttribute('data-lecture')).join(','),
    demande: Array.from(document.querySelectorAll('.demande-centrale')).map((e) => e.textContent.trim().replace(/\s+/g, ' ')).join(' | '),
    nSortie: document.querySelectorAll('.rencontre-sortie').length,
    boosts: document.querySelectorAll('.rencontre-sur-table .est-boost').length,
    question: !!document.querySelector('.tsm-bandeau.est-question'),
    bilan: !!document.querySelector('.tsm-bandeau.est-bilan'),
  }))
}
// Joue la phase du méchant en capturant chaque état distinct. choix(page, sig, w) peut renvoyer true pour dire qu'il a agi.
export async function phaseMechant(page, { prefere = [], prefereSel = [], tag, onState, choisir, max = 400, log = true, rafale = false, snapLecture = true } = {}) {
  const vus = new Set(); let n = 0; const journal = []
  let commencee = false
  let finDeJeu = 0
  const fin = page.getByRole('button', { name: /Fin du tour/ }).first()
  // Des invites peuvent déjà bloquer le tour joueur (ex. Rapide d'un sbire engagé) : les traiter et les capturer.
  { let np = 0; const vusPre = new Set()
    for (let k = 0; k < 120 && !(await fin.isEnabled().catch(() => false)); k++) {
      const sg = await signature(page); const c = JSON.stringify([sg.bandeau, sg.demande, sg.lecture])
      if (!vusPre.has(c) && (sg.bandeau || sg.demande || sg.lecture)) { vusPre.add(c); await sleep(sg.lecture ? 1800 : 400); np++; await page.screenshot({ path: `${OUT}/${tag}-pre-${String(np).padStart(2, '0')}.png` }); console.log(`${tag}-pre-${np}`, sg.bandeau.slice(0, 120), sg.demande.slice(0, 80), sg.lecture) }
      let fait = false
      if (sg.lecture === 'lecture') { const b = page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first(); if (await b.count()) { await b.click({ timeout: 1500 }).catch(ign); fait = true } }
      if (!fait && (sg.question || sg.demande)) for (const re of prefere) { const b = await boutonVisible(page, re); if (b) { await b.click({ timeout: 1500 }).catch(ign); fait = true; break } }
      if (!fait && !/entree|depart/.test(sg.lecture)) await prepa(page)
      await sleep(250)
    } }
  try { await fin.click({ timeout: 4000 }) } catch (e) { console.log('Fin du tour : clic bloqué, clic programmatique', tag); await page.evaluate(() => [...document.querySelectorAll('button')].find((x) => /Fin du tour/.test(x.textContent))?.click()) }
  if (rafale) for (let k = 1; k <= 4; k++) { await sleep(280); await page.screenshot({ path: `${OUT}/${tag}-ann-${k}.png` }) }
  for (let i = 0; i < max; i++) {
    const w = await monde()
    commencee ||= ['Main Scheme Place Threat', 'Enemy Activation', 'Deal Encounter Cards', 'Reveal Encounter Cards'].includes(w.phase)
    const sig = await signature(page)
    const cle = JSON.stringify([w.phase, sig.bandeau, sig.demande, sig.lecture, sig.nSortie, sig.boosts])
    if (!vus.has(cle) && (sig.bandeau || sig.lecture || sig.demande)) {
      vus.add(cle)
      await sleep(sig.lecture ? 1800 : 500)
      n++
      const nom = `${tag}-${String(n).padStart(2, '0')}`
      await page.screenshot({ path: `${OUT}/${nom}.png` })
      const info = { nom, phase: w.phase, ...sig }
      journal.push(info)
      if (log) console.log(nom, w.phase, '|', sig.phrase.slice(0, 80), '|', sig.bandeau.slice(0, 120), '|', sig.demande.slice(0,80), '|', sig.lecture)
      if (onState) await onState(page, info, w)
    }
    if (sig.bilan) { const b = page.locator('.tsm-bandeau.est-bilan .tsm-bouton'); await sleep(300); const nom = `${tag}-bilan`; await page.screenshot({ path: `${OUT}/${nom}.png` }); journal.push({ nom, bilan: true, ...sig }); await b.click(); await sleep(500); await page.screenshot({ path: `${OUT}/${tag}-retour1.png` }); await sleep(2000); await page.screenshot({ path: `${OUT}/${tag}-retour2.png` }); break }
    if (choisir && await choisir(page, sig, w)) { await sleep(150); continue }
    if ((sig.question || sig.demande) && prefere.length) {
      let fait = false
      for (const re of prefere) {
        const b = await boutonVisible(page, re)
        if (b) { await b.click({ timeout: 1500 }).catch(ign); fait = true; break }
      }
      if (!fait) for (const sel of prefereSel) { const e = page.locator(sel).first(); if (await e.count() && await e.isVisible()) { await e.click({ timeout: 1500 }).catch(ign); fait = true; break } }
      if (fait) { await sleep(200); continue }
    }
    if (sig.lecture === 'lecture') {
      const b = page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first()
      if (await b.count()) { await b.click({ timeout: 1500 }).catch(ign); await sleep(150); continue }
    }
    if (/entree|depart/.test(sig.lecture)) { await sleep(150); continue }
    if (!sig.question && !sig.bilan && !sig.lecture) {
      await page.evaluate(() => {
        if (document.querySelector('.tsm-bandeau.est-question, .tsm-bandeau.est-bilan, .rencontre-sur-table')) return
        document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton')?.click()
      })
      if (sig.demande || !sig.bandeau) await prepa(page, !commencee)
      else if (/vaincu|Continuer|défaite|victoire/i.test(sig.bandeau)) { const b = await boutonVisible(page, /^Continuer/); if (b) { await sleep(600); await page.screenshot({ path: `${OUT}/${tag}-fin.png` }); await b.click({ timeout: 1500 }).catch(ign); finDeJeu++; if (finDeJeu > 2) break } }
    } else await prepa(page, !commencee)
    await sleep(150)
  }
  return journal
}
export function trouve(w, cardId) {
  const out = []
  const walk = (o, p) => {
    if (Array.isArray(o)) o.forEach((v, i) => walk(v, `${p}[${i}]`))
    else if (o && typeof o === 'object') {
      if (o.card_id === cardId && 'game_area' in o) out.push([p, o.id, o.game_area, o.name])
      for (const [k, v] of Object.entries(o)) walk(v, p + '.' + k)
    }
  }
  walk(w, '')
  return out
}
export const zone = async (cardId) => trouve(await monde(), cardId)
