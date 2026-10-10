// L'ESSAI « NOUVELLE PHASE DU MÉCHANT » (10/10/2026) : captures réelles.
//
// Même partie que le n°72 (Klaw contre Spider-Man, Stepford Cuckoos à son
// dernier psi), mais en forme HÉROS : Klaw attaque avec ses boosts, puis
// Weapons Runner (Renfort) révèle Klaw's Vengeance, annulée par Stepford, et
// Sonic Boom la remplace.
//
// ⚠ JAMAIS SUR LE 2345 (la partie du joueur) : le cas crée une partie, sur un
// moteur d'essai dont la configuration porte `essai_phase_mechant: true`.
//   UI_CHECK_BASE=http://127.0.0.1:2338 ESSAI_PHASE=fr WSLENV=UI_CHECK_BASE:ESSAI_PHASE \
//     npx playwright test tests/phase-mechant-essai.spec.ts --project=pc
// ESSAI_PHASE vaut fr, en ou sobre. Sans lui, le fichier se saute.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

test.skip(!process.env.ESSAI_PHASE, 'captures de l’essai : ESSAI_PHASE=fr|en|sobre et un moteur d’essai');

const SORTIE = path.resolve('..', '.planning', 'captures-phase-mechant');
const VARIANTE = process.env.ESSAI_PHASE ?? 'fr';

async function partie(page: Page, largeur: number, hauteur: number) {
  await page.setViewportSize({ width: largeur, height: hauteur });
  const request = page.request;
  const essais = await (await request.get('/get_essais')).json();
  expect(essais.phase_mechant, 'le moteur d’essai doit porter essai_phase_mechant').toBe(true);
  const scenario = await (await request.get('/get_scenario_json?klaw')).json();
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?spider_man')).json())],
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
  await page.addInitScript((variante) => {
    try {
      localStorage.setItem('mc_affichage_v1', variante === 'sobre' ? 'sobre' : 'normal');
      localStorage.setItem('marvel-langue-choisie', '1');
      localStorage.setItem('marvel-langue', variante === 'en' ? 'en' : 'fr');
      localStorage.setItem('marvel-board-scans-fr', variante === 'en' ? 'off' : 'on');
      localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille');
    } catch { /* */ }
  }, VARIANTE);
  await page.goto('/app/board.html', { waitUntil: 'networkidle' });
  const commandes = [
    // La face EN JEU (alter ego au départ) passe à l'autre : Spider-Man, pour que Klaw ATTAQUE.
    "Puzzle.ChangeForm('01001b')",
    "Puzzle.PutIntoPlay('45049')",
    "Puzzle.Counter('45049', 'psi', -2)",
    ...['01123', '01122', '01121', '01186', '01188'].map((c) => `Puzzle.PutIntoDeck('${c}')`),
  ];
  const reponse = await request.post('/sandbox_command?p=0', { data: { commands: commandes } });
  console.log(`COMMANDES -> ${reponse.status()} ${(await reponse.text()).slice(0, 200)}`);
}

const visible = async (page: Page, nom: RegExp) => {
  const b = page.getByRole('button', { name: nom }).first();
  return (await b.count()) > 0 && (await b.isVisible()) ? b : undefined;
};

/** Un pas : utiliser Stepford Cuckoos si on le propose, sinon passer ou continuer. */
let formeChangee = false;

