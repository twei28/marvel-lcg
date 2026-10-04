// VERIFICATION PONCTUELLE (04/10/2026) : deux corrections de contraste de
// styles/teinte.css, sur table CLAIRE : le bouton actif `.mode-actions`
// (Reglages) et `.pile-vide`. Moteur d'ESSAI seulement (cree une partie).
import { test, expect } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const SORTIE = process.env.SORTIE_CAPTURES || path.resolve('captures-tmp');

test('table claire : bouton actif des Reglages et piles vides lisibles', async ({ page, request }) => {
  test.setTimeout(240_000);
  fs.mkdirSync(SORTIE, { recursive: true });
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const deck = await (await request.get('/get_hero_json?spider_man')).json();
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(deck)], rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
  await page.setViewportSize({ width: 1600, height: 900 });
  for (const [nom, valeur] of [['gris-clair', '200,6,60'], ['sable-clair', '40,14,52']]) {
    await page.addInitScript((v) => {
      try { localStorage.setItem('mc_affichage_v1', 'normal'); localStorage.setItem('mc_teinte_v1', v); } catch { /* */ }
    }, valeur);
    await page.goto('/app/board.html', { waitUntil: 'networkidle' });
    await expect(page.getByRole('button', { name: /^Garder ma main/ }).first()).toBeVisible({ timeout: 30_000 });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(SORTIE, `contraste-${nom}-table.png`) });
    const pile = page.locator('.pile-vide').first();
    if (await pile.count()) await pile.screenshot({ path: path.join(SORTIE, `contraste-${nom}-pile-vide.png`) });
    await page.getByRole('button', { name: /Plus d'options/ }).first().click();
    await page.getByRole('button', { name: /Réglages/ }).first().click();
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(SORTIE, `contraste-${nom}-reglages.png`) });
    const groupe = page.locator('.mode-actions').first();
    await groupe.screenshot({ path: path.join(SORTIE, `contraste-${nom}-mode-actions.png`) });
    // Le texte du bouton actif contre son fond : mesure, pas seulement l'oeil.
    const couleurs = await groupe.locator('[aria-pressed="true"], .est-actif, .actif').first().evaluate((n) => {
      const s = getComputedStyle(n); return { texte: s.color, fond: s.backgroundColor };
    }).catch(() => undefined);
    console.log(nom, 'bouton actif', JSON.stringify(couleurs));
  }
});
