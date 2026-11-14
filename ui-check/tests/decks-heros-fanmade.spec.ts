// Un héros fan-made sans deck de départ se présente comme un héros officiel (30/10/2026) : « Deck de départ »
// (vide, expliqué), « Decks de la communauté » (où arrivent les decks importés), puis « Proposition de deck… »
// (les paquets d'aspect). Rien n'est choisi à sa place : Continuer attend un deck.
//
//   UI_CHECK_BASE=http://127.0.0.1:2346 npx playwright test tests/decks-heros-fanmade.spec.ts --project=pc
//
// Le test pose un fichier dans deck/custom/ du jeu d'essai (le deck d'un « autre joueur ») et le retire à la fin.
import { test, expect } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

const FICHIER = path.resolve('..', 'Fusion', 'marvel-lcg-src', 'deck', 'custom', 'zz-test-deck-raphael-importe.json');
const DECK = {
  version: '0.5.8', name: 'Raphael custom (de inkwire)', metadata: { url: '' },
  hero: ['tr001a,tr001b'], hero_deck: ['tr002', 'tr003'], set_aside: [], obligations: ['tr013'], nemesis_set: ['tr014'],
  player_deck: ['ua017', '35018', '35018', '35018'],
};

test.beforeEach(() => fs.writeFileSync(FICHIER, JSON.stringify(DECK)));
test.afterEach(() => { try { fs.unlinkSync(FICHIER); } catch { /* déjà retiré */ } });

test('Raphael : trois blocs, deck importé visible en haut, rien de choisi, Continuer attend un deck', async ({ page }) => {
  test.setTimeout(90_000);
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.addInitScript(() => {
    try { localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', 'fr'); localStorage.setItem('mc_affichage_v1', 'epure'); localStorage.setItem('mc_affichage_migre', '2026-10-19'); } catch { /* */ }
  });
  await page.goto('/prepare.html');
  await page.getByRole('button', { name: /^Solo/ }).first().click({ timeout: 30_000 });
  await page.getByRole('button', { name: /^fan-made$/i }).click();
  await page.locator('#hero-grid .tb-port[data-hero="raphael"]').first().click({ timeout: 30_000 });
  const valider = page.locator('.vh-panel, .deck-modal').getByRole('button', { name: /valider/i });
  if (await valider.isVisible({ timeout: 3_000 }).catch(() => false)) await valider.click();
  await page.getByRole('button', { name: /^Continuer/i }).click();

  const liste = page.locator('#deck-liste');
  await expect(liste).toBeVisible({ timeout: 20_000 });
  await expect(liste.locator('.deck-section').nth(0)).toHaveText(/Deck de départ/i);
  await expect(liste.locator('.deck-vide').first()).toContainText('pas de deck de départ');
  await expect(liste.locator('.deck-section').nth(1)).toContainText(/communauté \(1\)/i);
  // Le deck importé est tout en haut, pas enterré sous 29 paquets d'aspect.
  const hautDeck = await liste.locator('.tb-deck', { hasText: 'Raphael custom (de inkwire)' }).first().evaluate((e) => e.getBoundingClientRect().top);
  const hautListe = await liste.evaluate((e) => e.getBoundingClientRect().top);
  expect(hautDeck - hautListe, 'le deck importé est dans le premier écran').toBeLessThan(400);
  await expect(liste.locator('.tb-deck')).toHaveCount(1);
  await expect(liste.getByRole('button', { name: /Proposition de deck/i })).toBeVisible();
  await page.screenshot({ path: '../.planning/captures-page-difficulte/decks-fanmade.png' });

  // Rien n'est choisi d'office : Continuer attend.
  await expect(page.getByRole('button', { name: /^Continuer/i })).toBeDisabled();
  await liste.locator('.tb-deck', { hasText: 'Raphael custom (de inkwire)' }).first().click();
  await expect(page.getByRole('button', { name: /^Continuer/i })).toBeEnabled();

  // Choisir un deck propose les arts alternatifs : on referme cette fenêtre.
  if (await page.locator('.ac-modal').isVisible({ timeout: 2_000 }).catch(() => false)) await page.locator('.ac-modal [data-ac="non"]').click();

  // Les paquets d'aspect sont derrière le bouton.
  await liste.getByRole('button', { name: /Proposition de deck/i }).click();
  await expect(page.getByText('Brutish Aggression').first()).toBeVisible();
});
