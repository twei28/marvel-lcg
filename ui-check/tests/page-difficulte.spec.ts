// L'étape « Difficulté » (30/10/2026) : niveau, tous les sets modulaires rangés par boîte, propositions
// VillainTheory. On déroule l'assistant comme le joueur, jusqu'au lancement.
//
// ⚠ JAMAIS SUR LE 2345 (la partie du joueur) : le lancement crée une partie.
//   UI_CHECK_BASE=http://127.0.0.1:2346 npx playwright test tests/page-difficulte.spec.ts --project=pc
import { test, expect, type Page } from '@playwright/test';

async function jusquaLaDifficulte(page: Page) {
  await page.addInitScript(() => {
    try {
      localStorage.setItem('marvel-langue-choisie', '1');
      localStorage.setItem('marvel-langue', 'fr');
      localStorage.setItem('mc_affichage_v1', 'epure');
      localStorage.setItem('mc_affichage_migre', '2026-10-19');
    } catch { /* stockage indisponible */ }
  });
  await page.goto('/prepare.html');
  const tel = (await page.viewportSize())!.width < 700;
  if (tel) {
    await page.locator('.acc-tel-jouer').waitFor({ timeout: 30_000 });
    await page.locator('.acc-tel-jouer').tap();
    await page.locator('.acc-tel-feuille').getByRole('button', { name: /^Solo/ }).tap();
  } else {
    await page.locator('.acc-mode').first().waitFor({ timeout: 30_000 });
    await page.getByRole('button', { name: /^Solo/ }).first().click();
  }
  // Spider-Man a un deck de départ : « Continuer » est allumé aux Decks (un héros fan-made attend qu'on choisisse).
  const spider = page.locator('#hero-grid .tb-port[data-hero="spider_man"]').first();
  await spider.waitFor({ timeout: 30_000 });
  if (tel) {
    await spider.tap();
    await page.locator('.ts-btn.jaune').tap();
  } else {
    await spider.click();
    const valider = page.locator('.vh-panel, .deck-modal').getByRole('button', { name: /valider/i });
    if (await valider.isVisible({ timeout: 3_000 }).catch(() => false)) await valider.click();
  }
  for (let i = 0; i < 2; i++) {
    await page.getByRole('button', { name: /^Continuer/i }).click({ timeout: 10_000 });
    await page.waitForTimeout(1200);
  }
  // Rhino est le premier méchant du Set de base.
  await page.locator('.tb-port').first().click({ timeout: 10_000 });
  await page.getByRole('button', { name: /^Continuer/i }).click({ timeout: 10_000 });
  await expect(page.locator('.step.difficulte')).toBeVisible();
  await expect(page.locator('.dp-sets .dp-set').first()).toBeVisible();
}

const gauche = (page: Page) => page.locator('.dp-sets');

