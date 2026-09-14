// SUR LA TABLE, DANS UNE VRAIE PARTIE : L'ANNONCE ATTEND LE CLIC, ET UN SEUL
// PANNEAU OCCUPE LE CENTRE.
//
// ⚠ POURQUOI CE FICHIER EXISTE, ET POURQUOI IL LANCE UNE VRAIE PARTIE.
//
// Il garde DEUX défauts de la fiche du 14/09/2026, tous deux invisibles :
//
//  n°1, troisième cause — « je te l'ai dit mille fois, pourquoi est-ce que ça
//  continue tout seul sans que moi je mette suivant ? » En mode « Détaillé »,
//  une ANNONCE acquitte toute seule (décision 7 de la spec du 07/09, « pas de
//  clic sur va attaquer ») ; sur la table, l'utilisateur a décidé l'inverse :
//  deux clics par attaque, l'annonce portant le premier, « parce que c'est là
//  aussi où on peut choisir de défendre ». La garde est `!surTable`, dans
//  `ui-app/src/board/cartouche-a-jour.ts`.
//
//  n°2 — « c'est quoi cette merde qui se superpose » : le sélecteur de cibles,
//  le panneau du moteur et le cartouche replié, tous les trois au centre.
//
// ⚠ ET `phase-sur-table.spec.ts` NE PEUT GARDER NI L'UN NI L'AUTRE. Il lit un
// état ENREGISTRÉ, qui ne rejoue aucune trame du moteur et ne pose aucune
// question : il n'y a rien à relâcher, donc rien à retenir, et aucun panneau à
// empiler. Mesuré — en retirant la garde `!surTable` et en reconstruisant le
// plateau, ses cas restent VERTS.
//
//   npm run annonce-attend-le-clic
//
// ⚠ IL LANCE UNE NOUVELLE PARTIE sur le serveur visé : toute partie en cours y
// est perdue.
import { expect, test, type Page } from '@playwright/test';
import {
  avancerLaPartie,
  lancer,
  monde,
  ouvrirEtMettreEnPlace,
  type Conduite,
} from '../pilote-campagne';

/** Une partie ORDINAIRE, sans campagne (contrat-nouvelle-partie.json). */
const REGLES_STANDARD = [
  'v16_all',
  'no_crisis_of_infinite_deadpools',
  'no_encounter_cards_ignore_crisis',
];

/** Les quatre phases du méchant, au sens du moteur (ui-app/src/board/moteur.ts). */
const PHASES_MECHANT = [
  'Main Scheme Place Threat',
  'Enemy Activation',
  'Deal Encounter Cards',
  'Reveal Encounter Cards',
];

/** Le temps d'observation sans toucher à rien. Plus long que tous nos délais. */
const ATTENTE_MS = 5000;

/**
 * Le héros reste en forme HÉROS et frappe : sinon le méchant MANIGANCE au lieu
 * d'attaquer, et aucune annonce d'attaque n'arrive jamais.
 */
const CONDUITE: Conduite = { resterEnHeros: true, attaquer: true };

/**
 * Ce que le joueur lit en ce moment, à côté du bouton, sur la table.
 *
 * ⚠ `count()` D'ABORD, TOUJOURS. `innerText()` sur un élément absent ATTEND
 * cinq secondes avant d'échouer, et un `.catch()` masque cette attente : à deux
 * cents tours de boucle, un test de treize secondes en mettait sept minutes.
 * Mesuré le 14/09/2026, et c'est ce qui avait fait abandonner une première
 * version de ce fichier.
 */
async function recit(page: Page): Promise<string> {
  const bloc = page.locator('.deroule-recit').first();
  if (!(await bloc.count())) return '';
  return (await bloc.innerText()).replace(/\s+/g, ' ').trim();
}

/** Les panneaux qui occupent le centre, sans compter ceux qui s'emboîtent. */
async function panneauxAuCentre(page: Page): Promise<number> {
  return page.evaluate(() => {
    const tous = [
      ...document.querySelectorAll('.deroule-phase, .demande-centrale, .cibles-scene, .selecteur-cibles'),
    ].filter((e) => (e as HTMLElement).offsetParent !== null);
    return tous.filter((e) => !tous.some((autre) => autre !== e && autre.contains(e))).length;
  });
}

