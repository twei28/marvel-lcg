// Le mode Bataille envoie-t-il au moteur ce qu'il faut pour DEUX tables ?
//
// Le moteur sait monter une partie competitive (deux zones de jeu, deux
// leaders, deux decks rencontre), mais il ne le fait que si le descripteur de
// lancement le lui demande : `mode_competitive` dans `rules`, plus les trois
// cles `campaign_json_2`, `encounter_set_names_2` et `teams`. Rien ne relie
// l'ecran de preparation au moteur : une preparation qui oublie une de ces
// cles produit une partie ORDINAIRE, sans la moindre erreur nulle part.
//
// Le test verrouille les deux sens :
//   * une partie de Bataille porte les trois cles et le drapeau ;
//   * une partie ORDINAIRE n'en porte aucune -- c'est ce que mesure
//     contrat-nouvelle-partie.json, et le voir apparaitre serait un defaut.
import { test, expect } from '@playwright/test';

/** Un deck minimal : `buildDescriptor` ne fait que le serialiser. Le test
 *  mesure le DESCRIPTEUR, pas une partie jouee. */
const DECK = { name: 'Test', hero: ['01001a'], hero_deck: [], obligations: [], nemesis_set: [], player_deck: [] };

test('la tuile Bataille existe dans le selecteur de modes', async ({ page }) => {
  await page.goto('/prepare.html');
  await page.waitForSelector('.mode-pill', { timeout: 30000 });
  const libelles = (await page.locator('.mode-pill').allInnerTexts()).map((s) => s.trim());
  console.log('MODES PROPOSES :', libelles.join(' | ').replace(/\n/g, ' '));
  expect(libelles.join(' ').toLowerCase()).toContain('bataille');
});

test('le descripteur de Bataille porte les deux tables, une partie ordinaire non', async ({ page }) => {
  await page.goto('/prepare.html');
  await page.waitForSelector('.mode-pill', { timeout: 30000 });

  const resultat = await page.evaluate(async (deck) => {
    const { catalog } = await import('/public/js/prepare/catalog.js');
    const { buildDescriptor } = await import('/public/js/prepare/launcher.js');
    const { cards } = await import('/public/js/prepare/cards.js');
    await cards.load();

    // Les scenarios de bataille se reconnaissent dans les DONNEES : leur
    // adversaire est un LEADER. Meme regle que l'ecran de preparation.
    const batailles: any[] = [];
    for (const ext of await catalog.extensions()) {
      let liste: any[] = [];
      try { liste = await catalog.scenariosForExtension(ext.key); } catch (e) { continue; }
      for (const sc of liste) {
        const carte = cards.get((sc.villainCards || [])[0]);
        if (carte && String(carte.type) === 'Leader') batailles.push(sc);
      }
    }
    if (batailles.length < 2) return { erreur: `seulement ${batailles.length} scenario(s) de bataille` };

    const etat = (modeId: string, scenario2: any) => ({
      mode: { id: modeId },
      scenario: batailles[0],
      scenario2,
      playerCount: 2,
      premierJoueur: 0,
      players: [{ deck }, { deck }],
      difficulty: { base: 'standard', skirmish: false, heroic: 0, selectedModularSets: [] },
      seed: 1,
      timeoutSecondes: 0,
      reglesV16: true,
      campaignLog: {},
    });

    const bataille = await buildDescriptor(etat('bataille', batailles[1]));
    const ordinaire = await buildDescriptor(etat('hotseat', null));
    return {
      noms: [batailles[0].name, batailles[1].name],
      nombreDeBatailles: batailles.length,
      bataille: {
        cles: Object.keys(bataille).sort(),
        rules: bataille.rules,
        teams: (bataille as any).teams,
        sets2: (bataille as any).encounter_set_names_2,
        nomScenario2: JSON.parse((bataille as any).campaign_json_2 || '{}').name,
      },
      ordinaire: { cles: Object.keys(ordinaire).sort(), rules: ordinaire.rules },
    };
  }, DECK);

  expect(resultat.erreur, resultat.erreur || '').toBeUndefined();
  console.log('SCENARIOS DE BATAILLE TROUVES :', resultat.nombreDeBatailles, '->', resultat.noms?.join(' vs '));
  console.log('CLES EN BATAILLE  :', resultat.bataille!.cles.join(', '));
  console.log('CLES EN ORDINAIRE :', resultat.ordinaire!.cles.join(', '));

  const b = resultat.bataille!;
  expect(b.rules, 'le drapeau du mode competitif manque').toContain('mode_competitive');
  expect(b.cles).toContain('campaign_json_2');
  expect(b.cles).toContain('encounter_set_names_2');
  expect(b.cles).toContain('teams');
  expect(b.teams, 'le camp de chaque siege : 1v1').toEqual([0, 1]);
  expect(b.sets2!.length, 'la seconde table n a aucun set de rencontre').toBeGreaterThan(0);
  expect(b.nomScenario2, 'le second scenario n est pas celui choisi').toBe(resultat.noms![1]);

  const o = resultat.ordinaire!;
  expect(o.rules, 'une partie ordinaire ne doit pas etre competitive').not.toContain('mode_competitive');
  for (const cle of ['campaign_json_2', 'encounter_set_names_2', 'teams']) {
    expect(o.cles, `une partie ordinaire ne doit pas porter ${cle}`).not.toContain(cle);
  }
});
