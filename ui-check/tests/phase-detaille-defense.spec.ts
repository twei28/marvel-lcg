// LA FENÊTRE DE DÉFENSE, EN MODE DÉTAILLÉ, DANS UNE VRAIE PARTIE.
//
// ⚠ POURQUOI CE FICHIER EXISTE. Défaut signalé en partie le 14/09/2026 :
// « en mode détaillé il n'indique même plus quand on peut défendre, il fait
// cliquer sur la carte sans rien indiquer. C'est une putain de régression. »
//
// Cause mesurée ici même, en jouant : quand le moteur pose « Défendre /
// Passer » PENDANT l'animation d'un effet précédent (1,7 s par effet), la
// question n'était logée NI dans le panneau central NI dans la scène. Le
// cartouche se repliait sur « tu peux défendre ou répondre » SANS UN SEUL
// BOUTON, et il ne restait au joueur que le menu d'une carte de la table.
// La règle est désormais dans `ui-app/src/board/ou-va-la-question.ts`.
//
//   npm run phase-detaille-defense
//
// ⚠ IL LANCE UNE NOUVELLE PARTIE sur le serveur visé : commande à part, comme
// `npm run lancement`. Sur le serveur de chantier :
//   cd ui-check && UI_CHECK_BASE=http://127.0.0.1:2348 WSLENV=UI_CHECK_BASE \
//     npx playwright test tests/phase-detaille-defense.spec.ts --project=pc
import { test, expect, type Page, type APIRequestContext } from '@playwright/test';

const REGLES = ['v16_all', 'no_crisis_of_infinite_deadpools', 'no_encounter_cards_ignore_crisis'];

/** Les quatre phases du méchant, au sens du moteur (ui-app/src/board/moteur.ts). */
const PHASES_MECHANT = [
  'Main Scheme Place Threat',
  'Enemy Activation',
  'Deal Encounter Cards',
  'Reveal Encounter Cards',
];

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
    rules: REGLES,
    // Graine figée : c'est elle qui garantit que Rhino attaque au round 2.
    seed: 1234,
    timeout: 0,
  };
  const reponse = await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)));
  expect(reponse.status(), 'le moteur a refusé la partie').toBe(200);
}

/** Les options d'une demande : le moteur les envoie dans `options_json`. */
function optionsDe(ask: { options_json?: string } | undefined): Array<Record<string, never>> {
  if (!ask) return [];
  try {
    const lu = JSON.parse(String(ask.options_json ?? '[]'));
    return Array.isArray(lu) ? lu : [];
  } catch {
    return [];
  }
}

/**
 * Ce que le moteur demande en ce moment, ou undefined.
 *
 * ⚠ `/get_ask` répond un objet MÊME QUAND IL N'Y A RIEN À DEMANDER : il est
 * alors sans `event_name`. Le lire comme une question faisait échouer ce test
 * sur des moments où le moteur ne demandait rien du tout.
 */
async function demandeDuMoteur(page: Page) {
  const brut = await (await page.request.get('/get_ask?p=0')).text();
  if (!brut.trim()) return undefined;
  try {
    const lu = JSON.parse(brut);
    return typeof lu?.event_name === 'string' && lu.event_name ? lu : undefined;
  } catch {
    return undefined;
  }
}

/** Répond au moteur exactement comme le ferait un bouton du plateau. */
async function repondre(page: Page, option?: { id: number; all_legal_targets?: number[]; target_num_range?: [number, number] }) {
  const corps =
    option === undefined
      ? {}
      : (() => {
          const legales = option.all_legal_targets ?? [];
          const [min, max] = option.target_num_range ?? [0, 0];
          const combien = Math.min(Math.max(min, 0), legales.length, max);
          return { id: option.id, targets: legales.slice(0, combien), resources: [] };
        })();
  await page.evaluate(async (r) => {
    await fetch('/post?p=0', {
      method: 'POST',
      headers: { 'Content-type': 'application/x-www-form-urlencoded' },
      body: JSON.stringify(r),
    });
  }, corps);
}