async function unPas(page: Page): Promise<string | void> {
  // Une seule fois, au premier tour : passer en forme HÉROS, pour que Klaw ATTAQUE.
  if (!formeChangee) {
    const forme = await visible(page, /Changer de forme|Change Form|forme h[ée]ros|Spider-Man$/);
    if (forme && !(await forme.isDisabled({ timeout: 500 }).catch(() => true))) {
      formeChangee = true;
      console.log(`FORME : ${await forme.textContent()}`);
      await forme.click({ timeout: 2000 }).catch(() => {});
      return;
    }
  }
  const defausser = await visible(page, /^(Défausser|Discard) \d/);
  if (defausser && (await defausser.isDisabled({ timeout: 1000 }).catch(() => true))) {
    // Telephone : la carte ouvre sa fiche, « Utiliser cette carte » la coche.
    const utiliser = await visible(page, /^Utiliser cette carte/);
    if (utiliser) {
      await utiliser.click({ timeout: 2000 }).catch(() => {});
      return;
    }
    const main = page.getByRole('dialog', { name: 'Ta main' });
    if ((await page.getByRole('button', { name: /^Main$/ }).count()) > 0 && !(await main.isVisible().catch(() => false))) {
      await page.getByRole('button', { name: /^Main$/ }).first().click({ timeout: 2000 }).catch(() => {});
      return;
    }
    await page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié|Resource|Event|Upgrade|Support|Ally)$/, pressed: false })
      .first().click({ timeout: 2000 }).catch(() => {});
    return;
  }
  const cartouche = page.locator('.deroule-phase.est-scene');
  const n = await cartouche.locator('[data-choix]').count();
  for (let k = 0; k < n; k++) {
    const b = cartouche.locator('[data-choix]').nth(k);
    if (/Stepford/i.test((await b.getAttribute('aria-label')) ?? '') && (await b.isVisible())) {
      await b.click({ timeout: 2000 }).catch(() => {});
      return 'stepford';
    }
  }
  const valider = cartouche.locator('.deroule-sous-cadre .deroule-valider').first();
  if ((await valider.count()) > 0 && (await valider.isVisible())) {
    if (!(await valider.isDisabled({ timeout: 1000 }).catch(() => true))) {
      await valider.click({ timeout: 2000 }).catch(() => {});
      return;
    }
    const carte = cartouche.locator('.deroule-sous-cadre [data-choix][aria-pressed="false"]').first();
    if ((await carte.count()) > 0) {
      await carte.click({ timeout: 2000 }).catch(() => {});
      return;
    }
  }
  const centrale = page.locator('.demande-centrale .af-action', { hasText: /Stepford/i }).first();
  if ((await centrale.count()) > 0 && (await centrale.isVisible())) {
    await centrale.click({ timeout: 2000 }).catch(() => {});
    return 'stepford';
  }
  for (const nom of [
    /^Garder ma main/, /^(Défausser|Discard) \d/, /^Suivant/, /^Ne pas (défendre|utiliser|jouer)/, /^Aucune réponse/,
    /^Continuer sans rien jouer/, /^(Jouer|Play) (Boom Sonique|Sonic Boom)/, /^Passer/, /^Pass/, /^(Continuer|Continue)/, /^(Terminer|Finish)/, /^Keep my hand/, /^Don.t (defend|use|play)/, /^Next/, /^Fin de phase/i, /^End Phase/i, /Fin du tour/,
  ]) {
    const b = await visible(page, nom);
    if (b && !(await b.isDisabled({ timeout: 1000 }).catch(() => true))) {
      await b.click({ timeout: 2000 }).catch(() => {});
      return;
    }
  }
  // Anglais : le premier « End turn » est celui de la barre, souvent grisé ;
  // on prend le premier qui se clique.
  const fins = page.getByRole('button', { name: /End turn/ });
  for (let k = 0; k < (await fins.count()); k++) {
    const b = fins.nth(k);
    if ((await b.isVisible()) && !(await b.isDisabled({ timeout: 500 }).catch(() => true))) {
      await b.click({ timeout: 2000 }).catch(() => {});
      return;
    }
  }
  const force = cartouche.locator('[data-choix]').first();
  if ((await force.count()) > 0 && (await cartouche.locator('[data-refus]').count()) === 0 && (await force.isVisible())) {
    await force.click({ timeout: 2000 }).catch(() => {});
  }
}

