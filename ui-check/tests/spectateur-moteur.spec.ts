// UN SPECTATEUR REGARDE, ET NE PEUT RIEN FAIRE D'AUTRE.
//
// ⚠ POURQUOI CE FICHIER EXISTE. Demande de l'utilisateur, 15/09/2026 : « c'est
// possible d'ajouter un truc qui me permet de voir en live les parties que les
// gens jouent actuellement ? », puis, interrogé : le plateau en vrai, toutes
// les mains visibles, lui seul, et « regarder seulement, rien de cliquable ».
//
// ⚠ ET LA GARANTIE N'EST PAS DANS LE NAVIGATEUR. Désarmer le plateau côté
// client est une politesse : un raccourci clavier, une console ouverte ou un
// `curl` en feraient le tour. Ce fichier mesure donc le MOTEUR, pas l'écran :
// il envoie de vraies requêtes d'action en spectateur et exige un refus.
//
// La mesure du 15/09/2026 qui a rendu ce test nécessaire : sans le témoin
// `spectateur`, `allowed_seats` accorde tout siège ORPHELIN à n'importe quel
// client authentifié (« reprise d'un siège abandonné »). Un spectateur arrivé
// pendant qu'un joueur s'est déconnecté héritait donc de sa place.
//
//   npm run spectateur-moteur
//
// ⚠ IL LANCE UNE NOUVELLE PARTIE sur le serveur visé : toute partie en cours
// y est perdue.
import { expect, test, request as apiRequest } from '@playwright/test';
import { avancerLaPartie, lancer, ouvrirEtMettreEnPlace, type Conduite } from '../pilote-campagne';
import { ADRESSE_JEU } from '../playwright.config';

const REGLES = ['v16_all', 'no_crisis_of_infinite_deadpools', 'no_encounter_cards_ignore_crisis'];
const CONDUITE: Conduite = { resterEnHeros: true };

