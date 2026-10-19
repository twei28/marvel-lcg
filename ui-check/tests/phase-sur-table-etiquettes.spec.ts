// T1 (19/10/2026) : les étiquettes « Défendre avec … » ont EXACTEMENT la largeur de leur carte,
// ne se chevauchent pas et ne cachent pas la barre de PV, avec 1, 2 et 3 alliés, sur quatre formats d'écran.
import { test, expect } from '@playwright/test'
import { avancerJusqua, commandes, creerPartie, finDuTour, jusquAuTourJoueur, reglagesSurTable } from '../pilote-corrections'

test.skip(!process.env.UI_CHECK_BASE || /:2345\/?$/.test(process.env.UI_CHECK_BASE), 'moteur de test séparé requis')

const ecrans = [
  { nom: 'pc', width: 1280, height: 720, tactile: false },
  { nom: 'tablette', width: 1180, height: 820, tactile: true },
  { nom: 'paysage', width: 1050, height: 480, tactile: true },
  { nom: 'paysage-844', width: 844, height: 390, tactile: true },
]
const allies = ["Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01068', under_control=True)", "Puzzle.PutIntoPlay('01075', under_control=True)"]

for (const ecran of ecrans) for (const n of [1, 2, 3]) {
  test(`étiquettes de défense — ${ecran.nom}, ${n} allié(s)`, async ({ browser }, info) => {
    test.setTimeout(180_000)
    const ctx = await browser.newContext({
      viewport: { width: ecran.width, height: ecran.height },
      hasTouch: ecran.tactile, isMobile: ecran.tactile, reducedMotion: 'no-preference', baseURL: process.env.UI_CHECK_BASE,
    })
    await reglagesSurTable(ctx)
    const page = await ctx.newPage()
    await creerPartie(page.request)
    await page.goto('/app/board.html?phase=sur-table')
    await jusquAuTourJoueur(page, page.request)
    await commandes(page.request, ["Puzzle.ChangeForm('01001b')", ...allies.slice(0, n)])
    await finDuTour(page)
    await avancerJusqua(page, (b) => /Qui défend/.test(b))
    await expect(page.locator('.tsm-etiquette')).toHaveCount(n + 1)
    await page.waitForTimeout(600)
    const m = await page.evaluate(() => {
      const R = (e: Element) => e.getBoundingClientRect()
      const et = [...document.querySelectorAll('.tsm-etiquette')]
      const ca = [...document.querySelectorAll('.tsm-utilisable')]
      const chevauchements: string[] = []
      for (let i = 0; i < et.length; i++) for (let j = i + 1; j < et.length; j++) {
        const a = R(et[i]!), b = R(et[j]!)
        const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left), oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top)
        if (ox > 0.5 && oy > 0.5) chevauchements.push(`${i}/${j}: ${ox.toFixed(1)}px`)
      }
      const lignes = et.map((e, i) => {
        const a = R(e), c = R(ca[i]!)
        // la barre de PV de la carte : l'étiquette ne doit pas la recouvrir
        const carte = ca[i]!
        const centre = { x: c.left + c.width / 2, y: a.top + 1 }
        return { nom: e.textContent, wEtiquette: a.width, wCarte: c.width, haut: a.top, basCarte: c.bottom, dessusPV: a.top < c.bottom - 0.5, visible: a.left >= 0 && a.right <= innerWidth && a.bottom <= innerHeight + 1, centre, carteId: carte.getAttribute('aria-label') }
      })
      return { chevauchements, lignes }
    })
    await page.screenshot({ path: info.outputPath(`etiquettes-${ecran.nom}-${n}.png`) })
    info.annotations.push({ type: 'mesures', description: JSON.stringify(m.lignes.map((l) => [l.nom, Math.round(l.wEtiquette * 10) / 10, Math.round(l.wCarte * 10) / 10])) })
    expect(m.chevauchements, 'aucun recouvrement entre étiquettes voisines').toEqual([])
    for (const l of m.lignes) {
      expect(l.wEtiquette, `largeur de l'étiquette « ${l.nom} »`).toBeLessThanOrEqual(l.wCarte + 0.6)
      expect(l.wEtiquette, `largeur de l'étiquette « ${l.nom} »`).toBeGreaterThanOrEqual(l.wCarte - 0.6)
      expect(l.dessusPV, `l'étiquette « ${l.nom} » commence sous l'image de la carte`).toBe(false)
    }
    await ctx.close()
  })
}