async function capturer(page: Page, nom: string) {
  await page.waitForFunction(() => !document.querySelector('.splash-tour, .bandeau-phase'), undefined, { timeout: 4000 }).catch(() => {});
  await page.waitForTimeout(400);
  fs.mkdirSync(SORTIE, { recursive: true });
  await page.screenshot({ path: path.join(SORTIE, `${VARIANTE}-${nom}.png`) });
  const corps = await page.locator('.deroule-phase.est-scene .deroule-corps').first().getAttribute('aria-label', { timeout: 300 }).catch(() => null);
  console.log(`CAPTURE ${VARIANTE}-${nom} : ${corps}`);
  const deborde = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  expect.soft(deborde, 'defilement horizontal').toBe(false);
}

/**
 * Joue jusqu'a la phase du mechant et capture chaque carte de la chaine : la
 * carte a Renfort, la carte annulee, la carte de remplacement.
 */
async function derouler(page: Page, suffixe: string) {
  // Ordinateur : la scene (`.deroule-titre-court`). Telephone : l'ancien rendu (`.deroule-titre`).
  const titre = page.locator('.deroule-phase.est-scene .deroule-titre-court, .deroule-phase .deroule-titre').first();
  const essai = page.locator('.deroule-phase.est-essai');
  let vu = '';
  let rang = 0;
  let fin = 0;
  for (let i = 0; i < 300; i++) {
    const lu = (await titre.count()) > 0 ? ((await titre.textContent()) ?? '') : '';
    const corps = await page.locator('.deroule-phase.est-scene .deroule-corps').first().getAttribute('aria-label', { timeout: 200 }).catch(() => null);
    const chaine = (await page.locator('.deroule-chaine-texte').count()) > 0 ? await page.locator('.deroule-chaine-texte').first().textContent() : '';
    const cle = `${lu}|${corps ?? ''}|${chaine}|${await page.locator('.deroule-chaine-maillon, .deroule-renfort-vide, [data-choix]').count()}`;
    if (lu && cle !== vu && rang < 14) {
      vu = cle;
      rang += 1;
      await capturer(page, `${suffixe}-${String(rang).padStart(2, '0')}`);
    }
    if (i % 30 === 0) {
      const boutons = await page.locator('button:visible').evaluateAll((bs) => bs.map((b) => (b.getAttribute('aria-label') || b.textContent || '').trim().slice(0, 30)).filter(Boolean).slice(0, 18));
      console.log(`PAS ${i} titre=${lu} boutons=${JSON.stringify(boutons)}`);
    }
    if (/Révélée par|Revealed by|Sonic|Boom/i.test(lu)) fin += 1;
    // Le téléphone garde le rendu d'avant (l'essai ne touche que la scène du PC).
    if (i === 40 && (page.viewportSize()?.width ?? 0) >= 768)
      expect.soft(await essai.count(), 'le cartouche porte la classe de l’essai').toBeGreaterThan(0);
    if (fin > 12) break;
    await page.waitForTimeout(300);
    if ((await unPas(page)) === 'stepford') {
      await page.waitForTimeout(1200);
      await capturer(page, `${suffixe}-apres-stepford`);
    }
  }
  const monde = await (await page.request.get('/get_world?hot_seat&p=0')).json();
  const revelations = (monde.faits_mechant ?? []).filter((f: { genre?: string }) => f.genre === 'revelation');
  console.log(`FAITS : ${JSON.stringify(revelations.map((f: Record<string, unknown>) => [f.carte, f.par_surge, f.annulee_par, f.annulee_par_sort, f.revelee_par]))}`);
  return rang;
}

test.setTimeout(900_000);

test('essai : la phase du méchant, ordinateur 1920', async ({ page }) => {
  formeChangee = false;
  await partie(page, 1920, 1080);
  console.log(`CAPTURES : ${await derouler(page, 'pc')}`);
});

test('essai : la phase du méchant, téléphone 360 px', async ({ page }) => {
  formeChangee = false;
  await partie(page, 360, 780);
  console.log(`CAPTURES : ${await derouler(page, 'tel360')}`);
});
