// JETABLE (10/10/2026) : l'ordre des ecrans de la mise en place, Tower Defense.
import { test, expect } from '@playwright/test';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

test('ordre de la mise en place (Tower Defense)', async ({ page }) => {
  test.setTimeout(240_000);
  await page.setViewportSize({ width: 1600, height: 900 });
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
  await page.addInitScript(() => {
    try {
      localStorage.setItem('marvel-langue-choisie', '1');
      localStorage.setItem('marvel-langue', 'fr');
      localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille');
    } catch { /* */ }
  });
  if (process.env.DIST_BIS) {
    const fs = await import('node:fs');
    const path = await import('node:path');
    await page.route('**/app/**', async (route) => {
      const url = new URL(route.request().url());
      const rel = url.pathname.replace(/^\/app\//, '');
      const f = path.join(process.env.DIST_BIS!, rel);
      if (fs.existsSync(f) && f.endsWith('.html')) {
        // Les en-tetes du serveur (cookies de version et de table), le contenu du worktree.
        const reponse = await route.fetch();
        await route.fulfill({ response: reponse, body: fs.readFileSync(f, 'utf-8') });
      } else if (fs.existsSync(f)) {
        const type = f.endsWith('.js') ? 'application/javascript' : f.endsWith('.css') ? 'text/css' : undefined;
        await route.fulfill({ body: fs.readFileSync(f), contentType: type });
      } else await route.continue();
    });
  }
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  const vu: string[] = [];
  for (let i = 0; i < 60; i++) {
    await page.waitForTimeout(700);
    if (i === 0 || vu.length === 0) {
      const d = await page.evaluate(async () => (await (await fetch('/get_ask?p=0')).text()).slice(0, 300)).catch(() => '');
      if (d && d.length > 4) vu.push('T' + i + ' DEMANDE ' + d.replace(/\s+/g, ' '));
    }
    const mep = page.locator('.mep-couche');
    if (await mep.isVisible().catch(() => false)) {
      const leg = await mep.locator('.mep-legende').textContent().catch(() => '');
      const alt = await mep.locator('img').first().getAttribute('src').catch(() => '');
      vu.push(`FILE   ${leg} ${alt}`);
      if (vu.length === 1) await page.screenshot({ path: '../.planning/captures-mise-en-place/zz-ordre-premier.png' });
      if (vu.length === 1) {
        const d = await page.evaluate(async () => (await (await fetch('/get_ask?p=0')).text()).slice(0, 600));
        vu.push('DEMANDE ' + d.replace(/\s+/g, ' '));
      }
      await mep.locator('.mep-continuer').click();
      continue;
    }
    const panneau = page.locator('.panneau-manigance');
    if (await panneau.isVisible().catch(() => false)) {
      const txt = (await panneau.innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 120);
      const alt = await panneau.locator('img').first().getAttribute('alt').catch(() => '');
      vu.push(`PANNEAU ${alt} | ${txt}`);
      await panneau.locator('button').last().click();
      await panneau.waitFor({ state: 'hidden', timeout: 8000 }).catch(() => {});
      continue;
    }
    const tour = page.getByRole('button', { name: /Avengers Tower|Tour des Avengers/i }).first();
    if (await tour.isVisible().catch(() => false)) { vu.push('CHOIX tour'); await tour.click(); continue; }
    if (await page.getByText(/mulligan/i).first().isVisible().catch(() => false)) break;
  }
  await page.screenshot({ path: '../.planning/captures-mise-en-place/zz-ordre-fin.png' });
  const zone = await page.evaluate(() => [...document.querySelectorAll('.zone-complot-principal .scan-card[data-card-id]')]
    .map((e) => (e as HTMLElement).dataset.cardId + ':' + ((e.querySelector('img') as HTMLImageElement | null)?.getAttribute('src') ?? '')));
  vu.push('ZONE ' + zone.join(' '));
  console.log('ORDRE\n' + vu.join('\n'));
});
