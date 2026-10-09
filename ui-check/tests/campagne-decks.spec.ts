// Le deck se refait entre deux scenarios, l'identite jamais.
//
// Le livret l'ecrit noir sur blanc : « each player must use their chosen
// identity for the entire campaign, but they are free to change aspects and
// alter the contents of their deck between scenarios ». La Genese des Mutants
// en fait meme un pilier, le role-building : on gagne des ameliorations de
// role d'un scenario a l'autre, et on remonte son deck autour.
//
// Le parcours passe par TROIS endroits qui ne se parlent que par le stockage
// local : l'ecran des campagnes ecrit un brouillon, l'ecran de preparation le
// relit et y depose l'equipe, l'ecran des campagnes le reprend et enregistre.
// Rien dans le code ne relie ces trois moitiés : une renommee de cle, un
// `modifie` oublie, et la modification retomberait silencieusement dans la
// branche de CREATION — elle fabriquerait une deuxieme campagne au lieu de
// modifier la premiere, sans le moindre message. C'est ce que ce test tient.
//
//   npm run campagne-decks
//
// Un seul gabarit (ordinateur) : on verifie une mecanique, pas une apparence.
//
// ATTENTION : ce test cree une campagne sur le serveur, la modifie, puis la
// supprime. Il ne touche a aucune campagne existante (il ne connait que la
// sienne, par son nom) et ne lance aucune partie.
// Selecteurs mis a jour le 09/10/2026 : la refonte « Affiche » de l'assistant
// (b8895bca, 07/09) a remplace #db-<i>/.deck-opt par #deck-liste/.tb-deck, et la
// fenetre des variantes du heros (3d5524b4, 11/09) s'ouvre au clic.
import { test, expect, type Page, type APIRequestContext } from '@playwright/test';

/** Nom de la campagne temoin. Assez singulier pour n'etre celui de personne. */
const NOM_CAMPAGNE = 'Essai automatique - decks';

/** Le heros de la campagne, et celui qu'on essaiera d'y glisser en fraude. */
const HEROS = /^Colossus/;
const HEROS_INTERDIT = /^Cyclops/;

type Membre = { nomHeros?: string; identite?: string[]; deck: { player_deck?: string[] } };
type Campagne = { id: string; nom?: string; equipe?: Membre[] };

let identifiant = '';

/* ================================ mesures ================================ */

/**
 * L'empreinte d'un deck, c'est sa LISTE DE CARTES, jamais son nom.
 *
 * Piege mesure : `validerEquipeCampagne` reecrit `deck.name` avec le nom du
 * HEROS. Deux decks totalement differents de Colossus s'appellent donc tous
 * les deux « Colossus » une fois enregistres. Comparer les noms ferait passer
 * ce test au vert alors que rien n'aurait ete ecrit.
 */
const empreinte = (membre: Membre) => (membre.deck.player_deck ?? []).slice().sort().join(',');

async function campagnes(request: APIRequestContext): Promise<Campagne[]> {
  return (await request.get('/list_campagnes?')).json();
}

async function laNotre(request: APIRequestContext): Promise<Campagne> {
  const trouvee = (await campagnes(request)).find((c) => c.id === identifiant);
  expect(trouvee, `La campagne temoin ${identifiant} a disparu du serveur.`).toBeTruthy();
  return trouvee!;
}

/* =============================== parcours ================================ */

/** Ouvre la campagne temoin depuis la liste. */
async function ouvrirLaCampagne(page: Page) {
  await page.goto('/campagne.html', { waitUntil: 'networkidle' });
  const carte = page.locator('.cmp-carte', { hasText: NOM_CAMPAGNE });
  await expect(carte, "La campagne temoin n'apparait pas dans la liste.").toHaveCount(1);
  await carte.locator('.cmp-carte-ouvrir').click();
  await expect(page.locator('.cmp-page-campagne')).toBeVisible();
}

/**
 * Choisit un heros a l'etape 1, puis passe a l'etape des decks.
 *
 * Toujours dans cet ordre : c'est le heros qui active « Continuer ». La lecon
 * vient de lancement-partie.spec.ts, reste rouge quatre jours pour l'avoir
 * fait dans l'autre sens.
 */
