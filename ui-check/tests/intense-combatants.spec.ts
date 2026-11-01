// te201 Intense Combatants : l'environnement OPTIONNEL des scénarios TMNT (16/10/2026).
//
// Décision de l'utilisateur : une case à la préparation, DÉCOCHÉE par défaut,
// proposée seulement quand le scénario joue TMNT Standard ou TMNT Expert.
// Cochée, le lanceur ajoute `tmnt_intense_combatants` à `rules` (le canal de
// Skirmish et d'Héroïque) ; le moteur met te201 en jeu au Setup.
//
//   npx playwright test tests/intense-combatants.spec.ts --project=pc
//
// Laisse une capture dans ui-check/intense-combatants.png pour l'œil humain.
import { test, expect, type Page } from '@playwright/test';

async function etapeMechant(page: Page) {
  await page.addInitScript(() => {
    localStorage.setItem('marvel-langue', 'fr');
    localStorage.setItem('marvel-langue-choisie', '1');
  });
  await page.goto('/prepare.html');
  await page.getByRole('button', { name: /^Solo/ }).first().click({ timeout: 30_000 });
  await expect(page.locator('#hero-grid .tb-port').first()).toBeVisible({ timeout: 30_000 });
  await page.locator('#hero-grid .tb-port[data-hero="spider_man"]').first().click();
  const valider = page.getByRole('button', { name: /^(Valider|Confirm)$/ });
  if (await valider.isVisible({ timeout: 2_000 }).catch(() => false)) await valider.click();
  await page.getByRole('button', { name: /^(Continuer|Continue)$/ }).click();
  await page.waitForTimeout(800);
  await page.getByRole('button', { name: /^(Continuer|Continue)$/ }).click();
  await expect(page.locator('#scn-grid .tb-port').first()).toBeVisible({ timeout: 30_000 });
}

async function choisirMechant(page: Page, boite: string, scn: string) {
  // Depuis le 19/10/2026 la liste n'a que les boîtes officielles OU que les fan-made : le filtre « Fan-made » bascule.
  // Le filtre est devenu l'onglet de groupe « FAN-MADE » (#ext-groupes).
  if (/custom/i.test(boite)) await page.locator('#ext-groupes').getByText(/fan-made/i).click();
  await page.waitForTimeout(500);
  // Les pochettes n'ont plus d'attribut `title` : on les trouve a leur nom (« Set de base » en francais).
  const etiquette = boite.replace(/^\d+\.\s*/, '');
  const motif = etiquette === 'Core Set' ? /Set de base|Core Set/ : new RegExp(etiquette.replace(/^Custom \((.*)\)$/, '$1'), 'i');
  await page.locator('#ext-tabs .ext-tab').filter({ hasText: motif }).first().click();
  await page.locator(`#scn-grid .tb-port[data-scn="${scn}"]`).click();
  await page.mouse.move(5, 5);
  await page.waitForTimeout(3_000); // la carte qui surgit au choix dure 2,8 s
}

const CASE = '#tb-niveau .intense-combatants input[type="checkbox"]';

test('la case apparait pour Shredder (TMNT Standard), decochee, avec le texte FR de te201', async ({ page }) => {
  test.setTimeout(120_000);
  await page.setViewportSize({ width: 1920, height: 1080 });
  await etapeMechant(page);
  await choisirMechant(page, '190. Custom (Shredder)', 'shredder');
  await page.getByRole('button', { name: /continuer/i }).click(); // l'etape Difficulte porte la case (30/10/2026)

  const ligne = page.locator('#tb-niveau .intense-combatants');
  await expect(ligne).toBeVisible();
  await expect(ligne).toContainText('Intense Combatants (environnement optionnel)');
  await expect(ligne).toContainText('Interruption forcée');
  await expect(ligne).toHaveAttribute('title', /Sets TMNT Standard et Expert uniquement/);
  await expect(page.locator(CASE)).not.toBeChecked();
  await ligne.scrollIntoViewIfNeeded();
  await page.screenshot({ path: 'intense-combatants.png' });
  await expect(page.locator(CASE)).toHaveCount(1);
});

