// Le relevé des illustrations : la page qui dit QUI est dessiné sur chaque carte.
//
// Pourquoi elle existe : le moteur lit du texte et des mots-clés, il ne voit
// aucune image. Quatre cartes du set Muse parlent pourtant de « la carte qui
// porte l'image de ton identité ». On relève donc à la main.
//
//   npm run releve-images
//
// ⚠ CE QUE CE TEST PROTÈGE AVANT TOUT : la distinction entre « relevé sans
// personne dessus » et « pas encore regardé ». Les deux donnent une liste vide
// côté affichage ; seul le premier doit être écrit dans le fichier. Les
// confondre ferait passer 5746 cartes non relevées pour 5746 cartes sans
// personne, et Muse ne se déclencherait plus jamais.
//
// Le test ne relève RIEN pour de vrai : il intercepte /save_images_cartes et
// regarde ce que la page voulait écrire. Le fichier de production n'est pas
// touché.
import { test, expect, type Page, type Route } from '@playwright/test';

const IDENTITES = [
  { id: 'spider-man-peter-parker', nom: 'Spider-Man', alias: ['Peter Parker'],
    genre: 'joueur', faces: ['01001a', '01001b'] },
  { id: 'rhino', nom: 'Rhino', alias: [], genre: 'adverse', faces: ['01094', '01095', '01096'] },
  { id: 'ironheart', nom: 'Ironheart', alias: ['Riri Williams'], genre: 'joueur', faces: ['29001a'] },
  // Deux homonymes volontaires : le héros du paquet `core` et un sbire du
  // paquet `cw`. Ils partagent un nom de code, pas un visage.
  { id: 'spider-man-tisseur', nom: 'Spider-Man', alias: ['Ben Reilly'],
    genre: 'joueur', faces: ['27030a'] },
  { id: 'spider-man', nom: 'Spider-Man', alias: [], genre: 'adverse', faces: ['56180'] },
];

const CARTES = {
  core: [
    // ⚠ Les cartes d'identité DOIVENT être là : c'est en retrouvant 01001a dans
    // le paquet `core` que la page sait de quel Spider-Man parle le set.
    { card_id: '01001a', name: '* Spider-Man', subtitle: '', type: 'Hero',
      set_name: 'Spider-Man', traits: [], desc: {} },
    { card_id: '01001b', name: '* Peter Parker', subtitle: '', type: 'AlterEgo',
      set_name: 'Spider-Man', traits: [], desc: {} },
    // Une carte signature de Spider-Man : priorité 0, donc en tête de file.
    { card_id: '01002', name: '* Black Cat', subtitle: '', type: 'Ally',
      set_name: 'Spider-Man', traits: [], desc: { Class: 'Hero' } },
    // Une carte de rencontre de Rhino : priorité 2, donc après.
    { card_id: '01097', name: 'Breakin & Takin', subtitle: '', type: 'Treachery',
      set_name: 'Rhino', traits: [], desc: {} },
    // Une carte d'aspect sans set nommé : aucune suggestion évidente.
    { card_id: '01050', name: 'Enraged', subtitle: '', type: 'Upgrade',
      set_name: 'Aggression', traits: [], desc: { Class: 'Aggression' } },
  ],
  // Un second paquet, pour prouver que le paquet départage les homonymes.
  cw: [
    { card_id: '56180', name: '* Spider-Man', subtitle: '', type: 'Minion',
      set_name: 'Civil War', traits: [], desc: {} },
  ],
};

/** Monte la page avec un catalogue minuscule, et sans jamais écrire. */
async function ouvrir(page: Page, dejaReleve: Record<string, string[]> = {}) {
  const ecritures: Array<{ carte: string; identites: string[] }> = [];

  await page.route('**/get_site_admin', (r: Route) =>
    r.fulfill({ json: { url: 'http://exemple/admin' } }));
  await page.route('**/get_cards_json*', (r: Route) => r.fulfill({ json: CARTES }));
  await page.route('**/get_identites', (r: Route) => r.fulfill({ json: { identites: IDENTITES } }));
  await page.route('**/get_images_cartes', (r: Route) => r.fulfill({ json: { cartes: dejaReleve } }));
  await page.route('**/save_images_cartes', async (r: Route) => {
    ecritures.push(JSON.parse(r.request().postData() || '{}'));
    await r.fulfill({ json: { ok: true } });
  });
  // Les scans ne servent à rien ici et ralentissent tout : un pixel suffit.
  await page.route('**/hd/**', (r: Route) => r.fulfill({
    contentType: 'image/gif',
    body: Buffer.from('R0lGODlhAQABAAAAACw=', 'base64'),
  }));

  await page.goto('/releve-images.html');
  await expect(page.locator('#atelier')).toBeVisible();
  return ecritures;
}

test('les cartes signature passent en premier', async ({ page }) => {
  await ouvrir(page);
  // 01002 est la seule carte de classe « Hero » du jeu de test.
  await expect(page.locator('#legende')).toContainText('Black Cat');
  await expect(page.locator('#position')).toHaveText('1 / 6');
});

