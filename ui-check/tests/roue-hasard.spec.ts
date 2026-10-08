// « Partie au hasard » : le tirage de la roue (08/10/2026).
//
// `roue.js` décide ce qui peut sortir et tire sans doublon. Cas fabriqués,
// module réel importé dans la page. Décisions :
// .planning/todos/2026-10-08-roue-du-hasard.md.
import { test, expect, type Page } from '@playwright/test';

const HEROS = [
  { id: 'spider_man', heroCardId: '01001a', name: 'Spider-Man', homebrew: false },
  { id: 'iron_man', heroCardId: '01029a', name: 'Iron Man', homebrew: false },
  { id: 'she_hulk', heroCardId: '01019a', name: 'She-Hulk', homebrew: false },
  { id: 'zeus', heroCardId: 'ze001a', name: 'Zeus', homebrew: true },
];
const SCENARIOS = [
  { id: 'rhino', name: 'Rhino', extension: '1. Core Set', homebrew: false, challenges: [] },
  { id: 'klaw', name: 'Klaw', extension: '1. Core Set', homebrew: false, challenges: [] },
  { id: 'gorr_expert', name: 'Gorr', extension: '136. Custom (Gorr)', homebrew: true, challenges: [] },
  { id: 'gorr', name: 'Gorr', extension: '136. Custom (Gorr)', homebrew: true, challenges: [] },
  { id: '2401_the_ground_is_lava', name: 'Lava', extension: 'Weekly Challenges', homebrew: false, challenges: ['c'] },
  { id: 'vision_pvp_competitive', name: 'Vision', extension: '57. Synthezoid Smackdown', homebrew: false, challenges: [] },
  { id: 'vision_pvp', name: 'Vision', extension: '57. Synthezoid Smackdown', homebrew: false, challenges: [] },
  { id: 'rhino', name: 'Rhino', extension: 'defis', homebrew: false, challenges: [] },
];

async function roue(page: Page, corps: string) {
  return page.evaluate(async ({ corps, HEROS, SCENARIOS }) => {
    const mod: any = await import('/public/js/prepare/roue.js');
    return new Function('mod', 'HEROS', 'SCENARIOS', corps)(mod, HEROS, SCENARIOS);
  }, { corps, HEROS, SCENARIOS });
}

test.beforeEach(async ({ page }) => { await page.goto('/prepare.html'); });

test('officiels seulement par defaut, fan-made sur la case', async ({ page }) => {
  const r = await roue(page, `return {
    off: mod.herosTirables(HEROS).map((h) => h.id),
    tous: mod.herosTirables(HEROS, { fanmade: true }).map((h) => h.id),
    scnOff: mod.scenariosTirables(SCENARIOS).map((s) => s.id),
    scnTous: mod.scenariosTirables(SCENARIOS, { fanmade: true }).map((s) => s.id),
  };`);
  expect(r.off).toEqual(['spider_man', 'iron_man', 'she_hulk']);
  expect(r.tous).toEqual(['spider_man', 'iron_man', 'she_hulk', 'zeus']);
  // Ni défi, ni Expert, ni compétitif, ni doublon d'onglet.
  expect(r.scnOff).toEqual(['rhino', 'klaw', 'vision_pvp']);
  expect(r.scnTous).toEqual(['rhino', 'klaw', 'gorr', 'vision_pvp']);
});

test('legacy : seul ce qui est ouvert sort', async ({ page }) => {
  const r = await roue(page, `
    const verrou = {
      heros: (h) => ({ ouvert: h.id !== 'iron_man' }),
      scenario: (s) => ({ ouvert: s.id === 'klaw' }),
    };
    return {
      heros: mod.herosTirables(HEROS, { fanmade: true, verrou }).map((h) => h.id),
      scn: mod.scenariosTirables(SCENARIOS, { fanmade: true, verrou }).map((s) => s.id),
    };`);
  expect(r.heros).toEqual(['spider_man', 'she_hulk', 'zeus']);
  expect(r.scn).toEqual(['klaw']);
});

test('jamais deux fois le meme heros, et jamais un exclu', async ({ page }) => {
  const r = await roue(page, `
    const pool = mod.herosTirables(HEROS, { fanmade: true });
    const tirages = [];
    for (let i = 0; i < 200; i++) tirages.push(mod.tirerPlusieurs(pool, 3, { exclus: ['zeus'] }).map((h) => h.id));
    const relance = [];
    for (let i = 0; i < 100; i++) relance.push(mod.tirer(pool, { exclus: ['spider_man', 'iron_man', 'she_hulk'] }).id);
    return {
      doublon: tirages.some((t) => new Set(t).size !== t.length),
      zeus: tirages.some((t) => t.includes('zeus')),
      tailles: [...new Set(tirages.map((t) => t.length))],
      relance: [...new Set(relance)],
      trop: mod.tirerPlusieurs(pool, 9).length,
      vide: mod.tirer(pool, { exclus: pool.map((h) => h.id) }),
    };`);
  expect(r.doublon).toBe(false);
  expect(r.zeus).toBe(false);
  expect(r.tailles).toEqual([3]);
  expect(r.relance).toEqual(['zeus']);
  // Le pool s'épuise : moins de cases, jamais de doublon inventé.
  expect(r.trop).toBe(4);
  expect(r.vide).toBeNull();
});

test('la bande s arrete sur le gagnant et repart de ce qu on voyait', async ({ page }) => {
  const r = await roue(page, `
    const pool = HEROS.map((h) => ({ id: h.id }));
    const gagnant = { id: 'she_hulk' };
    const depart = { id: 'zeus' };
    const b = mod.bande(pool, gagnant, { depart });
    return {
      gagnant: b.cases[b.indexGagnant].id,
      depart: b.cases[b.indexDepart].id,
      apres: b.cases.length - b.indexGagnant - 1,
      bornes: [mod.avancement(0), mod.avancement(1), mod.avancement(2)],
      ralentit: mod.avancement(0.5) > 0.5,
    };`);
  expect(r.gagnant).toBe('she_hulk');
  expect(r.depart).toBe('zeus');
  expect(r.apres).toBe(4);
  expect(r.bornes).toEqual([0, 1, 1]);
  expect(r.ralentit).toBe(true);
});
