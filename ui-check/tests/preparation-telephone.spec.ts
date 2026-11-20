// La preparation d'une partie, sur un telephone.
//
// Le plateau ne se joue plus qu'en portrait depuis le 11/09/2026 ; les ecrans
// qui viennent AVANT la partie doivent tenir dans le meme format, sinon on
// tourne son telephone pour preparer puis on le redresse pour jouer.
//
// Ce fichier mesure a 480x1050 (Samsung S24 Ultra en portrait) ce qu'aucun
// autre ne regarde : non pas « la page repond », mais « ce qui est dessine
// tient dans le cadre et se lit ».
//
//   npm run preparation-telephone
import { test, expect, type Page } from '@playwright/test';

test.use({ viewport: { width: 480, height: 1050 }, hasTouch: true, isMobile: true });

/** Choisit Spider-Man et avance jusqu'a l'ecran demande. */
async function jusquA(page: Page, etape: 'heros' | 'decks' | 'mechant') {
  await page.goto('/prepare.html');
  // Accueil au téléphone (zone 2, 09/10/2026) : Jouer ouvre la feuille des modes.
  await page.locator('.acc-tel-jouer').click({ timeout: 20000 });
  await page.locator('.acc-tel-feuille').getByRole('button', { name: /^Solo/ }).click();
  await page.waitForSelector('#hero-grid .tb-port', { timeout: 20000 });
  if (etape === 'heros') return;
  // ⚠ Sur telephone (refonte du 09/10/2026) le toucher PRESENTE le heros dans
  // le bandeau ; c'est « Choisir » qui recrute, et l'equipe complete file
  // d'elle-meme aux Decks (plus de modale d'options).
  await page.locator('#hero-grid .tb-port').filter({ hasText: /^Spider-Man/ }).first().click();
  await page.locator('.ts-btn.jaune').click();
  await page.waitForSelector('#deck-liste .tb-deck', { timeout: 20000 });
  const suivant = async () => {
    await page.getByRole('button', { name: /continuer/i }).click();
    await page.waitForTimeout(900);
  };
  if (etape === 'decks') return;
  await suivant();
  await page.waitForSelector('#scn-grid .tb-port', { timeout: 20000 });
}

// ⚠ LE DEFAUT CORRIGE LE 13/09/2026. Sous le nom d'un heros on lisait ses
// traits imprimes (« GARDIEN, MYSTIQUE. ») et le debut de ses regles
// (« defaussez 1 carte ») : trois textes empiles dans 40 px. Ce n'etait pas le
// bandeau du nom, c'etait le CADRAGE, qui montrait la carte jusqu'a 71 % de sa
// hauteur alors que sa zone de texte commence vers 58 %.
test('les vignettes cadrent l illustration, pas la zone de texte', async ({ page }) => {
  await jusquA(page, 'heros');
  const cadre = await page.evaluate(() => {
    const p = document.querySelector('#hero-grid .portrait') as HTMLElement;
    const cs = getComputedStyle(p);
    const tuile = (document.querySelector('#hero-grid .tb-port') as HTMLElement).getBoundingClientRect();
    const zoom = parseFloat(cs.backgroundSize);       // en %
    const decalage = parseFloat(cs.backgroundPosition.split(' ')[1]); // en %
    // La carte affichee fait `tuile.width * zoom / 0.7` de haut (ratio 615/880).
    const hauteurCarte = (tuile.width * zoom / 100) / 0.7;
    const debut = ((hauteurCarte - tuile.height) * decalage / 100) / hauteurCarte * 100;
    const fin = debut + (tuile.height / hauteurCarte) * 100;
    return { debut: Math.round(debut), fin: Math.round(fin), largeurAffichee: Math.round(tuile.width * zoom / 100) };
  });
  console.log('CADRAGE ' + JSON.stringify(cadre));
  // On commence SOUS le bandeau de titre imprime (0-10 %)...
  expect(cadre.debut).toBeGreaterThanOrEqual(10);
  // ...et on s'arrete AVANT la zone de texte (58 %).
  expect(cadre.fin).toBeLessThanOrEqual(58);
  // Et on zoome sans jamais agrandir : le scan fait 615 px de large.
  expect(cadre.largeurAffichee).toBeLessThanOrEqual(615);
});

