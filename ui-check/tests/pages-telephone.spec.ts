// Les autres pages au téléphone portrait (zone 2 de la refonte du 09/10/2026,
// fiche .planning/todos/2026-10-09-mode-telephone-refonte.md) : accueil,
// statistiques, galerie, campagne, éditeur de deck.
//
// Pour chaque largeur de 320 à 430 px, chaque écran doit tenir :
//   - aucun débordement horizontal de la page ;
//   - aucune zone tactile visible sous 44 px.
// Plus le comportement : en-tête fin à burger, Retour du système = étape
// précédente (ou feuille refermée), feuilles basses, mode sobre.
//
// Lancement (Windows, port d'essai, jamais celui du jeu de l'utilisateur) :
//   export UI_CHECK_BASE=http://127.0.0.1:2337 WSLENV=UI_CHECK_BASE
//   npx playwright test tests/pages-telephone.spec.ts --project=pc
// CAPTURES_TEL=1 (relayé par WSLENV) range aussi des captures 360 et 430 dans
// .planning/captures-telephone/zone2/.
import { test, expect, type Page, type APIRequestContext } from '@playwright/test';

const FORMATS = [
  { w: 320, h: 640 },
  { w: 360, h: 740 },
  { w: 390, h: 844 },
  { w: 430, h: 932 },
];
const CAPTURER = !!process.env.CAPTURES_TEL;
const DOSSIER = '../.planning/captures-telephone/zone2';
const NOM_CAMPAGNE = 'Essai pages telephone';

/** La page déborde-t-elle en largeur ? Rend les éléments fautifs. */
async function debordements(page: Page): Promise<string[]> {
  return page.evaluate(() => {
    const largeur = document.documentElement.clientWidth;
    const fautifs: string[] = [];
    if (document.documentElement.scrollWidth > largeur + 1) fautifs.push('page:' + document.documentElement.scrollWidth);
    for (const e of Array.from(document.querySelectorAll('body *'))) {
      const r = (e as HTMLElement).getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      const cs = getComputedStyle(e as HTMLElement);
      if (cs.display === 'none' || cs.visibility === 'hidden' || cs.position === 'fixed') continue;
      // Un défilement horizontal VOULU clippe ses enfants.
      let p: HTMLElement | null = (e as HTMLElement).parentElement;
      let clippe = false;
      while (p && p !== document.body) {
        const o = getComputedStyle(p).overflowX;
        if (o === 'auto' || o === 'scroll' || o === 'hidden') { clippe = true; break; }
        p = p.parentElement;
      }
      if (clippe) continue;
      if (r.right > largeur + 1 || r.left < -1) {
        fautifs.push((e as HTMLElement).tagName.toLowerCase() + '.' + String((e as HTMLElement).className).slice(0, 40) + ' [' + Math.round(r.left) + ',' + Math.round(r.right) + ']');
      }
    }
    return fautifs.slice(0, 8);
  });
}

/** Les zones tactiles visibles de moins de 44 px. */
async function petitesZones(page: Page): Promise<string[]> {
  return page.evaluate(() => {
    const out: string[] = [];
    const sel = 'button, a[href], input:not([type=hidden]), select, summary, [role=button]';
    for (const e of Array.from(document.querySelectorAll<HTMLElement>(sel))) {
      let cible: HTMLElement = e;
      if (e instanceof HTMLInputElement && (e.type === 'checkbox' || e.type === 'radio')) {
        cible = (e.closest('label') as HTMLElement) || e;
      }
      const cs = getComputedStyle(cible);
      const r = cible.getBoundingClientRect();
      if (cs.display === 'none' || cs.visibility === 'hidden' || r.width === 0 || r.height === 0) continue;
      if (cible.closest('[hidden]')) continue;
      // Un menu replié (burger fermé) n'est pas à l'écran.
      let p: HTMLElement | null = cible;
      let cache = false;
      while (p) { const c = getComputedStyle(p); if (c.display === 'none' || c.visibility === 'hidden') { cache = true; break; } p = p.parentElement; }
      if (cache) continue;
      if (r.width < 43.5 || r.height < 43.5) {
        out.push(cible.tagName.toLowerCase() + '.' + String(cible.className).slice(0, 40) + ' "' + (cible.textContent || '').trim().slice(0, 20) + '" ' + Math.round(r.width) + 'x' + Math.round(r.height));
      }
    }
    return out.slice(0, 10);
  });
}

