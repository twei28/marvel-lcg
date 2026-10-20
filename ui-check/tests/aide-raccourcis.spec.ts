// L'aide du plateau liste les touches du clavier qui existent (E, Espace, U, B, 1 a 9, Echap).
//
//   npx playwright test tests/aide-raccourcis.spec.ts --project=pc
//
// ATTENTION : cree une NOUVELLE partie sur le serveur de jeu (la languette d'aide
// n'existe pas sur une page d'etat figee).
import { test, expect } from '@playwright/test';

test('l aide liste les raccourcis clavier existants', async ({ page, request }) => {
  await page.setViewportSize({ width: 1280, height: 720 });
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const deck = await (await request.get('/get_hero_json?spider_man')).json();
  const charge = {
    campaign_json: JSON.stringify(scenario),
    campaign_log: {},
    challenges: scenario.challenges ?? [],
    encounter_set_names: [
      ...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])]),
    ],
    hero_json: [JSON.stringify(deck)],
    rules: ['standard'],
    seed: 1234,
    timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
  await page.goto('/app/board.html?p=0');
  await page.waitForSelector('.volet-aide-languette', { timeout: 30000 });
  await page.waitForTimeout(1500);
  // On fait defiler la mise en place pour que la capture montre l'aide sur la table libre.
  for (let k = 0; k < 40 && (await page.locator('.mep-couche').count()) > 0; k++) {
    await page.locator('.mep-couche .mep-continuer').first().click({ timeout: 1500, force: true }).catch(() => {});
    await page.waitForTimeout(400);
  }
  // Le mulligan se ferme avec son bouton ; l'aide reste ouvrable par-dessus.
  await page.locator('.volet-aide-languette').dispatchEvent('click');
  const aide = page.locator('#volet-aide-auto');
  await expect(aide).toBeVisible();
  for (const texte of ['Pendant la partie', 'Espace', 'Copier le rapport de bug', '1 à 9', 'Choisir l’option portant ce numéro']) {
    await expect(aide).toContainText(texte);
  }
  await page.screenshot({ path: 'captures-tmp/aide-raccourcis.png' });
});
