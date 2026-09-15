// LA MAIN D'UN JOUEUR NE SORT PAS DU MOTEUR POUR LES AUTRES.
//
// ⚠ POURQUOI CE FICHIER EXISTE. Mesure du 15/09/2026, en partie à deux héros :
// `/get_world` rendait à n'importe quel client la main de TOUS les joueurs, nom
// des cartes compris, et l'ordre complet du deck rencontre (32 cartes nommées,
// face cachée). Le plateau cachait déjà tout cela à l'écran (`isVisibleFor`,
// world.ts) : la règle existait côté client, et seulement là. Un `curl` en
// faisait le tour, et un joueur invité connaît le mot de passe de la table.
//
// Demande de l'utilisateur, le même jour : « ce n'est que moi qui doit pouvoir
// voir les autres ».
//
// ⚠ CE QUE CE TEST DOIT PROUVER, C'EST LES DEUX CÔTÉS À LA FOIS :
//   — un JOUEUR ne voit ni la main de l'autre, ni le deck rencontre ;
//   — il voit parfaitement la sienne, et toute la table.
// Sans le second, on saurait masquer et pas jouer.
//
//   npm run mains-privees
//
// ⚠ IL LANCE UNE NOUVELLE PARTIE sur le serveur visé : toute partie en cours
// y est perdue.
import { expect, test, request as apiRequest } from '@playwright/test';
import { avancerLaPartie, lancer, ouvrirEtMettreEnPlace, type Conduite } from '../pilote-campagne';
import { ADRESSE_JEU } from '../playwright.config';

const REGLES = ['v16_all', 'no_crisis_of_infinite_deadpools', 'no_encounter_cards_ignore_crisis'];
const CONDUITE: Conduite = { resterEnHeros: true };

type Carte = { name?: string; visible_for_players?: number[] };

/** Toutes les cartes du descripteur, où qu'elles soient rangées. */
function cartes(noeud: unknown): Carte[] {
  if (Array.isArray(noeud)) return noeud.flatMap(cartes);
  if (noeud && typeof noeud === 'object') {
    const objet = noeud as Record<string, unknown>;
    const ici = 'visible_for_players' in objet && 'name' in objet ? [objet as Carte] : [];
    return [...ici, ...Object.values(objet).flatMap(cartes)];
  }
  return [];
}

const nommees = (liste: Carte[]) => liste.filter((c) => (c.name ?? '') !== '');

test('⚠ un joueur ne voit pas la main des autres, ni le deck rencontre', async ({
  page,
  request,
}) => {
  test.setTimeout(300000);

  await lancer(request, {
    scenario: 'rhino',
    heros: ['spider_man', 'captain_america'],
    regles: REGLES,
    seed: 4242,
  });

  await page.goto('/main.html');
  await page.evaluate(() => localStorage.setItem('marvel-langue-choisie', '1'));
  await ouvrirEtMettreEnPlace(page, request);
  await avancerLaPartie(page, request, ({ monde: m }) => String(m.phase).includes('Turn'), 30, CONDUITE);

  // ⚠ CE TEST NE VAUT QUE SUR UNE TABLE PROTÉGÉE PAR DES CLÉS DE SIÈGE.
  // Une partie locale ouverte ne masque rien, volontairement : c'est la même
  // personne qui joue les deux héros sur un écran. Le serveur de dev sait
  // reproduire une table de production :
  //
  //   python3 ui-check/scripts/serveur-dev.py --port 2346 --sieges-proteges
  //   UI_CHECK_BASE=http://127.0.0.1:2346 npm run mains-privees
  //
  // Sans cela on passerait au vert en ne mesurant rien, et c'est le pire des
  // tests. On le DIT donc, et on s'arrête.
  const anonyme = await apiRequest.newContext({ baseURL: ADRESSE_JEU });
  const tel_quel = await (await anonyme.get('/get_world?p=0')).json();
  const toutes = cartes(tel_quel);
  expect(toutes.length, 'aucune carte à mesurer : la partie n’est pas montée').toBeGreaterThan(20);
  const protegee = nommees(toutes).length === 0;
  await anonyme.dispose();
  test.skip(
    !protegee,
    'table sans clés de siège : relance le serveur avec --sieges-proteges (voir l’en-tête)'
  );

  // LE JOUEUR DU SIÈGE 0, tel qu'il arrive vraiment : par son lien personnel,
  // qui lui pose son cookie de siège.
  const joueur0 = await apiRequest.newContext({ baseURL: ADRESSE_JEU });
  await joueur0.get('/claim_seat?p=0&key=cle-0');
  const vu = cartes(await (await joueur0.get('/get_world?p=0')).json());

  const sienne = nommees(vu.filter((c) => (c.visible_for_players ?? []).includes(0)));
  const autres = nommees(vu.filter((c) => !(c.visible_for_players ?? []).includes(0)));

  // ⚠ LES DEUX MOITIÉS COMPTENT AUTANT. Sans la première on ne masque rien ;
  // sans la seconde on a masqué la partie elle-même.
  expect(
    autres.map((c) => c.name),
    'des cartes que le siège 0 n’a pas le droit de voir sortent NOMMÉES du moteur'
  ).toEqual([]);
  expect(
    sienne.length,
    'le siège 0 ne voit plus ni sa main ni la table : le masquage est allé trop loin'
  ).toBeGreaterThan(5);

  // Et le SPECTATEUR, lui, voit tout : c'est le sens de la demande
  // (« ce n'est que moi qui doit pouvoir voir les autres »).
  const spectateur = await apiRequest.newContext({ baseURL: ADRESSE_JEU });
  await spectateur.get('/spectateur?p=0');
  const vuSpectateur = cartes(await (await spectateur.get('/get_world?p=0')).json());
  const mainsDesAutres = nommees(
    vuSpectateur.filter((c) => (c.visible_for_players ?? []).length > 0 && !(c.visible_for_players ?? []).includes(0))
  );
  expect(
    mainsDesAutres.length,
    'le spectateur ne voit plus la main des autres : le masquage l’a pris pour un joueur'
  ).toBeGreaterThan(0);

  await joueur0.dispose();
  await spectateur.dispose();
});
