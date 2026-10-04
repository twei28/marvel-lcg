// VERIFICATION PONCTUELLE (04/10/2026) : les choix de defense cote a cote.
import { test, expect, type Page } from '@playwright/test';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const visible = async (page: Page, nom: RegExp) => {
  const b = page.getByRole('button', { name: nom }).first();
  return (await b.count()) > 0 && (await b.isVisible()) ? b : undefined;
};

for (const [l, h] of [[1024, 640], [1600, 900]]) test(`defense ${l}`, async ({ page }) => {
  test.setTimeout(240_000);
  const request = page.request;
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const deck = await (await request.get('/get_hero_json?spider_man')).json();
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(deck)], rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
  await page.setViewportSize({ width: l, height: h });
  await page.addInitScript(() => { try { localStorage.setItem('mc_affichage_v1', 'normal'); localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille'); } catch { /* */ } });
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  const r = await page.request.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('Black Widow', True)", "Puzzle.PutIntoPlay('Hawkeye', True)"] } });
  console.log('SANDBOX', r.status(), (await r.text()).slice(0, 300));
  for (let i = 0; i < 300; i++) {
    if ((await page.getByRole('button', { name: /^Défendre avec/ }).count()) >= 2) break;
    await page.waitForTimeout(300);
    const defausser = await visible(page, /^Défausser \d/);
    if (defausser && (await defausser.isDisabled())) {
      await page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/ }).first().click({ timeout: 2000 }).catch(() => {});
      continue;
    }
    for (const nom of [/^Garder ma main/, /^Défausser \d/, /^Suivant$/, /^Ne pas utiliser/, /^Passer/, /^Continuer/, /^Fin de phase/i, /Fin du tour/]) {
      const b = await visible(page, nom);
      if (b && !(await b.isDisabled())) { await b.click({ timeout: 2000 }).catch(() => {}); break; }
    }
  }
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.resolve('captures-tmp', `defense-${l}.png`) });
  const tops = await page.locator('.deroule-phase.est-question .dc-boutons > *').evaluateAll((n) => n.map((e) => Math.round(e.getBoundingClientRect().bottom)));
  console.log('BAS DES CHOIX', l, tops);
  expect(new Set(tops).size).toBe(1);
});
