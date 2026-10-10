// Le plateau du TELEPHONE, zone 3 de la refonte (10/10/2026,
// .planning/todos/2026-10-09-mode-telephone-refonte.md, « Plateau »).
//
// Sur une partie neuve, en 320, 360, 390 et 430 px de large (tactile) :
// - rien ne deborde en largeur, la page ne defile pas (la table, si) ;
// - tout ce qu'on touche fait au moins 44 px ;
// - les languettes sont fines (24 px visibles) et semi-transparentes au repos ;
// - « Garder ma main » allume le bandeau « Annuler », qui tient dans l'ecran ;
// - toucher une carte jouable fait apparaitre « Jouer » ;
// - la taille du texte « tres grande » ne fait rien deborder ;
// Puis : 768 px et plus = plateau PC, telephone couche (844 px) = plateau PC.
//
// Les captures de la zone 3 (360 et 430 px) partent dans
// .planning/captures-telephone/zone3/.
//
// ATTENTION : ce filet lance une NOUVELLE partie sur le serveur de jeu.
//
//   UI_CHECK_BASE=http://127.0.0.1:<port> npx playwright test plateau-telephone --project=mobile
import { test, expect, type Page, type APIRequestContext } from '@playwright/test';
import { fileURLToPath } from 'node:url';

const CIBLE_MINIMUM = 44;
const TOLERANCE = 1;
const CAPTURES = fileURLToPath(new URL('../../.planning/captures-telephone/zone3/', import.meta.url));

const LARGEURS = [
  { largeur: 320, hauteur: 640 },
  { largeur: 360, hauteur: 780 },
  { largeur: 390, hauteur: 844 },
  { largeur: 430, hauteur: 932 },
];

test.use({ hasTouch: true });
test.setTimeout(180_000);

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

/** Debordement horizontal de la page, et page qui defile (c'est la table qui doit defiler). */
async function verifierLeCadre(page: Page, etape: string) {
  const mesure = await page.evaluate(() => ({
    largeurPage: document.documentElement.scrollWidth,
    largeurEcran: window.innerWidth,
    pageDefile: document.documentElement.scrollHeight > window.innerHeight + 1,
  }));
  expect(mesure.largeurPage, `${etape} : la page deborde en largeur`).toBeLessThanOrEqual(mesure.largeurEcran + TOLERANCE);
  expect(mesure.pageDefile, `${etape} : la page defile, pas la table`).toBe(false);
}

