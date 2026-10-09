// Une carte inscrite au carnet ne sort pas du deck.
//
// LA REGLE, ET CE QU'ELLE VISE VRAIMENT
//
// Le livret de Rise of Red Skull (p.3) dit : « Added cards must be included in
// the player's deck for the rest of the campaign. » Dans ce jeu, la plupart des
// cartes gagnees vivent AU CARNET et non dans le deck enregistre : le moteur
// les repose a chaque mise en place depuis leur cle (ameliorations Tech de
// trors, materiel S.H.I.E.L.D. de sm, allie de campagne d'aoa, cartes du Marche
// de gmw). Personne ne peut donc les retirer d'un deck ou elles n'ont jamais
// ete, et la regle est tenue par construction.
//
// UNE recompense fait l'inverse et cherche la carte DANS le deck du joueur :
// « Planning Ahead » (sm, Reputation 17). Le livret : « Each player chooses one
// card from their deck », puis au scenario suivant « each player searches their
// deck and discard pile for 1 copy of the card recorded in their Planning Ahead
// section ». Mesure a la sonde, avec temoin : carte notee presente, elle arrive
// EN MAIN a la mise en place ; carte notee absente, il ne se passe RIEN — pas
// d'erreur, pas de message, la recompense disparait en silence.
//
// D'ou le refus teste ici, au retour de « Modifier les decks », le seul moment
// ou le deck d'une campagne change.
//
//   npm run campagne-cartes-imposees
//
// ATTENTION : ce test cree une campagne sur le serveur, la modifie et la
// supprime. Il ne touche a aucune campagne existante et ne lance aucune partie.
// Selecteurs mis a jour le 09/10/2026 : la refonte « Affiche » de l'assistant
// (b8895bca, 07/09) a remplace #db-<i>/.deck-opt par #deck-liste/.tb-deck, et la
// fenetre des variantes du heros (3d5524b4, 11/09) s'ouvre au clic.
import { test, expect, type Page, type APIRequestContext } from '@playwright/test'

const NOM_CAMPAGNE = 'Essai automatique - cartes imposees'
const HEROS = /^Colossus/

/** La cle du carnet, exactement comme le moteur la lit (sm/campaign.py). */
const CLE = 'Player 1 Planning Ahead: Reputation Track Reward'

/**
 * Une amelioration « Campaign - Tech » de Rise of Red Skull.
 *
 * Choisie pour une seule raison : aucun deck que l'ecran de preparation sait
 * composer ne la contient, ni deck de base, ni paquet d'aspect conseille. Le
 * refus est donc certain quel que soit le deck retenu — sans elle, le test
 * dependrait du hasard du contenu du paquet choisi.
 */
const CARTE_HORS_DECK = '04155'

type Membre = { nomHeros?: string; identite?: string[]; deck: { player_deck?: string[] } }
type Campagne = { id: string; nom?: string; equipe?: Membre[]; carnet?: Record<string, string> }

let identifiant = ''

const empreinte = (membre: Membre) => (membre.deck.player_deck ?? []).slice().sort().join(',')

async function campagnes(request: APIRequestContext): Promise<Campagne[]> {
  return (await request.get('/list_campagnes?')).json()
}

async function laNotre(request: APIRequestContext): Promise<Campagne> {
  const trouvee = (await campagnes(request)).find((c) => c.id === identifiant)
  expect(trouvee, `La campagne temoin ${identifiant} a disparu du serveur.`).toBeTruthy()
  return trouvee!
}

/** Inscrit une carte au carnet, cote serveur, comme le ferait le panneau. */
async function inscrireAuCarnet(request: APIRequestContext, carte: string) {
  const campagne = await laNotre(request)
  campagne.carnet = { ...(campagne.carnet ?? {}), 'Reputation Track': '17', [CLE]: carte }
  const reponse = await request.post('/save_campagne', { data: { campagne } })
  expect(reponse.status()).toBe(200)
}

async function ouvrirLaCampagne(page: Page) {
  await page.goto('/campagne.html', { waitUntil: 'networkidle' })
  const carte = page.locator('.cmp-carte', { hasText: NOM_CAMPAGNE })
  await expect(carte, "La campagne temoin n'apparait pas dans la liste.").toHaveCount(1)
  await carte.locator('.cmp-carte-ouvrir').click()
  await expect(page.locator('.cmp-page-campagne')).toBeVisible()
}

/** Passe a l'etape des decks, sans toucher au choix de l'etape 1. */
async function allerAuxDecks(page: Page) {
  await page.getByRole('button', { name: /continuer/i }).click()
  await expect(page.locator('#deck-liste')).toBeVisible()
}

/**
 * Depuis le commit 3d5524b4 (11/09/2026), un clic sur un heros qui a des
 * variantes (arts alternatifs, version du deck, identite) ouvre la fenetre
 * « Options de ce heros » par-dessus l'ecran. On la valide telle quelle.
 */