async function choisirHerosPuisDecks(page: Page, motif: RegExp) {
  await page.getByRole('button', { name: motif }).first().click();
  await validerOptionsDuHeros(page);
  await allerAuxDecks(page);
}

/**
 * Depuis le commit 3d5524b4 (11/09/2026), un clic sur un heros qui a des
 * variantes (arts alternatifs, version du deck, identite) ouvre la fenetre
 * « Options de ce heros » par-dessus l'ecran. On la valide telle quelle.
 */
async function validerOptionsDuHeros(page: Page) {
  const modale = page.locator('.deck-modal')
  if (await modale.isVisible().catch(() => false)) {
    await modale.getByRole('button', { name: /valider|confirm/i }).click()
    await expect(modale).toHaveCount(0)
  }
}


/** Passe a l'etape des decks, sans toucher au choix de l'etape 1. */
async function allerAuxDecks(page: Page) {
  await page.getByRole('button', { name: /continuer/i }).click();
  await expect(page.locator('#deck-liste')).toBeVisible();
}

/**
 * Retient un paquet d'aspect conseille, et rend son nom.
 *
 * Pourquoi ceux-la et pas un deck sauvegarde : les conseilles sont FABRIQUES
 * par l'ecran a partir des cartes du jeu, donc presents sur n'importe quelle
 * installation. Les sauvegardes, eux, sont les decks du joueur : ce test
 * n'existerait plus sur une installation neuve.
 *
 * Ils sont replies par defaut, derriere « Paquets d'aspect conseilles (n) » :
 * sans ce clic les boutons existent dans le DOM mais mesurent 0x0, et
 * Playwright attend indefiniment un element qu'aucun humain ne pourrait
 * cliquer non plus.
 */
async function retenirUnDeckDAspect(page: Page, rang: number): Promise<string> {
  const bascule = page.locator('#deck-liste .deck-aspects-bascule', { hasText: /aspect/i });
  await expect(bascule, "Le dépliage des paquets d'aspect a disparu de l'étape des decks.").toBeVisible();
  await bascule.click();
  const option = page.locator('#deck-liste .deck-aspects.est-deplie .tb-deck').nth(rang);
  await option.scrollIntoViewIfNeeded();
  const nom = (await option.locator('.do-name').innerText()).trim();
  await option.click();
  await expect(page.locator('#deck-liste .tb-deck.chosen .do-name')).toHaveText(nom);
  return nom;
}

/* ================================= menage ================================ */

test.beforeAll(async ({ request }) => {
  // Un essai precedent interrompu (fenetre fermee, machine eteinte) laisserait
  // sa campagne derriere lui, et la creation ci-dessous en ferait une seconde
  // du meme nom, suffixee _2. On repart propre.
  for (const c of await campagnes(request)) {
    if (c.nom === NOM_CAMPAGNE) await request.post('/delete_campagne', { data: { id: c.id } });
  }
});

test.afterAll(async ({ request }) => {
  if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } });
});

/* ================================= tests ================================= */

