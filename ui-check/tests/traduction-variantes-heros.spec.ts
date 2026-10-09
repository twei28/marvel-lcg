// La fenêtre « Options de ce héros » montre les scans HD ANGLAIS des arts du
// héros. Jeu en français : la traduction est posée dessus (public/js/traduction),
// et elle suit quand on change d'art avec les flèches.
import { test, expect, type Page } from '@playwright/test';

async function ouvrirModale(page: Page, heros: string) {
  await page.addInitScript(() => localStorage.setItem('marvel-langue', 'fr'));
  await page.goto('/prepare.html');
  await page.getByRole('button', { name: /^Solo/ }).first().click();
  await page.locator(`.tb-port[data-hero="${heros}"]`).first().click();
  await expect(page.locator('.vh-panel')).toBeVisible();
}

/** Avance le carrousel de la face héros jusqu'à l'art nommé `nom`. */
async function allerA(page: Page, nom: RegExp) {
  const carrousel = page.locator('.vh-panel .ca').first();
  for (let i = 0; i < 6; i += 1) {
    if (nom.test(await carrousel.locator('.ca-nom').innerText())) return;
    // « Même série » coché : seule la flèche droite de l'alter ego est visible.
    await page.locator('.vh-panel .ca-fleche-d:visible').last().click();
  }
  throw new Error(`art ${nom} introuvable`);
}

test('Black Widow, série Comic : la traduction est posée sur les deux faces', async ({ page }) => {
  await ouvrirModale(page, 'black_widow');
  await allerA(page, /Comic/);
  const poses = page.locator('.vh-panel .ca-cadre .traduction-posee');
  await expect(poses).toHaveCount(2, { timeout: 15000 });
  await expect(poses.first()).toContainText(/[éèàç]|Réponse/);
  await page.waitForTimeout(800);
  await page.locator('.vh-panel').screenshot({ path: 'test-results/variantes-black-widow-comic.png' });
});

test('Spider-Man, série M3T4LB0X : la traduction suit le changement d’art', async ({ page }) => {
  await ouvrirModale(page, 'spider_man');
  await allerA(page, /M3T4LB0X/);
  const carrousel = page.locator('.vh-panel .ca').first();
  await expect(carrousel.locator('.traduction-posee')).toHaveCount(1, { timeout: 15000 });
  await page.waitForTimeout(800);
  await page.locator('.vh-panel').screenshot({ path: 'test-results/variantes-spider-man-m3t.png' });
});
