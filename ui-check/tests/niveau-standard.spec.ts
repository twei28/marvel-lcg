// Standard I, II ou III : le joueur choisit, et le moteur reçoit le bon set.
//
// ⚠ POURQUOI CE FICHIER EXISTE (16/09/2026). Question d'un joueur : « is
// standard III implemented ». Les 7 cartes de Standard III et les 6 de
// Standard II étaient scriptées depuis toujours, et INCHOISISSABLES : l'écran
// n'offrait que « Standard » et « Expert », et `catalog.js` écarte de la liste
// des modulaires tout set commençant par « standard ». Les 6 cartes de
// Standard II n'avaient donc jamais été jouées, aucun scénario ne les
// déclarant.
//
//   npm run niveau-standard
import { test, expect, type Page } from '@playwright/test';

async function mod(page: Page, appel: string) {
  return page.evaluate(async (source) => {
    const m: any = await import('/js/prepare/niveau-standard.js');
    // eslint-disable-next-line no-new-func
    return new Function('m', `return (${source})(m)`)(m);
  }, appel);
}

test.beforeEach(async ({ page }) => {
  await page.goto('/prepare.html');
});

test('le niveau remplace le set standard, et lui seul', async ({ page }) => {
  // rhino_expert declare ["standard", "expert"] : Expert doit SURVIVRE.
  const sets = await mod(page, `(m) => m.appliquerNiveau(['standard', 'expert'], 'standard_iii')`);
  expect(sets).toEqual(['standard_iii', 'expert']);
});

test('les sets du scenario ne bougent pas', async ({ page }) => {
  const sets = await mod(page,
    `(m) => m.appliquerNiveau(['kingpin', 'standard_iii', 'bodyguard'], 'standard')`);
  expect(sets).toEqual(['kingpin', 'standard', 'bodyguard']);
});

// ⚠ LE CAS QUI PROTEGE LES SCENARIOS SANS SET STANDARD. Leur en ajouter un
// changerait leur difficulte sans que personne l'ait demande.
test('un scenario sans set standard n en recoit pas', async ({ page }) => {
  const sets = await mod(page, `(m) => m.appliquerNiveau(['kingpin', 'bodyguard'], 'standard_iii')`);
  expect(sets).toEqual(['kingpin', 'bodyguard']);
});

test('le mode Bataille garde son set de base', async ({ page }) => {
  // `standard_pvp` n'est PAS de la famille : il n'a pas de niveaux.
  const sets = await mod(page, `(m) => m.appliquerNiveau(['standard_pvp', 'thunderbolts'], 'standard_iii')`);
  expect(sets).toEqual(['standard_pvp', 'thunderbolts']);
});

test('pas de doublon si le niveau voulu est deja la', async ({ page }) => {
  const sets = await mod(page, `(m) => m.appliquerNiveau(['standard', 'standard_iii'], 'standard_iii')`);
  expect(sets).toEqual(['standard_iii']);
});

// ⚠ L'ECRAN NE DOIT PAS MENTIR. Web of Deceit joue Standard III : afficher
// « Standard I » sur cette partie serait faux.
test('le niveau presente est celui du scenario', async ({ page }) => {
  expect(await mod(page, `(m) => m.niveauDuScenario({ encounter_sets: ['kingpin', 'standard_iii'] })`))
    .toBe('standard_iii');
  expect(await mod(page, `(m) => m.niveauDuScenario({ encounter_sets: ['standard'] })`))
    .toBe('standard');
  expect(await mod(page, `(m) => m.niveauDuScenario({ encounter_sets: ['kingpin'] })`))
    .toBe('standard');
  expect(await mod(page, `(m) => m.niveauDuScenario(null)`)).toBe('standard');
});

test('une valeur inconnue retombe sur Standard I', async ({ page }) => {
  const sets = await mod(page, `(m) => m.appliquerNiveau(['standard'], 'standard_xii')`);
  expect(sets).toEqual(['standard']);
});

test('les trois niveaux sont proposes, dans l ordre', async ({ page }) => {
  const niveaux = await mod(page, `(m) => m.NIVEAUX_STANDARD`);
  expect(niveaux).toEqual(['standard', 'standard_ii', 'standard_iii']);
  const libelles = await mod(page, `(m) => m.NIVEAUX_STANDARD.map(m.libelleNiveau)`);
  expect(libelles).toEqual(['Standard I', 'Standard II', 'Standard III']);
});
