// Le glisser-deposer, dans une VRAIE partie.
//
// Les cas vitest (`ui-app/src/board/glisser/`) couvrent le geste et les regles
// separement, avec un `elementFromPoint` simule. Ce qu'ils ne peuvent pas
// prouver, c'est la chaine complete : un vrai moteur, de vraies options, un
// vrai pointeur, et un mechant qui perd vraiment des points de vie.
//
// La survie du CLIC, elle, reste chez vitest (`geste.test.tsx` : appui sans
// deplacement, tremblement sous le seuil, plateau sans reglages) : trois cas
// deterministes valent mieux qu'un quatrieme qui dependrait de l'etat d'une
// partie reelle.
//
//   npm run glisser
//
// ATTENTION : comme `npm run lancement`, ce test cree une NOUVELLE partie sur
// le serveur de jeu. Toute partie en cours est perdue. C'est pourquoi il a sa
// propre commande et ne participe pas aux captures.
import { test, expect, type Page, type APIRequestContext } from '@playwright/test';

const AVERTISSEMENT =
  'Attention : ce test lance une NOUVELLE partie. Si une partie est en cours, elle sera perdue.';

test.beforeAll(() => {
  console.log('');
  console.log('  ' + AVERTISSEMENT);
  console.log('');
});

/** Une partie solo Spider-Man contre Rhino, graine figee. */
async function nouvellePartie(request: APIRequestContext) {
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const deck = await (await request.get('/get_hero_json?spider_man')).json();
  const charge = {
    campaign_json: JSON.stringify(scenario),
    campaign_log: {},
    challenges: scenario.challenges ?? [],
    encounter_set_names: [
      ...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])]),
    ],
    hero_json: [JSON.stringify(deck)],
    rules: ['standard'],
    seed: 1234,
    timeout: 0,
  };
  const reponse = await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)));
  expect(reponse.status(), 'le moteur a refuse de creer la partie').toBe(200);
}

/**
 * Les points de vie d'une carte, lus chez le MOTEUR et non a l'ecran.
 *
 * ⚠ ON ACCEPTE LE NOMBRE COMME LA CHAINE : le descripteur ecrit selon les
 * champs « 14 » ou 14, et exiger un `number` rendait la lecture muette sur le
 * mechant, donc le cas rouge sans qu'aucun defaut n'existe.
 */
async function pointsDeVie(page: Page, id: number): Promise<number | undefined> {
  return page.evaluate(async (cible) => {
    const monde = await (await fetch('/get_world?p=0')).json();
    let trouve: number | undefined;
    const nombre = (valeur: unknown): number | undefined => {
      const n =
        typeof valeur === 'string' ? Number(valeur) : typeof valeur === 'number' ? valeur : NaN;
      return Number.isFinite(n) ? n : undefined;
    };
    const parcourir = (valeur: unknown) => {
      if (Array.isArray(valeur)) return valeur.forEach(parcourir);
      if (!valeur || typeof valeur !== 'object') return;
      const objet = valeur as Record<string, unknown>;
      if (objet.id === cible) {
        const info = objet.info as Record<string, unknown> | undefined;
        const lu = nombre(info?.health) ?? nombre(objet.health);
        if (lu !== undefined) trouve = lu;
      }
      Object.values(objet).forEach(parcourir);
    };
    parcourir(monde);
    return trouve;
  }, id);
}

