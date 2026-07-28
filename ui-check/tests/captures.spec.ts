// Le filet de securite visuel.
//
// Pour chaque ecran declare dans ecrans.ts, et pour chacun des 3 gabarits,
// on prend une photo de la page et on la compare a l'image de reference.
// Si un pixel change, le test devient rouge : c'est exactement le but.
//
//   npm run captures            -> compare aux references (ne modifie rien)
//   npm run captures:comparer   -> compare puis ouvre la page avant/apres
//   npm run captures:valider    -> fige les nouvelles images comme references
import { test, expect } from '@playwright/test';
import { ECRANS } from '../ecrans';

// Titre de la page d'avertissement de cache. Le serveur peut la renvoyer a la
// place de n'importe quel ecran, avec un code 200 : sans ce garde-fou on
// figerait 18 fois la meme image sans s'en apercevoir.
const TITRE_PAGE_AVERTISSEMENT = 'Version Mismatch';

test.beforeEach(async ({ page }) => {
  // Aucun acces a Internet : les images de cartes doivent venir du disque,
  // sinon les captures dependent de la meteo du reseau.
  await page.route('**://*/**', (route) => {
    const hote = new URL(route.request().url()).hostname;
    return hote === '127.0.0.1' || hote === 'localhost' ? route.continue() : route.abort();
  });

  // Neutralise le hasard : l'ancienne page de preparation tire un numero
  // aleatoire a chaque ouverture et l'affiche.
  await page.addInitScript(() => {
    Math.random = () => 0.42;
  });
});

for (const ecran of ECRANS) {
  test(ecran.titre, async ({ page }) => {
    await page.goto(ecran.url, { waitUntil: 'networkidle' });

    // Garde-fou 1 : ce n'est pas la page d'avertissement de cache.
    expect(
      await page.title(),
      `Le serveur a renvoye la page d'avertissement de cache au lieu de "${ecran.titre}". ` +
        `Le cookie de version n'a pas ete pose.`
    ).not.toBe(TITRE_PAGE_AVERTISSEMENT);

    // Garde-fou 2 : l'element caracteristique de l'ecran est bien la.
    await expect(
      page.locator(ecran.marqueur).first(),
      `L'element "${ecran.marqueur}" est introuvable sur ${ecran.url} : ` +
        `ce n'est probablement pas la bonne page.`
    ).toBeVisible();

    await expect(page).toHaveScreenshot(`${ecran.cle}.png`, {
      fullPage: true,
      mask: (ecran.masques ?? []).map((selecteur) => page.locator(selecteur)),
    });
  });
}
