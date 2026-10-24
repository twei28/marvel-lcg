// L'assistant de préparation sur téléphone portrait (refonte du 09/10/2026,
// fiche .planning/todos/2026-10-09-mode-telephone-refonte.md).
//
// Pour chaque largeur de 320 à 430 px, on déroule l'assistant au doigt
// (Solo, héros, decks, méchant, final) et on exige à CHAQUE écran :
//   - aucun débordement horizontal de la page ;
//   - aucune zone tactile visible sous 44 px.
// Plus le comportement : aperçu au toucher puis « Choisir », bandeau qui
// rétrécit au défilement, Retour du système = étape précédente, feuille
// basse fermée en glissant, menu burger, mode sobre.
//
// Lancement (Windows, port d'essai, jamais celui du jeu de l'utilisateur) :
//   export UI_CHECK_BASE=http://127.0.0.1:2331 WSLENV=UI_CHECK_BASE
//   npx playwright test tests/assistant-telephone.spec.ts --project=pc
// CAPTURES_TEL=1 (relayé par WSLENV) range aussi des captures 360 et 430 dans
// .planning/captures-telephone/.
import { test, expect, type Page } from '@playwright/test';

const FORMATS = [
  { w: 320, h: 640 },
  { w: 360, h: 740 },
  { w: 390, h: 844 },
  { w: 430, h: 932 },
];
const CAPTURER = !!process.env.CAPTURES_TEL;
const DOSSIER = '../.planning/captures-telephone';

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
      // Un défilement horizontal VOULU (rangée d'extensions) clippe ses enfants.
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
      // Hors de l'écran (sous le pli d'une zone qui défile) : on mesure quand même.
      if (r.width < 43.5 || r.height < 43.5) {
        out.push(cible.tagName.toLowerCase() + '.' + String(cible.className).slice(0, 40) + ' "' + (cible.textContent || '').trim().slice(0, 20) + '" ' + Math.round(r.width) + 'x' + Math.round(r.height));
      }
    }
    return out.slice(0, 10);
  });
}

/** Accueil au téléphone (zone 2) : le gros bouton Jouer ouvre la feuille des
 *  façons de jouer, où l'on touche Solo. */
async function solo(page: Page) {
  const jouer = page.locator('.acc-tel-jouer');
  await jouer.waitFor({ timeout: 30_000 });
  await jouer.tap();
  await page.locator('.acc-tel-feuille').getByRole('button', { name: /^Solo/ }).tap();
}

async function verifier(page: Page, nom: string) {
  expect(await debordements(page), 'débordement horizontal : ' + nom).toEqual([]);
  expect(await petitesZones(page), 'zones tactiles sous 44 px : ' + nom).toEqual([]);
}

async function capturer(page: Page, w: number, nom: string) {
  if (!CAPTURER || (w !== 360 && w !== 430)) return;
  await page.waitForTimeout(250);
  await page.screenshot({ path: `${DOSSIER}/${w}-${nom}.png` });
}

