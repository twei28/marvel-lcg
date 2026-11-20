// Cartes jumelles (Katana + Other Katana de Leonardo) : le raccord des deux
// moitiés ne doit laisser AUCUN trait, ni sur la table (panorama) ni dans
// l'aperçu double au survol (20/10/2026).
//
// Cause mesurée : la table est mise à l'échelle par un `transform: scale()`, le
// raccord tombe sur une fraction de pixel d'écran, les deux bords anticrénelés se
// composent au lieu de s'additionner et le fond / l'anneau de camp filtre (voir
// `ui-app/src/components/panorama-jumelles.css`).
//
// Mesure : on photographie, puis on compare la colonne du raccord (et ses deux
// voisines) à des colonnes de contrôle prises plus loin dans la même illustration.
// Une colonne d'illustration varie naturellement (détail fin) ; une ligne de fond
// ou d'anneau, elle, dépasse très largement le bruit de l'illustration.
//
// Moteur d'ESSAI seulement : UI_CHECK_BASE=http://127.0.0.1:<port libre, jamais 2345>.
// Le plateau lit /get_world : on y ajoute les deux katanas en jeu (route simulée),
// la partie réelle est un Leonardo contre Rhino, passée jusqu'aux mulligans.
// SORTIE_CAPTURES=<dossier> garde les captures (PREFIXE_CAPTURES les nomme).
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

const SORTIE = process.env.SORTIE_CAPTURES;
const PREFIXE = process.env.PREFIXE_CAPTURES || 'raccord';
/** Part des rangées du raccord qui peuvent laisser filtrer la couleur de détection. */
const PART_TOLEREE = 0.02;
/** Un pixel est « magenta » quand min(R, B) dépasse G de plus que ceci (aucun pixel du dessin ne l'est). */
const SEUIL_MAGENTA = 50;
/** Tout ce qui n'est pas le scan est passé en magenta : fond de table, fond du cadre, repli, anneau de camp. */
const CSS_DETECTION = `
  html, body, .plateau-cadre, .plateau-scene, .plateau-emplacement, .plateau-cartes, .plateau-groupe,
  .panorama-jumelles, .plateau-unite { background: #ff00ff !important; }
  .scan-card { --lisere: #ff00ff !important; --accent: #ff00ff !important; --fond: #ff00ff !important; --camp-ring: #ff00ff !important; }
`;

async function partie(page: Page) {
  const request = page.request;
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const decks = [JSON.stringify(await (await request.get('/get_hero_json?leonardo')).json())];
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: decks, rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
}

type Cadre = { x: number; y: number; w: number; h: number }

/** Lit les pixels d'une capture PNG dans une page vierge : pour chaque colonne autour du raccord, la part de rangées « magenta ». */
async function colonnesMagenta(page: Page, png: Buffer, zoom: number, seam: Cadre, cadre: Cadre) {
  const lecteur = await page.context().newPage();
  try {
    return await lecteur.evaluate(
      async ({ b64, z, xs, y0, y1, seuil }) => {
        const blob = await (await fetch('data:image/png;base64,' + b64)).blob();
        const img = await createImageBitmap(blob);
        const cv = new OffscreenCanvas(img.width, img.height);
        const cx = cv.getContext('2d')!;
        cx.drawImage(img, 0, 0);
        const px = cx.getImageData(0, 0, img.width, img.height).data;
        const c0 = Math.round(xs * z);
        const out: { colonne: number; part: number }[] = [];
        for (let c = c0 - 4; c <= c0 + 5; c++) {
          let n = 0, mag = 0;
          for (let y = Math.floor(y0 * z); y < Math.floor(y1 * z); y++) {
            const i = (y * img.width + c) * 4;
            n++;
            if (Math.min(px[i], px[i + 2]) - px[i + 1] > seuil) mag++;
          }
          out.push({ colonne: c, part: mag / n });
        }
        return out;
      },
      // De 12 % à 85 % de la hauteur : l'illustration, hors du bandeau du haut et des arrondis.
      { b64: png.toString('base64'), z: zoom, xs: seam.x, y0: cadre.y + cadre.h * 0.12, y1: cadre.y + cadre.h * 0.85, seuil: SEUIL_MAGENTA }
    );
  } finally {
    await lecteur.close();
  }
}

const rect = (page: Page, sel: string) =>
  page.evaluate((s) => {
    const r = (document.querySelector(s) as HTMLElement).getBoundingClientRect();
    return { x: r.x, y: r.y, w: r.width, h: r.height };
  }, sel);

