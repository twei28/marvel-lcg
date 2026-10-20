// Backlog 9 : en coop locale, le deck de chaque heros se choisit puis se VALIDE,
// l'un apres l'autre ; aucun deck n'est retenu d'office. Le solo ne change pas.
//
// Drapeau : COOP_DECKS_SEQUENTIELS dans public/js/prepare/app.js.
// Captures : dossier donne par CAPTURES_COOP (defaut : captures-tmp/backlog-9).
import { test, expect, type Page } from '@playwright/test';
import path from 'node:path';

const DOSSIER = process.env.CAPTURES_COOP || path.join(__dirname, '..', 'captures-tmp', 'backlog-9');

async function recruter(page: Page, nom: RegExp) {
  await page.getByRole('button', { name: nom }).first().click();
  const options = page.locator('.deck-modal');
  if (await options.count()) await options.getByRole('button', { name: /valider/i }).click();
  await expect(options).toHaveCount(0);
}

/** Un clic sur le premier deck ; la question des arts alternatifs, si elle s'ouvre, recoit « Non ». */
async function choisirPremierDeck(page: Page) {
  await page.locator('.tb-deck').first().click();
  const non = page.locator('.deck-modal').getByRole('button', { name: /^non$/i });
  try { await non.click({ timeout: 3000 }); } catch { /* pas de question pour ce heros */ }
  await expect(page.locator('.deck-modal')).toHaveCount(0);
}

async function ouvrir(page: Page, mode: RegExp, nombre?: number) {
  await page.goto('/prepare.html?ui=new', { waitUntil: 'load' });
  if (nombre) {
    await page.locator('.acc-tuile', { has: page.getByRole('button', { name: mode }) })
      .locator(`.acc-nombre[title^="${nombre} "]`).click();
  } else {
    await page.getByRole('button', { name: mode }).first().click();
  }
}

test.use({ viewport: { width: 1280, height: 720 } });

test.describe('Coop locale : decks un heros apres l autre', () => {
  test('2 heros de bout en bout, sans deck par defaut', async ({ page }) => {
    await ouvrir(page, /^Coop locale/, 2);
    await recruter(page, /^Spider-Man/);
    await recruter(page, /^Iron Man/);
    await page.getByRole('button', { name: /continuer/i }).click();

    // Etape Decks : rien n'est choisi, le bouton de validation est bloque,
    // et « Continuer » n'existe pas.
    const valider = page.locator('#btn-valider-deck');
    await expect(valider).toBeVisible({ timeout: 30_000 });
    await expect(valider).toBeDisabled();
    await expect(page.getByRole('button', { name: /^continuer$/i })).toHaveCount(0);
    await expect(page.locator('.tb-deck.chosen')).toHaveCount(0);
    await expect(page.locator('.tb-tampons')).toContainText('Aucun deck choisi');
    await page.screenshot({ path: path.join(DOSSIER, '1-coop-heros1-aucun-deck.png') });

    // Le siege 2 est verrouille tant que le heros 1 n'a pas valide.
    await page.locator('.tb-siege').nth(1).click();
    await expect(page.locator('.tb-siege').nth(0)).toHaveClass(/actif/);

    // Heros 1 : un clic sur un deck (le deck de depart, explicitement).
    await choisirPremierDeck(page);
    await expect(page.locator('.tb-deck.chosen')).toHaveCount(1);
    await expect(valider).toBeEnabled();
    await page.screenshot({ path: path.join(DOSSIER, '2-coop-heros1-deck-choisi.png') });
    await valider.click();

    // Heros 2 : de nouveau rien de choisi.
    await expect(page.locator('.tb-siege').nth(1)).toHaveClass(/actif/);
    await expect(page.locator('.tb-deck.chosen')).toHaveCount(0);
    await expect(page.locator('#btn-valider-deck')).toBeDisabled();
    await page.screenshot({ path: path.join(DOSSIER, '3-coop-heros2-aucun-deck.png') });
    await choisirPremierDeck(page);
    await page.locator('#btn-valider-deck').click();

    // Tous valides : « Continuer » revient, le mechant suit, puis le lancement.
    const continuer = page.getByRole('button', { name: /^continuer$/i });
    await expect(continuer).toBeEnabled();
    await page.screenshot({ path: path.join(DOSSIER, '4-coop-tous-valides.png') });
    await continuer.click();
    await page.getByRole('button', { name: /^Rhino\b/ }).first().click();
    await page.getByRole('button', { name: /^continuer$/i }).click();
    await expect(page.getByRole('button', { name: /lancer la partie/i })).toBeEnabled();
    await page.screenshot({ path: path.join(DOSSIER, '5-coop-final.png') });
  });

  test('solo temoin : un seul ecran de deck, deck de base retenu, Continuer direct', async ({ page }) => {
    await ouvrir(page, /^Solo/);
    await recruter(page, /^Spider-Man/);
    await page.getByRole('button', { name: /^continuer$/i }).click();
    await expect(page.locator('.tb-deck.chosen')).toHaveCount(1, { timeout: 30_000 });
    await expect(page.locator('#btn-valider-deck')).toHaveCount(0);
    await expect(page.getByRole('button', { name: /^continuer$/i })).toBeEnabled();
    await page.screenshot({ path: path.join(DOSSIER, '6-solo-temoin-decks.png') });
  });
});
