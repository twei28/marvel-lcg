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
// ⚠ IL LANCE UNE NOUVELLE PARTIE sur le serveur visé, comme tout test qui
// importe `pilote-campagne` : toute partie en cours y est perdue.
import { expect, test, type Page } from '@playwright/test';
import {
  avancerLaPartie,
  lancer,
  monde,
  ouvrirEtMettreEnPlace,
  type Conduite,
} from '../pilote-campagne';

/** Les quatre phases du méchant, au sens du moteur (ui-app/src/board/moteur.ts). */
const PHASES_MECHANT = [
  'Main Scheme Place Threat',
  'Enemy Activation',
  'Deal Encounter Cards',
  'Reveal Encounter Cards',
];

/** Une partie ORDINAIRE, sans campagne (contrat-nouvelle-partie.json). */
const REGLES_STANDARD = [
  'v16_all',
  'no_crisis_of_infinite_deadpools',
  'no_encounter_cards_ignore_crisis',
];

/**
 * Le héros reste en forme HÉROS et frappe : sans cela le méchant MANIGANCE au
 * lieu d'attaquer, et la fenêtre de défense n'arrive jamais. Il ne se défend
 * pas (`seDefendre` absent) : c'est le choix courant d'un joueur, et surtout
 * c'est ce qui laisse les dégâts passer — donc l'animation, donc la fenêtre où
 * le défaut se produisait.
 */
const CONDUITE: Conduite = { resterEnHeros: true, attaquer: true };

/**
 * ⚠ LE MOUCHARD, ET C'EST LUI QUI GARDE LE DÉFAUT.
 *
 * Le cartouche REPLIÉ veut dire « le client SAIT que le moteur attend une
 * réponse ». En mode Détaillé, pendant la phase du méchant, cette branche ne
 * porte AUCUN bouton : la scène est le seul endroit où répondre. Tant qu'on ne
 * clique aucune carte (ce test n'en clique aucune), elle ne doit jamais
 * paraître.
 *
 * Il relève l'écran toutes les 50 ms DEPUIS LA PAGE, et non depuis le test :
 * le défaut ne durait que le temps d'une animation d'effet (1,7 s), et un
 * échantillonnage piloté depuis Node le manquait — mesuré le 14/09/2026,
 * ancienne règle remise, test au vert à tort.
 *
 * Il ne lit QUE l'état du client, jamais celui du moteur : aucun délai de
 * propagation ne peut le rendre instable.
 */
async function poserLeMouchard(page: Page) {
  await page.evaluate(() => {
    const fenetre = window as unknown as { __replis?: string[]; __mouchard?: number };
    fenetre.__replis = [];
    if (fenetre.__mouchard !== undefined) window.clearInterval(fenetre.__mouchard);
    fenetre.__mouchard = window.setInterval(() => {
      const replie = document.querySelector('.deroule-phase.est-replie');
      if (replie) {
        fenetre.__replis!.push((replie as HTMLElement).innerText.replace(/\s+/g, ' ').slice(0, 120));
      }
    }, 50);
  });
}

const replisReleves = (page: Page): Promise<string[]> =>
  page.evaluate(() => (window as unknown as { __replis?: string[] }).__replis ?? []);

