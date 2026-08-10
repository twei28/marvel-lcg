// La police Marvel ne sait pas ecrire les accents.
//
// MarvelRegular-Dj83.ttf ne contient que TRENTE caracteres : A-Z majuscules,
// le point et l'espace. Un « â » n'y existe pas du tout, le navigateur va donc
// le chercher dans la police de repli (Arial Narrow) et le mot s'affiche
// moitie dans une police, moitie dans l'autre. C'est laid et ca saute aux yeux
// sur un titre.
//
// La regle du projet : tout texte affiche en classe `.mvl` passe par un
// retrait des accents. Elle vivait dans prepare/app.js ; l'ecran des campagnes
// utilisait la meme classe sans l'appliquer, et « L'Avenement de Crane Rouge »
// s'affichait avec ses accents. Signale en jeu le 10/8/2026.
//
// Ce cas verifie la REGLE, pas un ecran : il ouvre les deux frontends qui
// utilisent `.mvl` et refuse le moindre caractere accentue. Un troisieme
// frontend qui oublierait la regle serait attrape ici.
//
//   npx playwright test tests/police-marvel.spec.ts --project=pc
import { test, expect, type Page } from '@playwright/test';

/** Tout ce que la police Marvel ne sait pas dessiner, hors ponctuation. */
const ACCENTUE = /[À-ɏ]/;

/** Les textes rendus en police Marvel sur la page courante. */
async function textesMarvel(page: Page): Promise<string[]> {
  return page.$$eval('.mvl', (elements) =>
    elements.map((e) => (e.textContent ?? '').trim()).filter(Boolean)
  );
}

function fautifs(textes: string[]): string[] {
  return textes.filter((t) => ACCENTUE.test(t));
}

test.describe('La police Marvel', () => {
  test("l'ecran des campagnes n'affiche aucun accent en police Marvel", async ({ page }) => {
    await page.goto('/campagne.html', { waitUntil: 'networkidle' });
    // L'ecran de creation est celui qui porte les noms de boites, donc les
    // accents : « L'Avenement de Crane Rouge », « Intentions Sinistres ».
    const nouvelle = page.getByRole('button', { name: /nouvelle campagne|new campaign/i }).first();
    await expect(
      nouvelle,
      "Le bouton de creation est introuvable : l'ecran a change, ce cas ne verifie plus rien."
    ).toBeVisible();
    await nouvelle.click();

    const textes = await textesMarvel(page);
    expect(
      textes.length,
      "Aucun element .mvl trouve : le cas passerait au vert sans rien verifier."
    ).toBeGreaterThan(1);
    expect(
      fautifs(textes),
      'Ces textes sont affiches en police Marvel, qui ne contient aucun accent : ' +
        'ils seront rendus moitie dans une police, moitie dans une autre.'
    ).toEqual([]);
  });

  test("l'assistant de preparation n'affiche aucun accent en police Marvel", async ({ page }) => {
    await page.goto('/prepare.html?ui=new', { waitUntil: 'networkidle' });
    const textes = await textesMarvel(page);
    expect(
      textes.length,
      "Aucun element .mvl trouve : le cas passerait au vert sans rien verifier."
    ).toBeGreaterThan(1);
    expect(fautifs(textes), 'Textes accentues en police Marvel').toEqual([]);
  });
});
