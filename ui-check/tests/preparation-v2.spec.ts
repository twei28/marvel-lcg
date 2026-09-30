import { test, expect } from '@playwright/test';

const LARGEURS = [360, 390, 480];

test.describe('La préparation mobile V2 privée', () => {
  test.use({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });

  test('la V1 reste le rendu par défaut', async ({ page }) => {
    await page.goto('/prepare.html');
    await expect(page.locator('.acc-mode').first()).toBeVisible({ timeout: 30_000 });
    await expect(page.locator('html')).not.toHaveAttribute('data-ui-version', 'v2');
    const hauteur = await page.locator('.acc-mode').first().evaluate(
      (element) => Math.round(element.getBoundingClientRect().height)
    );
    expect(hauteur, 'la V1 ne doit pas recevoir la hauteur compacte V2').not.toBe(76);
  });

  test('le cookie active la V2 avant le rendu', async ({ page, context }) => {
    await page.goto('/prepare.html');
    await context.addCookies([{ name: 'ui_version', value: 'v2', url: page.url() }]);
    await page.reload();
    await expect(page.locator('html')).toHaveAttribute('data-ui-version', 'v2');
    await expect(page.locator('.acc-mode').first()).toBeVisible({ timeout: 30_000 });
  });

  for (const largeur of LARGEURS) {
    test(`${largeur}px : accueil et première étape restent tactiles et sans débordement`, async ({
      page,
      context,
    }) => {
      await page.setViewportSize({ width: largeur, height: 844 });
      await page.goto('/prepare.html');
      await context.addCookies([{ name: 'ui_version', value: 'v2', url: page.url() }]);
      await page.reload();
      await expect(page.locator('.acc-mode').first()).toBeVisible({ timeout: 30_000 });

      const accueil = await page.evaluate(() => ({
        largeurPage: document.documentElement.scrollWidth,
        largeurEcran: window.innerWidth,
        modes: [...document.querySelectorAll<HTMLElement>('.acc-mode')].map((element) => ({
          largeur: element.getBoundingClientRect().width,
          hauteur: element.getBoundingClientRect().height,
        })),
      }));
      expect(accueil.largeurPage).toBeLessThanOrEqual(accueil.largeurEcran);
      expect(accueil.modes.length).toBeGreaterThanOrEqual(4);
      for (const mode of accueil.modes) {
        expect(mode.largeur).toBeGreaterThanOrEqual(44);
        expect(mode.hauteur).toBeGreaterThanOrEqual(44);
      }

      await page.getByRole('button', { name: /^Solo/ }).first().tap();
      await expect(page.locator('#hero-grid .tb-port').first()).toBeVisible({ timeout: 30_000 });

      const etape = await page.evaluate(() => {
        const nav = document.querySelector<HTMLElement>('.nav');
        const contenu = document.querySelector<HTMLElement>('.stage');
        const actions = [...document.querySelectorAll<HTMLElement>(
          '.progress button, .nav button'
        )].filter((element) => element.getBoundingClientRect().width > 0);
        return {
          largeurPage: document.documentElement.scrollWidth,
          largeurEcran: window.innerWidth,
          navHaut: nav?.getBoundingClientRect().top ?? 0,
          contenuBas: contenu?.getBoundingClientRect().bottom ?? 0,
          actions: actions.map((element) => ({
            largeur: element.getBoundingClientRect().width,
            hauteur: element.getBoundingClientRect().height,
          })),
        };
      });
      expect(etape.largeurPage).toBeLessThanOrEqual(etape.largeurEcran);
      expect(etape.contenuBas).toBeGreaterThanOrEqual(etape.navHaut);
      for (const action of etape.actions) {
        expect(action.largeur).toBeGreaterThanOrEqual(44);
        expect(action.hauteur).toBeGreaterThanOrEqual(36);
      }
    });
  }
});