async function validerOptionsDuHeros(page: Page) {
  const modale = page.locator('.deck-modal')
  if (await modale.isVisible().catch(() => false)) {
    await modale.getByRole('button', { name: /valider|confirm/i }).click()
    await expect(modale).toHaveCount(0)
  }
}

/** Retient un paquet d'aspect conseille : fabrique par l'ecran, donc partout. */
async function retenirUnDeckDAspect(page: Page, rang: number): Promise<string> {
  const bascule = page.locator('#deck-liste .deck-aspects-bascule', { hasText: /aspect/i })
  await expect(bascule, "Le depliage des paquets d'aspect a disparu.").toBeVisible()
  await bascule.click()
  const option = page.locator('#deck-liste .deck-aspects.est-deplie .tb-deck').nth(rang)
  await option.scrollIntoViewIfNeeded()
  const nom = (await option.locator('.do-name').innerText()).trim()
  await option.click()
  await expect(page.locator('#deck-liste .tb-deck.chosen .do-name')).toHaveText(nom)
  return nom
}

test.beforeAll(async ({ request }) => {
  for (const c of await campagnes(request)) {
    if (c.nom === NOM_CAMPAGNE) await request.post('/delete_campagne', { data: { id: c.id } })
  }
})

test.afterAll(async ({ request }) => {
  if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
})

test.describe.serial('Campagne : les cartes que le carnet impose au deck', () => {
  test('La campagne temoin de Sinister Motives se cree', async ({ page, request }) => {
    await page.goto('/campagne.html', { waitUntil: 'networkidle' })
    await page.getByRole('button', { name: /nouvelle campagne/i }).click()
    await page.locator('.cmp-boite', { hasText: /sinistre|sinister/i }).first().click()
    await page.locator('.cmp-saisie').fill(NOM_CAMPAGNE)
    await page.getByRole('button', { name: /choisir l'équipe/i }).click()

    await expect(page.locator('.campagne-bandeau')).toContainText(NOM_CAMPAGNE, { timeout: 30000 })
    await page.getByRole('button', { name: HEROS }).first().click()
    await validerOptionsDuHeros(page)
    await allerAuxDecks(page)
    await page.getByRole('button', { name: /valider l'équipe/i }).click()

    await expect(page.locator('.cmp-page-campagne')).toBeVisible()
    await expect(page.locator('.cmp-erreur')).toHaveCount(0)

    const creee = (await campagnes(request)).filter((c) => c.nom === NOM_CAMPAGNE)
    expect(creee, "La creation n'a pas produit exactement une campagne.").toHaveLength(1)
    identifiant = creee[0].id
  })

  test('Carte imposee absente du nouveau deck : refus, et rien n est ecrit', async ({
    page,
    request,
  }) => {
    await inscrireAuCarnet(request, CARTE_HORS_DECK)
    const avant = await laNotre(request)

    await ouvrirLaCampagne(page)
    await page.getByRole('button', { name: /modifier les decks/i }).click()
    await allerAuxDecks(page)
    await retenirUnDeckDAspect(page, 0)
    await page.getByRole('button', { name: /valider les decks/i }).click()

    // Le message nomme la carte : un refus qui ne dit pas laquelle laisserait le
    // joueur devant un ecran de preparation sans savoir quoi remettre.
    const erreur = page.locator('.cmp-erreur')
    await expect(erreur, 'La modification est passee alors que la carte imposee a disparu.')
      .toContainText(/carnet/i)
    await expect(erreur).toContainText(CARTE_HORS_DECK)

    const apres = await laNotre(request)
    expect(apres.equipe, 'Le refus a quand meme ecrit l equipe.').toEqual(avant.equipe)
  })

  test('Carte imposee toujours la : la modification passe', async ({ page, request }) => {
    // Une carte du deck actuel, et on revalide ce meme deck : la carte reste
    // donc en place. C'est le temoin du cas precedent — sans lui, un controle
    // qui refuserait TOUT passerait pour bon.
    const avant = await laNotre(request)
    const presente = (avant.equipe![0].deck.player_deck ?? [])[0]
    expect(presente, 'Le deck de la campagne est vide : rien a inscrire au carnet.').toBeTruthy()
    await inscrireAuCarnet(request, presente!)

    await ouvrirLaCampagne(page)
    await page.getByRole('button', { name: /modifier les decks/i }).click()
    await allerAuxDecks(page)
    const enCours = page.locator('#deck-liste .tb-deck', { hasText: /campagne|campaign/i }).first()
    await expect(enCours, "Le deck en cours de la campagne n'est pas propose.").toBeVisible()
    await enCours.click()
    await page.getByRole('button', { name: /valider les decks/i }).click()

    await expect(
      page.locator('.cmp-erreur'),
      'La modification a ete refusee alors que la carte imposee etait toujours dans le deck.'
    ).toHaveCount(0)
    await expect(page.locator('.cmp-page-campagne')).toBeVisible()

    const apres = await laNotre(request)
    expect(empreinte(apres.equipe![0]), 'Le deck enregistre n est pas celui qui etait retenu.')
      .toBe(empreinte(avant.equipe![0]))
  })
})