test('⚠ le spectateur voit tout, et le moteur lui refuse tout', async ({ page, request }) => {
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

  // ⚠ UN CONTEXTE NEUF. Celui du test a mis la partie en place : s'en servir
  // ici mesurerait ses droits à lui, pas ceux d'un spectateur.
  const spectateur = await apiRequest.newContext({ baseURL: ADRESSE_JEU });

  // La porte : elle redirige vers le plateau et pose le témoin.
  const porte = await spectateur.get('/spectateur?p=1', { maxRedirects: 0 });
  expect(
    [302, 303, 307, 404].includes(porte.status()),
    `/spectateur a répondu ${porte.status()} : la route n’est pas en place`
  ).toBe(true);
  expect(porte.status(), '/spectateur devrait rediriger vers le plateau').not.toBe(404);
  expect(porte.headers()['location']).toContain('spectateur=1');
  // ⚠ ET SURTOUT : elle ne donne AUCUNE clé de siège.
  const poses = porte.headersArray().filter((h) => h.name.toLowerCase() === 'set-cookie');
  expect(
    poses.filter((h) => h.value.includes('seat_token')),
    'la porte du spectateur distribue une clé de siège : elle ne doit jamais le faire'
  ).toEqual([]);

  // Ce qu'il VOIT : les mains de tous les sièges, par les yeux de celui qu'il
  // demande. C'est la moitié de la demande (« oui, tout, je suis le proprio »).
  const mains: Record<string, number[]> = {};
  for (const siege of [0, 1]) {
    const monde = await (await spectateur.get(`/get_world?p=${siege}`)).json();
    mains[`p=${siege}`] = (monde.players ?? []).map(
      (j: { hand_cards?: unknown[] }) => (j.hand_cards ?? []).length
    );
    const nommees = (monde.players ?? []).every((j: { hand_cards?: Array<{ name?: string }> }) =>
      (j.hand_cards ?? []).every((c) => typeof c.name === 'string' && c.name.length > 0)
    );
    expect(nommees, `les cartes en main sont anonymes vues du siège ${siege}`).toBe(true);
  }
  expect(mains['p=0'].length, 'la partie de mesure doit avoir deux sièges').toBe(2);

  // ⚠ CE QU'IL NE PEUT PAS FAIRE, et c'est tout l'objet du test.
  for (const siege of [0, 1]) {
    const refus = await spectateur.post(`/post?p=${siege}`, { data: '' });
    expect(
      refus.status(),
      `le moteur a ACCEPTÉ une action du spectateur sur le siège ${siege} ` +
        `(HTTP ${refus.status()}) : il peut jouer à la place de quelqu’un`
    ).toBe(403);
  }

  // ⚠ LE TÉMOIN DE CONTRÔLE, et sans lui ce test ne prouverait rien. Le 403
  // ci-dessus pourrait venir d'autre chose (une requête mal formée, une route
  // absente). On envoie donc EXACTEMENT la même requête depuis un client qui
  // n'est PAS spectateur : si elle est refusée elle aussi, le refus ne dit
  // rien du spectateur.
  const ordinaire = await apiRequest.newContext({ baseURL: ADRESSE_JEU });
  const temoin = await ordinaire.post('/post?p=0', { data: '' });
  expect(
    temoin.status(),
    'un client ordinaire est refusé lui aussi : le 403 du spectateur ne prouve rien'
  ).not.toBe(403);
  await ordinaire.dispose();

  // Et le moteur ne lui pose aucune question : il n'a pas à y répondre.
  const demande = await (await spectateur.get('/get_ask?p=0')).json();
  expect(
    Object.keys(demande),
    'le moteur pose une question au spectateur : elle est destinée au joueur'
  ).toEqual([]);

  await spectateur.dispose();

  // ⚠ ET L'ÉCRAN, PAS SEULEMENT LE MOTEUR. Le plateau du spectateur doit dire
  // qu'on regarde, montrer la main du siège demandé, et ne proposer AUCUNE
  // action. Un navigateur neuf, comme plus haut.
  const navigateur = await page.context().browser()!.newContext({ baseURL: ADRESSE_JEU });
  const ecran = await navigateur.newPage();
  // ⚠ LE COMPTEUR SE POSE AVANT LE CHARGEMENT. `addInitScript` s'execute avant
  // tout script de la page : un compteur pose apres coup aurait manque le
  // socket ouvert au montage, c'est-a-dire exactement celui qu'on traque.
  await ecran.addInitScript(() => {
    const fenetre = window as unknown as { __socketsOuverts: number };
    fenetre.__socketsOuverts = 0;
    const Vrai = window.WebSocket;
    // @ts-expect-error on remplace volontairement le constructeur global
    window.WebSocket = function (...args: unknown[]) {
      fenetre.__socketsOuverts += 1;
      // @ts-expect-error appel du vrai constructeur
      return new Vrai(...args);
    };
  });
  // Tout ce que le plateau du spectateur DEMANDE au moteur : c'est cette liste
  // qui decide ce qu'on lui laisse, le reste etant ferme.
  const demandes = new Set<string>();
  ecran.on('request', (r) => {
    const u = new URL(r.url());
    if (u.origin === new URL(ADRESSE_JEU).origin) demandes.add(`${r.method()} ${u.pathname}`);
  });
  await ecran.goto('/spectateur?p=1');
  // ⚠ SURTOUT PAS `networkidle` : le spectateur INTERROGE le moteur toutes les
  // 700 ms (il n'a pas de socket, c'est tout l'objet du mode). Le reseau n'est
  // jamais au repos, et l'attente expire au bout de cinq minutes. Mesure du
  // 15/09/2026, a mes depens.
  await ecran.waitForSelector('.barre-spectateur', { timeout: 20000 });
  await ecran.waitForTimeout(2500);

  expect(ecran.url(), 'la porte n’a pas mené au plateau du siège demandé').toContain(
    'spectateur=1'
  );
  await expect(
    ecran.locator('.barre-spectateur'),
    'rien ne dit au spectateur qu’il regarde : un plateau sans boutons passe pour cassé'
  ).toBeVisible();

  // La main du siège 1, pas celle du siège 0 : c'est la promesse « je choisis
  // le siège, et je peux en changer ».
  const vues = await ecran.evaluate(() => {
    const visible = (e: Element) => (e as HTMLElement).offsetParent !== null;
    return {
      main: document.querySelectorAll('.zone-main .scan-card').length,
      // ⚠ « Annuler » EST LE CAS QUI COMPTE : il appelle `/debug?/undo auto` et
      // annulerait le coup de celui qu'on regarde. Découvert le 15/09/2026 en
      // REGARDANT la capture, pas en relisant le code.
      boutonsDeJeu: [...document.querySelectorAll('.board-actions button, .bouton-fin-tour')]
        .filter(visible)
        .map((b) => (b.textContent ?? '').trim()),
    };
  });
  expect(vues.main, 'le spectateur ne voit aucune main').toBeGreaterThan(0);
  expect(
    vues.boutonsDeJeu,
    'le plateau du spectateur propose encore des boutons qui agissent sur la partie'
  ).toEqual([]);

  // ⚠ ET LES PORTES DU MOTEUR SONT FERMÉES, pas seulement cachées. On les
  // frappe directement, comme le ferait une console ouverte.
  for (const route of ['/debug?/undo auto', '/set_language?en', '/new?data={}']) {
    const refus = await ecran.request.get(route);
    expect(
      refus.status(),
      `le moteur laisse un spectateur appeler ${route} (HTTP ${refus.status()})`
    ).toBe(403);
  }

  if (process.env.CAPTURE_SPECTATEUR) {
    await ecran.screenshot({ path: `${process.env.CAPTURE_SPECTATEUR}/spectateur.png` });
  }

  // ⚠ ET IL N'OUVRE AUCUN SOCKET : c'est ce qui le rend invisible. Mesuré le
  // 15/09/2026 : hors multijoueur le plateau s'annonce POUR TOUS LES SIÈGES,
  // et ferait croire au moteur qu'un joueur absent est connecté.
  const sockets = await ecran.evaluate(
    () => (window as unknown as { __socketsOuverts?: number }).__socketsOuverts ?? 0
  );
  expect(sockets, 'le spectateur a ouvert un socket : il s’annonce au moteur').toBe(0);

  console.log('DEMANDES DU SPECTATEUR ' + JSON.stringify([...demandes].sort(), null, 1));

  await ecran.close();
  await navigateur.close();
});
