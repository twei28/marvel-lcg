// L'aide des tuiles de mode, sur l'ecran d'accueil.
//
// Les cinq tuiles ne portaient qu'un sous-titre de trois mots. « Bac a sable »
// et « Bataille » ne disent rien a qui ne connait pas le jeu, et « Coop
// locale » cache son second usage : une seule personne qui joue plusieurs
// heros. Une phrase par tuile, au survol.
//
// Trois choses a tenir, et aucune ne se voit dans le code :
//   1. la bulle est CACHEE au repos et sort au survol ;
//   2. elle sort AUSSI au clavier, sans quoi elle n'existe pas pour qui
//      navigue au Tab ;
//   3. elle ne bloque RIEN : elle deborde sous la tuile, et sans
//      `pointer-events:none` elle passerait devant celle d'en dessous, qui ne
//      repondrait plus au clic.
//
//   npm run aide-modes
import { test, expect } from '@playwright/test';

// ⚠ LA BULLE EST HORS DU BOUTON, ET C'EST OBLIGATOIRE. Les tuiles portent un
// `clip-path` pour leur coin coupe, qui DECOUPE tout ce qu'elles contiennent :
// une bulle placee a l'interieur existait pour le navigateur et pour ces tests,
// et n'apparaissait a l'ecran nulle part. D'ou l'enveloppe `.acc-tuile`, qui
// tient le bouton ET sa bulle.
test.beforeEach(async ({ page }) => {
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-mode', { timeout: 20000 });
});

test('chaque tuile porte sa phrase, et une seule', async ({ page }) => {
  const tuiles = page.locator('.acc-tuile');
  const combien = await tuiles.count();
  expect(combien).toBeGreaterThanOrEqual(5);
  for (let i = 0; i < combien; i++) {
    const aides = tuiles.nth(i).locator('.acc-aide');
    await expect(aides).toHaveCount(1);
    const texte = (await aides.textContent())?.trim() ?? '';
    // Une phrase, pas un mot-cle : on refuse une aide vide ou telegraphique.
    expect(texte.length, `aide trop courte sur la tuile ${i}`).toBeGreaterThan(25);
    expect(texte.endsWith('.'), `l aide de la tuile ${i} n est pas une phrase`).toBe(true);
  }
});

test('la bulle est cachee au repos et sort au survol', async ({ page }) => {
  const tuile = page.locator('.acc-tuile').first();
  const bulle = tuile.locator('.acc-aide');
  await expect(bulle).toBeHidden();
  await tuile.locator('.acc-mode').hover();
  await expect(bulle).toBeVisible();
});

// ⚠ LE CAS QUI A MORDU. Le `clip-path` du coin coupe decoupait la bulle placee
// dans le bouton : elle etait « visible » pour tout le monde sauf pour l'oeil.
// On mesure donc qu'elle DEBORDE de la tuile, ce qu'un element decoupe ne peut
// pas faire.
test('elle deborde vraiment sous la tuile, hors du coin coupe', async ({ page }) => {
  const tuile = page.locator('.acc-tuile').first();
  await tuile.locator('.acc-mode').hover();
  const bouton = await tuile.locator('.acc-mode').boundingBox();
  const bulle = await tuile.locator('.acc-aide').boundingBox();
  expect(bouton && bulle).toBeTruthy();
  expect(bulle!.y).toBeGreaterThan(bouton!.y + bouton!.height - 1);
  expect(bulle!.height).toBeGreaterThan(20);
});

// Une aide qui n'existe qu'a la souris n'existe pas pour qui navigue au Tab.
test('elle sort aussi au clavier', async ({ page }) => {
  const tuile = page.locator('.acc-tuile').first().locator('.acc-mode');
  const bulle = page.locator('.acc-tuile').first().locator('.acc-aide');
  await tuile.focus();
  await page.keyboard.press('Shift+Tab');
  await page.keyboard.press('Tab');
  await expect(bulle).toBeVisible();
});

// ⚠ LE CAS QUI COMPTE. La bulle deborde SOUS la tuile : sans
// `pointer-events:none`, elle recouvrirait la tuile d'en dessous, qui ne
// repondrait plus au clic. Une aide qui casse le bouton qu'elle explique
// serait pire que pas d'aide.
test('elle ne vole pas le clic de la tuile du dessous', async ({ page }) => {
  const bulle = page.locator('.acc-aide').first();
  expect(await bulle.evaluate((n) => getComputedStyle(n).pointerEvents)).toBe('none');
});

// ⚠ L'ANGLAIS N'EST PAS FACULTATIF. L'assistant est bilingue : une phrase
// oubliee dans dico-en.js s'afficherait en francais au milieu d'un ecran
// traduit, sans que rien ne le signale. Meme exigence que le journal des
// nouveautes.
test('les phrases existent aussi en anglais', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('marvel-langue', 'en'));
  await page.goto('/prepare.html');
  // `attached`, pas `visible` : au repos la bulle est bien la, mais cachee.
  await page.waitForSelector('.acc-aide', { state: 'attached', timeout: 20000 });
  const phrases = await page.$$eval('.acc-aide', (n) => n.map((x) => x.textContent!.trim()));
  console.log('AIDES EN :', JSON.stringify(phrases, null, 1));
  expect(phrases.length).toBeGreaterThanOrEqual(5);
  for (const phrase of phrases) {
    // Les accents et les mots francais les plus surs : s'ils survivent, la
    // traduction manque.
    expect(phrase, `phrase restee en francais : ${phrase}`)
      .not.toMatch(/héros|écran|mêmes|scénarios|méchant|compétitif/i);
  }
});

// Le lecteur d'ecran annonce la phrase APRES le nom du mode, comme une
// precision : `aria-describedby`, pas `aria-label` qui l'aurait ecrase.
test('elle est rattachee a son bouton pour les lecteurs d ecran', async ({ page }) => {
  const tuile = page.locator('.acc-mode').first();
  const id = await tuile.getAttribute('aria-describedby');
  expect(id).toBeTruthy();
  await expect(page.locator(`#${id}`)).toHaveCount(1);
});

// Le narval, mascotte du site, seul logo de l'en-tete des etapes depuis
// l'en-tete fin du 09/10/2026. Le meme fichier sert d'icone d'onglet et
// d'icone de l'appli : s'il manque, les trois manquent.
test('l en-tete porte le narval, seul logo', async ({ page }) => {
  await page.getByRole('button', { name: /^Solo/ }).first().click();
  const narval = page.locator('header .brand-narwhal');
  await expect(narval).toBeVisible();
  const ok = await narval.evaluate((img: HTMLImageElement) => img.complete && img.naturalWidth > 0);
  expect(ok).toBe(true);
  await expect(page.locator('header .brand-logo')).toHaveCount(0);
  await page.locator('header .brand').screenshot({ path: 'C:/tmp/narwhal-header.png' });
});

