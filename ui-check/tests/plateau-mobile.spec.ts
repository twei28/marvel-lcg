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

      const vue = page.locator('.plateau-mobile');
      await expect(vue, 'Le rendu mobile ne s\'est pas monte').toBeVisible();

      // 1. Rien ne deborde : la hauteur de contenu ne depasse pas la hauteur visible.
      const debordement = await vue.evaluate((element) => ({
        contenu: element.scrollHeight,
        visible: element.clientHeight,
      }));
      expect(
        debordement.contenu,
        `La vue d'etat deborde de ${debordement.contenu - debordement.visible} px : la condensation n'a pas suffi`
      ).toBeLessThanOrEqual(debordement.visible + TOLERANCE_ARRONDI);

      // 2. Aucune bande ne cache de tuile en silence. .plateau-mobile ET
      // .pm-bandes ont eux-memes overflow:hidden avec min-height:0 : une
      // grille CSS qui manque de place les laisse toujours EXACTEMENT a la
      // taille disponible (jamais plus), donc l'assertion 1 ci-dessus ne
      // peut, par construction, JAMAIS detecter un debordement qui se
      // produit plus bas dans l'arbre. Le vrai bord de decoupe silencieux
      // est .bande-tuiles (une bande a la fois, gap:8px flex-wrap avec
      // overflow:hidden) : si son scrollHeight depasse son clientHeight,
      // des tuiles existent dans le DOM mais sont invisibles, sans etre
      // comptees dans la pastille « +N ». C'est exactement le bug que ce
      // plan existe pour empecher.
      const bandes = page.locator('.bande-tuiles');
      const nombreBandes = await bandes.count();
      for (let index = 0; index < nombreBandes; index += 1) {
        const mesure = await bandes.nth(index).evaluate((element) => ({
          contenu: element.scrollHeight,
          visible: element.clientHeight,
          bande: element.closest('.bande')?.querySelector('.bande-titre')?.textContent ?? '?',
        }));
        expect(
          mesure.contenu,
          `Bande "${mesure.bande}" : ${mesure.contenu - mesure.visible} px de tuiles caches sans pastille +N`
        ).toBeLessThanOrEqual(mesure.visible + TOLERANCE_ARRONDI);
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
