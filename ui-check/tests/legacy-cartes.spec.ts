// Quelles CARTES on a deja, en Legacy : le module pur eprouve sur des donnees
// fabriquees, puis sur le VRAI catalogue.
//
//   npm run legacy-cartes
import { test, expect, type Page } from '@playwright/test';

const ETAT = { parcours: { etapes: [
  { vague: 0, nom: 'Set de base', ouvert: true },
  { vague: 1, nom: 'Vague 1', ouvert: false },
] } };
const EXTENSIONS = [{ key: '1. Core Set', code: 'core' }, { key: '2. The Green Goblin', code: 'green_goblin' },
                    { key: '98. Custom (Night Thrasher)', code: 'night_thrasher' }];
const PAQUETS: Record<string, string> = { '01088': 'core', '02001': 'green_goblin', 'nt001a': 'night_thrasher' };

async function dispo(page: Page, appel: string, arg: unknown) {
  return page.evaluate(async ({ appel, arg, ETAT, EXTENSIONS, PAQUETS }) => {
    const mod: any = await import('/js/prepare/legacy-cartes.js');
    const d = mod.fabriquerDisponibilite(ETAT, EXTENSIONS, (id: string) => PAQUETS[id] || '');
    return d[appel](arg);
  }, { appel, arg, ETAT, EXTENSIONS, PAQUETS });
}

test.beforeEach(async ({ page }) => { await page.goto('/prepare.html'); });

test('une carte du Set de base est disponible', async ({ page }) => {
  expect(await dispo(page, 'carte', '01088')).toEqual({ ouvert: true, etiquette: '' });
});

test('une carte d une boite fermee dit sa boite', async ({ page }) => {
  expect(await dispo(page, 'carte', '02001')).toEqual({ ouvert: false, etiquette: 'Vague 1' });
});

// On n'invente pas de regle pour ce qui n'est dans aucun palier.
test('une carte sans vague reste libre', async ({ page }) => {
  expect(await dispo(page, 'carte', 'nt001a')).toEqual({ ouvert: true, etiquette: '' });
  expect(await dispo(page, 'carte', 'inconnue')).toEqual({ ouvert: true, etiquette: '' });
});

test('un deck est jouable quand TOUTES ses cartes le sont', async ({ page }) => {
  expect(await dispo(page, 'deck', { hero: ['01001a,01001b'], hero_deck: [], player_deck: ['01088', '01088'] }))
    .toEqual({ ouvert: true, manquantes: [] });
  expect(await dispo(page, 'deck', { player_deck: ['01088', '02001', '02001'] }))
    .toEqual({ ouvert: false, manquantes: ['02001'] });
});

// ⚠ LE CAS QUI COMPTE : sur le vrai catalogue, un joueur du Set de base doit
// pouvoir jouer le deck de base de Spider-Man, et PAS le paquet d'aspect qui
// pioche dans les boites suivantes.
test('sur le vrai catalogue, le deck de base passe et un paquet d aspect non', async ({ page }) => {
  const bilan = await page.evaluate(async () => {
    const cartes: any = await import('/js/prepare/legacy-cartes.js');
    const cat: any = await import('/js/prepare/catalog.js');
    const fiche: any = await import('/js/prepare/legacy-fiche.js');
    const c: any = await import('/js/prepare/cards.js');
    await c.cards.load();
    // Un etat fabrique : seul le Set de base ouvert, quoi que dise la fiche.
    const e = await fiche.etat();
    e.parcours.etapes = e.parcours.etapes.map((x: any, i: number) => ({ ...x, ouvert: i === 0 }));
    const d = cartes.fabriquerDisponibilite(e, await cat.catalog.extensions(),
      (id: string) => { const k = c.cards.get(id); return k ? k.package_name : ''; });
    const heros = (await cat.catalog.heroes()).find((h: any) => h.name === 'Spider-Man');
    const decks = await cat.catalog.decksForHero(heros);
    return decks.map((dk: any) => ({ source: dk.source, nom: dk.name, ...d.deck(dk.deck) }));
  });
  console.log('DECKS DE SPIDER-MAN :', JSON.stringify(bilan.map((b: any) => [b.source, b.nom, b.ouvert, b.manquantes.length])));
  const base = bilan.find((b: any) => b.source === 'base');
  expect(base).toBeTruthy();
  expect(base.ouvert).toBe(true);
  const paquets = bilan.filter((b: any) => b.source === 'aspect');
  expect(paquets.length).toBeGreaterThan(0);
  expect(paquets.some((b: any) => !b.ouvert)).toBe(true);
});