/**
 * ⚠ LA SURVEILLANCE FINE, ET C'EST ELLE QUI GARDE LE DÉFAUT.
 *
 * Le cartouche REPLIÉ veut dire « le client SAIT que le moteur attend une
 * réponse ». En mode Détaillé, pendant la phase du méchant, cette branche ne
 * porte AUCUN bouton : la scène est le seul endroit où répondre. Tant qu'on ne
 * clique aucune carte (ce test n'en clique aucune), elle ne doit jamais
 * paraître.
 *
 * Elle se lit sur l'état du CLIENT seul, jamais sur celui du moteur : aucun
 * délai de propagation ne peut la rendre instable.
 *
 * ⚠ ET ELLE S'APPELLE JUSTE APRÈS CHAQUE CLIC. Le défaut ne durait que le
 * temps d'une animation d'effet (1,7 s), déclenchée par les dégâts que le clic
 * vient de laisser passer. Une mesure par seconde de boucle le manquait :
 * vérifié le 14/09/2026, ancienne règle remise, test au vert à tort.
 */
async function surveillerLeCartouche(page: Page, millisecondes: number) {
  const pas = 200;
  for (let passe = 0; passe * pas < millisecondes; passe += 1) {
    expect(
      await page.locator('.deroule-phase.est-replie').count(),
      'le cartouche s’est replié SANS BOUTON pendant que le moteur attendait une réponse : ' +
        'c’est exactement le défaut du 14/09/2026 (voir ou-va-la-question.ts)'
    ).toBe(0);
    await page.waitForTimeout(pas);
  }
}

