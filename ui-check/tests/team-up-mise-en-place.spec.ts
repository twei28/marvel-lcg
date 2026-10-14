// Rules Reference 1.8, annexe I : à la mise en place, une carte d'identité qui
// « correspond » au héros d'un autre joueur peut être remplacée par la carte
// Team-Up qui nomme les deux identités. La règle dit « may » : le lancement
// pose la question, échange par échange (décision de l'utilisateur, 11/10/2026).
//
// Cyclops (allié * Phoenix) et Phoenix (allié * Cyclops) : deux questions,
// Psychic Rapport (33023, réimprimé en 34023) nomme les deux. Les decks de
// départ l'incluent déjà : on l'en retire, sans quoi il n'y a rien à proposer.
// On accepte la première, on refuse la seconde, et on lit le descripteur
// réellement envoyé à /new. Aucune partie n'est créée : la requête est interceptée.
import { test, expect } from '@playwright/test';

test('Cyclops et Phoenix : deux questions Team-Up, seul l’échange accepté part au moteur', async ({ page }) => {
  await page.goto('/prepare.html');

  const questions: string[] = [];
  page.on('dialog', async (d) => {
    questions.push(d.message());
    if (questions.length === 1) await d.accept();
    else await d.dismiss();
  });

  let descripteur: { hero_json: string[] } | undefined;
  await page.route('**/new?data=*', async (route) => {
    const data = new URL(route.request().url()).searchParams.get('data') || '{}';
    descripteur = JSON.parse(data);
    await route.fulfill({ status: 200, body: '{}' });
  });
  await page.route('**/app/board.html', (route) => route.fulfill({ status: 200, body: '<html></html>' }));

  await page.evaluate(async () => {
    const lire = (n: string) => fetch(`/read_file?deck/starter/${n}.json`).then((r) => r.json());
    const [cyclops, phoenix] = await Promise.all([lire('cyclops'), lire('phoenix')]);
    const sansRapport = (d: { player_deck: string[] }) => ({ ...d, player_deck: d.player_deck.filter((x) => x !== '33023' && x !== '34023') });
    const { launch } = await import('/public/js/prepare/launcher.js');
    await launch({
      mode: { id: 'standard' },
      scenario: { rawJson: { encounter_sets: [] } },
      players: [
        { hero: { name: 'Cyclops' }, deck: sansRapport(cyclops) },
        { hero: { name: 'Phoenix' }, deck: sansRapport(phoenix) },
      ],
      playerCount: 2,
      premierJoueur: 0,
      seed: 1,
      timeoutSecondes: 0,
      difficulty: { base: 'standard', skirmish: false, heroic: 0, selectedModularSets: [] },
    });
  });

  expect(questions).toHaveLength(2);
  expect(questions[0]).toContain('Phoenix');
  expect(questions[0]).toContain('Psychic Rapport');
  expect(questions[1]).toContain('Cyclops');

  expect(descripteur).toBeDefined();
  const [deckCyclops, deckPhoenix] = descripteur!.hero_json.map((j) => JSON.parse(j));
  expect(deckCyclops.hero_deck).toContain('33023');
  expect(deckCyclops.hero_deck).not.toContain('33002');
  expect(deckPhoenix.hero_deck).toContain('34003');
  expect(deckPhoenix.hero_deck).not.toContain('33023');
  expect(deckPhoenix.hero_deck).not.toContain('34023');
});

test('decks de départ tels quels : Psychic Rapport y est déjà, aucune question', async ({ page }) => {
  await page.goto('/prepare.html');
  const questions: string[] = [];
  page.on('dialog', async (d) => { questions.push(d.message()); await d.dismiss(); });
  await page.route('**/new?data=*', (route) => route.fulfill({ status: 200, body: '{}' }));
  await page.route('**/app/board.html', (route) => route.fulfill({ status: 200, body: '<html></html>' }));
  await page.evaluate(async () => {
    const lire = (n: string) => fetch(`/read_file?deck/starter/${n}.json`).then((r) => r.json());
    const [cyclops, phoenix] = await Promise.all([lire('cyclops'), lire('phoenix')]);
    const { launch } = await import('/public/js/prepare/launcher.js');
    await launch({
      mode: { id: 'standard' },
      scenario: { rawJson: { encounter_sets: [] } },
      players: [
        { hero: { name: 'Cyclops' }, deck: cyclops },
        { hero: { name: 'Phoenix' }, deck: phoenix },
      ],
      playerCount: 2,
      premierJoueur: 0,
      seed: 1,
      timeoutSecondes: 0,
      difficulty: { base: 'standard', skirmish: false, heroic: 0, selectedModularSets: [] },
    });
  });
  expect(questions).toEqual([]);
});
