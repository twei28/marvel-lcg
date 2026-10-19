// T4 (19/10/2026) : « Fin du tour » n'est jamais recouvert (ni par la zone des manigances annexes ni par rien d'autre)
// à 844×390, 1050×480, 390×844 portrait, tablette et PC ; les boutons de la barre font ≥ 44 px quand le pointeur est tactile.
import { test, expect } from '@playwright/test'
import { commandes, creerPartie, jusquAuTourJoueur, reglagesSurTable } from '../pilote-corrections'

test.skip(!process.env.UI_CHECK_BASE || /:2345\/?$/.test(process.env.UI_CHECK_BASE), 'moteur de test séparé requis')

const ecrans = [
  { nom: 'pc', width: 1280, height: 720, tactile: false },
  { nom: 'tablette', width: 1180, height: 820, tactile: true },
  { nom: 'paysage-1050', width: 1050, height: 480, tactile: true },
  { nom: 'paysage-844', width: 844, height: 390, tactile: true },
  { nom: 'portrait-390', width: 390, height: 844, tactile: true },
]

for (const ecran of ecrans) {
  test(`« Fin du tour » reçoit le clic — ${ecran.nom}`, async ({ browser }, info) => {
    test.setTimeout(150_000)
    const ctx = await browser.newContext({ viewport: { width: ecran.width, height: ecran.height }, hasTouch: ecran.tactile, isMobile: ecran.tactile, baseURL: process.env.UI_CHECK_BASE })
    await reglagesSurTable(ctx)
    const page = await ctx.newPage()
    await creerPartie(page.request)
    await page.goto('/app/board.html?phase=sur-table')
    await jusquAuTourJoueur(page, page.request)
    await commandes(page.request, ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01109')", "Puzzle.PutIntoPlay('01125')", "Puzzle.PutIntoPlay('01151')"])
    await page.waitForTimeout(1200)
    const m = await page.evaluate(() => {
      const visible = (b: Element) => b.getBoundingClientRect().width > 0 && b.getBoundingClientRect().height > 0
      const mesure = (b: Element) => {
        const r = b.getBoundingClientRect()
        const e = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2)
        return { texte: (b.textContent ?? '').trim().slice(0, 24), x: r.x, y: r.y, w: r.width, h: r.height, recu: e === b || b.contains(e), couvertPar: e?.closest('[class]')?.className?.toString().slice(0, 60) ?? '' }
      }
      const fin = [...document.querySelectorAll('button')].filter((b) => /Fin du tour/.test(b.textContent ?? '') && visible(b)).map(mesure)
      const barre = document.querySelector('.plateau-barre')?.getBoundingClientRect()
      const boutons = [...document.querySelectorAll('.plateau-barre button')].filter(visible).map(mesure)
      return { fin, boutons, barre: barre ? { y: barre.y, b: barre.bottom } : null, coarse: matchMedia('(pointer: coarse)').matches, portrait: innerWidth < 641 }
    })
    await page.screenshot({ path: (process.env.CAPTURES_DIR ? process.env.CAPTURES_DIR + '/' : '') + `t4-test-${ecran.nom}.png` })
    info.annotations.push({ type: 'mesures', description: JSON.stringify(m.fin) })
    expect(m.fin.length, '« Fin du tour » visible').toBeGreaterThan(0)
    for (const f of m.fin) expect(f.recu, `« Fin du tour » (${Math.round(f.x)},${Math.round(f.y)}) recouvert par ${f.couvertPar}`).toBe(true)
    if (m.coarse) {
      for (const f of m.fin) expect(f.h, 'hauteur de « Fin du tour » au toucher').toBeGreaterThanOrEqual(44)
      if (!m.portrait) for (const b of m.boutons) {
        expect(b.h, `cible tactile « ${b.texte} »`).toBeGreaterThanOrEqual(44)
        expect(b.w, `cible tactile « ${b.texte} »`).toBeGreaterThanOrEqual(44)
      }
    }
    if (!m.portrait && m.barre) {
      // aucune seconde ligne : tous les boutons de la barre restent dans la barre
      for (const b of m.boutons) expect(b.y + b.h, `« ${b.texte} » reste dans la barre`).toBeLessThanOrEqual(m.barre.b + 1)
      for (const b of m.boutons) expect(b.recu, `« ${b.texte} » reçoit le clic`).toBe(true)
    }
    await ctx.close()
  })
}
