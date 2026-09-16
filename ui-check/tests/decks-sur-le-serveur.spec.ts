// Les decks importés vivent SUR LE SERVEUR, pas dans le cache du navigateur.
//
// ⚠ POURQUOI CE FICHIER EXISTE (16/09/2026). Signalé en jeu : « je suis sur le
// téléphone et je ne retrouve pas les decks que j'ai importés, alors que je les
// ai sur PC ». Ils étaient rangés dans `localStorage`, donc dans UN navigateur.
// Le vrai danger n'était pas le téléphone : vider le cache les effaçait sans un
// mot.
//
//   npm run decks-serveur
import { test, expect, type Page } from '@playwright/test';

/** Le module, chargé dans la page, avec le réseau sous contrôle. */
async function dansLaPage<T>(page: Page, corps: (mod: any) => Promise<T> | T): Promise<T> {
  return page.evaluate(async (source) => {
    const mod: any = await import('/js/prepare/decks-serveur.js');
    // eslint-disable-next-line no-new-func
    return await new Function('mod', `return (${source})(mod)`)(mod);
  }, corps.toString()) as Promise<T>;
}

const DECK = {
  name: 'Mon deck importé',
  hero: ['01001a'],
  player_deck: ['01002', '01003'],
};

test.beforeEach(async ({ page }) => {
  await page.goto('/prepare.html');
  await page.evaluate(() => window.localStorage.clear());
});

test('un deck importé part sur le serveur', async ({ page }) => {
  const envois: any[] = [];
  await page.route('**/save_deck', async (route) => {
    envois.push(JSON.parse(route.request().postData() || '{}'));
    await route.fulfill({ status: 200, contentType: 'application/json', body: '{"result":"saved"}' });
  });

  const ok = await dansLaPage(page, (mod) => mod.sauverDeck({
    name: 'Mon deck importé', hero: ['01001a'], player_deck: ['01002'],
  }));
  expect(ok).toBe(true);
  expect(envois).toHaveLength(1);
  expect(envois[0].deck.name).toBe('Mon deck importé');
  // Le nom de fichier est nettoyé : le moteur écrit un fichier avec.
  expect(envois[0].file_name).toMatch(/^mcdb-[A-Za-z0-9_-]+$/);
});

// ⚠ LE CAS QUI COMPTE POUR LE JOUEUR. Serveur muet, on ne perd pas son deck :
// il reste sur l'appareil, et l'écran le dit.
test('serveur muet : le deck est gardé en local plutôt que perdu', async ({ page }) => {
  await page.route('**/save_deck', (route) => route.fulfill({ status: 502, body: 'nope' }));
  const ok = await dansLaPage(page, (mod) => mod.sauverDeck({
    name: 'Deck de secours', hero: ['01001a'], player_deck: ['01002'],
  }));
  expect(ok).toBe(false);
  const garde = await page.evaluate(() => {
    const brut = window.localStorage.getItem('mc_prepare_prefs_v1') || '{}';
    return JSON.parse(brut).savedDecks || [];
  });
  expect(garde).toHaveLength(1);
  expect(garde[0].name).toBe('Deck de secours');
});

// ⚠ SEULS LES DECKS DU JOUEUR. `/list_deck` rend AUSSI les decks de base et le
// dossier commun : les prendre pour des decks importés les afficherait en
// double dans la liste, sous le mauvais libellé.
test('seuls les decks du dossier du joueur sont rendus', async ({ page }) => {
  await page.route('**/list_deck*', (route) => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify([
      './deck/starter/spider_man.json',
      './deck/custom/un_deck_partage.json',
      './deck/serveur-3/mcdb-le_mien.json',
    ]),
  }));
  await page.route('**/get_hero_json*', (route) => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({ name: 'Le mien', hero: ['01001a'], player_deck: ['01002'] }),
  }));

  const decks = await dansLaPage(page, (mod) => mod.decksSauvegardesPourHeros('01001a'));
  expect(decks).toHaveLength(1);
  expect(decks[0].name).toBe('Le mien');
});

test('un deck d un autre heros ne remonte pas', async ({ page }) => {
  await page.route('**/list_deck*', (route) => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify(['./deck/serveur-3/mcdb-autre.json']),
  }));
  await page.route('**/get_hero_json*', (route) => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({ name: 'Autre', hero: ['01004a'], player_deck: [] }),
  }));
  const decks = await dansLaPage(page, (mod) => mod.decksSauvegardesPourHeros('01001a'));
  expect(decks).toHaveLength(0);
});

// ⚠ LA MIGRATION, ET C'EST ELLE QUI SAUVE L'EXISTANT. Les decks déjà rangés
// dans le cache doivent monter sur le serveur tout seuls, sans que le joueur
// ait à les réimporter un par un.
test('les decks restés dans le cache montent sur le serveur', async ({ page }) => {
  await page.evaluate((deck) => {
    window.localStorage.setItem('mc_prepare_prefs_v1', JSON.stringify({ savedDecks: [deck] }));
  }, DECK);

  const envois: any[] = [];
  await page.route('**/save_deck', async (route) => {
    envois.push(JSON.parse(route.request().postData() || '{}'));
    await route.fulfill({ status: 200, contentType: 'application/json', body: '{"result":"saved"}' });
  });
  await page.route('**/list_deck*', (route) => route.fulfill({
    status: 200, contentType: 'application/json', body: JSON.stringify([]),
  }));

  await dansLaPage(page, (mod) => mod.decksSauvegardesPourHeros('01001a'));
  expect(envois).toHaveLength(1);
  expect(envois[0].deck.name).toBe('Mon deck importé');

  // Et elle ne se rejoue pas : sinon chaque ouverture du wizard renverrait
  // toute la liste au serveur.
  await dansLaPage(page, (mod) => mod.decksSauvegardesPourHeros('01001a'));
  expect(envois).toHaveLength(1);
});

// Hors ligne, le joueur garde ses decks sous les yeux.
test('serveur injoignable : on retombe sur le cache', async ({ page }) => {
  await page.evaluate((deck) => {
    window.localStorage.setItem('mc_prepare_prefs_v1',
      JSON.stringify({ savedDecks: [deck] }));
    window.localStorage.setItem('mc_decks_migres_v1', '1');
  }, DECK);
  await page.route('**/list_deck*', (route) => route.fulfill({ status: 502, body: 'nope' }));

  const decks = await dansLaPage(page, (mod) => mod.decksSauvegardesPourHeros('01001a'));
  expect(decks).toHaveLength(1);
  expect(decks[0].name).toBe('Mon deck importé');
});
