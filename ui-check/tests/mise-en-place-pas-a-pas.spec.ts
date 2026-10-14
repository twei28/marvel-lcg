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

/** Les cartes que la table montre en pointillés, et si leur contenu est bien caché. */
async function enAttente(page: Page): Promise<{ id: string; existe: boolean; cachee: boolean }[]> {
  return page.evaluate(() => {
    const style = [...document.querySelectorAll('style')].find((s) => s.textContent?.includes('outline: 2px dashed'));
    const ids = [...new Set([...(style?.textContent ?? '').matchAll(/data-card-id="(\d+)"/g)].map((m) => m[1]))];
    return ids.map((id) => {
      const el = document.querySelector<HTMLElement>(`.scan-card[data-card-id="${id}"]:not(.mep-fantome)`);
      const enfant = el?.firstElementChild as HTMLElement | null | undefined;
      // La pile des stades à venir derrière la carte attend avec elle.
      const stades = [...(el?.parentElement?.querySelectorAll<HTMLElement>(':scope > .stage-arriere') ?? [])];
      const stadesCaches = stades.every((st) => getComputedStyle(st).visibility === 'hidden');
      return { id, existe: Boolean(el), cachee: enfant ? getComputedStyle(enfant).visibility === 'hidden' && stadesCaches : false };
    });
  });
}

// 13/10/2026 : la table ne montre une carte qu'après son « Continuer ».
test('Tower Defense : les cartes attendent leur « Continuer » en pointillés (PC)', async ({ page }) => {
  test.skip(process.env.MEP !== 'apres', 'comportement du 13/10/2026');
  test.setTimeout(240_000);
  fs.mkdirSync(SORTIE, { recursive: true });
  await partie(page, 1920, 1080);
  let etapesVues = 0;
  let poseesVues = 0;
  let volVu = false;
  let retournementsVus = 0;
  const vus: string[] = [];
  for (let i = 0; i < 60; i++) {
    await page.waitForTimeout(600);
    if (await page.locator('.mep-couche').isVisible().catch(() => false)) {
      const legende = (await page.locator('.mep-legende').innerText()).trim();
      const retournement = /retourn|flipped/i.test(legende);
      const jeton = /^(Dégâts|Menace|Damage|Threat)$/i.test(legende);
      const avant = await enAttente(page);
      for (const c of avant) expect(c, `carte ${c.id} en pointillés`).toMatchObject({ existe: true, cachee: true });
      if (!retournement && !jeton) expect(avant.length, `${legende} : la carte attend en pointillés`).toBeGreaterThan(0);
      // Un retournement : la table montre encore l'autre face, la nouvelle n'arrive qu'au clic.
      // Le plateau sert /vignette/<image>, la grande carte /scan/<image> : on compare le nom.
      const grande = ((await page.locator('.mep-cadre img').getAttribute('src')) ?? '').split('/').pop() ?? '';
      const surTable = (nom: string) =>
        page.evaluate(
          (n) => [...document.querySelectorAll('.scan-card:not(.mep-fantome) img')].some((i) => (i.getAttribute('src') ?? '').split('/').pop() === n),
          nom
        );
      if (retournement) expect(await surTable(grande), 'face B pas encore sur la table').toBe(false);
      vus.push(legende);
      if (etapesVues === 0) await page.screenshot({ path: path.join(SORTIE, `table-attente-avant.png`) });
      await page.locator('.mep-continuer').click();
      await page.waitForTimeout(180);
      if (await page.locator('.mep-couche.est-en-vol').isVisible().catch(() => false)) {
        if (!volVu) await page.screenshot({ path: path.join(SORTIE, `table-attente-vol.png`) });
        volVu = true;
      }
      await page.waitForTimeout(700);
      const apres = new Set((await enAttente(page)).map((c) => c.id));
      const posees = avant.filter((c) => !apres.has(c.id))
      for (const c of posees) {
        const visible = await page.evaluate((id) => {
          const el = document.querySelector<HTMLElement>(`.scan-card[data-card-id="${id}"]`);
          const enfant = el?.firstElementChild as HTMLElement | null | undefined;
          return enfant ? getComputedStyle(enfant).visibility !== 'hidden' : false;
        }, c.id);
        expect(visible, `carte ${c.id} posée et visible`).toBe(true);
      }
      poseesVues += posees.length;
      if (retournement) {
        expect(await surTable(grande), 'face B sur la table après le clic').toBe(true);
        retournementsVus++;
      }
      if (etapesVues === 0) await page.screenshot({ path: path.join(SORTIE, `table-attente-apres.png`) });
      etapesVues++;
      continue;
    }
    const panneau = page.locator('.panneau-manigance');
    if (await panneau.isVisible().catch(() => false)) {
      const attente = await enAttente(page);
      expect(attente.length, 'la manigance du panneau attend en pointillés').toBeGreaterThan(0);
      await panneau.locator('button').last().click();
      await panneau.waitFor({ state: 'hidden', timeout: 8000 }).catch(() => {});
      continue;
    }
    const tour = page.getByRole('button', { name: /Avengers Tower|Tour des Avengers/i }).first();
    if (await tour.isVisible().catch(() => false)) {
      await tour.click();
      continue;
    }
    if (await page.getByText(/mulligan/i).first().isVisible().catch(() => false)) break;
  }
  console.log(`étapes ${etapesVues} (${vus.join(' | ')}), cartes posées ${poseesVues}, retournements ${retournementsVus}, vol vu ${volVu}`);
  expect(etapesVues).toBeGreaterThan(2);
  expect(poseesVues).toBeGreaterThan(0);
  expect(volVu).toBe(true);
  // Au mulligan, plus rien n'attend.
  expect(await enAttente(page)).toEqual([]);
});
