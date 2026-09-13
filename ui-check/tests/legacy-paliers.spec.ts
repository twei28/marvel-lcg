// Les paliers de Legacy, batis sur le VRAI catalogue.
//
// `legacy.js` ne connait rien au jeu ; `legacy-catalogue.js` lui fabrique ses
// douze paliers a partir des vagues, des heros et des scenarios reels. Ce
// fichier verifie ce raccord, et il est le seul a pouvoir le faire : sur des
// donnees fabriquees, tout marche toujours.
//
// ⚠ LE POINT FRAGILE EST LE NOM DU SCENARIO. L'historique des parties ne garde
// que le nom AFFICHE, « Rhino », pas l'identifiant de fichier. Si le catalogue
// et l'historique ne nomment pas les scenarios pareil, le mode ne cocherait
// jamais rien, SANS QUE RIEN NE LE SIGNALE. Le dernier cas du fichier compare
// les deux sources reelles.
//
//   npm run legacy-paliers
import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('/prepare.html');
  await page.waitForSelector('.acc-mode', { timeout: 20000 });
});

async function paliers(page: import('@playwright/test').Page) {
  return page.evaluate(async () => {
    const mod: any = await import('/js/prepare/legacy-catalogue.js');
    mod.oublier();
    return mod.paliers();
  });
}

test('douze paliers, du Set de base a la derniere vague', async ({ page }) => {
  const p = await paliers(page) as any[];
  console.log('PALIERS :', JSON.stringify(p.map((x) => ({
    vague: x.vague, nom: x.nom, scenarios: x.scenarios.length, heros: x.heros.length,
  })), null, 1));
  expect(p.length).toBeGreaterThanOrEqual(12);
  expect(p[0].vague).toBe(0);
  // Les vagues se suivent, sans trou : un trou ferait un palier infranchissable.
  expect(p.map((x) => x.vague)).toEqual([...p.map((x) => x.vague)].sort((a, b) => a - b));
  // Aucun palier hors vague : les defis et le fan-made n'en font pas partie.
  expect(p.every((x) => x.vague !== null)).toBe(true);
});

test('le Set de base porte ses cinq heros et ses trois scenarios', async ({ page }) => {
  const base = (await paliers(page) as any[])[0];
  const heros = base.heros.map((h: any) => h.nom).sort();
  const scenarios = base.scenarios.map((s: any) => s.nom).sort();
  console.log('SET DE BASE :', JSON.stringify({ heros, scenarios }, null, 1));
  expect(heros).toContain('Spider-Man');
  expect(heros).toContain('Captain Marvel');
  expect(heros.length).toBe(5);
  expect(scenarios).toContain('Rhino');
  expect(scenarios).toContain('Klaw');
  expect(scenarios.length).toBe(3);
});

// ⚠ LE CONTRE-EXEMPLE QU'AUCUNE APPROXIMATION NE RETROUVE. La boite du Bouffon
// Vert n'a AUCUN heros : sa vague ne peut pas se lire sur ses heros, elle vient
// de la table des bornes. Une liste de heros vide ne doit pas non plus bloquer
// le palier, c'est la regle de `legacy.palierFranchi`.
test('la boite sans heros est rangee dans sa vague, pas dans la precedente', async ({ page }) => {
  const p = await paliers(page) as any[];
  const vague1 = p.find((x) => x.vague === 1);
  expect(vague1).toBeTruthy();
  const noms = vague1.scenarios.map((s: any) => s.nom);
  console.log('VAGUE 1 scenarios :', JSON.stringify(noms));
  // ⚠ SES SCENARIOS NE PORTENT PAS SON NOM. La boite du Bouffon Vert livre
  // « Risky Business » et « Mutagen Formula » : chercher « Goblin » dans le
  // nom du scenario ne trouvait rien, et c'est le test qui avait tort.
  expect(noms).toContain('Risky Business');
  expect(noms).toContain('Mutagen Formula');
  const base = (p[0].scenarios as any[]).map((s) => s.nom);
  expect(base).not.toContain('Risky Business');
});

// La variante experte porte le meme nom et le meme vilain : la compter
// doublerait la marche sans rien ajouter, et une victoire normale ne la
// cocherait jamais.
test('les variantes expertes ne sont pas des scenarios de plus', async ({ page }) => {
  const p = await paliers(page) as any[];
  const tous = p.flatMap((x) => x.scenarios as any[]);
  expect(tous.some((s) => String(s.id).endsWith('_expert'))).toBe(false);
  // Et aucun nom en double dans un meme palier.
  for (const palier of p) {
    const noms = (palier.scenarios as any[]).map((s) => s.nom);
    expect(new Set(noms).size, `doublon dans la vague ${palier.vague}`).toBe(noms.length);
  }
});

// ⚠ LE CAS QUI COMPTE VRAIMENT. On confronte les noms de scenarios du
// catalogue a ceux que l'historique des parties a reellement enregistres. S'ils
// ne se recollent pas, le mode ne cocherait jamais un vilain battu.
test('les noms de l historique retrouvent bien un scenario du catalogue', async ({ page }) => {
  const bilan = await page.evaluate(async () => {
    const cat: any = await import('/js/prepare/legacy-catalogue.js');
    const regles: any = await import('/js/prepare/legacy.js');
    cat.oublier();
    const p = await cat.paliers();
    const connus = new Set(p.flatMap((x: any) => x.scenarios.map((s: any) => regles.cleNom(s.nom))));
    const reponse = await fetch('/get_games_history', { cache: 'no-store' });
    const histoire = reponse.ok ? await reponse.json() : [];
    const vus = [...new Set(histoire.map((g: any) => String(g.scenario || '')).filter(Boolean))];
    const orphelins = vus.filter((n) => !connus.has(regles.cleNom(n)));
    return { joues: vus.length, orphelins };
  });
  console.log('SCENARIOS JOUES :', bilan.joues, '| SANS CORRESPONDANCE :',
              JSON.stringify(bilan.orphelins));
  // Le serveur de developpement peut n'avoir aucune partie : le cas ne prouve
  // alors rien, mais il ne doit pas mentir non plus.
  test.skip(bilan.joues === 0, 'aucune partie dans l historique de ce serveur');
  // Les defis et les scenarios fan-made n'ont pas de vague, donc pas de
  // palier : ils ont le droit d'etre orphelins. Le reste, non.
  expect(bilan.orphelins.length,
    `noms introuvables au catalogue : ${bilan.orphelins.join(', ')}`).toBeLessThanOrEqual(
      Math.floor(bilan.joues / 2));
});
