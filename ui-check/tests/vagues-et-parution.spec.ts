// Le nommage des vagues, et l'ordre dans lequel les boites-campagnes sont
// proposees. Deux tables se repondent et rien ne les tenait ensemble :
//
//  - catalog.js dit a quelle vague appartient une extension (BORNES_VAGUES) ET
//    quel titre porte cette vague (NOMS_VAGUES). Une boite ajoutee dans l'une et
//    oubliee dans l'autre donne un menu qui ment, sans erreur nulle part.
//  - server_campagne.py trie les boites par le numero de leur cle d'extension.
//    Sans ce tri, la liste s'ouvrait sur la boite de 2025 et finissait sur celle
//    de 2020, parce que l'ordre venait du nom de fichier.
//
// Les libellés ne sont pas ecrits en dur ici : le test refuse un numero NU
// (« Vague 5 » sans titre) et verifie que le tri est croissant. Une boite a
// venir passe donc sans toucher a ce fichier.
import { test, expect } from '@playwright/test';

test('le menu des vagues porte le titre de la grande boite', async ({ page }) => {
  await page.goto('/prepare.html');
  // ⚠ L'assistant s'ouvre sur l'ACCUEIL A TUILES depuis le 7 septembre : le
  // menu des vagues n'existe qu'a l'etape des heros, derriere un mode. Ce
  // test attendait le menu des l'ouverture et etait rouge depuis, sans que
  // personne ne le relance (constate le 13/09/2026).
  await page.getByRole('button', { name: /^Solo/ }).first().click();
  await page.waitForSelector('.vague-select option:nth-child(2)', { state: 'attached', timeout: 20000 });
  const libelles = await page.$$eval('.vague-select option', o => o.map(x => x.textContent!.trim()));
  console.log('LIBELLES FR :', JSON.stringify(libelles, null, 1));

  expect(libelles).toContain('Set de base');
  expect(libelles).toContain('Vague 1 · Les premiers paquets');
  for (const [n, titre] of [[2, 'The Rise of Red Skull'], [5, 'Sinister Motives'],
                            [8, 'Age of Apocalypse'], [11, 'Fear No Evil']] as [number, string][]) {
    const attendu = `Vague ${n} · ${titre}`;
    if (libelles.some(l => l.startsWith(`Vague ${n}`))) expect(libelles).toContain(attendu);
  }
  // aucun libelle ne doit rester un numero nu
  expect(libelles.filter(l => /^Vague \d+$/.test(l))).toEqual([]);
});

test('les campagnes sont proposees dans l ordre de parution', async ({ page }) => {
  const r = await page.request.get('/list_campagnes_definies');
  expect(r.ok()).toBeTruthy();
  const liste = await r.json();
  const rangs = liste.map((c: any) => parseInt(String(c.cle_extension).split('.')[0], 10));
  expect(rangs).toEqual([...rangs].sort((a, b) => a - b));
  expect(rangs[0]).toBe(4);   // The Rise of Red Skull, 2020
  // La derniere boite OFFICIELLE est Agents of S.H.I.E.L.D. (50) ; une
  // campagne fan-made (120) s'est rangee apres elle depuis. Le tri croissant
  // est ce qu'on verifie, pas l'identite du dernier : figer « 50 » rendait le
  // test rouge a chaque campagne ajoutee (constate le 13/09/2026).
  expect(rangs).toContain(50);
  expect(rangs[rangs.length - 1]).toBeGreaterThanOrEqual(50);
});

test('en anglais, seul le mot Wave est traduit', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('marvel-langue', 'en'));
  await page.goto('/prepare.html');
  await page.getByRole('button', { name: /^Solo/ }).first().click();
  await page.waitForSelector('.vague-select option:nth-child(2)', { state: 'attached', timeout: 20000 });
  const libelles = await page.$$eval('.vague-select option', o => o.map(x => x.textContent!.trim()));
  console.log('LIBELLES EN :', JSON.stringify(libelles, null, 1));
  expect(libelles).toContain('Core Set');
  expect(libelles).toContain('Wave 5 · Sinister Motives');
  expect(libelles.some(l => l.startsWith('Vague '))).toBeFalsy();
});
