// CAPTURE PONCTUELLE (16/10/2026) : le gris du mode Epure a plusieurs niveaux, pour choisir.
// Les jetons sont poses en ligne sur <html> (ils passent devant la feuille). Ce n'est pas une verification.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const hex = (n: number) => '#' + [n, n + 2, n + 7].map((v) => Math.min(255, v).toString(16).padStart(2, '0')).join('');
// Niveau 0 = actuel (fond 196). Chaque niveau retire 9 points de clarte.
const NIVEAUX = [0, 1, 2, 3, 4, 5].map((i) => {
  const fond = 196 - 9 * i, surface = 214 - 9 * i, champ = 236 - 9 * i;
  return { i, fond: hex(fond), surface: hex(surface), champ: hex(champ), bord: hex(152 - 9 * i), fort: hex(108 - 7 * i), soft: hex(188 - 9 * i) };
});
const SORTIE = path.resolve('captures-epure', 'niveaux');
fs.mkdirSync(SORTIE, { recursive: true });

async function preparer(page: Page) {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.addInitScript(() => {
    localStorage.setItem('marvel-langue-choisie', '1');
    localStorage.setItem('mc_affichage_v1', 'epure');
  });
  await page.route('**/get_preferences*', (r) => r.fulfill({ json: {} }));
}
/** Les jetons, poses par une feuille `!important` apres chaque navigation (une feuille en ligne
    sur <html> etait effacee par la page). */
async function teinter(page: Page, n: (typeof NIVEAUX)[number]) {
  const v: Record<string, string> = {
    '--ep-fond': n.fond, '--ep-surface': n.surface, '--ep-champ': n.champ, '--ep-bord': n.bord, '--ep-bord-fort': n.fort,
    '--ink': n.fond, '--ink2': n.surface, '--steel': n.surface, '--steel2': n.champ, '--steel3': n.soft, '--line': n.bord,
    '--soft': n.soft, '--fond': n.fond, '--panneau': n.surface, '--carte': n.champ, '--hf-fond': n.fond, '--hf-panneau': n.surface,
    '--w-bg-0': n.fond, '--w-bg-1': n.surface, '--w-panel': n.surface, '--w-panel-2': n.champ, '--w-line': n.bord, '--w-line-soft': n.soft,
  };
  const css = 'html[data-epure]{' + Object.entries(v).map(([k, x]) => `${k}:${x} !important`).join(';') + '}';
  await page.addStyleTag({ content: css });
}
const photo = (page: Page, i: number, nom: string) => page.screenshot({ path: path.join(SORTIE, `${nom}-${i}.png`) });
test.setTimeout(300_000);

for (const n of NIVEAUX) {
  test(`niveau ${n.i}`, async ({ page, request }) => {
    await preparer(page);
    await page.goto('/prepare.html');
    await teinter(page, n);
    await page.getByRole('button', { name: /^Solo/ }).first().click({ timeout: 30_000 });
    await expect(page.locator('#hero-grid .tb-port').first()).toBeVisible({ timeout: 30_000 });
    await page.locator('#hero-grid .tb-port').nth(2).hover();
    await page.waitForTimeout(700);
    await photo(page, n.i, 'selection');
    await page.goto('/deck-builder.html?hero=spider_man');
    await teinter(page, n);
    await page.waitForSelector('.db-chip', { timeout: 30_000 });
    await page.waitForTimeout(1000);
    await photo(page, n.i, 'editeur');
    // Le plateau et ses Reglages.
    const scenario = await (await request.get('/get_scenario_json?rhino')).json();
    const deck = await (await request.get('/get_hero_json?spider_man')).json();
    const charge = {
      campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
      encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
      hero_json: [JSON.stringify(deck)], rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard, seed: 4321, timeout: 0,
    };
    expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
    await page.goto('/app/board.html', { waitUntil: 'networkidle' });
    await teinter(page, n);
    await page.waitForTimeout(2500);
    for (let k = 0; k < 40; k++) {
      await page.waitForTimeout(600);
      let agi = false;
      for (const nom of [/^Continuer/, /^Garder ma main/]) {
        const b = page.getByRole('button', { name: nom }).first();
        if ((await b.count()) > 0 && (await b.isVisible()) && !(await b.isDisabled())) { await b.click({ timeout: 2000 }).catch(() => {}); agi = true; break; }
      }
      if (!agi && k > 12) break;
    }
    await page.waitForTimeout(1200);
    await page.getByRole('button', { name: /Réglages/ }).first().click();
    await page.waitForTimeout(900);
    await photo(page, n.i, 'reglages');
  });
}