for (const [largeur, hauteur] of [[1280, 720], [1920, 1080]] as const) {
  for (const zoom of [1, 1.25, 1.5]) {
    for (const epuisee of [false, true]) {
      test(`raccord sans trait : ${largeur}x${hauteur}, zoom ${zoom * 100} %, ${epuisee ? 'épuisée' : 'prête'}`, async ({ browser }) => {
        test.setTimeout(150_000);
        // Zoom du navigateur N % = fenêtre divisée par N, pixels d'écran multipliés par N.
        const ctx = await browser.newContext({
          viewport: { width: Math.round(largeur / zoom), height: Math.round(hauteur / zoom) },
          deviceScaleFactor: zoom,
          storageState: './.auth/state.json',
          reducedMotion: 'reduce',
        });
        const page = await ctx.newPage();
        await partie(page);
        await page.route('**/get_world*', async (route) => {
          const rep = await route.fetch();
          const w = await rep.json();
          if (w.players?.length && w.players[0].area_hero.length) {
            const h = w.players[0].area_hero;
            const modele = JSON.parse(JSON.stringify(h[0]));
            for (const [id, code, nom] of [[91, 'tl011', "Leonardo's Katana"], [92, 'tl012', "Leonardo's Other Katana"]] as const) {
              if (!h.some((c: { id: number }) => c.id === id)) {
                h.push({ ...modele, id, card_id: code, pic_id: code, name: nom, card_type: 'Upgrade', bind_object_id: 1, is_ready: !epuisee, down_card_ids: [], info: {}, traits: {}, effects: [], resources: [] });
              }
            }
          }
          await route.fulfill({ response: rep, json: w });
        });
        await page.goto('/app/board.html', { waitUntil: 'networkidle' });
        await expect(page.locator('.scan-card.est-panorama.panorama-gauche')).toBeVisible({ timeout: 40_000 });
        // Passe les cartes de mise en place jusqu'à la table.
        for (let i = 0; i < 12; i++) {
          const b = page.getByRole('button', { name: /Continuer/ }).first();
          if (await b.isVisible().catch(() => false)) await b.click().catch(() => {});
          else if (i > 2) break;
          await page.waitForTimeout(700);
        }
        await page.waitForFunction(() =>
          [...document.querySelectorAll('.scan-card.est-panorama img')].every((i) => (i as HTMLImageElement).complete && (i as HTMLImageElement).naturalWidth > 0)
        );
        await page.waitForTimeout(500);

        const photo = async (nom: string) => {
          const png = await page.screenshot();
          if (SORTIE) {
            fs.mkdirSync(SORTIE, { recursive: true });
            fs.writeFileSync(path.join(SORTIE, `${PREFIXE}-${nom}-${largeur}-${zoom}-${epuisee ? 'epuisee' : 'prete'}.png`), png);
          }
          return png;
        };
        const verifier = async (nom: string, selGauche: string, selDroite: string) => {
          const png = await page.screenshot();
          const g = await rect(page, selGauche);
          const d = await rect(page, selDroite);
          const colonnes = await colonnesMagenta(page, png, zoom, d, g);
          const pire = colonnes.reduce((a, b) => (b.part > a.part ? b : a));
          expect(
            pire.part,
            `${nom} : la colonne ${pire.colonne} laisse filtrer le fond sur ${(pire.part * 100).toFixed(0)} % de sa hauteur`
          ).toBeLessThanOrEqual(PART_TOLEREE);
        };

        const table = {
          g: '.plateau-scene .scan-card.panorama-gauche .scan-frame',
          d: '.plateau-scene .scan-card.panorama-droite .scan-frame',
        };
        await photo('table');

        // Aperçu double au survol : la souris sur la moitié gauche.
        const cible = await rect(page, table.g);
        await page.mouse.move(cible.x + cible.w / 2, cible.y + cible.h / 2);
        await expect(page.locator('.carte-apercu.a-jumelles .scan-card.panorama-droite')).toBeVisible({ timeout: 10_000 });
        await page.waitForFunction(() =>
          [...document.querySelectorAll('.carte-apercu.a-jumelles img')].every((i) => (i as HTMLImageElement).complete && (i as HTMLImageElement).naturalWidth > 0)
        );
        await page.waitForTimeout(500);
        await photo('apercu');

        // Détection : tout sauf le scan devient magenta, aucune colonne du raccord ne doit en laisser voir.
        await page.addStyleTag({ content: CSS_DETECTION });
        await page.waitForTimeout(300);
        await verifier(
          'apercu',
          '.carte-apercu.a-jumelles .scan-card.panorama-gauche .scan-frame',
          '.carte-apercu.a-jumelles .scan-card.panorama-droite .scan-frame'
        );
        await page.mouse.move(5, 5);
        await expect(page.locator('.carte-apercu.a-jumelles')).toHaveCount(0, { timeout: 10_000 });
        await page.waitForTimeout(300);
        await verifier('table', table.g, table.d);
        await ctx.close();
      });
    }
  }
}
