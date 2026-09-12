// Le plateau portrait EN BANDES (spec du 12/09/2026), sur chaque etat
// enregistre de /fixtures.html, au gabarit s24 (480x1050, tactile) :
//
// - le rendu se monte, la page ne deborde jamais en largeur ;
// - quatre bandes, et chaque carte posee dans un rail fait au moins 140 px
//   de large (« lisibles : trois par largeur d'ecran ») ;
// - toute cible tactile (`data-tactile`) fait au moins 44 px ;
// - la main est CACHEE derriere son encoche ; un tap sur l'encoche l'ouvre,
//   un tap sur le voile la referme ; l'encoche de gauche ouvre le tiroir ;
// - aucune erreur console.
//
// Le plateau DEFILE verticalement (c'est voulu) : on ne mesure plus
// scrollHeight, on verifie que c'est bien `.portrait-table` qui defile et
// pas la page.
//
//   npm run plateau-mobile
import { test, expect } from '@playwright/test';

const TITRE_PAGE_AVERTISSEMENT = 'Version Mismatch';
const CIBLE_MINIMUM = 44;
const LARGEUR_CARTE_MINIMUM = 140;
const TOLERANCE_ARRONDI = 1;

type Entree = { fichier: string; titre: string };

test('Le plateau en bandes se joue au doigt sur chaque etat enregistre', async ({ page }) => {
  const erreurs: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') erreurs.push(`[console] ${message.text()}`);
  });
  page.on('pageerror', (erreur) => erreurs.push(`[page] ${erreur.message}`));

  await page.goto('/fixtures.html', { waitUntil: 'networkidle' });
  expect(await page.title()).not.toBe(TITRE_PAGE_AVERTISSEMENT);
  const catalogue: Entree[] = await page.evaluate(
    () => (window as unknown as { FIXTURES?: Entree[] }).FIXTURES ?? []
  );
  expect(catalogue.length, 'Le catalogue des etats enregistres est vide').toBeGreaterThanOrEqual(20);

  for (const entree of catalogue) {
    await test.step(entree.titre, async () => {
      await page.goto(`/app/board.html?etat=${encodeURIComponent(entree.fichier)}`, {
        waitUntil: 'networkidle',
      });
      const vue = page.locator('.plateau-portrait');
      await expect(vue, 'Le rendu portrait ne s\'est pas monte').toBeVisible();
      await expect(page.locator('body')).toHaveClass(/mode-plateau-portrait/);
      await expect(page.locator('.bande'), 'quatre bandes, toujours').toHaveCount(4);

      const mesure = await page.evaluate(() => ({
        largeurPage: document.documentElement.scrollWidth,
        largeurEcran: window.innerWidth,
        pageDefile: document.documentElement.scrollHeight > window.innerHeight + 1,
      }));
      expect(
        mesure.largeurPage,
        `La page deborde en largeur de ${mesure.largeurPage - mesure.largeurEcran} px`
      ).toBeLessThanOrEqual(mesure.largeurEcran + TOLERANCE_ARRONDI);
      expect(mesure.pageDefile, 'c est .portrait-table qui defile, jamais la page').toBe(false);

      // Les cartes posees dans les rails : lisibles.
      const cartes = page.locator('.bande-rail > .bande-carte > .plateau-unite > .scan-card');
      const nombreCartes = await cartes.count();
      for (let index = 0; index < nombreCartes; index += 1) {
        const boite = await cartes.nth(index).boundingBox();
        if (!boite || boite.width === 0) continue;
        expect(boite.width, `Une carte posee ne fait que ${Math.round(boite.width)} px de large`).toBeGreaterThanOrEqual(
          LARGEUR_CARTE_MINIMUM
        );
      }

      // Ce qu'on touche : 44 px au moins.
      const cibles = page.locator('[data-tactile]:visible');
      const nombre = await cibles.count();
      for (let index = 0; index < nombre; index += 1) {
        const boite = await cibles.nth(index).boundingBox();
        if (!boite) continue;
        expect(
          Math.min(boite.width, boite.height),
          `Cible tactile trop petite (${Math.round(boite.width)}x${Math.round(boite.height)})`
        ).toBeGreaterThanOrEqual(CIBLE_MINIMUM);
      }

      // La main : cachee, puis ouverte par l'encoche, refermee par le voile.
      await expect(page.locator('.main-feuille'), 'la main doit etre cachee au depart').toHaveCount(0);
      await page.locator('.encoche-main').tap();
      await expect(page.locator('.main-feuille')).toBeVisible();
      const feuille = await page.locator('.main-feuille').boundingBox();
      const ecran = page.viewportSize()!;
      expect(feuille!.y + feuille!.height, 'la main touche le bas de l ecran').toBeGreaterThanOrEqual(ecran.height - 1);
      await page.touchscreen.tap(ecran.width / 2, 80);
      await expect(page.locator('.main-feuille')).toHaveCount(0);

      // Le tiroir des piles.
      await page.locator('.encoche-piles').tap();
      await expect(page.locator('.tiroir')).toBeVisible();
      await page.touchscreen.tap(ecran.width - 20, ecran.height / 2);
      await expect(page.locator('.tiroir')).toHaveCount(0);
    });
  }

  expect(erreurs, `Erreurs signalees par le navigateur :\n${erreurs.join('\n')}`).toHaveLength(0);
});
