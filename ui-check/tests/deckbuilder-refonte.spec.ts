// L'éditeur de deck refait (09/10/2026) : trois colonnes, aperçu, résumé,
// onglets Liste / Statistiques / Pioche, rail des filtres sous 1600 px,
// barre du bas sur mobile.
//
//   npx playwright test tests/deckbuilder-refonte.spec.ts --project=pc
//
// ⚠ Aucun test n'enregistre dans le jeu : /save_deck écrit dans deck/custom/,
// le vrai dossier des decks du joueur.
import { test, expect, type Page } from '@playwright/test';

async function ouvrir(page: Page, url = '/deck-builder.html?hero=colossus&deck=colossus') {
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(String(e)));
  await page.goto('/main.html');
  await page.evaluate(() => { localStorage.setItem('marvel-langue', 'fr'); localStorage.removeItem('mc-deckbuilder-drafts'); localStorage.removeItem('mc-deckbuilder-filtres-replies'); });
  await page.goto(url);
  await page.waitForSelector('#db-grille .db-carte', { timeout: 60000 });
  return erreurs;
}
const nombreGrille = async (page: Page) => Number((await page.locator('#db-grille-info b').innerText()).trim());

test.describe('1920 px', () => {
  test.use({ viewport: { width: 1920, height: 1080 } });

  test('trois colonnes, deck de base valide, aperçu du héros', async ({ page }) => {
    const erreurs = await ouvrir(page);
    await expect(page.locator('#db-filtres-col')).toBeVisible();
    await expect(page.locator('#db-deck-col')).toBeVisible();
    await expect(page.locator('#db-filtres .db-sec[data-section="aspects"] .db-chip').first()).toBeVisible();
    await expect(page.locator('.db-valide')).toHaveText(/VALIDE/);
    await expect(page.locator('.db-total b')).toHaveText('25 + 15 = 40');
    await expect(page.locator('#db-apercu img')).toHaveAttribute('src', /32001a/);
    // Aspects par défaut : ceux du deck et Basique.
    await expect(page.locator('.db-chip.est-actif[data-aspect]')).toHaveCount(2);
    await expect(page.locator('#db-save-game')).toBeEnabled();
    expect(erreurs.join(' | ')).toBe('');
  });

  test('clic gauche ajoute, clic droit retire, le badge et la ligne suivent', async ({ page }) => {
    const erreurs = await ouvrir(page, '/deck-builder.html?hero=colossus');
    await expect(page.locator('#db-deck .db-ligne')).toHaveCount(0);
    const tuile = page.locator('#db-grille .db-carte:not(.est-verrou)').first();
    const id = await tuile.getAttribute('data-carte');
    await tuile.click();
    await expect(tuile.locator('.db-badge')).toHaveText(/^1\//);
    await expect(page.locator(`#db-deck .db-ligne[data-carte="${id}"] .db-ligne-n`)).toHaveText('×1');
    await tuile.click({ button: 'right' });
    await expect(tuile.locator('.db-badge')).toHaveCount(0);
    await expect(page.locator(`#db-deck .db-ligne[data-carte="${id}"]`)).toHaveCount(0);
    // Deck invalide : pas d'enregistrement, la liste des problèmes s'ouvre.
    await tuile.click();
    await expect(page.locator('#db-save-game')).toBeDisabled();
    await page.keyboard.press('Control+s');
    await expect(page.locator('.db-problemes')).toContainText('Deck trop petit');
    await expect(page.locator('#db-status')).toHaveClass(/est-erreur/);
    expect(erreurs.join(' | ')).toBe('');
  });

  test('au maximum : badge plein, plus grisé, carte assombrie', async ({ page }) => {
    await ouvrir(page);
    const pleine = page.locator('#db-grille .db-carte.est-max').first();
    await page.locator('#db-recherche').fill('Powerful Punch');
    await expect(page.locator('#db-grille .db-carte.est-max').first()).toBeVisible();
    await expect(pleine.locator('.db-badge')).toHaveText('3/3');
    await expect(pleine.locator('button[data-action="plus"]')).toBeDisabled();
  });

  test('brouillon automatique, même invalide, proposé dans « Partir de »', async ({ page }) => {
    await ouvrir(page, '/deck-builder.html?hero=colossus');
    await page.locator('#db-grille .db-carte:not(.est-verrou)').first().click();
    await page.waitForTimeout(900);
    const n = await page.evaluate(() => Object.keys(JSON.parse(localStorage.getItem('mc-deckbuilder-drafts') || '{}')).length);
    expect(n).toBe(1);
    await expect(page.locator('#db-partir optgroup[label="Brouillons"] option')).toHaveCount(1);
  });

  test('« Partir de » demande confirmation avant de remplacer le deck', async ({ page }) => {
    await ouvrir(page);
    await page.locator('#db-partir').selectOption('vide');
    await expect(page.locator('#db-modale')).toBeVisible();
    await page.locator('#db-modale button', { hasText: 'Annuler' }).click();
    await expect(page.locator('.db-total b')).toHaveText('25 + 15 = 40');
    await page.locator('#db-partir').selectOption('vide');
    await page.locator('#db-modale .db-oui').click();
    await expect(page.locator('.db-total b')).toHaveText('0 + 15 = 15');
    await expect(page.locator('.db-valide')).toHaveText(/problème/);
  });

  test('syntaxe courte, aide, étiquette de filtre', async ({ page }) => {
    await ouvrir(page);
    await page.locator('#db-recherche').fill('ty:allié c:3');
    await page.waitForTimeout(300);
    const avec = await nombreGrille(page);
    expect(avec).toBeGreaterThan(0);
    await page.locator('#db-recherche').fill('ty:allié c:3 zzzz-rien');
    await page.waitForTimeout(300);
    expect(await nombreGrille(page)).toBe(0);
    await page.locator('#db-aide').click();
    await expect(page.locator('#db-aide-texte')).toContainText('t:avenger');
    await page.keyboard.press('Escape');
    await expect(page.locator('#db-aide-texte')).toBeHidden();
    // L'étiquette des aspects retire le filtre d'un clic.
    const avant = await nombreGrille(page);
    await page.locator('#db-recherche').fill('');
    await page.locator('#db-etiquettes button').first().click();
    await expect(page.locator('.db-chip.est-actif[data-aspect]')).toHaveCount(0);
    expect(await nombreGrille(page)).toBeGreaterThan(avant);
  });

  test('fan-made caché par défaut pour un héros officiel, interrupteur sans mémoire', async ({ page }) => {
    await ouvrir(page);
    await expect(page.locator('.db-chip[data-aspect="Determination"]')).toHaveCount(0);
    await page.locator('.db-inter').click();
    await expect(page.locator('.db-chip[data-aspect="Determination"]')).toHaveCount(1);
    await page.reload();
    await page.waitForSelector('#db-grille .db-carte', { timeout: 60000 });
    await expect(page.locator('#db-fanmade')).not.toBeChecked();
  });

  test('onglets Statistiques et Pioche, chances d une carte survolée', async ({ page }) => {
    const erreurs = await ouvrir(page);
    await page.locator('#db-onglets [data-onglet="stats"]').click();
    await expect(page.locator('#db-deck .db-stats')).toContainText('Ressources générées');
    await page.locator('#db-onglets [data-onglet="pioche"]').click();
    // Colossus : alter ego Piotr Rasputin, 6 cartes.
    const main = page.locator('#db-deck .db-main img');
    const taille = await main.count();
    expect(taille).toBeGreaterThanOrEqual(4);
    await page.locator('.db-pboutons button', { hasText: 'Piocher 1' }).click();
    await expect(main).toHaveCount(taille + 1);
    await page.locator('.db-pboutons button', { hasText: 'Nouvelle main' }).click();
    await expect(main).toHaveCount(taille);
    await main.first().hover();
    await expect(page.locator('.db-proba')).toContainText('En main de départ');
    await page.screenshot({ path: 'test-results/deckbuilder-refonte/1920-pioche.png' });
    expect(erreurs.join(' | ')).toBe('');
  });

  test('clic sur le nom d une ligne : aperçu épinglé', async ({ page }) => {
    await ouvrir(page);
    const ligne = page.locator('#db-deck .db-ligne').first();
    const id = await ligne.getAttribute('data-carte');
    await ligne.locator('.db-ligne-nom').click();
    await expect(page.locator('#db-apercu .db-epingle')).toBeVisible();
    await page.locator('#db-grille .db-carte').nth(3).hover();
    await expect(page.locator('#db-apercu img')).toHaveAttribute('src', new RegExp(id!));
    await page.keyboard.press('Escape');
    await expect(page.locator('#db-apercu .db-epingle')).toHaveCount(0);
    await page.screenshot({ path: 'test-results/deckbuilder-refonte/1920.png' });
  });
});

test.describe('1366 px', () => {
  test.use({ viewport: { width: 1366, height: 768 } });
  test('filtres en rail, ouverts en panneau', async ({ page }) => {
    const erreurs = await ouvrir(page);
    await expect(page.locator('#db-rail')).toBeVisible();
    await expect(page.locator('#db-filtres')).toBeHidden();
    await page.screenshot({ path: 'test-results/deckbuilder-refonte/1366.png' });
    await page.locator('#db-rail button').nth(2).click();
    await expect(page.locator('#db-filtres .db-sec[data-section="couts"]')).toBeVisible();
    await page.screenshot({ path: 'test-results/deckbuilder-refonte/1366-panneau.png' });
    await page.keyboard.press('Escape');
    await expect(page.locator('#db-filtres')).toBeHidden();
    expect(erreurs.join(' | ')).toBe('');
  });
});

test.describe('mobile', () => {
  test.use({ viewport: { width: 480, height: 1050 }, hasTouch: true, isMobile: true });
  test('grille plein écran, barre du bas, panneaux', async ({ page }) => {
    const erreurs = await ouvrir(page);
    await expect(page.locator('#db-deck-col')).toBeHidden();
    await expect(page.locator('#db-mob-deck')).toContainText('Deck (40)');
    await page.screenshot({ path: 'test-results/deckbuilder-refonte/mobile.png' });
    await page.locator('#db-mob-deck').click();
    await expect(page.locator('#db-deck-col')).toBeVisible();
    await expect(page.locator('#db-deck .db-ligne').first()).toBeVisible();
    await page.screenshot({ path: 'test-results/deckbuilder-refonte/mobile-deck.png' });
    await page.locator('#db-deck-col .db-fermer-panneau').click();
    await page.locator('#db-mob-filtres').click();
    await expect(page.locator('#db-filtres')).toBeVisible();
    await page.screenshot({ path: 'test-results/deckbuilder-refonte/mobile-filtres.png' });
    expect(erreurs.join(' | ')).toBe('');
  });
});
