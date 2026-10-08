// « Partie au hasard » à l'écran (08/10/2026) : la tuile, les bandeaux qui
// tournent puis s'arrêtent l'un après l'autre, la relance d'un seul bandeau,
// le parcours habituel ensuite, et le bouton Aléatoire de l'étape Scénario
// qui tire dans toutes les boîtes. Décisions :
// .planning/todos/2026-10-08-roue-du-hasard.md. Moteur requis.
import { test, expect, type Page } from '@playwright/test';

// La config du harnais coupe le mouvement : ici on VEUT voir tourner.
test.use({ reducedMotion: 'no-preference' });
// Le premier tirage lit tous les scénarios de toutes les boîtes : moteur froid, c'est long.
test.setTimeout(120000);

async function accueil(page: Page) {
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-mode', { timeout: 30000 });
}

/** Le nom sous le repère de chaque bandeau, dans l'ordre. */
async function sousLesReperes(page: Page): Promise<string[]> {
  return page.$$eval('.roue-modal .roue-fenetre', (fenetres) => fenetres.map((f) => {
    const r = f.querySelector('.roue-repere')!.getBoundingClientRect();
    const centre = r.left + r.width / 2;
    const c = [...f.querySelectorAll('.roue-case')].find((x) => {
      const b = x.getBoundingClientRect();
      return b.left <= centre && centre <= b.right;
    });
    return c ? (c.querySelector('.roue-case-nom')?.textContent ?? '') : '';
  }));
}

async function ouvrirRoue(page: Page, nombre: number) {
  const tuile = page.locator('.acc-tuile', { hasText: 'Partie au hasard' });
  await expect(tuile).toHaveCount(1);
  if (nombre === 1) await tuile.locator('.acc-mode').click({ position: { x: 20, y: 20 } });
  else await tuile.locator('.acc-nombre', { hasText: String(nombre) }).click();
  await page.waitForSelector('.roue-modal .roue-fenetre');
  // Les heures d'arrêt, bandeau par bandeau.
  await page.evaluate(() => {
    (window as any).__arrets = [];
    const obs = new MutationObserver(() => {
      document.querySelectorAll('.roue-fenetre.est-arrete').forEach((f, i) => {
        const tous = [...document.querySelectorAll('.roue-fenetre')];
        const idx = tous.indexOf(f);
        if (!(window as any).__arrets.some((a: any) => a.idx === idx)) {
          (window as any).__arrets.push({ idx, t: performance.now() });
        }
      });
    });
    obs.observe(document.body, { subtree: true, attributes: true, attributeFilter: ['class'] });
  });
}

async function attendreArret(page: Page) {
  await page.waitForFunction(() => document.querySelectorAll('.roue-fenetre.en-cours').length > 0, null, { timeout: 30000 });
  await page.waitForFunction(() => document.querySelectorAll('.roue-fenetre.en-cours').length === 0, null, { timeout: 15000 });
}

test('solo : un heros, un scenario, puis le parcours habituel', async ({ page }) => {
  // Le fichier est en cache après le premier clic : on compte les lectures,
  // pas les requêtes.
  await page.addInitScript(() => {
    (window as any).__clics = 0;
    const jouer = HTMLMediaElement.prototype.play;
    HTMLMediaElement.prototype.play = function (this: HTMLMediaElement) {
      if (this.src.endsWith('/survol.wav')) (window as any).__clics += 1;
      return jouer.call(this).catch(() => {});
    };
  });
  await accueil(page);
  await ouvrirRoue(page, 1);
  await expect(page.locator('.roue-modal .roue-fenetre')).toHaveCount(2);
  await expect(page.locator('.roue-modal .roue-fanmade input')).toBeVisible();
  await page.waitForFunction(() => document.querySelectorAll('.roue-fenetre.en-cours').length > 0, null, { timeout: 30000 });
  await page.waitForTimeout(900);
  await page.screenshot({ path: 'captures-tmp/roue-solo-en-cours.png' });
  await attendreArret(page);
  const [heros, scenario] = await sousLesReperes(page);
  expect(heros).not.toBe('');
  expect(scenario).not.toBe('');
  await page.screenshot({ path: 'captures-tmp/roue-solo-arret.png' });
  // Le heros s'arrete AVANT le scenario.
  const arrets = await page.evaluate(() => (window as any).__arrets);
  expect(arrets.map((a: any) => a.idx)).toEqual([0, 1]);
  const clics = await page.evaluate(() => (window as any).__clics);
  expect(clics, 'des clics pendant que ca tourne').toBeGreaterThan(5);

  await page.locator('.roue-actions .btn.primary').click();
  await expect(page.locator('.roue-modal')).toHaveCount(0);
  // Étape Decks, avec le heros tire.
  await expect(page.locator('.progress, .steps, header').first()).toBeVisible();
  await page.locator('.nav .btn.primary').click();
  // Étape Scénario : le scenario tire est pose.
  await page.waitForSelector('#scn-grid .tb-port');
  const nomChoisi = await page.locator('#scn-grid .tb-port.chosen .tb-port-nom').first().textContent();
  expect(nomChoisi?.trim()).toBeTruthy();
  await page.screenshot({ path: 'captures-tmp/roue-solo-etape-scenario.png' });
});

