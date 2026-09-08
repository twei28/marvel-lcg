// Le bloc « Nouveautés » de l'accueil (8 septembre 2026).
//
// Il tient sur un fichier de contenu que l'on remplit à la main,
// `public/js/prepare/nouveautes.js`. Deux choses peuvent se perdre en route et
// ne se verraient nulle part ailleurs :
//
//  - une entrée écrite seulement en français. L'assistant est bilingue :
//    l'oubli passe inaperçu tant qu'on ne bascule pas la langue, et un joueur
//    anglophone tombe sur une ligne française au milieu d'un écran traduit.
//  - un genre mal orthographié. L'étiquette perd sa couleur, sans erreur.
//
// Ces deux cas se lisent directement dans le fichier de contenu, sans monter
// de partie : on l'importe dans la page et on le relit.
import { test, expect } from '@playwright/test';

test('les trois dernières nouveautés s\'affichent sur l\'accueil', async ({ page }) => {
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-nouv', { timeout: 20000 });

  // Les lignes visibles sans rien déplier : exactement trois.
  const enTete = page.locator('.acc-nouv > .acc-nouv-liste > li');
  await expect(enTete).toHaveCount(3);

  // La plus récente en tête. On compare les dates du fichier, pas le texte
  // affiché, qui est mis en forme selon la langue.
  const dates = await page.evaluate(async () => {
    const m = await import('/public/js/prepare/nouveautes.js');
    return m.nouveautesTriees().map((n: any) => n.date);
  });
  expect(dates.length).toBeGreaterThan(0);
  expect(dates).toEqual([...dates].sort().reverse());

  // Chaque ligne porte sa date et son étiquette de genre.
  await expect(enTete.first().locator('.acc-nouv-date')).not.toBeEmpty();
  await expect(enTete.first().locator('.acc-nouv-genre')).not.toBeEmpty();
});

test('« Tout voir » déplie le reste du journal', async ({ page }) => {
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-nouv', { timeout: 20000 });

  const total = await page.evaluate(async () => {
    const m = await import('/public/js/prepare/nouveautes.js');
    return m.nouveautesTriees().length;
  });
  test.skip(total <= 3, 'moins de quatre nouveautés : rien à déplier');

  const repliees = page.locator('.acc-nouv-plus .acc-nouv-liste > li');
  await expect(repliees).toHaveCount(total - 3);
  // Repliées, elles ne sont pas visibles : c'est tout l'intérêt du <details>.
  await expect(repliees.first()).toBeHidden();

  await page.locator('.acc-nouv-plus > summary').click();
  await expect(repliees.first()).toBeVisible();
});

test('chaque nouveauté est écrite dans les deux langues et porte un genre connu', async ({ page }) => {
  await page.goto('/prepare.html');
  const soucis = await page.evaluate(async () => {
    const m = await import('/public/js/prepare/nouveautes.js');
    const genres = Object.keys(m.GENRES);
    return (m.NOUVEAUTES as any[])
      .filter((n) => !n || !n.date || !n.fr || !n.en || !genres.includes(n.genre))
      .map((n) => JSON.stringify(n));
  });
  expect(soucis).toEqual([]);

  // ⚠ LE TÉMOIN QUI COMPTE : `nouveautesTriees` ÉCARTE les entrées bancales.
  // Sans cette égalité, une entrée sans anglais disparaîtrait de l'écran en
  // silence et le premier cas resterait vert.
  const [ecrites, affichables] = await page.evaluate(async () => {
    const m = await import('/public/js/prepare/nouveautes.js');
    return [m.NOUVEAUTES.length, m.nouveautesTriees().length];
  });
  expect(affichables).toBe(ecrites);
});

test('en anglais, le bloc parle anglais', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('marvel-langue', 'en'));
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-nouv', { timeout: 20000 });

  await expect(page.locator('.acc-nouv h2')).toHaveText("What's new");

  // Le texte de la première ligne est bien la version anglaise du fichier, et
  // pas la française : c'est la seule façon de prouver que la traduction est
  // lue, un titre traduit ne dirait rien du contenu.
  const attendu = await page.evaluate(async () => {
    const m = await import('/public/js/prepare/nouveautes.js');
    const premiere = m.nouveautesTriees()[0];
    return { en: premiere.en, fr: premiere.fr };
  });
  const affiche = await page.locator('.acc-nouv .acc-nouv-texte').first().innerText();
  expect(affiche.trim()).toBe(attendu.en.trim());
  if (attendu.en !== attendu.fr) expect(affiche.trim()).not.toBe(attendu.fr.trim());
});