async function verifier(page: Page, nom: string) {
  expect(await debordements(page), 'débordement horizontal : ' + nom).toEqual([]);
  expect(await petitesZones(page), 'zones tactiles sous 44 px : ' + nom).toEqual([]);
}

async function capturer(page: Page, w: number, nom: string) {
  if (!CAPTURER || (w !== 360 && w !== 430)) return;
  await page.waitForTimeout(300);
  await page.screenshot({ path: `${DOSSIER}/${w}-${nom}.png` });
}

/** Le menu burger s'ouvre, ses lignes font 44 px, et il se referme. */
async function menuBurger(page: Page, nom: string) {
  const burger = page.locator('.tp-burger, .tel-burger').first();
  await expect(burger, 'burger : ' + nom).toBeVisible();
  await burger.tap();
  const menu = page.locator('.tp-menu, .tel-menu').first();
  await expect(menu).toBeVisible();
  await verifier(page, 'menu ' + nom);
  await burger.tap();
  await expect(menu).toBeHidden();
}

async function enFrancais(page: Page, url: string) {
  await page.goto(url);
  await page.evaluate(() => localStorage.setItem('marvel-langue', 'fr'));
  await page.goto(url);
}

const HISTOIRE = [
  ['Spider-Man', 'Rhino', true], ['Captain Marvel', 'Klaw', false], ['Spider-Man', 'Ultron', true],
].map(([hero, scenario, won], i) => ({ time: 1760000000 + i * 3600, heroes: [{ name: hero }], scenario, rounds: 5 + i, won, expert: i === 2 }));

let idCampagne = '';
test.beforeAll(async ({ request }: { request: APIRequestContext }) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{ id: string; nom?: string }>;
  for (const c of liste) if ((c.nom || '').startsWith(NOM_CAMPAGNE)) await request.post('/delete_campagne', { data: { id: c.id } });
  const r = await request.post('/save_campagne', {
    data: { campagne: { code: 'hunting_season', nom: NOM_CAMPAGNE, difficulte: 'standard',
      equipe: [{ heros: 'spider_man', nomHeros: 'Spider-Man', identite: ['01001a,01001b'] }],
      termines: [], carnet: {}, tentatives: {}, partieEnCours: null } },
  });
  idCampagne = (await r.json()).id;
});
test.afterAll(async ({ request }) => { if (idCampagne) await request.post('/delete_campagne', { data: { id: idCampagne } }); });

