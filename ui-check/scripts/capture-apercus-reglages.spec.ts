// CAPTURE PONCTUELLE (04/10/2026) : les images d'exemple des Reglages (apercu
// au survol d'un choix). Vraies parties, moteur d'ESSAI seulement. Ecrit dans
// public/img/reglages/ (servi en .jpg). Range HORS de tests/.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const DEST = path.resolve('..', 'Fusion', 'marvel-lcg-src', 'public', 'img', 'reglages');
const image = (page: Page, nom: string) =>
  page.screenshot({ path: path.join(DEST, nom), type: 'jpeg', quality: 62 });

async function partie(page: Page, reglages: Record<string, string>) {
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
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.addInitScript((r) => {
    try {
      localStorage.setItem('mc_affichage_v1', 'normal');
      for (const [k, v] of Object.entries(r)) localStorage.setItem(k, v);
    } catch { /* */ }
  }, reglages);
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  await page.request.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.ChangeForm('01001b')"] } });
}

const visible = async (page: Page, nom: RegExp) => {
  const b = page.getByRole('button', { name: nom }).first();
  return (await b.count()) > 0 && (await b.isVisible()) ? b : undefined;
};

/** Avance (tour du joueur puis phase du mechant) jusqu'a ce que `fini` soit vrai. */
async function jouerJusqua(page: Page, fini: () => Promise<boolean>, tours = 400) {
  for (let i = 0; i < tours; i++) {
    if (await fini()) return true;
    await page.waitForTimeout(300);
    // Fin de tour, main trop grande : choisir une carte a defausser.
    const defausser = await visible(page, /^Défausser \d/);
    if (defausser && (await defausser.isDisabled())) {
      await page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/ })
        .first().click({ timeout: 2000 }).catch(() => {});
      continue;
    }
    for (const nom of [/^Garder ma main/, /^Défausser \d/, /^Suivant$/, /^Ne pas (défendre|utiliser)/, /^Passer/, /^Continuer/, /^Fin de phase/i, /Fin du tour/]) {
      const b = await visible(page, nom);
      if (b && !(await b.isDisabled())) { await b.click({ timeout: 2000 }).catch(() => {}); break; }
    }
  }
  return fini();
}

test('apercus des reglages', async ({ page }) => {
  test.setTimeout(600_000);
  fs.mkdirSync(DEST, { recursive: true });

  // 1. Phase du mechant, etape par etape : le cartouche et sa frise.
  await partie(page, { 'marvel-board-mode-phase-mechant': 'detaille' });
  const titre = page.locator('.deroule-phase .deroule-titre');
  expect(await jouerJusqua(page, async () => (await titre.count()) > 0 && /attaque/i.test((await titre.first().textContent()) ?? ''))).toBe(true);
  await page.waitForTimeout(1200);
  await image(page, 'phase-etape.jpg');

  // 2. D'un coup + carte revelee en grand : la carte au centre, puis le recap.
  await partie(page, { 'marvel-board-mode-phase-mechant': 'instantane', 'marvel-board-revelation': 'long' });
  const revelee = page.locator('.couche-revelation .revelation');
  if (await jouerJusqua(page, async () => (await revelee.count()) > 0)) {
    await page.waitForTimeout(700);
    await image(page, 'revelation.jpg');
  } else console.log('REVELATION introuvable');
  const recap = page.locator('.recap-mechant-fait');
  if (await jouerJusqua(page, async () => (await recap.count()) > 0, 120)) {
    await page.waitForTimeout(800);
    await image(page, 'phase-coup.jpg');
  } else console.log('RECAP introuvable');

  // 3. Aide quand je joue une carte : courte, puis detaillee.
  for (const [mode, nom] of [['simple', 'aide-courte.jpg'], ['detailed', 'aide-detaillee.jpg']]) {
    await partie(page, { 'marvel-board-action-mode': mode, 'marvel-board-mode-phase-mechant': 'detaille' });
    await jouerJusqua(page, async () => !(await visible(page, /^Garder ma main/)), 30);
    await page.waitForTimeout(800);
    const carte = page.getByRole('button', { name: /, (Allié|Amélioration|Soutien)$/ }).first();
    await carte.click({ timeout: 4000 }).catch(() => {});
    await page.waitForTimeout(500);
    const jouer = await visible(page, /^Jouer/);
    if (jouer) await jouer.click({ timeout: 3000 }).catch(() => {});
    await page.waitForTimeout(900);
    console.log('ASSISTANT', mode, await page.locator('.assistant-action').count());
    await image(page, nom);
    await page.keyboard.press('Escape');
  }

  // 4. Meteo et decor : l'apercu « Pluie » des Reglages.
  await page.getByRole('button', { name: 'Réglages' }).click();
  await page.getByRole('button', { name: 'Pluie' }).first().click();
  await page.keyboard.press('Escape');
  await page.waitForTimeout(1500);
  await image(page, 'meteo.jpg');
});
