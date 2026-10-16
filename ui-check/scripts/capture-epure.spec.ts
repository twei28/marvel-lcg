// CAPTURE PONCTUELLE (16/10/2026) : chaque page en mode Epure, pour la page avant / apres.
//   ETIQUETTE=avant UI_CHECK_BASE=http://127.0.0.1:2345 npx playwright test tests/zz-capture-epure.spec.ts --project=pc
// Copie temporaire dans tests/ ; ce n'est pas une verification.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const ETIQ = process.env.ETIQUETTE || 'avant';
const SORTIE = path.resolve('captures-epure', ETIQ);
fs.mkdirSync(SORTIE, { recursive: true });

async function preparer(page: Page) {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.addInitScript(() => {
    localStorage.setItem('marvel-langue-choisie', '1');
    localStorage.setItem('mc_affichage_v1', 'epure');
  });
  await page.route('**/get_preferences*', (r) => r.fulfill({ json: {} }));
}
const photo = (page: Page, nom: string) => page.screenshot({ path: path.join(SORTIE, nom + '.png') });

test.describe.configure({ mode: 'serial' });
test.setTimeout(240_000);

test('accueil', async ({ page }) => {
  await preparer(page);
  await page.goto('/prepare.html');
  await page.waitForTimeout(2500);
  await photo(page, 'accueil');
});
test('options', async ({ page }) => {
  await preparer(page);
  await page.goto('/prepare.html');
  await page.waitForTimeout(2000);
  await page.getByText(/^Options$/).first().click({ timeout: 20000 });
  await page.waitForTimeout(1200);
  await photo(page, 'options');
});
test('selection des personnages', async ({ page }) => {
  await preparer(page);
  await page.goto('/prepare.html');
  await page.getByRole('button', { name: /^Solo/ }).first().click({ timeout: 30_000 });
  await expect(page.locator('#hero-grid .tb-port').first()).toBeVisible({ timeout: 30_000 });
  await page.locator('#hero-grid .tb-port').nth(2).hover();
  await page.waitForTimeout(800);
  await photo(page, 'selection-personnages');
});
test('campagne', async ({ page }) => {
  await preparer(page);
  await page.goto('/campagne.html');
  await page.waitForTimeout(2500);
  await photo(page, 'campagne');
});
test('editeur de deck', async ({ page }) => {
  await preparer(page);
  await page.goto('/deck-builder.html?hero=spider_man');
  await page.waitForSelector('.db-chip', { timeout: 30_000 });
  await page.waitForTimeout(1200);
  await photo(page, 'editeur-de-deck');
});
test('galerie', async ({ page }) => {
  await preparer(page);
  await page.goto('/galerie.html');
  await page.waitForTimeout(3000);
  await photo(page, 'galerie');
});
test('salon', async ({ page }) => {
  await preparer(page);
  await page.goto('/salon.html');
  await page.waitForTimeout(2500);
  await photo(page, 'salon');
});

test('plateau et modale', async ({ page, request }) => {
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const deck = await (await request.get('/get_hero_json?spider_man')).json();
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(deck)],
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
  await preparer(page);
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  await page.request.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.ChangeForm('01001b')"] } });
  await page.waitForTimeout(3000);
  await photo(page, 'modale-mise-en-place');
  const visible = async (nom: RegExp) => {
    const b = page.getByRole('button', { name: nom }).first();
    return (await b.count()) > 0 && (await b.isVisible()) ? b : undefined;
  };
  for (let i = 0; i < 40; i++) {
    await page.waitForTimeout(700);
    let agi = false;
    for (const nom of [/^Continuer/, /^Garder ma main/, /Suivant/]) {
      const b = await visible(nom);
      if (b && !(await b.isDisabled())) { await b.click({ timeout: 2000 }).catch(() => {}); agi = true; break; }
    }
    if (!agi && i > 12) break;
  }
  await page.waitForTimeout(1500);
  await photo(page, 'plateau');
  await page.getByRole('button', { name: /Réglages/ }).first().click();
  await page.waitForTimeout(800);
  await photo(page, 'reglages-plateau');
});
