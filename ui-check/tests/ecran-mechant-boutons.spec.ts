// Écran du méchant, sur ordinateur (10/10/2026) : « Livret de règles » et
// « Carnet de campagne » en rangée sous les pastilles de stats, sans rien
// chevaucher ; les vignettes des méchants s'agrandissent pour remplir la place.
//   UI_CHECK_BASE=http://127.0.0.1:2319 WSLENV=UI_CHECK_BASE npx playwright test tests/ecran-mechant-boutons.spec.ts --project=pc
import { test, expect, type Page } from '@playwright/test';

const ECRANS = [
  { nom: '1920', width: 1920, height: 1080 },
  { nom: '1366', width: 1366, height: 768 },
  { nom: '1030', width: 1030, height: 830 },
];

async function etapeMechant(page: Page, langue: 'fr' | 'en', affichage: 'normal' | 'sobre') {
  await page.addInitScript(([l, a]) => {
    localStorage.setItem('marvel-langue', l);
    localStorage.setItem('marvel-langue-choisie', '1');
    localStorage.setItem('mc_affichage_v1', a);
  }, [langue, affichage]);
  await page.goto('/prepare.html');
  await page.getByRole('button', { name: /^Solo/ }).first().click({ timeout: 30_000 });
  await expect(page.locator('#hero-grid .tb-port').first()).toBeVisible({ timeout: 30_000 });
  await page.locator('#hero-grid .tb-port').first().click();
  const valider = page.getByRole('button', { name: /^(Valider|Confirm)$/ });
  if (await valider.isVisible({ timeout: 2_000 }).catch(() => false)) await valider.click();
  await page.getByRole('button', { name: /^(Continuer|Continue)$/ }).click();
  await page.waitForTimeout(800);
  await page.getByRole('button', { name: /^(Continuer|Continue)$/ }).click();
  await expect(page.locator('#scn-grid .tb-port').first()).toBeVisible({ timeout: 30_000 });
}

async function choisirBoite(page: Page, cle: string) {
  await page.locator(`#ext-tabs .ext-tab[title="${cle}"]`).click();
  await expect(page.locator('#scn-grid .tb-port').first()).toBeVisible({ timeout: 30_000 });
  await page.waitForTimeout(600);
}

/** Les rectangles visibles du pied de scène et des pastilles ne se touchent pas. */
async function chevauchements(page: Page) {
  return page.evaluate(() => {
    const scene = document.querySelector<HTMLElement>('#tb-scene')!;
    const boites = [
      ...scene.querySelectorAll<HTMLElement>('.tb-tampons > *'),
      ...scene.querySelectorAll<HTMLElement>('.tb-bas > a, .tb-bas > button, .tb-bas > details > summary'),
    ].filter((e) => e.offsetParent !== null);
    const r = boites.map((e) => ({ nom: e.textContent!.trim().slice(0, 30), b: e.getBoundingClientRect() }));
    const s = scene.getBoundingClientRect();
    const fautes: string[] = [];
    for (let i = 0; i < r.length; i++) {
      if (r[i].b.bottom > s.bottom + 1 || r[i].b.left < s.left - 1) fautes.push(`${r[i].nom} sort de la scène`);
      for (let j = i + 1; j < r.length; j++) {
        const a = r[i].b, b = r[j].b;
        if (a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1) {
          fautes.push(`${r[i].nom} / ${r[j].nom}`);
        }
      }
    }
    return { fautes, docs: scene.querySelectorAll('.tb-bas .target-doc').length };
  });
}

for (const ecran of ECRANS) {
  for (const langue of ['fr', 'en'] as const) {
    for (const affichage of ['normal', 'sobre'] as const) {
      test(`${ecran.nom} ${langue} ${affichage} : boutons alignés, vignettes agrandies`, async ({ page }) => {
        test.setTimeout(120_000);
        await page.setViewportSize({ width: ecran.width, height: ecran.height });
        await etapeMechant(page, langue, affichage);
        const suffixe = `${ecran.nom}-${langue}-${affichage}`;

        // Set de base : 3 méchants, les vignettes grandissent sans défiler.
        await choisirBoite(page, "1. Core Set");
        await page.locator('#scn-grid .tb-port').nth(1).click();
        // La carte qui surgit au choix dure 2,8 s : on mesure après elle.
        await page.waitForTimeout(3_000);
        const grille = await page.evaluate(() => {
          const g = document.querySelector<HTMLElement>('#scn-grid')!;
          const t = [...g.querySelectorAll<HTMLElement>('.tb-port')].map((e) => e.getBoundingClientRect());
          return {
            largeur: Math.round(t[0].width),
            hauteur: Math.round(t[0].height),
            defile: g.scrollHeight > g.clientHeight + 1,
            menaceVisible: !!document.querySelector('#tb-menace')?.getBoundingClientRect().height,
          };
        });
        console.log(suffixe, 'core', JSON.stringify(grille));
        // Sous 1100 px la page passe en une colonne : la grille prend la hauteur
        // de son contenu, il n'y a pas de vide à remplir.
        if (ecran.width >= 1100) expect.soft(grille.largeur).toBeGreaterThan(148 * 1.2);
        expect.soft(grille.largeur).toBeLessThanOrEqual(2 * 148 + 2);
        expect.soft(grille.defile).toBe(false);
        expect.soft(grille.menaceVisible).toBe(true);
        // L'en-tête dit le méchant choisi, plus « Méchant inconnu ».
        await expect.soft(page.locator('.tb-mode').first()).toContainText('Klaw');
        const klaw = await chevauchements(page);
        expect.soft(klaw.fautes, 'Klaw').toEqual([]);

        // Convoitise Galactique : livret ET carnet de campagne.
        await choisirBoite(page, "16. Galaxy's Most Wanted");
        await page.locator('#scn-grid .tb-port').nth(1).click();
        await page.waitForTimeout(3_000);
        await expect.soft(page.locator('#tb-scene .target-doc')).toHaveCount(2, { timeout: 15_000 });
        const musee = await chevauchements(page);
        expect.soft(musee.fautes, 'Infiltrate the Museum').toEqual([]);
        expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
        const n = await page.locator('#scn-grid .tb-port').count();
        console.log(suffixe, 'gmw', n, 'méchants');
      });
    }
  }
}
