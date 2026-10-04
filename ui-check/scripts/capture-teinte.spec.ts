// VERIFICATION PONCTUELLE (04/10/2026) : la teinte du fond sur le plateau et
// dans la fenetre d'accueil. Moteur d'ESSAI seulement (cree une partie).
import { test, expect } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const SORTIE = process.env.SORTIE_CAPTURES || path.resolve('captures-tmp');
const TEINTES: Array<[string, string | null]> = [
  ['origine', null], ['nuit', '220,8,12'], ['brun', '30,14,22'], ['sauge', '140,10,40'], ['gris-clair', '200,6,60'],
];

test('teinte du fond : plateau en Normal et en Sobre, puis Reglages', async ({ page, request }) => {
  test.setTimeout(300_000);
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
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  await expect(page.getByRole('button', { name: /^Garder ma main/ }).first()).toBeVisible({ timeout: 30_000 });

  for (const mode of ['normal', 'sobre']) {
    for (const [nom, valeur] of TEINTES) {
      await page.evaluate(([m, v]) => {
        localStorage.setItem('mc_affichage_v1', m as string);
        if (v) localStorage.setItem('mc_teinte_v1', v as string); else localStorage.removeItem('mc_teinte_v1');
      }, [mode, valeur]);
      await page.reload({ waitUntil: 'networkidle' });
      await page.waitForTimeout(2500);
      await page.screenshot({ path: path.join(SORTIE, `teinte-${mode}-${nom}.png`) });
    }
  }
  // La roue dans les Reglages, sur la derniere teinte.
  await page.getByRole('button', { name: /Plus d'options/ }).first().click();
  await page.getByRole('button', { name: /Réglages/ }).first().click();
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(SORTIE, 'teinte-reglages.png') });
});

test('fenetre d accueil avec la roue', async ({ page }) => {
  await page.setViewportSize({ width: 1600, height: 1000 });
  await page.goto('/prepare.html', { waitUntil: 'networkidle' });
  const francais = page.getByRole('button', { name: /^Français/ });
  if (await francais.count()) await francais.first().click();
  const fenetre = page.locator('.affichage-modal');
  await expect(fenetre).toBeVisible({ timeout: 15_000 });
  // Un geste sur le curseur de luminosite : l'apercu doit changer de fond.
  const avant = await fenetre.locator('.rt-apercu').evaluate((n) => getComputedStyle(n).backgroundColor);
  await fenetre.getByLabel('Luminosité du fond').fill('50');
  const apres = await fenetre.locator('.rt-apercu').evaluate((n) => getComputedStyle(n).backgroundColor);
  expect(apres).not.toBe(avant);
  await page.screenshot({ path: path.join(SORTIE, 'teinte-accueil.png') });
  await fenetre.getByRole('button', { name: /^Sobre/ }).click();
  await fenetre.getByRole('button', { name: /^Valider/ }).click();
  await expect(fenetre).toHaveCount(0);
  const teinte = await page.evaluate(() => localStorage.getItem('mc_teinte_v1'));
  expect(teinte).toMatch(/^\d+,\d+,50$/);
  await expect(page.locator('html')).toHaveAttribute('data-affichage', 'sobre');
});
