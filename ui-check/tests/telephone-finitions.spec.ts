// FINITIONS DU MODE TÉLÉPHONE (10/10/2026) : la nouvelle phase du méchant en
// feuille basse, le plateau PC lisible au téléphone couché, la languette du
// journal effacée quand la main est ouverte.
//
// ⚠ JAMAIS SUR LE 2345 : chaque cas crée une partie. Le moteur d'essai doit
// porter `essai_phase_mechant: true`.
//   UI_CHECK_BASE=http://127.0.0.1:<port> WSLENV=UI_CHECK_BASE \
//     npx playwright test tests/telephone-finitions.spec.ts --project=pc
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const SORTIE = path.resolve('..', '.planning', 'captures-telephone', 'finitions');
const VARIANTE = 'fr';
test.use({ hasTouch: true, isMobile: true });
test.setTimeout(600_000);

async function capture(page: Page, nom: string) {
  fs.mkdirSync(SORTIE, { recursive: true });
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(SORTIE, `${nom}.png`) });
}

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


test('la phase du méchant en essai : feuille basse de 70 %, Continuer pleine largeur (360 px)', async ({ page }) => {
  formeChangee = false;
  await partie(page, 360, 780);
  const essai = page.locator('.deroule-phase.est-scene.est-essai');
  let vues = 0;
  let vu = '';
  for (let i = 0; i < 300 && vues < 8; i++) {
    if ((await essai.count()) > 0 && (await essai.isVisible())) {
      const cle = (await essai.locator('.deroule-corps').first().getAttribute('aria-label').catch(() => '')) ?? '';
      if (cle !== vu) {
        vu = cle;
        vues += 1;
        const boite = (await essai.boundingBox())!;
        const ecran = page.viewportSize()!;
        expect(Math.round(boite.x), 'la feuille part du bord gauche').toBeLessThanOrEqual(1);
        expect(Math.round(boite.width), 'pleine largeur').toBeGreaterThanOrEqual(ecran.width - 1);
        expect(Math.round(boite.y + boite.height), 'collée au bas').toBeGreaterThanOrEqual(ecran.height - 1);
        expect(boite.height, 'au plus 70 % de la hauteur').toBeLessThanOrEqual(ecran.height * 0.7 + 1);
        expect(await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth), 'débordement').toBe(false);
        const titre = essai.locator('.deroule-titre-court').first();
        if ((await titre.count()) > 0 && (await titre.isVisible())) {
          expect((await titre.boundingBox())!.width, 'le titre garde sa largeur').toBeGreaterThan(120);
        }
        const suivant = essai.locator('.deroule-suivant').first();
        if ((await suivant.count()) > 0 && (await suivant.isVisible())) {
          const b = (await suivant.boundingBox())!;
          expect(b.width, 'Continuer pleine largeur').toBeGreaterThanOrEqual(boite.width - 40);
          expect(b.height, 'Continuer de 44 px au moins').toBeGreaterThanOrEqual(44);
        }
        for (const choix of await essai.locator('.essai-choix').all()) {
          if (!(await choix.isVisible())) continue;
          expect((await choix.boundingBox())!.height, 'choix de défense de 44 px').toBeGreaterThanOrEqual(44);
        }
        await capture(page, `360-phase-${String(vues).padStart(2, '0')}`);
      }
    }
    await page.waitForTimeout(250);
    await unPas(page);
  }
  expect(vues, 'la phase du méchant en essai s’est affichée sur téléphone').toBeGreaterThan(0);
  // Réduire : la feuille ne garde que sa ligne du haut.
  if ((await essai.count()) > 0 && (await essai.isVisible())) {
    await essai.locator('.essai-reduire').tap();
    await page.waitForTimeout(300);
    expect((await essai.boundingBox())!.height).toBeLessThan(page.viewportSize()!.height * 0.3);
    await capture(page, '360-phase-reduite');
  }
});

test('téléphone couché : le plateau PC reste lisible et se fait glisser', async ({ page }) => {
  formeChangee = false;
  await partie(page, 844, 390);
  await expect(page.locator('.plateau-scene')).toBeVisible({ timeout: 60_000 });
  await expect(page.locator('body')).toHaveClass(/plateau-paysage-tel/);
  const carte = page.locator('.plateau-scene .scan-card').first();
  await expect(carte).toBeVisible();
  expect((await carte.boundingBox())!.width, 'une carte de la table mesure au moins 85 px').toBeGreaterThanOrEqual(85);
  const cadre = await page.locator('.plateau-cadre').evaluate((el) => ({ sw: el.scrollWidth, cw: el.clientWidth }));
  expect(cadre.sw, 'la table dépasse et se fait glisser').toBeGreaterThan(cadre.cw);
  expect(await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth), 'la page elle-même ne déborde pas').toBe(false);
  await capture(page, '844x390-paysage');
  // Et l'ordinateur ne bouge pas.
  await page.setViewportSize({ width: 1366, height: 768 });
  await page.waitForTimeout(500);
  await expect(page.locator('body')).not.toHaveClass(/plateau-paysage-tel/);
});

test('la languette du journal s’efface quand la main est ouverte (360 px)', async ({ page }) => {
  formeChangee = false;
  await partie(page, 360, 780);
  await expect(page.locator('.plateau-portrait')).toBeVisible({ timeout: 60_000 });
  // La mise en place ouvre la main d'elle-même (la main de départ).
  const main = page.locator('.main-feuille');
  if (!(await main.isVisible().catch(() => false))) await page.locator('.encoche-main').tap();
  await expect(main).toBeVisible();
  await expect(page.locator('.volet-journal-languette')).toBeHidden();
  await capture(page, '360-main-ouverte');
  await main.locator('.main-feuille-fermer').tap();
  await expect(main).toHaveCount(0);
  await expect(page.locator('.volet-journal-languette')).toBeVisible();
});
