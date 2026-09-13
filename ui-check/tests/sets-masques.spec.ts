// Les extensions MISES DE COTE, et leurs sets de rencontre.
//
// Un set fan-made peut etre termine, teste et commite sans devoir partir en
// production. Le drapeau `indisponible: true` dans data/sets_info.json le
// retire de l'ecran de preparation : ses fichiers restent en place, le moteur
// sait toujours le monter (tools/autoplay.py --modulaires s'en sert), mais un
// joueur ne le voit nulle part.
//
// C'est un drapeau de DONNEES lu par une seule fonction de catalog.js. Rien ne
// le protegeait : une refonte du catalogue pouvait le laisser tomber et
// publier un set mis de cote SANS QUE RIEN NE LE SIGNALE. D'ou ce test, qui
// interroge le catalogue REEL dans la page, pas une copie.
//
//   npm run sets-masques
//
// Le test ne nomme aucun set : il lit sets_info.json, prend ce qui y est
// marque indisponible, et exige que le catalogue l'ait ecarte. Un set remis en
// service (cle `indisponible` supprimee) le fait passer sans le toucher.
import { test, expect } from '@playwright/test';

type Extension = { name?: string; encounters?: string[]; indisponible?: boolean };

test('un set de rencontre mis de cote n est propose nulle part', async ({ page }) => {
  const r = await page.request.get('/get_sets_json?');
  expect(r.ok()).toBeTruthy();
  const brut: Record<string, Extension | string> = await r.json();

  const masques: string[] = [];
  const clesMasquees: string[] = [];
  for (const [cle, v] of Object.entries(brut)) {
    if (typeof v !== 'object' || v === null || !v.indisponible) continue;
    clesMasquees.push(cle);
    masques.push(...(v.encounters ?? []));
  }
  console.log('EXTENSIONS MISES DE COTE :', JSON.stringify(clesMasquees));
  console.log('SETS DE RENCONTRE MASQUES :', JSON.stringify(masques));

  // On ouvre la page pour son ORIGINE, pas pour son ecran : le catalogue se
  // charge tout seul par api.js. Inutile de traverser l'assistant, qui s'ouvre
  // desormais sur le choix du mode de jeu et n'a pas encore de liste de sets.
  await page.goto('/prepare.html');

  // Le catalogue de la page, celui-la meme que lit l'ecran de preparation.
  const vu = await page.evaluate(async () => {
    const { catalog } = await import('/js/prepare/catalog.js');
    const sets = await catalog.encounterSets();
    const exts = await catalog.extensions();
    return {
      setsProposes: sets.map((s: any) => s.name),
      modulaires: sets.filter((s: any) => s.kind === 'modular').map((s: any) => s.name),
      clesExtensions: exts.map((e: any) => e.key),
    };
  });

  // 1. Aucun set masque ne figure dans la liste, modulaires compris : ce sont
  //    les chips « Personnalises » et le tirage « Aleatoire ».
  for (const nom of masques) {
    expect(vu.setsProposes, `le set masque « ${nom} » est propose`).not.toContain(nom);
    expect(vu.modulaires, `le set masque « ${nom} » est tirable au hasard`).not.toContain(nom);
  }
  // 2. Ni l'extension elle-meme, qui sinon ouvrirait un onglet vide.
  for (const cle of clesMasquees) {
    expect(vu.clesExtensions, `l extension mise de cote « ${cle} » est listee`).not.toContain(cle);
  }
  // 3. TEMOIN : le filtre ecarte ce qui est marque, et RIEN D'AUTRE. Sans
  //    cette ligne, un filtre qui renverrait une liste vide passerait au vert.
  expect(vu.modulaires.length).toBeGreaterThan(20);
  expect(vu.setsProposes).toContain('bomb_scare');
});