test('⚠ sur la table, « va attaquer » N’AVANCE PAS tout seul', async ({ page, request }) => {
  test.setTimeout(240000);

  await lancer(request, {
    scenario: 'rhino',
    heros: ['spider_man'],
    regles: REGLES_STANDARD,
    seed: 1234,
  });

  // Les réglages AVANT d'ouvrir le plateau : il les lit à son montage.
  //
  // ⚠ PAS D'INTERCEPTION DE `/get_site_admin` ICI. Elle ne sert qu'à afficher le
  // choix du mode dans les réglages ; le mode lui-même se lit dans le stockage
  // local. Et une route interceptée empêche le `waitUntil: 'networkidle'`
  // d'`ouvrirEtMettreEnPlace` de se satisfaire — mesuré le 14/09/2026, le test
  // restait bloqué cinq minutes avant même sa première boucle.
  await page.goto('/main.html');
  await page.evaluate(() => {
    localStorage.setItem('marvel-langue-choisie', '1');
    localStorage.setItem('marvel-board-mode-phase-mechant', 'sur-table');
    // ⚠ ALLUMÉE À DESSEIN. « Avance toute seule » est grisée hors du mode
    // Détaillé, mais griser ne désactive pas : sa valeur s'appliquait quand
    // même, et c'était la PREMIÈRE des trois causes du défaut n°1. L'allumer
    // ici fait de ce test le témoin des deux causes à la fois.
    localStorage.setItem('marvel-board-avance-auto', 'on');
  });

  await ouvrirEtMettreEnPlace(page, request);

  // ⚠ LE TOUR DU HÉROS SE JOUE PAR LE PILOTE, LA PHASE DU MÉCHANT PAR L'ÉCRAN.
  // Sur la table, la phase n'avance QUE sur le clic du joueur : le cartouche
  // retient la trame du moteur tant qu'il ne l'a pas eu. Appeler le pilote
  // pendant cette phase le fait attendre une question qui ne viendra jamais.
  let annonce = '';
  let panneauxMax = 0;
  for (let round = 0; round < 4 && !annonce; round += 1) {
    if (!PHASES_MECHANT.includes(String((await monde(request)).phase))) {
      await avancerLaPartie(
        page,
        request,
        ({ monde: courant }) => PHASES_MECHANT.includes(String(courant.phase)),
        60,
        CONDUITE
      );
    }

    for (let temps = 0; temps < 40 && !annonce; temps += 1) {
      panneauxMax = Math.max(panneauxMax, await panneauxAuCentre(page));

      const texte = await recit(page);
      // L'annonce, telle que le moteur la nomme : « X va attaquer Y ».
      if (/va attaquer/i.test(texte)) {
        annonce = texte;
        break;
      }

      const bouton = page.locator('.deroule-rond');
      if ((await bouton.count()) && (await bouton.first().isVisible())) {
        await bouton.first().click();
        await page.waitForTimeout(350);
        continue;
      }

      // Une question du moteur au centre : on passe, comme un joueur qui
      // encaisse. C'est ce qui laisse l'activation suivante arriver.
      const passer = page.getByRole('button', { name: /^passer$/i }).first();
      if (await passer.count()) {
        await passer.click();
        await page.waitForTimeout(350);
        continue;
      }

      // La main est revenue au héros : on ressort jouer son tour.
      if (!PHASES_MECHANT.includes(String((await monde(request)).phase))) break;
      await page.waitForTimeout(400);
    }
  }

  // ⚠ NE PAS VOIR L'ANNONCE EST DÉJÀ LE DÉFAUT. Sans la garde `!surTable`, le
  // cartouche acquitte le moteur sur l'annonce : elle passe toute seule, et le
  // joueur ne la lit jamais. Mesuré le 14/09/2026 en retirant la garde — c'est
  // par ce message-ci que ce test échoue alors.
  expect(
    annonce,
    'aucune annonce « va attaquer » n’a pu être LUE : soit la phase n’en produit ' +
      'aucune, soit elle défile toute seule sans attendre le clic — le défaut n°1, ' +
      'troisième cause (voir ui-app/src/board/cartouche-a-jour.ts)'
  ).not.toBe('');

  // ⚠ LE CŒUR DU TEST : ON NE TOUCHE À RIEN, ET ON REGARDE.
  await page.waitForTimeout(ATTENTE_MS);

  // ⚠ DEUX ÉCRANS SONT JUSTES ICI, ET UN SEUL EST FAUX.
  //
  //  1. l'annonce est toujours là : le cartouche attend le clic ;
  //  2. le cartouche s'est TU et le panneau du moteur a pris sa place
  //     (« Défendre / Passer »). Sur la table il ne double jamais le panneau du
  //     moteur : c'est le correctif du défaut n°2. C'est même LA raison pour
  //     laquelle l'annonce porte un clic, « parce que c'est là aussi où on peut
  //     choisir de défendre ».
  //
  // Le cas FAUX, celui que ce test garde : le déroulé est passé au temps
  // SUIVANT sans que personne n'ait cliqué.
  const apres = await recit(page);
  const question = await page.getByRole('button', { name: /^(passer|défendre)$/i }).count();
  expect(
    apres === annonce || (apres === '' && question > 0),
    `l'annonce a été acquittée TOUTE SEULE en ${ATTENTE_MS} ms : « ${annonce} » est devenu ` +
      `« ${apres} » et aucune question du moteur n'est ouverte (défaut n°1, troisième cause).`
  ).toBe(true);

  // Défaut n°2 : jamais deux panneaux empilés au centre, à aucun moment de la
  // phase — y compris sur une VRAIE question du moteur, ce qu'aucun état
  // enregistré ne sait produire.
  panneauxMax = Math.max(panneauxMax, await panneauxAuCentre(page));
  expect(panneauxMax, `${panneauxMax} panneaux empilés au centre`).toBeLessThanOrEqual(1);

  // Puis on répond, comme un joueur qui encaisse, et on REGARDE ENCORE : le
  // temps suivant doit lui aussi attendre.
  if (question > 0) {
    await page.getByRole('button', { name: /^passer$/i }).first().click();
    await page.waitForTimeout(1500);
  }
  const suite = await recit(page);
  expect(suite, 'plus rien ne s’affiche après la réponse : la phase serait perdue').not.toBe('');
  await page.waitForTimeout(ATTENTE_MS);
  expect(
    await recit(page),
    `le temps suivant est passé TOUT SEUL en ${ATTENTE_MS} ms : « ${suite} » a changé sans un clic`
  ).toBe(suite);

  // Et le bouton est bien là pour avancer à la main, quand le joueur le voudra.
  await expect(
    page.locator('.deroule-rond').first(),
    'plus aucun bouton pour avancer : la phase serait bloquée'
  ).toBeVisible();
});
