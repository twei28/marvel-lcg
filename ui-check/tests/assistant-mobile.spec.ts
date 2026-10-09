// L'assistant au doigt. Depuis la refonte téléphone du 09/10/2026
// (.planning/todos/2026-10-09-mode-telephone-refonte.md) : le toucher d'un
// héros le PRÉSENTE dans le bandeau du haut, le bouton « Choisir » du bandeau
// l'assigne, puis l'assistant file aux Decks (plus de fenêtre « Options de ce
// héros »). La fiche s'ouvre depuis « Fiche », en feuille basse. Le rendu PC
// ne change pas.
//
//   npm run assistant-mobile
import { test, expect } from '@playwright/test';

test.describe("L'assistant au telephone", () => {
  test('un toucher presente le heros dans le bandeau, « Choisir » l assigne', async ({ page }) => {
    await page.goto('/prepare.html');
    await page.getByRole('button', { name: /^Solo/ }).first().tap();
    const tuile = page.locator('.tb-port[data-hero="storm"]');
    await tuile.waitFor({ timeout: 30_000 });
    await tuile.tap();
    await expect(page.locator('.ts-titre b')).toContainText(/storm/i);
    await expect(tuile, 'le toucher ne doit PAS choisir le heros').not.toHaveClass(/\bchosen\b/);
    await expect(page.locator('.fiche-heros'), 'plus de fiche ouverte au toucher').toHaveCount(0);
    const choisir = page.locator('.ts-btn.jaune');
    const b = await choisir.boundingBox();
    expect(b!.height, 'le bouton fait au moins 44 px').toBeGreaterThanOrEqual(44);
    await choisir.tap();
    await expect(page.locator('.pstep.active'), 'equipe complete : on file aux decks').toContainText(/decks/i, { timeout: 8_000 });
    await expect(page.locator('.vh-panel'), 'plus de fenetre « Options de ce heros »').toHaveCount(0);
  });

  test('la fiche s ouvre depuis le bandeau, en feuille basse pleine largeur', async ({ page }) => {
    await page.goto('/prepare.html');
    await page.getByRole('button', { name: /^Solo/ }).first().tap();
    const tuile = page.locator('.tb-port[data-hero="storm"]');
    await tuile.waitFor({ timeout: 30_000 });
    await tuile.tap();
    // Atteindre la tuile a fait defiler la grille : le bandeau reduit cache
    // « Fiche ». On remonte, comme le ferait le joueur.
    await page.locator('.tb-droite').evaluate((e) => { e.scrollTop = 0; });
    await page.getByRole('button', { name: /^fiche/i }).tap();
    const fiche = page.locator('.fiche-heros');
    await expect(fiche).toBeVisible();
    await expect(fiche.locator('.fh-art')).toBeVisible();
    await expect(fiche.getByText('Biographie')).toBeVisible();
    const boite = await fiche.boundingBox();
    expect(boite!.width, 'la fiche est pleine largeur').toBeGreaterThanOrEqual(page.viewportSize()!.width - 2);
    await page.touchscreen.tap(240, 20);
    await expect(fiche).toHaveCount(0);
    await expect(tuile).not.toHaveClass(/\bchosen\b/);
  });

  // Un heros sans deck de base (player_deck vide) : pas de deck fantome de
  // 15 cartes, tous les paquets d'aspect du tableur, deplies, le premier
  // paquet legal choisi d'office (decision du 12/09/2026).
  test('un heros sans deck de base recoit tous les paquets d aspect, le premier legal choisi', async ({ page }) => {
    await page.goto('/prepare.html');
    await page.getByRole('button', { name: /^Solo/ }).first().tap();
    await page.locator('.tb-port').first().waitFor({ timeout: 30_000 });
    await page.getByRole('button', { name: /fan-made/i }).first().tap();
    const tuile = page.locator('.tb-port[data-hero="angela"]');
    await tuile.waitFor({ timeout: 15_000 });
    await tuile.tap();
    await page.locator('.ts-btn.jaune').tap();
    await expect(page.locator('.pstep.active')).toContainText(/decks/i, { timeout: 8_000 });
    await page.locator('.do-name').first().waitFor({ timeout: 30_000 });
    await expect(page.locator('.tb-deck .tag', { hasText: /^base$/i })).toHaveCount(0);
    await expect(page.locator('.deck-aspects.est-deplie')).toHaveCount(1);
    expect(await page.locator('.deck-aspects .tb-deck').count()).toBeGreaterThanOrEqual(25);
    const choisi = page.locator('.tb-deck.chosen');
    await expect(choisi.locator('.do-name')).toHaveText('Brutish Aggression');
    await expect(choisi.locator('.do-alerte')).toHaveCount(0);
  });
});
