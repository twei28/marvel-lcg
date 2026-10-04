// VERIFICATION PONCTUELLE (04/10/2026) : la table personnalisable. Editeur,
// grille aimantee, taille des cartes, enregistrement, une disposition par
// nombre de joueurs, disposition d'origine, garde-fou ; plusieurs tailles
// d'ecran. Moteur d'ESSAI seulement (cree des parties). Range HORS de tests/.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const SORTIE = process.env.SORTIE_CAPTURES || path.resolve('captures-tmp');

async function partie(page: Page, heros: string[]) {
  const request = page.request;
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const decks = await Promise.all(heros.map(async (h) => JSON.stringify(await (await request.get('/get_hero_json?' + h)).json())));
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: decks, rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
}

async function ouvrir(page: Page, largeur: number, hauteur: number) {
  await page.setViewportSize({ width: largeur, height: hauteur });
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  await expect(page.locator('.plateau-scene')).toBeVisible({ timeout: 30_000 });
  await page.waitForTimeout(1500);
}

const tables = (page: Page) => page.evaluate(() => localStorage.getItem('mc_table_v1'));

test('table personnalisable : solo, editeur, enregistrement, tailles d ecran', async ({ page }) => {
  test.setTimeout(300_000);
  fs.mkdirSync(SORTIE, { recursive: true });
  await partie(page, ['spider_man']);
  await page.addInitScript(() => { try { localStorage.setItem('mc_affichage_v1', 'normal'); } catch { /* */ } });
  await ouvrir(page, 1600, 900);
  await page.screenshot({ path: path.join(SORTIE, 'table-origine-1600.png') });

  // Reglages → « Modifier la table ».
  await page.getByRole('button', { name: /Plus d'options/ }).first().click();
  await page.getByRole('button', { name: /Réglages/ }).first().click();
  await page.getByRole('button', { name: 'Modifier la table' }).click();
  await expect(page.locator('.editeur-table')).toBeVisible();
  expect(await page.locator('.editeur-zone').count()).toBe(9);
  await page.screenshot({ path: path.join(SORTIE, 'table-editeur.png') });

  // Glisser « Piles du héros » deux lignes plus haut (place libre a gauche).
  const piles = page.locator('.editeur-zone[data-zone="piles-joueur"]');
  const b = (await piles.boundingBox())!;
  const ligne = b.height / 2; // la zone fait deux lignes
  await page.mouse.move(b.x + b.width / 2, b.y + 10);
  await page.mouse.down();
  await page.mouse.move(b.x + b.width / 2, b.y + 10 - 2 * ligne, { steps: 8 });
  await page.screenshot({ path: path.join(SORTIE, 'table-editeur-glisse.png') });
  await page.mouse.up();
  // Glisser « Main » sur le combat : refuse (rouge), rien ne change.
  const main = page.locator('.editeur-zone[data-zone="main"]');
  const m = (await main.boundingBox())!;
  await page.mouse.move(m.x + m.width / 2, m.y + 20);
  await page.mouse.down();
  await page.mouse.move(m.x + m.width / 2, m.y + 20 - 4 * (m.height / 2), { steps: 8 });
  await expect(page.locator('.editeur-fantome.est-refuse')).toBeVisible();
  await page.screenshot({ path: path.join(SORTIE, 'table-editeur-refus.png') });
  await page.mouse.up();
  expect(await main.getAttribute('style')).toContain('7 / 3 / span 2 / span 10');
  // La taille des cartes de la main : +20 % au clavier.
  const poignee = main.locator('.editeur-poignee-taille');
  await poignee.focus();
  for (let i = 0; i < 4; i++) await page.keyboard.press('ArrowUp');
  await expect(poignee).toHaveText(/120%/);
  await page.getByRole('button', { name: 'Terminer' }).click();
  await expect(page.locator('.editeur-table')).toHaveCount(0);
  const ecrit = await tables(page);
  console.log('STOCKE', ecrit);
  expect(ecrit).toContain('table-1');
  await page.screenshot({ path: path.join(SORTIE, 'table-perso-1600.png') });

  // Tailles d'ecran : la disposition suit.
  for (const [l, h] of [[1920, 1080], [1366, 768], [1280, 720]]) {
    await ouvrir(page, l, h);
    await page.screenshot({ path: path.join(SORTIE, `table-perso-${l}.png`) });
  }

  // Garde-fou : une disposition abimee revient a l'origine.
  await page.evaluate(() => localStorage.setItem('mc_table_v1', JSON.stringify({ 'table-1': '12x8|abime' })));
  await ouvrir(page, 1600, 900);
  await page.screenshot({ path: path.join(SORTIE, 'table-garde-fou.png') });
  const aires = await page.locator('.plateau-scene').evaluate((n) => (n as HTMLElement).style.gridTemplateAreas);
  expect(aires).toContain('piles-rencontre rencontre complot-principal complots-secondaires');
});

test('table personnalisable : une disposition par nombre de joueurs, puis l origine', async ({ page }) => {
  test.setTimeout(300_000);
  fs.mkdirSync(SORTIE, { recursive: true });
  await partie(page, ['spider_man', 'black_panther']);
  await page.addInitScript(() => {
    try {
      localStorage.setItem('mc_affichage_v1', 'normal');
      // Une table « solo » deja choisie : elle ne doit PAS servir a deux joueurs.
      localStorage.setItem('mc_table_v1', JSON.stringify({
        'table-1': '12x8|1,1,2,2,100;3,1,2,2,100;5,1,3,2,100;8,1,5,2,100;3,3,10,2,100;3,5,10,2,100;1,5,2,2,100;1,7,2,2,100;3,7,10,2,140',
      }));
    } catch { /* */ }
  });
  await ouvrir(page, 1600, 900);
  const colonnes = await page.locator('.plateau-scene').evaluate((n) => (n as HTMLElement).style.gridTemplateColumns);
  expect(colonnes, 'a deux joueurs, la table solo ne doit pas s appliquer').toBe('');
  await page.screenshot({ path: path.join(SORTIE, 'table-2-joueurs-origine.png') });
  await page.getByRole('button', { name: /Plus d'options/ }).first().click();
  await page.getByRole('button', { name: /Réglages/ }).first().click();
  await page.getByRole('button', { name: 'Modifier la table' }).click();
  const poignee = page.locator('.editeur-zone[data-zone="terrain-soutien"] .editeur-poignee-taille');
  await poignee.focus();
  for (let i = 0; i < 4; i++) await page.keyboard.press('ArrowDown');
  await page.getByRole('button', { name: 'Terminer' }).click();
  const ecrit = await tables(page);
  console.log('STOCKE-2', ecrit);
  expect(ecrit).toContain('table-2');
  await page.screenshot({ path: path.join(SORTIE, 'table-2-joueurs-perso.png') });
  // « Disposition d'origine » remet tout pour ce nombre de joueurs.
  await page.getByRole('button', { name: /Plus d'options/ }).first().click();
  await page.getByRole('button', { name: /Réglages/ }).first().click();
  await page.getByRole('button', { name: 'Modifier la table' }).click();
  await page.getByRole('button', { name: 'Disposition d’origine' }).click();
  await page.getByRole('button', { name: 'Terminer' }).click();
  const apres = await tables(page);
  console.log('STOCKE-3', apres);
  expect(apres).not.toContain('table-2');
  expect(apres).toContain('table-1');
});

for (const heros of [['spider_man', 'black_panther', 'captain_marvel'], ['spider_man', 'black_panther', 'captain_marvel', 'she_hulk']]) {
  test(`table personnalisable : ${heros.length} joueurs`, async ({ page }) => {
    test.setTimeout(300_000);
    fs.mkdirSync(SORTIE, { recursive: true });
    await partie(page, heros);
    await page.addInitScript(() => { try { localStorage.setItem('mc_affichage_v1', 'normal'); } catch { /* */ } });
    await ouvrir(page, 1600, 900);
    await page.screenshot({ path: path.join(SORTIE, `table-${heros.length}-joueurs-origine.png`) });
    await page.getByRole('button', { name: /Plus d'options/ }).first().click();
    await page.getByRole('button', { name: /Réglages/ }).first().click();
    await page.getByRole('button', { name: 'Modifier la table' }).click();
    const poignee = page.locator('.editeur-zone[data-zone="terrain-soutien"] .editeur-poignee-taille');
    await poignee.focus();
    for (let i = 0; i < 6; i++) await page.keyboard.press('ArrowDown');
    await page.getByRole('button', { name: 'Terminer' }).click();
    const ecrit = await tables(page);
    expect(ecrit).toContain(`table-${heros.length}`);
    await page.screenshot({ path: path.join(SORTIE, `table-${heros.length}-joueurs-perso.png`) });
  });
}
