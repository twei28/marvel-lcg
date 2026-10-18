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
  // ⚠ LA MODALE D'EXPLICATION PASSE AVANT TOUT (16/09/2026). Elle s'ouvre a
  // chaque entree tant qu'on n'a pas coche « ne plus afficher », et elle ne se
  // ferme que par OK : sans ce clic, le reste du parcours est hors d'atteinte.
  const ok = page.locator('.legacy-explique').getByRole('button', { name: /^OK$/ });
  if (await ok.count()) await ok.click();
  // ⚠ LES DEUX LANGUES : en anglais le bouton s'appelle « Count my past games ».
  // Un libelle francais en dur faisait echouer le cas de traduction, qui teste
  // justement l'ecran en anglais.
  await page.getByRole('button', { name: /Reprendre mes parties|Count my past games/ }).click();
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
  // ⚠ La modale d'explication (16/09/2026) passe avant : on la coche une fois
  // pour de bon, sinon elle reviendrait a la seconde entree et le dernier cas
  // du test la prendrait pour la question d'activation.
  await page.getByRole('button', { name: /^Legacy/ }).first().click();
  await page.locator('.legacy-explique input[type="checkbox"]').check();
  await page.locator('.legacy-explique').getByRole('button', { name: /^OK$/ }).click();
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
  await page.locator('.ext-tab').filter({ hasText: /Green Goblin|Bouffon Vert/ }).first().click();
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
  expect(etiquettes.some((e) => /Base|Deck de départ|Starter/.test(e))).toBe(true);
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

// ⚠ CE QUI BLOQUE ET CE QUI RAPPORTE, SUR DEUX LIGNES (16/09/2026). Depuis
// que seuls les mechants ouvrent la vague suivante, la phrase de condition ne
// doit plus nommer un seul heros : l'y laisser ferait croire a une exigence.
// Les heros gardent leur interet, et la bande est le seul endroit qui le dit.
test('la bande separe la condition des jetons a prendre', async ({ page }) => {
  await entrer(page);
  const suite = page.locator('.legacy-suite');
  await expect(suite).toHaveCount(1);
  const phrase = (await suite.textContent()) || '';
  console.log('CONDITION :', phrase);
  // Au depart, rien n'est gagne : la condition nomme les vilains du Set de base.
  expect(phrase).toMatch(/Rhino|Klaw|Ultron|bats/i);
  expect(phrase, 'la condition ne doit plus exiger de heros').not.toMatch(/gagne avec|win with/i);

  // Et la ligne des jetons annonce les heros qui n'ont pas encore gagne.
  const bonus = page.locator('.legacy-bonus');
  await expect(bonus).toHaveCount(1);
  console.log('JETONS A PRENDRE :', await bonus.textContent());
  await expect(bonus).toContainText(/\d+ héros de cette boîte/);

  // Le mot sur la regle, pour celui qui s'etait fixe l'ancien objectif.
  await expect(page.locator('.legacy-regle')).toContainText(/méchants ouvrent/i);
});

// ⚠ L'ANGLAIS N'EST PAS FACULTATIF : une phrase oubliee dans dico-en.js
// s'afficherait en francais au milieu d'un ecran traduit. Meme exigence que
// l'aide des modes.
test('les deux nouvelles lignes existent aussi en anglais', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('marvel-langue', 'en'));
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-mode', { timeout: 20000 });
  await entrer(page);
  for (const classe of ['.legacy-bonus', '.legacy-regle']) {
    const texte = (await page.locator(classe).textContent()) || '';
    console.log(`${classe} EN :`, texte);
    expect(texte, `phrase restee en francais : ${texte}`)
      .not.toMatch(/héros|méchants|boîte|jeton/i);
  }
});


// ⚠ LA MODALE D'EXPLICATION (16/09/2026). « Une modale quand on commence le
// mode legacy qui explique exactement ce que ca fait, qui s'ouvre a chaque
// fois, sauf qu'il y a un truc qu'on peut cocher en disant ne plus afficher ».
test('elle s ouvre a l entree, et dit les trois regles qui comptent', async ({ page }) => {
  await page.evaluate(() => localStorage.removeItem('marvel-legacy-explique'));
  await page.getByRole('button', { name: /^Legacy/ }).first().click();
  const modale = page.locator('.legacy-explique');
  await expect(modale).toHaveCount(1);
  const texte = (await modale.textContent()) || '';
  console.log('MODALE :', texte.slice(0, 160));
  expect(texte).toMatch(/bats tous les méchants/i);
  expect(texte).toMatch(/jetons/i);
  expect(texte).toMatch(/hors de portée/i);
});

// ⚠ ELLE PASSE AVANT LA QUESTION DE L'ACTIVATION. « Reprendre mes parties
// passees ou repartir de zero » ne se refait pas : le poser avant d'avoir
// explique le mode, c'est le poser a l'aveugle.
test('la question du depart n arrive qu apres le OK', async ({ page }) => {
  await page.evaluate(() => localStorage.removeItem('marvel-legacy-explique'));
  await page.getByRole('button', { name: /^Legacy/ }).first().click();
  await expect(page.getByRole('button', { name: /Reprendre mes parties/ })).toHaveCount(0);
  await page.locator('.legacy-explique').getByRole('button', { name: /^OK$/ }).click();
  await expect(page.getByRole('button', { name: /Reprendre mes parties/ })).toHaveCount(1);
});

test('cochee, elle ne revient plus ; sinon elle revient', async ({ page }) => {
  await page.evaluate(() => localStorage.removeItem('marvel-legacy-explique'));
  // Premier passage : on NE coche pas, elle doit revenir.
  await page.getByRole('button', { name: /^Legacy/ }).first().click();
  await page.locator('.legacy-explique').getByRole('button', { name: /^OK$/ }).click();
  await page.getByRole('button', { name: /Annuler/ }).click();
  await page.getByRole('button', { name: /^Legacy/ }).first().click();
  await expect(page.locator('.legacy-explique'),
    'sans la case cochee, elle doit revenir a chaque entree').toHaveCount(1);
  // Cette fois on coche : elle ne doit plus reparaitre.
  await page.locator('.legacy-explique input[type="checkbox"]').check();
  await page.locator('.legacy-explique').getByRole('button', { name: /^OK$/ }).click();
  await page.getByRole('button', { name: /Annuler/ }).click();
  await page.getByRole('button', { name: /^Legacy/ }).first().click();
  await expect(page.locator('.legacy-explique')).toHaveCount(0);
});

test('et son texte existe aussi en anglais', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('marvel-langue', 'en');
    localStorage.removeItem('marvel-legacy-explique');
  });
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-mode', { timeout: 20000 });
  await page.getByRole('button', { name: /^Legacy/ }).first().click();
  const texte = (await page.locator('.legacy-explique').textContent()) || '';
  console.log('MODALE EN :', texte.slice(0, 160));
  expect(texte, `phrase restee en francais : ${texte}`)
    .not.toMatch(/méchants|héros|boîte|jetons|Ne plus afficher/i);
});
