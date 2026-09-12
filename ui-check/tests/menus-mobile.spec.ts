// Les menus du plateau portrait sont des FEUILLES (spec du 07/09/2026, §5,
// sous-projet 2 ; livre le 12/09/2026).
//
// Ce que ce filet prouve, sur une partie neuve, au gabarit s24 (480x1050,
// tactile) : Options, Historique et le menu « … » s'ouvrent depuis la barre du
// bas en une feuille qui tient dans l'ecran, AU-DESSUS de la barre (c'est le
// bouton qui a ouvert la feuille qui la referme, il doit rester sous le
// doigt), avec des lignes d'au moins 44 px ; et la feuille se referme.
//
// Mesure avant le correctif : Options se posait a 1 050 px du haut (hors
// ecran), Historique en popover PC coupe dans le coin, la question du moteur
// flottait au milieu, tronquee.
//
//   npm run menus-mobile
import { test, expect, type Page, type APIRequestContext } from '@playwright/test';

const CIBLE_MINIMUM = 44;

// ATTENTION : ce filet lance une NOUVELLE partie sur le serveur de jeu (comme
// npm run lancement et npm run glisser) : toute partie en cours est perdue.
// Un etat enregistre (`?etat=`) ne suffit pas : la barre du bas n'y porte ni
// Options, ni Historique, ni « … » (rien a jouer derriere une vue d'etat).
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

async function ouvrirLEtat(page: Page) {
  await nouvellePartie(page.request);
  await page.goto('/app/board.html');
  await expect(page.locator('.plateau-portrait')).toBeVisible({ timeout: 60_000 });
  await expect(page.locator('body')).toHaveClass(/mode-plateau-portrait/);
  // La mise en place : on garde la main, et la barre du tour apparait.
  const garder = page.locator('.assistant-confirmer').first();
  await garder.waitFor({ state: 'visible', timeout: 60_000 });
  await garder.tap();
  await expect(page.locator('.bh-options').first()).toBeVisible({ timeout: 30_000 });
}

/** La feuille tient dans l'ecran et s'arrete au-dessus de la barre du bas. */
async function verifierLaFeuille(page: Page, selecteur: string) {
  const feuille = page.locator(selecteur).first();
  await expect(feuille, `${selecteur} ne s'est pas ouverte`).toBeVisible();
  const boite = await feuille.boundingBox();
  const barre = await page.locator('.pm-barre').first().boundingBox();
  const ecran = page.viewportSize()!;
  expect(boite, 'feuille sans boite').not.toBeNull();
  expect(boite!.x, 'la feuille commence au bord gauche').toBeLessThanOrEqual(1);
  expect(boite!.width, 'la feuille est pleine largeur').toBeGreaterThanOrEqual(ecran.width - 2);
  expect(boite!.y, 'la feuille commence dans l’ecran').toBeGreaterThanOrEqual(0);
  expect(boite!.y + boite!.height, 'la feuille ne deborde pas de l’ecran').toBeLessThanOrEqual(ecran.height + 1);
  if (barre) {
    expect(boite!.y + boite!.height, 'la feuille s’arrete au-dessus de la barre du bas').toBeLessThanOrEqual(barre.y + 1);
  }
  // Ce qu'on touche : chaque bouton visible de la feuille fait au moins 44 px.
  const boutons = feuille.locator('button');
  const n = await boutons.count();
  let mesures = 0;
  for (let i = 0; i < n; i++) {
    const b = await boutons.nth(i).boundingBox();
    if (!b || b.height === 0) continue;
    mesures += 1;
    expect(b.height, `un bouton de ${selecteur} fait ${b.height} px de haut`).toBeGreaterThanOrEqual(CIBLE_MINIMUM);
  }
  expect(mesures, `${selecteur} n'a aucun bouton mesurable`).toBeGreaterThan(0);
}

test.describe('Les menus du plateau portrait en feuilles', () => {
  test('Options : une feuille au-dessus de la barre, refermee par son bouton', async ({ page }) => {
    await ouvrirLEtat(page);
    const bouton = page.locator('.bh-options').first();
    await bouton.tap();
    await verifierLaFeuille(page, '.popover-options');
    await bouton.tap();
    await expect(page.locator('.popover-options')).toHaveCount(0);
  });

  test('Historique : une feuille haute, refermee par un tap en dehors', async ({ page }) => {
    await ouvrirLEtat(page);
    await page.locator('.bh-history').first().tap();
    await verifierLaFeuille(page, '.historique-panneau');
    await page.touchscreen.tap(240, 20);
    await expect(page.locator('.historique-panneau')).toHaveCount(0);
  });

  test('Le menu « … » : une feuille basse aux lignes de 48 px', async ({ page }) => {
    await ouvrirLEtat(page);
    const bouton = page.locator('.bh-plus').first();
    await bouton.tap();
    await verifierLaFeuille(page, '.popover-plus');
    await bouton.tap();
    await expect(page.locator('.popover-plus')).toHaveCount(0);
  });
});
