// UNE PARTIE EN FRANÇAIS EST-ELLE VRAIMENT EN FRANÇAIS, DE BOUT EN BOUT ?
//
// ⚠ POURQUOI CE FICHIER EXISTE. Constat de l'utilisateur, 15/09/2026 :
// « j'ai remarqué que quand je joue en français, le texte est encore et
// toujours en anglais », puis, quand je lui ai demandé QUOI exactement :
// « quand je joue en français tout doit être en français, je comprends pas que
// tu me poses encore la question ».
//
// Il a raison de ne pas vouloir répondre : c'est à la mesure de le dire, pas à
// lui. Ce fichier est donc le miroir de `site-en-anglais.spec.ts` — celui-là
// vérifie que le SITE se traduit en anglais, celui-ci que la PARTIE ne retombe
// jamais en anglais.
//
// ⚠ CE QU'IL NE PEUT PAS VOIR. Un nom de carte anglais sans mot repère
// (« Rhino », « Klaw ») passe au travers : aucune mesure de texte ne peut
// deviner qu'il existait une traduction. Ce filet attrape les PHRASES et les
// libellés, c'est-à-dire l'essentiel de ce qu'on lit.
//
//   npm run partie-en-francais
//
// ⚠ IL LANCE UNE NOUVELLE PARTIE sur le serveur visé, comme tout test qui
// importe `pilote-campagne` : toute partie en cours y est perdue.
import { expect, test, type Page } from '@playwright/test';
import { avancerLaPartie, lancer, monde, ouvrirEtMettreEnPlace, type Conduite } from '../pilote-campagne';

const PHASES_MECHANT = [
  'Main Scheme Place Threat',
  'Enemy Activation',
  'Deal Encounter Cards',
  'Reveal Encounter Cards',
];

const REGLES_STANDARD = [
  'v16_all',
  'no_crisis_of_infinite_deadpools',
  'no_encounter_cards_ignore_crisis',
];

const CONDUITE: Conduite = { resterEnHeros: true, attaquer: true };

/**
 * LES MOTS QUI TRAHISSENT L'ANGLAIS, et rien qu'eux.
 *
 * ⚠ CHAQUE MOT DE CETTE LISTE A ÉTÉ CHOISI POUR NE PAS EXISTER EN FRANÇAIS.
 * « place », « menu », « boost », « round », « stade » sont volontairement
 * ABSENTS : le jeu les emploie en français, et les inscrire ici rendrait la
 * mesure rouge sur un écran parfaitement traduit. Une gate qui crie à tort
 * finit ignorée, ce qui est pire que pas de gate.
 */
const MOTS_ANGLAIS = [
  'the', 'and', 'with', 'your', 'you', 'this', 'that', 'when', 'while', 'each',
  'card', 'cards', 'draw', 'discard', 'damage', 'threat', 'minion', 'minions',
  'villain', 'scheme', 'schemes', 'hero', 'heroes', 'player', 'players',
  'ready', 'exhaust', 'exhausted', 'attack', 'attacks', 'attacking', 'defend',
  'defense', 'encounter', 'response', 'forced', 'reveal', 'revealed',
  'remove', 'next', 'save', 'close', 'cancel', 'confirm', 'settings',
  'deal', 'deals', 'choose', 'target', 'targets', 'during', 'instead',
];

const MOTIF = new RegExp(`\\b(${MOTS_ANGLAIS.join('|')})\\b`, 'i');

/**
 * Tout ce qu'un joueur LIT à l'écran, un élément par ligne.
 *
 * ⚠ ON NE LIT QUE LES FEUILLES. `innerText` d'un conteneur rend le texte de
 * tous ses enfants : relever le plateau entier aurait donné une seule chaîne
 * de dix mille caractères, impossible à imputer à un coupable. On descend donc
 * jusqu'aux éléments qui portent leur propre texte.
 *
 * ⚠ ET ON IGNORE LES IMAGES DE CARTES. Un scan anglais est un défaut d'IMAGE
 * (assets/pics-fr), pas de texte : il se traite ailleurs, et son `alt` n'est
 * pas ce que le joueur lit.
 */
async function textesVisibles(page: Page): Promise<string[]> {
  return page.evaluate(() => {
    const vus: string[] = [];
    const visible = (e: Element) => {
      const r = e.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return false;
      const style = window.getComputedStyle(e);
      return style.visibility !== 'hidden' && style.opacity !== '0';
    };
    document.querySelectorAll('body *').forEach((e) => {
      if (e.closest('.scan-card, script, style')) return;
      const propre = [...e.childNodes]
        .filter((n) => n.nodeType === Node.TEXT_NODE)
        .map((n) => n.textContent ?? '')
        .join(' ')
        .replace(/\s+/g, ' ')
        .trim();
      if (!propre || !visible(e)) return;
      // Le chemin depuis la racine : « qui affiche ça » est la moitié de la
      // correction, et une classe seule ne le dit pas.
      const chemin: string[] = [];
      for (let p: Element | null = e; p && chemin.length < 4; p = p.parentElement) {
        chemin.unshift(String(p.className || p.tagName).split(' ')[0]);
      }
      vus.push(`${chemin.join('>')} :: ${propre}`);
    });
    return vus;
  });
}

const enAnglais = (lignes: string[]) =>
  [...new Set(lignes.filter((l) => MOTIF.test(l.split(' :: ').slice(1).join(' ')))) ];

test('⚠ une partie en français ne montre pas un mot d’anglais', async ({ page, request }) => {
  test.setTimeout(300000);

  await lancer(request, {
    scenario: 'rhino',
    heros: ['spider_man'],
    regles: REGLES_STANDARD,
    seed: 1234,
  });

  await page.goto('/main.html');
  await page.evaluate(() => {
    localStorage.setItem('marvel-langue-choisie', '1');
    localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille');
    localStorage.setItem('marvel-board-avance-auto', 'off');
  });

  await ouvrirEtMettreEnPlace(page, request);

  /** Tout ce qu'on a relevé, tour après tour : le verdict est pris à la fin. */
  const fautes: string[] = [];
  const noter = async () => {
    for (const ligne of enAnglais(await textesVisibles(page))) {
      if (!fautes.includes(ligne)) fautes.push(ligne);
    }
  };

  await noter();

  // On traverse une phase du méchant entière, en relevant à chaque étape :
  // c'est là que le plateau compose le plus de phrases lui-même.
  for (let tour = 0; tour < 60; tour += 1) {
    await noter();
    const suivant = page.locator('.deroule-suivant');
    const passer = page.getByRole('button', { name: /^passer$/i }).first();

    if ((await suivant.count()) && (await suivant.first().isVisible())) {
      await suivant.first().click();
      await page.waitForTimeout(400);
      continue;
    }

    const m = await monde(request);
    if (PHASES_MECHANT.includes(String(m.phase))) {
      if ((await passer.count()) && (await passer.first().isVisible())) {
        await passer.first().click();
        await page.waitForTimeout(400);
      } else {
        await page.waitForTimeout(300);
      }
      continue;
    }

    if (tour > 4) break;
    await avancerLaPartie(
      page,
      request,
      ({ monde: courant }) => PHASES_MECHANT.includes(String(courant.phase)),
      40,
      CONDUITE
    );
  }

  await noter();

  expect(
    fautes,
    `du texte ANGLAIS s’affiche dans une partie en français :\n  ${fautes.join('\n  ')}`
  ).toEqual([]);
});
