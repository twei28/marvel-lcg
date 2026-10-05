// LA FENÊTRE DES ÉTAPES DU MÉCHANT SE DÉPLACE À LA VRAIE SOURIS.
//
// ⚠ POURQUOI CE FICHIER EXISTE. Signalement Yarro #37 puis retour du
// 01/10/2026 : « je ne peux toujours pas bouger la fenêtre des étapes ». La
// poignée (le bandeau rouge, une trentaine de pixels) était quittée par la
// souris avant le seuil de 6 px où le hook posait la capture : les mouvements
// partaient vers l'élément dessous. Les tests unitaires appelaient les
// gestionnaires à la main et passaient. Ici : vraie souris, vrai navigateur.
//
//   npm run glisser-fenetre-etapes
//
// ⚠ IL NE LANCE AUCUNE PARTIE : il lit une page d'état figée (?etat=).
import { test, expect } from '@playwright/test';

test('glisser la fenêtre des étapes par son bandeau', async ({ page }) => {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.route('**/get_site_admin', (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ url: 'test' }) }));
  await page.goto('/app/board.html');
  await page.evaluate(() => localStorage.setItem('marvel-langue-choisie', '1'));
  await page.goto('/app/board.html?etat=rhino__spider_man__phase-mechant-complet.js');
  await page.waitForSelector('.deroule-phase .deroule-ligne-haut', { timeout: 30000 });
  await page.waitForTimeout(2500);

  const fenetre = page.locator('.deroule-phase').first();
  const chrono = page.locator('.deroule-phase .deroule-ligne-haut').first();
  const avant = (await fenetre.boundingBox())!;
  const c = (await chrono.boundingBox())!;
  const x = c.x + c.width - 40;
  const y = c.y + c.height / 2;

  await page.mouse.move(x, y);
  await page.mouse.down();
  await page.mouse.move(x - 150, y - 200, { steps: 8 });
  await page.mouse.up();

  const apres = (await fenetre.boundingBox())!;
  expect(Math.round(apres.x - avant.x)).toBe(-150);
  expect(Math.round(apres.y - avant.y)).toBe(-200);

  await page.locator('.deroule-phase button:has-text("Suivant")').first().click();
  await page.waitForTimeout(1200);
  const apresSuivant = (await fenetre.boundingBox())!;
  expect(Math.round(apresSuivant.x)).toBe(Math.round(apres.x));
});
