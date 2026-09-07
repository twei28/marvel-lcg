// Le plateau paysage tient-il a l'ecran, en vraies cartes lisibles, au doigt ?
//
// Sur les 34 etats enregistres, en 1050 x 480 (projet s24-paysage) :
//   1. le plateau ne deborde JAMAIS verticalement ;
//   2. aucune rangee ne rogne ses cartes en silence (voir plus bas) ;
//   3. chaque carte posee mesure au moins 84 px de large (le plancher de
//      lisibilite de la spec) ;
//   4. toute cible tactile mesure au moins 44 px dans les deux axes ;
//   5. aucun ecran portrait n'est affiche ;
//   6. le voile « +N » (cartes hors champ) est bien exerce au moins une fois,
//      quitte a forcer le debordement sur l'etat le plus charge s'il n'est
//      jamais apparu tout seul.
// Et en 480 x 1050 (projet s24), sur trois etats : l'ecran « Tourne ton
// telephone » couvre toute la fenetre.
//
//   npm run plateau-paysage
//
// La page est ouverte avec ?etat=<fixture> : aucune partie n'a besoin de tourner.
import { test, expect } from '@playwright/test';

const TITRE_PAGE_AVERTISSEMENT = 'Version Mismatch';
const CIBLE_MINIMUM = 44;
const CARTE_MINIMUM = 84;
const TOLERANCE_ARRONDI = 1;

type Entree = { fichier: string; titre: string };

async function catalogue(page: import('@playwright/test').Page): Promise<Entree[]> {
  await page.goto('/fixtures.html', { waitUntil: 'networkidle' });
  expect(await page.title()).not.toBe(TITRE_PAGE_AVERTISSEMENT);
  const entrees: Entree[] = await page.evaluate(
    () => (window as unknown as { FIXTURES?: Entree[] }).FIXTURES ?? []
  );
  expect(entrees.length, 'Le catalogue des etats enregistres est vide').toBeGreaterThanOrEqual(20);
  return entrees;
}

