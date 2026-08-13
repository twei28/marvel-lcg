// Une partie The Spot se met-elle en place SUR LE PLATEAU ?
//
// Ni `autoplay` ni les verificateurs ne repondent a cette question : ils
// tournent dans leur propre processus, avec un moteur fraichement charge. Le
// joueur, lui, arrive sur un plateau servi par un moteur DEJA DEMARRE. C'est
// exactement ce qui a fait croire a un scenario casse le 13/08 : le serveur
// tournait depuis avant que les cartes existent, et la partie s'arretait apres
// la mise en place du heros.
//
// Ce test demande donc au plateau ce qu'il MONTRE. Il exige la partie en cours,
// pas un ecran vide.
import { test, expect } from '@playwright/test';

test('le plateau met en place une partie The Spot', async ({ page }) => {
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(e.message));

  await page.goto('/app/board.html');
  await page.waitForTimeout(20000);
  const texte = await page.locator('body').innerText();
  console.log('PLATEAU :', texte.replace(/\n+/g, ' | ').slice(0, 400));

  expect(erreurs, 'erreurs JS sur le plateau').toEqual([]);
  // Le vilain, son complot et son environnement doivent etre poses.
  expect(texte).toContain('The Spot');
  expect(texte).toContain('Heightened Threat');
  expect(texte).toContain('What Goes Around');
});
