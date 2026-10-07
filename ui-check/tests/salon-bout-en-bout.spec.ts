// LE SALON, LA CHAINE ENTIERE, A L'ECRAN.
//
// ⚠ POURQUOI CE FICHIER EXISTE, ET POURQUOI IL NE DOUBLE PAS
// `bascule-salon.spec.ts`. Celui-la eprouve la REGLE PURE (`decisionSalon`) :
// il l'appelle avec des etats fabriques, sans moteur, sans page, sans reseau.
// Il est reste vert pendant les deux rondes de correction du 21/09/2026 et les
// six defauts qu'elles ont trouves, parce qu'AUCUN n'etait dans la regle :
// ils etaient dans l'assemblage (un repere ecrit et jamais relu, un repere
// releve apres l'envoi, un repere efface a tort) et dans le RENDU (un statut
// efface toutes les deux secondes, un bouton reconstruit sous le doigt).
//
// Ce fichier-ci fait tourner la chaine : deux navigateurs distincts, leurs
// cookies de siege, le vrai moteur, la vraie page, le vrai sondage de deux
// secondes. Il voit donc ce que la regle pure ne peut pas voir.
//
// ⚠ IL EXIGE UN MOTEUR A SIEGES PROTEGES, ET UN SEUL LOT DE CAS A LA FOIS.
// Le moteur est un singleton : au-dela de quelques parties creees sur le meme
// processus, son etat se met a MENTIR sans lever d'erreur (constate au
// 18/09/2026, rapport de la tache 8 du mode manuel). Chaque lot ci-dessous
// tient en deux parties et se lance sur un moteur FRAIS :
//
//   ~/marvel-work/python/bin/python3.10 serveur-essai-salon.py --port 2347 --sieges-proteges
//   export UI_CHECK_BASE=http://127.0.0.1:2347 WSLENV=UI_CHECK_BASE
//   npx playwright test tests/salon-bout-en-bout.spec.ts --project=pc -g "cas 7"
//
// ⚠ JAMAIS SUR `.game` NI SUR LE PORT 2345 : lancer le moteur depuis WSL sur
// le cache de production detruit la table du joueur.
import { test, expect, request as apiRequest, type APIRequestContext, type Browser, type Page } from '@playwright/test';
import { ADRESSE_JEU } from '../playwright.config';

/** Les cles que `serveur-essai-salon.py --sieges-proteges` installe. */
const cle = (siege: number) => `cle-${siege}`;

/** Le scenario des manches d'essai. Il n'a aucune importance ici : ce qui
 *  compte est qu'une partie TOURNE, et avec quel heros a quel siege. */
const SCENARIO = 'rhino';
const REGLES = ['v16_all', 'no_crisis_of_infinite_deadpools', 'no_encounter_cards_ignore_crisis'];

/* ------------------------------------------------------------------ */
/* L'HOTE : celui qui cree la partie.                                  */
/* ------------------------------------------------------------------ */

async function hote(): Promise<APIRequestContext> {
  return clientDeSiege(0);
}

/**
 * Un client muni du cookie d'UN siege.
 *
 * ⚠ IL EN FAUT UN PAR SIEGE, ET C'EST LA ROUTE QUI L'EXIGE.
 * `/get_heros_du_siege` est gardee par `tient_le_siege` : l'hote lisant `?p=1`
 * recoit 403, pas l'etat du siege 1. C'est voulu (un invite ne doit pas lire
 * le siege du voisin), et c'est une chose que seul un essai a l'ecran
 * rencontre — la regle pure ne parle jamais a la route.
 */
async function clientDeSiege(siege: number): Promise<APIRequestContext> {
  const ctx = await apiRequest.newContext({ baseURL: ADRESSE_JEU });
  await ctx.get('/get_version'); // cookie app_version
  await ctx.get(`/claim_seat?p=${siege}&key=${cle(siege)}&to=prepare`);
  return ctx;
}

