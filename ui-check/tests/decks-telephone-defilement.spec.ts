// Décks au téléphone (rapport de l'utilisateur, 26/10/2026, Chrome Android ~412 px) : deux défauts.
//
//  1. « Voir les cartes » d'un deck : le volet n'affichait que les trois ou quatre premières rangées de cartes,
//     IMPOSSIBLE de défiler au doigt jusqu'à la dernière. Cause : `html[data-epure] .deck-modal-panel { overflow: hidden }`
//     (affichage-epure-pages.css) écrase le `overflow: auto` du panneau, et rien d'autre ne défilait.
//  2. Onglet Decks : un grand cadre vide en pointillés avant les decks. Cause : `.deck-aspects-bascule { flex: 0 0 100% }`
//     (prepare.css), pensé pour une rangée qui passe à la ligne ; sur téléphone la liste est une COLONNE, et 100 %
//     devient 100 % de la HAUTEUR de la liste : chaque bouton « Paquets d'aspect / Decks du tableur » faisait ~273 px.
//
// Lancement (port d'essai, jamais celui du jeu de l'utilisateur) :
//   export UI_CHECK_BASE=http://127.0.0.1:2331
//   npx playwright test tests/decks-telephone-defilement.spec.ts --project=pc
import { test, expect, type Page } from '@playwright/test';

const FORMATS = [
  { w: 360, h: 740 },
  { w: 390, h: 844 },
  { w: 412, h: 915 },
];

/** Accueil au téléphone → Solo → un héros → étape Decks. */
async function versLesDecks(page: Page) {
  await page.goto('/prepare.html');
  await page.locator('.acc-tel-jouer').waitFor({ timeout: 60_000 });
  await page.locator('.acc-tel-jouer').tap();
  await page.locator('.acc-tel-feuille').getByRole('button', { name: /^Solo/ }).tap();
  const tuile = page.locator('.tb-port[data-hero="storm"]');
  await tuile.waitFor({ timeout: 60_000 });
  await tuile.tap();
  await page.getByRole('button', { name: /^continuer/i }).tap();
  await expect(page.locator('.pstep.active')).toContainText(/decks/i, { timeout: 15_000 });
  await page.locator('.tel-deck').first().waitFor({ timeout: 60_000 });
  await page.waitForTimeout(500);
}

// Les deux affichages : « normal » (celui du filet) et « épuré » (le défaut du jeu, celui du téléphone de l'utilisateur,
// où `html[data-epure] .deck-modal-panel { overflow: hidden }` bloquait le défilement).
const AFFICHAGES = ['normal', 'epure'];