// ⚠ TROIS COLONNES, ET NON DEUX. A 145 px, trois vignettes plus leurs deux
// ecarts de 8 faisaient 451 px pour 448 disponibles : il en manquait TROIS, et
// la grille retombait a deux colonnes. Les 69 heros faisaient alors 35 rangees,
// soit 7853 px a faire defiler pour en voir le bout.
test('la grille des heros tient sur trois colonnes', async ({ page }) => {
  await jusquA(page, 'heros');
  const g = await page.evaluate(() => {
    const grille = document.querySelector('#hero-grid') as HTMLElement;
    const tuile = document.querySelector('#hero-grid .tb-port') as HTMLElement;
    return { colonnes: getComputedStyle(grille).gridTemplateColumns.split(' ').length,
             tuile: Math.round(tuile.getBoundingClientRect().width),
             hauteur: document.documentElement.scrollHeight };
  });
  console.log('GRILLE ' + JSON.stringify(g));
  expect(g.colonnes).toBe(3);
  // La vignette reste assez large pour que le nom se lise (« Black Panther
  // (Shuri) » est le plus long du roster).
  expect(g.tuile).toBeGreaterThanOrEqual(135);
  // Et la page a bien maigri : 7853 px avant, un tiers de moins attendu.
  expect(g.hauteur).toBeLessThan(6000);
});

// ⚠ L'AUTRE DEFAUT DU 13/09/2026 : le bloc de la menace, borne a 190 px, coupait une puce. Depuis le 30/10/2026 le
// niveau a sa page (onglet « Niveau » sur telephone, sans hauteur bornee) : on verifie que rien n'y deborde.
test('l etape Difficulte ne coupe aucun bouton de niveau', async ({ page }) => {
  await jusquA(page, 'mechant');
  await page.locator('#scn-grid .tb-port').first().click();
  await page.locator('.ts-btn.jaune').click();
  await page.waitForTimeout(900);
  await page.getByRole('button', { name: /continuer/i }).click();
  await page.locator('.dp-onglets .tampon').nth(1).click();
  const g = await page.evaluate(() => {
    const bloc = document.querySelector('#tb-niveau') as HTMLElement;
    const largeur = document.documentElement.clientWidth;
    const boutons = [...bloc.querySelectorAll('button')] as HTMLElement[];
    const debordent = boutons.filter((e) => e.getBoundingClientRect().right > largeur + 1);
    return { combien: boutons.length, debordent: debordent.map((e) => e.textContent?.trim().slice(0, 18)) };
  });
  expect(g.combien).toBeGreaterThan(3);
  expect(g.debordent, `boutons coupes : ${g.debordent.join(', ')}`).toEqual([]);
});

// ⚠ LE TROISIEME DEFAUT DU 13/09/2026. Sous 900 px, `.face-a-face` passe en
// hauteur AUTOMATIQUE : l'ecran final ne faisait plus que 520 px sur les 1050
// du telephone, et les 450 px restants etaient noirs, ce qui donnait une page
// inachevee. Et la carte etait bornee a 146 px par un chiffre pose en dur.
test('l ecran final remplit l ecran, et ses cartes sont lisibles', async ({ page }) => {
  await jusquA(page, 'mechant');
  await page.locator('#scn-grid .tb-port').first().click();
  await page.locator('.ts-btn.jaune').click();
  await page.waitForTimeout(800);
  await page.getByRole('button', { name: /continuer/i }).click();
  await page.getByRole('button', { name: /continuer/i }).click(); // Mechant -> Difficulte -> Final (30/10/2026)
  await page.waitForSelector('.faceoff', { timeout: 20000 });
  const g = await page.evaluate(() => {
    const f = document.querySelector('.faceoff') as HTMLElement;
    const c = document.querySelector('.fo-card') as HTMLElement;
    const nav = document.querySelector('.nav') as HTMLElement;
    return { faceoff: Math.round(f.getBoundingClientRect().height),
             basFaceoff: Math.round(f.getBoundingClientRect().bottom),
             hautNav: Math.round(nav.getBoundingClientRect().top),
             carte: Math.round(c.getBoundingClientRect().width),
             vue: window.innerHeight };
  });
  console.log('FINAL ' + JSON.stringify(g));
  // Le face-a-face occupe au moins les trois quarts de la hauteur utile : plus
  // de bande noire sous le contenu.
  expect(g.faceoff).toBeGreaterThan(g.vue * 0.75);
  // Et il s'arrete avant la barre du bas, qu'il ne doit jamais recouvrir.
  expect(g.basFaceoff).toBeLessThanOrEqual(g.hautNav + 60);
  // La carte se lit : 146 px etait le chiffre pose en dur qu'on a releve.
  expect(g.carte).toBeGreaterThan(160);
});

// Rien ne doit sortir du cadre par les cotes : sur un telephone, un debordement
// horizontal se paie par un defilement lateral parasite sur toute la page.
test('aucun ecran ne deborde sur les cotes', async ({ page }) => {
  for (const etape of ['heros', 'decks', 'mechant'] as const) {
    await jusquA(page, etape);
    const d = await page.evaluate(() => ({
      doc: document.documentElement.scrollWidth, fenetre: window.innerWidth,
    }));
    expect(d.doc, `debordement a l etape ${etape}`).toBeLessThanOrEqual(d.fenetre);
  }
});
