// Le contrat de lancement d'une partie.
//
// Le seul point de contact entre l'ecran de preparation et le moteur est une
// requete : GET /new?data=<descripteur JSON encode>. Elle n'est documentee
// nulle part. La phase 4 refera entierement la preparation : sans ce test,
// une refonte pourrait casser le demarrage d'une partie SANS QUE RIEN NE LE
// SIGNALE (l'ecran s'afficherait, le clic ne ferait rien d'utile).
//
// Deux verifications, volontairement independantes :
//
//   1. « Sans l'ecran » — on rejoue le contrat directement sur /new, sans
//      navigateur. Elle reste valable meme quand la preparation est en
//      chantier, et elle passe en premier parce qu'elle coute 20 ms : si elle
//      est rouge, le probleme est dans le CONTRAT, pas dans l'ECRAN.
//   2. « Depuis l'ecran » — on joue le parcours complet dans le navigateur,
//      on intercepte la vraie requete, on compare son descripteur au contrat
//      fige (ui-check/contrat-nouvelle-partie.json), puis on prouve qu'on
//      atteint le plateau en interrogeant le moteur (/get_world). Elle passe
//      en dernier pour laisser le serveur sur une partie reellement mise en
//      place, et non sur une partie creee que personne n'a affichee.
//
//   npm run lancement
//
// Un seul gabarit (ordinateur) : on verifie une mecanique, pas une apparence.
// L'apparence, c'est npm run captures qui la surveille.
//
// ATTENTION : ce test lance une NOUVELLE partie sur le serveur de jeu.
// new_game appelle self.game.NewGame(...) sur l'instance unique : toute partie
// en cours est perdue. C'est pourquoi npm run lancement est une commande a
// part, jamais melangee a npm run captures (qui, lui, est en lecture seule).
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

/* ============================ le contrat fige ============================ */

const CHEMIN_CONTRAT = fileURLToPath(new URL('../contrat-nouvelle-partie.json', import.meta.url));

type Contrat = {
  cles: Record<string, string>;
  regles_attendues: string[];
  regles_partie_standard: string[];
  reponse_attendue: unknown;
};

const contrat: Contrat = JSON.parse(fs.readFileSync(CHEMIN_CONTRAT, 'utf8'));

const AVERTISSEMENT =
  'Attention : ce test lance une NOUVELLE partie. Si une partie est en cours, elle sera perdue.';

/* ====================== comparaison au contrat fige ====================== */

/** Le type d'une valeur, dans le vocabulaire du contrat ("string[]", "object"...). */
function typeDe(valeur: unknown): string {
  if (Array.isArray(valeur)) {
    const types = [...new Set(valeur.map((x) => typeof x))];
    return types.length === 1 ? `${types[0]}[]` : 'any[]';
  }
  if (valeur === null) return 'null';
  return typeof valeur;
}

/**
 * Une valeur est-elle compatible avec le type attendu par le contrat ?
 * Tolerance voulue : un tableau vide est compatible avec n'importe quel
 * "X[]" (challenges est vide dans la plupart des scenarios), et "any[]"
 * accepte n'importe quel tableau.
 */
function typeCompatible(attendu: string, valeur: unknown): boolean {
  if (attendu.endsWith('[]')) {
    if (!Array.isArray(valeur)) return false;
    const base = attendu.slice(0, -2);
    return base === 'any' || valeur.every((x) => typeof x === base);
  }
  if (attendu === 'object') {
    return typeof valeur === 'object' && valeur !== null && !Array.isArray(valeur);
  }
  return typeof valeur === attendu;
}

