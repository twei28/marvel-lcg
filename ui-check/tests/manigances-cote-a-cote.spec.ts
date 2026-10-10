// PLUSIEURS MANIGANCES PRINCIPALES COTE A COTE (10/10/2026) : sur une vraie
// partie Tower Defense (deux principales en jeu), elles ne se chevauchent pas,
// ne debordent pas de leur zone, et les annexes ne debordent pas non plus.
//
// ⚠ JAMAIS SUR LE 2345 (la partie du joueur) : le cas cree une partie.
//   UI_CHECK_BASE=http://127.0.0.1:2313 MANIG=1 WSLENV=UI_CHECK_BASE:MANIG \
//     npx playwright test tests/manigances-cote-a-cote.spec.ts --project=pc
import { test, expect, type Page } from '@playwright/test';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

test.skip(!process.env.MANIG, 'manigances côte à côte : MANIG=1 et un moteur d’essai');

async function partie(page: Page, largeur: number, hauteur: number, table?: string) {
  await page.setViewportSize({ width: largeur, height: hauteur });
  const request = page.request;
  const scenario = await (await request.get('/get_scenario_json?the_tower_defense')).json();
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?spider_man')).json())],
    rules: [...(contrat as { regles_partie_standard: string[] }).regles_partie_standard,
      'confirm_main_scheme', 'confirm_side_scheme', 'confirm_scheme_setup_order'],
    seed: 2468, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
  await page.addInitScript((t) => {
    try {
      // Une table personnalisee (« Modifier la table »), si le cas en donne une.
      if (t) localStorage.setItem('mc_table_v1', JSON.stringify({ 'table-1': t }));
      localStorage.setItem('marvel-langue-choisie', '1');
      localStorage.setItem('marvel-langue', 'fr');
      localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille-bis');
    } catch { /* */ }
  }, table ?? '');
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
}

/** Passe la mise en place jusqu'au mulligan. */
async function derouler(page: Page) {
  for (let i = 0; i < 40; i++) {
    await page.waitForTimeout(600);
    if (await page.locator('.mep-couche').isVisible().catch(() => false)) {
      await page.locator('.mep-continuer').click();
      continue;
    }
    const panneau = page.locator('.panneau-manigance');
    if (await panneau.isVisible().catch(() => false)) {
      await panneau.locator('button').last().click();
      await panneau.waitFor({ state: 'hidden', timeout: 8000 }).catch(() => {});
      continue;
    }
    const tour = page.getByRole('button', { name: /Avengers Tower|Tour des Avengers/i }).first();
    if (await tour.isVisible().catch(() => false)) {
      await tour.click();
      continue;
    }
    if (await page.getByText(/mulligan/i).first().isVisible().catch(() => false)) break;
  }
}

async function mesurer(page: Page) {
  return page.evaluate(() => {
    const r = (e: Element) => e.getBoundingClientRect();
    const zp = document.querySelector('.zone-complot-principal')!;
    const za = document.querySelector('.zone-complots-secondaires');
    const cartes = [...zp.querySelectorAll(':scope .plateau-unite > .scan-card, :scope .plateau-unite .scan-card:not(.stage-arriere .scan-card)')]
      .filter((c) => !c.closest('.stage-arriere') && !c.closest('.est-attachee'))
      .map((c) => r(c.querySelector('.scan-frame') ?? c));
    const uniques = cartes.filter((a, i) => cartes.findIndex((b) => Math.abs(a.left - b.left) < 1 && Math.abs(a.top - b.top) < 1) === i);
    const chevauche = uniques.some((a, i) => uniques.slice(i + 1).some((b) => a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1));
    const zpR = r(zp), zaR = za ? r(za) : null;
    const deborde = uniques.some((c) => c.left < zpR.left - 1 || c.right > zpR.right + 1);
    const annexes = za ? [...za.querySelectorAll('.plateau-unite')].map(r) : [];
    const annexesDebordent = zaR ? annexes.some((c) => c.right > zaR.right + 1 || c.left < zaR.left - 1) : false;
    const memeLigne = uniques.length > 1 && uniques.every((c) => Math.abs(c.top - uniques[0].top) < 2);
    return { principales: uniques.length, chevauche, deborde, memeLigne, annexes: annexes.length, annexesDebordent,
      zp: Math.round(zpR.width), za: zaR ? Math.round(zaR.width) : 0, zonesSeChevauchent: zaR ? zpR.right > zaR.left + 1 : false };
  });
}

for (const [largeur, hauteur] of [[1920, 1080], [1366, 768]] as const) {
  test(`Tower Defense : principales côte à côte (${largeur})`, async ({ page }) => {
    test.setTimeout(240_000);
    await partie(page, largeur, hauteur);
    await derouler(page);
    // MANIG_AVANT=1 : remet le passage a la ligne d'avant, pour voir le test echouer.
    if (process.env.MANIG_AVANT) await page.addStyleTag({ content: '.plateau-scene.avec-bande .zone-complot-principal .plateau-cartes, .plateau-scene.avec-bande .zone-complot-principal .plateau-groupe { flex-wrap: wrap !important }' });
    await page.waitForTimeout(300);
    const m = await mesurer(page);
    console.log(largeur, JSON.stringify(m));
    expect(m.principales).toBeGreaterThanOrEqual(2);
    expect(m.memeLigne).toBe(true);
    expect(m.chevauche).toBe(false);
    expect(m.deborde).toBe(false);
    expect(m.annexesDebordent).toBe(false);
    expect(m.zonesSeChevauchent).toBe(false);
  });
}

// Table personnalisee ou la principale n'a que DEUX cases (de quoi tenir une
// seule carte) : elle doit en gagner une sur les annexes, voisines a droite.
const TABLE_ETROITE =
  '12x8|pr:1,1,2,2,100;me:3,1,2,2,100;mp:5,1,2,2,100;mx:7,1,6,2,100;al+sb+en:3,3,10,2,100;he+so:3,5,10,2,100;pj:1,5,2,2,100;an:1,7,2,2,100;ma:3,7,10,2,100';

test('Tower Defense : principales côte à côte sur une table personnalisée (1920)', async ({ page }) => {
  test.setTimeout(240_000);
  await partie(page, 1920, 1080, TABLE_ETROITE);
  await derouler(page);
  const m = await mesurer(page);
  console.log('perso', JSON.stringify(m));
  expect(m.principales).toBeGreaterThanOrEqual(2);
  expect(m.memeLigne).toBe(true);
  expect(m.chevauche).toBe(false);
  expect(m.deborde).toBe(false);
  expect(m.zonesSeChevauchent).toBe(false);
});