/** Tout ce qu'on touche : 44 px au moins (les deux cotes pour data-tactile, la hauteur pour les boutons). */
async function verifierLesCibles(page: Page, etape: string) {
  const trop = await page.evaluate((min) => {
    const visibles = (el: Element) => {
      const r = el.getBoundingClientRect();
      const s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' &&
        r.bottom > 0 && r.top < window.innerHeight && r.right > 0 && r.left < window.innerWidth;
    };
    const fautes: string[] = [];
    for (const el of Array.from(document.querySelectorAll('[data-tactile]'))) {
      if (!visibles(el)) continue;
      const r = el.getBoundingClientRect();
      if (Math.min(r.width, r.height) < min - 0.5) fautes.push(`${el.getAttribute('data-tactile')} ${Math.round(r.width)}x${Math.round(r.height)}`);
    }
    const boutons = document.querySelectorAll(
      '.portrait-bandeau button, .main-feuille button, .bandeau-annuler button, .portrait-menu button, .tiroir button'
    );
    for (const el of Array.from(boutons)) {
      if (!visibles(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.height < min - 0.5) fautes.push(`${el.className || el.textContent} ${Math.round(r.width)}x${Math.round(r.height)}`);
    }
    return fautes;
  }, CIBLE_MINIMUM);
  expect(trop, `${etape} : zones tactiles sous 44 px`).toEqual([]);
}

async function capture(page: Page, nom: string, largeur: number) {
  if (largeur !== 360 && largeur !== 430) return;
  await page.screenshot({ path: `${CAPTURES}${largeur}-${nom}.png` });
}

for (const { largeur, hauteur } of LARGEURS) {
  test(`plateau au telephone en ${largeur} px`, async ({ page }) => {
    const erreurs: string[] = [];
    page.on('pageerror', (erreur) => erreurs.push(erreur.message));
    await page.setViewportSize({ width: largeur, height: hauteur });
    await page.goto('/prepare.html');
    await page.evaluate(() => {
      localStorage.removeItem('marvel-tel-taille-texte');
      localStorage.setItem('marvel-langue', 'fr');
    });
    await nouvellePartie(page.request);
    await page.goto('/app/board.html');
    await expect(page.locator('.plateau-portrait')).toBeVisible({ timeout: 60_000 });
    await expect(page.locator('.bande')).toHaveCount(4);

    // Les languettes : fines et semi-transparentes au repos, 44 px pour le doigt.
    for (const cote of ['.encoche-main', '.encoche-piles']) {
      const mesure = await page.locator(cote).evaluate((el) => {
        const corps = el.querySelector('.encoche-corps')!;
        return {
          bouton: el.getBoundingClientRect().width,
          corps: corps.getBoundingClientRect().width,
          opacite: Number(getComputedStyle(corps).opacity),
        };
      });
      expect(mesure.bouton, `${cote} : zone tactile`).toBeGreaterThanOrEqual(CIBLE_MINIMUM);
      expect(mesure.corps, `${cote} : languette fine`).toBeLessThanOrEqual(26);
      expect(mesure.opacite, `${cote} : semi-transparente au repos`).toBeLessThan(1);
    }

    await verifierLeCadre(page, 'mulligan');
    await verifierLesCibles(page, 'mulligan');
    await capture(page, '1-arrivee', largeur);

    // « Garder ma main » est une action : le bandeau « Annuler » s'allume.
    const garder = page.locator('.assistant-confirmer').first();
    await garder.waitFor({ state: 'visible', timeout: 60_000 });
    await garder.tap();
    const bandeau = page.locator('.bandeau-annuler');
    await expect(bandeau, 'le bandeau Annuler apres une action').toBeVisible({ timeout: 10_000 });
    const boite = (await bandeau.boundingBox())!;
    expect(boite.x).toBeGreaterThanOrEqual(0);
    expect(boite.x + boite.width).toBeLessThanOrEqual(largeur + TOLERANCE);
    await verifierLesCibles(page, 'bandeau Annuler');
    await capture(page, '2-bandeau-annuler', largeur);
    await expect(bandeau, 'le bandeau part seul au bout de 5 s').toHaveCount(0, { timeout: 8_000 });

    // La main : toucher une carte jouable fait apparaitre « Jouer ».
    await page.locator('.encoche-main').tap();
    await expect(page.locator('.main-feuille')).toBeVisible();
    const cartes = page.locator('.main-portrait-carte');
    const n = await cartes.count();
    expect(n).toBeGreaterThan(0);
    let jouer = false;
    for (let i = 0; i < n && !jouer; i++) {
      await cartes.nth(i).locator('.scan-card').tap();
      if (await page.locator('.carte-ouverte').isVisible()) {
        await page.locator('.carte-ouverte-fermer').tap();
        continue;
      }
      jouer = await page.locator('.main-feuille-jouer').isVisible();
    }
    expect(jouer, 'aucune carte de la main ne propose « Jouer » au premier tour').toBe(true);
    await verifierLeCadre(page, 'main ouverte');
    await verifierLesCibles(page, 'main ouverte');
    await capture(page, '3-main-jouer', largeur);
    await page.locator('.main-feuille-fermer').tap();

    // Le menu « … » en feuille basse.
    await page.locator('.portrait-menu-bouton').tap();
    await expect(page.locator('.portrait-menu')).toBeVisible();
    await verifierLesCibles(page, 'menu');
    await capture(page, '4-menu', largeur);
    await page.locator('.portrait-menu-bouton').tap();

    // La taille du texte, au plus grand : rien ne deborde, rien ne retrecit.
    await page.evaluate(() => {
      localStorage.setItem('marvel-tel-taille-texte', 'tres-grand');
      window.dispatchEvent(new CustomEvent('marvel:reglages-telephone'));
    });
    await expect(page.locator('html')).toHaveAttribute('data-taille-texte', 'tres-grand');
    await verifierLeCadre(page, 'texte tres grand');
    await verifierLesCibles(page, 'texte tres grand');
    await capture(page, '5-texte-tres-grand', largeur);
    await page.locator('.encoche-main').tap();
    await verifierLeCadre(page, 'texte tres grand, main ouverte');
    await verifierLesCibles(page, 'texte tres grand, main ouverte');
    await capture(page, '6-texte-tres-grand-main', largeur);
    await page.locator('.main-feuille-fermer').tap();

    // Les reglages du telephone, dans la fenetre des Reglages.
    await page.locator('.portrait-menu-bouton').tap();
    await page.locator('.portrait-menu .bh-plus').first().tap();
    await expect(page.getByRole('group', { name: 'Taille du texte' })).toBeVisible();
    await expect(page.getByRole('switch', { name: /Verrou portrait/ })).toBeVisible();
    await capture(page, '7-reglages', largeur);
    await page.evaluate(() => localStorage.removeItem('marvel-tel-taille-texte'));

    expect(erreurs, 'erreurs de page').toEqual([]);
  });
}

test('a 768 px et plus, et telephone couche (844 px) : le plateau PC', async ({ page }) => {
  await nouvellePartie(page.request);
  for (const [w, h] of [[768, 1024], [844, 390], [1366, 768]] as const) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto('/app/board.html');
    await expect(page.locator('.plateau-scene'), `${w}x${h} : plateau PC`).toBeVisible({ timeout: 60_000 });
    await expect(page.locator('.plateau-portrait')).toHaveCount(0);
    if (w === 844) await page.screenshot({ path: `${CAPTURES}844x390-paysage-plateau-pc.png` });
  }
});