test('⚠ en mode Détaillé, on sait TOUJOURS quand on peut défendre', async ({ page, request }) => {
  // Une partie réelle jusqu'aux attaques : lent PAR NATURE.
  test.setTimeout(300000);

  await lancer(request, {
    scenario: 'rhino',
    heros: ['spider_man'],
    regles: REGLES_STANDARD,
    seed: 1234,
  });

  // Les réglages AVANT d'ouvrir le plateau : il les lit à son montage.
  await page.goto('/main.html');
  await page.evaluate(() => {
    localStorage.setItem('marvel-langue-choisie', '1');
    // LE MODE QUI NOUS INTÉRESSE, écrit explicitement : c'est le défaut du
    // jeu, mais un test ne doit pas dépendre d'un défaut.
    localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille');
    localStorage.setItem('marvel-board-avance-auto', 'off');
  });

  await ouvrirEtMettreEnPlace(page, request);
  await poserLeMouchard(page);

  // ⚠ DEUX FENÊTRES DE DÉFENSE, PAS UNE. C'est la SECONDE qui porte le défaut :
  // elle arrive pendant que l'animation des dégâts de la première est encore à
  // l'écran. Un test qui s'arrêtait à la première passait au vert sur le code
  // défectueux — vérifié le 14/09/2026 en remettant l'ancienne règle.
  const DEFENSES_A_VOIR = 2;
  let defensesVues = 0;
  /** Le survol d'un nom ne s'éprouve qu'une fois : il ne dépend pas de l'étape. */
  let nomEprouve = false;

  // ⚠ LE TOUR DU HÉROS SE JOUE PAR LE PILOTE, LA PHASE DU MÉCHANT PAR L'ÉCRAN.
  // En mode Détaillé, la phase n'avance QUE sur le clic « Suivant » du joueur :
  // le cartouche retient la trame du moteur tant qu'il ne l'a pas eu. Un pilote
  // qui ne répond qu'en HTTP reste donc bloqué au premier temps de la phase —
  // mesuré le 14/09/2026, une seule fenêtre de défense atteinte au lieu de deux.
  for (let tour = 0; tour < 200 && defensesVues < DEFENSES_A_VOIR; tour += 1) {
    const suivant = page.locator('.deroule-suivant');
    const defendre = page.getByRole('button', { name: /défendre/i }).first();
    const passer = page.getByRole('button', { name: /^passer$/i }).first();

    if (await defendre.count()) {
      defensesVues += 1;

      // La question est posée : l'écran doit la porter, bandeau ET boutons.
      await expect(
        page.locator('.deroule-a-toi'),
        'le moteur demande « Défendre / Passer » et rien ne l’annonce'
      ).toBeVisible();
      await expect(passer, 'fenêtre de défense sans bouton « Passer »').toBeVisible();

      // Un seul panneau au centre, jamais deux (défaut n°2 du 14/09/2026).
      // ⚠ ON NE COMPTE QUE LES PANNEAUX DE PREMIER NIVEAU : en mode Détaillé, la
      // demande du moteur est IMBRIQUÉE dans le cartouche
      // (`.deroule-question-scene`). C'est un seul panneau, pas deux qui se
      // recouvrent — compter les nœuds à plat faisait échouer ce test sur un
      // écran parfaitement correct.
      const panneaux = await page.evaluate(() => {
        const tous = [
          ...document.querySelectorAll('.deroule-phase, .demande-centrale, .cibles-scene'),
        ].filter((e) => (e as HTMLElement).offsetParent !== null);
        return tous.filter((e) => !tous.some((autre) => autre !== e && autre.contains(e))).length;
      });
      expect(panneaux, `${panneaux} panneaux empilés au centre`).toBeLessThanOrEqual(1);

      // ⚠ LE CARTOUCHE TIENT DANS L'ÉCRAN. Mesuré le 15/09/2026 en 1920×1080 :
    // `top: -44px`, le haut du panneau (la chronologie MENACE / MÉCHANT /
    // SBIRES…) était coupé par le bord de l'écran. Deux causes cumulées, dans
    // `board.css` : la variante « est-question » remonte le bord bas à 34vh
    // alors que la hauteur maximale en supposait 31, et la boîte est en
    // content-box, donc padding et bordures s'ajoutent à cette hauteur.
    const boite = await page.evaluate(() => {
      const e = document.querySelector('.deroule-phase') as HTMLElement | null;
      if (!e) return null;
      const r = e.getBoundingClientRect();
      return { haut: Math.round(r.top), bas: Math.round(r.bottom), ecran: window.innerHeight };
    });
    expect(boite, 'aucun cartouche à mesurer').not.toBeNull();
    expect(
      boite!.haut,
      `le cartouche sort de l'écran par le HAUT (top ${boite!.haut}px) : son début est coupé`
    ).toBeGreaterThanOrEqual(0);
    expect(
      boite!.bas,
      `le cartouche sort de l'écran par le BAS (${boite!.bas}px pour ${boite!.ecran}px)`
    ).toBeLessThanOrEqual(boite!.ecran);

    // ⚠ ET IL NE DÉFILE JAMAIS, À AUCUNE TAILLE DE FENÊTRE.
    //
    // Signalé le 15/09/2026, capture à l'appui, dans une fenêtre de 1009×663 :
    // « on doit scroll putain, je t'ai dit que je voulais jamais scroll ». Le
    // cartouche TENAIT dans l'écran (les deux mesures ci-dessus passaient) mais
    // son CONTENU débordait et une barre de défilement apparaissait dedans.
    //
    // ⚠ PUIS J'AI CORRIGÉ LA PETITE FENÊTRE ET LAISSÉ LA GRANDE CASSÉE, parce
    // que la règle était bornée à 800 px de haut. Signalé en partie, à juste
    // titre : « tu te fous vraiment de ma gueule en fait ??? ». Mesurer une
    // seule taille ne prouve rien.
    //
    // D'où cette liste, arrêtée avec lui le 15/09/2026 (« une mesure à
    // plusieurs tailles de fenêtre », puis « les mêmes, plus un très grand
    // écran ») : son écran, un très grand écran, un portable ordinaire, la
    // fenêtre exacte de sa capture, et un plancher serré.
    const TAILLES = [
      { width: 1920, height: 1080 },
      { width: 2560, height: 1440 },
      { width: 1280, height: 800 },
      { width: 1009, height: 663 },
      { width: 1000, height: 600 },
    ];
    const AVANT = page.viewportSize();
    for (const taille of TAILLES) {
      await page.setViewportSize(taille);
      await page.waitForTimeout(300);
      const mesure = await page.evaluate(() => {
        const e = document.querySelector('.deroule-phase') as HTMLElement | null;
        if (!e) return null;
        // Le détail par enfant : quand ça défile, il faut savoir CE QUI prend
        // la place, sinon on règle au hasard. On descend tant que le bloc est
        // gros : savoir QUE ça déborde ne sert à rien, il faut savoir QUOI.
        const h = (c: Element) => Math.round((c as HTMLElement).getBoundingClientRect().height);
        const l = (c: Element) => Math.round((c as HTMLElement).getBoundingClientRect().width);
        const decrire = (c: Element, reste: number): string => {
          const nom = `${String(c.className || c.tagName).split(' ')[0]}|${l(c)}w`;
          const enfants = [...c.children];
          const dedans =
            reste > 0 && enfants.length > 0 && h(c) > 80
              ? '(' + enfants.map((x) => decrire(x, reste - 1)).join(' ') + ')'
              : '';
          return `${nom}=${h(c)}${dedans}`;
        };
        const r = e.getBoundingClientRect();
        return {
          contenu: e.scrollHeight,
          visible: e.clientHeight,
          haut: Math.round(r.top),
          bas: Math.round(r.bottom),
          largeur: window.innerWidth,
          hauteur: window.innerHeight,
          detail: [...e.children].map((c) => decrire(c, 4)).join(' '),
        };
      });
      expect(mesure, `aucun cartouche à mesurer en ${taille.width}×${taille.height}`).not.toBeNull();
      // La preuve à l'œil, à chaque taille, quand on la demande.
      if (process.env.CAPTURE_PETITE) {
        await page.screenshot({
          path: `${process.env.CAPTURE_PETITE}/${taille.width}x${taille.height}-${defensesVues}.png`,
        });
      }
      expect.soft(
        mesure!.contenu,
        `le cartouche DÉFILE en ${mesure!.largeur}×${mesure!.hauteur} : ` +
          `${mesure!.contenu}px de contenu pour ${mesure!.visible}px visibles` +
          ` — par enfant : ${mesure!.detail}`
      ).toBeLessThanOrEqual(mesure!.visible + 1);
      // Et il reste dans l'écran, à cette taille-là aussi : un cartouche qui ne
      // défile pas mais dont le haut est coupé ne vaut pas mieux.
      expect.soft(
        mesure!.haut,
        `le cartouche sort de l'écran par le HAUT en ${mesure!.largeur}×${mesure!.hauteur} ` +
          `(top ${mesure!.haut}px) — par enfant : ${mesure!.detail}`
      ).toBeGreaterThanOrEqual(0);
      expect.soft(
        mesure!.bas,
        `le cartouche sort de l'écran par le BAS en ${mesure!.largeur}×${mesure!.hauteur} ` +
          `(${mesure!.bas}px pour ${mesure!.hauteur}px)`
      ).toBeLessThanOrEqual(mesure!.hauteur);
    }
    if (AVANT) await page.setViewportSize(AVANT);
    await page.waitForTimeout(200);

    // La preuve à l'œil, à la demande : un moteur au vert ne dit rien du rendu.
      if (process.env.CAPTURE_DEFENSE) {
        await page.screenshot({
          path: `${process.env.CAPTURE_DEFENSE}/defense-${defensesVues}.png`,
        });
      }

      // On PASSE, comme un joueur qui encaisse : les dégâts tombent, l'animation
      // démarre, et c'est pendant elle que l'ennemi suivant attaque.
      await passer.click();
      await page.waitForTimeout(1200);
      continue;
    }

    // ⚠ AU PASSAGE, LE DÉFAUT N°5 : « Maîtres du Chaos révèle Maîtres du
    // Chaos », signalé DEUX FOIS le 14/09/2026. Sur une révélation, `carteId`
    // désigne la carte RÉVÉLÉE ; traduire l'auteur avec lui écrivait le nom de
    // la carte des deux côtés de la phrase. On le regarde ici parce que la
    // révélation tombe dans cette même phase, à deux clics de la défense.
    // ⚠ `count()` D'ABORD, TOUJOURS. `innerText()` sur un élément absent ATTEND
    // cinq secondes avant d'échouer, et le `.catch()` masque cette attente : à
    // deux cents tours de boucle, un test de treize secondes en mettait cinq
    // minutes. Mesuré le 14/09/2026, et c'est ce qui a fait abandonner un
    // premier test en vraie partie.
    const bloc = page.locator('.deroule-titre').first();
    const titre = (await bloc.count()) ? await bloc.innerText() : '';
    const revele = /^(.+?)\s+RÉVÈLE\s+(.+)$/i.exec(titre.replace(/\s+/g, ' ').trim());
    if (revele) {
      expect(
        revele[1].trim().toLowerCase(),
        `« ${titre.trim()} » : le héros qui révèle porte le nom de la carte révélée ` +
          `(défaut n°5, voir DeroulePhase.tsx, auteurNom)`
      ).not.toBe(revele[2].trim().toLowerCase());
    }

    // ⚠ LE SURVOL D'UN NOM OUVRE SA CARTE, ET LA REFERME QUAND ON S'EN VA.
    //
    // C'est ce qui REMPLACE les cartes de l'etape depuis le 15/09/2026 : « il
    // n'y a pas besoin de montrer les cartes ; par contre, quand on hover sur
    // le nom, on voit la carte en question ». Si ce geste ne marche pas, la
    // refonte a retire quelque chose sans rien rendre — on le verifie donc en
    // vraie partie, une fois, sur le premier nom rencontre.
    if (!nomEprouve && (await page.locator('.deroule-nom').count())) {
      nomEprouve = true;
      const nom = page.locator('.deroule-nom').first();
      await nom.hover();
      await expect(
        page.locator('.carte-apercu'),
        'survoler un nom de carte n’ouvre pas la carte en grand'
      ).toBeVisible();
      if (process.env.CAPTURE_PETITE) {
        await page.screenshot({ path: `${process.env.CAPTURE_PETITE}/nom-survole.png` });
      }
      // « Dès que le curseur quitte le nom » : on s'en va, et rien ne reste.
      await page.mouse.move(4, 4);
      await expect(
        page.locator('.carte-apercu'),
        'la carte reste ouverte alors que le curseur a quitté le nom'
      ).toBeHidden();
    }

    if ((await suivant.count()) && (await suivant.first().isVisible())) {
      await suivant.first().click();
      await page.waitForTimeout(500);
      continue;
    }

    const m = await monde(request);
    if (PHASES_MECHANT.includes(String(m.phase))) {
      // Une question de la phase du méchant qui n'est pas une défense (une
      // interruption, un ciblage) : on la passe par l'écran quand on peut.
      if ((await passer.count()) && (await passer.first().isVisible())) {
        await passer.first().click();
        await page.waitForTimeout(500);
      } else {
        await page.waitForTimeout(400);
      }
      continue;
    }

    // Hors phase du méchant : le pilote joue le tour du héros et s'arrête dès
    // que la phase du méchant reprend.
    await avancerLaPartie(
      page,
      request,
      ({ monde: courant }) => PHASES_MECHANT.includes(String(courant.phase)),
      40,
      CONDUITE
    );
  }

  expect(
    nomEprouve,
    'aucun nom de carte survolable n’est apparu de toute la phase : le cartouche ne ' +
      'montre plus les cartes de l’étape, il DOIT montrer leurs noms (15/09/2026)'
  ).toBe(true);

  expect(
    defensesVues,
    'les deux fenêtres « Défendre / Passer » attendues n’ont pas été atteintes : ' +
      'sans la seconde, ce test ne garde rien (voir l’en-tête)'
  ).toBeGreaterThanOrEqual(DEFENSES_A_VOIR);

  const replis = await replisReleves(page);
  expect(
    replis,
    'le cartouche s’est replié SANS BOUTON pendant que le moteur attendait une réponse : ' +
      'c’est exactement le défaut du 14/09/2026 (voir ou-va-la-question.ts)'
  ).toEqual([]);
});
