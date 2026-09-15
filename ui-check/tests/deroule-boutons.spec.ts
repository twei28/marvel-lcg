// Les boutons de decision restent sous les yeux, quoi qu'il y ait au-dessus.
//
// ⚠ LE DEFAUT RAPPORTE PAR L'UTILISATEUR LE 13/09/2026, capture a l'appui :
// « on doit scroll et c'est pas clair du tout ». Le panneau de la phase du
// mechant empile la chronologie, les deux cartes de l'attaque, le titre geant,
// le degat annonce, le bandeau « A toi de jouer », les cartes candidates, PUIS
// les boutons Defendre / Demander / Passer, PUIS le texte des capacites. Trop
// haut pour l'ecran, il defilait EN ENTIER : il fallait chercher les boutons,
// alors que ce sont eux la question posee.
//
// On reconstruit ici la structure exacte du panneau avec la VRAIE feuille de
// style du plateau, on la remplit jusqu'a la faire deborder, et on mesure que
// les boutons restent visibles sans toucher a la molette.
//
// ⚠ LA GARANTIE A CHANGE DE MOYEN LE 15/09/2026, PAS DE FOND. Les boutons
// etaient COLLANTS (`position: sticky`) au bas d'une colonne qui defilait.
// Depuis que la fenetre de defense est un BANDEAU — le boost, la phrase, la
// carte et les boutons cote a cote, decision de l'utilisateur apres sa capture
// « pourquoi ca prend toute la page ? » — il n'y a plus de colonne a faire
// defiler : les boutons sont sur la meme ligne que la phrase, et c'est le
// panneau ENTIER qui ne deborde plus. On mesure donc cela, qui est plus fort :
// aucun defilement, et les boutons dans le panneau ET dans l'ecran.
//
// Ce que la phrase ne peut plus faire : grandir au point d'emporter les boutons
// hors de vue. Le plafond est dans board.css (`.est-question .dc-texte`), et le
// remplissage de 600 px ci-dessous existe pour le prouver.
//
//   npm run deroule-boutons
import { test, expect } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

/** La feuille de style du plateau, lue sur le disque.
 *
 *  ⚠ ON LA LIT, ON NE LA DEVINE PAS. Une premiere version cherchait son nom
 *  dans /app/index.html : il ne l'y nomme pas (le bundle la charge lui-meme),
 *  la feuille n'etait donc jamais injectee, et le cas passait au vert en
 *  mesurant une page sans style. Le nom porte une empreinte qui change a
 *  chaque reconstruction : on prend le seul fichier `board-*.css` du dossier. */
function feuilleDuPlateau(): string {
  const assets = path.join(
    path.dirname(fileURLToPath(import.meta.url)),
    '..', '..', 'Fusion', 'marvel-lcg-src', 'public', 'app', 'assets');
  const nom = fs.readdirSync(assets).find((f) => /^board-.*\.css$/.test(f));
  if (!nom) throw new Error(`Aucun board-*.css dans ${assets} : reconstruis le plateau (bash ui-app/deployer.sh).`);
  return fs.readFileSync(path.join(assets, nom), 'utf8');
}

/** Le panneau, tel que DeroulePhase et DemandeCentrale le composent. */
const PANNEAU = `
<section class="deroule-phase est-question" role="dialog">
  <p class="deroule-a-toi">À toi de jouer</p>
  <div class="deroule-question-scene">
    <div class="demande-centrale est-en-scene">
      <div class="dc-texte">
        <span class="plateau-eyebrow">Défense</span>
        <strong>Spider-Man est attaqué par Klaw</strong>
        <span class="dc-reagit">Spider-Man peut réagir</span>
        <div style="height:600px">remplissage : les cartes de l'attaque et les candidates</div>
      </div>
      <div class="af-boutons dc-boutons">
        <span class="af-action-wrap"><button type="button" class="af-action">DÉFENDRE</button></span>
        <span class="af-action-wrap"><button type="button" class="af-action">DEMANDER</button></span>
        <span class="af-action-wrap"><button type="button" class="af-action dc-pass">PASSER</button></span>
      </div>
      <div class="dc-capacites">
        <p class="dc-capacite">Défendre — Rayon Venimeux — Spécial : infligez 2 dégâts à un ennemi.</p>
        <p class="dc-capacite">Demander — Rayon Venimeux — Spécial : infligez 2 dégâts à un ennemi.</p>
      </div>
    </div>
  </div>
</section>`;

async function poser(page: import('@playwright/test').Page) {
  await page.goto('/app/index.html');
  await page.evaluate(({ html, css }) => {
    const st = document.createElement('style');
    st.textContent = css;
    document.head.appendChild(st);
    document.body.style.margin = '0';
    document.body.insertAdjacentHTML('beforeend', html);
  }, { html: PANNEAU, css: feuilleDuPlateau() });
  await page.waitForTimeout(300);
}

test('les boutons restent visibles sans defiler', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await poser(page);
  const mesure = await page.evaluate(() => {
    const panneau = document.querySelector('.deroule-phase') as HTMLElement;
    const boutons = document.querySelector('.dc-boutons') as HTMLElement;
    const p = panneau.getBoundingClientRect();
    const b = boutons.getBoundingClientRect();
    return {
      deborde: panneau.scrollHeight > panneau.clientHeight,
      defilement: panneau.scrollTop,
      boutonsDansLePanneau: b.top >= p.top - 1 && b.bottom <= p.bottom + 1,
      collePresDuBas: p.bottom - b.bottom,
      boutonsDansLEcran: b.top >= 0 && b.bottom <= window.innerHeight,
      sticky: getComputedStyle(boutons).position,
    };
  });
  console.log('BOUTONS ' + JSON.stringify(mesure));
  // ⚠ LE PANNEAU NE DEBORDE PAS, meme sous 600 px de remplissage : c'est la
  // phrase qui est plafonnee, pas les boutons qui se raccrochent.
  expect(mesure.deborde, 'le panneau deborde : il faudra defiler pour tout voir').toBe(false);
  expect(mesure.defilement).toBe(0);
  // ⚠ LE CAS QUI COMPTE : sans defiler, les boutons sont DANS le panneau...
  expect(mesure.boutonsDansLePanneau).toBe(true);
  // ... et dans l'ecran, ce qui est la vraie question posee a l'utilisateur.
  expect(mesure.boutonsDansLEcran, 'les boutons sortent de l’ecran').toBe(true);
  await page.screenshot({ path: 'C:/tmp/deroule-boutons.png' });
});

test('ils restent visibles aussi sur un ecran bas', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 620 });
  await poser(page);
  const ok = await page.evaluate(() => {
    const p = (document.querySelector('.deroule-phase') as HTMLElement).getBoundingClientRect();
    const b = (document.querySelector('.dc-boutons') as HTMLElement).getBoundingClientRect();
    return b.top >= p.top - 1 && b.bottom <= p.bottom + 1 && b.bottom <= window.innerHeight;
  });
  expect(ok).toBe(true);
});
