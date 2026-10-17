import { test } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

// Capture de chaque page du jeu en Épuré (outil de session, pas un test).
const SORTIE = process.env.ZZ_SORTIE ?? '/tmp/pages-epure';
const PAGES = (process.env.ZZ_PAGES ?? '').split(',').filter(Boolean);

test('pages epure', async ({ page }) => {
  test.setTimeout(600_000);
  fs.mkdirSync(SORTIE, { recursive: true });
  await page.addInitScript(() => {
    try {
      localStorage.setItem('mc_affichage_v1', 'epure');
      sessionStorage.setItem('mc_epure_permis', 'oui');
    } catch { /* rien */ }
  });
  for (const p of PAGES) {
    const nom = p.replace(/[/?=&.]+/g, '_');
    try {
      await page.goto('/' + p, { waitUntil: 'networkidle', timeout: 30_000 });
    } catch { /* on capture quand meme */ }
    await page.waitForTimeout(2500);
    const etat = await page.evaluate(() => ({ titre: document.title, epure: document.documentElement.dataset.epure ?? '', aff: document.documentElement.dataset.affichage ?? '' }));
    console.log(`PAGE ${p} | ${etat.titre} | epure=${etat.epure} aff=${etat.aff}`);
    await page.screenshot({ path: path.join(SORTIE, `${nom}.png`) });
  }
});
