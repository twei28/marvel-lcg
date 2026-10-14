// JETABLE (10/10/2026) : rapport n76 de Yarro, Controle climatique de Storm sur tablette.
import { test, expect } from '@playwright/test';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const SORTIE = '../.planning/captures-storm';
test.use({ hasTouch: true });
let traces: string[] = [];

test('Storm : Controle climatique', async ({ page }) => {
  test.setTimeout(90_000);
  page.on('console', (m) => { if (m.text().includes('TRACE-PILE')) traces.push(m.text()); });
  const request = page.request;
  const scenario = await (await request.get('/get_scenario_json?klaw')).json();
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?storm')).json())],
    rules: [...(contrat as { regles_partie_standard: string[] }).regles_partie_standard],
    seed: 1357, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
  await page.addInitScript(() => {
    try {
      localStorage.setItem('marvel-langue-choisie', '1');
      localStorage.setItem('marvel-langue', 'fr');
      localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille');
    } catch { /* */ }
  });
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  // Mise en place : on avance jusqu'au tour de Storm, en forme heros.
  for (let i = 0; i < 40; i++) {
    await page.waitForTimeout(700);
    const mep = page.locator('.mep-continuer');
    if (await mep.isVisible().catch(() => false)) { await mep.click(); continue; }
    const panneau = page.locator('.panneau-manigance');
    if (await panneau.isVisible().catch(() => false)) { await panneau.locator('button').last().click(); continue; }
    const garder = page.getByRole('button', { name: /Garder ma main|Keep/i }).first();
    if (await garder.isVisible().catch(() => false)) { await garder.click(); continue; }
    const choix = page.locator('.demande-centrale button, .af-action').first();
    if (await page.getByText(/Contrôle Climatique|Weather Control/i).first().isVisible().catch(() => false)) break;
    if (await choix.isVisible().catch(() => false) && i > 30) break;
  }
  await page.screenshot({ path: `${SORTIE}/1-table.png` });
  const fenetre = page.getByRole('dialog').filter({ has: page.getByRole('button', { name: 'Valider' }) });
  const journal: string[] = [];
  // 1. Mise en place : « I feel a storm coming... »
  await page.getByRole('button', { name: /storm coming/i }).first().tap();
  await fenetre.waitFor({ timeout: 8000 });
  journal.push('MEP fenetre ouverte, Valider actif=' + !(await fenetre.getByRole('button', { name: 'Valider' }).isDisabled()));
  journal.push('MEP panneau central visible=' + (await page.locator('.assistant-action, .af-panneau').first().isVisible().catch(() => false)));
  await page.screenshot({ path: `${SORTIE}/2-fenetre-mise-en-place.png` });
  await fenetre.locator('.plateau-selecteur-carte').nth(1).locator('[role="button"], button, .scan-card').first().tap();
  await page.waitForTimeout(400);
  await page.screenshot({ path: `${SORTIE}/3-juste-apres-toucher.png` });
  console.log('APRES TOUCHER dialog=' + (await page.getByRole('dialog').count()) + ' boutons=' + JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('button')].map((b) => (b.textContent || '').trim()).filter(Boolean).slice(0, 12))));
  journal.push('MEP apres choix, Valider actif=' + !(await fenetre.getByRole('button', { name: 'Valider' }).isDisabled()));
  await page.screenshot({ path: `${SORTIE}/3-carte-choisie.png` });
  await fenetre.getByRole('button', { name: 'Valider' }).tap();
  await page.waitForTimeout(1500);
  journal.push('MEP fenetre fermee=' + !(await fenetre.isVisible().catch(() => false)));
  // Jusqu'au tour de Storm.
  for (let i = 0; i < 25; i++) {
    await page.waitForTimeout(700);
    const garder = page.getByRole('button', { name: /Garder ma main|Keep/i }).first();
    if (await garder.isVisible().catch(() => false)) { await garder.tap(); continue; }
    const mep = page.locator('.mep-continuer');
    if (await mep.isVisible().catch(() => false)) { await mep.tap(); continue; }
    if (i > 6) break;
  }
  await page.screenshot({ path: `${SORTIE}/4-tour.png` });
  const fermerAmbiance = async () => {
    const garder = page.getByRole('button', { name: /Oui, garder/i });
    if (await garder.isVisible().catch(() => false)) { await garder.tap(); await page.waitForTimeout(600); }
  };
  await fermerAmbiance();
  // Forme heros par le bac a sable (Controle climatique est une Action de heros).
  const rep = await page.request.post('/sandbox_command', { data: { commands: ["Puzzle.ChangeForm('36001b')"] } });
  journal.push('changement de forme ' + rep.status());
  await page.waitForTimeout(2500);
  const meteoEnJeu = () => page.evaluate(() => [...document.querySelectorAll('.zone-meteo .scan-card img, [class*="meteo"] .scan-card img')].map((i) => i.getAttribute('src')).slice(0, 3).join(','));
  journal.push('meteo avant : ' + (await meteoEnJeu()));
  // 2b. Le menu de Storm.
  await fermerAmbiance();
  const storm = page.locator('.scan-card[data-card-id="1"]').first();
  await storm.tap();
  await page.waitForTimeout(1000);
  journal.push('MENU etiquettes hors table=' + (await page.locator('.ma-cible.est-hors-table').count()));
  await page.screenshot({ path: `${SORTIE}/6-menu.png` });
  await page.getByText(/Contrôle Climatique|Weather Control/i).first().tap();
  await page.waitForTimeout(1200);
  journal.push('ACTION fenetre=' + (await fenetre.isVisible().catch(() => false)));
  await page.screenshot({ path: `${SORTIE}/7-fenetre-action.png` });
  if (await fenetre.isVisible().catch(() => false)) {
    await fenetre.locator('.plateau-selecteur-carte').first().locator('[role="button"], button, .scan-card').first().tap();
    await page.waitForTimeout(500);
    journal.push('ACTION Valider actif=' + !(await fenetre.getByRole('button', { name: 'Valider' }).isDisabled()));
    await fenetre.getByRole('button', { name: 'Valider' }).tap();
    await page.waitForTimeout(2000);
    journal.push('ACTION fenetre fermee=' + !(await fenetre.isVisible().catch(() => false)));
    await fermerAmbiance();
  }
  journal.push('meteo apres : ' + (await meteoEnJeu()));
  await page.screenshot({ path: `${SORTIE}/8-apres.png` });
  console.log('TRACES ' + traces.slice(-3).join(' || '));
  console.log('JOURNAL\n' + journal.join('\n'));
});
