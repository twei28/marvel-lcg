// LA MISE EN PLACE DANS L'ORDRE DU LIVRET (10/10/2026), sur une vraie partie
// Tower Defense : les deux manigances se montrent avant le choix de dégâts du
// Black Order Besieger, et chaque carte qui arrive en jeu est présentée en
// grand, une par une, avec « Continuer ».
//
// ⚠ JAMAIS SUR LE 2345 (la partie du joueur) : le cas crée une partie.
//   UI_CHECK_BASE=http://127.0.0.1:2386 MEP=apres WSLENV=UI_CHECK_BASE:MEP \
//     npx playwright test tests/mise-en-place-pas-a-pas.spec.ts --project=pc
// Sans MEP, le fichier se saute. MEP nomme les captures
// (`.planning/captures-mise-en-place/<MEP>-...png`). MEP_EN=1 : en anglais.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

test.skip(!process.env.MEP, 'mise en place pas à pas : MEP=avant|apres et un moteur d’essai');

const SORTIE = path.resolve('..', '.planning', 'captures-mise-en-place');
const EN = Boolean(process.env.MEP_EN);
const VARIANTE = `${process.env.MEP ?? 'apres'}${EN ? '-en' : ''}`;

async function partie(page: Page, largeur: number, hauteur: number) {
  await page.setViewportSize({ width: largeur, height: hauteur });
  const request = page.request;
  const scenario = await (await request.get('/get_scenario_json?the_tower_defense')).json();
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?spider_man')).json())],
    // Les règles d'une partie neuve lancée par la préparation (launcher.js).
    rules: [...(contrat as { regles_partie_standard: string[] }).regles_partie_standard,
      'confirm_main_scheme', 'confirm_side_scheme', 'confirm_scheme_setup_order'],
    seed: 2468, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
  await page.addInitScript((en) => {
    try {
      localStorage.setItem('marvel-langue-choisie', '1');
      localStorage.setItem('marvel-langue', en ? 'en' : 'fr');
      // La mise en place pas à pas n'existe que dans ce mode (10/10/2026).
      localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille');
    } catch { /* */ }
  }, EN);
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
}

/** Avance la mise en place jusqu'au mulligan et note ce qui s'est montré. */
async function derouler(page: Page, prefixe: string, capture = false): Promise<string[]> {
  fs.mkdirSync(SORTIE, { recursive: true });
  const vu: string[] = [];
  for (let i = 0; i < 40; i++) {
    await page.waitForTimeout(700);
    const nom = `${prefixe}-${String(i).padStart(2, '0')}`;
    const couche = page.locator('.mep-couche');
    if (await couche.isVisible().catch(() => false)) {
      const legende = (await page.locator('.mep-legende').innerText()).trim();
      vu.push(`carte:${legende}`);
      // Une seule capture : le sbire présenté avant son choix de dégâts.
      if (capture && /^(Sbire|Minion)$/.test(legende)) await page.screenshot({ path: path.join(SORTIE, `${nom}-carte.png`) });
      await page.locator('.mep-continuer').click();
      continue;
    }
    const panneau = page.locator('.panneau-manigance');
    if (await panneau.isVisible().catch(() => false)) {
      const alt = await panneau.locator('img').first().getAttribute('alt');
      vu.push(`manigance:${alt}`);
      await panneau.locator('button').last().click();
      await panneau.waitFor({ state: 'hidden', timeout: 8000 }).catch(() => {});
      continue;
    }
    const tour = page.getByRole('button', { name: /Avengers Tower|Tour des Avengers/i }).first();
    if (await tour.isVisible().catch(() => false)) {
      vu.push('choix:Black Order Besieger');
      await tour.click();
      continue;
    }
    if (await page.getByText(/mulligan/i).first().isVisible().catch(() => false)) {
      vu.push('mulligan');
      break;
    }
  }
  console.log(`${prefixe} : ${vu.join(' | ')}`);
  return vu;
}

test('Tower Defense : la mise en place dans l’ordre du livret (PC)', async ({ page }) => {
  test.setTimeout(240_000);
  await partie(page, 1920, 1080);
  const vu = await derouler(page, `${VARIANTE}-1920`, true);
  if (process.env.MEP === 'apres') {
    const choix = vu.indexOf('choix:Black Order Besieger');
    expect(choix).toBeGreaterThan(0);
    expect(vu.slice(0, choix).filter((x) => x.startsWith('manigance:')).length).toBe(2);
    expect(vu.slice(0, choix).some((x) => x.startsWith('carte:'))).toBe(true);
  }
});

test('Tower Defense : la mise en place sur téléphone (360 px)', async ({ page }) => {
  test.setTimeout(240_000);
  await partie(page, 360, 780);
  await derouler(page, `${VARIANTE}-360`);
  const largeur = await page.evaluate(() => document.documentElement.scrollWidth);
  expect(largeur).toBeLessThanOrEqual(360);
});
