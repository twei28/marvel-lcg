// Le plateau mobile tient-il vraiment a l'ecran, et se joue-t-il au doigt ?
//
// Trois affirmations, verifiees sur les 34 etats enregistres :
//   1. la vue d'etat ne deborde JAMAIS (c'est toute la promesse du modele) ;
//   2. aucune bande ne cache de tuile en silence (voir plus bas) ;
//   3. toute cible tactile mesure au moins 44 px dans les deux axes.
//
//   npm run plateau-mobile
//
// La page est ouverte avec ?etat=<fixture> : aucune partie n'a besoin de tourner.
import { test, expect } from '@playwright/test';

const TITRE_PAGE_AVERTISSEMENT = 'Version Mismatch';
const CIBLE_MINIMUM = 44;
const LARGEUR_CARTE_MINIMUM = 96;
/**
 * scrollHeight et clientHeight arrondissent chacun INDEPENDAMMENT un rendu
 * dont la hauteur reelle peut etre fractionnaire (sous-pixel) : verifie sur
 * le gabarit s24, une seule tuile de 64px pile peut ainsi rapporter un
 * scrollHeight de 65 sans qu'aucun contenu ne soit reellement cache (une
 * seule unite existe, elle est bien affichee, rien n'est replie dans le +N).
 * Au-dela de cette tolerance, ce n'est plus de l'arrondi.
 */
const TOLERANCE_ARRONDI = 1;

type Entree = { fichier: string; titre: string };

test('La vue d\'etat tient a l\'ecran et se joue au doigt', async ({ page }) => {
  // PORTE SUR LE RENDU PORTRAIT le 12/09/2026 (spec du 07/09, §7.1) : l'ancien
  // rendu a medaillons (`&medaillons`) est un vestige, sa languette de tiroir
  // fait 18 px et le faisait echouer. Ce que l'on tient ici, sur chaque etat
  // enregistre : le plateau portrait ne defile ni en largeur ni en hauteur,
  // chaque carte posee fait au moins 96 px de large, chaque cible tactile au
  // moins 44 px, et le navigateur ne signale aucune erreur.
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

      const mesure = await page.evaluate(() => ({
        largeurPage: document.documentElement.scrollWidth,
        largeurEcran: window.innerWidth,
      }));
      expect(
        mesure.largeurPage,
        `La page deborde en largeur de ${mesure.largeurPage - mesure.largeurEcran} px`
      ).toBeLessThanOrEqual(mesure.largeurEcran + TOLERANCE_ARRONDI);

      const debordement = await vue.evaluate((element) => ({
        contenu: element.scrollHeight,
        visible: element.clientHeight,
      }));
      expect(
        debordement.contenu,
        `Le plateau portrait deborde de ${debordement.contenu - debordement.visible} px : il ne doit jamais defiler`
      ).toBeLessThanOrEqual(debordement.visible + TOLERANCE_ARRONDI);

      // Les vraies cartes posees (pas les vignettes d'un panneau) : lisibles.
      const cartes = page.locator('.portrait-carte .scan-card, .main-carte .scan-card');
      const nombreCartes = await cartes.count();
      for (let index = 0; index < nombreCartes; index += 1) {
        const boite = await cartes.nth(index).boundingBox();
        if (!boite || boite.width === 0) continue;
        expect(boite.width, `Une carte posee ne fait que ${Math.round(boite.width)} px de large`).toBeGreaterThanOrEqual(
          LARGEUR_CARTE_MINIMUM
        );
      }

      const cibles = page.locator('[data-tactile]');
      const nombre = await cibles.count();
      for (let index = 0; index < nombre; index += 1) {
        const boite = await cibles.nth(index).boundingBox();
        if (!boite) continue;
        expect(
          Math.min(boite.width, boite.height),
          `Cible tactile trop petite (${Math.round(boite.width)}x${Math.round(boite.height)})`
        ).toBeGreaterThanOrEqual(CIBLE_MINIMUM);
      }
    });
  }

  expect(erreurs, `Erreurs signalees par le navigateur :\n${erreurs.join('\n')}`).toHaveLength(0);
});
