// Le preavis de mise a jour, sur l'ecran de preparation.
//
// Pourquoi ce test existe : un deploiement fait `systemctl restart narwhal`,
// l'orchestrateur emporte tous ses moteurs, et TOUTE PARTIE EN COURS EST
// PERDUE. Le bandeau est le seul avertissement que recoit un joueur. Le
// plateau a ses propres cas (ui-app/src/board/annonce.test.tsx) ; celui-ci
// couvre l'autre moitie du besoin : ne pas laisser quelqu'un LANCER une partie
// qui va mourir dans trois minutes.
//
// On force la reponse du moteur avec page.route : le serveur de developpement
// n'a pas de site derriere lui, et repond donc toujours « rien a dire ». C'est
// justement le dernier cas du fichier.
//
//   npm run annonce
import { test, expect } from '@playwright/test';

const ROUTE = '**/get_annonce*';

test('le preavis du site s affiche en haut de l assistant', async ({ page }) => {
  await page.route(ROUTE, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json',
                body: JSON.stringify({ texte: 'Mise a jour du jeu en approche.', secondes: 420 }) }));
  await page.goto('/prepare.html');

  const bandeau = page.locator('.annonce-site');
  await expect(bandeau).toBeVisible({ timeout: 15000 });
  await expect(bandeau).toContainText('Mise a jour du jeu en approche.');
  // Le delai, pas une heure : le navigateur du joueur n'est pas a l'heure du
  // serveur, et un instant absolu lui afficherait un decompte faux.
  await expect(bandeau.locator('.annonce-site-delai')).toHaveText('7 minutes');
  // Il s'adresse a quelqu'un qui regarde ailleurs.
  await expect(bandeau).toHaveAttribute('role', 'alert');
});

test('une annonce deja perimee ne s affiche pas', async ({ page }) => {
  await page.route(ROUTE, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json',
                body: JSON.stringify({ texte: 'Trop tard', secondes: 0 }) }));
  await page.goto('/prepare.html');
  await page.waitForTimeout(2000);
  await expect(page.locator('.annonce-site')).toHaveCount(0);
});

// TEMOIN, et il compte autant que les autres : en partie locale il n'y a aucun
// site derriere le moteur. Le bandeau ne doit alors JAMAIS apparaitre, et la
// preparation ne doit pas s'en trouver genee.
test('sans site derriere le moteur, rien ne s affiche', async ({ page }) => {
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(e.message));
  await page.goto('/prepare.html');
  await page.waitForTimeout(2000);
  const reponse = await page.request.get('/get_annonce');
  expect(await reponse.json()).toEqual({});
  await expect(page.locator('.annonce-site')).toHaveCount(0);
  expect(erreurs).toEqual([]);
});
