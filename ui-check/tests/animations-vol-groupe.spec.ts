// AU-DELA DE DIX CARTES, LE PLATEAU ANIME AUTREMENT QU'EN NE FAISANT RIEN.
//
// Fiche .planning/todos/2026-09-14-animations-molles.md, point 5 : au-dela de
// `MAX_VOLS` (10) mouvements d'un coup, la couche d'animation sautait tout. Elle
// fait maintenant voler UNE pile fantome par groupe, avec le nombre de cartes.
//
//   npx playwright test tests/animations-vol-groupe.spec.ts --project=pc
//
// ATTENTION : comme `glisser-plateau`, ce test cree une NOUVELLE partie sur le
// serveur de jeu. Toute partie en cours est perdue.
//
// ⚠ Les captures de reference coupent les animations (`reducedMotion: 'reduce'`
// dans la config) : ce cas les remet, sinon la couche n'anime rien du tout.
import { test, expect, type Page, type APIRequestContext } from '@playwright/test';

test.use({ reducedMotion: 'no-preference' });

async function nouvellePartie(request: APIRequestContext) {
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
  const reponse = await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)));
  expect(reponse.status(), 'le moteur a refuse de creer la partie').toBe(200);
}

async function ouvrirLaTable(page: Page) {
  await page.goto('/app/board.html?p=0');
  await page.waitForSelector('.scan-card[data-card-id]', { timeout: 30000 });
  const confirmer = page.getByRole('button', { name: /^(Confirmer|Garder ma main)/ }).first();
  let confirme = false;
  let calme = 0;
  for (let k = 0; k < 120 && calme < 4; k++) {
    const mep = page.locator('.mep-couche .mep-continuer').first();
    if (await mep.isVisible().catch(() => false)) {
      calme = 0;
      await mep.click({ timeout: 1500, force: true }).catch(() => {});
    } else if ((await page.locator('.mep-couche').count()) > 0) {
      calme = 0;
    } else if (!confirme && (await confirmer.isVisible().catch(() => false))) {
      calme = 0;
      confirme = true;
      await confirmer.click({ timeout: 3000 }).catch(() => {
        confirme = false;
      });
    } else if (confirme) {
      calme++;
    }
    await page.waitForTimeout(400);
  }
  expect(confirme, "le mulligan ne s'est jamais ouvert").toBe(true);
  await page.waitForSelector('.zone-main .scan-card[data-card-id]', { timeout: 30000 });
  await page.waitForTimeout(1500);
}

test('douze cartes piochees d un coup volent en une pile groupee', async ({ page, request }) => {
  await page.setViewportSize({ width: 1280, height: 720 });
  await nouvellePartie(request);
  await ouvrirLaTable(page);

  // Un releve des fantomes a chaque changement du DOM : un vol dure ~250 ms, un
  // sondage par `waitForTimeout` le manquerait.
  await page.evaluate(() => {
    const w = window as unknown as { __vols: { max: number; pile: number; nombre: string } };
    w.__vols = { max: 0, pile: 0, nombre: '' };
    new MutationObserver(() => {
      const tous = document.querySelectorAll('.vol-carte');
      w.__vols.max = Math.max(w.__vols.max, tous.length);
      const pile = document.querySelector('.vol-carte.est-pile .vol-carte-nombre');
      if (pile) {
        w.__vols.pile = document.querySelectorAll('.vol-carte.est-pile').length;
        w.__vols.nombre = pile.textContent ?? '';
      }
    }).observe(document.body, { childList: true, subtree: true });
  });

  const avant = await page.locator('.zone-main .scan-card[data-card-id]').count();
  await page.screenshot({ path: 'captures-tmp/vol-groupe-avant.png', animations: 'allow' });

  const rep = await page.request.post('/sandbox_command?p=0', { data: { commands: ['Puzzle.Draw(12)'] } });
  expect(rep.status()).toBe(200);

  const pile = page.locator('.vol-carte.est-pile');
  await pile.first().waitFor({ state: 'attached', timeout: 15000 });
  await page.screenshot({ path: 'captures-tmp/vol-groupe-en-vol.png', animations: 'allow' });

  await expect(page.locator('.vol-carte')).toHaveCount(0, { timeout: 5000 });
  await page.screenshot({ path: 'captures-tmp/vol-groupe-apres.png', animations: 'allow' });

  const mesure = await page.evaluate(
    () => (window as unknown as { __vols: { max: number; pile: number; nombre: string } }).__vols
  );
  const apres = await page.locator('.zone-main .scan-card[data-card-id]').count();
  console.log(`mains : ${avant} -> ${apres} ; fantomes simultanes max : ${mesure.max} ; piles : ${mesure.pile} ; pastille : ${mesure.nombre}`);

  expect(apres - avant, 'la pioche de 12 cartes n est pas arrivee').toBeGreaterThanOrEqual(11);
  // Un seul fantome pour toute la pioche, pas douze et pas zero.
  expect(mesure.max).toBeLessThanOrEqual(2);
  expect(Number(mesure.nombre)).toBeGreaterThanOrEqual(11);
  // Toutes les vraies cartes sont revenues visibles.
  const cachees = await page.$$eval('.zone-main .scan-card', (els) =>
    els.filter((e) => (e as HTMLElement).style.visibility === 'hidden').length
  );
  expect(cachees).toBe(0);
});
