// La fiche du mode Legacy : ce qu'il retient d'un compte.
//
// Trois choses, et trois seulement, qui NE SE DEDUISENT PAS de l'historique des
// parties : le mode est-il actif, a partir de quand les parties comptent, et
// quels heros fan-made ont ete achetes. Tout le reste se recalcule.
//
// ⚠ L'INSTANTANE N'EST PAS LA VERITE, et c'est ce qui rend l'ensemble sur. La
// verite est `games_history`, ecrit par le moteur a chaque fin de partie.
// L'instantane est jetable : `reconstruire()` le refait a partir de rien.
//
// Ces cas ecrivent vraiment dans le fichier du serveur de developpement, et le
// remettent a zero en partant.
//
//   npm run legacy-fiche
import { test, expect, type Page } from '@playwright/test';

async function fiche(page: Page, nom: string, args: unknown[] = []) {
  return page.evaluate(async ({ nom, args }) => {
    const mod: Record<string, (...a: unknown[]) => unknown> =
      await import('/js/prepare/legacy-fiche.js');
    return JSON.parse(JSON.stringify(await mod[nom](...(args as unknown[])), (_c, v) =>
      v instanceof Set ? [...v].sort() : v));
  }, { nom, args });
}

async function vider(page: Page) {
  await page.evaluate(async () => {
    const mod: any = await import('/js/prepare/legacy-fiche.js');
    await mod.ecrire(mod.ficheVide());
  });
}

test.beforeEach(async ({ page }) => {
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-mode', { timeout: 20000 });
  await vider(page);
});

test.afterAll(async ({ browser }) => {
  const page = await browser.newPage();
  await page.goto('/prepare.html');
  await vider(page);
  await page.close();
});

test('une fiche jamais ecrite est vierge, pas absente', async ({ page }) => {
  const f = await fiche(page, 'lire') as any;
  expect(f).toEqual({ actif: false, depuis: 0, jetonsDepenses: [], instantane: null });
});

// ⚠ ON NE FAIT CONFIANCE A RIEN de ce qui sort du fichier : il a pu etre ecrit
// par une version precedente, tronque par une coupure, ou edite a la main. Un
// champ manquant vaut sa valeur par defaut, jamais `undefined`, qui se
// propagerait jusqu'a l'ecran.
test('une fiche abimee est remise en forme', async ({ page }) => {
  const remis = await page.evaluate(async () => {
    const mod: any = await import('/js/prepare/legacy-fiche.js');
    return [mod.normaliser(null), mod.normaliser({ depuis: 'demain', jetonsDepenses: 'x' }),
            mod.normaliser({ jetonsDepenses: ['a', 'a', 'b'] })];
  });
  expect(remis[0].depuis).toBe(0);
  expect(remis[1].depuis).toBe(0);
  expect(remis[1].jetonsDepenses).toEqual([]);
  // Un doublon ne coute pas deux jetons.
  expect(remis[2].jetonsDepenses).toEqual(['a', 'b']);
});

test('ce qu on ecrit se relit', async ({ page }) => {
  await page.evaluate(async () => {
    const mod: any = await import('/js/prepare/legacy-fiche.js');
    await mod.ecrire({ actif: true, depuis: 1234, jetonsDepenses: ['nt001a'] });
  });
  const f = await fiche(page, 'lire') as any;
  expect(f.actif).toBe(true);
  expect(f.depuis).toBe(1234);
  expect(f.jetonsDepenses).toEqual(['nt001a']);
});

test('activer en reprenant ses parties passees ne pose aucune date', async ({ page }) => {
  const f = await fiche(page, 'activer', [false]) as any;
  expect(f.actif).toBe(true);
  expect(f.depuis).toBe(0);
});

test('activer en repartant de zero pose la date du jour', async ({ page }) => {
  const f = await fiche(page, 'activer', [true, 1_700_000_000_000]) as any;
  // L'historique porte des SECONDES, pas des millisecondes.
  expect(f.depuis).toBe(1_700_000_000);
});

// ⚠ UNE ACTIVATION NE SE REJOUE PAS. Reactiver un mode deja actif remettrait la
// date de depart a aujourd'hui et effacerait tout le parcours de quelqu'un qui
// a seulement reclique.
test('reactiver ne remet pas le compteur a zero', async ({ page }) => {
  await fiche(page, 'activer', [false]);
  const f = await fiche(page, 'activer', [true, 1_700_000_000_000]) as any;
  expect(f.depuis).toBe(0);
});

test('sans jeton, on n achete rien', async ({ page }) => {
  await page.evaluate(async () => {
    const mod: any = await import('/js/prepare/legacy-fiche.js');
    await mod.ecrire({ actif: true, depuis: 9_999_999_999, jetonsDepenses: [] });
  });
  const r = await fiche(page, 'acheter', ['nt001a']) as any;
  expect(r.ok).toBe(false);
  expect(r.raison).toBeTruthy();
});

// ⚠ SANS CE CONTROLE, UN DOUBLE CLIC COUTAIT DEUX JETONS POUR UN SEUL HEROS.
test('on n achete pas deux fois le meme heros', async ({ page }) => {
  await page.evaluate(async () => {
    const mod: any = await import('/js/prepare/legacy-fiche.js');
    await mod.ecrire({ actif: true, depuis: 0, jetonsDepenses: ['nt001a'] });
  });
  const r = await fiche(page, 'acheter', ['nt001a']) as any;
  expect(r.ok).toBe(false);
});

test('l etat rend la fiche, les paliers et le parcours', async ({ page }) => {
  const e = await fiche(page, 'etat') as any;
  expect(e.fiche).toBeTruthy();
  expect(e.paliers.length).toBeGreaterThanOrEqual(12);
  expect(e.parcours.etapes.length).toBe(e.paliers.length);
  expect(e.parcours.etapes[0].ouvert).toBe(true);
});

// L'outil de reconstruction promis par la spec : la fiche peut etre perdue,
// tronquee ou perimee, tout ce qui compte se retrouve dans games_history. Seuls
// `depuis` et les jetons depenses ne s'en deduisent pas, et ceux-la survivent.
test('reconstruire refait l instantane sans toucher au reste', async ({ page }) => {
  await page.evaluate(async () => {
    const mod: any = await import('/js/prepare/legacy-fiche.js');
    await mod.ecrire({ actif: true, depuis: 4242, jetonsDepenses: ['nt001a'],
                       instantane: { vagueOuverte: 99, mensonge: true } });
  });
  const f = await fiche(page, 'reconstruire') as any;
  expect(f.depuis).toBe(4242);
  expect(f.jetonsDepenses).toEqual(['nt001a']);
  expect(f.instantane.vagueOuverte).not.toBe(99);
  expect(f.instantane.quand).toBeGreaterThan(0);
});
