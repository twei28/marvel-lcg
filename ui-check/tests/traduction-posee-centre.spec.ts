// La traduction posée sur les affichages EN GRAND au centre (manigance de la
// mise en place, carte révélée) et sur les arts alternatifs de héros (aperçu).
// Moteur d'essai : TRAD=1 UI_CHECK_BASE=http://127.0.0.1:<port> WSLENV=UI_CHECK_BASE:TRAD
import { test, expect, type Page } from '@playwright/test';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

test.skip(!process.env.TRAD, 'traduction posée au centre : TRAD=1 et le moteur d’essai');

const SORTIE = path.resolve('captures-tmp');

async function partieVermin(page: Page, artsHeros: Record<string, string>, heros = 'spider_man') {
  const request = page.request;
  const scenario = await (await request.get('/get_scenario_json?hs_vermin')).json();
  const deck = JSON.stringify(await (await request.get(`/get_hero_json?${heros}`)).json());
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [deck],
    rules: [...(contrat as { regles_partie_standard: string[] }).regles_partie_standard, 'confirm_main_scheme', 'confirm_side_scheme'],
    seed: 4321, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
  await page.addInitScript((arts) => {
    try {
      localStorage.setItem('marvel-langue', 'fr');
      localStorage.setItem('marvel-langue-choisie', '1');
      localStorage.setItem('marvel-board-scans-fr', 'on');
      localStorage.setItem('mc_hero_art_v1', JSON.stringify(arts));
    } catch { /* */ }
  }, artsHeros);
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
}

test('manigance de mise en place et révélation : traduction posée', async ({ page }) => {
  test.setTimeout(120000);
  await partieVermin(page, {});
  const panneau = page.locator('.panneau-manigance');
  await expect(panneau).toBeVisible({ timeout: 30000 });
  await expect(panneau.locator('.traduction-posee').first()).toBeVisible({ timeout: 15000 });
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(SORTIE, 'trad-mise-en-place-face-a.png') });
  const bouton = panneau.locator('.panneau-manigance-ok');
  await bouton.click();
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(SORTIE, 'trad-mise-en-place-face-b.png') });
  await expect(panneau.locator('.panneau-manigance-cadre-verso .traduction-posee')).toHaveCount(1);

  // Une carte RÉVÉLÉE pendant la partie, montrée en grand au centre.
  await bouton.click();
  await page.waitForTimeout(900);
  const garder = page.getByRole('button', { name: 'Garder ma main' });
  if (await garder.isVisible().catch(() => false)) await garder.click();
  await page.waitForTimeout(4000);
  const r = await page.request.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.Reveal('hs022')"] } });
  console.log('REVELATION', r.status(), (await r.text()).slice(0, 200));
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(SORTIE, 'trad-revelation.png') });
  await expect(page.locator('.traduction-posee').first()).toBeVisible({ timeout: 10000 });
});

test('arts alternatifs Comic, Rose of Gondolin et M3T4LB0X : traduction posée dans l’aperçu', async ({ page }) => {
  test.setTimeout(240000);
  const cas = [
    { heros: 'spider_man', arts: { '01001': 'cb' }, image: '01001b_cb', forme: [] as string[] },
    { heros: 'spider_man', arts: { '01001': 'm3t' }, image: '01001a_m3t', forme: ["Puzzle.ChangeForm('01001b')"] },
    { heros: 'she_hulk', arts: { '01019': 'rog' }, image: '01019b_rog', forme: [] as string[] },
  ];
  for (const { heros, arts, image, forme } of cas) {
    await partieVermin(page, arts, heros);
    const panneau = page.locator('.panneau-manigance');
    for (let i = 0; i < 2; i += 1) {
      const ok = panneau.locator('.panneau-manigance-ok');
      if (await ok.isVisible().catch(() => false)) {
        await ok.click();
        await page.waitForTimeout(900);
      }
    }
    const garder = page.getByRole('button', { name: 'Garder ma main' });
    if (await garder.isVisible().catch(() => false)) await garder.click();
    if (forme.length) {
      const r = await page.request.post('/sandbox_command?p=0', { data: { commands: forme } });
      console.log('FORME', r.status(), (await r.text()).slice(0, 200));
      await page.waitForTimeout(1500);
    }
    const identite = page.locator(`img[src*="${image}"]`).first();
    await expect(identite).toBeAttached({ timeout: 30000 });
    await identite.hover({ force: true });
    const apercu = page.locator('.traduction-posee').first();
    await expect(apercu).toBeVisible({ timeout: 15000 });
    await page.waitForTimeout(900);
    await page.screenshot({ path: path.join(SORTIE, `trad-art-${image}.png`) });
  }
});