test('le set de la carte suggère la bonne personne, en un clic', async ({ page }) => {
  const ecritures = await ouvrir(page);
  const puces = page.locator('#suggestions .r-puce');
  await expect(puces.first()).toContainText('Spider-Man / Peter Parker');

  await puces.first().click();
  await expect(page.locator('.r-retenu')).toContainText('Spider-Man');
  await page.locator('#btn-valider').click();

  await expect.poll(() => ecritures.length).toBe(1);
  expect(ecritures[0]).toEqual({ carte: '01002', identites: ['spider-man-peter-parker'] });
});

test('plusieurs personnes sur une meme illustration', async ({ page }) => {
  const ecritures = await ouvrir(page);
  await page.locator('#recherche').fill('spider');
  await page.locator('#liste .r-ligne').first().click();
  await page.locator('#recherche').fill('rhino');
  await page.locator('#liste .r-ligne').first().click();
  await expect(page.locator('.r-retenu')).toHaveCount(2);

  await page.locator('#btn-valider').click();
  await expect.poll(() => ecritures.length).toBe(1);
  expect(ecritures[0].identites.sort()).toEqual(['rhino', 'spider-man-peter-parker']);
});

test('« Aucune identite » ecrit une liste VIDE, pas rien', async ({ page }) => {
  const ecritures = await ouvrir(page);
  await page.locator('#btn-aucune').click();
  await expect.poll(() => ecritures.length).toBe(1);
  // ⚠ Le cœur du dispositif : la carte est bien écrite, avec zéro personne.
  expect(ecritures[0]).toEqual({ carte: '01002', identites: [] });
});

test('« Je verrai plus tard » n ecrit RIEN et passe a la suivante', async ({ page }) => {
  const ecritures = await ouvrir(page);
  const avant = await page.locator('#legende').textContent();
  await page.locator('#btn-plus-tard').click();
  await expect(page.locator('#legende')).not.toHaveText(avant || '');
  expect(ecritures).toHaveLength(0);
});

test('une carte deja relevee sort de la file', async ({ page }) => {
  await ouvrir(page, { '01002': ['spider-man-peter-parker'] });
  // Il reste 2 des 3 cartes, et la signature déjà faite n'est plus proposée.
  await expect(page.locator('#position')).toHaveText('1 / 5');
  await expect(page.locator('#legende')).not.toContainText('Black Cat');
  await expect(page.locator('#avancement')).toContainText('1 / 6');
});

test('revoir les cartes deja relevees remet les cases cochees', async ({ page }) => {
  await ouvrir(page, { '01002': ['spider-man-peter-parker'] });
  await page.locator('#toggle-tout').check();
  await expect(page.locator('#position')).toHaveText('1 / 6');
  await expect(page.locator('#legende')).toContainText('Black Cat');
  await expect(page.locator('.r-retenu')).toContainText('Spider-Man');
});

test('une carte sans indice ne propose personne au hasard', async ({ page }) => {
  await ouvrir(page, {
    '01002': ['spider-man-peter-parker'], '01097': ['rhino'],
    '01001a': ['spider-man-peter-parker'], '01001b': ['spider-man-peter-parker'],
  });
  await expect(page.locator('#legende')).toContainText('Enraged');
  // « Aggression » n'est le nom de personne : mieux vaut ne rien
  // proposer que de proposer à côté, l'administrateur validerait sans regarder.
  await expect(page.locator('#suggestions .r-puce')).toHaveCount(0);
  await expect(page.locator('#btn-valider')).toBeDisabled();
});

test('un invite est renvoye, meme si le moteur refuse deja', async ({ page }) => {
  await page.route('**/get_site_admin', (r: Route) => r.fulfill({ json: { url: '' } }));
  await page.goto('/releve-images.html');
  await expect(page.locator('#message')).toContainText('réservée à l\'administrateur');
  await expect(page.locator('#atelier')).toBeHidden();
});

test('l annuaire absent le dit, au lieu d afficher une liste vide', async ({ page }) => {
  await page.route('**/get_site_admin', (r: Route) => r.fulfill({ json: { url: 'http://exemple/admin' } }));
  await page.route('**/get_cards_json*', (r: Route) => r.fulfill({ json: CARTES }));
  await page.route('**/get_identites', (r: Route) => r.fulfill({ json: { identites: [] } }));
  await page.route('**/get_images_cartes', (r: Route) => r.fulfill({ json: { cartes: {} } }));
  await page.goto('/releve-images.html');
  await expect(page.locator('#message')).toContainText('annuaire-identites.py');
});

test('entre homonymes, le paquet de la carte tranche', async ({ page }) => {
  // ⚠ Défaut réel du 13/09/2026, trouvé sur le catalogue complet : cinq
  // personnes s'appellent « Spider-Man », et la page proposait le SBIRE de
  // Civil War en tête de toutes les cartes signature de Peter Parker. Le nom
  // seul ne désigne pas quelqu'un ; le paquet, lui, tranche.
  await ouvrir(page);
  await expect(page.locator('#legende')).toContainText('Black Cat');
  const puces = page.locator('#suggestions .r-puce');
  await expect(puces.first()).toContainText('Spider-Man / Peter Parker');
  // Et une fois tranché, les autres porteurs du nom ne polluent pas la rangée.
  await expect(puces.filter({ hasText: 'Spider-Man' })).toHaveCount(1);
});
