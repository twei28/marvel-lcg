// Outil de session (17/10/2026) : capture de tous les écrans hors plateau, en Épuré, pour comparer
// avant / après une retouche de style. Pas un test.
import { test, type Page } from '@playwright/test';
import fs from 'node:fs';

const D = process.env.ZZ_D ?? '/tmp/revue';
test.use({ reducedMotion: 'reduce' });

test('revue', async ({ page }) => {
  test.setTimeout(400_000);
  fs.mkdirSync(D, { recursive: true });
  await page.addInitScript(() => {
    localStorage.setItem('mc_affichage_v1', 'epure');
    sessionStorage.setItem('mc_epure_permis', 'oui');
  });
  await page.route('**/get_choix_sieges*', (r) => r.fulfill({ contentType: 'application/json', body: JSON.stringify({ multi: true, sieges: {} }) }));
  // Les boutons d'outils de l'en-tête arrivent dans un ordre variable : on les masque.
  const masque = () => page.addStyleTag({ content: '.reprise-boutons{visibility:hidden!important}' }).catch(() => {});
  const shot = async (nom: string) => { await masque(); await page.mouse.move(1, 1079); await page.waitForTimeout(900); await page.screenshot({ path: `${D}/${nom}.png` }); };
  const aller = async (u: string) => { try { await page.goto('/' + u, { waitUntil: 'networkidle', timeout: 25000 }); } catch { /* */ } await page.waitForTimeout(3000); };
  const essai = async (f: () => Promise<unknown>) => { try { await f(); } catch (e) { console.log('ECHEC', String(e).slice(0, 120)); } };

  await aller('prepare.html'); await shot('01-accueil');
  await essai(async () => { await page.locator('.acc-tuile[data-cle="options"] .acc-mode').click(); await page.waitForTimeout(1200); await shot('02-options'); });
  await aller('nouveautes.html'); await shot('03-nouveautes');
  await essai(async () => { await page.locator('.nv-rangee').nth(1).click(); await page.waitForTimeout(800); await shot('04-nouveautes-famille'); });
  await aller('prepare.html');
  await essai(async () => { await page.locator('.acc-tuile[data-cle="legacy"] .acc-mode').click(); await page.waitForTimeout(2500); await shot('05-legacy'); });
  await aller('prepare.html');
  await essai(async () => { await page.locator('.acc-tuile[data-cle="hasard"] .acc-nombre').first().click(); await page.waitForTimeout(2500); await shot('06-hasard'); });
  await aller('prepare.html');
  await essai(async () => { await page.locator('.acc-tuile[data-cle="bataille"] .acc-mode').click(); await page.waitForTimeout(2000); await shot('07-bataille'); });
  await aller('prepare.html');
  await page.locator('.acc-tuile[data-cle="solo"] .acc-mode').click(); await page.waitForTimeout(2200); await shot('08-heros');
  await page.locator('.tb-port').nth(12).click(); await page.waitForTimeout(1200); await shot('09-options-heros');
  await page.locator('.vh-actions .tampon.jaune').click(); await page.waitForTimeout(800);
  await page.locator('footer.nav .btn.primary').click(); await page.waitForTimeout(2200); await shot('10-decks');
  await page.locator('footer.nav .btn.primary').click(); await page.waitForTimeout(2200); await shot('11-mechant');
  await essai(async () => { await page.locator('.ext-tab').nth(2).click(); await page.waitForTimeout(1500); await shot('12-mechant-boite'); });
  await page.locator('.tb-roster-scn .tb-port').nth(1).click(); await page.waitForTimeout(1500); await shot('13-mechant-choisi');
  await page.locator('footer.nav .btn.primary').click(); await page.waitForTimeout(2500); await shot('14-final');
  await aller('campagne.html'); await shot('15-campagnes');
  await essai(async () => { await page.getByRole('button', { name: /nouvelle campagne/i }).first().click(); await page.waitForTimeout(1800); await shot('16-campagne-nouvelle'); });
  await aller('deck-builder.html'); await shot('17-editeur');
  await essai(async () => { await page.locator('#db-hero-bloc').click(); await page.waitForTimeout(1500); await shot('18-editeur-heros'); });
  await aller('palettes-heros.html'); await shot('19-palettes');
  await aller('galerie.html'); await shot('20-galerie');
  await aller('salon.html'); await shot('21-salon');
  await aller('rejoindre.html'); await shot('22-rejoindre');
  await aller('achievements.html'); await shot('23-succes');
});
