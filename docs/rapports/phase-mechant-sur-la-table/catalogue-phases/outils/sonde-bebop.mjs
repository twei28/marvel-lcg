import * as L from './lib.mjs'
await L.nouvellePartie({ scenario: 'bebop_rocksteady' })
const { browser, ctx } = await L.contexte()
const page = await L.ouvrir(ctx)
await L.attendreTourJoueur([page])
await L.cmd(["Puzzle.ChangeForm('01001b')"])
await page.getByRole('button', { name: /Fin du tour/ }).first().click()
for (let i = 0; i < 60; i++) { await L.sleep(700); const s = await L.signature(page); console.log(i, (await L.monde()).phase, s.bandeau.slice(0, 90), '|', s.demande.slice(0, 90), s.lecture); await page.screenshot({ path: `${L.OUT}/zz-bebop-${i}.png` }); if (!s.question && !s.lecture && !s.bandeau) { await L.prepa(page, true) } else if (s.demande) { const b = page.locator('.demande-centrale button:visible'); console.log('btns', await b.count(), await b.allTextContents()); await L.prepa(page, true) } else if (s.question) await L.prepa(page); else if (s.lecture==='lecture') await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click().catch(()=>{}); else await page.evaluate(() => document.querySelector('.tsm-acteur:not([disabled])')?.click()) }
await browser.close()