test.describe.serial('Campagne : refaire son deck entre deux scenarios', () => {
  test('La campagne temoin se cree depuis l ecran des campagnes', async ({ page, request }) => {
    await page.goto('/campagne.html', { waitUntil: 'networkidle' });
    await page.getByRole('button', { name: /nouvelle campagne/i }).click();
    await page.locator('.cmp-boite', { hasText: /genese/i }).first().click();
    await page.locator('.cmp-saisie').fill(NOM_CAMPAGNE);
    await page.getByRole('button', { name: /choisir l'équipe/i }).click();

    await expect(page.locator('.campagne-bandeau')).toContainText(NOM_CAMPAGNE);
    await choisirHerosPuisDecks(page, HEROS);
    await page.getByRole('button', { name: /valider l'équipe/i }).click();

    await expect(page.locator('.cmp-page-campagne')).toBeVisible();
    await expect(page.locator('.cmp-erreur')).toHaveCount(0);

    const creee = (await campagnes(request)).filter((c) => c.nom === NOM_CAMPAGNE);
    expect(creee, 'La creation n a pas produit exactement une campagne.').toHaveLength(1);
    identifiant = creee[0].id;
    expect(creee[0].equipe?.[0]?.nomHeros).toMatch(HEROS);
  });

  test('Meme identite, autre deck : le deck est remplace sur le serveur', async ({
    page,
    request,
  }) => {
    const avant = await laNotre(request);

    await ouvrirLaCampagne(page);
    await page.getByRole('button', { name: /modifier les decks/i }).click();

    // Le bandeau doit rappeler les identites a reprendre : c'est la seule
    // indication que le joueur ait de ce qu'on attend de lui, l'ecran de
    // preparation revenant vierge.
    await expect(page.locator('.campagne-bandeau')).toContainText(avant.equipe![0].nomHeros!);

    // L'equipe revient DEJA EN PLACE : aucun clic sur un heros ici. Ce serait
    // meme nuisible, `assignHero` remettant le deck de base au passage.
    await expect(
      page.locator('.tb-port.chosen'),
      "L'equipe de la campagne n'a pas ete remise en place : l'ecran est reparti d'une page blanche."
    ).toHaveCount(1);
    await allerAuxDecks(page);

    // Le deck deja joue a sa propre entree, en tete et retenue : sans elle, le
    // joueur arriverait ici sans savoir lequel de ces paquets est le sien.
    const enCours = page.locator('#deck-liste .tb-deck').first();
    await expect(enCours).toHaveClass(/\bchosen\b/);
    await expect(enCours.locator('.do-name')).toHaveText(/campagne|campaign/i);

    const deckChoisi = await retenirUnDeckDAspect(page, 0);
    await page.getByRole('button', { name: /valider les decks/i }).click();

    await expect(
      page.locator('.cmp-erreur'),
      'La modification a ete refusee alors que l identite n avait pas bouge.'
    ).toHaveCount(0);
    await expect(page.locator('.cmp-page-campagne')).toBeVisible();

    const apres = await laNotre(request);
    expect(
      (await campagnes(request)).filter((c) => c.nom === NOM_CAMPAGNE),
      'La modification a fabrique une SECONDE campagne au lieu de modifier la premiere : '
        + 'le brouillon est reparti dans la branche de creation.'
    ).toHaveLength(1);
    expect(
      apres.equipe![0].identite,
      'L identite a bouge alors que seul le deck devait changer.'
    ).toEqual(avant.equipe![0].identite);
    expect(
      empreinte(apres.equipe![0]),
      `Le deck « ${deckChoisi} } » a ete retenu a l ecran mais rien n a change sur le serveur.`
    ).not.toBe(empreinte(avant.equipe![0]));
  });

  test('Le deck de la campagne reste recuperable apres un clic sur son propre heros', async ({
    page,
    request,
  }) => {
    const avant = await laNotre(request);

    await ouvrirLaCampagne(page);
    await page.getByRole('button', { name: /modifier les decks/i }).click();

    // Le reflexe naturel : cliquer sur son heros, deja retenu. `assignHero` y
    // remet le deck de BASE. Le deck de la campagne doit survivre a ce clic,
    // sinon il serait perdu pour de bon sans le moindre avertissement.
    await choisirHerosPuisDecks(page, HEROS);

    const enCours = page.locator('#deck-liste .tb-deck', { hasText: /campagne|campaign/i }).first();
    await expect(
      enCours,
      'Un clic sur son propre heros a fait disparaitre le deck de la campagne de la liste.'
    ).toBeVisible();
    await enCours.click();
    await page.getByRole('button', { name: /valider les decks/i }).click();

    await expect(page.locator('.cmp-erreur')).toHaveCount(0);
    const apres = await laNotre(request);
    expect(
      empreinte(apres.equipe![0]),
      'Reprendre le deck de la campagne a enregistre autre chose que ce deck.'
    ).toBe(empreinte(avant.equipe![0]));
  });

  test('Changer d identite est refuse, et rien n est ecrit', async ({ page, request }) => {
    const avant = await laNotre(request);

    await ouvrirLaCampagne(page);
    await page.getByRole('button', { name: /modifier les decks/i }).click();
    await choisirHerosPuisDecks(page, HEROS_INTERDIT);
    await page.getByRole('button', { name: /valider les decks/i }).click();

    await expect(
      page.locator('.cmp-erreur'),
      'Une campagne vient de changer de heros en silence.'
    ).toContainText(/identit/i);

    const apres = await laNotre(request);
    expect(apres.equipe, 'Le refus a quand meme ecrit l equipe.').toEqual(avant.equipe);
  });
});
