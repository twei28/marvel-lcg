// « Dans quelle langue veux-tu tes cartes ? », posee une seule fois.
//
// Le jeu part en francais pour tout le monde sans avoir rien demande, et ceux
// qui preferent l'anglais ne savent pas forcement que le bouton FR/EN existe.
//
// ⚠ LA CLE EST NEUVE, ET C'EST TOUT L'INTERET. `marvel-langue` existe deja chez
// tous les joueurs actuels : s'y fier n'aurait jamais pose la question a
// personne. `marvel-langue-choisie` n'existe chez personne, donc chacun se la
// voit poser une fois, sa langue actuelle deja cochee.
//
//   npm run langue
import { test, expect, type Page } from '@playwright/test';

/** Ouvre la page comme un joueur qui n'a jamais repondu.
 *
 *  ⚠ LE SCRIPT NE S'EXECUTE QU'UNE FOIS, et il le faut : `addInitScript`
 *  rejoue a CHAQUE navigation, rechargements compris. Sans ce garde-fou, la
 *  reponse du joueur etait effacee par le rechargement qu'elle declenche, et
 *  deux cas echouaient en accusant le produit. */
async function neuf(page: Page, langue?: 'fr' | 'en') {
  await page.addInitScript((l) => {
    if (sessionStorage.getItem('test-langue-prete') === '1') return;
    sessionStorage.setItem('test-langue-prete', '1');
    localStorage.removeItem('marvel-langue-choisie');
    if (l) localStorage.setItem('marvel-langue', l); else localStorage.removeItem('marvel-langue');
  }, langue ?? null);
  await page.goto('/prepare.html');
}

test('la question est posee a la premiere visite', async ({ page }) => {
  await neuf(page);
  const modale = page.locator('.langue-modal');
  await expect(modale).toBeVisible({ timeout: 20000 });
  await expect(modale).toContainText('Dans quelle langue');
  // ⚠ ELLE DIT QU'ON PEUT CHANGER, et nomme le bouton : une question posee une
  // fois sans porte de sortie inquiete plus qu'elle n'aide.
  await expect(modale).toContainText('FR / EN');
  await expect(modale.getByRole('button', { name: 'Français' })).toBeVisible();
  await expect(modale.getByRole('button', { name: 'English' })).toBeVisible();
  await page.screenshot({ path: 'C:/tmp/langue-modale.png' });
});

// ⚠ LE SEUL ECRAN QUI PARLE LES DEUX LANGUES A LA FOIS (16/09/2026). Partout
// ailleurs `t()` traduit selon la langue choisie ; ici personne n'a choisi, et
// la langue vaut « fr » par defaut. Un anglophone lisait donc la question ET
// ses explications en francais. Signale par l'utilisateur.
test('l ecran de langue parle francais ET anglais', async ({ page }) => {
  await neuf(page);
  const modale = page.locator('.langue-modal');
  await expect(modale).toBeVisible({ timeout: 20000 });
  const texte = (await modale.textContent()) || '';
  console.log('MODALE DE LANGUE :', texte.slice(0, 200));
  // La question, dans les deux langues.
  expect(texte).toContain('Dans quelle langue');
  expect(texte).toContain('Which language');
  // Ce que la langue ne peut pas faire, dans les deux langues.
  expect(texte).toContain('sans scan dans la langue choisie');
  expect(texte).toContain('no scan in the chosen language');
  // Et la porte de sortie, dans les deux langues.
  expect(texte).toContain('FR / EN');
  expect(texte).toContain('You can switch at any time');
});

// ⚠ UN JOUEUR QUI EXISTE DEJA la voit AUSSI, avec sa langue cochee : il n'a
// jamais choisi, il a herite du francais par defaut.
test('un joueur deja en francais la voit, avec le francais coche', async ({ page }) => {
  await neuf(page, 'fr');
  const modale = page.locator('.langue-modal');
  await expect(modale).toBeVisible({ timeout: 20000 });
  await expect(modale.locator('.lg-choix.on')).toHaveText(/Français/);
});

test('repondre la meme langue ne recharge rien et ferme la question', async ({ page }) => {
  await neuf(page, 'fr');
  await page.locator('.langue-modal').getByRole('button', { name: 'Français' }).click();
  await expect(page.locator('.langue-modal')).toHaveCount(0);
  expect(await page.evaluate(() => localStorage.getItem('marvel-langue-choisie'))).toBe('1');
  expect(await page.evaluate(() => localStorage.getItem('marvel-langue'))).toBe('fr');
});

test('choisir l anglais bascule tout, cartes comprises', async ({ page }) => {
  await neuf(page, 'fr');
  await page.locator('.langue-modal').getByRole('button', { name: 'English' }).click();
  await page.waitForSelector('.acc-mode', { timeout: 20000 });
  const etat = await page.evaluate(() => ({
    langue: localStorage.getItem('marvel-langue'),
    // Les scans du PLATEAU suivent : sans cela on jouait une interface
    // anglaise sur des cartes francaises.
    scans: localStorage.getItem('marvel-board-scans-fr'),
    choisie: localStorage.getItem('marvel-langue-choisie'),
  }));
  expect(etat).toEqual({ langue: 'en', scans: 'off', choisie: '1' });
  await expect(page.locator('.acc-titre')).toContainText('How do you want to play?');
});

// ⚠ ELLE NE REVIENT PAS. Une question qui se repose a chaque visite est une
// question qu'on finit par fermer sans lire.
test('elle ne revient plus une fois repondue', async ({ page }) => {
  await neuf(page, 'fr');
  await page.locator('.langue-modal').getByRole('button', { name: 'Français' }).click();
  await expect(page.locator('.langue-modal')).toHaveCount(0);
  await page.reload();
  await page.waitForSelector('.acc-mode', { timeout: 20000 });
  await expect(page.locator('.langue-modal')).toHaveCount(0);
});

// ⚠ ET UN CLIC A COTE NE VAUT PAS REPONSE, a la difference des autres modales
// de cet ecran : la question ne reviendrait jamais.
test('un clic a cote ne la ferme pas', async ({ page }) => {
  await neuf(page);
  await expect(page.locator('.langue-modal')).toBeVisible({ timeout: 20000 });
  await page.mouse.click(5, 5);
  await expect(page.locator('.langue-modal')).toBeVisible();
});
