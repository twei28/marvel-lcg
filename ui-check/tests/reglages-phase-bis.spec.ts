// « Étape par étape bis » dans les Réglages du plateau (16/10/2026). En local, le
// moteur ouvre l'essai (essais.ts, estHoteLocal) : les deux présentations se proposent.
// Partie neuve : ⚠ jamais sur un moteur où l'on joue.
import { test, expect } from '@playwright/test';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

test('les Réglages proposent « Étape par étape » et « Étape par étape bis », et retiennent le choix', async ({ page, request }) => {
  test.setTimeout(120_000);
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
  await page.addInitScript(() => { localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('mc_affichage_v1', 'normal'); });
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  // La mise en place carte par carte couvre la table : on la passe.
  for (let k = 0; k < 40; k++) {
    await page.waitForTimeout(500);
    let agi = false;
    for (const nom of [/^Continuer/, /^Garder ma main/]) {
      const bouton = page.getByRole('button', { name: nom }).first();
      if ((await bouton.count()) > 0 && (await bouton.isVisible()) && !(await bouton.isDisabled())) {
        await bouton.click({ timeout: 2000 }).catch(() => {});
        agi = true;
        break;
      }
    }
    if (!agi && k > 8) break;
  }
  await page.getByRole('button', { name: /Réglages/ }).first().click();
  await page.getByRole('tab', { name: /^Jeu$/ }).or(page.getByRole('button', { name: /^Jeu$/ })).first().click();
  const fenetre = page.locator('.reglages-fenetre');
  await expect(fenetre.getByRole('button', { name: /^Étape par étape bis$/ })).toBeVisible();
  await expect(fenetre.getByRole('button', { name: /^Étape par étape$/ })).toBeVisible();
  await fenetre.getByRole('button', { name: /^Étape par étape$/ }).click();
  expect(await page.evaluate(() => localStorage.getItem('mc_phase_bis'))).toBe('non');
  await fenetre.getByRole('button', { name: /^Étape par étape bis$/ }).click();
  expect(await page.evaluate(() => localStorage.getItem('mc_phase_bis'))).toBe('oui');
  // L'apparence : en local, l'Épuré reste proposé (moteur de la machine).
  await page.getByRole('tab', { name: /^Apparence$/ }).or(page.getByRole('button', { name: /^Apparence$/ })).first().click();
  await expect(fenetre.getByRole('button', { name: /^Épuré$/ })).toBeVisible();
});
