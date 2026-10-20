// Connexion et inscription du site (refonte du 20/10/2026) : en-tete fin, scene
// a gauche (~30 %), formulaire a droite ; au telephone, bandeau + formulaire.
// Site d'ESSAI seulement (faux comptes, base jetable) :
//   python3 site/serveur_essai_decks_admin.py 8097 &
//   SITE=http://127.0.0.1:8097 npx playwright test -c playwright.site.config.ts connexion-site
import { test, expect, type Page } from '@playwright/test';

const SITE = process.env.SITE || '';
const CAPTURES = process.env.CAPTURES_DIR || 'captures-tmp/connexion';

const TAILLES = [
  { nom: 'pc', width: 1280, height: 720, mobile: false },
  { nom: 'mobile', width: 390, height: 844, mobile: true },
];
const LANGUES = [
  { code: 'fr', titre: 'Se connecter', inscription: 'Créer un compte', bouton: 'Entrer' },
  { code: 'en', titre: 'Sign in', inscription: 'Create an account', bouton: 'Enter' },
];

async function sansDebordement(page: Page) {
  return page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
}

test.describe('connexion et inscription du site', () => {
  test.skip(!SITE, 'SITE non défini : site d’essai absent');

  for (const t of TAILLES) {
    for (const l of LANGUES) {
      test(`${t.nom} ${l.code} : connexion puis inscription`, async ({ browser }) => {
        const ctx = await browser.newContext({
          viewport: { width: t.width, height: t.height },
          locale: l.code === 'en' ? 'en-GB' : 'fr-FR',
          reducedMotion: 'reduce',
        });
        await ctx.addCookies([{ name: 'nc_langue', value: l.code, url: SITE }]);
        const page = await ctx.newPage();
        await page.goto(SITE + '/connexion');
        await expect(page.locator('h1')).toHaveText(l.titre);
        await expect(page.getByRole('button', { name: l.bouton })).toBeVisible();
        expect(await sansDebordement(page)).toBe(true);
        // Épuré (20/10/2026) : fond #111318, bouton bleu Captain #3f86e0, titres en Bangers.
        const couleurs = await page.evaluate(() => ({
          fond: getComputedStyle(document.body).backgroundColor,
          bouton: getComputedStyle(document.querySelector('form button[type=submit]')!).backgroundColor,
          titre: getComputedStyle(document.querySelector('h1')!).fontFamily,
        }));
        expect(couleurs.fond).toBe('rgb(17, 19, 24)');
        expect(couleurs.bouton).toBe('rgb(63, 134, 224)');
        expect(couleurs.titre).toContain('Bangers');

        const scene = await page.locator('.scene').boundingBox();
        const carte = await page.locator('.carte').boundingBox();
        if (t.mobile) {
          // Le bandeau est fin, et le formulaire se voit sans défiler.
          expect(scene!.height).toBeLessThan(90);
          expect(scene!.width).toBeGreaterThan(t.width - 2);
          expect(carte!.y).toBeGreaterThanOrEqual(scene!.y + scene!.height);
          const bouton = await page.locator('form button[type=submit]').boundingBox();
          expect(bouton!.y + bouton!.height).toBeLessThanOrEqual(t.height);
          expect(bouton!.height).toBeGreaterThanOrEqual(44);
          // Le sélecteur FR / EN est à droite du bandeau, mêmes boutons que sur PC.
          const sel = await page.locator('a.lang').boundingBox();
          expect(sel!.x + sel!.width).toBeGreaterThan(t.width - 24);
          expect(sel!.y + sel!.height).toBeLessThanOrEqual(scene!.height + 2);
          await expect(page.locator('a.lang span')).toHaveText(['FR', 'EN']);
        } else {
          // Scène ~30 %, formulaire à droite, rien à faire défiler.
          const part = scene!.width / t.width;
          expect(part).toBeGreaterThan(0.25);
          expect(part).toBeLessThan(0.36);
          expect(carte!.x).toBeGreaterThan(scene!.x + scene!.width - 60);
          await expect(page.locator('.entete')).toBeVisible();
          expect(await page.evaluate(() => document.documentElement.scrollHeight <= window.innerHeight + 1)).toBe(true);
        }
        // Le pied : une ligne par phrase, lisible.
        expect(await page.locator('.pied .ligne').count()).toBeGreaterThanOrEqual(3);
        await page.screenshot({ path: `${CAPTURES}/connexion-${t.nom}-${l.code}.png` });

        // Une erreur : le message est traduit et la page reste en place.
        await page.fill('input[name=pseudo]', 'inconnu');
        await page.fill('input[name=mdp]', 'mauvais-mdp-123');
        await page.getByRole('button', { name: l.bouton }).click();
        await expect(page.locator('.erreur')).toBeVisible();
        expect(await sansDebordement(page)).toBe(true);
        await page.screenshot({ path: `${CAPTURES}/erreur-${t.nom}-${l.code}.png` });

        await page.goto(SITE + '/inscription');
        await expect(page.locator('h1')).toHaveText(l.inscription);
        expect(await sansDebordement(page)).toBe(true);
        await page.screenshot({ path: `${CAPTURES}/inscription-${t.nom}-${l.code}.png` });
        await ctx.close();
      });
    }
  }

  test('accents remis en français, anglais complet', async ({ browser }) => {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    await page.goto(SITE + '/connexion');
    const fr = await page.locator('.pied').innerText();
    expect(fr).toContain('Mot de passe oublié');
    expect(fr).toContain('réinitialisation');
    await page.goto(SITE + '/inscription');
    expect(await page.locator('.pied').innerText()).toContain('Déjà un compte');
    await ctx.addCookies([{ name: 'nc_langue', value: 'en', url: SITE }]);
    await page.goto(SITE + '/connexion');
    expect(await page.locator('.pied').innerText()).toContain('Forgotten your password');
    await ctx.close();
  });

  test('accents : aucune forme sans accent sur connexion et inscription', async ({ browser }) => {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    for (const chemin of ['/connexion', '/inscription']) {
      await page.goto(SITE + chemin);
      const texte = await page.locator('body').innerText();
      expect(texte).not.toMatch(/\b(Deja|reinitialisation|Ecris|comptees)\b/);
    }
    await ctx.close();
  });
});
