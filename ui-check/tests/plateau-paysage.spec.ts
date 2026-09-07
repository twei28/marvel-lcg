// Le plateau paysage tient-il a l'ecran, en vraies cartes lisibles, au doigt ?
//
// Sur les 34 etats enregistres, en 1050 x 480 (projet s24-paysage) :
//   1. le plateau ne deborde JAMAIS verticalement ;
//   2. chaque carte posee mesure au moins 84 px de large (le plancher de
//      lisibilite de la spec) ;
//   3. toute cible tactile mesure au moins 44 px dans les deux axes ;
//   4. aucun ecran portrait n'est affiche.
// Et en 480 x 1050 (projet s24), sur trois etats : l'ecran « Tourne ton
// telephone » couvre toute la fenetre.
//
//   npm run plateau-paysage
//
// La page est ouverte avec ?etat=<fixture> : aucune partie n'a besoin de tourner.
import { test, expect } from '@playwright/test';

const TITRE_PAGE_AVERTISSEMENT = 'Version Mismatch';
const CIBLE_MINIMUM = 44;
const CARTE_MINIMUM = 84;
const TOLERANCE_ARRONDI = 1;

type Entree = { fichier: string; titre: string };

async function catalogue(page: import('@playwright/test').Page): Promise<Entree[]> {
  await page.goto('/fixtures.html', { waitUntil: 'networkidle' });
  expect(await page.title()).not.toBe(TITRE_PAGE_AVERTISSEMENT);
  const entrees: Entree[] = await page.evaluate(
    () => (window as unknown as { FIXTURES?: Entree[] }).FIXTURES ?? []
  );
  expect(entrees.length, 'Le catalogue des etats enregistres est vide').toBeGreaterThanOrEqual(20);
  return entrees;
}

test('En paysage, deux rangees de vraies cartes qui tiennent a l\'ecran', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 's24-paysage', 'Gabarit paysage seulement');
  const erreurs: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') erreurs.push(`[console] ${message.text()}`);
  });
  page.on('pageerror', (erreur) => erreurs.push(`[page] ${erreur.message}`));

  for (const entree of await catalogue(page)) {
    await test.step(entree.titre, async () => {
      await page.goto(`/app/board.html?etat=${encodeURIComponent(entree.fichier)}`, {
        waitUntil: 'networkidle',
      });

      const vue = page.locator('.plateau-paysage');
      await expect(vue, 'Le rendu paysage ne s\'est pas monte').toBeVisible();
      await expect(page.locator('.ecran-portrait'), 'Ecran portrait affiche en paysage').toHaveCount(0);

      // 1. Rien ne deborde verticalement.
      const debordement = await vue.evaluate((element) => ({
        contenu: element.scrollHeight,
        visible: element.clientHeight,
      }));
      expect(
        debordement.contenu,
        `Le plateau deborde de ${debordement.contenu - debordement.visible} px`
      ).toBeLessThanOrEqual(debordement.visible + TOLERANCE_ARRONDI);

      // 2. Chaque carte posee se lit : au moins 84 px de large.
      const cartes = page.locator('.carte-posee > .scan-card');
      const nombreCartes = await cartes.count();
      expect(nombreCartes, 'Aucune carte posee dessinee').toBeGreaterThan(0);
      for (let index = 0; index < nombreCartes; index += 1) {
        const boite = await cartes.nth(index).boundingBox();
        if (!boite) continue;
        expect(boite.width, `Carte trop etroite (${Math.round(boite.width)} px)`).toBeGreaterThanOrEqual(CARTE_MINIMUM);
      }

      // 3. Toute cible tactile respecte le plancher de 44 px.
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

test('En portrait, l\'ecran « Tourne ton telephone » couvre tout', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 's24', 'Gabarit portrait seulement');
  const entrees = (await catalogue(page)).slice(0, 3);
  const fenetre = page.viewportSize();
  expect(fenetre).not.toBeNull();

  for (const entree of entrees) {
    await test.step(entree.titre, async () => {
      await page.goto(`/app/board.html?etat=${encodeURIComponent(entree.fichier)}`, {
        waitUntil: 'networkidle',
      });
      const voile = page.locator('.ecran-portrait');
      await expect(voile).toBeVisible();
      const boite = await voile.boundingBox();
      expect(boite?.width).toBe(fenetre!.width);
      expect(boite?.height).toBe(fenetre!.height);
      // Le plateau est toujours la, dessous : rien n'a ete demonte.
      await expect(page.locator('.plateau-paysage')).toHaveCount(1);
    });
  }
});
