// CAPTURE PONCTUELLE (05/10/2026) : les trois images de la fenetre « Choisis ta
// phase du mechant » du lanceur (public/img/phase-modes/). Vraies parties
// Spider-Man / Rhino, une par mode, moteur d'ESSAI seulement (UI_CHECK_BASE),
// jamais contre une partie en cours. Ce n'est pas une verification.
// Range HORS de tests/ : le copier dans tests/ le temps de le lancer.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

test.use({ reducedMotion: 'no-preference' });
const DEST = path.resolve('..', 'Fusion', 'marvel-lcg-src', 'public', 'img', 'phase-modes');

async function partie(page: Page, mode: string) {
  const request = page.request;
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const deck = await (await request.get('/get_hero_json?spider_man')).json();
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(deck)], rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.addInitScript((m) => {
    try {
      localStorage.setItem('mc_affichage_v1', 'normal');
      localStorage.setItem('marvel-board-mode-phase-mechant', m);
      localStorage.setItem('marvel-board-revelation', 'off');
    } catch { /* */ }
  }, mode);
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  await page.request.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.ChangeForm('01001b')"] } });
}

const visible = async (page: Page, nom: RegExp) => {
  const b = page.getByRole('button', { name: nom }).first();
  return (await b.count()) > 0 && (await b.isVisible()) ? b : undefined;
};

async function jouerJusqua(page: Page, fini: () => Promise<boolean>, tours = 400) {
  for (let i = 0; i < tours; i++) {
    if (await fini()) return true;
    await page.waitForTimeout(300);
    if (await fini()) return true;
    const defausser = await visible(page, /^Défausser \d/);
    if (defausser && (await defausser.isDisabled())) {
      await page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/ })
        .first().click({ timeout: 2000 }).catch(() => {});
      continue;
    }
    for (const nom of [/^Garder ma main/, /^Défausser \d/, /^Suivant/, /^Ne pas (défendre|utiliser)/, /^Passer/, /^Continuer/, /^Fin de phase/i, /Fin du tour/]) {
      const b = await visible(page, nom);
      if (b && !(await b.isDisabled())) { await b.click({ timeout: 2000 }).catch(() => {}); break; }
    }
  }
  return fini();
}

const CIBLES: Record<string, { fichier: string; atteint: (page: Page) => Promise<boolean> }> = {
  // Cartouche central, frise des etapes et bouton « Suivant » : etape « Attaque ».
  detaille: {
    fichier: 'etape.jpg',
    atteint: async (page) => {
      const titre = page.locator('.deroule-titre-court');
      return (await titre.count()) > 0 && /attaque/i.test((await titre.first().textContent()) ?? '');
    },
  },
  // Les cartes bougent sur la table : l'annonce « va attaquer », l'attaquant en surbrillance.
  'sur-table': {
    fichier: 'sur-table.jpg',
    atteint: async (page) => (await page.getByText(/va attaquer/i).count()) > 0,
  },
  // L'interruption : le joueur peut jouer une carte (Sens d'araignee) avant l'attaque.
  instantane: {
    fichier: 'd-un-coup.jpg',
    atteint: async (page) => (await page.getByText(/peut réagir/i).count()) > 0,
  },
};

for (const mode of ['detaille', 'sur-table', 'instantane']) {
  test(`mode ${mode}`, async ({ page }) => {
    test.setTimeout(300_000);
    fs.mkdirSync(DEST, { recursive: true });
    await partie(page, mode);
    const cible = CIBLES[mode];
    expect(await jouerJusqua(page, () => cible.atteint(page))).toBe(true);
    const TMP = path.resolve('captures-tmp-modes');
    await page.waitForTimeout(3000);
    let traits = 0;
    let recaps = 0;
    for (let n = 0; n < 70 && traits < 8; n++) {
      for (let k = 0; k < 8; k++) {
        if ((await page.locator('svg.trait-phase, .ligne-cible, .charge-carte').count()) > 0) {
          await page.screenshot({ path: path.join(TMP, `${mode}-trait${String(traits).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 62 });
          traits++;
        }
        await page.waitForTimeout(110);
      }
      if ((await page.getByRole('dialog', { name: /Défaite|Victoire/ }).count()) > 0) break;
      if (recaps < 4 && (await visible(page, /^Continuer/))) {
        for (let r = 0; r < 4; r++) { await page.waitForTimeout(1300); await page.screenshot({ path: path.join(TMP, `${mode}-recap${recaps}.jpg`), type: 'jpeg', quality: 62 }); recaps++; }
      }
      const defausser = await visible(page, /^Défausser \d/);
      if (defausser && (await defausser.isDisabled())) {
        await page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/ }).first().click({ timeout: 2000 }).catch(() => {});
      } else {
        for (const nom of [/^Garder ma main/, /^Défausser \d/, /^Suivant/, /^Ne pas (défendre|utiliser)/, /^Passer/, /^Continuer/, /^Fin de phase/i, /Fin du tour/]) {
          const bt = await visible(page, nom);
          if (bt && !(await bt.isDisabled())) { await bt.click({ timeout: 2000 }).catch(() => {}); break; }
        }
      }
    }
    console.log('TRAITS', traits);
  });
}
