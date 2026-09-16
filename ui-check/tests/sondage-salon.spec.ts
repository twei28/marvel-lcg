// La CADENCE du sondage du salon, eprouvee sur le vrai module.
//
// ⚠ POURQUOI CE FICHIER EXISTE. Mesure du 16/09/2026 sur les journaux de
// Caddy, 3,2 heures d'observation : `/get_choix_sieges` pesait 5917 requetes,
// soit 61 % de TOUT le trafic vers les tables — une toutes les deux secondes
// par client, en solo comme en multi, onglet cache compris. A cent joueurs,
// cinquante requetes par seconde pour apprendre que rien n'a change.
//
// ⚠ ET CES APPELS EMPECHAIENT LES TABLES DE S'ETEINDRE : le faucheur juge
// l'inactivite sur la date du journal du moteur, que chaque requete fait
// vivre. Un onglet oublie tenait une table allumee jusqu'au minuteur des huit
// heures.
//
//   npm run sondage-salon
import { test, expect, type Page } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('/prepare.html');
});

/** Appelle la fonction PURE du vrai module, dans la page. */
async function cadence(page: Page, etat: { cache: boolean; enAttente: boolean }) {
  return page.evaluate(async (e) => {
    const mod: any = await import('/js/prepare/app.js');
    return mod.cadenceSondage(e);
  }, etat);
}

test('onglet cache : on ne sonde pas du tout', async ({ page }) => {
  expect(await cadence(page, { cache: true, enAttente: false })).toBe(0);
  // ⚠ MEME EN PLEINE ATTENTE. Personne ne regarde : le rattrapage se fait au
  // retour sur l'onglet, pas en continuant a frapper le serveur.
  expect(await cadence(page, { cache: true, enAttente: true })).toBe(0);
});

test('on attend quelqu un : deux secondes, comme avant', async ({ page }) => {
  expect(await cadence(page, { cache: false, enAttente: true })).toBe(2000);
});

// ⚠ LE CAS QUI FAIT TOUT LE GAIN. En solo, ou une fois le salon complet, il
// n'y a plus rien a guetter : c'est l'ecrasante majorite du temps passe sur
// cet ecran.
test('rien a attendre : on ralentit franchement', async ({ page }) => {
  const calme = await cadence(page, { cache: false, enAttente: false });
  expect(calme).toBe(15000);
  const attente = await cadence(page, { cache: false, enAttente: true });
  expect(calme).toBeGreaterThan(attente * 3);
});
