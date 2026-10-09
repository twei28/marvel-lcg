// Les cartes fan-made de Determination s'affichent-elles en francais ?
//
// La traduction d'une carte passe normalement par son IMAGE (assets/pics-fr) :
// le jeu demande fr_<code>.jpg et retombe seul sur l'anglais quand elle manque.
// Determination est fan-made, il n'existe aucun scan FR et il n'y en aura pas.
// Son texte francais vit donc dans public/js/prepare/cartes-fr.js.
//
// Il n'est PAS dans data/cards.json, et c'est volontaire : deux endroits LISENT
// le texte anglais pour decider — dt133.py compte les personnages « Fragile. »
// et scheme_main.py reconnait une manigance perdante a sa phrase. Traduire en
// place les casserait.
import { test, expect } from '@playwright/test';

test('le module FR couvre les 142 cartes et s applique', async ({ page }) => {
  await page.goto('/galerie.html');
  await page.waitForTimeout(2500);

  const r = await page.evaluate(async () => {
    const m: any = await import('/public/js/prepare/cartes-fr.js');
    return {
      nb: Object.keys(m.CARTES_FR).length,
      traduit: m.carteFr({ card_id: 'dt008', name: 'Merc Squad', text: 'x' }).name,
      nomFr: m.nomFr({ card_id: 'dt008', name: 'Merc Squad' }),
      // Une carte hors du pack doit rester intacte.
      intacte: m.carteFr({ card_id: '01064', name: 'Surveillance Team', text: 'x' }).name,
    };
  });

  expect(r.nb, 'le pack compte 142 cartes').toBe(142);
  expect(r.traduit).toBe('Escouade de mercenaires');
  expect(r.nomFr, 'nomFr rend une chaine, pour les objets Card a methodes')
    .toBe('Escouade de mercenaires');
  expect(r.intacte, 'une carte hors pack ne doit pas etre touchee')
    .toBe('Surveillance Team');
});

test('l editeur de deck cherche et affiche en francais', async ({ page }) => {
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(String(e)));

  await page.goto('/deck-builder.html?hero=spider_man');
  await page.waitForSelector('.db-chip', { timeout: 30000 });
  // Determination est fan-made : caché tant que l'interrupteur n'est pas mis.
  await page.locator('.db-inter').click();

  // La recherche doit trouver le mot FRANCAIS, celui que le joueur lit. La
  // grille ne répète plus le nom sous le scan : il est dans le texte de l'image.
  await page.locator('.db-recherche').first().fill('Escouade');
  await page.waitForTimeout(1000);

  await expect(page.locator('#db-grille .db-carte img[alt="Escouade de mercenaires"]'),
    'la recherche francaise ne trouve pas la carte').toHaveCount(1);
  expect(erreurs.join(' | ')).toBe('');
});
