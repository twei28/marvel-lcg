// L'import d'un fichier OCTGN (.o8d) dans la preparation, pour de vrai (16/10/2026) :
// le fichier est celui d'un Beast fan-made (« Brain over Brawl »), importe sur Adam Warlock (quatre aspects permis).
import { test, expect } from '@playwright/test';
import path from 'node:path';

const FICHIER = path.resolve('tests', 'fixtures', 'Beast_Brain_over_Brawl.o8d');

test("un .o8d s'importe sur le heros du siege et dit ce qu'il n'a pas pu reprendre", async ({ page }) => {
  test.setTimeout(90_000);
  await page.addInitScript(() => {
    localStorage.setItem('marvel-langue-choisie', '1');
    localStorage.setItem('mc_affichage_v1', 'normal');
  });
  const dits: string[] = [];
  // Le deck n'est legal pour aucun heros (cartes d'un autre Beast, trois exemplaires...) : le jeu propose de
  // forcer, et forcer ENVOIE un rapport au serveur. On l'intercepte : le test ne doit rien poster.
  await page.route('**/post_rapport_bug', (r) => r.fulfill({ status: 200, body: 'ok' }));
  page.on('dialog', async (d) => {
    dits.push(d.message());
    // 1er dialogue : « importer quand meme ? » -> OK ; le dernier (« sauvegarder ? ») -> Annuler.
    if (/sauvegarder/i.test(d.message())) await d.dismiss(); else await d.accept();
  });

  await page.goto('/prepare.html?ui=new', { waitUntil: 'load' });
  await page.getByRole('button', { name: /^Solo/ }).first().click();
  await page.getByRole('button', { name: /^Adam Warlock/ }).first().click();
  // « Options de ce heros » s'ouvre au choix d'un heros : on valide sans rien changer.
  await page.locator('.deck-modal').getByRole('button', { name: 'Valider' }).click();
  await page.getByRole('button', { name: /continuer/i }).click();
  await expect(page.locator('#mcdb-0')).toBeVisible();

  await page.locator('#o8d-0').setInputFiles(FICHIER);
  await expect.poll(() => dits.some((m) => /sauvegarder/i.test(m)), { timeout: 20_000 }).toBe(true);
  const message = dits.find((m) => /sauvegarder/i.test(m)) as string;
  expect(message, 'le nom du deck vient du fichier').toMatch(/Beast Brain over Brawl/);
  // Les cartes propres a l'autre Beast sont dites, pas avalees.
  expect(message).toMatch(/Addition by Subtraction/);
  expect(message).toMatch(/non reprises/);

  const range = await page.evaluate(() => {
    const o = JSON.parse(localStorage.getItem('mc_prepare_prefs_v1') || '{}');
    return (o.savedDecks || []).slice(-1)[0] ?? null;
  });
  // On n'a pas accepte de sauvegarder (dismiss) : le deck est dans la preparation, pas range.
  expect(range).toBeNull();
});

test("l'accueil a une tuile « Éditeur de deck » qui ouvre l'éditeur", async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('marvel-langue-choisie', '1');
    localStorage.setItem('mc_affichage_v1', 'normal');
  });
  await page.goto('/prepare.html', { waitUntil: 'load' });
  const tuile = page.getByRole('button', { name: /[EÉ]diteur de deck/ });
  await expect(tuile).toBeVisible();
  await page.screenshot({ path: 'test-results/accueil-editeur.png' });
  await tuile.click();
  await page.waitForURL('**/deck-builder.html', { timeout: 15_000 });
  await expect(page.locator('.db-chip').first()).toBeVisible({ timeout: 30_000 });
});
