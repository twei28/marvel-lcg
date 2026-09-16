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
async function cadence(page: Page, etat: { cache: boolean; enAttente: boolean; injoignable?: boolean }) {
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

// ⚠ LA TABLE FERMEE, DEFAUT VU EN PRODUCTION LE 16/09/2026. Une table qu'on
// ferme laisse son onglet ouvert : Caddy rend un 502, `sonderSalon` avalait
// l'echec sans un mot, et l'ecran restait la comme si de rien n'etait. Mesure
// dans les journaux : 525 requetes en quinze minutes, toutes en erreur, pour
// un ecran que son proprietaire croyait vivant.

/** Appelle la seconde fonction PURE du module, dans la page. */
async function fermee(page: Page, etat: { premierEchec: number | null; maintenant: number }) {
  return page.evaluate(async (e) => {
    const mod: any = await import('/js/prepare/app.js');
    return mod.tableFermee(e);
  }, etat);
}

test('tout va bien : aucune table declaree fermee', async ({ page }) => {
  expect(await fermee(page, { premierEchec: null, maintenant: 1_000_000 })).toBe(false);
});

// ⚠ LE CAS QUI PROTEGE DU FAUX POSITIF. Un deploiement coupe les tables une
// dizaine de secondes : annoncer « table fermee » a la premiere erreur ferait
// mentir le bandeau a chaque mise a jour du site.
test('une coupure courte ne declare rien', async ({ page }) => {
  const debut = 1_000_000;
  expect(await fermee(page, { premierEchec: debut, maintenant: debut + 5_000 })).toBe(false);
  expect(await fermee(page, { premierEchec: debut, maintenant: debut + 29_000 })).toBe(false);
});

test('trente secondes sans reponse : la table est fermee', async ({ page }) => {
  const debut = 1_000_000;
  expect(await fermee(page, { premierEchec: debut, maintenant: debut + 30_000 })).toBe(true);
  expect(await fermee(page, { premierEchec: debut, maintenant: debut + 600_000 })).toBe(true);
});

// Declaree fermee, on ne martele plus — mais on ne renonce pas : le site peut
// redemarrer, et le bandeau doit alors s'effacer tout seul.
test('table fermee : on ralentit sans couper', async ({ page }) => {
  const lent = await cadence(page, { cache: false, enAttente: true, injoignable: true });
  expect(lent).toBe(30000);
  expect(lent).toBeGreaterThan(await cadence(page, { cache: false, enAttente: true }));
  // L'onglet cache reste prioritaire : personne ne regarde, on ne sonde pas.
  expect(await cadence(page, { cache: true, enAttente: false, injoignable: true })).toBe(0);
});

// ⚠ LES REGLES CI-DESSUS SONT PURES, ET UNE REGLE VERTE NE PROUVE AUCUN
// AFFICHAGE (lecon du 15/09/2026 sur board.tsx). Ce dernier cas monte donc le
// VRAI ecran, lui sert de vrais 502 — la page d'erreur HTML de Caddy, celle
// qui faisait trebucher `res.json()` — et regarde ce que le joueur voit.
test('502 en rafale : le joueur apprend que sa table est fermee', async ({ page }) => {
  await page.clock.install();
  await page.route('**/get_choix_sieges*', (route) =>
    route.fulfill({ status: 502, contentType: 'text/html', body: '<html>502 Bad Gateway</html>' })
  );
  await page.goto('/prepare.html');

  // Avant le delai, RIEN : un deploiement coupe les tables quelques secondes,
  // et un bandeau qui crie a chaque mise a jour ne serait plus jamais cru.
  await page.clock.runFor(20_000);
  await expect(page.locator('.table-fermee')).toHaveCount(0);

  await page.clock.runFor(40_000);
  await expect(page.locator('.table-fermee')).toBeVisible();
  await expect(page.locator('.table-fermee')).toContainText('Cette table a été fermée');
  await expect(page.getByRole('button', { name: "Revenir à l'accueil" })).toBeVisible();
});

// Le site redemarre, la table repond de nouveau : le bandeau doit partir seul.
test('la table revient : le bandeau s efface', async ({ page }) => {
  await page.clock.install();
  let morte = true;
  await page.route('**/get_choix_sieges*', (route) =>
    morte
      ? route.fulfill({ status: 502, contentType: 'text/html', body: '<html>502</html>' })
      : route.fulfill({ status: 200, contentType: 'application/json', body: '{"multi":false}' })
  );
  await page.goto('/prepare.html');
  await page.clock.runFor(60_000);
  await expect(page.locator('.table-fermee')).toBeVisible();

  morte = false;
  // Le battement lent de la table declaree fermee : 30 s.
  await page.clock.runFor(35_000);
  await expect(page.locator('.table-fermee')).toHaveCount(0);
});
