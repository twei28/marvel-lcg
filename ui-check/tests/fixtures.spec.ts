// Relecture des etats de jeu enregistres.
//
// Ce test prouve le point le plus important du filet de securite cote plateau :
// on peut AFFICHER un etat de partie complet sans lancer la moindre partie.
// Il ouvre /fixtures.html pour chacun des etats du catalogue, et verifie que
// des cartes s'affichent vraiment et que le navigateur ne signale aucune erreur.
//
//   npm run fixtures
//
// Les etats sont produits par ~/marvel-work/tools/dump_get_world.py depuis de
// vraies parties jouees automatiquement ; le catalogue est
// public/js/fixtures/index.js dans le dossier du jeu.
import { test, expect } from '@playwright/test';

// Un seul gabarit suffit : cette page est un outil de travail, pas un ecran du
// jeu. La jouer sur les 3 gabarits triplerait la duree sans rien prouver de plus.
// (La forme "test.skip(callback)" au niveau du fichier ne recoit pas testInfo :
//  le filtre par projet se fait donc dans un beforeEach.)
test.beforeEach(({}, testInfo) => {
  test.skip(testInfo.project.name !== 'pc', 'Un seul gabarit suffit');
});

// Titre de la page d'avertissement de cache : le serveur peut la renvoyer a la
// place de n'importe quelle page, avec un code 200.
const TITRE_PAGE_AVERTISSEMENT = 'Version Mismatch';

// En dessous, c'est que l'etat ne s'est pas affiche (un plateau Marvel a
// toujours plus de 10 cartes : main, deck, vilain, complot...).
const CARTES_MINIMUM = 10;

type Entree = { fichier: string; titre: string };

test('Chaque etat enregistre s\'affiche hors partie', async ({ page }) => {
  const erreurs: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') erreurs.push(`[console] ${message.text()}`);
  });
  page.on('pageerror', (erreur) => erreurs.push(`[page] ${erreur.message}`));

  await page.goto('/fixtures.html', { waitUntil: 'networkidle' });

  expect(
    await page.title(),
    "Le serveur a renvoye la page d'avertissement de cache : le cookie de version n'a pas ete pose."
  ).not.toBe(TITRE_PAGE_AVERTISSEMENT);

  // Le catalogue est expose par la page elle-meme : le test n'a pas besoin de
  // connaitre l'emplacement du jeu sur le disque.
  const catalogue: Entree[] = await page.evaluate(
    () => (window as unknown as { FIXTURES?: Entree[] }).FIXTURES ?? []
  );

  expect(catalogue.length, 'Le catalogue des etats enregistres est vide').toBeGreaterThanOrEqual(20);
  expect(catalogue.length, 'Plus de 40 etats : le catalogue devient un dossier fourre-tout')
    .toBeLessThanOrEqual(40);

  for (const entree of catalogue) {
    await test.step(entree.titre, async () => {
      await page.goto(`/fixtures.html?etat=${encodeURIComponent(entree.fichier)}`, {
        waitUntil: 'networkidle',
      });

      // La page marque l'etat effectivement charge : preuve qu'on regarde bien
      // celui qui etait demande, et pas le premier de la liste.
      await expect(page.locator('body')).toHaveAttribute('data-etat', entree.fichier);
      await expect(page.locator('#erreur')).toBeHidden();

      const cartes = await page.locator('li.carte').count();
      expect(cartes, `${entree.fichier} : ${cartes} carte(s) affichee(s)`).toBeGreaterThanOrEqual(
        CARTES_MINIMUM
      );

      // Le compteur affiche en haut de page doit correspondre a ce qui est rendu.
      await expect(page.locator('#total-cartes')).toHaveText(new RegExp(`^${cartes} cartes`));
    });
  }

  expect(erreurs, `Le navigateur a signale des erreurs :\n${erreurs.join('\n')}`).toEqual([]);
});
