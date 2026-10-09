// L'editeur de deck montre les illustrations des cartes reimprimees avec un
// autre art (arts-reeditions.js) et laisse choisir celle du deck. Depuis la
// refonte du 09/10/2026, le choix se fait par les vignettes « ARTS » posees a
// cote de l'apercu.
import { test, expect } from '@playwright/test';

test('choisir l illustration d une carte reimprimee', async ({ page }) => {
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(String(e)));
  await page.goto('/deck-builder.html?hero=spider_man');
  await page.evaluate(() => localStorage.setItem('marvel-langue', 'en'));
  await page.reload();
  await page.waitForSelector('.db-chip', { timeout: 30000 });
  await page.locator('.db-recherche').fill('Power of Leadership');
  await page.waitForTimeout(500);

  const tuile = page.locator('#db-grille .db-carte').first();
  await expect(tuile).toHaveAttribute('data-carte', '01072');
  await tuile.hover();
  const choix = page.locator('#db-arts img');
  await expect(choix).toHaveCount(2);
  await page.screenshot({ path: 'test-results/arts-reeditions-choix.png' });

  // Une copie dans le deck, puis on passe sur l'autre art : la copie suit.
  await tuile.locator('button[data-action="plus"]').click();
  await expect(page.locator('#db-deck .db-ligne[data-carte="01072"]')).toHaveCount(1);
  await page.locator('#db-arts img[data-version="45019"]').click();
  await expect(page.locator('#db-grille .db-carte').first()).toHaveAttribute('data-carte', '45019');
  await expect(page.locator('#db-deck .db-ligne[data-carte="45019"]')).toHaveCount(1);
  await expect(page.locator('#db-deck .db-ligne[data-carte="01072"]')).toHaveCount(0);
  await expect(page.locator('#db-deck .db-ligne[data-carte="45019"] .db-ligne-n')).toHaveText('×1');
  await expect(page.locator('#db-arts img.est-active')).toHaveAttribute('data-version', '45019');
  await page.waitForTimeout(1500);
  await page.locator('#db-grille').screenshot({ path: 'test-results/arts-reeditions-apres.png' });
  expect(erreurs.join(' | '), 'erreur JS dans l editeur').toBe('');
});

test('en francais, pas de choix d illustration (scans FR identiques)', async ({ page }) => {
  await page.goto('/deck-builder.html?hero=spider_man');
  await page.evaluate(() => localStorage.setItem('marvel-langue', 'fr'));
  await page.reload();
  await page.waitForSelector('.db-chip', { timeout: 30000 });
  await page.locator('.db-recherche').fill('Power of Leadership');
  await page.waitForTimeout(500);
  await expect(page.locator('#db-grille .db-carte')).toHaveCount(1);
  await page.locator('#db-grille .db-carte').first().hover();
  await expect(page.locator('#db-arts img')).toHaveCount(0);
});
