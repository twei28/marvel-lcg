// CAPTURE PONCTUELLE (04/10/2026) : les deux apercus de la fenetre « Choisis ton
// affichage » de la preparation. Une vraie partie (Spider-Man / Rhino), menee
// jusqu'a la question de defense de la phase du mechant, capturee en Normal
// puis en Sobre. A lancer contre le moteur d'ESSAI (UI_CHECK_BASE), jamais
// contre une partie en cours. Ce n'est pas une verification.
// Range HORS de tests/ pour ne jamais partir avec la suite : le copier dans
// tests/ le temps de le lancer, puis l'en retirer.
import { test, expect } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const SORTIE = process.env.SORTIE_CAPTURES || path.resolve('captures-tmp');

test('apercus Normal / Sobre sur une question de la phase du mechant', async ({ page, request }) => {
  test.setTimeout(240_000);
  fs.mkdirSync(SORTIE, { recursive: true });
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const deck = await (await request.get('/get_hero_json?spider_man')).json();
  const charge = {
    campaign_json: JSON.stringify(scenario),
    campaign_log: {},
    challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(deck)],
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321,
    timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);

  await page.setViewportSize({ width: 1600, height: 900 });
  await page.addInitScript(() => { try { localStorage.setItem('mc_affichage_v1', 'normal'); } catch { /* */ } });
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  // Spider-Man commence en forme civile : contre un alter ego, Rhino manigance
  // et n'attaque pas, la question de defense n'arriverait jamais. Moteur
  // d'ESSAI seulement : on le passe en forme heros par l'API Puzzle.
  const bascule = await page.request.post('/sandbox_command?p=0', {
    data: { commands: ["Puzzle.ChangeForm('01001b')"] },
  });
  console.log('bascule', bascule.status(), await bascule.text());

  const visible = async (nom: RegExp) => {
    const b = page.getByRole('button', { name: nom }).first();
    return (await b.count()) > 0 && (await b.isVisible()) ? b : undefined;
  };
  let trouve = false;
  for (let i = 0; i < 120 && !trouve; i++) {
    await page.waitForTimeout(700);
    if (await visible(/^Ne pas (défendre|utiliser)|^Ne rien jouer/)) { trouve = true; break; }
    const defausser = await visible(/^Défausser \d/);
    if (defausser && (await defausser.isDisabled())) {
      await page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/ })
        .first().click({ timeout: 2000 }).catch(() => {});
      continue;
    }
    for (const nom of [/^Garder ma main/, /^Défausser \d/, /Suivant/, /^Continuer/, /^Fin de phase/i, /Fin du tour/]) {
      const b = await visible(nom);
      if (b && !(await b.isDisabled())) { await b.click({ timeout: 2000 }).catch(() => {}); break; }
    }
    if (i % 10 === 0) await page.screenshot({ path: path.join(SORTIE, `etape-${i}.png`) });
  }
  expect(trouve, 'aucune question de la phase du mechant').toBe(true);
  await page.waitForTimeout(2500);
  await page.screenshot({ path: path.join(SORTIE, 'affichage-normal.png') });

  // Bascule par les Reglages, SANS recharger : un rechargement reconstruit le
  // cartouche et fausse la comparaison (onglets et titre perdus).
  await page.getByRole('button', { name: /Plus d'options/ }).first().click();
  await page.getByRole('button', { name: /Réglages/ }).first().click();
  await page.getByRole('button', { name: /^Sobre$/ }).first().click();
  await page.screenshot({ path: path.join(SORTIE, 'reglages-ouverts.png') });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(2500);
  await page.screenshot({ path: path.join(SORTIE, 'affichage-sobre.png') });
});
