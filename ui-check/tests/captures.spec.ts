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

  // Mode demonstration : provoque volontairement une difference visible, pour
  // montrer a quoi ressemble une regression detectee (page de comparaison
  // avant/apres). Sans la variable d'environnement UI_CHECK_DEMO, rien ne change.
  //
  // On passe par addInitScript et non addStyleTag : ce beforeEach s'execute
  // AVANT le goto du test, il n'y a donc pas encore de page ou injecter le style.
  if (process.env.UI_CHECK_DEMO) {
    await page.addInitScript(() => {
      const poserLeStyle = () => {
        const style = document.createElement('style');
        style.setAttribute('data-ui-check-demo', '1');
        // Une simple teinte (hue-rotate) ne bouge PAS assez de pixels sur les
        // ecrans a fond tres sombre : la difference passe sous le seuil de
        // tolerance et la demonstration ne montre rien. L'inversion de
        // luminosite en conservant les teintes (le classique "mode sombre
        // automatique") change tous les ecrans de facon nette et lisible.
        style.textContent =
          'html { filter: invert(1) hue-rotate(180deg) !important; background: #fff !important; }';
        (document.head ?? document.documentElement).appendChild(style);
      };
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', poserLeStyle);
      } else {
        poserLeStyle();
      }
    });
  }
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

    // Garde-fou 3 : quand l'ecran vise un panneau masque du wizard, on l'ouvre
    // et on prouve que son contenu est bien a l'ecran avant de photographier.
    if (ecran.etape !== undefined) {
      // On passe par wizardShow(i) et NON par un clic sur .w-step : dans
      // scene.html, le clic est conditionne par canPass[cur]() et ne fait
      // rien tant que l'etape courante n'est pas valide.
      await page.evaluate((i) => {
        (window as unknown as { wizardShow: (n: number) => void }).wizardShow(i);
      }, ecran.etape);

      await expect(
        page.locator(`.w-step-panel[data-panel="${ecran.etape}"]`),
        `Le panneau ${ecran.etape} ne s'est pas ouvert : wizardShow est-il toujours expose par scene.html ?`
      ).toHaveClass(/(^|\s)on(\s|$)/);

      // Deplier ce que la page replie par defaut, sinon une partie du panneau
      // n'entre jamais dans la photo et echappe a la surveillance.
      for (const depliage of ecran.depliages ?? []) {
        await page
          .locator(depliage)
          .first()
          .click({ timeout: 5000 });
      }

      for (const preuve of ecran.preuves ?? []) {
        await expect(
          page.locator(preuve).first(),
          `"${preuve}" n'est pas visible : la photo ne montrerait pas le contenu du panneau.`
        ).toBeVisible();
      }

      // Le wizard fait un scrollTo en 'smooth' : on laisse le defilement finir.
      await page.waitForTimeout(500);
    }

    await expect(page).toHaveScreenshot(`${ecran.cle}.png`, {
      fullPage: true,
      mask: (ecran.masques ?? []).map((selecteur) => page.locator(selecteur)),
    });
  });
}