/** L'identifiant de carte heros d'un deck de depart ("spider_man" -> "01001a").
 *  C'est exactement ce que le salon compare (`heroCardId`) et ce que
 *  `/get_heros_du_siege` publie. */
async function carteHeros(ctx: APIRequestContext, deck: string): Promise<string> {
  const json = await (await ctx.get(`/get_hero_json?${deck}`)).json();
  return String((json.hero ?? [])[0] ?? '').split(',')[0];
}

/** Le lancement, tel que `prepare/launcher.js` le fait : un `/new?data=`. */
async function lancerManche(
  ctx: APIRequestContext,
  heros: string[],
  regles: readonly string[] = REGLES
): Promise<void> {
  const definition = await (await ctx.get(`/get_scenario_json?${SCENARIO}`)).json();
  const decks: string[] = [];
  for (const h of heros) decks.push(JSON.stringify(await (await ctx.get(`/get_hero_json?${h}`)).json()));
  const reponse = await ctx.get(
    '/new?data=' +
      encodeURIComponent(
        JSON.stringify({
          campaign_json: JSON.stringify(definition),
          campaign_log: {},
          challenges: definition.challenges ?? [],
          encounter_set_names: [
            ...new Set([...(definition.encounter_sets ?? []), ...(definition.modular_sets ?? [])]),
          ],
          hero_json: decks,
          rules: regles,
          seed: 4242,
          timeout: 0,
        })
      )
  );
  expect(reponse.ok(), 'le moteur a refuse la creation de la partie').toBeTruthy();
}

/** Le repere que la table publie pour un siege, et s'il s'y joue quelque chose.
 *  ⚠ Lu par l'HOTE : la route est gardee par siege. */
async function table(ctx: APIRequestContext, siege: number) {
  const r = await ctx.get(`/get_heros_du_siege?p=${siege}`);
  const brut = (await r.json()) as { en_jeu?: boolean; heros?: string; debut?: string; error?: string };
  expect(brut.error, `la table refuse de parler du siege ${siege} : ${brut.error}`).toBeUndefined();
  return { en_jeu: !!brut.en_jeu, heros: String(brut.heros ?? ''), debut: String(brut.debut ?? '') };
}

/** Une partie ne TOURNE vraiment que lorsqu'un client s'est connecte : sans
 *  navigateur, `controller.world` reste vide et la table se dit hors jeu.
 *  On ouvre donc le plateau de l'hote, comme il le fait en vrai apres avoir
 *  clique « Lancer ». */
async function ouvrirLePlateauDeLHote(browser: Browser): Promise<Page> {
  const ctx = await browser.newContext({ baseURL: ADRESSE_JEU });
  const page = await ctx.newPage();
  await page.goto('/get_version');
  await page.goto('/main.html');
  await page.evaluate(() => localStorage.setItem('marvel-langue-choisie', '1'));
  await page.goto(`/claim_seat?p=0&key=cle-0&to=`);
  await page.goto('/app/board.html?p=0&multi=1', { waitUntil: 'domcontentloaded' });
  return page;
}

/** Attend que la table se declare EN JEU (le monde est monte). */
async function attendreQueLaTableTourne(ctx: APIRequestContext, siege: number): Promise<string> {
  await expect
    .poll(async () => (await table(ctx, siege)).en_jeu, {
      timeout: 120_000,
      message: 'la partie ne demarre pas : aucun client connecte, ou le moteur est bloque',
    })
    .toBe(true);
  return (await table(ctx, siege)).debut;
}

/**
 * La mise en place, traversee A L'ECRAN, siege par siege.
 *
 * ⚠ SANS ELLE, « arriver sur son plateau » ne prouve pas grand-chose. Un
 * invite qui bascule au bon moment tombe d'abord sur une table EN COURS DE
 * MONTAGE : la premiere identite est posee, le reste attend que chaque siege
 * reponde a son mulligan. Mesure du 21/09/2026 : la premiere version de ce cas
 * se contentait du premier `.plateau-unite` venu et capturait un plateau ou
 * l'invite du siege 1 ne voyait que le heros du siege 0. On clique donc
 * « Garder cette main » sur CHAQUE page, comme les joueurs le font, et on
 * attend que le moteur quitte sa phase d'initialisation.
 */
