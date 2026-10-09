// L'assistant en 30 / 70 : la scène du héros à gauche (même style), le contenu
// élargi à droite. On mesure ce qui compte : combien de héros se voient sans
// défiler, et que rien ne déborde de la page.
import { test, expect, type Page } from '@playwright/test';

const ECRANS = [
  { nom: '1920', width: 1920, height: 1080, colonnesMin: 8, rangeesMin: 3 },
  { nom: '1536', width: 1536, height: 864, colonnesMin: 7, rangeesMin: 2 },
  { nom: '1366', width: 1366, height: 768, colonnesMin: 6, rangeesMin: 2 },
];

async function etapeEquipe(page: Page) {
  await page.goto('/prepare.html');
  await page.getByRole('button', { name: /^Solo/ }).first().click({ timeout: 30_000 });
  await expect(page.locator('#hero-grid .tb-port').first()).toBeVisible({ timeout: 30_000 });
}

/** Le nom géant ne doit pas dépasser la scène : coupé par son biais, il se
 *  lirait « MÉCHAN ». */
async function titreTientDansLaScene(page: Page) {
  return page.evaluate(() => {
    const scene = document.querySelector<HTMLElement>('#tb-scene')!;
    const nom = scene.querySelector<HTMLElement>('.tb-nomg')!;
    const pente = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--affiche-pente')) || 70;
    return nom.scrollWidth <= nom.clientWidth + 1
      && nom.getBoundingClientRect().right <= scene.getBoundingClientRect().right - pente * 0.5;
  });
}

async function grilleVisible(page: Page) {
  return page.evaluate(() => {
    const grille = document.querySelector<HTMLElement>('#hero-grid')!;
    const g = grille.getBoundingClientRect();
    const tuiles = [...grille.querySelectorAll<HTMLElement>('.tb-port')].map((t) => t.getBoundingClientRect());
    const entieres = tuiles.filter((t) => t.top >= g.top - 1 && t.bottom <= g.bottom + 1);
    const colonnes = new Set(entieres.map((t) => Math.round(t.left))).size;
    const rangees = new Set(entieres.map((t) => Math.round(t.top))).size;
    return {
      colonnes,
      rangees,
      largeurPage: document.documentElement.scrollWidth,
      largeurEcran: window.innerWidth,
      hauteurPage: document.documentElement.scrollHeight,
      hauteurEcran: window.innerHeight,
    };
  });
}

for (const ecran of ECRANS) {
  test(`${ecran.nom} : la grille des héros montre plus de héros, la scène reste`, async ({ page }) => {
    await page.setViewportSize({ width: ecran.width, height: ecran.height });
    await etapeEquipe(page);
    await page.waitForTimeout(500);
    await page.screenshot({ path: `test-results/assistant-3070-equipe-vide-${ecran.nom}.png` });
    expect(await titreTientDansLaScene(page), 'le titre par défaut déborde de la scène').toBe(true);
    await page.locator('#hero-grid .tb-port').first().hover();
    await page.waitForTimeout(700);
    const m = await grilleVisible(page);
    console.log(ecran.nom, JSON.stringify(m));
    expect(m.largeurPage).toBeLessThanOrEqual(m.largeurEcran);
    expect(m.colonnes).toBeGreaterThanOrEqual(ecran.colonnesMin);
    expect(m.rangees).toBeGreaterThanOrEqual(ecran.rangeesMin);
    await expect(page.locator('#tb-scene .tb-nomg')).toBeVisible();
    await page.screenshot({ path: `test-results/assistant-3070-equipe-${ecran.nom}.png` });

    // Étape Decks : on recrute le premier héros, on ferme la fenêtre des arts
    // si elle s'ouvre, puis Continuer.
    await page.locator('#hero-grid .tb-port').first().click();
    const valider = page.getByRole('button', { name: /^(Valider|Confirm)$/ });
    if (await valider.isVisible({ timeout: 2_000 }).catch(() => false)) await valider.click();
    await page.getByRole('button', { name: /^(Continuer|Continue)$/ }).click();
    await page.waitForTimeout(1_200);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    await page.screenshot({ path: `test-results/assistant-3070-decks-${ecran.nom}.png` });

    await page.getByRole('button', { name: /^(Continuer|Continue)$/ }).click();
    await page.waitForTimeout(1_200);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    expect(await titreTientDansLaScene(page), 'le titre du méchant déborde de la scène').toBe(true);
    await page.screenshot({ path: `test-results/assistant-3070-mechant-${ecran.nom}.png` });
  });
}

test('mobile : la scène passe au-dessus, sans débordement', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await etapeEquipe(page);
  const m = await grilleVisible(page);
  expect(m.largeurPage).toBeLessThanOrEqual(m.largeurEcran);
  await page.screenshot({ path: 'test-results/assistant-3070-equipe-mobile.png' });
});
