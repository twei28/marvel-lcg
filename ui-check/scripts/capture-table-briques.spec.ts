// VERIFICATION PONCTUELLE (05/10/2026) : la table par briques. Origine,
// editeur avec pastilles, une brique sortie (Sbires), deux briques reunies
// (manigance principale + annexes). Moteur d'ESSAI seulement. Range HORS de
// tests/ : le copier dans tests/ le temps de le lancer.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const SORTIE = process.env.SORTIE_CAPTURES || path.resolve('captures-tmp');

async function partie(page: Page, heros: string[]) {
  const request = page.request;
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const decks = await Promise.all(heros.map(async (h) => JSON.stringify(await (await request.get('/get_hero_json?' + h)).json())));
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: decks, rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
}

async function ouvrir(page: Page) {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  await expect(page.locator('.plateau-scene')).toBeVisible({ timeout: 30_000 });
  await page.waitForTimeout(1500);
}

async function glisser(page: Page, de: { x: number; y: number }, vers: { x: number; y: number }) {
  await page.mouse.move(de.x, de.y);
  await page.mouse.down();
  await page.mouse.move(vers.x, vers.y, { steps: 10 });
  await page.mouse.up();
}

const centre = async (page: Page, sel: string) => {
  const b = (await page.locator(sel).first().boundingBox())!;
  return { x: b.x + b.width / 2, y: b.y + b.height / 2, b };
};

test('table par briques', async ({ page }) => {
  test.setTimeout(100_000);
  fs.mkdirSync(SORTIE, { recursive: true });
  await partie(page, ['spider_man']);
  await page.addInitScript(() => { try { localStorage.setItem('mc_affichage_v1', 'normal'); } catch { /* */ } });
  await ouvrir(page);
  await page.screenshot({ path: path.join(SORTIE, 'briques-origine.png') });

  await page.getByRole('button', { name: /Réglages/ }).first().click();
  await page.getByRole('button', { name: 'Modifier la table' }).click();
  await expect(page.locator('.editeur-table')).toBeVisible();
  await page.screenshot({ path: path.join(SORTIE, 'briques-editeur.png') });

  // Sbires : glisser la pastille sur la case libre en haut a gauche des deux lignes du combat.
  const grille = (await page.locator('.editeur-table').boundingBox())!;
  const colonne = grille.width / 12;
  const ligne = grille.height / 8;
  const sbires = await centre(page, '.editeur-brique[data-brique="sbires"]');
  await glisser(page, sbires, { x: grille.x + colonne * 0.5, y: grille.y + ligne * 2.5 });
  await expect(page.locator('.editeur-brique[data-brique="sbires"]')).toBeVisible();
  expect(await page.locator('.editeur-zone').count()).toBe(10);
  await page.screenshot({ path: path.join(SORTIE, 'briques-editeur-sbires.png') });

  // Manigance principale sur Manigances annexes : une seule zone.
  const mp = await centre(page, '.editeur-brique[data-brique="manigance-principale"]');
  const mx = await centre(page, '.editeur-zone[data-zone="manigances-annexes"]');
  await glisser(page, mp, { x: mx.x, y: mx.y + 30 });
  expect(await page.locator('.editeur-zone').count()).toBe(9);
  await page.screenshot({ path: path.join(SORTIE, 'briques-editeur-fusion.png') });

  await page.getByRole('button', { name: 'Terminer' }).click();
  await expect(page.locator('.editeur-table')).toHaveCount(0);
  console.log('STOCKE', await page.evaluate(() => localStorage.getItem('mc_table_v1')));
  await page.screenshot({ path: path.join(SORTIE, 'briques-table-eclatee.png') });
  console.log('TITRES', JSON.stringify(await page.locator('.plateau-scene h2, .plateau-scene .zone-titre').allInnerTexts()));
});