async function traverserLaMiseEnPlace(ctx: APIRequestContext, pages: Page[]): Promise<string> {
  const phase = async () => String(((await (await ctx.get('/get_world?p=0')).json()) as any).phase ?? '');
  let vue = await phase();
  for (let i = 0; i < 120 && (vue === '' || /Initialize|Setup|Mulligan/i.test(vue)); i++) {
    for (const page of pages) {
      const bouton = page.getByRole('button', { name: /Garder cette main|Confirmer/ });
      if ((await bouton.count()) > 0) await bouton.first().click({ timeout: 3_000 }).catch(() => {});
    }
    await pages[0].waitForTimeout(1_000);
    vue = await phase();
  }
  return vue;
}

/* ------------------------------------------------------------------ */
/* UN INVITE : son navigateur, son cookie de siege, son salon.         */
/* ------------------------------------------------------------------ */

/**
 * ⚠ UN CONTEXTE PAR INVITE, ET SANS `storageState`. Deux invites sur le meme
 * contexte partageraient cookies ET localStorage : le repere de l'un
 * ecraserait celui de l'autre, et c'est precisement ce que `cleRepere(siege)`
 * evite. On repart donc d'un navigateur nu, et c'est le LIEN DE SIEGE qui pose
 * le cookie — l'URL seule ne donne aucun droit.
 */
async function invite(browser: Browser, siege: number) {
  const ctx = await browser.newContext({ baseURL: ADRESSE_JEU });
  const page = await ctx.newPage();
  // Le cookie de version, sinon le moteur sert une page d'avertissement de
  // cache A LA PLACE du salon, avec un code 200.
  await page.goto('/get_version');
  await page.goto('/main.html');
  await page.evaluate(() => localStorage.setItem('marvel-langue-choisie', '1'));
  await page.goto(`/claim_seat?p=${siege}&key=${cle(siege)}&to=salon`);
  await expect(page).toHaveURL(new RegExp(`/salon\\.html\\?p=${siege}$`));
  return { ctx, page };
}

/** Rouvre le salon de ce siege : c'est le RECHARGEMENT de page de l'invite.
 *  Le cookie et le localStorage restent, seul le script repart de zero. */
async function rechargerLeSalon(page: Page, siege: number) {
  await page.goto(`/salon.html?p=${siege}`);
}

/** Choisit un heros dans la grille, puis son premier deck — a la souris.
 *  Le heros est vise par son POSITION dans le catalogue, calculee depuis son
 *  identifiant de carte : les libelles changent avec la langue, pas les ids. */
async function choisirLeHeros(page: Page, heroCardId: string) {
  const rang = await page.evaluate(async (id) => {
    const mod: any = await import('/public/js/prepare/catalog.js');
    const heroes = await mod.catalog.heroes();
    return heroes.findIndex((h: any) => h.heroCardId === id);
  }, heroCardId);
  expect(rang, `heros ${heroCardId} absent du catalogue du salon`).toBeGreaterThanOrEqual(0);
  await page.locator('.salon-hero').nth(rang).click();
  await page.locator('.salon-deck').first().click();
  // Le bandeau « Tu es pret » est le signe que le choix est parti ET accepte.
  await expect(page.locator('#salon-attente')).toHaveClass(/est-visible/, { timeout: 15_000 });
}

/** Le repere que CE navigateur a retenu pour ce siege. */
async function repereRetenu(page: Page, siege: number) {
  return page.evaluate(
    (s) => JSON.parse(window.localStorage.getItem(`mc-salon-repere-${s}`) ?? 'null'),
    siege
  );
}

/* ================================================================== */
/* 1. LE CAS 7, EN VRAI.                                              */
/* ================================================================== */

