// Le verrou de Legacy : ce qui est ouvert, ce qui est ferme, et pourquoi.
//
// `legacy-verrou.js` repond a la seule question que l'ecran pose des centaines
// de fois : « ce heros, ce scenario, je peux le prendre ? et sinon, qu'est-ce
// qu'il me faut ? ». Cas fabriques, module reel importe dans la page.
//
//   npm run legacy-verrou
import { test, expect, type Page } from '@playwright/test';

const ETAT = {
  fiche: { actif: true, depuis: 0, jetonsDepenses: ['nt001a'] },
  paliers: [
    { vague: 0, nom: 'Set de base', scenarios: [{ id: 'rhino', nom: 'Rhino' }], heros: [] },
    { vague: 1, nom: 'Vague 1', scenarios: [{ id: 'risky', nom: 'Risky Business' }], heros: [] },
  ],
  parcours: {
    vagueOuverte: 0,
    jetons: { gagnes: 2, depenses: 1, restants: 1 },
    etapes: [
      { vague: 0, nom: 'Set de base', ouvert: true, franchi: false,
        vilainsRestants: [{ id: 'rhino', nom: 'Rhino' }], herosRestants: [{ id: '06001a', nom: 'Thor' }] },
      { vague: 1, nom: 'Vague 1', ouvert: false, franchi: false, vilainsRestants: [], herosRestants: [] },
    ],
  },
};
const HEROS = [
  { id: 'spider', heroCardId: '01001a', name: 'Spider-Man', vague: 0, homebrew: false },
  { id: 'cap', heroCardId: '04001a', name: 'Captain America', vague: 1, homebrew: false },
  { id: 'nt', heroCardId: 'nt001a', name: 'Night Thrasher', vague: null, homebrew: true },
  { id: 'zeus', heroCardId: 'ze001a', name: 'Zeus', vague: null, homebrew: true },
];

async function verrou(page: Page, etat = ETAT, heros = HEROS) {
  return page.evaluate(async ({ etat, heros }) => {
    const mod: any = await import('/js/prepare/legacy-verrou.js');
    const v = mod.fabriquerVerrou(etat, heros);
    return {
      heros: Object.fromEntries(heros.map((h: any) => [h.name, v.heros(h)])),
      rhino: v.scenario({ name: 'Rhino' }), risky: v.scenario({ name: 'Risky Business' }),
      defi: v.scenario({ name: 'Gorr the God Butcher' }),
      prochaine: v.prochaine && v.prochaine.vague, jetons: v.jetons,
    };
  }, { etat, heros });
}

test.beforeEach(async ({ page }) => { await page.goto('/prepare.html'); });

test('un heros de la vague ouverte est libre', async ({ page }) => {
  const v = await verrou(page);
  expect(v.heros['Spider-Man']).toEqual({ ouvert: true, etiquette: '', condition: '', achetable: false });
});

// ⚠ ON NOMME CE QUI MANQUE. « Grise, avec sa condition affichee » : le joueur
// sait quoi faire, pas seulement qu'il ne peut pas.
test('un heros d une vague fermee dit sa boite et ce qu il faut d abord', async ({ page }) => {
  const v = await verrou(page);
  expect(v.heros['Captain America'].ouvert).toBe(false);
  expect(v.heros['Captain America'].condition).toContain('Vague 1');
  expect(v.heros['Captain America'].condition).toContain('Rhino');
  // ⚠ PLUS UN HEROS DANS LA CONDITION (16/09/2026). Elle citait « Thor » tant
  // que les heros fermaient la route ; depuis que seuls les mechants ouvrent
  // la vague suivante, l'y laisser ferait croire a une exigence.
  expect(v.heros['Captain America'].condition).not.toContain('Thor');
  // Sur la vignette, seulement la boite : la phrase entiere couvrait les
  // portraits et se repetait soixante fois.
  expect(v.heros['Captain America'].etiquette).toBe('Vague 1');
});

test('un fan-made achete est libre, un autre s achete si on a un jeton', async ({ page }) => {
  const v = await verrou(page);
  expect(v.heros['Night Thrasher'].ouvert).toBe(true);
  expect(v.heros['Zeus'].ouvert).toBe(false);
  expect(v.heros['Zeus'].achetable).toBe(true);
  expect(v.heros['Zeus'].condition).toContain('1 jeton');
});

test('sans jeton, un fan-made dit comment en gagner', async ({ page }) => {
  const sans = { ...ETAT, parcours: { ...ETAT.parcours, jetons: { gagnes: 1, depenses: 1, restants: 0 } } };
  const v = await verrou(page, sans);
  expect(v.heros['Zeus'].achetable).toBe(false);
  expect(v.heros['Zeus'].condition).toContain('officiel');
});

test('les scenarios suivent leur vague, et un defi hors vague reste libre', async ({ page }) => {
  const v = await verrou(page);
  expect(v.rhino.ouvert).toBe(true);
  expect(v.risky.ouvert).toBe(false);
  expect(v.risky.condition).toContain('Vague 1');
  // On n'invente pas de regle pour ce qui n'est dans aucun palier.
  expect(v.defi).toEqual({ ouvert: true, etiquette: '', condition: '' });
});

test('la prochaine etape est la premiere ouverte non franchie', async ({ page }) => {
  const v = await verrou(page);
  expect(v.prochaine).toBe(0);
  expect(v.jetons.restants).toBe(1);
});

test('tout franchi : plus de prochaine etape, tout est ouvert', async ({ page }) => {
  const fini = { ...ETAT, parcours: { ...ETAT.parcours, vagueOuverte: 1,
    etapes: ETAT.parcours.etapes.map((e) => ({ ...e, ouvert: true, franchi: true, vilainsRestants: [], herosRestants: [] })) } };
  const v = await verrou(page, fini);
  expect(v.prochaine).toBeNull();
  expect(v.heros['Captain America'].ouvert).toBe(true);
  expect(v.risky.ouvert).toBe(true);
});