/** Liste, en francais, tout ce qui s'ecarte du contrat. Vide = tout va bien. */
function ecartsAuContrat(descripteur: Record<string, unknown>): string[] {
  const ecarts: string[] = [];

  const attendues = Object.keys(contrat.cles).sort();
  const recues = Object.keys(descripteur).sort();

  const apparues = recues.filter((c) => !attendues.includes(c));
  const disparues = attendues.filter((c) => !recues.includes(c));

  if (apparues.length) {
    ecarts.push(`Cles APPARUES (le moteur ne les attend peut-etre pas) : ${apparues.join(', ')}`);
  }
  if (disparues.length) {
    ecarts.push(`Cles DISPARUES (le moteur les attend) : ${disparues.join(', ')}`);
  }

  for (const cle of attendues) {
    if (!recues.includes(cle)) continue;
    const attendu = contrat.cles[cle];
    const valeur = descripteur[cle];
    if (!typeCompatible(attendu, valeur)) {
      ecarts.push(`Type change pour "${cle}" : contrat = ${attendu}, recu = ${typeDe(valeur)}`);
    }
  }

  const regles = Array.isArray(descripteur.rules) ? (descripteur.rules as unknown[]) : [];
  const manquantes = contrat.regles_attendues.filter((r) => !regles.includes(r));
  if (manquantes.length) {
    ecarts.push(
      `Regles obligatoires absentes de "rules" : ${manquantes.join(', ')} ` +
        `(recu : ${regles.length ? regles.join(', ') : 'aucune regle'})`
    );
  }

  return ecarts;
}

function messageDEcart(origine: string, ecarts: string[]): string {
  return [
    `Le contrat de lancement de partie a change (${origine}).`,
    '',
    ...ecarts.map((e) => `  - ${e}`),
    '',
    'Ce que ca veut dire : ce qui est envoye a GET /new?data= ne correspond plus',
    'a ui-check/contrat-nouvelle-partie.json. Une partie risque de ne plus demarrer.',
    '',
    'Si le changement est ACCIDENTEL : corriger le code de la preparation.',
    'Si le changement est VOULU et mesure : mettre a jour le contrat fige',
    'dans le MEME commit, en expliquant pourquoi.',
  ].join('\n');
}

/* ============================== le parcours ============================== */

const TITRE_PAGE_AVERTISSEMENT = 'Version Mismatch';

async function verifierQueCeNestPasLaPageDeCache(page: Page) {
  expect(
    await page.title(),
    "Le serveur a renvoye la page d'avertissement de cache : le cookie de version n'a pas ete pose."
  ).not.toBe(TITRE_PAGE_AVERTISSEMENT);
}

/**
 * Passe a l'etape suivante de l'assistant. Le bouton est desactive tant que
 * l'etape n'est pas complete : Playwright attend qu'il devienne cliquable,
 * ce qui vaut assertion « l'etape precedente est bien validee ».
 */
async function continuer(page: Page) {
  await page.getByRole('button', { name: /continuer/i }).click();
}

test.beforeAll(() => {
  console.log('');
  console.log('  ' + AVERTISSEMENT);
  console.log('');
});