test('⚠ en mode Détaillé, on sait TOUJOURS quand on peut défendre', async ({ page, request }) => {
  // Une partie réelle jusqu'au round 2 : ce test est lent PAR NATURE.
  test.setTimeout(300000);

  await nouvellePartie(request);

  await page.goto('/main.html');
  await page.evaluate(() => {
    localStorage.setItem('marvel-langue-choisie', '1');
    // LE MODE QUI NOUS INTÉRESSE, écrit explicitement : c'est le défaut du
    // jeu, mais un test ne doit pas dépendre d'un défaut.
    localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille');
    localStorage.setItem('marvel-board-avance-auto', '0');
  });
  await page.goto('/app/board.html');
  await expect
    .poll(async () => (await (await request.get('/get_world?p=0')).json()).render_id, {
      timeout: 90_000,
      intervals: [1000],
    })
    .toBeGreaterThan(0);
  await page.waitForSelector('.plateau-scene', { timeout: 60000 });
  await page.waitForTimeout(2500);

  const garder = page.getByRole('button', { name: /garder cette main/i }).first();
  if (await garder.count()) {
    await garder.click();
    await page.waitForTimeout(2500);
  }

  let basculeFaite = false;
  let questionsVues = 0;
  // ⚠ DEUX FENÊTRES DE DÉFENSE, PAS UNE. C'est la SECONDE qui porte le défaut :
  // elle arrive pendant que l'animation des dégâts de la première est encore à
  // l'écran. Un test qui s'arrêtait à la première passait au vert sur le code
  // défectueux — vérifié le 14/09/2026 en remettant l'ancienne règle.
  const DEFENSES_A_VOIR = 2;
  let defensesVues = 0;

  for (let tick = 0; tick < 90 && defensesVues < DEFENSES_A_VOIR; tick += 1) {
    const monde = await (await page.request.get('/get_world?p=0')).json();
    const ask = await demandeDuMoteur(page);
    const enPhaseMechant = PHASES_MECHANT.includes(monde.phase);

    if (enPhaseMechant) await surveillerLeCartouche(page, 400);

    if (enPhaseMechant && ask) {
      questionsVues += 1;
      console.log(
        `t${tick} phase=${monde.phase} ask=${ask.event_name}/${ask.ability_type} ` +
          `cartouche=${await page.locator('.deroule-phase').count()} ` +
          `classes=${await page.locator('.deroule-phase').first().getAttribute('class').catch(() => null)} ` +
          `dc=${await page.locator('.demande-centrale').count()}`
      );
      // La question est posée : l'écran doit la porter, bandeau et boutons.
      // ⚠ Délai généreux À DESSEIN : le client apprend la question par son
      // socket, après le moteur. Ce n'est pas ce délai que ce test garde —
      // c'est l'invariant ci-dessus.
      await expect(
        page.locator('.deroule-a-toi'),
        'le moteur pose une question et rien ne l’annonce'
      ).toBeVisible({ timeout: 15000 });
      const reponses = page.locator('.deroule-question-scene .af-action:visible');
      expect(
        await reponses.count(),
        'le moteur attend une réponse et aucun bouton ne permet de la donner'
      ).toBeGreaterThan(0);
      // Un seul panneau au centre, jamais deux (défaut n°2 du 14/09/2026).
      // ⚠ ON NE COMPTE QUE LES PANNEAUX DE PREMIER NIVEAU. En mode Détaillé,
      // la demande du moteur est IMBRIQUÉE dans le cartouche
      // (`.deroule-question-scene`) : c'est un seul panneau, pas deux qui se
      // recouvrent. Compter les nœuds à plat faisait échouer ce test sur un
      // écran parfaitement correct.
      const panneaux = await page.evaluate(() => {
        const tous = [
          ...document.querySelectorAll('.deroule-phase, .demande-centrale, .cibles-scene'),
        ].filter((e) => (e as HTMLElement).offsetParent !== null);
        return tous.filter((e) => !tous.some((autre) => autre !== e && autre.contains(e))).length;
      });
      expect(panneaux, `${panneaux} panneaux empilés au centre`).toBeLessThanOrEqual(1);

      if (/BeingAttack/i.test(String(ask.event_name))) {
        defensesVues += 1;
        await expect(
          page.getByRole('button', { name: /défendre/i }).first(),
          'la fenêtre de défense est ouverte sans bouton « Défendre »'
        ).toBeVisible();
        // La preuve à l'œil, à la demande : un moteur au vert ne dit rien du
        // rendu. CAPTURE_DEFENSE=<dossier> écrit l'écran de chaque fenêtre.
        if (process.env.CAPTURE_DEFENSE) {
          await page.screenshot({
            path: `${process.env.CAPTURE_DEFENSE}/defense-${defensesVues}.png`,
          });
        }
      }
    }

    // On avance comme un joueur : le bouton du cartouche, sinon « Passer ».
    const suivant = page.locator('.deroule-suivant');
    const passer = page.locator('.dc-pass');
    if ((await suivant.count()) > 0 && (await suivant.first().isVisible())) {
      await suivant.first().click();
      // ⚠ LA MESURE QUI COMPTE : c'est ce clic qui laisse passer les dégâts,
      // donc l'animation, donc la fenêtre où la question disparaissait.
      await surveillerLeCartouche(page, 2500);
    } else if ((await passer.count()) > 0 && (await passer.first().isVisible())) {
      await passer.first().click();
      await surveillerLeCartouche(page, 2500);
    } else if (ask && !enPhaseMechant) {
      // Le tour du héros ne nous intéresse pas : on le passe, SAUF la bascule
      // en identité héros — sans elle le méchant manigance au lieu d'attaquer,
      // et la fenêtre de défense n'arrive jamais.
      const options = optionsDe(ask) as Array<Record<string, string | number | number[]>>;
      const bascule = options.find((o) => /change_form/i.test(String(o.name ?? '')));
      if (bascule && !basculeFaite) {
        basculeFaite = true;
        await repondre(page, bascule as never);
      } else if (ask.show_cancel) {
        await repondre(page);
      } else if (options.length) {
        await repondre(page, options[0] as never);
      }
      await page.waitForTimeout(700);
    } else {
      await page.waitForTimeout(900);
    }
  }

  expect(questionsVues, 'aucune question du moteur pendant la phase du méchant').toBeGreaterThan(0);
  expect(
    defensesVues,
    'les deux fenêtres « Défendre / Passer » attendues n’ont pas été atteintes : ' +
      'sans la seconde, ce test ne garde rien (voir l’en-tête)'
  ).toBeGreaterThanOrEqual(DEFENSES_A_VOIR);
});
