// L'assistant au doigt (spec du 07/09/2026, §6.2) : la FICHE DU HEROS AU TAP.
//
// Sans survol, rien ne presentait un heros avant de le choisir : le tap
// l'assignait d'un coup. Le premier tap ouvre une fiche (portrait, traits,
// PV, biographie, « Voir ses cartes ») ; « Choisir ce heros », ou un second
// tap sur la meme tuile, l'assigne. Le rendu PC ne change pas.
//
//   npm run assistant-mobile
import { test, expect } from '@playwright/test';

test.describe("L'assistant au telephone", () => {
  test('le premier tap sur un heros ouvre sa fiche, « Choisir ce heros » l assigne', async ({ page }) => {
    await page.goto('/prepare.html');
    await page.getByRole('button', { name: /^Solo/ }).first().tap();
    const tuile = page.locator('.tb-port[data-hero="storm"]');
    await tuile.waitFor({ timeout: 30_000 });
    await tuile.tap();
    const fiche = page.locator('.fiche-heros');
    await expect(fiche, 'la fiche du heros ne s’est pas ouverte').toBeVisible();
    await expect(fiche.locator('.fh-art')).toBeVisible();
    await expect(fiche.getByText('Biographie')).toBeVisible();
    await expect(tuile, 'le premier tap ne doit PAS choisir le heros').not.toHaveClass(/\bchosen\b/);
    const boite = await fiche.boundingBox();
    expect(boite!.width, 'la fiche est pleine largeur').toBeGreaterThanOrEqual(page.viewportSize()!.width - 2);
    const choisir = fiche.getByRole('button', { name: /choisir ce héros/i });
    const b = await choisir.boundingBox();
    expect(b!.height, 'le bouton fait au moins 44 px').toBeGreaterThanOrEqual(44);
    await choisir.tap();
    await expect(fiche).toHaveCount(0);
    await expect(tuile).toHaveClass(/\bchosen\b/);
    await expect(page.getByRole('button', { name: /continuer/i }).first()).toBeEnabled();
  });

  test('un second tap sur la meme tuile choisit sans rouvrir la fiche', async ({ page }) => {
    await page.goto('/prepare.html');
    await page.getByRole('button', { name: /^Solo/ }).first().tap();
    const tuile = page.locator('.tb-port[data-hero="storm"]');
    await tuile.waitFor({ timeout: 30_000 });
    await tuile.tap();
    await expect(page.locator('.fiche-heros')).toBeVisible();
    // On referme la fiche d'un tap a cote, puis on retape la tuile.
    await page.touchscreen.tap(240, 20);
    await expect(page.locator('.fiche-heros')).toHaveCount(0);
    await tuile.tap();
    await expect(page.locator('.fiche-heros')).toHaveCount(0);
    await expect(tuile).toHaveClass(/\bchosen\b/);
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
    await page.locator('.fiche-heros').getByRole('button', { name: /choisir ce héros/i }).tap();
    await page.getByRole('button', { name: /continuer/i }).first().tap();
    await page.locator('.do-name').first().waitFor({ timeout: 30_000 });
    await expect(page.locator('.tb-deck .tag', { hasText: /^base$/i })).toHaveCount(0);
    await expect(page.locator('.deck-aspects.est-deplie')).toHaveCount(1);
    expect(await page.locator('.deck-aspects .tb-deck').count()).toBeGreaterThanOrEqual(25);
    const choisi = page.locator('.tb-deck.chosen');
    await expect(choisi.locator('.do-name')).toHaveText('Brutish Aggression');
    await expect(choisi.locator('.do-alerte')).toHaveCount(0);
  });
});
