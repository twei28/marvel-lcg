// « VOIR LA TABLE » ET LA POIGNÉE DU CARTOUCHE DE QUESTION, DANS UN VRAI NAVIGATEUR.
//
// ⚠ POURQUOI CE FICHIER EXISTE. Signalement Yarro du 30/09/2026 : « je peux
// bouger la fenêtre dans le fond mais pas la fenêtre principale ». La poignée
// du 28/09 avait déjà échoué en silence parce que `.assistant-action` est en
// `pointer-events: none` : les tests unitaires appelaient le gestionnaire
// directement et passaient. Ici on interroge `elementFromPoint`, ce qui est
// ce que fait un vrai doigt.
//
// On reconstruit les fenêtres avec la VRAIE feuille de style du plateau
// (celle du dossier déployé, ou PLATEAU_CSS_DIR pour viser `ui-app/dist`).
//
//   npm run voir-la-table
//
// ⚠ IL NE LANCE AUCUNE PARTIE ET NE TOUCHE À AUCUN SERVEUR.
import { test, expect } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

function feuilleDuPlateau(): string {
  const assets =
    process.env.PLATEAU_CSS_DIR ||
    path.join(path.dirname(fileURLToPath(import.meta.url)),
      '..', '..', 'Fusion', 'marvel-lcg-src', 'public', 'app', 'assets');
  const nom = fs.readdirSync(assets).find((f) => /^board-.*\.css$/.test(f));
  if (!nom) throw new Error(`Aucun board-*.css dans ${assets} : reconstruis le plateau.`);
  return fs.readFileSync(path.join(assets, nom), 'utf8');
}

const TABLE = `
<div id="table" style="position:fixed;inset:0;z-index:1;background:#234"></div>
<section class="deroule-phase est-question" role="dialog">
  <p class="deroule-a-toi poignee-glisser">À toi de jouer</p>
  <div class="deroule-question-scene"><button type="button" id="choix">Choisir</button></div>
</section>
<div class="plateau-selecteur" role="group">
  <div class="plateau-selecteur-entete poignee-glisser">Cibles hors table</div>
</div>
<button type="button" class="bh-bouton bh-voir-table">Voir la table</button>`;

async function poser(page: import('@playwright/test').Page) {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto('about:blank');
  await page.evaluate(({ html, css }) => {
    const st = document.createElement('style');
    st.textContent = css;
    document.head.appendChild(st);
    document.body.style.margin = '0';
    document.body.insertAdjacentHTML('beforeend', html);
  }, { html: TABLE, css: feuilleDuPlateau() });
}

/** Ce qu'un vrai pointeur toucherait au centre de l'élément visé. */
const toucheAuCentre = (page: import('@playwright/test').Page, selecteur: string) =>
  page.evaluate((sel) => {
    const r = (document.querySelector(sel) as HTMLElement).getBoundingClientRect();
    const touche = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) as HTMLElement | null;
    return touche
      ? { id: touche.id, classes: touche.className, dansLaFenetre: Boolean(touche.closest('.deroule-phase, .plateau-selecteur')) }
      : null;
  }, selecteur);

test('le bandeau rouge du cartouche de question reçoit le pointeur', async ({ page }) => {
  await poser(page);
  const touche = await toucheAuCentre(page, '.deroule-a-toi');
  expect(touche?.classes, 'le bandeau n est pas ce que le pointeur touche').toContain('deroule-a-toi');
});

test("« Voir la table » rend les fenêtres fantômes et la table cliquable à travers", async ({ page }) => {
  await poser(page);
  await page.evaluate(() => document.body.classList.add('voir-la-table'));

  const opacites = await page.evaluate(() => ({
    cartouche: getComputedStyle(document.querySelector('.deroule-phase')!).opacity,
    selecteur: getComputedStyle(document.querySelector('.plateau-selecteur')!).opacity,
  }));
  expect(opacites.cartouche).toBe('0.15');
  expect(opacites.selecteur).toBe('0.15');

  // Le bandeau, la poignée et le bouton « Choisir » ne captent plus rien.
  for (const sel of ['.deroule-a-toi', '#choix', '.plateau-selecteur-entete']) {
    const touche = await toucheAuCentre(page, sel);
    expect(touche?.id, `${sel} capte encore le pointeur`).toBe('table');
  }

  // Le bouton, lui, reste atteignable pour ramener les fenêtres.
  const bouton = await toucheAuCentre(page, '.bh-voir-table');
  expect(bouton?.classes).toContain('bh-voir-table');
});