test('glisser le heros sur le mechant l attaque', async ({ page, request }) => {
  await nouvellePartie(request);
  await page.goto('/app/board.html?p=0');
  await page.waitForSelector('.scan-card[data-card-id]', { timeout: 30000 });

  // Le mulligan d'ouverture s'ouvre quelques instants apres le plateau : sans
  // cette attente, on cliquait dans le vide et la partie restait bloquee.
  // La mise en place carte par carte (manigance, méchant...) passe avant le mulligan : on la fait défiler.
  for (let k = 0; k < 30 && (await page.locator('.mep-couche').count()) > 0; k++) {
    const continuer = page.locator('.mep-couche .mep-continuer').first();
    if (await continuer.isVisible().catch(() => false)) await continuer.click({ timeout: 1500, force: true }).catch(() => {});
    await page.waitForTimeout(400);
  }
  const confirmer = page.getByRole('button', { name: /^(Confirmer|Garder ma main)/ }).first();
  await confirmer.waitFor({ state: 'visible', timeout: 40000 });
  await confirmer.click();

  // Le changement de forme se fait par la commande du bac à sable : depuis le 18/10/2026 le bouton de la barre du bas
  // n'existe plus (le menu de la carte propose « Changer de forme », mais ce cas teste le GLISSER, pas ce menu).
  const rep = await page.request.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.ChangeForm('01001a')"] } });
  expect(rep.status()).toBe(200);
  await page.waitForSelector('.scan-card.kind-hero[data-card-id]', { timeout: 30000 });

  // ⚠ ON ATTEND QUE LE PLATEAU OFFRE LE GESTE. Juste apres un changement de
  // forme, il se recompose : pendant cette fraction de seconde, aucune carte
  // n'est encore soulevable, et un glisser lance la tombait dans le vide. Le
  // temoin `data-glisser` existe pour repondre a la question sans deviner.
  await page.waitForSelector('.plateau-cadre[data-glisser="offert"]', { timeout: 30000 });

  const heros = await page
    .locator('.scan-card.kind-hero[data-card-id]')
    .first()
    .getAttribute('data-card-id');
  expect(heros, 'aucun heros sur la table').toBeTruthy();

  // On souleve le heros et on s'arrete la : les cibles legales s'allument.
  const boite = await page.locator(`.scan-card[data-card-id="${heros}"]`).first().boundingBox();
  expect(boite, "le heros n'est pas a l'ecran").not.toBeNull();
  await page.mouse.move(boite!.x + boite!.width / 2, boite!.y + boite!.height / 2);
  await page.mouse.down();
  // Plusieurs pas : le seuil se franchit en chemin, comme sous une vraie main.
  await page.mouse.move(boite!.x + boite!.width / 2 + 40, boite!.y + boite!.height / 2 - 40, {
    steps: 8,
  });
  await expect(page.locator('.plateau-cadre.est-en-glisser')).toBeVisible();
  await expect(page.locator('.glisser-carte')).toBeVisible();
  await expect(page.locator('.glisser-trait line')).toHaveCount(1);

  // ⚠ LA CIBLE SORT DU GESTE, ELLE N'EST PAS DEVINEE. Le plateau allume ce que
  // le heros peut viser : on prend le mechant parmi ces cartes-la. Choisir un
  // vilain a l'aveugle tombait sur celui qui attend son tour de scenario, que
  // rien ne permet d'attaquer et qui n'a meme pas de points de vie lisibles.
  const cibles = await page.$$eval(
    '.scan-card.is-target-pulse.kind-villain[data-card-id]',
    (elements) => elements.map((element) => (element as HTMLElement).dataset.cardId)
  );
  expect(cibles.length, "le geste n'allume aucun mechant : rien a attaquer").toBeGreaterThan(0);
  const vilain = cibles[0]!;

  const avant = await pointsDeVie(page, Number(vilain));
  expect(avant, 'le mechant n a pas de points de vie lisibles').toBeGreaterThan(0);

  const arrivee = await page.locator(`.scan-card[data-card-id="${vilain}"]`).first().boundingBox();
  await page.mouse.move(arrivee!.x + arrivee!.width / 2, arrivee!.y + arrivee!.height / 2, {
    steps: 12,
  });
  const etiquette = await page.locator('.glisser-etiquette').textContent();
  expect(etiquette, "l'etiquette doit annoncer ce qui va se passer").toBeTruthy();

  await page.mouse.up();
  await page.waitForTimeout(1500);

  // ⚠ LE CAS QUI COMPTE : on ne verifie pas un affichage, on verifie que le
  // MOTEUR a recu l'attaque. Les points de vie viennent de /get_world.
  const apres = await pointsDeVie(page, Number(vilain));
  expect(apres, "le mechant n'a pas encaisse l'attaque lachee sur lui").toBeLessThan(avant!);

  // Le geste est fini : plus de couche, plus de cadre marque.
  await expect(page.locator('.couche-glisser')).toHaveCount(0);
  await expect(page.locator('.plateau-cadre.est-en-glisser')).toHaveCount(0);
});