test.describe('page Difficulté sur PC', () => {
  test.use({ viewport: { width: 1600, height: 900 } });

  test('niveau, sets par boîte, propositions, puis le lancement porte les bons sets', async ({ page }) => {
    test.setTimeout(150_000);
    const erreurs: string[] = [];
    page.on('pageerror', (e) => erreurs.push(e.message));
    await jusquaLaDifficulte(page);

    // Le fil compte cinq étapes ; la quatrième est active ; l'écran Méchant n'a plus ni niveau ni sets.
    await expect(page.locator('.pstep')).toHaveCount(5);
    await expect(page.locator('.pstep.active')).toContainText(/difficult/i);
    await expect(gauche(page)).toContainText('Rhino');
    await expect(gauche(page)).toContainText('Standard I');
    await expect(gauche(page)).toContainText('Alerte à la Bombe');
    // La note de difficulté n'est plus dans le panneau de gauche : seulement avec les propositions.
    await expect(page.locator('.dp-diff')).toHaveCount(0);

    // Le niveau suit : Standard II change la ligne « suit le niveau ».
    await page.locator('#tb-niveau').getByRole('button', { name: 'Standard II', exact: true }).click();
    await expect(gauche(page)).toContainText('Standard II');

    // Tous les sets modulaires, par boîte, avec la boîte en français.
    const boites = page.locator('.dp-boite > summary');
    expect(await boites.count()).toBeGreaterThan(5);
    await expect(page.locator('.dp-liste')).toContainText('Set de base');

    // La recherche trouve un set et sa boîte ; le cocher l'ajoute à « Ajoutés par toi », la note devient « — ».
    await page.locator('#dp-recherche').fill('hydra patrol');
    const hydra = page.locator('.dp-case', { hasText: 'Hydra Patrol' });
    await expect(hydra).toBeVisible();
    await hydra.locator('input').check();
    await expect(gauche(page).locator('.dp-set.ajoute')).toContainText('Hydra Patrol');
    await gauche(page).locator('.dp-set.ajoute .dp-x').click();
    await expect(gauche(page).locator('.dp-set.ajoute')).toHaveCount(0);
    await page.locator('#dp-recherche').fill('');

    // Les propositions VillainTheory : « Stay Hydrated » = Hydra Patrol seul, +1.
    await expect(page.locator('.dp-props')).toBeHidden();
    await expect(page.locator('.dp-vt')).toHaveClass(/\btampon\b/);
    const hauteurs = await page.evaluate(() => ['.dp-rapide .tampon:not(.dp-vt)', '.dp-vt'].map((q) => document.querySelector(q)!.getBoundingClientRect().height));
    expect(Math.abs(hauteurs[0] - hauteurs[1]), 'même hauteur que Recommandés').toBeLessThan(2);
    await page.locator('.dp-vt').click();
    await expect(page.locator('.dp-vt')).toHaveClass(/\bon\b/);
    const carte = page.locator('.dp-carte', { hasText: 'Stay Hydrated' });
    await expect(carte).toBeVisible();
    await expect(carte.locator('.dp-note')).toHaveText('+1');
    await carte.getByRole('button', { name: 'Utiliser' }).click();
    await expect(page.locator('.dp-selection')).toContainText('+1');
    await expect(page.locator('.dp-selection')).toContainText('Stay Hydrated');
    await expect(gauche(page).locator('.dp-set.ajoute')).toContainText('Hydra Patrol');
    await expect(gauche(page).locator('.dp-set.attenue')).toContainText('Alerte à la Bombe');
    await expect(carte).toHaveClass(/\bactive\b/);

    // « Recommandés » remet la sélection de départ.
    await gauche(page).getByRole('button', { name: 'Recommandés' }).click();
    await expect(page.locator('.dp-selection')).toContainText('+0');

    // On rechoisit la proposition, puis Continuer mène au face à face et Lancer envoie les sets choisis.
    await carte.getByRole('button', { name: 'Utiliser' }).click();
    await page.screenshot({ path: '../.planning/captures-page-difficulte/pc-normal.png' });
    await page.getByRole('button', { name: /^Continuer/i }).click();
    await expect(page.locator('.pstep.active')).toContainText(/final/i);
    const requete = page.waitForRequest((r) => r.url().includes('/new?data='));
    await page.getByRole('button', { name: /Lancer la partie/i }).click();
    const charge = JSON.parse(decodeURIComponent(new URL((await requete).url()).searchParams.get('data')!));
    expect(charge.encounter_set_names).toEqual(expect.arrayContaining(['standard_ii', 'hydra_patrol']));
    expect(charge.encounter_set_names).not.toContain('bomb_scare');
    expect(erreurs, 'aucune erreur JS').toEqual([]);
  });
});

test.describe('page Difficulté sur téléphone', () => {
  test.use({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });

  test('trois onglets, un panneau à la fois, rien ne déborde', async ({ page }) => {
    test.setTimeout(150_000);
    await jusquaLaDifficulte(page);
    const onglets = page.locator('.dp-onglets .tampon');
    await expect(onglets).toHaveCount(3);
    await expect(page.locator('.dp-sets')).toBeVisible();
    await expect(page.locator('.dp-reglages')).toBeHidden();
    await onglets.nth(1).tap();
    await expect(page.locator('.dp-reglages')).toBeVisible();
    await expect(page.locator('.dp-sets')).toBeHidden();
    await expect(page.locator('#tb-niveau')).toContainText('Standard II');
    await onglets.nth(2).tap();
    await expect(page.locator('.dp-props')).toBeVisible();
    await expect(page.locator('.dp-carte', { hasText: 'Stay Hydrated' })).toBeVisible();
    const large = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(large, 'pas de défilement horizontal').toBeLessThanOrEqual(1);
    await page.screenshot({ path: '../.planning/captures-page-difficulte/tel-propositions.png' });
  });
});