test('⚠ cas 7 : manche precedente chargee, deux invites choisissent, 90 s sans lancement', async ({
  browser,
}) => {
  test.setTimeout(420_000);
  const ctx = await hote();

  // LA MANCHE PRECEDENTE. Elle reste chargee sur la table — c'est le chemin le
  // plus emprunte d'une soiree : jouer, ecran de fin, « Retour au menu ».
  const spider = await carteHeros(ctx, 'spider_man');
  const captain = await carteHeros(ctx, 'captain_america');
  const sheHulk = await carteHeros(ctx, 'she_hulk');
  await lancerManche(ctx, ['spider_man', 'captain_america', 'she_hulk']);
  const plateauHote = await ouvrirLePlateauDeLHote(browser);
  const vu1 = await clientDeSiege(1);
  const vu2 = await clientDeSiege(2);
  const repereAncien = await attendreQueLaTableTourne(vu1, 1);
  expect(repereAncien, 'la table ne publie aucun repere de partie').not.toBe('');
  // Les sieges 1 et 2 tiennent bien, dans CETTE partie, les heros que les
  // invites vont rechoisir. C'est tout le piege du cas 7.
  expect((await table(vu1, 1)).heros).toBe(captain);
  expect((await table(vu2, 2)).heros).toBe(sheHulk);
  // L'hote quitte le plateau : la partie reste chargee, plus personne ne la
  // regarde. Exactement « Retour au menu ».
  await plateauHote.goto('/main.html');

  // LES DEUX INVITES ARRIVENT, ET RECHOISISSENT LE MEME HEROS QU'A LA MANCHE
  // PRECEDENTE. Sans le repere de fraicheur, chacun « se reconnaitrait » dans
  // la partie d'avant et y serait expedie.
  const a = await invite(browser, 1);
  const b = await invite(browser, 2);
  await choisirLeHeros(a.page, captain);
  await choisirLeHeros(b.page, sheHulk);

  // Le repere retenu est bien celui de la manche PRECEDENTE.
  expect(await repereRetenu(a.page, 1)).toMatchObject({ h: captain, d: repereAncien });
  expect(await repereRetenu(b.page, 2)).toMatchObject({ h: sheHulk, d: repereAncien });

  // ⚠ 90 SECONDES SANS QUE L'HOTE LANCE — le double du delai de proposition
  // (DELAI_PROPOSITION = 45 s). C'est la duree qui compte : la version de la
  // ronde 1 ouvrait ici un bouton « Rejoindre cette partie » qui menait DROIT
  // dans la manche precedente.
  await a.page.waitForTimeout(90_000);

  for (const [page, siege] of [[a.page, 1], [b.page, 2]] as const) {
    await expect(page, `l'invite du siege ${siege} a quitte le salon`).toHaveURL(
      new RegExp(`/salon\\.html\\?p=${siege}$`)
    );
    // ⚠ `toHaveCount(0)` ET NON `not.toHaveClass` : tant qu'aucun
    // avertissement n'a jamais ete montre, `zoneAvertissement()` n'a pas ete
    // appelee et le conteneur N'EXISTE PAS dans la page. Chercher une classe
    // dessus echouerait sur « element not found », c'est-a-dire sur le
    // resultat qu'on veut.
    await expect(
      page.locator('#salon-avertissement.est-visible'),
      `une proposition s'est ouverte au siege ${siege} : le cas 7 est rouvert`
    ).toHaveCount(0);
    // Et la page dit toujours la meme chose : le choix est pris, on attend.
    await expect(page.locator('#salon-attente')).toHaveClass(/est-visible/);
  }
  await a.page.screenshot({ path: 'salon-cas7.png' });

  expect(spider).not.toBe(''); // le siege 0 est bien celui de l'hote
  await a.ctx.close();
  await b.ctx.close();
  await ctx.dispose();
});

/* ================================================================== */
/* 2. LA BASCULE ORDINAIRE.                                           */
/* ================================================================== */

