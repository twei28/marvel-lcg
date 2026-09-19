// Le filtre « Fan-made » du roster honore les createurs (18/09/2026) :
//   1. chaque tuile porte le nom du heros SUIVI du createur entre parentheses,
//      ecrit en entier (pas d'ellipse : « Agent Anti-Venom (DesignHacker) ») ;
//   2. une ligne au-dessus de la grille remercie tous les createurs affiches ;
//   3. hors du filtre, ni parentheses ni remerciement ;
//   4. la recherche accepte le nom du CREATEUR, et le champ le dit ;
//   5. les VILAINS, les SETS MODULAIRES et les ASPECTS maison portent aussi
//      leur createur, et l'officiel n'en porte jamais.
//
//   npx playwright test tests/fanmade-createurs.spec.ts --project=pc
//
// Laisse une capture dans ui-check/fanmade-createurs.png pour l'oeil humain.
// Un seul gabarit (ordinateur) : on verifie une mecanique, pas une apparence.
import { test, expect, type Page } from '@playwright/test';

async function ouvrirLeRoster(page: Page) {
  await page.goto('/prepare.html');
  await page.getByRole('button', { name: /^Solo/ }).first().click();
  await expect(page.locator('.tb-port').first()).toBeVisible();
}

test.describe('Le filtre fan-made honore les createurs', () => {
  test('createur entre parentheses, ecrit en entier, et ligne de remerciement', async ({ page }) => {
    await ouvrirLeRoster(page);
    // Hors du filtre : rien.
    await expect(page.locator('#tb-merci')).toBeHidden();
    await expect(page.locator('.tb-port[data-hero="thor"] .tb-port-nom')).toHaveText(/^Thor$/);

    await page.getByRole('button', { name: /^fan-made$/i }).click();
    const merci = page.locator('#tb-merci');
    await expect(merci).toBeVisible();
    await expect(merci).toContainText('Un grand merci à');
    await expect(merci).toContainText('Nugget');
    await expect(merci).toContainText('pour leur travail');

    const nom = page.locator('.tb-port[data-hero="agent_anti_venom"] .tb-port-nom');
    await expect(nom).toHaveText('Agent Anti-Venom (DesignHacker)');
    // En entier : le texte n'est pas coupe par une ellipse (scrollWidth <= clientWidth).
    const coupe = await nom.evaluate((e) => e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 1);
    expect(coupe, 'le nom du createur est tronque sur la tuile').toBe(false);
    // Pas de doublon quand le libellé des homonymes porte deja le createur.
    await expect(page.locator('.tb-port[data-hero="spider_man_rainy"] .tb-port-nom')).toHaveText('Spider-Man (Rainy)');

    await page.screenshot({ path: 'fanmade-createurs.png' });
  });

  test('la recherche trouve un heros par son createur', async ({ page }) => {
    await ouvrirLeRoster(page);
    const champ = page.locator('.tb-search');
    // Hors du filtre, le champ ne promet pas le createur : un heros officiel
    // n'en a pas.
    await expect(champ).toHaveAttribute('placeholder', 'Rechercher un héros ou un trait');

    await page.getByRole('button', { name: /^fan-made$/i }).click();
    await expect(champ).toHaveAttribute('placeholder', 'Rechercher un héros, un trait ou un créateur');

    // Un createur d'un seul pack : la grille se reduit a SA tuile. Sans ce
    // compte, un filtre casse qui laisserait tout passer serait invisible.
    await champ.fill('nugget');
    await expect(page.locator('#hero-grid .tb-port')).toHaveCount(1);
    await expect(page.locator('#hero-grid .tb-port[data-hero="lockjaw"]')).toBeVisible();

    // Un createur cite dans un couple (« BlueHG + DesignHacker ») repond aussi.
    await champ.fill('bluehg');
    await expect(page.locator('#hero-grid .tb-port[data-hero="yondu"]')).toBeVisible();
    await expect(page.locator('#hero-grid .tb-port[data-hero="okoye"]')).toBeVisible();
    await expect(page.locator('#hero-grid .tb-port[data-hero="lockjaw"]')).toHaveCount(0);

    // TEMOIN : la recherche par nom et par trait marche toujours.
    await champ.fill('lockjaw');
    await expect(page.locator('#hero-grid .tb-port[data-hero="lockjaw"]')).toBeVisible();
    await champ.fill('good boy');
    await expect(page.locator('#hero-grid .tb-port[data-hero="lockjaw"]')).toBeVisible();

    // La phrase suit ce qui reste affiche, et se met au SINGULIER pour un seul
    // createur : « pour leur travail » a une personne seule sonnerait faux.
    await champ.fill('nugget');
    await expect(page.locator('#tb-merci')).toHaveText('Un grand merci à Nugget pour son travail : ces héros sont les siens.');
    await champ.fill('');
    await expect(page.locator('#tb-merci')).toContainText('pour leur travail');

    // Capture pour l'oeil humain : tout ce qu'un createur a dessine, d'un mot.
    await champ.fill('rainy');
    await expect(page.locator('#tb-merci')).toContainText('Rainy pour son travail');
    await page.screenshot({ path: 'fanmade-recherche-createur.png' });
  });

  test('vilains, sets modulaires et aspects maison portent leur createur', async ({ page }) => {
    await page.goto('/prepare.html');
    await page.getByRole('button', { name: /^Solo/ }).first().click();
    await expect(page.locator('.tb-port').first()).toBeVisible();
    // Storm n'a aucune option : sa tuile se choisit d'un clic, sans modale
    // (meme raison que dans modale-heros.spec.ts).
    await page.locator('.tb-port[data-hero="storm"]').click();
    await page.getByRole('button', { name: /continuer/i }).click();
    await page.getByRole('button', { name: /continuer/i }).click();

    // VILAINS : chaque extension ouvre ses scenarios.
    const tuile = (id) => page.locator(`.tb-port[data-scn="${id}"] .tb-port-nom`);
    await page.getByRole('button', { name: 'Custom (Gorr the God Butcher)' }).click();
    await expect(tuile('gorr')).toHaveText('Gorr the God Butcher (BlueHG)');
    await page.getByRole('button', { name: 'Custom (The Spot)' }).click();
    await expect(tuile('the_spot')).toHaveText('The Spot (DesignHacker)');
    await page.getByRole('button', { name: 'Custom (Web of Deceit)' }).click();
    await expect(tuile('wd_shocker')).toHaveText('Shocker (Ripper3)');
    await page.screenshot({ path: 'fanmade-vilains-createurs.png' });
    // TEMOIN : un vilain officiel reste nu, sinon on attribuerait a tort.
    await page.getByRole('button', { name: 'Core Set' }).click();
    await expect(tuile('rhino')).toHaveText('Rhino');

    // SETS MODULAIRES : la liste « Personnalises » du bloc de difficulte.
    await page.locator('.tb-port[data-scn="rhino"]').click();
    await page.getByRole('button', { name: /^Personnalisés$/ }).click();
    const chips = page.locator('.mod-chips .mod-chip');
    // Motifs ancres : « Muse » seul attraperait « Art Museum Heist ». Muse
    // n'est pas teste ici, il est mis de cote et ne parait dans aucune liste
    // joueur (_setsRencontreMasques).
    await expect(chips.filter({ hasText: /^Necroverse \(BlueHG\)$/ })).toHaveCount(1);
    await expect(chips.filter({ hasText: /^Intergalactic Hazards \(BlueHG\)$/ })).toHaveCount(1);
    // TEMOIN : un modulaire officiel reste nu, sans parentheses.
    await expect(chips.filter({ hasText: /^Bomb Scare$/ })).toHaveCount(1);
  });
});
