// Les REGLES du mode Legacy, eprouvees sur des donnees fabriquees.
//
// `public/js/prepare/legacy.js` ne lit ni reseau, ni stockage, ni catalogue :
// on lui passe tout, il repond. Ce fichier lui passe des cas choisis et verifie
// ce qu'il rend. Il tourne DANS LA PAGE (import dynamique), faute de harnais
// unitaire pour les modules de l'assistant : c'est le vrai module, pas une
// copie.
//
//   npm run legacy
import { test, expect, type Page } from '@playwright/test';

/** Appelle une fonction du VRAI module, dans la page. */
async function regle(page: Page, nom: string, args: unknown[]) {
  return page.evaluate(async ({ nom, args }) => {
    const mod: Record<string, (...a: unknown[]) => unknown> =
      await import('/js/prepare/legacy.js');
    const sortie = mod[nom](...(args as unknown[]));
    // Les Set ne traversent pas `evaluate` : on les rend en tableaux tries.
    return JSON.parse(JSON.stringify(sortie, (_c, v) =>
      v instanceof Set ? [...v].sort() : v));
  }, { nom, args });
}

test.beforeEach(async ({ page }) => {
  await page.goto('/prepare.html');
});

// Trois paliers de poche : la boite de base, une boite sans heros (le cas du
// Bouffon Vert), une boite sans scenario.
const PALIERS = [
  { vague: 0, nom: 'Set de base',
    scenarios: [{ id: 'rhino', nom: 'Rhino' }, { id: 'klaw', nom: 'Klaw' }],
    heros: [{ id: '01001a', nom: 'Spider-Man' }, { id: '01010a', nom: 'Captain Marvel' }] },
  { vague: 1, nom: 'Vague 1',
    scenarios: [{ id: 'goblin', nom: 'Green Goblin' }], heros: [] },
  { vague: 2, nom: 'The Rise of Red Skull',
    scenarios: [], heros: [{ id: '06001a', nom: 'Thor' }] },
];

function victoire(scenario: string, heros: string[], extra: object = {}) {
  return { time: 1000, scenario, won: true, expert: false,
           heroes: heros.map((id) => ({ card_id: id })), ...extra };
}

test('le nom d un scenario se compare sans casse ni accent', async ({ page }) => {
  expect(await regle(page, 'cleNom', ['  Le Bouffon   VERT '])).toBe('le bouffon vert');
  expect(await regle(page, 'cleNom', ['Crâne Rouge'])).toBe('crane rouge');
  expect(await regle(page, 'cleNom', [null])).toBe('');
});

test('au depart, seul le Set de base est ouvert', async ({ page }) => {
  const p = await regle(page, 'parcours', [PALIERS, []]) as any;
  expect(p.etapes.map((e: any) => e.ouvert)).toEqual([true, false, false]);
  expect(p.vagueOuverte).toBe(0);
  expect(p.jetons).toEqual({ gagnes: 0, depenses: 0, restants: 0 });
});

test('il faut TOUS les vilains ET TOUS les heros de la vague', async ({ page }) => {
  // Les deux vilains battus, un seul heros vainqueur : la marche ne passe pas.
  const presque = [victoire('Rhino', ['01001a']), victoire('Klaw', ['01001a'])];
  const p = await regle(page, 'parcours', [PALIERS, presque]) as any;
  expect(p.etapes[0].franchi).toBe(false);
  expect(p.etapes[0].herosRestants.map((h: any) => h.nom)).toEqual(['Captain Marvel']);
  expect(p.etapes[1].ouvert).toBe(false);
});

// ⚠ UNE VICTOIRE A PLUSIEURS COCHE TOUS LES HEROS DE LA TABLE. Fidele au jeu
// de plateau, et c'est ce qui recompense de jouer a plusieurs.
test('une victoire en coop coche tous les heros de la table', async ({ page }) => {
  const coop = [victoire('Rhino', ['01001a', '01010a']), victoire('Klaw', ['01001a'])];
  const p = await regle(page, 'parcours', [PALIERS, coop]) as any;
  expect(p.etapes[0].franchi).toBe(true);
  expect(p.etapes[1].ouvert).toBe(true);
  expect(p.vagueOuverte).toBe(1);
});

