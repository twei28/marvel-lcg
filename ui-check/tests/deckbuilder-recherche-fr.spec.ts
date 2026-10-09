// La recherche de l'editeur de deck trouve une carte par son nom francais
// OFFICIEL (noms-fr.js), sans accent, comme par son nom anglais.
import { test, expect } from '@playwright/test';

async function chercher(page: import('@playwright/test').Page, requete: string): Promise<string> {
  await page.locator('.db-recherche').fill(requete);
  await page.waitForTimeout(500);
  return page.locator('#db-grille').innerText();
}

test('recherche par nom francais, anglais et sans accent', async ({ page }) => {
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(String(e)));
  await page.goto('/deck-builder.html?hero=spider_man');
  await page.waitForSelector('.db-chip', { timeout: 30000 });

  const compte = async () => Number((await page.locator('#db-grille-info').innerText()).match(/\d+/)![0]);

  await chercher(page, 'Manoir des Avengers');
  expect(await compte(), 'nom francais introuvable').toBeGreaterThan(0);
  await chercher(page, 'heliporteur');
  expect(await compte(), 'nom francais sans accent introuvable').toBeGreaterThan(0);
  await chercher(page, 'Avengers Mansion');
  expect(await compte(), 'nom anglais introuvable').toBeGreaterThan(0);
  await chercher(page, 'zzzz-rien');
  expect(await compte()).toBe(0);
  expect(erreurs.join(' | '), 'erreur JS dans l editeur').toBe('');
});
