// L'onglet « Decks des joueurs » de /admin, sur le site d'ESSAI (base jetable,
// faux comptes alice et bob, decks synthetiques ; voir
// site/serveur_essai_decks_admin.py). Jamais la production.
//   python3 site/serveur_essai_decks_admin.py 8097 &
//   SITE=http://127.0.0.1:8097 npx playwright test -c playwright.site.config.ts
import { test, expect } from '@playwright/test';

const SITE = process.env.SITE || '';
const CAPTURES = process.env.CAPTURES_DIR || 'captures-tmp/admin-decks';

async function connecter(page, pseudo: string) {
  await page.context().route('**/entrer*', (r) => r.abort());
  const rep = await page.request.post(SITE + '/connexion',
    { form: { pseudo, mdp: 'essai-mdp-12345' }, maxRedirects: 0 });
  const jeton = /nc_session=([^;]+)/.exec(rep.headers()['set-cookie'] || '')![1];
  await page.context().addCookies([{ name: 'nc_session', value: jeton, url: SITE }]);
}

test.describe('decks des joueurs, vus par l’administrateur', () => {
  test.skip(!SITE, 'SITE non défini : site d’essai absent');
  test.use({ viewport: { width: 1280, height: 720 } });

  test('un joueur ordinaire n’a ni la page ni les données', async ({ page }) => {
    await connecter(page, 'alice');
    expect((await page.request.get(SITE + '/api/admin/decks-joueurs')).status()).toBe(403);
    expect((await page.request.get(SITE + '/admin')).status()).toBe(403);
  });

  test('liste, confirmation, import et retour clair', async ({ page }) => {
    await connecter(page, 'arnaud');
    await page.goto(SITE + '/admin');
    await page.locator('.onglet[data-onglet="decks"]').click();
    const fiches = page.locator('.dj-compte');
    await expect(fiches).toHaveCount(2);
    await expect(fiches.nth(0)).toContainText('alice');
    await expect(fiches.nth(1)).toContainText('bob');
    await expect(page.locator('.dj-importer')).toHaveCount(3);
    // Le nom HTML d'un deck est affiche tel quel, pas interprete.
    await expect(page.locator('.dj-liste')).toContainText('Agressif <b>test</b>');
    await page.screenshot({ path: CAPTURES + '/1-liste.png' });

    // Refuser la confirmation n'importe rien.
    page.once('dialog', (d) => d.dismiss());
    await page.locator('.dj-importer[data-deck="Protection"]').click();
    await expect(page.locator('.dj-message')).toHaveText('');

    page.once('dialog', (d) => {
      expect(d.message()).toContain('L\'original ne sera pas modifié');
      d.accept();
    });
    await page.locator('.dj-importer[data-deck="Protection"]').click();
    await expect(page.locator('.dj-message')).toContainText('de-bob-Protection');
    await expect(page.locator('.dj-message')).toHaveClass(/dj-ok/);
    await page.screenshot({ path: CAPTURES + '/2-importe.png' });
  });

  test('en anglais, les textes suivent', async ({ page }) => {
    await connecter(page, 'arnaud');
    await page.goto(SITE + '/langue?vers=en');
    await page.goto(SITE + '/admin');
    await page.locator('.onglet[data-onglet="decks"]').click();
    await expect(page.locator('.dj-importer').first()).toHaveText('Import into my account');
    await page.screenshot({ path: CAPTURES + '/3-anglais.png' });
  });
});