test('⚠ la bascule ordinaire : les deux invites arrivent sur LEUR plateau', async ({ browser }) => {
  test.setTimeout(420_000);
  const ctx = await hote();

  const captain = await carteHeros(ctx, 'captain_america');
  const sheHulk = await carteHeros(ctx, 'she_hulk');

  // La manche precedente, encore une fois : c'est elle qui rend la bascule
  // interessante. Si elle n'etait pas la, n'importe quel signal suffirait.
  await lancerManche(ctx, ['spider_man', 'captain_america', 'she_hulk']);
  let plateauHote = await ouvrirLePlateauDeLHote(browser);
  const vu1 = await clientDeSiege(1);
  const repereAncien = await attendreQueLaTableTourne(vu1, 1);
  await plateauHote.goto('/main.html');

  const a = await invite(browser, 1);
  const b = await invite(browser, 2);
  await choisirLeHeros(a.page, captain);
  await choisirLeHeros(b.page, sheHulk);

  // L'HOTE LANCE.
  await lancerManche(ctx, ['spider_man', 'captain_america', 'she_hulk']);
  await plateauHote.goto('/app/board.html?p=0&multi=1', { waitUntil: 'domcontentloaded' });
  const repereNeuf = await attendreQueLaTableTourne(vu1, 1);
  expect(repereNeuf, 'le repere n’a pas change : la partie neuve est prise pour l’ancienne')
    .not.toBe(repereAncien);

  // LES DEUX INVITES PARTENT SEULS. Aucun clic : c'est le sondage qui decide.
  for (const [page, siege] of [[a.page, 1], [b.page, 2]] as const) {
    await page.waitForURL(new RegExp(`/app/board\\.html\\?p=${siege}&multi=1$`), { timeout: 60_000 });
  }

  // ⚠ ET ILS ARRIVENT SUR LEUR PLATEAU, PAS SUR « Connexion a la partie... ».
  // C'est le corollaire reste entier : basculer au bon moment ne sert a rien
  // si la table qu'on trouve derriere est muette.
  for (const [page, siege] of [[a.page, 1], [b.page, 2]] as const) {
    await expect(
      page.locator('.plateau-unite').first(),
      `le siege ${siege} a bascule mais sa table ne se dessine pas`
    ).toBeVisible({ timeout: 120_000 });
    await expect(
      page.locator('.plateau-message'),
      `le siege ${siege} est reste sur « Connexion a la partie... »`
    ).toHaveCount(0);
  }

  // Et la table se monte vraiment : les trois sieges repondent a leur mulligan
  // depuis LEUR page, et la partie quitte l'initialisation.
  const phase = await traverserLaMiseEnPlace(ctx, [plateauHote, a.page, b.page]);
  expect(phase, 'la partie ne sort pas de la mise en place').not.toMatch(/Initialize|Setup|Mulligan/i);
  for (const [page, siege] of [[a.page, 1], [b.page, 2]] as const) {
    await expect(
      page.locator('.plateau-unite'),
      `le siege ${siege} ne voit qu'une poignee de cartes : la table n'est pas montee`
    ).not.toHaveCount(0);
    await expect(page.locator('.plateau-message')).toHaveCount(0);
  }
  await a.page.screenshot({ path: 'salon-bascule-siege1.png', fullPage: false });
  await b.page.screenshot({ path: 'salon-bascule-siege2.png', fullPage: false });

  await a.ctx.close();
  await b.ctx.close();
  await ctx.dispose();
});

/* ================================================================== */
/* 4. UN MESSAGE TRANSITOIRE QUI SURVIT CINQ SECONDES.                */
/* ================================================================== */

