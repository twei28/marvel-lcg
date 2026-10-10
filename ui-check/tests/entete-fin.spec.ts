// En-tete fin, une seule ligne (09/10/2026) : un logo, outils en icones, etapes
// numerotees. Le compte admin est le plus charge : ses quatre boutons en plus
// sont simules ici, comme les poserait lien-admin.js, panneau-documents.js...
import { test, expect, type Page } from '@playwright/test';

// La liste complete vue par l'administrateur (capture du 09/10/2026) : Player,
// Admin, Artwork survey, Hero palettes, Code backup, Report a bug, My reports,
// Documents, en plus de Resume, Replay, Stats, de la langue et de l'affichage.
const BOUTONS_ADMIN = ['🎫 Mes signalements', '⚙️ Administration', '🖼️ Relevé des illustrations', '🎨 Palettes des héros', '💾 Sauvegarde du code'];

async function etapeEquipe(page: Page, admin: boolean) {
  await page.goto('/prepare.html');
  // Au téléphone (zone 2, 09/10/2026), Solo vit dans la feuille du bouton Jouer.
  await page.waitForSelector('.acc-mode, .acc-tel-jouer', { timeout: 20000 });
  if (await page.locator('.acc-tel-jouer').isVisible()) await page.locator('.acc-tel-jouer').click();
  await page.getByRole('button', { name: /^Solo/ }).first().click();
  // Au téléphone, la rangée vit repliée dans le menu du burger : présente, pas visible.
  await page.waitForSelector('header.progress .reprise-boutons', { timeout: 20000, state: 'attached' });
  if (admin) {
    await page.evaluate((libelles) => {
      const rangee = document.querySelector('.reprise-boutons')!;
      const bascule = document.createElement('button');
      bascule.className = 'bouton-vue-joueur';
      bascule.textContent = 'Player';
      rangee.append(bascule);
      const present = (fa: string) => !!rangee.querySelector(`i.${fa}`);
      if (!present('fa-bug')) {
        const b = document.createElement('button');
        b.textContent = '🐞 Signaler un bug';
        rangee.append(b);
      }
      if (!present('fa-book')) {
        const b = document.createElement('button');
        const i = document.createElement('i');
        i.className = 'fa fa-book';
        b.append(i, ' Documents');
        rangee.append(b);
      }
      for (const l of libelles) {
        const b = document.createElement('button');
        b.textContent = l;
        rangee.append(b);
      }
    }, BOUTONS_ADMIN);
  }
  await page.waitForTimeout(300);
}

for (const [largeur, langue] of [[1366, 'fr'], [1366, 'en'], [1920, 'fr']] as const) {
  test(`une seule ligne en admin a ${largeur} px (${langue})`, async ({ page }) => {
    await page.setViewportSize({ width: largeur, height: 800 });
    await page.goto('/prepare.html');
    await page.evaluate((l) => localStorage.setItem('marvel-langue', l), langue);
    await etapeEquipe(page, true);
    const entete = page.locator('header.progress');
    const boite = await entete.boundingBox();
    expect(boite!.height, 'en-tete sur plusieurs lignes').toBeLessThanOrEqual(60);
    await expect(entete.locator('.brand-logo')).toHaveCount(0);
    await expect(entete.locator('.brand-narwhal')).toBeVisible();
    // Chaque outil : une icone, son nom pour les lecteurs d'ecran et au survol.
    const outils = entete.locator('.reprise-boutons > button');
    const n = await outils.count();
    expect(n).toBeGreaterThanOrEqual(11);
    for (let i = 0; i < n; i++) {
      const o = outils.nth(i);
      await expect(o.locator('i.fa')).toHaveCount(1);
      expect((await o.getAttribute('aria-label'))?.length ?? 0).toBeGreaterThan(1);
      expect((await o.getAttribute('title'))?.length ?? 0).toBeGreaterThan(1);
      const b = await o.boundingBox();
      expect(b!.width).toBeLessThanOrEqual(36);
    }
    await expect(entete.locator('.pstep .pnum').first()).toHaveText('1');
    await expect(entete.locator('.psep')).toHaveCount(3);
    await page.screenshot({ path: `test-results/entete-fin-admin-${largeur}-${langue}.png`, clip: { x: 0, y: 0, width: largeur, height: 120 } });
  });
}

// Au telephone (refonte du 09/10/2026) : l'en-tete n'a plus que le logo, la
// langue et le burger ; la rangee d'outils (Reprendre, Stats, Bug, admin...)
// vit DANS le menu du burger, chaque outil a 44 px avec son libelle.
test('mobile : l en-tete reste sur une ligne, les outils sont dans le burger', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await etapeEquipe(page, true);
  const rang = await page.locator('.tel-rang').boundingBox();
  expect(rang!.height, 'la ligne du logo et du burger').toBeLessThanOrEqual(56);
  const deborde = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  expect(deborde, 'la page defile horizontalement').toBe(false);
  // Repliee : aucun outil a l'ecran.
  const outils = page.locator('.tel-menu .reprise-boutons > button');
  await expect(page.locator('.tel-menu')).toBeHidden();
  // Le burger ouvre le menu : les outils y sont, admin compris, a 44 px.
  await page.locator('#tel-burger').click();
  await expect(page.locator('.tel-menu')).toBeVisible();
  await expect(page.locator('#tel-burger')).toHaveAttribute('aria-expanded', 'true');
  const n = await outils.count();
  expect(n).toBeGreaterThanOrEqual(11);
  await expect(outils.filter({ hasText: 'Administration' })).toHaveCount(1);
  for (let i = 0; i < n; i++) {
    const b = await outils.nth(i).boundingBox();
    if (!b) continue;
    expect(b.height, `outil ${i} sous 44 px`).toBeGreaterThanOrEqual(44);
    expect(b.x + b.width, `outil ${i} hors de l ecran`).toBeLessThanOrEqual(391);
  }
  const debordeOuvert = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  expect(debordeOuvert, 'menu ouvert : la page defile horizontalement').toBe(false);
  await page.screenshot({ path: 'test-results/entete-fin-mobile.png' });
  await page.locator('#tel-burger').click();
  await expect(page.locator('.tel-menu')).toBeHidden();
});

test('le joueur voit aussi ses outils en icones, et en anglais', async ({ page }) => {
  await page.setViewportSize({ width: 1366, height: 800 });
  await page.goto('/prepare.html');
  await page.evaluate(() => localStorage.setItem('marvel-langue', 'en'));
  await etapeEquipe(page, false);
  const stats = page.locator('.reprise-boutons > button', { has: page.locator('i.fa-bar-chart') });
  await expect(stats).toHaveAttribute('aria-label', 'Stats');
  await expect(page.locator('.btn-langue')).toHaveText('EN');
  await expect(page.locator('.btn-affichage')).toHaveAttribute('aria-label', /display/i);
});
