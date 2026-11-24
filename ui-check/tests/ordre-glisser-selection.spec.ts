// PERMUTER L'ORDRE D'ACTIVATION DES SBIRES AU GLISSER-DEPOSER, A LA VRAIE SOURIS.
//
// Demande de Yarro (fiche 2026-09-28-nice-to-have-yarro.md) : en plus des
// pastilles numerotees et des boutons « ← »/« → », pouvoir echanger deux cartes
// d'une selection ordonnee en les glissant. Ici : une vraie partie, deux sbires
// engages, la phase du mechant demande l'ordre, on choisit les deux sbires puis
// on glisse le premier sur le second.
//
//   npx playwright test tests/ordre-glisser-selection.spec.ts --project=pc
//
// ATTENTION : cree une NOUVELLE partie sur le serveur de jeu (toute partie en
// cours est perdue).
import { test, expect, type Page, type APIRequestContext } from '@playwright/test';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

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
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 1234,
    timeout: 0,
  };
  const reponse = await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)));
  expect(reponse.status(), 'le moteur a refuse de creer la partie').toBe(200);
}

async function passerLaMiseEnPlace(page: Page) {
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
}

test('glisser un sbire choisi sur l autre echange leur ordre', async ({ page, request }) => {
  test.setTimeout(240000);
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.addInitScript(() => {
    try {
      localStorage.setItem('marvel-langue-choisie', '1');
      localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille');
      localStorage.setItem('mc_aide_bulle_table', 'vue');
    } catch {
      /* */
    }
  });
  await nouvellePartie(request);
  await page.goto('/app/board.html?p=0');
  await page.waitForSelector('.scan-card[data-card-id]', { timeout: 30000 });
  await passerLaMiseEnPlace(page);
  await page.waitForSelector('.zone-main .scan-card[data-card-id]', { timeout: 30000 });
  const rep = await page.request.post('/sandbox_command?p=0', {
    data: { commands: ["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01120')"] },
  });
  console.log('commandes', rep.status(), (await rep.text()).slice(0, 200));
  await page.waitForTimeout(1500);
  await page.getByRole('button', { name: /Fin du tour/ }).first().click();
  const liste = [/^Fin de phase/i, /^Étape suivante/i, /^Garder ma main/, /(^|— )Suivant/, /^Défausser \d/, /^Terminer/, /Fin du tour/, /^Ne pas (défendre|utiliser|jouer)/, /^Aucune réponse/, /^Continuer sans rien jouer/, /(^|— )Continuer/, /^OK$/];
  const vignettes = page.locator('.deroule-vignette.est-choix[data-carte-id]');
  for (let k = 0; k < 100 && (await vignettes.count()) < 2; k++) {
    for (const nom of liste) {
      const b = page.getByRole('button', { name: nom }).first();
      if (await b.isVisible().catch(() => false)) {
        await b.click({ timeout: 2000 }).catch(() => {});
        break;
      }
    }
    await page.waitForTimeout(1000);
  }
  expect(await vignettes.count(), "l'ordre d'activation des sbires n'a jamais ete demande").toBeGreaterThanOrEqual(2);
  await page.waitForTimeout(800);

  const premiere = vignettes.nth(0);
  const idA = await premiere.getAttribute('data-carte-id');
  const idB = await vignettes.nth(1).getAttribute('data-carte-id');
  const ordreDe = (id: string | null) =>
    page.locator(`.deroule-vignette[data-carte-id="${id}"] .deroule-ordre`);

  // Rien n'est encore range : on ne peut pas glisser une carte pas encore choisie.
  await expect(page.locator('.deroule-vignette.est-permutable')).toHaveCount(0);

  // On choisit A puis B : A passe en 1, B en 2.
  await premiere.click();
  await expect(ordreDe(idA)).toHaveText('1');
  await page.locator(`.deroule-vignette[data-carte-id="${idB}"]`).click();
  await expect(ordreDe(idB)).toHaveText('2');
  await expect(page.locator('.deroule-vignette.est-permutable')).toHaveCount(2);
  await page.screenshot({ path: 'captures-tmp/ordre-glisser-avant.png' });

  // Le geste : A (rang 1) glisse sur B (rang 2). Les deux s'echangent.
  await page
    .locator(`.deroule-vignette[data-carte-id="${idA}"]`)
    .dragTo(page.locator(`.deroule-vignette[data-carte-id="${idB}"]`));
  await expect(ordreDe(idA)).toHaveText('2');
  await expect(ordreDe(idB)).toHaveText('1');
  await page.screenshot({ path: 'captures-tmp/ordre-glisser-apres.png' });

  // Et l'ordre echange est bien celui qui part au moteur : « Confirmer » s'allume.
  await expect(page.getByRole('button', { name: 'Confirmer' }).first()).toBeEnabled();
});