for (const { w, h } of FORMATS) {
  test.describe(`assistant au téléphone, ${w} px`, () => {
    test.use({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true });
    // Le filet force l'affichage « Coloré » (global-setup) : pour les captures on montre l'Épuré, le défaut du jeu.
    test.beforeEach(async ({ page }) => {
      if (CAPTURER) await page.addInitScript(() => { try { localStorage.setItem('mc_affichage_v1', 'epure'); } catch (e) { /* stockage indisponible */ } });
    });

    test('le parcours complet : sans débordement, zones de 44 px', async ({ page }) => {
      test.setTimeout(120_000);
      await page.goto('/prepare.html');
      await page.locator('.acc-tel-jouer').waitFor({ timeout: 30_000 });
      await capturer(page, w, '0-accueil');
      await solo(page);

      // --- Étape Héros : un toucher choisit, « Continuer » en bas ------------
      const tuile = page.locator('.tb-port[data-hero="storm"]');
      await tuile.waitFor({ timeout: 30_000 });
      await expect(page.locator('html')).toHaveClass(/\btel\b/);
      await expect(page.locator('.tel-entete')).toBeVisible();
      await expect(page.locator('.pstep.active')).toContainText(/[ée]quipe/i);
      await capturer(page, w, '1-heros');
      await verifier(page, 'héros');

      const cols = await page.evaluate(() => {
        const g = document.getElementById('hero-grid')!;
        return getComputedStyle(g).gridTemplateColumns.split(' ').length;
      });
      expect(cols, 'la grille a trois colonnes').toBe(3);

      await tuile.tap();
      await expect(page.locator('.ts-titre b')).toContainText(/storm/i);
      await expect(tuile, 'un toucher choisit le héros (24/10/2026)').toHaveClass(/\bchosen\b/);
      await expect(page.locator('.fiche-heros')).toHaveCount(0);
      const choisir = page.locator('.ts-btn.jaune');
      await expect(choisir).toBeVisible();
      await capturer(page, w, '2-heros-apercu');

      // Le bandeau rétrécit au défilement et garde « Choisir ». Toucher Storm a
      // fait défiler la grille : on remonte avant de mesurer la pleine hauteur.
      await page.locator('.tb-droite').evaluate((e) => { e.scrollTop = 0; });
      await expect(page.locator('.team-b')).not.toHaveClass(/\bcompact\b/);
      const plein = await page.locator('#tb-scene').evaluate((e) => e.getBoundingClientRect().height);
      expect(plein, 'le bandeau fait environ un quart de l’écran').toBeGreaterThan(h * 0.18);
      expect(plein).toBeLessThan(h * 0.4);
      await page.locator('.tb-droite').evaluate((e) => { e.scrollTop = 400; });
      await expect(page.locator('.team-b')).toHaveClass(/\bcompact\b/);
      const mini = await page.locator('#tb-scene').evaluate((e) => e.getBoundingClientRect().height);
      expect(mini, 'le bandeau réduit tient en une ligne').toBeLessThanOrEqual(70);
      await expect(page.locator('.ts-btn.jaune')).toBeVisible();
      await capturer(page, w, '3-heros-bandeau-reduit');
      await verifier(page, 'héros, bandeau réduit');
      await page.locator('.tb-droite').evaluate((e) => { e.scrollTop = 0; });

      // La fiche : feuille basse pleine largeur, fermée en glissant la poignée.
      await page.getByRole('button', { name: /^fiche/i }).tap();
      const fiche = page.locator('.fiche-heros');
      await expect(fiche).toBeVisible();
      // La feuille monte en 0,18 s : on mesure une fois posée.
      await page.waitForFunction(() => document.querySelector('.deck-modal-panel')!.getAnimations().length === 0);
      const bf = (await fiche.boundingBox())!;
      expect(bf.width).toBeGreaterThanOrEqual(w - 2);
      expect(bf.y + bf.height, 'la feuille est collée en bas').toBeGreaterThanOrEqual(h - 2);
      await capturer(page, w, '4-heros-fiche');
      await verifier(page, 'fiche du héros');
      const poignee = (await page.locator('.tel-poignee').boundingBox())!;
      expect(poignee.height).toBeGreaterThanOrEqual(44);
      const x = poignee.x + poignee.width / 2;
      const y = poignee.y + poignee.height / 2;
      await page.mouse.move(x, y);
      await page.mouse.down();
      await page.mouse.move(x, y + 40, { steps: 4 });
      await page.mouse.move(x, y + 160, { steps: 6 });
      await page.mouse.up();
      await expect(fiche, 'glisser la poignée ferme la feuille').toHaveCount(0);

      // Le héros est déjà choisi : « Continuer » en bas mène aux decks, sans « Options ».
      await page.getByRole('button', { name: /^continuer/i }).tap();
      await expect(page.locator('.pstep.active')).toContainText(/decks/i, { timeout: 8_000 });
      await expect(page.locator('.vh-panel'), 'plus de fenêtre « Options de ce héros »').toHaveCount(0);

      // Retour du système : on revient aux héros, Storm toujours choisie.
      await page.goBack();
      await expect(page.locator('.pstep.active')).toContainText(/[ée]quipe/i);
      await expect(page.locator('.tb-port[data-hero="storm"]')).toHaveClass(/\bchosen\b/);
      await page.getByRole('button', { name: /^continuer/i }).tap();
      await expect(page.locator('.pstep.active')).toContainText(/decks/i);

      // --- Étape Decks ---------------------------------------------------------
      await page.locator('.tel-deck').first().waitFor({ timeout: 30_000 });
      await capturer(page, w, '5-decks');
      await verifier(page, 'decks');
      await page.getByRole('button', { name: /importer/i }).tap();
      await expect(page.locator('.feuille-import')).toBeVisible();
      await capturer(page, w, '6-decks-import');
      await verifier(page, 'feuille d’import');
      await page.mouse.click(w / 2, 20);
      await expect(page.locator('.feuille-import')).toHaveCount(0);

      // --- Étape Méchant ---------------------------------------------------------
      await page.getByRole('button', { name: /^continuer/i }).tap();
      await expect(page.locator('.pstep.active')).toContainText(/m[ée]chant/i);
      const scn = page.locator('.tb-port[data-scn]').first();
      await scn.waitFor({ timeout: 30_000 });
      await capturer(page, w, '7-mechant');
      await verifier(page, 'méchant');
      await scn.tap();
      await capturer(page, w, '8-mechant-apercu');
      // Un toucher choisit le méchant (24/10/2026) : « Continuer » s'allume sans passer par « Choisir ».
      await expect(page.getByRole('button', { name: /^continuer/i })).toBeEnabled({ timeout: 8_000 });
      // L'en-tête de l'étape nomme le méchant choisi (il restait « inconnu »).
      for (const mode of await page.locator('.tb-mode').all()) {
        await expect(mode).not.toContainText(/inconnu/i);
      }
      await verifier(page, 'méchant choisi');

      // --- Étape Final -----------------------------------------------------------
      await page.getByRole('button', { name: /^continuer/i }).tap();
      await expect(page.locator('.pstep.active')).toContainText(/final/i);
      await capturer(page, w, '9-final');
      expect(await debordements(page), 'débordement : final').toEqual([]);
    });

    test('le menu burger : langue en un toucher, liens, fermeture', async ({ page }) => {
      await page.goto('/prepare.html');
      await solo(page);
      await page.locator('.tb-port').first().waitFor({ timeout: 30_000 });
      await expect(page.locator('.tel-langue'), 'la langue se change sans ouvrir le menu').toBeVisible();
      await expect(page.locator('.tel-menu')).toBeHidden();
      await page.locator('#tel-burger').tap();
      await expect(page.locator('.tel-menu')).toBeVisible();
      await capturer(page, w, 'a-menu');
      await verifier(page, 'menu ouvert');
      await page.mouse.click(w / 2, h - 30);
      await expect(page.locator('.tel-menu')).toBeHidden();
    });

    test('la barre d’étapes est cliquable et le Retour du système recule d’une étape', async ({ page }) => {
      await page.goto('/prepare.html');
      await solo(page);
      await page.locator('.tb-port[data-hero="storm"]').waitFor({ timeout: 30_000 });
      await page.locator('.tb-port[data-hero="storm"]').tap();
      await page.getByRole('button', { name: /^continuer/i }).tap();
      await expect(page.locator('.pstep.active')).toContainText(/decks/i, { timeout: 8_000 });
      // Revenir par la barre d'étapes rejoue le recul de l'historique : la pile
      // reste propre (pas d'aller-retour Héros, Decks, Héros à défaire).
      await page.locator('.pstep').first().tap();
      await expect(page.locator('.pstep.active')).toContainText(/[ée]quipe/i);
      await page.getByRole('button', { name: /^continuer/i }).tap();
      await expect(page.locator('.pstep.active')).toContainText(/decks/i);
      await page.goBack();
      await expect(page.locator('.pstep.active')).toContainText(/[ée]quipe/i);
      await page.goBack();
      await expect(page.locator('.acc-tel-jouer'), 'on retombe sur l’accueil').toBeVisible();
    });
  });
}

