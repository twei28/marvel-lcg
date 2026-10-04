// VERIFICATION PONCTUELLE (04/10/2026) : la frise de la phase du mechant.
// Six onglets, resultat court, etapes vides, relecture d'un onglet passe,
// revue dans le volet du journal ; PC puis telephone. Moteur d'ESSAI seulement
// (cree une partie). Range HORS de tests/ : le copier le temps du lancement.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const SORTIE = process.env.SORTIE_CAPTURES || path.resolve('captures-tmp');

async function nouvellePartie(page: Page, largeur: number, hauteur: number) {
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
  await page.setViewportSize({ width: largeur, height: hauteur });
  await page.addInitScript(() => {
    try {
      localStorage.setItem('mc_affichage_v1', 'normal');
      localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille');
    } catch { /* */ }
  });
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  await page.request.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.ChangeForm('01001b')"] } });
}

const visible = async (page: Page, nom: RegExp) => {
  const b = page.getByRole('button', { name: nom }).first();
  return (await b.count()) > 0 && (await b.isVisible()) ? b : undefined;
};

/** Joue le tour du joueur jusqu'a l'ouverture de la frise. */
async function jusquALaFrise(page: Page) {
  for (let i = 0; i < 150; i++) {
    await page.waitForTimeout(600);
    if (await page.locator('.deroule-phase .deroule-temps').count()) return;
    const defausser = await visible(page, /^Défausser \d/);
    if (defausser && (await defausser.isDisabled())) {
      await page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/ })
        .first().click({ timeout: 2000 }).catch(() => {});
      continue;
    }
    for (const nom of [/^Garder ma main/, /^Défausser \d/, /^Continuer/, /^Fin de phase/i, /Fin du tour/]) {
      const b = await visible(page, nom);
      if (b && !(await b.isDisabled())) { await b.click({ timeout: 2000 }).catch(() => {}); break; }
    }
  }
  await page.screenshot({ path: path.join(SORTIE, 'frise-jamais-ouverte.png') });
  throw new Error('la frise ne s est jamais ouverte');
}

/** Avance dans la phase en capturant chaque etape, jusqu'au bilan. */
async function jusquAuBilan(page: Page, prefixe: string) {
  const titres: string[] = [];
  for (let i = 0; i < 60; i++) {
    await page.waitForTimeout(900);
    if (await visible(page, /^À toi de jouer/)) return titres;
    const titres_ = page.locator('.deroule-phase .deroule-titre');
    const titre = (await titres_.count()) ? ((await titres_.first().textContent({ timeout: 1000 }).catch(() => '')) ?? '') : '';
    const suivant = await visible(page, /^Suivant$/);
    if (suivant) {
      titres.push(titre);
      await page.screenshot({ path: path.join(SORTIE, `${prefixe}-${String(titres.length).padStart(2, '0')}.png`) });
      await suivant.click({ timeout: 4000 }).catch((e) => console.log('SUIVANT REFUSE', String(e).slice(0, 400)));
      continue;
    }
    for (const nom of [/^Ne pas défendre/, /^Ne pas utiliser/, /^Ne rien jouer/, /^Passer/, /^Fin de phase/i]) {
      const b = await visible(page, nom);
      if (b) {
        await page.screenshot({ path: path.join(SORTIE, `${prefixe}-question-${i}.png`) });
        const ok = await b.click({ timeout: 4000 }).then(() => true).catch((e) => {
          console.log('CLIC REFUSE', nom, String(e).replace(/\s+/g, ' ').slice(0, 900));
          return false;
        });
        if (!ok) {
          await page.screenshot({ path: path.join(SORTIE, `${prefixe}-clic-refuse-${i}.png`) });
          await b.click({ force: true }).catch(() => {});
        }
        break;
      }
    }
  }
  await page.screenshot({ path: path.join(SORTIE, `${prefixe}-echec.png`) });
  throw new Error('jamais arrive au bilan ; titres vus : ' + titres.join(' | '));
}

test('frise : PC', async ({ page }) => {
  test.setTimeout(400_000);
  fs.mkdirSync(SORTIE, { recursive: true });
  await nouvellePartie(page, 1600, 900);
  await jusquALaFrise(page);
  const titres = await jusquAuBilan(page, 'frise-pc');
  console.log('ETAPES', JSON.stringify(titres));
  await page.screenshot({ path: path.join(SORTIE, 'frise-pc-bilan.png') });
  // Relecture d'un onglet passe : le second (2a, le mechant).
  await page.locator('.deroule-temps li button').nth(1).click();
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(SORTIE, 'frise-pc-relecture.png') });
  await page.getByRole('button', { name: /Revenir à l’étape en cours/ }).click();
  await page.getByRole('button', { name: /^À toi de jouer/ }).click();
  await page.waitForTimeout(1500);
  await page.locator('.volet-journal-languette').click();
  await page.getByRole('button', { name: 'Revoir la phase du méchant' }).click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(SORTIE, 'frise-pc-revue.png') });
  await page.keyboard.press('Escape');
  // HORS PHASE : en plein tour du joueur, le mechant s'active (une carte de
  // boost posee sur son paquet, Puzzle.Boost). Le cartouche d'un seul coup.
  await page.request.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.Boost('01101')"] } });
  for (let i = 0; i < 60; i++) {
    await page.waitForTimeout(700);
    if (i % 7 === 0) await page.screenshot({ path: path.join(SORTIE, `frise-pc-hors-phase-${i}.png`) });
    const b = await visible(page, /^Ne pas (défendre|utiliser)|^Passer|^Continuer|^OK/);
    if (b) { console.log('HORS-PHASE CLIC', await b.textContent()); await b.click({ timeout: 3000 }).catch(() => {}); }
    if (await page.locator('.deroule-phase.est-hors-phase').count()) break;
  }
  await page.screenshot({ path: path.join(SORTIE, 'frise-pc-hors-phase.png') });
  await expect(page.locator('.deroule-phase.est-hors-phase')).toBeVisible();
});

test('frise : telephone', async ({ page }) => {
  test.setTimeout(400_000);
  fs.mkdirSync(SORTIE, { recursive: true });
  // Le tour du joueur se joue en largeur PC (la defausse de fin de tour se fait
  // autrement au doigt) ; la largeur telephone vient une fois la phase ouverte.
  await nouvellePartie(page, 1600, 900);
  await jusquALaFrise(page);
  await page.setViewportSize({ width: 412, height: 900 });
  await page.waitForTimeout(1000);
  await jusquAuBilan(page, 'frise-tel');
  await page.screenshot({ path: path.join(SORTIE, 'frise-tel-bilan.png') });
});
