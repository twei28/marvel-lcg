// L'ecran de Legacy : la sixieme tuile, la question de l'activation, la grille
// grisee avec ses conditions, le retour au jeu libre.
//
// Tout ce qui precede (regles, paliers, fiche, verrou) est prouve module par
// module. Ce fichier prouve que l'assistant les BRANCHE : un module juste et
// un ecran qui ne l'appelle pas donnent un mode qui n'existe pas.
//
// Ces cas activent le mode sur le serveur de developpement, et remettent la
// fiche a zero en partant.
//
//   npm run legacy-ecran
import { test, expect, type Page } from '@playwright/test';

async function vider(page: Page) {
  await page.evaluate(async () => {
    const mod: any = await import('/js/prepare/legacy-fiche.js');
    await mod.ecrire(mod.ficheVide());
  });
}

/** Depuis l'accueil, entre dans Legacy en reprenant ses parties passees. */
async function entrer(page: Page) {
  await page.getByRole('button', { name: /^Legacy/ }).first().click();
  await page.getByRole('button', { name: /Reprendre mes parties/ }).click();
  await page.waitForSelector('.legacy-bande', { timeout: 20000 });
  await page.waitForSelector('#hero-grid .tb-port', { timeout: 20000 });
}

test.beforeEach(async ({ page }) => {
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-mode', { timeout: 20000 });
  await vider(page);
});

test.afterAll(async ({ browser }) => {
  const page = await browser.newPage();
  await page.goto('/prepare.html');
  await vider(page);
  await page.close();
});

test('la sixieme tuile est la, avec son sous-titre et sa phrase', async ({ page }) => {
  const tuile = page.locator('.acc-tuile').filter({ hasText: 'Legacy' });
  await expect(tuile).toHaveCount(1);
  await expect(tuile).toContainText('Boîte par boîte');
  await expect(tuile.locator('.acc-aide')).toContainText('boîte de base');
  // Comme la Coop, elle propose de 1 a 4 heros : une victoire a plusieurs
  // coche tous les heros de la table.
  await expect(tuile.locator('.acc-nombre')).toHaveCount(4);
  await page.screenshot({ path: 'C:/tmp/legacy-1-accueil.png', clip: { x: 400, y: 440, width: 1120, height: 320 } });
});

// ⚠ CE CHOIX NE SE REFAIT PAS, et la question doit le dire.
test('la premiere entree pose la question, une fois', async ({ page }) => {
  await page.getByRole('button', { name: /^Legacy/ }).first().click();
  const modale = page.locator('.deck-modal');
  await expect(modale).toContainText('parties déjà jouées');
  await expect(modale).toContainText('ne se refait pas');
  await page.screenshot({ path: 'C:/tmp/legacy-2-question.png' });
  await page.getByRole('button', { name: /Reprendre mes parties/ }).click();
  await page.waitForSelector('.legacy-bande', { timeout: 20000 });
  // Retour a l'accueil, re-entree : plus de question.
  await page.locator('.tb-mode').click();
  await page.waitForSelector('.acc-mode');
  await page.getByRole('button', { name: /^Legacy/ }).first().click();
  await page.waitForSelector('.legacy-bande', { timeout: 20000 });
  await expect(page.locator('.deck-modal')).toHaveCount(0);
});

