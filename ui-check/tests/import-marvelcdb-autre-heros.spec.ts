// Coller un lien MarvelCDB d'un AUTRE heros : le heros du siege l'emporte.
//
// Avant le 09/09/2026, le champ « coller un lien » lisait le `hero_code` du
// deck et BASCULAIT le slot sur ce heros-la, sans rien demander. Choisir
// She-Hulk puis coller un deck de Spider-Man donnait donc Spider-Man.
//
// Desormais le heros choisi reste, et seules les 25 cartes d'aspect du deck
// colle sont reprises (les 15 signatures partent a la conversion). Ce qui
// reste refuse, c'est une pioche que les regles de construction du heros
// n'admettent pas : le verdict est celui de l'editeur de deck
// (public/js/deckbuilder/regles.js), teste unitairement par
// `node outils/verifier-marvelcdb.mjs`.
//
//   npx playwright test tests/import-marvelcdb-autre-heros.spec.ts --project=pc
//
// Aucune requete ne sort vers marvelcdb.com : la reponse de l'API est
// fabriquee ici, a partir des decks de depart que le jeu sert deja.
import { test, expect, type Page, type APIRequestContext } from '@playwright/test';

const URL_FAUSSE = 'https://marvelcdb.com/decklist/view/99999';

/** Le deck de depart d'un heros, tel que le jeu le sert. */
async function starter(request: APIRequestContext, hero: string) {
  const r = await request.get(`/get_hero_json?${hero}`);
  expect(r.ok(), `/get_hero_json?${hero} a repondu ${r.status()}`).toBeTruthy();
  return await r.json();
}

/** Un deck marvelcdb (`slots`) fabrique a partir d'un deck de depart : ses 15
 *  cartes signature ET ses 25 cartes de pioche, comme le vrai site les melange. */
function slotsDe(deck: any): Record<string, number> {
  const slots: Record<string, number> = {};
  for (const id of [...(deck.hero_deck || []), ...(deck.player_deck || [])]) {
    const cle = String(id).split(',')[0];
    slots[cle] = (slots[cle] || 0) + 1;
  }
  return slots;
}

/** Repond a la place de marvelcdb.com. */
async function fausseApi(page: Page, nom: string, deck: any) {
  await page.route(/marvelcdb\.com\/api\/public\/(decklist|deck)\//, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        name: nom,
        hero_code: String((deck.hero || [])[0] || '').split(',')[0],
        slots: slotsDe(deck),
      }),
    }));
}

/** Accueil -> Solo -> etape Equipe : choisir un heros, puis passer aux Decks.
 *  L'accueil (tuiles de mode) precede l'assistant : sans le clic sur « Solo »,
 *  aucun heros n'est affiche. */
async function choisirHeros(page: Page, nom: RegExp) {
  // Premier lancement : sans choix range, les fenetres de la langue et de l'affichage
  // couvriraient l'ecran.
  await page.addInitScript(() => {
    localStorage.setItem('marvel-langue-choisie', '1');
    localStorage.setItem('mc_affichage_v1', 'normal');
  });
  await page.goto('/prepare.html?ui=new', { waitUntil: 'load' });
  await page.getByRole('button', { name: /^Solo/ }).first().click();
  await page.getByRole('button', { name: nom }).first().click();
  // « Options de ce heros » (art, faces) s'ouvre au choix d'un heros : on valide tel quel.
  const options = page.locator('.deck-modal').getByRole('button', { name: 'Valider' });
  if (await options.isVisible({ timeout: 3000 }).catch(() => false)) await options.click();
  await page.getByRole('button', { name: /continuer/i }).click();
  await expect(page.locator('#mcdb-0')).toBeVisible();
}

/** Colle l'URL, clique Import, et rend le texte des boites de dialogue. */
async function importer(page: Page): Promise<string[]> {
  const dits: string[] = [];
  page.on('dialog', async (d) => { dits.push(d.message()); await d.accept(); });
  await page.locator('#mcdb-0').fill(URL_FAUSSE);
  await page.getByRole('button', { name: /^Import$/ }).click();
  await expect.poll(() => dits.length, { timeout: 15000 }).toBeGreaterThan(0);
  return dits;
}

test("un deck d'un autre heros garde le heros du siege et ne prend que ses cartes d'aspect",
  async ({ page, request }) => {
    const spiderMan = await starter(request, 'spider_man');   // Justice
    const sheHulk = await starter(request, 'she_hulk');       // le heros choisi
    await fausseApi(page, 'Web of Justice', spiderMan);
    await choisirHeros(page, /^She-Hulk/);

    // Le deck se range SUR LE SERVEUR (/save_deck, decks-serveur.js), plus dans le
    // navigateur : on capte l'envoi, sans rien ecrire sur le disque du jeu.
    let envoye: any = null;
    await page.route('**/save_deck', async (route) => {
      envoye = route.request().postDataJSON().deck;
      await route.fulfill({ status: 200, contentType: 'application/json', body: '{}' });
    });
    const dits = await importer(page);
    // Le nom porte le heros d'accueil : deux imports du meme deck sur deux
    // heros ne se confondent plus dans la liste des decks sauvegardes.
    expect(dits[0]).toMatch(/Web of Justice \(She-Hulk\)/);
    expect(dits[0]).toMatch(/25/);

    // La preuve : le deck envoye au serveur porte le heros DE SHE-HULK, et les
    // cartes DE SPIDER-MAN.
    await expect.poll(() => envoye, { timeout: 10_000 }).toBeTruthy();
    const range = envoye;
    expect(range.hero).toEqual(sheHulk.hero);
    expect(range.hero_deck).toEqual(sheHulk.hero_deck);
    expect(range.obligations).toEqual(sheHulk.obligations);
    expect(range.player_deck.slice().sort()).toEqual(spiderMan.player_deck.slice().sort());
    // Aucune carte signature de Spider-Man n'a franchi la frontiere.
    for (const sig of spiderMan.hero_deck) {
      expect(range.player_deck, `signature ${sig} importee a tort`).not.toContain(sig);
    }
  });

test("un deck que les regles du heros refusent est rejete, avec la raison",
  async ({ page, request }) => {
    // Adam Warlock construit sur QUATRE aspects : personne d'autre n'a le droit.
    const warlock = await starter(request, 'adam_warlock');
    await fausseApi(page, 'Warlock Rainbow', warlock);
    await choisirHeros(page, /^She-Hulk/);

    const dits = await importer(page);
    expect(dits[0]).toMatch(/légal|legal/i);
    expect(dits[0]).toMatch(/She-Hulk/);

    // Rien n'a ete range : l'import a ete refuse, pas a moitie applique.
    const range = await page.evaluate(() => {
      const o = JSON.parse(localStorage.getItem('mc_prepare_prefs_v1') || '{}');
      return (o.savedDecks || []).length;
    });
    expect(range).toBe(0);
  });
