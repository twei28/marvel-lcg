// Le bouton FR / EN est TOUJOURS atteignable, dans les menus comme en jeu.
//
// ⚠ CE TEST EXISTE POUR UNE PROMESSE. La modale posee a la premiere connexion
// dit au joueur : « tu peux changer a tout moment : le bouton FR / EN, en haut
// de l'ecran ». Une promesse faite au joueur ne peut pas dependre d'un
// rangement.
//
// Elle a pourtant ete rompue DEUX FOIS le 14/09/2026, des deux cotes a la fois :
//  - sur le PLATEAU, en rangeant les reglages dans leur nouvelle fenetre, la
//    langue y avait suivi les autres reglages et le bouton disparaissait ;
//  - dans l'ASSISTANT, l'ecran d'accueil n'a deliberement pas d'en-tete, et
//    c'est justement la que la modale s'affiche : elle promettait un bouton
//    qui n'etait nulle part.
//
//   npm run bouton-langue
import { test, expect, type APIRequestContext, type Page } from '@playwright/test';

async function nouvellePartie(request: APIRequestContext) {
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const deck = await (await request.get('/get_hero_json?spider_man')).json();
  const charge = {
    campaign_json: JSON.stringify(scenario),
    campaign_log: {},
    challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(deck)],
    rules: ['standard'],
    seed: 1234,
    timeout: 0,
  };
  const reponse = await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)));
  expect(reponse.status(), 'le moteur a refuse de creer la partie').toBe(200);
}

async function repondreALaLangue(page: Page) {
  await page.goto('/prepare.html');
  await page.evaluate(() => localStorage.setItem('marvel-langue-choisie', '1'));
}

test('l ecran d accueil porte le bouton, MEME SANS EN-TETE', async ({ page }) => {
  // ⚠ L'accueil n'a pas d'en-tete, et c'est voulu (app.js, `render`). Le bouton
  // vit donc dans la rangee flottante, avec les autres outils. C'est l'ecran ou
  // la question de la langue est posee : y promettre un bouton absent etait le
  // defaut le plus direct.
  await repondreALaLangue(page);
  await page.reload({ waitUntil: 'load' });
  const bouton = page.locator('.btn-langue').first();
  await expect(bouton, 'le bouton FR / EN manque sur l accueil').toBeVisible({ timeout: 30_000 });
  await expect(bouton).toHaveText(/^(FR|EN)$/);
});

test('la barre du plateau le porte aussi, en jeu', async ({ page }) => {
  await repondreALaLangue(page);
  await nouvellePartie(page.request);
  await page.goto('/app/board.html');
  await page.waitForSelector('.bh-bouton', { timeout: 60_000 });
  const bouton = page.locator('.bh-langue');
  await expect(bouton, 'le bouton FR / EN manque dans la barre du plateau').toBeVisible();
  await expect(bouton).toHaveText(/^(FR|EN)$/);
});

test('un clic bascule vraiment la langue', async ({ page }) => {
  // Un bouton present mais inerte tiendrait la promesse a la lettre et la
  // trahirait en fait.
  await repondreALaLangue(page);
  await nouvellePartie(page.request);
  await page.goto('/app/board.html');
  await page.waitForSelector('.bh-langue', { timeout: 60_000 });
  const bouton = page.locator('.bh-langue');
  const avant = (await bouton.textContent())?.trim();
  await bouton.click();
  await expect(bouton).not.toHaveText(avant ?? '', { timeout: 15_000 });
});