for (const { w, h } of FORMATS) for (const affichage of AFFICHAGES) {
  test.describe(`decks au téléphone, ${w}×${h}, affichage ${affichage}`, () => {
    test.use({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true });
    test.beforeEach(async ({ page }) => {
      await page.addInitScript((a) => { try { localStorage.setItem('mc_affichage_v1', a); } catch (e) { /* stockage indisponible */ } }, affichage);
    });

    test('la liste des decks suit les boutons : aucun bouton de bascule géant, aucun blanc', async ({ page }) => {
      await versLesDecks(page);
      const m = await page.evaluate(() => {
        const liste = document.getElementById('deck-liste')!;
        const outils = document.getElementById('deck-outils')!;
        const rl = liste.getBoundingClientRect();
        const ro = outils.getBoundingClientRect();
        const enfants = Array.from(liste.children).map((c) => {
          const r = c.getBoundingClientRect();
          return { cls: String(c.className).slice(0, 30), top: Math.round(r.top), bottom: Math.round(r.bottom), h: Math.round(r.height) };
        });
        const bascules = Array.from(document.querySelectorAll('.deck-aspects-bascule')).map((b) => Math.round(b.getBoundingClientRect().height));
        const dernier = enfants.filter((e) => e.h > 0).reduce((a, e) => Math.max(a, e.bottom), 0);
        return { listeH: Math.round(rl.height), listeTop: Math.round(rl.top), outilsBottom: Math.round(ro.bottom), bascules, dernierBas: dernier, nb: enfants.length };
      });
      expect(m.bascules.length, 'au moins une bascule « paquets d’aspect »').toBeGreaterThan(0);
      for (const hb of m.bascules) {
        expect(hb, 'un bouton de bascule fait une ligne, pas un quart d’écran').toBeLessThan(90);
      }
      expect(m.listeH, 'la liste englobe ses enfants (rien ne déborde de sa boîte)').toBeGreaterThanOrEqual(m.dernierBas - m.listeTop - 2);
      expect(m.listeTop - m.outilsBottom, 'pas de blanc entre les boutons et les decks').toBeLessThan(120);
      // Le premier deck (ou la première bascule) est dans le premier écran.
      const premier = await page.evaluate(() => {
        const e = document.querySelector('#deck-liste > *:not(.deck-aspects)') as HTMLElement;
        return Math.round(e.getBoundingClientRect().top);
      });
      expect(premier, 'le premier élément de la liste se voit sans défiler').toBeLessThan(h * 0.9);
    });

    test('le volet « Voir les cartes » défile au doigt jusqu’à la dernière carte, fermer reste visible', async ({ page }) => {
      await versLesDecks(page);
      await page.getByRole('button', { name: /voir les cartes/i }).first().tap();
      const panneau = page.locator('.deck-modal-panel');
      await panneau.waitFor({ timeout: 15_000 });
      await page.waitForFunction(() => document.querySelector('.deck-modal-panel')!.getAnimations().length === 0);
      await page.waitForTimeout(800);
      const avant = await page.evaluate(() => {
        const g = document.querySelector('.dm-grid') as HTMLElement;
        const p = document.querySelector('.deck-modal-panel') as HTMLElement;
        const zones = [p, g].map((e) => ({ oy: getComputedStyle(e).overflowY, sh: e.scrollHeight, ch: e.clientHeight }));
        const rp = p.getBoundingClientRect();
        return { zones, panneauBas: Math.round(rp.bottom), vh: innerHeight, droite: (document.querySelector('.tb-droite') as HTMLElement | null)?.scrollTop ?? 0 };
      });
      // Une des deux zones (le panneau ou la grille) est réellement défilable à la main.
      const defilable = avant.zones.find((z) => /(auto|scroll)/.test(z.oy) && z.sh > z.ch + 4);
      expect(defilable, 'le panneau ou la grille a une barre de défilement utilisable').toBeTruthy();
      expect(avant.panneauBas, 'la feuille ne dépasse pas le bas de l’écran').toBeLessThanOrEqual(avant.vh + 1);

      // Geste tactile réel (événements tactiles du protocole Chrome, comme un doigt). `Input.synthesizeScrollGesture` ne
      // déclenche rien en mode sans fenêtre : on envoie touchStart / touchMove / touchEnd nous-mêmes.
      const cdp = await page.context().newCDPSession(page);
      const x = Math.round(w / 2);
      const glisser = async (y0: number, y1: number) => {
        await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y: y0 }] });
        for (let i = 1; i <= 30; i += 1) {
          await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x, y: y0 + ((y1 - y0) * i) / 30 }] });
          await page.waitForTimeout(14);
        }
        await page.waitForTimeout(120);
        await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
        await page.waitForTimeout(450);
      };
      const bas0 = Math.round(h * 0.82);
      const haut0 = Math.round(h * 0.28);
      const lire = () => page.evaluate(() => {
        const g = document.querySelector('.dm-grid') as HTMLElement;
        const p = document.querySelector('.deck-modal-panel') as HTMLElement;
        return { g: g.scrollTop, p: p.scrollTop, page: scrollY, droite: (document.querySelector('.tb-droite') as HTMLElement | null)?.scrollTop ?? 0 };
      });
      const t0 = await lire();
      await glisser(bas0, haut0);
      const t1 = await lire();
      expect(t1.g + t1.p, 'un glissement du doigt fait défiler le deck').toBeGreaterThan(t0.g + t0.p + 100);
      expect(t1.page, 'la page derrière ne bouge pas').toBe(t0.page);
      expect(t1.droite, 'la colonne derrière ne bouge pas').toBe(t0.droite);

      // Jusqu'en bas : la dernière carte est entière à l'écran, et le bouton fermer se voit toujours.
      for (let i = 0; i < 8; i += 1) await glisser(bas0, haut0 - 20);
      const bas = await page.evaluate(() => {
        const cartes = document.querySelectorAll('.dm-card');
        const der = cartes[cartes.length - 1].getBoundingClientRect();
        const f = document.querySelector('.dm-close')!.getBoundingClientRect();
        const p = document.querySelector('.deck-modal-panel')!.getBoundingClientRect();
        return { derHaut: Math.round(der.top), derBas: Math.round(der.bottom), vh: innerHeight, fermerHaut: Math.round(f.top), fermerBas: Math.round(f.bottom), panneauHaut: Math.round(p.top) };
      });
      expect(bas.derBas, 'la dernière carte est atteinte').toBeLessThanOrEqual(bas.vh + 1);
      expect(bas.derHaut, 'la dernière carte est à l’écran').toBeGreaterThanOrEqual(0);
      expect(bas.fermerHaut, 'le bouton fermer reste visible en bas du deck').toBeGreaterThanOrEqual(0);
      expect(bas.fermerBas).toBeLessThanOrEqual(bas.vh);

      // Fermer fonctionne toujours.
      await page.locator('.dm-close').tap();
      await expect(page.locator('.deck-modal-panel')).toHaveCount(0);
    });
  });
}

