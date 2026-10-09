// Le deck-builder en Legacy : on construit avec ce qu'on a.
//
// Ouvert depuis l'assistant avec `?legacy=1`, il grise les cartes des boites
// pas encore ouvertes et refuse de les ajouter, par TOUTES les portes : le
// bouton, l'image, un deck charge. Sans le drapeau, il ne verrouille rien.
//
//   npm run legacy-deckbuilder
import { test, expect, type Page } from '@playwright/test';

async function ficheSetDeBase(page: Page) {
  // Actif, en repartant de zero : rien n'est gagne, seul le Set de base est ouvert.
  await page.evaluate(async () => {
    const mod: any = await import('/js/prepare/legacy-fiche.js');
    await mod.ecrire({ actif: true, depuis: 9_000_000_000, jetonsDepenses: [] });
  });
}
async function vider(page: Page) {
  await page.evaluate(async () => {
    const mod: any = await import('/js/prepare/legacy-fiche.js');
    await mod.ecrire(mod.ficheVide());
  });
}
async function idSpiderMan(page: Page): Promise<string> {
  return page.evaluate(async () => {
    const cat: any = await import('/js/prepare/catalog.js');
    return (await cat.catalog.heroes()).find((h: any) => h.name === 'Spider-Man').id;
  });
}

test.beforeEach(async ({ page }) => {
  await page.goto('/prepare.html');
  await ficheSetDeBase(page);
});
test.afterAll(async ({ browser }) => {
  const page = await browser.newPage();
  await page.goto('/prepare.html');
  await vider(page);
  await page.close();
});

test('en Legacy, les cartes des boites fermees sont grisees et ne s ajoutent pas', async ({ page }) => {
  const id = await idSpiderMan(page);
  await page.goto(`/deck-builder.html?hero=${encodeURIComponent(id)}&legacy=1`);
  await page.waitForSelector('#db-grille .db-carte', { timeout: 30000 });
  await expect(page.locator('.db-legacy')).toContainText('Legacy');
  const fermees = page.locator('#db-grille .db-carte.est-verrou');
  expect(await fermees.count()).toBeGreaterThan(10);
  await expect(fermees.first().locator('.db-verrou')).not.toBeEmpty();
  // Le bouton « + » d'une carte fermee est inerte, et l'image aussi.
  const premiere = fermees.first();
  await expect(premiere.locator('.db-carte-boutons button').nth(1)).toBeDisabled();
  await premiere.locator('img').click({ force: true });
  await expect(premiere).not.toHaveClass(/est-choisie/);
  // Une carte du Set de base, elle, s'ajoute.
  const ouverte = page.locator('#db-grille .db-carte:not(.est-verrou)').first();
  await ouverte.hover();
  await ouverte.locator('.db-carte-boutons button').nth(1).click();
  await expect(ouverte).toHaveClass(/est-choisie/);
  await page.screenshot({ path: 'C:/tmp/legacy-5-deckbuilder.png' });
});

test('les decks de depart proposes sont ceux qu on peut jouer', async ({ page }) => {
  const id = await idSpiderMan(page);
  await page.goto(`/deck-builder.html?hero=${encodeURIComponent(id)}&legacy=1`);
  // « Partir de » est un menu déroulant depuis la refonte du 09/10/2026.
  await page.waitForSelector('#db-partir optgroup option', { state: 'attached', timeout: 30000 });
  const puces = await page.$$eval('#db-partir optgroup:not([label="Brouillons"]) option', (n) => n.map((x) => x.textContent || ''));
  expect(puces.some((p) => /Base/.test(p))).toBe(true);
  // Les paquets d'aspect du tableur piochent dans toutes les vagues : aucun
  // ne tient au Set de base.
  expect(puces.filter((p) => !/Base/.test(p)).length).toBe(0);
});

// ⚠ SANS LE DRAPEAU, RIEN N'EST VERROUILLE, meme avec le mode actif sur le
// compte. Le jeu libre n'est jamais verrouille.
test('sans le drapeau, le deck-builder ne verrouille rien', async ({ page }) => {
  const id = await idSpiderMan(page);
  await page.goto(`/deck-builder.html?hero=${encodeURIComponent(id)}`);
  await page.waitForSelector('#db-grille .db-carte', { timeout: 30000 });
  await expect(page.locator('#db-grille .db-carte.est-verrou')).toHaveCount(0);
  await expect(page.locator('.db-legacy')).toHaveCount(0);
});
