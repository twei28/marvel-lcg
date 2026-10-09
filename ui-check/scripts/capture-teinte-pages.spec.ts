// VERIFICATION PONCTUELLE (04/10/2026) : la teinte du fond « partout »,
// etape 2. La preparation applique la teinte EN DIRECT apres « Valider », et
// les 12 pages du site prennent la teinte rangee dans le navigateur.
// Moteur d'ESSAI seulement. Range HORS de tests/ : le copier dans tests/ le
// temps de le lancer, puis l'en retirer.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

const SORTIE = process.env.SORTIE_CAPTURES || path.resolve('captures-tmp');
const PAGES = [
  'prepare.html', 'campagne.html', 'cards.html', 'deck.html', 'deck-builder.html',
  'galerie.html', 'palettes-heros.html', 'rejoindre.html', 'salon.html', 'replay.html', 'scene.html',
];
const fondDuCorps = (page: Page) => page.evaluate(() => getComputedStyle(document.body).backgroundImage + ' | ' + getComputedStyle(document.body).backgroundColor);

test('preparation : la teinte s applique des « Valider », sans recharger', async ({ page }) => {
  fs.mkdirSync(SORTIE, { recursive: true });
  await page.setViewportSize({ width: 1600, height: 1000 });
  await page.goto('/prepare.html', { waitUntil: 'networkidle' });
  const francais = page.getByRole('button', { name: /^Français/ });
  if (await francais.count()) await francais.first().click();
  const fenetre = page.locator('.affichage-modal');
  await expect(fenetre).toBeVisible({ timeout: 15_000 });
  const avant = await fondDuCorps(page);
  // Une teinte saturee (fleches : teinte et saturation), puis plus claire.
  const disque = fenetre.locator('.rt-disque');
  await disque.focus();
  for (let i = 0; i < 10; i++) await page.keyboard.press('ArrowUp');
  await fenetre.getByLabel('Luminosité du fond').fill('40');
  await fenetre.getByRole('button', { name: /^Valider/ }).click();
  await expect(fenetre).toHaveCount(0);
  await expect(page.locator('html')).toHaveAttribute('data-teinte', /^(sombre|claire)$/);
  const apres = await fondDuCorps(page);
  expect(apres).not.toBe(avant);
  await page.screenshot({ path: path.join(SORTIE, 'teinte-pages-prepare-apres-valider.png') });
});

for (const [nom, valeur] of [['brun', '30,14,40'], ['sauge', '140,12,18']] as const) {
  for (const fichier of PAGES) {
    test(`${fichier} prend la teinte ${nom}`, async ({ page }) => {
      fs.mkdirSync(SORTIE, { recursive: true });
      await page.setViewportSize({ width: 1440, height: 900 });
      // Langue et affichage deja choisis : aucune fenetre d'accueil par-dessus.
      await page.addInitScript((v) => {
        try {
          localStorage.setItem('mc_affichage_v1', 'normal');
          localStorage.setItem('marvel-langue', 'fr');
          localStorage.setItem('marvel-langue-choisie', '1');
          localStorage.setItem('mc_teinte_v1', v);
        } catch { /* */ }
      }, valeur);
      await page.goto('/' + fichier, { waitUntil: 'networkidle' });
      await page.waitForTimeout(1200);
      await expect(page.locator('html')).toHaveAttribute('data-teinte', 'sombre');
      await page.screenshot({ path: path.join(SORTIE, `teinte-pages-${nom}-${fichier.replace('.html', '')}.png`) });
    });
  }
}
