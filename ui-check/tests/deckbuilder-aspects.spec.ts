// L'editeur de deck propose-t-il TOUS les aspects du jeu ?
//
// Le moteur derive sa liste d'aspects de deux `Literal` (card_player.py), mais
// l'editeur tient la SIENNE, en dur : `ASPECTS` dans js/deckbuilder/app.js. Rien
// ne relie les deux. Un cinquieme aspect ajoute au moteur, avec ses cartes, ses
// images et ses modules, reste donc INVISIBLE ici — les cartes sont filtrees
// (app.js, `if (!ASPECTS.includes(c.class) ...) return false`) et aucune erreur
// n'apparait nulle part. C'est exactement ce qui s'est passe pour Determination
// le 13/08/2026 : 20 cartes dans le jeu, aucune deckable.
//
// Le test ne verrouille pas une liste : il demande que chaque aspect PRESENT
// DANS LES DONNEES ait sa puce et ses cartes. Un aspect a venir passera donc
// sans toucher a ce fichier.
import { test, expect } from '@playwright/test';

// Les classes qui ne sont pas des aspects de construction de deck.
const NON_ASPECTS = new Set([
  'Basic', 'IdentitySpecific', 'Encounter', 'Campaign', 'Aspect', 'Hero',
]);

test('chaque aspect present dans les donnees a sa puce dans l editeur', async ({ page }) => {
  await page.goto('/deck-builder.html?hero=spider_man');
  await page.waitForSelector('.db-chip', { timeout: 30000 });
  // Les aspects fan-made ne sont proposés qu'avec l'interrupteur « fan-made ».
  await page.locator('.db-inter').click();

  // Les aspects vus par les DONNEES, pas par une liste ecrite ici.
  const aspects: string[] = await page.evaluate(async () => {
    const reponse = await fetch('get_cards_json?');
    const packs = await reponse.json();
    const vus = new Set<string>();
    for (const liste of Object.values(packs) as any[]) {
      if (!Array.isArray(liste)) continue;
      for (const carte of liste) {
        const classe = carte?.desc?.Class;
        if (classe) vus.add(String(classe));
      }
    }
    return [...vus];
  });

  // Une carte signature porte une classe composee (« Hero;Aggression ») : elle
  // ne designe pas un aspect de construction de deck.
  const attendus = aspects.filter((a) => !a.includes(';') && !NON_ASPECTS.has(a));
  expect(attendus.length, 'aucun aspect trouve dans les donnees').toBeGreaterThan(4);

  // Seules les puces d'ASPECT : la meme classe CSS sert aux sources de cartes
  // (« Vide », « Base : Spider-Man ») et aux types.
  // `data-aspect` porte la classe du moteur : le libellé, lui, est traduit.
  const puces = await page.locator('.db-chip[data-aspect]').evaluateAll(
    (n) => n.map((x) => x.getAttribute('data-aspect') || ''));
  console.log('ASPECTS DANS LES DONNEES :', attendus.join(', '));
  console.log('PUCES DE L EDITEUR       :', puces.join(', '));

  for (const aspect of attendus) {
    expect(puces, `l'aspect ${aspect} n'a pas de puce dans l'editeur`).toContain(aspect);
  }
});

test('filtrer sur Determination montre des cartes choisissables', async ({ page }) => {
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(String(e)));

  await page.goto('/deck-builder.html?hero=spider_man');
  await page.waitForSelector('.db-chip', { timeout: 30000 });
  await page.locator('.db-inter').click();
  await page.locator('.db-chip[data-aspect="Determination"]').click();
  await page.waitForTimeout(1000);

  // Le nombre grandira a chaque lot : on demande qu'il y en ait, pas combien.
  const trouve = Number((await page.locator('#db-grille-info b').innerText()).trim());
  console.log('CARTES DETERMINATION PROPOSEES :', trouve);
  expect(trouve).toBeGreaterThanOrEqual(20);
  expect(erreurs.join(' | '), 'erreur JS dans l editeur').toBe('');
});