test('la case n apparait pas pour Rhino', async ({ page }) => {
  test.setTimeout(120_000);
  await page.setViewportSize({ width: 1920, height: 1080 });
  await etapeMechant(page);
  await choisirMechant(page, '1. Core Set', 'rhino');
  await page.getByRole('button', { name: /continuer/i }).click();
  await expect(page.locator('#tb-niveau .tb-menace-ligne').first()).toBeVisible();
  await expect(page.locator('#tb-niveau .intense-combatants')).toHaveCount(0);
});

test('le descripteur porte la regle seulement case cochee ET scenario TMNT', async ({ page }) => {
  await page.goto('/prepare.html');
  const r = await page.evaluate(async () => {
    const { catalog } = await import('/public/js/prepare/catalog.js');
    const { buildDescriptor } = await import('/public/js/prepare/launcher.js');
    const deck = { name: 'Test', hero: ['01001a'], hero_deck: [], obligations: [], nemesis_set: [], player_deck: [] };
    const trouver = async (id: string) => {
      for (const ext of await catalog.extensions()) {
        let liste: any[] = [];
        try { liste = await catalog.scenariosForExtension(ext.key); } catch (e) { continue; }
        const sc = liste.find((s) => s.id === id);
        if (sc) return sc;
      }
      return null;
    };
    const etat = (scenario: any, coche: boolean) => ({
      mode: { id: 'hotseat' }, scenario, playerCount: 1, premierJoueur: 0, players: [{ deck }],
      difficulty: { base: 'standard', standard: 'standard', skirmish: false, heroic: 0,
                    selectedModularSets: [], intenseCombatants: coche },
      seed: 1, timeoutSecondes: 0, reglesV16: true, campaignLog: {},
    });
    const shredder = await trouver('shredder');
    const rhino = await trouver('rhino');
    const R = 'tmnt_intense_combatants';
    return {
      shredderCoche: (await buildDescriptor(etat(shredder, true))).rules.includes(R),
      shredderDecoche: (await buildDescriptor(etat(shredder, false))).rules.includes(R),
      rhinoCoche: (await buildDescriptor(etat(rhino, true))).rules.includes(R),
    };
  });
  expect(r).toEqual({ shredderCoche: true, shredderDecoche: false, rhinoCoche: false });
});

test('cocher la case envoie la regle au serveur (/new)', async ({ page }) => {
  test.setTimeout(180_000);
  await page.setViewportSize({ width: 1920, height: 1080 });
  let envoye: any = null;
  await page.route(/\/new\?data=/, async (route) => {
    envoye = JSON.parse(decodeURIComponent(route.request().url().split('data=')[1]));
    await route.fulfill({ status: 200, body: '{}' });
  });
  await page.route(/\/app\/board\.html/, (route) => route.fulfill({ status: 200, body: 'plateau' }));
  await etapeMechant(page);
  await choisirMechant(page, '190. Custom (Shredder)', 'shredder');
  await page.getByRole('button', { name: /continuer/i }).click(); // l'etape Difficulte porte la case (30/10/2026)
  await page.locator(CASE).check();
  // Jusqu'au lancement : « Continuer » (decks, puis final), puis « Lancer la partie » (.btn.launch).
  await page.locator('footer.nav .btn.primary').click({ timeout: 10_000 });
  await page.waitForTimeout(1_500);
  await page.locator('footer.nav .btn.launch').click({ force: true, timeout: 10_000 });
  for (let i = 0; i < 20 && envoye === null; i++) await page.waitForTimeout(500);
  expect(envoye, 'aucun appel /new intercepte').not.toBeNull();
  expect(envoye.rules).toContain('tmnt_intense_combatants');
  expect(envoye.encounter_set_names).toContain('tmnt_standard');
});