test('⚠ « Import en cours… » n’est pas efface par le sondage de deux secondes', async ({
  browser,
}) => {
  test.setTimeout(180_000);
  const a = await invite(browser, 1);

  // Un import qui PREND DU TEMPS, comme un vrai : marvelcdb repond au bout de
  // huit secondes. Sans reseau lent, le message disparaitrait avant qu'on
  // puisse rien mesurer, et le cas ne prouverait rien.
  await a.page.route('https://marvelcdb.com/**', async (route) => {
    await new Promise((r) => setTimeout(r, 8_000));
    await route.fulfill({ status: 404, body: '{}' });
  });

  // N'importe quel heros : ce qui est mesure ici est le DOM, pas le choix.
  await a.page.locator('.salon-hero').first().click();
  await expect(a.page.locator('.salon-mcdb-champ')).toBeVisible();

  await a.page.locator('.salon-mcdb-champ').fill('12345');
  await a.page.locator('.salon-mcdb-bouton').click();
  await expect(a.page.locator('#salon-statut')).toHaveText(/Import en cours/);

  // ⚠ CINQ SECONDES, SOIT TROIS TOURS DE SONDAGE. La version de la ronde 1
  // repeignait `#salon-statut` a chaque tour : le message tenait moins de deux
  // secondes, et l'invite ne voyait jamais ce qui se passait.
  await a.page.waitForTimeout(5_000);
  await expect(
    a.page.locator('#salon-statut'),
    'le sondage a efface le message transitoire : la ronde 2 est rouverte'
  ).toHaveText(/Import en cours/);

  await a.ctx.close();
});

/* ================================================================== */
/* 5. UN CLIC SUR « Rejoindre avec X » PENDANT QU'UN SONDAGE TOURNE.  */
/* ================================================================== */

test('⚠ « Rejoindre avec X » part du premier coup, sans etre reconstruit sous le doigt', async ({
  browser,
}) => {
  test.setTimeout(420_000);
  const ctx = await hote();

  const captain = await carteHeros(ctx, 'captain_america');
  const sheHulk = await carteHeros(ctx, 'she_hulk');

  // Manche precedente, puis l'invite du siege 1 choisit Captain America.
  await lancerManche(ctx, ['spider_man', 'captain_america', 'she_hulk']);
  const plateauHote = await ouvrirLePlateauDeLHote(browser);
  const vu1 = await clientDeSiege(1);
  await attendreQueLaTableTourne(vu1, 1);
  await plateauHote.goto('/main.html');

  const a = await invite(browser, 1);
  await choisirLeHeros(a.page, captain);

  // ⚠ L'HOTE LANCE EN CHANGEANT LE HEROS DU SIEGE 1. C'est le cas « sans-toi »
  // avec une sortie : le salon propose de rejoindre quand meme.
  await lancerManche(ctx, ['spider_man', 'she_hulk', 'captain_america']);
  await plateauHote.goto('/app/board.html?p=0&multi=1', { waitUntil: 'domcontentloaded' });
  await attendreQueLaTableTourne(vu1, 1);
  expect((await table(vu1, 1)).heros).toBe(sheHulk);

  const bouton = a.page.locator('.salon-avertissement-bouton');
  await expect(bouton).toBeVisible({ timeout: 60_000 });
  const libelle = await bouton.textContent();
  expect(libelle, 'le bouton ne nomme pas le heros du siege').toMatch(/Rejoindre avec/);

  // ⚠ ON ATTEND D'ETRE A CHEVAL SUR UN SONDAGE. La version de la ronde 1
  // rappelait `replaceChildren` toutes les deux secondes : le bouton etait
  // DETRUIT et refait sous le doigt, et un clic tombe pile la ne declenchait
  // rien. On clique donc juste apres un tour de sondage, la ou le risque est
  // maximal, et le noeud doit etre LE MEME avant et apres.
  await a.page.waitForTimeout(2_100);
  const memeNoeud = await a.page.evaluate(() => {
    const n = document.querySelector('.salon-avertissement-bouton');
    (window as any).__noeudBouton = n;
    return !!n;
  });
  expect(memeNoeud).toBe(true);
  await a.page.waitForTimeout(2_100);
  expect(
    await a.page.evaluate(
      () => (window as any).__noeudBouton === document.querySelector('.salon-avertissement-bouton')
    ),
    'le bouton a ete reconstruit par le sondage : un clic a cheval se perdrait'
  ).toBe(true);

  await bouton.click();
  await a.page.waitForURL(/\/app\/board\.html\?p=1&multi=1$/, { timeout: 15_000 });
  await a.page.screenshot({ path: 'salon-rejoindre.png' });

  await a.ctx.close();
  await ctx.dispose();
});