// ⚠ UNE LISTE VIDE NE BLOQUE RIEN. La boite du Bouffon Vert apporte deux
// scenarios et zero heros. Sans cette tolerance, elle fermait la route pour
// toujours.
test('une vague sans heros s ouvre sur ses seuls vilains', async ({ page }) => {
  const jusquAuGobelin = [
    victoire('Rhino', ['01001a', '01010a']), victoire('Klaw', ['01001a']),
    victoire('Green Goblin', ['01001a']),
  ];
  const p = await regle(page, 'parcours', [PALIERS, jusquAuGobelin]) as any;
  expect(p.etapes[1].franchi).toBe(true);
  expect(p.etapes[2].ouvert).toBe(true);
  // Et la vague 2 n'a pas de scenario : seul Thor la ferme.
  expect(p.etapes[2].vilainsRestants).toEqual([]);
  expect(p.etapes[2].herosRestants.map((h: any) => h.nom)).toEqual(['Thor']);
});

// ⚠ LES PALIERS S'OUVRENT DANS L'ORDRE. Quelqu'un qui avait deja gagne avec
// Thor avant d'activer le mode ne saute pas les deux premieres boites : sans
// cette barriere, le mode n'aurait plus de parcours du tout.
test('un palier lointain deja rempli n ouvre pas la route', async ({ page }) => {
  const p = await regle(page, 'parcours', [PALIERS, [victoire('Peu importe', ['06001a'])]]) as any;
  expect(p.etapes[2].ouvert).toBe(false);
  expect(p.etapes[2].franchi).toBe(false);
  expect(p.vagueOuverte).toBe(0);
});

test('la premiere victoire d un heros officiel donne un jeton', async ({ page }) => {
  const p = await regle(page, 'parcours', [PALIERS, [victoire('Rhino', ['01001a'])]]) as any;
  expect(p.jetons.gagnes).toBe(1);
  // Rejouer le meme heros ne rapporte rien de plus.
  const deux = [victoire('Rhino', ['01001a']), victoire('Klaw', ['01001a'])];
  expect(((await regle(page, 'parcours', [PALIERS, deux])) as any).jetons.gagnes).toBe(1);
});

test('en expert, cette premiere victoire en rapporte deux', async ({ page }) => {
  const dur = [victoire('Rhino', ['01001a'], { expert: true })];
  expect(((await regle(page, 'parcours', [PALIERS, dur])) as any).jetons.gagnes).toBe(2);
});

// ⚠ LE BONUS SE DECIDE A LA PREMIERE VICTOIRE, ET UNE SEULE FOIS. Sinon il
// suffisait de rejouer en expert un heros deja valide pour battre monnaie.
test('rejouer en expert un heros deja gagnant ne rapporte rien', async ({ page }) => {
  const apres = [victoire('Rhino', ['01001a']), victoire('Klaw', ['01001a'], { expert: true })];
  expect(((await regle(page, 'parcours', [PALIERS, apres])) as any).jetons.gagnes).toBe(1);
});

test('les jetons depenses se retranchent', async ({ page }) => {
  const deux = [victoire('Rhino', ['01001a']), victoire('Klaw', ['01010a'])];
  const p = await regle(page, 'parcours',
    [PALIERS, deux, { jetonsDepenses: ['nt001a'] }]) as any;
  expect(p.jetons).toEqual({ gagnes: 2, depenses: 1, restants: 1 });
});

// « Repartir de zero », choisi une fois a l'activation du mode.
test('une date de depart efface tout ce qui precede', async ({ page }) => {
  const vieux = [{ ...victoire('Rhino', ['01001a', '01010a']), time: 100 },
                 { ...victoire('Klaw', ['01001a']), time: 100 }];
  const p = await regle(page, 'parcours', [PALIERS, vieux, { depuis: 500 }]) as any;
  expect(p.etapes[0].franchi).toBe(false);
  expect(p.jetons.gagnes).toBe(0);
});

test('une defaite ne compte pas', async ({ page }) => {
  const perdue = [{ ...victoire('Rhino', ['01001a']), won: false }];
  const p = await regle(page, 'parcours', [PALIERS, perdue]) as any;
  expect(p.etapes[0].vilainsRestants.length).toBe(2);
  expect(p.jetons.gagnes).toBe(0);
});

// ⚠ ON NOMME CE QUI MANQUE, ON NE COMPTE PAS. « Gagne avec Thor » se lit et
// s'execute ; « il reste 3 heros » oblige a chercher lesquels.
test('la condition nomme ce qui manque', async ({ page }) => {
  const p = await regle(page, 'parcours', [PALIERS, [victoire('Rhino', ['01001a'])]]) as any;
  const phrase = await page.evaluate(async (etape) => {
    const mod: any = await import('/js/prepare/legacy.js');
    return mod.condition(etape);
  }, p.etapes[0]);
  expect(phrase).toContain('Klaw');
  expect(phrase).toContain('Captain Marvel');
});