test.describe('mode sobre au téléphone', () => {
  test.use({ viewport: { width: 360, height: 740 }, hasTouch: true, isMobile: true });

  test('sans flou ni dégradé, mêmes règles de taille', async ({ page }) => {
    await page.addInitScript(() => { try { localStorage.setItem('mc_affichage_v1', 'sobre'); } catch (e) { /* stockage indisponible */ } });
    await page.goto('/prepare.html');
    await expect(page.locator('html')).toHaveAttribute('data-affichage', 'sobre');
    await solo(page);
    await page.locator('.tb-port[data-hero="storm"]').waitFor({ timeout: 30_000 });
    await page.locator('.tb-port[data-hero="storm"]').tap();
    const flous = await page.evaluate(() => ['.tel-entete', '.nav'].map((s) => getComputedStyle(document.querySelector(s)!).backdropFilter));
    expect(flous).toEqual(['none', 'none']);
    const fond = await page.locator('#tb-scene').evaluate((e) => getComputedStyle(e, '::after').backgroundImage);
    expect(fond, 'plus de dégradé sur le bandeau').not.toMatch(/gradient/);
    expect(await debordements(page)).toEqual([]);
    expect(await petitesZones(page)).toEqual([]);
    if (CAPTURER) await page.screenshot({ path: `${DOSSIER}/360-sobre-heros.png` });
  });
});

test.describe('le PC ne bouge pas', () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  test('à 1280 px : pas de mode téléphone', async ({ page }) => {
    await page.goto('/prepare.html');
    await page.getByRole('button', { name: /^Solo/ }).first().click();
    await page.locator('.tb-port').first().waitFor({ timeout: 30_000 });
    await expect(page.locator('html')).not.toHaveClass(/\btel\b/);
    await expect(page.locator('.tel-entete')).toHaveCount(0);
    await expect(page.locator('.tb-nomg')).toBeVisible();
  });
});
