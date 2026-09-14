// LE TEXTE SOUS LA CARTE AGRANDIE EST EN FRANÇAIS, OU IL N'Y EST PAS.
//
// ⚠ POURQUOI CE FICHIER EXISTE. Défaut n°6 de la fiche du 14/09/2026, capture à
// l'appui : « je suis en FR et le texte dans le tooltip sous la carte est en
// anglais............... »
//
// LA CAUSE, mesurée sur l'API elle-même : `fr.marvelcdb.com` REND L'ANGLAIS
// quand la traduction française n'existe pas, et rien dans sa réponse ne le
// dit — sauf ceci : `text` et `real_text` y sont alors IDENTIQUES. Sur une
// carte traduite ils diffèrent (Spider-Man : « Sens d'Araignée » contre
// « Spider-Sense »). Le proxy du serveur (`server_get.py`, `marvelcdb_card`)
// retire donc le texte dans ce cas, et le plateau n'affiche plus rien.
//
// ⚠ CE TEST TOUCHE LE RÉSEAU (fr.marvelcdb.com, via le proxy du serveur). Sans
// réseau il ne peut rien prouver : il le dit et s'arrête, plutôt que de passer
// au vert sans avoir rien vérifié.
//
//   npm run marvelcdb-francais
import { expect, test, type APIRequestContext } from '@playwright/test';

/** Une carte SANS traduction française sur marvelcdb (pack Civil War). */
const SANS_TRADUCTION = '56033'; // Hulk Shape — la carte même de la capture
/** Une carte traduite depuis toujours. */
const TRADUITE = '01001a'; // Spider-Man

async function carte(request: APIRequestContext, code: string) {
  const reponse = await request.get(`/marvelcdb_card?${code}`);
  return { statut: reponse.status(), corps: reponse.ok() ? await reponse.json() : undefined };
}

test('⚠ une carte NON TRADUITE ne renvoie pas son texte anglais', async ({ request }) => {
  const { statut, corps } = await carte(request, SANS_TRADUCTION);
  test.skip(statut === 502, 'pas de réseau vers marvelcdb : ce test ne peut rien prouver');
  expect(statut, `le proxy a répondu ${statut}`).toBe(200);

  expect(
    corps.text,
    `le texte anglais de la carte ${SANS_TRADUCTION} est servi comme du français : ` +
      `« ${String(corps.text).slice(0, 60)} »`
  ).toBeUndefined();
  expect(corps.non_traduit, 'le proxy ne signale pas l’absence de traduction').toBe(true);
  // Le nom, lui, reste : un nom identique dans les deux langues n'a rien de faux.
  expect(corps.name).toBeTruthy();
});

test('⚠ une carte TRADUITE garde son texte français', async ({ request }) => {
  const { statut, corps } = await carte(request, TRADUITE);
  test.skip(statut === 502, 'pas de réseau vers marvelcdb : ce test ne peut rien prouver');
  expect(statut).toBe(200);

  expect(corps.text, 'le texte français a disparu avec le correctif').toBeTruthy();
  expect(corps.non_traduit).toBeUndefined();
  // Et c'est bien du français : le texte anglais de cette carte dit
  // « Spider-Sense — Interrupt: When the villain initiates an attack… ».
  expect(
    String(corps.text),
    `le texte servi n'est pas le français attendu : « ${String(corps.text).slice(0, 60)} »`
  ).toMatch(/Interruption|Araignée/i);
});
