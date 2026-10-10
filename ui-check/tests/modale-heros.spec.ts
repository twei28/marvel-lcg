// La modale du heros (11/09/2026) : une seule tuile par heros, et au clic une
// fenetre qui propose ce que CE heros a de particulier (version du deck,
// identite, art, ressources), memorisee d'une partie a l'autre.
//
// Ce que ce filet prouve, sur Hellcat (deux versions : Iron Man ou Miss Hulk
// en allie signature) :
//   1. la variante `hellcat_she_hulk` est REPLIEE sous la tuile Hellcat ;
//   2. la modale s'ouvre au clic, la version de base est preselectionnee ;
//   3. choisir Miss Hulk puis Valider se lit dans le rappel de l'etape DECKS ;
//   4. au retour sur l'ecran, la modale se rouvre SUR le dernier choix ;
//   5. un heros sans option n'ouvre aucune modale : la tuile se choisit
//      directement. Storm a recu un art alternatif (donc une option) : le
//      temoin est depuis le 10/10/2026 Agatha Harkness, fan-made sans art,
//      sans version ni identite alternative.
//
//   npm run modale-heros
//
// Un seul gabarit (ordinateur) : on verifie une mecanique, pas une apparence.
import { test, expect, type Page } from '@playwright/test';

async function ouvrirLeRoster(page: Page) {
  await page.goto('/prepare.html');
  await page.getByRole('button', { name: /^Solo/ }).first().click();
}

/** Les heros fan-made sont derriere le filtre « Fan-made » du roster. */
async function montrerLesFanMade(page: Page) {
  await page.getByRole('button', { name: /^fan-made$/i }).click();
}

function tuile(page: Page, id: string) {
  return page.locator(`.tb-port[data-hero="${id}"]`);
}

/** Les boutons de la PREMIERE section de la modale (les versions du deck). */
function versions(page: Page) {
  return page.locator('.vh-panel .res-art').first().locator('.ra-option');
}

test.describe('La modale du heros', () => {
  test('Hellcat : deux versions, le choix est applique, rappele et memorise', async ({ page }) => {
    await ouvrirLeRoster(page);
    await montrerLesFanMade(page);

    await expect(tuile(page, 'hellcat'), 'une seule tuile Hellcat').toHaveCount(1);
    await expect(
      tuile(page, 'hellcat_she_hulk'),
      'la variante Miss Hulk doit etre repliee sous Hellcat, pas en tuile a part'
    ).toHaveCount(0);

    await tuile(page, 'hellcat').click();
    const modale = page.locator('.vh-panel');
    await expect(modale, 'la modale ne s’est pas ouverte au clic sur Hellcat').toBeVisible();
    await expect(modale.getByText('Version du deck de héros')).toBeVisible();
    await expect(versions(page)).toHaveCount(2);
    await expect(versions(page).nth(0), 'la version de base est preselectionnee').toHaveClass(/\bsel\b/);

    await versions(page).nth(1).click();
    await expect(versions(page).nth(1)).toHaveClass(/\bsel\b/);
    await modale.getByRole('button', { name: /^valider$/i }).click();
    await expect(modale).toBeHidden();

    // Le rappel, a l'etape DECKS.
    await page.getByRole('button', { name: /continuer/i }).click();
    await expect(
      page.locator('.tb-variantes-rappel').first(),
      'le rappel de l’etape DECKS doit nommer la version choisie'
    ).toContainText(/Hulk/);

    // La memoire : on revient sur l'ecran, la modale se rouvre sur Miss Hulk.
    await ouvrirLeRoster(page);
    await montrerLesFanMade(page);
    await tuile(page, 'hellcat').click();
    await expect(page.locator('.vh-panel')).toBeVisible();
    await expect(versions(page).nth(1), 'le dernier choix n’a pas ete retenu').toHaveClass(/\bsel\b/);
    await page.locator('.vh-panel').getByRole('button', { name: /^annuler$/i }).click();
    await expect(page.locator('.vh-panel')).toBeHidden();
  });

  // ATTENTION : ce test lance une NOUVELLE partie sur le serveur de jeu (comme
  // npm run lancement) : toute partie en cours sur ce serveur est perdue.
  test('Hellcat version Miss Hulk : le deck ENVOYE au moteur est celui de la version', async ({ page }) => {
    await ouvrirLeRoster(page);
    await montrerLesFanMade(page);
    await tuile(page, 'hellcat').click();
    await versions(page).nth(1).click();
    await page.locator('.vh-panel').getByRole('button', { name: /^valider$/i }).click();
    await page.getByRole('button', { name: /continuer/i }).click();
    await page.getByRole('button', { name: /continuer/i }).click();
    await page.getByRole('button', { name: /^Rhino\b/ }).first().click();
    await page.getByRole('button', { name: /continuer/i }).click();
    const lancer = page.getByRole('button', { name: /lancer la partie/i });
    await expect(lancer).toBeEnabled();
    const [requete] = await Promise.all([page.waitForRequest(/\/new\?data=/), lancer.click()]);
    const brut = decodeURIComponent(new URL(requete.url()).searchParams.get('data')!);
    const descripteur = JSON.parse(brut) as { hero_json: string[] };
    const deck = JSON.parse(descripteur.hero_json[0]!) as { hero_deck?: string[]; name?: string };
    expect(deck.hero_deck, 'le deck envoye doit porter Miss Hulk (hc012)').toContain('hc012');
    expect(deck.hero_deck, 'et pas Iron Man (hc002), l’allie de la version de base').not.toContain('hc002');
  });

  test('Agatha Harkness : aucune option, donc aucune modale, la tuile se choisit directement', async ({ page }) => {
    await ouvrirLeRoster(page);
    await montrerLesFanMade(page);
    await tuile(page, 'agatha_harkness').click();
    await expect(tuile(page, 'agatha_harkness')).toHaveClass(/\bchosen\b/);
    await expect(page.locator('.vh-panel')).toHaveCount(0);
  });
});
