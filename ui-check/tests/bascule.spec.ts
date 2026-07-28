// La sortie de secours vers l'ancienne version.
//
// Ce que ce fichier prouve, sur le couple prepare.html (nouvelle preparation)
// et scene.html (ancienne preparation) :
//
//   1. sans rien demander, on reste sur la nouvelle version ;
//   2. l'adresse ?ui=old fait bien basculer sur l'ancienne, avec son bandeau ;
//   3. le choix est MEMORISE : une navigation ulterieure sans parametre reste
//      sur l'ancienne version. C'est le point qui compte vraiment, parce que le
//      parametre d'adresse est perdu des le lancement d'une partie
//      (launcher.js fait location.href = "/?hot_seat") ;
//   4. le bandeau ramene a la nouvelle version, et ca tient au rechargement.
//
//   npm run bascule
//
// Un seul gabarit (ordinateur) : on verifie une mecanique de navigation, pas
// une apparence. L'apparence, c'est npm run captures qui la surveille.
import { test, expect, type BrowserContext, type Page } from '@playwright/test';

// Meme etat que les captures : il porte le cookie de version, sans lequel le
// serveur renvoie sa page d'avertissement de cache a la place de tout ecran.
// Il ne contient AUCUN stockage local : chaque contexte demarre donc sans
// preference d'interface, ce qui est exactement le point de depart voulu.
const ETAT_NAVIGATEUR = './.auth/state.json';
const GABARIT_PC = { width: 1920, height: 1080 };

const TITRE_PAGE_AVERTISSEMENT = 'Version Mismatch';

const NOUVELLE_PREPARATION = /\/prepare\.html(\?.*)?$/;
const ANCIENNE_PREPARATION = /\/scene\.html(\?.*)?$/;

// L'aiguillage de prepare.html redirige pendant l'analyse du document : le
// chargement en cours est donc annule par le navigateur. Ce n'est pas une
// erreur, c'est le comportement recherche (aucun affichage avant la bascule).
async function ouvrir(page: Page, adresse: string) {
  await page.goto(adresse, { waitUntil: 'commit' }).catch(() => undefined);
}

async function verifierQueCeNestPasLaPageDeCache(page: Page) {
  expect(
    await page.title(),
    "Le serveur a renvoye la page d'avertissement de cache : le cookie de version n'a pas ete pose."
  ).not.toBe(TITRE_PAGE_AVERTISSEMENT);
}

test.describe('Bascule entre la nouvelle et l\'ancienne preparation', () => {
  test('Sans preference, on reste sur la nouvelle preparation', async ({ browser }) => {
    const contexte = await browser.newContext({
      storageState: ETAT_NAVIGATEUR,
      viewport: GABARIT_PC,
    });
    const page = await contexte.newPage();

    await ouvrir(page, '/prepare.html');
    await page.waitForLoadState('load');

    await verifierQueCeNestPasLaPageDeCache(page);
    await expect(page, "Sans preference, aucune redirection ne doit avoir lieu.").toHaveURL(
      NOUVELLE_PREPARATION
    );
    await expect(page.locator('#app')).toBeVisible();

    // Le lien de sortie de secours est la, sinon personne ne peut basculer.
    await expect(page.locator('#ui-switch-lien')).toBeVisible();
    await expect(page.locator('#ui-switch-lien')).toHaveText("Revenir à l'ancienne version");

    await contexte.close();
  });

  // Les trois etapes suivantes se jouent dans LE MEME navigateur, dans l'ordre :
  // c'est la memorisation du choix qui est en jeu, elle n'a aucun sens dans
  // trois navigateurs neufs.
  test.describe.serial('Aller et retour dans un meme navigateur', () => {
    let contexte: BrowserContext;
    let page: Page;

    test.beforeAll(async ({ browser }) => {
      contexte = await browser.newContext({
        storageState: ETAT_NAVIGATEUR,
        viewport: GABARIT_PC,
      });
      page = await contexte.newPage();
    });

    test.afterAll(async () => {
      await contexte.close();
    });

    test("L'adresse ?ui=old bascule sur l'ancienne preparation", async () => {
      await ouvrir(page, '/prepare.html?ui=old');
      await page.waitForURL(ANCIENNE_PREPARATION, { waitUntil: 'load' });

      await verifierQueCeNestPasLaPageDeCache(page);
      await expect(page.locator('#w-stepper')).toBeVisible();

      const bandeau = page.locator('#ui-switch-bandeau');
      await expect(bandeau).toBeVisible();
      await expect(bandeau).toContainText("Vous utilisez l'ancienne version.");
      await expect(page.locator('#ui-switch-retour')).toBeVisible();
    });

    test('Le choix est memorise sans le parametre d\'adresse', async () => {
      // Exactement ce qui se passe apres un lancement de partie : on revient
      // sur /prepare.html sans aucun parametre.
      await ouvrir(page, '/prepare.html');
      await page.waitForURL(ANCIENNE_PREPARATION, { waitUntil: 'load' });

      await expect(page.locator('#ui-switch-bandeau')).toBeVisible();
      expect(
        await page.evaluate(() => localStorage.getItem('ui')),
        "La preference doit rester 'old' tant qu'on n'en change pas."
      ).toBe('old');
    });

    test('Le bandeau ramene a la nouvelle preparation, durablement', async () => {
      await page.locator('#ui-switch-retour').click();
      await page.waitForURL(NOUVELLE_PREPARATION, { waitUntil: 'load' });
      await expect(page.locator('#app')).toBeVisible();

      // Le vrai test du retour : recharger ne doit PAS renvoyer sur l'ancienne.
      await page.reload({ waitUntil: 'load' });
      await expect(page).toHaveURL(NOUVELLE_PREPARATION);
      await expect(page.locator('#ui-switch-lien')).toBeVisible();
      expect(await page.evaluate(() => localStorage.getItem('ui'))).toBe('new');
    });
  });
});