test('le Set de base est libre, la suite est grisee avec sa condition', async ({ page }) => {
  await entrer(page);
  const grille = page.locator('#hero-grid');
  const spidey = grille.locator('.tb-port[title="Spider-Man"], .tb-port').filter({ hasText: /^Spider-Man/ }).first();
  await expect(spidey).not.toHaveClass(/est-verrou/);
  const fermes = grille.locator('.tb-port.est-verrou');
  expect(await fermes.count()).toBeGreaterThan(20);
  // La condition est ECRITE sur la vignette : on sait quoi faire.
  const premiere = fermes.first();
  await expect(premiere.locator('.tb-verrou')).not.toBeEmpty();
  await expect(premiere.locator('.tb-verrou')).toContainText(/D'abord|Vague/);
  // Le bandeau dit ou l'on en est.
  await expect(page.locator('.legacy-bande')).toContainText('Legacy');
  await expect(page.locator('.legacy-bande')).toContainText(/jeton/);
  await page.screenshot({ path: 'C:/tmp/legacy-3-heros.png' });
});

// ⚠ UN CLIC SUR UN HEROS FERME NE LE RECRUTE PAS. Sinon le verrou n'est qu'un
// decor.
test('cliquer un heros grise ne le recrute pas', async ({ page }) => {
  await entrer(page);
  const ferme = page.locator('#hero-grid .tb-port.est-verrou').first();
  await ferme.click({ force: true });
  await expect(ferme).not.toHaveClass(/chosen/);
  await expect(page.locator('#hero-grid .tb-port.chosen')).toHaveCount(0);
});

test('les fan-made sont grises avec leur prix, pas caches', async ({ page }) => {
  await entrer(page);
  await page.getByRole('button', { name: 'Fan-made' }).click();
  await page.waitForSelector('#hero-grid .tb-port', { timeout: 20000 });
  const premier = page.locator('#hero-grid .tb-port').first();
  await expect(premier).toHaveClass(/est-verrou/);
  await expect(premier.locator('.tb-verrou')).toContainText('jeton');
});

test('le hasard ne pioche que dans ce qui est ouvert', async ({ page }) => {
  await entrer(page);
  const choisi = await page.evaluate(async () => {
    // Le bouton « Aleatoire » vit dans la barre du bas.
    const b = [...document.querySelectorAll('button')].find((x) => /al[ée]atoire|random/i.test(x.textContent || ''));
    if (b) (b as HTMLButtonElement).click();
    await new Promise((r) => setTimeout(r, 800));
    const c = document.querySelector('#hero-grid .tb-port.chosen') as HTMLElement | null;
    return c ? { verrou: c.classList.contains('est-verrou'), nom: c.getAttribute('title') } : null;
  });
  expect(choisi).not.toBeNull();
  expect(choisi!.verrou).toBe(false);
});

test('les scenarios de la boite du Bouffon Vert sont grises, Rhino est libre', async ({ page }) => {
  await entrer(page);
  // On prend Spider-Man et on avance jusqu'au mechant.
  await page.locator('#hero-grid .tb-port').filter({ hasText: /^Spider-Man/ }).first().click();
  // ⚠ Spider-Man a des variantes : sa modale d'options s'ouvre d'elle-meme au
  // recrutement et intercepte tout clic tant qu'elle est la. C'est aussi ce
  // qui fait echouer lancement-partie.spec.ts depuis cette modale.
  const options = page.locator('.deck-modal');
  if (await options.count()) await options.getByRole('button', { name: /valider/i }).click();
  await expect(options).toHaveCount(0);
  await page.getByRole('button', { name: /continuer/i }).click();
  await page.getByRole('button', { name: /continuer/i }).click();
  await page.waitForSelector('#scn-grid .tb-port', { timeout: 20000 });
  const rhino = page.locator('#scn-grid .tb-port').filter({ hasText: /^Rhino/ }).first();
  await expect(rhino).not.toHaveClass(/est-verrou/);
  // L'onglet de la boite du Bouffon Vert (n°2).
  await page.locator('.ext-tab').filter({ hasText: /Green Goblin/ }).first().click();
  await page.waitForSelector('#scn-grid .tb-port', { timeout: 20000 });
  const risky = page.locator('#scn-grid .tb-port').filter({ hasText: /Risky Business/ }).first();
  await expect(risky).toHaveClass(/est-verrou/);
  await expect(risky.locator('.tb-verrou')).toContainText(/Vague 1/);
  await page.screenshot({ path: 'C:/tmp/legacy-4-scenarios.png' });
});

// Le deck-building aussi construit avec ce qu'on a (idee de l'utilisateur,
// 13/09/2026). A l'etape des decks, un deck tout fait qui contient une carte
// d'une boite fermee est CACHE : les paquets d'aspect du tableur piochent dans
// toutes les vagues, aucun ne passe au Set de base. Le deck de base reste.
test('a l etape des decks, seuls les decks jouables avec ce qu on a sont proposes', async ({ page }) => {
  await entrer(page);
  await page.locator('#hero-grid .tb-port').filter({ hasText: /^Spider-Man/ }).first().click();
  const options = page.locator('.deck-modal');
  if (await options.count()) await options.getByRole('button', { name: /valider/i }).click();
  await page.getByRole('button', { name: /continuer/i }).click();
  await page.waitForSelector('#deck-liste .tb-deck', { timeout: 20000 });
  const etiquettes = await page.$$eval('#deck-liste .tb-deck', (n) => n.map((x) => x.textContent || ''));
  console.log('DECKS PROPOSES :', JSON.stringify(etiquettes.map((e) => e.slice(0, 40))));
  expect(etiquettes.some((e) => /Base/.test(e))).toBe(true);
  expect(etiquettes.some((e) => /Paquet|Conseill/.test(e))).toBe(false);
  // Et l'editeur de deck s'ouvre en Legacy : il verrouillera les memes cartes.
  const [popup] = await Promise.all([
    page.waitForEvent('popup'),
    page.getByRole('button', { name: /diteur de deck/ }).click(),
  ]);
  expect(popup.url()).toContain('legacy=1');
  await popup.close();
});

// Le jeu libre n'est jamais verrouille : sortir de Legacy rend tout.
test('choisir un autre mode leve le verrou', async ({ page }) => {
  await entrer(page);
  await page.locator('.tb-mode').click();
  await page.waitForSelector('.acc-mode');
  await page.getByRole('button', { name: /^Solo/ }).first().click();
  await page.waitForSelector('#hero-grid .tb-port', { timeout: 20000 });
  await expect(page.locator('#hero-grid .tb-port.est-verrou')).toHaveCount(0);
  await expect(page.locator('.legacy-bande')).toHaveCount(0);
});
