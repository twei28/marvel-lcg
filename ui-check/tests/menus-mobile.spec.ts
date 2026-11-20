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
  // Depuis le plateau en bandes (12/09/2026), Options, Historique et « … »
  // vivent dans le menu du bandeau : on l'ouvre d'abord.
  const menu = page.locator('.portrait-menu-bouton');
  await expect(menu).toBeVisible({ timeout: 30_000 });
  await menu.tap();
  await expect(page.locator('.portrait-menu .bh-plus').first()).toBeVisible({ timeout: 30_000 });
}

/** La feuille tient dans l'ecran (plus de barre du bas depuis le 12/09/2026). */
async function verifierLaFeuille(page: Page, selecteur: string) {
  const feuille = page.locator(selecteur).first();
  await expect(feuille, `${selecteur} ne s'est pas ouverte`).toBeVisible();
  const boite = await feuille.boundingBox();
  const ecran = page.viewportSize()!;
  expect(boite, 'feuille sans boite').not.toBeNull();
  expect(boite!.x, 'la feuille commence au bord gauche').toBeLessThanOrEqual(1);
  expect(boite!.width, 'la feuille est pleine largeur').toBeGreaterThanOrEqual(ecran.width - 2);
  expect(boite!.y, 'la feuille commence dans l’ecran').toBeGreaterThanOrEqual(0);
  expect(boite!.y + boite!.height, 'la feuille ne deborde pas de l’ecran').toBeLessThanOrEqual(ecran.height + 1);
  expect(boite!.y + boite!.height, 'la feuille touche le bas de l’ecran').toBeGreaterThanOrEqual(ecran.height - 1);
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
  // ⚠ 14/09/2026 : les reglages ne sont plus une feuille mais une FENETRE a
  // onglets, ouverte au centre. Elle remplace l'empilement « popover Reglages
  // -> popover Options » que l'utilisateur trouvait illisible. Ce cas verifie
  // donc qu'elle tient dans l'ecran du telephone et que ses onglets sont la.
  test('Reglages : une fenetre a onglets qui tient dans l ecran', async ({ page }) => {
    await ouvrirLEtat(page);
    await page.locator('.bh-plus').first().tap();
    const fenetre = page.locator('.reglages-fenetre');
    await expect(fenetre).toBeVisible();

    const boite = (await fenetre.boundingBox())!;
    const ecran = page.viewportSize()!;
    expect(Math.round(boite.width), 'la fenetre deborde en largeur').toBeLessThanOrEqual(ecran.width);
    expect(Math.round(boite.height), 'la fenetre deborde en hauteur').toBeLessThanOrEqual(ecran.height);

    // Les quatre onglets, en bandeau horizontal sur telephone.
    const onglets = page.locator('.reglages-onglet');
    await expect(onglets).toHaveCount(4);
    const premier = (await onglets.first().boundingBox())!;
    const deuxieme = (await onglets.nth(1).boundingBox())!;
    expect(deuxieme.y, 'les onglets doivent etre cote a cote, pas empiles').toBeCloseTo(premier.y, 0);

    // ⚠ Un sous-reglage inutilisable reste VISIBLE : c'est le coeur du
    // changement, un reglage qui apparait est un reglage qu'on ne decouvre
    // jamais.
    // Depuis le 04/10/2026 les onglets sont Apparence, Son, Jeu, Avancé.
    await page.getByRole('tab', { name: /Jeu/ }).tap();
    await expect(page.locator('.ligne-option', { hasText: 'Présentation' }).first()).toBeVisible();

    await page.locator('.reglages-fermer').tap();
    await expect(fenetre).toHaveCount(0);
  });

  // L'historique vit dans le VOLET du journal depuis le 03/10/2026
  // (VoletJournal.tsx) : sur telephone il prend tout l'ecran.
  test('Journal : le volet prend l ecran et se referme', async ({ page }) => {
    await ouvrirLEtat(page);
    await page.locator('.portrait-menu-bouton').tap();
    await page.locator('.volet-journal-languette').tap();
    // Le volet glisse depuis la droite : on attend la fin du glissement.
    await expect.poll(async () => (await page.locator('.volet-journal').boundingBox())?.x ?? 999).toBeLessThanOrEqual(1);
    await verifierLaFeuille(page, '.volet-journal');
    const boite = (await page.locator('.volet-journal').boundingBox())!;
    expect(Math.round(boite.width)).toBeLessThanOrEqual(page.viewportSize()!.width);
    await page.locator('.volet-journal .reglages-fermer').tap();
    await expect(page.locator('.volet-journal')).toHaveCount(0);
  });

  // Le Retour Android (retour-android.ts) : la feuille du sommet se referme,
  // la page reste. Sans lui, le Retour quittait le plateau au milieu d'une partie.
  test('Le Retour referme la feuille au lieu de quitter la partie', async ({ page }) => {
    await ouvrirLEtat(page);
    await page.locator('.bh-plus').first().tap();
    await expect(page.locator('.reglages-fond')).toBeVisible();
    await page.goBack();
    await expect(page.locator('.reglages-fond')).toHaveCount(0);
    expect(page.url(), 'le Retour a quitte le plateau').toContain('/app/board.html');
    // Le menu du bandeau est encore la : un second Retour le referme.
    await expect(page.locator('.portrait-menu')).toBeVisible();
    await page.goBack();
    await expect(page.locator('.portrait-menu')).toHaveCount(0);
    await expect(page.locator('.plateau-portrait')).toBeVisible();
    // La main derriere son encoche, puis une carte ouverte au tap : deux
    // Retour, dans l'ordre inverse, et la page reste.
    await page.locator('.encoche-main').tap();
    const carte = page.locator('.main-feuille .scan-card').first();
    await carte.tap();
    await expect(page.locator('.carte-ouverte-voile')).toBeVisible();
    await page.goBack();
    await expect(page.locator('.carte-ouverte-voile')).toHaveCount(0);
    await expect(page.locator('.main-feuille')).toBeVisible();
    await page.goBack();
    await expect(page.locator('.main-feuille')).toHaveCount(0);
    expect(page.url()).toContain('/app/board.html');
  });

  test('Le menu du bandeau : une feuille basse aux lignes de 48 px, Reglages a plat', async ({ page }) => {
    await ouvrirLEtat(page);
    await verifierLaFeuille(page, '.portrait-menu');
    // Sur telephone, le menu « Partie » du PC n'existe pas : ses lignes sont a
    // plat dans la feuille.
    // ⚠ `.bh-musique` n'y est PLUS depuis le 14/09/2026 : c'est un reglage, il
    // vit dans l'onglet « Image et son » de la fenetre.
    // ⚠ MAIS `.bh-langue` Y EST RESTE, et c'est delibere : la modale de
    // premiere connexion PROMET « le bouton FR / EN, en haut de l'ecran ». Une
    // promesse faite au joueur ne peut pas dependre d'un rangement. Ce bouton a
    // ete retire le matin du 14/09 puis remis le jour meme, l'utilisateur ayant
    // constate qu'il n'y etait plus. Voir `bouton-langue.spec.ts`.
    await expect(page.locator('.portrait-menu .bh-reglages')).toHaveCount(0);
    await expect(page.locator('.portrait-menu .bh-musique'),
                 'la musique devrait etre dans les reglages').toHaveCount(0);
    // Historique et log vivent dans le volet du journal depuis le 03/10/2026.
    for (const ligne of ['.bh-plus', '.bh-undo', '.bh-save', '.bh-langue', '.bh-menu']) {
      await expect(page.locator(`.portrait-menu ${ligne}`).first(), `${ligne} manque dans la feuille`).toBeVisible();
    }
    await page.locator('.portrait-menu-bouton').tap();
    await expect(page.locator('.portrait-menu')).toHaveCount(0);
  });
});