test('En paysage, deux rangees de vraies cartes qui tiennent a l\'ecran', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 's24-paysage', 'Gabarit paysage seulement');
  const erreurs: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') erreurs.push(`[console] ${message.text()}`);
  });
  page.on('pageerror', (erreur) => erreurs.push(`[page] ${erreur.message}`));

  // Nombre d'etats ou le voile « +N » est apparu tout seul (sans le forcer) :
  // si ce compteur reste a 0 apres la boucle, sa cible tactile de 44 px n'a
  // jamais ete exercee, et un pas dedie force le debordement plus bas.
  let etatsAvecVoile = 0;
  const entrees = await catalogue(page);

  for (const entree of entrees) {
    await test.step(entree.titre, async () => {
      await page.goto(`/app/board.html?etat=${encodeURIComponent(entree.fichier)}`, {
        waitUntil: 'networkidle',
      });

      const vue = page.locator('.plateau-paysage');
      await expect(vue, 'Le rendu paysage ne s\'est pas monte').toBeVisible();
      await expect(page.locator('.ecran-portrait'), 'Ecran portrait affiche en paysage').toHaveCount(0);

      // 1. Rien ne deborde verticalement.
      const debordement = await vue.evaluate((element) => ({
        contenu: element.scrollHeight,
        visible: element.clientHeight,
      }));
      expect(
        debordement.contenu,
        `Le plateau deborde de ${debordement.contenu - debordement.visible} px`
      ).toBeLessThanOrEqual(debordement.visible + TOLERANCE_ARRONDI);

      // 2. Aucune rangee ne rogne ses cartes en silence. .plateau-paysage a
      // lui-meme overflow:hidden, min-height:0 dans toute sa chaine de
      // conteneurs : une grille CSS qui manque de place les laisse toujours
      // EXACTEMENT a la taille disponible (jamais plus), donc l'assertion 1
      // ci-dessus ne peut, par construction, JAMAIS detecter un debordement
      // qui se produit plus bas dans l'arbre. Le vrai bord de decoupe
      // silencieux est .rangee-cartes-defilement (une rangee a la fois,
      // overflow-y:hidden) : si son scrollHeight depasse son clientHeight,
      // la carte posee est plus haute que sa case et se fait rogner en bas,
      // sans aucune pastille pour le dire. Meme principe que la bande de
      // tuiles du plateau a medaillons (plateau-mobile.spec.ts).
      const rangees = page.locator('.rangee-cartes-defilement');
      const nombreRangees = await rangees.count();
      for (let index = 0; index < nombreRangees; index += 1) {
        const mesure = await rangees.nth(index).evaluate((element) => ({
          contenu: element.scrollHeight,
          visible: element.clientHeight,
          nom: element.closest('.rangee-cartes')?.getAttribute('aria-label') ?? '?',
        }));
        expect(
          mesure.contenu,
          `Rangee "${mesure.nom}" : ${mesure.contenu - mesure.visible} px de carte rognes en bas`
        ).toBeLessThanOrEqual(mesure.visible + TOLERANCE_ARRONDI);
      }

      // 3. Chaque carte posee se lit : au moins 84 px de large.
      const cartes = page.locator('.carte-posee > .scan-card');
      const nombreCartes = await cartes.count();
      expect(nombreCartes, 'Aucune carte posee dessinee').toBeGreaterThan(0);
      for (let index = 0; index < nombreCartes; index += 1) {
        const boite = await cartes.nth(index).boundingBox();
        if (!boite) continue;
        expect(boite.width, `Carte trop etroite (${Math.round(boite.width)} px)`).toBeGreaterThanOrEqual(CARTE_MINIMUM);
      }

      // 4. Toute cible tactile respecte le plancher de 44 px.
      const cibles = page.locator('[data-tactile]');
      const nombre = await cibles.count();
      for (let index = 0; index < nombre; index += 1) {
        const boite = await cibles.nth(index).boundingBox();
        if (!boite) continue;
        expect(
          Math.min(boite.width, boite.height),
          `Cible tactile trop petite (${Math.round(boite.width)}x${Math.round(boite.height)})`
        ).toBeGreaterThanOrEqual(CIBLE_MINIMUM);
      }

      if (await page.locator('.rangee-cartes-suite').count() > 0) etatsAvecVoile += 1;
    });
  }

  expect(erreurs, `Erreurs signalees par le navigateur :\n${erreurs.join('\n')}`).toHaveLength(0);

  // 6. Le voile « +N » : sa cible tactile de 44 px doit avoir ete mesuree au
  // moins une fois. Il ne s'affiche que quand une rangee deborde
  // (RangeeCartes.tsx, horsChamp > 0) : rien ne garantit qu'un des 34 etats
  // enregistres en produise un tout seul en 1050 x 480.
  await test.step(`Le voile "+N" est exerce (${etatsAvecVoile}/${entrees.length} etats)`, async () => {
    if (etatsAvecVoile > 0) {
      // Le titre du pas ci-dessus porte deja le compte : rien a affirmer de
      // plus, le test aurait echoue avant d'arriver ici si le voile n'etait
      // jamais apparu.
      test.info().annotations.push({ type: 'voile', description: `${etatsAvecVoile}/${entrees.length} etats` });
      return;
    }

    // Aucun etat ne l'a produit tout seul : on force le debordement sur
    // l'etat qui a le plus de cartes posees dans la rangee ennemie, en
    // retrecissant la fenetre pour que sa rangee deborde a coup sur.
    let etatLePlusCharge = entrees[0];
    let plusDeCartes = -1;
    for (const entree of entrees) {
      await page.goto(`/app/board.html?etat=${encodeURIComponent(entree.fichier)}`, {
        waitUntil: 'networkidle',
      });
      const nombre = await page.locator('.rangee-ennemie .carte-posee').count();
      if (nombre > plusDeCartes) {
        plusDeCartes = nombre;
        etatLePlusCharge = entree;
      }
    }

    const largeurOrigine = page.viewportSize()!;
    await page.setViewportSize({ width: 600, height: 480 });
    try {
      await page.goto(`/app/board.html?etat=${encodeURIComponent(etatLePlusCharge.fichier)}`, {
        waitUntil: 'networkidle',
      });
      const voile = page.locator('.rangee-cartes-suite').first();
      await expect(voile, `Voile +N absent meme force sur "${etatLePlusCharge.titre}"`).toBeVisible();
      const boite = await voile.boundingBox();
      expect(boite?.width, 'Voile +N trop etroit').toBeGreaterThanOrEqual(CIBLE_MINIMUM);
      expect(boite?.height, 'Voile +N trop bas').toBeGreaterThanOrEqual(CIBLE_MINIMUM);
    } finally {
      await page.setViewportSize(largeurOrigine);
    }
  });
});

test('En portrait, l\'ecran « Tourne ton telephone » couvre tout', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 's24', 'Gabarit portrait seulement');
  const entrees = (await catalogue(page)).slice(0, 3);
  const fenetre = page.viewportSize();
  expect(fenetre).not.toBeNull();

  for (const entree of entrees) {
    await test.step(entree.titre, async () => {
      await page.goto(`/app/board.html?etat=${encodeURIComponent(entree.fichier)}`, {
        waitUntil: 'networkidle',
      });
      const voile = page.locator('.ecran-portrait');
      await expect(voile).toBeVisible();
      const boite = await voile.boundingBox();
      expect(boite?.width).toBe(fenetre!.width);
      expect(boite?.height).toBe(fenetre!.height);
      // Le plateau est toujours la, dessous : rien n'a ete demonte.
      await expect(page.locator('.plateau-paysage')).toHaveCount(1);
    });
  }
});