for (const { w, h } of FORMATS) {
  test.describe(`pages au téléphone, ${w} px`, () => {
    test.use({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true });

    test('accueil : en-tête fin, gros bouton Jouer en feuille basse, vignettes, statistiques en cartes', async ({ page }) => {
      test.setTimeout(90_000);
      await page.route('**/get_games_history*', (r) => r.fulfill({ json: HISTOIRE }));
      await page.route('**/get_statistics_json*', (r) => r.fulfill({ json: { games_won: 2, games_lost: 1 } }));
      await enFrancais(page, '/prepare.html');
      const jouer = page.locator('.acc-tel-jouer');
      await jouer.waitFor({ timeout: 30_000 });
      await expect(page.locator('.tel-entete')).toBeVisible();
      await expect(page.locator('.tel-etapes')).toHaveCount(0);
      await expect(page.locator('.acc-tel-vignette')).toHaveCount(4);
      const haut = await jouer.evaluate((n) => n.getBoundingClientRect().height);
      expect(haut, 'le bouton Jouer est le plus gros de l’écran').toBeGreaterThan(100);
      await capturer(page, w, 'accueil');
      await verifier(page, 'accueil');
      await menuBurger(page, 'accueil');

      // Jouer : les façons de jouer en feuille basse ; Retour la referme.
      await jouer.tap();
      const feuille = page.locator('.acc-tel-feuille');
      await expect(feuille).toBeVisible();
      await page.waitForTimeout(250);
      await capturer(page, w, 'accueil-jouer');
      await verifier(page, 'feuille Jouer');
      await page.goBack();
      await expect(feuille).toHaveCount(0);
      await expect(jouer).toBeVisible();
      // Un mode choisi dans la feuille mène à l'étape Héros ; Retour ramène à l'accueil.
      await jouer.tap();
      await feuille.locator('.acc-tel-mode-nom', { hasText: /^Solo/ }).tap();
      await expect(page.locator('.tel-etapes .pstep.active')).toBeVisible();
      await expect(page.locator('.acc-tel-feuille')).toHaveCount(0);
      await page.goBack();
      await expect(jouer).toBeVisible();

      // Statistiques : une feuille basse, les tableaux en cartes empilées.
      await page.locator('.tel-burger').tap();
      await page.locator('.tel-menu button', { hasText: 'Stats' }).tap();
      const panneau = page.locator('.reprise-panneau');
      await expect(panneau).toBeVisible();
      await expect(panneau.locator('.stats-table tr td[data-label]').first()).toBeVisible();
      await page.waitForTimeout(250);
      const disposition = await panneau.locator('.stats-table tr').nth(1).evaluate((n) => getComputedStyle(n).display);
      expect(disposition, 'une ligne de tableau devient une carte').toBe('block');
      await capturer(page, w, 'stats');
      await verifier(page, 'statistiques');
      await page.goBack();
      await expect(panneau).toHaveCount(0);
      await expect(jouer).toBeVisible();
    });

    test('galerie : recherche, feuille de filtres à pastilles, 3 colonnes, aperçu en feuille', async ({ page }) => {
      test.setTimeout(90_000);
      await enFrancais(page, '/galerie.html');
      await page.locator('.g-carte').first().waitFor({ timeout: 30_000 });
      await expect(page.locator('html')).toHaveClass(/\btel\b/);
      await expect(page.locator('.tp-entete')).toBeVisible();
      await expect(page.locator('.g-entete')).toBeHidden();
      await expect(page.locator('#select-type')).toBeHidden();
      const cols = await page.evaluate(() => getComputedStyle(document.getElementById('grille')!).gridTemplateColumns.split(' ').length);
      expect(cols, 'trois colonnes de cartes').toBe(3);
      await capturer(page, w, 'galerie');
      await verifier(page, 'galerie');
      await menuBurger(page, 'galerie');
      await expect(page.locator('.tp-menu .reprise-boutons')).toHaveCount(1);

      // Les filtres : une feuille à pastilles, comptée sur le bouton.
      await page.locator('#g-btn-filtres').tap();
      const feuille = page.locator('.g-feuille');
      await expect(feuille).toBeVisible();
      await capturer(page, w, 'galerie-filtres');
      await verifier(page, 'feuille de filtres');
      const avant = await page.locator('#compteur').textContent();
      await feuille.locator('.g-pastille', { hasText: /^Allié$/ }).tap();
      await expect(feuille.locator('.g-pastille.actif', { hasText: /^Allié$/ })).toHaveCount(1);
      await expect(page.locator('#select-type')).toHaveValue('Ally');
      expect(await page.locator('#compteur').textContent()).not.toBe(avant);
      // Retour Android : la feuille se ferme, on reste sur la galerie.
      await page.goBack();
      await expect(feuille).toHaveCount(0);
      await expect(page).toHaveURL(/galerie\.html/);
      await expect(page.locator('#g-btn-filtres')).toHaveText(/Filtres \(1\)/);

      // L'aperçu : une feuille basse, fermée par Retour.
      await page.locator('.g-carte').first().tap();
      await expect(page.locator('.g-apercu')).toBeVisible();
      await expect(page.locator('.g-apercu > .tel-poignee')).toBeVisible();
      await page.waitForTimeout(250);
      const bas = await page.locator('.g-apercu').evaluate((n) => Math.round(n.getBoundingClientRect().bottom));
      expect(bas, 'la feuille est collée en bas').toBe(h);
      await page.locator('.g-apercu img').first().evaluate((i) => (i as HTMLImageElement).decode().catch(() => null));
      await capturer(page, w, 'galerie-apercu');
      await verifier(page, 'aperçu');
      await page.goBack();
      await expect(page.locator('.g-voile')).toHaveCount(0);
      await expect(page).toHaveURL(/galerie\.html/);
    });

    test('campagne : en-tête fin, livre page par page qui glisse, Retour = vue précédente', async ({ page }) => {
      test.setTimeout(90_000);
      await enFrancais(page, '/campagne.html');
      const carte = page.locator('.cmp-carte', { hasText: NOM_CAMPAGNE });
      await carte.waitFor({ timeout: 30_000 });
      await expect(page.locator('.tp-entete')).toBeVisible();
      await expect(page.locator('.cmp-entete')).toHaveCount(0);
      await capturer(page, w, 'campagne-liste');
      await verifier(page, 'liste des campagnes');
      await menuBurger(page, 'campagne');

      // Nouvelle campagne : une vue de plus, Retour ramène à la liste.
      await page.getByRole('button', { name: 'Nouvelle campagne' }).tap();
      await expect(page.locator('.cmp-titre', { hasText: 'Nouvelle campagne' })).toBeVisible();
      await capturer(page, w, 'campagne-creation');
      await verifier(page, 'création de campagne');
      await page.goBack();
      await expect(carte).toBeVisible();

      await carte.locator('.cmp-carte-ouvrir').tap();
      await expect(page.locator('.cmp-livre-scene')).toBeVisible();
      await expect(page.locator('.cmp-livre-double .cmp-livre-feuille')).toHaveCount(1);
      await expect(page.locator('.cmp-livre-compteur')).toHaveText('1 / 4');
      await page.locator('.cmp-livre-double img').first().evaluate((i) => (i as HTMLImageElement).decode().catch(() => null));
      await capturer(page, w, 'campagne-livre');
      await verifier(page, 'livre de campagne');

      // Le doigt glisse vers la gauche : la page suit, puis la suivante arrive.
      const scene = page.locator('.cmp-livre-scene');
      const b = (await scene.boundingBox())!;
      const y = b.y + b.height / 2;
      await scene.dispatchEvent('pointerdown', { pointerType: 'touch', clientX: b.x + b.width * 0.8, clientY: y, isPrimary: true });
      await scene.dispatchEvent('pointermove', { pointerType: 'touch', clientX: b.x + b.width * 0.5, clientY: y, isPrimary: true });
      const decale = await page.locator('.cmp-livre-double').evaluate((n) => (n as HTMLElement).style.transform);
      expect(decale, 'la page suit le doigt').toMatch(/translateX\(-\d/);
      await scene.dispatchEvent('pointerup', { pointerType: 'touch', clientX: b.x + b.width * 0.2, clientY: y, isPrimary: true });
      await expect(page.locator('.cmp-livre-compteur')).toHaveText('2 / 4');
      await expect(page.locator('.cmp-livre-double')).toHaveClass(/glisse-avance/);
      await page.locator('.cmp-livre-fleche.gauche').tap();
      await expect(page.locator('.cmp-livre-compteur')).toHaveText('1 / 4');

      // La loupe se referme par Retour, sans quitter la campagne.
      await page.locator('.cmp-livre-double img').first().tap();
      await expect(page.locator('.cmp-loupe')).toBeVisible();
      await page.goBack();
      await expect(page.locator('.cmp-loupe')).toHaveCount(0);
      await expect(page.locator('.cmp-livre-scene')).toBeVisible();

      // Retour Android : la vue précédente (la liste), pas la page précédente.
      await page.goBack();
      await expect(page.locator('.cmp-page-liste')).toBeVisible();
      await expect(page).toHaveURL(/campagne\.html/);
    });

    test('éditeur de deck : grille plein écran, barre du bas Filtres · Deck, panneaux glissants', async ({ page }) => {
      test.setTimeout(120_000);
      await enFrancais(page, '/deck-builder.html?hero=spider_man');
      await page.locator('#db-grille .db-carte').first().waitFor({ timeout: 60_000 });
      await expect(page.locator('.db-basmob')).toBeVisible();
      await expect(page.locator('#db-mob-deck')).toHaveText(/Deck \(\d+\)/);
      const cols = await page.evaluate(() => getComputedStyle(document.getElementById('db-grille')!).gridTemplateColumns.split(' ').length);
      expect(cols, 'trois colonnes de cartes').toBe(3);
      await capturer(page, w, 'deckbuilder');
      await verifier(page, 'éditeur de deck');
      await menuBurger(page, 'éditeur de deck');

      // Filtres : un panneau qui glisse, refermé par Retour Android.
      await page.locator('#db-mob-filtres').tap();
      await expect(page.locator('#db-filtres-col')).toBeVisible();
      await page.waitForTimeout(300);
      await capturer(page, w, 'deckbuilder-filtres');
      await verifier(page, 'panneau des filtres');
      await page.goBack();
      await expect(page.locator('body')).not.toHaveClass(/db-panneau-filtres/);
      await expect(page).toHaveURL(/deck-builder\.html/);

      // Deck : idem, et la croix le referme aussi.
      await page.locator('#db-mob-deck').tap();
      await expect(page.locator('#db-deck-col')).toBeVisible();
      await page.waitForTimeout(300);
      await capturer(page, w, 'deckbuilder-deck');
      await verifier(page, 'panneau du deck');
      await page.locator('#db-deck-col .db-fermer-panneau').tap();
      await expect(page.locator('body')).not.toHaveClass(/db-panneau-deck/);
      await page.waitForTimeout(200);
      await expect(page).toHaveURL(/deck-builder\.html/);
    });
  });
}

test.describe('mode sobre au téléphone, pages hors assistant', () => {
  test.use({ viewport: { width: 360, height: 740 }, hasTouch: true, isMobile: true });

  test('mêmes règles qu’au PC : palette ternie, sans animation de feuille, 44 px', async ({ page }) => {
    test.setTimeout(90_000);
    await page.addInitScript(() => { try { localStorage.setItem('mc_affichage_v1', 'sobre'); } catch (e) { /* stockage indisponible */ } });
    await enFrancais(page, '/prepare.html');
    await expect(page.locator('html')).toHaveAttribute('data-affichage', 'sobre');
    await page.locator('.acc-tel-jouer').waitFor({ timeout: 30_000 });
    await verifier(page, 'accueil sobre');
    const rouge = await page.locator('.acc-tel-jouer').evaluate((n) => getComputedStyle(n).backgroundColor);
    expect(rouge, 'le rouge du bouton Jouer est le rouge terni du sobre').toBe('rgb(92, 63, 63)');
    if (CAPTURER) await page.screenshot({ path: `${DOSSIER}/360-sobre-accueil.png` });

    await enFrancais(page, '/galerie.html');
    await page.locator('.g-carte').first().waitFor({ timeout: 30_000 });
    await page.locator('#g-btn-filtres').tap();
    const feuille = page.locator('.g-feuille');
    await expect(feuille).toBeVisible();
    const duree = await feuille.evaluate((n) => getComputedStyle(n).animationDuration);
    expect(parseFloat(duree), 'pas d’animation en sobre').toBeLessThanOrEqual(0.001);
    await feuille.locator('.g-pastille').first().tap();
    const actif = await feuille.locator('.g-pastille.actif').first().evaluate((n) => getComputedStyle(n).backgroundColor);
    expect(actif, 'la pastille active prend le rouge terni').toBe('rgb(92, 63, 63)');
    await verifier(page, 'galerie sobre');
    if (CAPTURER) await page.screenshot({ path: `${DOSSIER}/360-sobre-galerie-filtres.png` });
  });
});

// ---- Le site (orchestrateur) : connexion, inscription, signalements,
// administration, suivi. Testé à part, sur un site d'essai LOCAL (base
// jetable, compte « arnaud » / « essai-zone2-mdp »), jamais en production :
//   export SITE=http://127.0.0.1:8093 WSLENV=UI_CHECK_BASE:SITE
const SITE = process.env.SITE || '';

async function connecterSite(page: Page) {
  // Jamais /entrer : il allumerait une table.
  await page.context().route('**/entrer*', (r) => r.abort());
  const rep = await page.request.post(SITE + '/connexion', { form: { pseudo: 'arnaud', mdp: 'essai-zone2-mdp' }, maxRedirects: 0 });
  const jeton = /nc_session=([^;]+)/.exec(rep.headers()['set-cookie'] || '')![1];
  await page.context().addCookies([{ name: 'nc_session', value: jeton, url: SITE }]);
}

for (const { w, h } of FORMATS) {
  test.describe(`site au téléphone, ${w} px`, () => {
    test.skip(!SITE, 'SITE non défini : site d’essai local absent');
    test.use({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true });

    test('connexion et inscription : bandeau fin, formulaire, bouton visible clavier ouvert', async ({ page }) => {
      for (const chemin of ['/connexion', '/inscription']) {
        await page.goto(SITE + chemin);
        const bandeau = page.locator('.marque');
        const hb = await bandeau.evaluate((n) => n.getBoundingClientRect().height);
        expect(hb, 'bandeau fin : ' + chemin).toBeLessThanOrEqual(56);
        const haut = await page.locator('form').evaluate((n) => n.getBoundingClientRect().top);
        expect(haut, 'le formulaire commence en haut : ' + chemin).toBeLessThan(140);
        await capturer(page, w, 'site' + chemin.replace('/', '-'));
        await verifier(page, chemin);
        // Clavier ouvert : la fenêtre visible rétrécit (~45 %). Le bouton
        // d'envoi doit rester dedans une fois le dernier champ touché.
        await page.setViewportSize({ width: w, height: Math.round(h * 0.55) });
        await page.locator('input[name="mdp"]').tap();
        await page.waitForTimeout(400);
        const bouton = await page.locator('form button[type="submit"]').evaluate((n) => {
          const r = n.getBoundingClientRect();
          return { haut: r.top, bas: r.bottom, ecran: innerHeight };
        });
        expect(bouton.bas, 'bouton sous le clavier : ' + chemin).toBeLessThanOrEqual(bouton.ecran + 1);
        expect(bouton.haut, 'bouton au-dessus de l’écran : ' + chemin).toBeGreaterThanOrEqual(0);
        await page.setViewportSize({ width: w, height: h });
      }
    });

    test('signalements, administration, suivi : en-tête fin à burger, cartes empilées', async ({ page }) => {
      await connecterSite(page);
      await page.goto(SITE + '/signalements');
      await expect(page.locator('.barre-burger')).toBeVisible();
      await capturer(page, w, 'site-signalements');
      await verifier(page, 'signalements');
      await page.locator('.barre-burger').tap();
      await expect(page.locator('.barre-nav')).toBeVisible();
      await verifier(page, 'menu du site');
      await page.locator('.barre-burger').tap();
      await expect(page.locator('.barre-nav')).toBeHidden();

      await page.goto(SITE + '/admin');
      for (const onglet of ['comptes', 'rapports', 'joueurs', 'parties', 'journal']) {
        await page.locator(`.onglet[data-onglet="${onglet}"]`).tap();
        if (onglet === 'parties') await page.locator('.sous-onglet[data-sous="parties-play"]').tap();
        await page.waitForTimeout(200);
        await capturer(page, w, 'site-admin-' + onglet);
        await verifier(page, 'administration ' + onglet);
      }
      // Les tableaux : une ligne = une carte, chaque valeur avec son libellé.
      const ligne = page.locator('section[data-panneau="journal"] tr:has(td)').first();
      expect(await ligne.evaluate((n) => getComputedStyle(n).display)).toBe('block');
      expect(await ligne.locator('td').first().getAttribute('data-label')).toBeTruthy();

      await page.goto(SITE + '/suivi');
      await capturer(page, w, 'site-suivi');
      await verifier(page, 'suivi');
    });
  });
}
