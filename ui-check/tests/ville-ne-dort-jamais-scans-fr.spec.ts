// « La ville ne dort jamais » : The City (pu005) et Never Sleeps (pu006) sont deux environnements dont les illustrations se raccordent
// (panorama-jumelles.ts). En FRANCAIS, ce sont les scans francais de l'equipe MC×DC (`fr_pu005`, `fr_pu006`, illustrations recollees par
// .planning/mcdc-punisher/panorama-city-fr.py) qui doivent s'afficher, sans voile ; scans francais coupes, on retrouve l'anglais.
//
// Moteur d'ESSAI seulement : UI_CHECK_BASE=http://127.0.0.1:<port libre, jamais 2345>. Meme montage que panorama-sans-trait.spec.ts :
// la partie reelle est un Leonardo contre Rhino, les deux cartes sont ajoutees au /get_world par une route simulee.
// SORTIE_CAPTURES=<dossier> garde la capture.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const SORTIE = process.env.SORTIE_CAPTURES;

async function partie(page: Page) {
  const request = page.request;
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const decks = [JSON.stringify(await (await request.get('/get_hero_json?leonardo')).json())];
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: decks, rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
}

for (const [reglage, attendu] of [['on', 'fr_'], ['off', '']] as const) {
  test(`The City + Never Sleeps : scans ${reglage === 'on' ? 'francais' : 'anglais'} sur la table`, async ({ browser }) => {
    test.setTimeout(150_000);
    const ctx = await browser.newContext({ viewport: { width: 1600, height: 900 }, storageState: './.auth/state.json', reducedMotion: 'reduce' });
    await ctx.addInitScript((r) => window.localStorage.setItem('marvel-board-scans-fr', r), reglage);
    const page = await ctx.newPage();
    await partie(page);
    await page.route('**/get_world*', async (route) => {
      const rep = await route.fetch();
      const w = await rep.json();
      if (w.players?.length && w.players[0].area_hero.length) {
        const h = w.players[0].area_hero;
        const modele = JSON.parse(JSON.stringify(h[0]));
        for (const [id, code, nom] of [[91, 'pu005', 'The City'], [92, 'pu006', 'Never Sleeps']] as const) {
          if (!h.some((c: { id: number }) => c.id === id)) {
            h.push({ ...modele, id, card_id: code, pic_id: code, name: nom, card_type: 'Environment', bind_object_id: 1, is_ready: true, down_card_ids: [], info: {}, traits: {}, effects: [], resources: [] });
          }
        }
      }
      await route.fulfill({ response: rep, json: w });
    });
    await page.goto('/app/board.html', { waitUntil: 'networkidle' });
    await expect(page.locator('.scan-card.est-panorama.panorama-gauche')).toBeVisible({ timeout: 40_000 });
    for (let i = 0; i < 12; i++) {
      const b = page.getByRole('button', { name: /Continuer/ }).first();
      if (await b.isVisible().catch(() => false)) await b.click().catch(() => {});
      else if (i > 2) break;
      await page.waitForTimeout(700);
    }
    await page.waitForFunction(() =>
      [...document.querySelectorAll('.scan-card.est-panorama img')].every((i) => (i as HTMLImageElement).complete && (i as HTMLImageElement).naturalWidth > 0)
    );
    const sources = await page.locator('.scan-card.est-panorama img').evaluateAll((l) => l.map((i) => (i as HTMLImageElement).currentSrc));
    expect(sources.some((s) => s.includes(`/${attendu}pu005`)), `gauche : ${sources.join(' | ')}`).toBe(true);
    expect(sources.some((s) => s.includes(`/${attendu}pu006`)), `droite : ${sources.join(' | ')}`).toBe(true);
    if (!attendu) expect(sources.some((s) => s.includes('fr_pu00'))).toBe(false);
    if (SORTIE) {
      fs.mkdirSync(SORTIE, { recursive: true });
      fs.writeFileSync(path.join(SORTIE, `ville-${reglage}.png`), await page.screenshot());
    }
    await ctx.close();
  });
}