test('3 joueurs : trois heros differents, arret l un apres l autre, relance d un seul', async ({ page }) => {
  await accueil(page);
  await ouvrirRoue(page, 3);
  await expect(page.locator('.roue-modal .roue-fenetre')).toHaveCount(4);
  await attendreArret(page);
  const avant = await sousLesReperes(page);
  expect(new Set(avant.slice(0, 3)).size).toBe(3);
  const arrets = await page.evaluate(() => (window as any).__arrets);
  expect(arrets.map((a: any) => a.idx)).toEqual([0, 1, 2, 3]);
  await page.screenshot({ path: 'captures-tmp/roue-3-arret.png' });

  // Relance du joueur 2 : seul son bandeau tourne.
  await page.locator('.roue-ligne').nth(1).locator('.roue-relancer').click();
  await page.waitForFunction(() => document.querySelectorAll('.roue-fenetre.en-cours').length === 1, null, { timeout: 5000 });
  const enCours = await page.$$eval('.roue-fenetre', (fs) => fs.map((f) => f.classList.contains('en-cours')));
  expect(enCours).toEqual([false, true, false, false]);
  await page.waitForFunction(() => document.querySelectorAll('.roue-fenetre.en-cours').length === 0, null, { timeout: 10000 });
  const apres = await sousLesReperes(page);
  expect(apres[0]).toBe(avant[0]);
  expect(apres[2]).toBe(avant[2]);
  expect(apres[3]).toBe(avant[3]);
  expect(apres[1]).not.toBe(avant[1]);
  expect(new Set(apres.slice(0, 3)).size).toBe(3);
});

test('le bouton Aleatoire de l etape Scenario tire dans toutes les boites', async ({ page }) => {
  await accueil(page);
  await ouvrirRoue(page, 1);
  await attendreArret(page);
  await page.locator('.roue-actions .btn.primary').click();
  await page.locator('.nav .btn.primary').click();
  await page.waitForSelector('#scn-grid .tb-port');
  const onglets = new Set<string>();
  for (let i = 0; i < 8; i++) {
    await page.locator('.nav .btn.ghost', { hasText: 'Aléatoire' }).click();
    await page.waitForTimeout(700);
    const onglet = await page.locator('.ext-tab.on').getAttribute('title');
    if (onglet) onglets.add(onglet);
    await expect(page.locator('#scn-grid .tb-port.chosen')).toHaveCount(1);
  }
  expect(onglets.size, [...onglets].join(' | ')).toBeGreaterThan(1);
  for (const o of onglets) expect(o).not.toMatch(/Custom|Weekly|defis/);
});

test('mouvement reduit : les bandeaux se posent sans defiler', async ({ browser }) => {
  const contexte = await browser.newContext({ reducedMotion: 'reduce', storageState: './.auth/state.json' });
  const page = await contexte.newPage();
  await accueil(page);
  await ouvrirRoue(page, 2);
  await page.waitForFunction(() => document.querySelectorAll('.roue-fenetre.est-pose').length === 3, null, { timeout: 90000 });
  expect(await page.locator('.roue-fenetre.en-cours').count()).toBe(0);
  const noms = await sousLesReperes(page);
  expect(noms.every(Boolean)).toBe(true);
  await page.screenshot({ path: 'captures-tmp/roue-reduit.png' });
  await contexte.close();
});