test.describe("Lancement d'une partie", () => {
  test("Sans l'ecran : le contrat seul suffit a creer une partie", async ({ request }) => {
    // Meme charge utile que celle de launcher.js, reconstruite ici a partir
    // des donnees du serveur. Aucun navigateur : si ce test passe alors que
    // le suivant echoue, c'est l'ECRAN qui a casse, pas le CONTRAT.
    const scenario = await (await request.get('/get_scenario_json?rhino')).json();
    const deck = await (await request.get('/get_hero_json?spider_man')).json();

    const charge: Record<string, unknown> = {
      campaign_json: JSON.stringify(scenario),
      campaign_log: {},
      challenges: scenario.challenges ?? [],
      encounter_set_names: [
        ...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])]),
      ],
      hero_json: [JSON.stringify(deck)],
      rules: contrat.regles_partie_standard,
      seed: 1234,
      timeout: 0,
    };

    // La charge construite doit elle-meme respecter le contrat, sinon on
    // testerait le moteur avec quelque chose que l'ecran n'envoie jamais.
    const ecarts = ecartsAuContrat(charge);
    expect(ecarts, messageDEcart('charge reconstruite depuis le contrat', ecarts)).toEqual([]);

    const reponse = await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)));

    expect(
      reponse.status(),
      `Le moteur a refuse une partie construite selon le contrat fige (HTTP ${reponse.status()}). ` +
        `Le contrat de ui-check/contrat-nouvelle-partie.json ne correspond plus a ce qu'attend /new.`
    ).toBe(200);

    expect(await reponse.json()).toEqual(contrat.reponse_attendue);
  });

  test("Depuis l'ecran de preparation : le contrat est respecte et le plateau repond", async ({
    page,
  }) => {
    // ?ui=new : on veut explicitement la NOUVELLE preparation, quelle que soit
    // la preference eventuellement rangee dans le stockage local (cf. bascule).
    await page.goto('/prepare.html?ui=new', { waitUntil: 'load' });
    await verifierQueCeNestPasLaPageDeCache(page);

    // Parcours minimal, choisi pour etre stable : tout vient de la boite de
    // base, qui ne disparaitra jamais du jeu.
    //   Etape 1 - Mode ......... « Solo » est deja selectionne par defaut.
    await continuer(page);

    //   Etape 2 - Heros ........ Spider-Man (deux heros portent ce nom).
    await page
      .getByRole('button', { name: /^Spider-Man/ })
      .first()
      .click();
    await continuer(page);

    //   Etape 3 - Decks ........ le deck de base est deja retenu.
    await continuer(page);

    //   Etape 4 - Scenario ..... Rhino, premier scenario de la boite de base.
    await page.getByRole('button', { name: /^Rhino$/ }).first().click();
    await continuer(page);

    //   Etape 5 - Difficulte ... les reglages par defaut conviennent.
    await continuer(page);

    //   Etape 6 - Recapitulatif  le bouton de lancement doit etre actif.
    const lancer = page.getByRole('button', { name: /lancer la partie/i });
    await expect(
      lancer,
      "Le bouton de lancement n'est pas utilisable : l'assistant considere la partie comme incomplete."
    ).toBeEnabled();

    // On attrape la vraie requete au vol, avant toute navigation. On attend
    // aussi sa REPONSE : c'est ce qui rend la suite honnete. Le moteur appelle
    // NewGame() avant de repondre, et NewGame remet le monde a zero
    // (render_id = 0, mesure). Sans cette attente, le sondage ci-dessous
    // pourrait lire le monde de la partie PRECEDENTE et se declarer satisfait
    // sans rien avoir prouve.
    const [requete, reponseNew] = await Promise.all([
      page.waitForRequest(/\/new\?data=/),
      page.waitForResponse(/\/new\?data=/),
      lancer.click(),
    ]);

    const brut = decodeURIComponent(new URL(requete.url()).searchParams.get('data')!);
    const descripteur = JSON.parse(brut) as Record<string, unknown>;

    const ecarts = ecartsAuContrat(descripteur);
    expect(ecarts, messageDEcart("depuis l'ecran de preparation", ecarts)).toEqual([]);

    expect(
      reponseNew.status(),
      `Le moteur a refuse la partie envoyee par l'ecran de preparation (HTTP ${reponseNew.status()}).`
    ).toBe(200);

    // Le monde est donc bien celui de la partie qu'on vient de creer.
    const mondeNeuf = await (await page.request.get('/get_world?p=0')).json();
    expect(
      mondeNeuf.render_id,
      'Le monde n\'a pas ete remis a zero par /new : le sondage qui suit lirait la partie precedente.'
    ).toBe(0);

    // Le contrat respecte ne prouve pas que la partie demarre : le client
    // navigue ensuite vers /?hot_seat et le moteur met la scene en place.
    // On interroge le moteur plutot qu'un selecteur du plateau actuel : ce
    // runtime est intouchable, et son DOM ne nous regarde pas.
    // page.request decompresse le gzip renvoye par /get_world ; un fetch brut
    // cote page, non.
    await expect
      .poll(
        async () => {
          const reponse = await page.request.get('/get_world?p=0');
          const monde = await reponse.json();
          return monde.render_id;
        },
        {
          timeout: 60_000,
          intervals: [1000],
          message:
            "La partie a ete creee mais le plateau n'a jamais repondu : le moteur n'a pas fini la mise en place en 60 secondes.",
        }
      )
      .toBeGreaterThan(0);

    const monde = await (await page.request.get('/get_world?p=0')).json();
    expect(
      typeof monde.phase === 'string' && monde.phase.length > 0,
      `Le moteur a rendu un monde mais sans phase de jeu (recu : ${JSON.stringify(monde.phase)}). ` +
        `La mise en place ne s'est pas deroulee normalement.`
    ).toBe(true);
  });
});
