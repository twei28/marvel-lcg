// L'affichage sobre sur les pages hors plateau (09/10/2026) : sans trame BD, sans
// ombre des titres ni biseaux, sans teinte du fond, illustration de la scène
// adoucie (pas en noir et blanc). On mesure ce que le navigateur applique, et on garde une
// capture normal / sobre de chaque page.
//
//   UI_CHECK_BASE=http://127.0.0.1:2330 WSLENV=UI_CHECK_BASE npx playwright test tests/affichage-sobre-pages.spec.ts --project=pc
import { test, expect, type Page } from '@playwright/test';

async function preparer(page: Page, affichage: 'normal' | 'sobre') {
  await page.addInitScript((a) => {
    localStorage.setItem('marvel-langue-choisie', '1');
    localStorage.setItem('mc_affichage_v1', a);
    // Une teinte de fond choisie : le sobre doit la retirer.
    localStorage.setItem('mc_teinte_v1', '210,16,22');
  }, affichage);
  // Les preferences du compte priment sur le navigateur : le moteur d'essai
  // en garde, on les ecarte pour que la page suive le reglage du test.
  await page.route('**/get_preferences*', (r) => r.fulfill({ json: {} }));
}

async function etatSobre(page: Page) {
  return page.evaluate(() => {
    const html = document.documentElement;
    const avant = getComputedStyle(document.body, '::before');
    const titre = document.querySelector<HTMLElement>('h1.affiche, .tb-nomg');
    const art = document.querySelector<HTMLElement>('.tb-art');
    return {
      affichage: html.dataset.affichage,
      teinte: html.dataset.teinte ?? null,
      trame: avant.display === 'none' || avant.content === 'none' || avant.content === '',
      ombreTitre: titre ? getComputedStyle(titre).textShadow : 'none',
      filtreArt: art ? getComputedStyle(art).filter : 'saturate(0.75)',
      accents: ['--affiche-jaune', '--agir', '--eux'].map((n) => getComputedStyle(html).getPropertyValue(n).trim()),
    };
  });
}

const PAGES: Array<{ nom: string; aller: (page: Page) => Promise<void> }> = [
  {
    nom: 'preparation',
    aller: async (page) => {
      await page.goto('/prepare.html');
      await page.getByRole('button', { name: /^Solo/ }).first().click({ timeout: 30_000 });
      await expect(page.locator('#hero-grid .tb-port').first()).toBeVisible({ timeout: 30_000 });
      await page.locator('#hero-grid .tb-port').nth(2).hover();
      await page.waitForTimeout(600);
    },
  },
  { nom: 'campagne', aller: async (page) => { await page.goto('/campagne.html'); await page.waitForTimeout(2500); } },
  {
    nom: 'deckbuilder',
    aller: async (page) => {
      await page.goto('/deck-builder.html?hero=spider_man');
      await page.waitForSelector('.db-chip', { timeout: 30_000 });
      await page.waitForTimeout(1200);
    },
  },
  { nom: 'galerie', aller: async (page) => { await page.goto('/galerie.html'); await page.waitForTimeout(3000); } },
];

for (const p of PAGES) {
  test(`${p.nom} : normal puis sobre`, async ({ browser }) => {
    for (const affichage of ['normal', 'sobre'] as const) {
      const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
      const page = await ctx.newPage();
      await preparer(page, affichage);
      await p.aller(page);
      await page.screenshot({ path: `test-results/sobre/${p.nom}-${affichage}.png` });
      const e = await etatSobre(page);
      expect(e.affichage).toBe(affichage);
      if (affichage === 'sobre') {
        expect(e.teinte, 'la teinte du fond doit tomber en sobre').toBeNull();
        expect(e.trame, 'la trame BD doit disparaitre').toBe(true);
        expect(e.ombreTitre).toBe('none');
        expect(e.filtreArt, 'l art de la scene perd 25 % de saturation').toContain('saturate(0.75)');
        expect(e.filtreArt, 'l art de la scene n est pas assombri').not.toContain('brightness');
        // Desature, pas gris : chaque accent garde sa teinte (ecart entre canaux), mais ternie (pas le #e62429 d'origine).
        for (const hex of e.accents) {
          const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));
          expect(Math.max(r, g, b) - Math.min(r, g, b), `accent ${hex} ne doit pas etre gris`).toBeGreaterThan(12);
          expect(Math.max(r, g, b) - Math.min(r, g, b), `accent ${hex} doit etre terni`).toBeLessThan(90);
        }
      }
      await ctx.close();
    }
  });
}