/** Le PC : préparation → Solo → Storm → Decks → « Voir les cartes » d'un deck. */
async function voletSurPC(page: Page) {
  await page.goto('/prepare.html');
  await page.getByText(/^Solo/i).first().click({ timeout: 20_000 });
  const tuile = page.locator('.tb-port[data-hero="storm"]');
  await tuile.waitFor({ timeout: 30_000 });
  await tuile.click();
  await page.waitForTimeout(800);
  const valider = page.getByRole('button', { name: /^valider/i });
  if (await valider.count()) await valider.first().click();
  await page.waitForTimeout(600);
  await page.locator('.pstep', { hasText: /decks/i }).first().click({ timeout: 8_000 });
  await page.locator('.do-view').first().waitFor({ timeout: 30_000 });
  await page.locator('.do-view').first().click();
  await page.locator('.deck-modal-panel').waitFor({ timeout: 10_000 });
  await page.waitForTimeout(800);
}

// Le même verrou existait sur ordinateur : `overflow: hidden` sur le panneau, donc rien ne défilait à la molette. Invisible en
// 1920×1080 (le deck tient), mais sur un portable en 1366×768 la dernière rangée de cartes était coupée.
for (const { w, h } of [{ w: 1920, h: 1080 }, { w: 1366, h: 768 }]) for (const affichage of AFFICHAGES) {
  test.describe(`le PC, ${w}×${h}, affichage ${affichage}`, () => {
    test.use({ viewport: { width: w, height: h } });
    test.beforeEach(async ({ page }) => {
      await page.addInitScript((a) => { try { localStorage.setItem('mc_affichage_v1', a); } catch (e) { /* stockage indisponible */ } }, affichage);
    });
    test('le volet d’un deck : titre en place, la grille défile à la molette jusqu’à la dernière carte', async ({ page }) => {
      const erreurs: string[] = [];
      page.on('pageerror', (e) => erreurs.push(String(e)));
      await voletSurPC(page);
      expect(await page.evaluate(() => document.documentElement.classList.contains('tel')), 'pas de mode téléphone sur grand écran').toBe(false);
      const m = await page.evaluate(() => {
        const p = document.querySelector('.deck-modal-panel') as HTMLElement;
        const g = p.querySelector('.dm-grid') as HTMLElement;
        const rp = p.getBoundingClientRect();
        return { panneauBas: Math.round(rp.bottom), panneauHaut: Math.round(rp.top), vh: innerHeight, gOv: getComputedStyle(g).overflowY, gSH: g.scrollHeight, gCH: g.clientHeight };
      });
      expect(m.panneauHaut, 'le panneau tient dans la fenêtre').toBeGreaterThanOrEqual(0);
      expect(m.panneauBas).toBeLessThanOrEqual(m.vh + 1);
      // Si le deck dépasse (portable), la grille défile ; sinon (grand écran) il n'y a rien à défiler et rien n'est coupé.
      if (m.gSH > m.gCH + 4) expect(m.gOv, 'la grille défile quand elle dépasse').toBe('auto');
      const box = (await page.locator('.dm-grid').boundingBox())!;
      // Sur la gouttière de la grille (barre de défilement) : l'aperçu d'une carte survolée, en affichage normal, se pose sous le
      // curseur et avale la molette, ce qui n'a rien à voir avec ce qu'on mesure ici.
      await page.mouse.move(box.x + box.width - 6, box.y + box.height / 2);
      for (let i = 0; i < 6; i += 1) { await page.mouse.wheel(0, 700); await page.waitForTimeout(120); }
      await page.waitForTimeout(300);
      const bas = await page.evaluate(() => {
        const cartes = document.querySelectorAll('.dm-card');
        const der = cartes[cartes.length - 1].getBoundingClientRect();
        const f = document.querySelector('.dm-close')!.getBoundingClientRect();
        return { derBas: Math.round(der.bottom), derHaut: Math.round(der.top), vh: innerHeight, fermerHaut: Math.round(f.top) };
      });
      expect(bas.derBas, 'la dernière carte est atteignable à la molette').toBeLessThanOrEqual(bas.vh + 1);
      expect(bas.derHaut).toBeGreaterThanOrEqual(0);
      expect(bas.fermerHaut, 'le bouton fermer reste visible').toBeGreaterThanOrEqual(0);
      await page.locator('.dm-close').click();
      await expect(page.locator('.deck-modal-panel')).toHaveCount(0);
      expect(erreurs).toEqual([]);
    });
  });
}