/* ================================================================== */
/* 3. LA CAMPAGNE RECHARGEE.                                          */
/* ================================================================== */

test('⚠ campagne : un invite qui recharge APRES le lancement bascule seul', async ({ browser }) => {
  test.setTimeout(420_000);
  const ctx = await hote();

  // Une campagne en cours, ecrite dans le dossier ISOLE du serveur d'essai
  // (`campagne_folder`), jamais dans celui du joueur.
  const membres = ['spider_man', 'captain_america', 'she_hulk'];
  const equipe = [];
  for (const h of membres) {
    const deck = await (await ctx.get(`/get_hero_json?${h}`)).json();
    equipe.push({ heros: h, nomHeros: String(deck.name ?? h), identite: deck.hero, deck });
  }
  const enregistree = await ctx.post('/save_campagne', {
    data: {
      campagne: {
        code: 'fne',
        nom: 'Essai salon a l ecran',
        difficulte: 'standard',
        equipe,
        termines: [],
        carnet: {},
        tentatives: {},
        partieEnCours: { scenario: SCENARIO, depuis: new Date().toISOString() },
      },
    },
  });
  expect(enregistree.ok(), 'la campagne d’essai n’a pas pu etre enregistree').toBeTruthy();

  // La manche precedente de la campagne, encore chargee. LANCEE EN MODE
  // CAMPAGNE (`mode_campaign`, comme le fait launcher.js) : depuis le
  // 07/10/2026 la route ne parle que si la partie que tient le moteur est de
  // campagne, `partieEnCours` seul ne suffit plus (une table ordinaire ne doit
  // pas s'annoncer « equipe fixee par la campagne »).
  const reglesCampagne = [...REGLES, 'mode_campaign'];
  await lancerManche(ctx, membres, reglesCampagne);
  const encours = await (await ctx.get('/get_campagne_en_cours?')).json();
  expect(encours.id, 'le moteur ne voit aucune campagne en cours').toBeTruthy();
  const plateauHote = await ouvrirLePlateauDeLHote(browser);
  const vu1 = await clientDeSiege(1);
  const repereAncien = await attendreQueLaTableTourne(vu1, 1);
  await plateauHote.goto('/main.html');

  // L'INVITE DE CAMPAGNE. Rien a choisir : le livret a fixe l'equipe.
  const a = await invite(browser, 1);
  await expect(a.page.locator('.salon-campagne-heros')).toContainText(/Tu tiens|You play/);
  // Son repere se releve au premier sondage, faute de choix ou l'accrocher.
  await expect
    .poll(async () => (await repereRetenu(a.page, 1))?.d, { timeout: 20_000 })
    .toBe(repereAncien);

  // ⚠ IL QUITTE SA PAGE AVANT LE LANCEMENT. Sans cela il basculerait en direct
  // et on ne mesurerait pas le RECHARGEMENT, qui est le chemin qu'une
  // correction vient d'ouvrir (le repere de campagne etait ecrit, jamais relu).
  await a.page.goto('/main.html');

  await lancerManche(ctx, membres, reglesCampagne);
  await plateauHote.goto('/app/board.html?p=0&multi=1', { waitUntil: 'domcontentloaded' });
  const repereNeuf = await attendreQueLaTableTourne(vu1, 1);
  expect(repereNeuf).not.toBe(repereAncien);

  // RECHARGEMENT APRES LE LANCEMENT : il doit repartir SEUL, sans clic.
  await rechargerLeSalon(a.page, 1);
  await a.page.waitForURL(/\/app\/board\.html\?p=1&multi=1$/, { timeout: 60_000 });
  await expect(a.page.locator('.plateau-unite').first()).toBeVisible({ timeout: 120_000 });
  await a.page.screenshot({ path: 'salon-campagne.png' });

  await a.ctx.close();
  await ctx.dispose();
});
