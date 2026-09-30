import { test, expect, type BrowserContext, type Page } from '@playwright/test';

const PAGES = ['/cards.html', '/deck.html', '/replay.html'];
const LARGEURS = [360, 390, 480];

async function activerV2(page: Page, context: BrowserContext, chemin: string) {
  await page.goto(chemin, { waitUntil: 'domcontentloaded' });
  await context.addCookies([{ name: 'ui_version', value: 'v2', url: page.url() }]);
  await page.reload({ waitUntil: 'domcontentloaded' });
  await expect(page.locator('html')).toHaveAttribute('data-ui-version', 'v2');
}

test.describe('Les écrans historiques dans la V2 mobile', () => {
  test.use({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });

  for (const chemin of PAGES) {
    test(`${chemin} reste strictement V1 sans cookie`, async ({ page }) => {
      await page.goto(chemin, { waitUntil: 'domcontentloaded' });
      await expect(page.locator('html')).not.toHaveAttribute('data-ui-version', 'v2');
      await expect(page.locator('meta[name="viewport"]')).toHaveCount(0);
    });
  }

  for (const largeur of LARGEURS) {
    for (const chemin of PAGES) {
      test(`${chemin} tient à ${largeur}px en V2`, async ({ page, context }) => {
        await page.setViewportSize({ width: largeur, height: 844 });
        await activerV2(page, context, chemin);
        await expect(page.locator('meta[name="viewport"]')).toHaveAttribute(
          'content',
          /width=device-width/
        );

        // Laisser aux modules historiques le temps de monter leurs premières
        // cartes. Le test de structure reste valable même si le catalogue est
        // vide sur une fixture particulière.
        await page.waitForTimeout(1_000);
        const mesure = await page.evaluate(() => {
          const interactifs = [...document.querySelectorAll<HTMLElement>(
            'button, input, select, textarea, label'
          )].filter((element) => {
            const boite = element.getBoundingClientRect();
            const style = getComputedStyle(element);
            return boite.width > 0 && boite.height > 0 && style.visibility !== 'hidden';
          });
          const cartes = [...document.querySelectorAll<HTMLElement>('.image-div')]
            .filter((element) => element.getBoundingClientRect().width > 0);
          return {
            largeurPage: document.documentElement.scrollWidth,
            largeurEcran: window.innerWidth,
            tropPetits: interactifs
              .filter((element) => element.getBoundingClientRect().height < 43)
              .slice(0, 10)
              .map((element) => `${element.tagName}.${element.className}`),
            cartes: cartes.slice(0, 8).map((element) => element.getBoundingClientRect().width),
          };
        });

        expect(mesure.largeurPage, `${chemin} déborde à ${largeur}px`).toBeLessThanOrEqual(
          mesure.largeurEcran + 1
        );
        expect(mesure.tropPetits, `cibles trop petites : ${mesure.tropPetits.join(', ')}`).toEqual([]);
        for (const carte of mesure.cartes) {
          // Les miniatures du replay sont volontairement compactes ; les deux
          // écrans de consultation/édition gardent des cartes lisibles.
          expect(carte).toBeGreaterThanOrEqual(chemin === '/replay.html' ? 70 : 120);
        }
      });
    }
  }
});
