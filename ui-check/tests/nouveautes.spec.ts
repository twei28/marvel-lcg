// Le journal des nouveautés (8 septembre 2026, refondu le 17/09).
//
// ⚠ IL ÉTAIT UNE LISTE SOUS LES TUILES, IL EST DEVENU UNE TUILE. À 69 entrées,
// le bloc poussait les modes de jeu hors de l'écran : « tout ne rentre pas sur
// une page à cause des mises à jour ». Le journal complet vit maintenant
// derrière une tuile « Mises à jour », classé par famille.
//
// Il tient sur un fichier de contenu que l'on remplit à la main,
// `public/js/prepare/nouveautes.js`. Deux choses peuvent s'y perdre et ne se
// verraient nulle part ailleurs :
//
//  - une entrée écrite seulement en français. L'assistant est bilingue :
//    l'oubli passe inaperçu tant qu'on ne bascule pas la langue, et un joueur
//    anglophone tombe sur une ligne française au milieu d'un écran traduit.
//  - un genre mal orthographié. L'étiquette perd sa couleur, sans erreur.
//
// Ces deux cas se lisent directement dans le fichier de contenu, sans monter
// de partie : on l'importe dans la page et on le relit.
import { test, expect } from '@playwright/test';

test('l\'accueil porte une tuile « Mises à jour », et plus de liste', async ({ page }) => {
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-nouv-tuile', { timeout: 20000 });

  // ⚠ LE CAS QUI PROTÈGE L'ACCUEIL. C'est l'ancien bloc déroulant qui poussait
  // les modes hors de l'écran : il ne doit pas revenir par mégarde.
  await expect(page.locator('.acc-nouv')).toHaveCount(0);

  // La tuile est dans la grille des modes, au même format que les autres.
  await expect(page.locator('.acc-modes .acc-nouv-tuile')).toHaveCount(1);
});

test('la tuile ouvre le journal, classé par famille', async ({ page }) => {
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-nouv-tuile', { timeout: 20000 });
  await page.locator('.acc-nouv-tuile').click();

  const modale = page.locator('.nouveautes-modal');
  await expect(modale).toBeVisible();

  // Autant de familles que de genres réellement utilisés, ni plus ni moins.
  const attendues = await page.evaluate(async () => {
    const m: any = await import('/public/js/prepare/nouveautes.js');
    const genres = Object.keys(m.GENRES);
    return genres.filter((g) => m.nouveautesTriees().some((n: any) => n.genre === g)).length;
  });
  await expect(modale.locator('.nouv-famille')).toHaveCount(attendues);

  // ⚠ TOUT LE JOURNAL, PAS UN EXTRAIT : c'est la raison d'être de cet écran.
  const total = await page.evaluate(async () => {
    const m: any = await import('/public/js/prepare/nouveautes.js');
    return m.nouveautesTriees().length;
  });
  await expect(modale.locator('.acc-nouv-liste > li')).toHaveCount(total);

  // Dans une section déjà titrée par sa famille, l'étiquette de genre ferait
  // doublon sur chaque ligne.
  await expect(modale.locator('.acc-nouv-genre')).toHaveCount(0);
  await expect(modale.locator('.acc-nouv-liste > li').first().locator('.acc-nouv-date'))
    .not.toBeEmpty();
});

test('dans chaque famille, le plus récent est en tête', async ({ page }) => {
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-nouv-tuile', { timeout: 20000 });
  await page.locator('.acc-nouv-tuile').click();

  const dates = await page.evaluate(async () => {
    const m: any = await import('/public/js/prepare/nouveautes.js');
    const genres = Object.keys(m.GENRES);
    return genres
      .map((g) => m.nouveautesTriees().filter((n: any) => n.genre === g).map((n: any) => n.date))
      .filter((l) => l.length > 0);
  });
  expect(dates.length).toBeGreaterThan(0);
  for (const lot of dates) expect(lot).toEqual([...lot].sort().reverse());
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

test('en anglais, la tuile et le journal parlent anglais', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('marvel-langue', 'en'));
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-nouv-tuile', { timeout: 20000 });

  await expect(page.locator('.acc-nouv-tuile b')).toHaveText('Updates');
  await page.locator('.acc-nouv-tuile').click();

  // Le texte de la première ligne est bien la version anglaise du fichier, et
  // pas la française : c'est la seule façon de prouver que la traduction est
  // lue, un titre traduit ne dirait rien du contenu.
  const attendu = await page.evaluate(async () => {
    const m: any = await import('/public/js/prepare/nouveautes.js');
    const premiere = m.nouveautesTriees()[0];
    return { en: premiere.en, fr: premiere.fr, genre: premiere.genre };
  });
  const lignes = page.locator(`.nouv-famille-titre.${attendu.genre} + .acc-nouv-liste .acc-nouv-texte`);
  const affiche = await lignes.first().innerText();
  expect(affiche.trim()).toBe(attendu.en.trim());
  if (attendu.en !== attendu.fr) expect(affiche.trim()).not.toBe(attendu.fr.trim());
});
