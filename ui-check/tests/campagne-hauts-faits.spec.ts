// Terminer une campagne débloque un haut fait. La perdre, non.
//
// Le plateau affichait des hauts faits depuis longtemps, aucun ne récompensait
// une campagne menée à son terme — la chose la plus longue que le jeu propose.
//
// Ce test passe par le SERVEUR et pas par un banc en mémoire, pour une raison :
// la mesure traverse deux moitiés qui peuvent casser séparément. Le serveur
// résume les campagnes du disque (`resume_campagnes`, qui sait qu'une campagne
// perdue n'est pas gagnée), et `game/achievements.py` décide à partir de ce
// résumé sans jamais lire un fichier. Un banc sur l'une des deux ne prouverait
// rien sur l'autre.
//
//   npm run campagne-hauts-faits
//
// ATTENTION : ce test DÉBLOQUE réellement le haut fait « Chroniqueur » sur
// l'installation visée. Un haut fait débloqué ne se reprend pas. Il est écrit
// dans `achievements.json`, à côté du jeu servi — sur le serveur de
// développement c'est un artefact de `.game`, sans effet sur la partie du
// joueur. À ne pas lancer sur son installation de jeu.
import { test, expect, type APIRequestContext } from '@playwright/test'

const NOM = 'Essai automatique - hauts faits'
const SCENARIOS = ['sabretooth', 'project_wideawake', 'master_mold', 'mansion_attack', 'magneto']

type Haut = { cle: string; valeur: number; seuil: number; debloque: number | null }

let identifiant = ''

async function hautsFaits(request: APIRequestContext): Promise<Record<string, Haut>> {
  const reponse = await request.get('/get_achievements')
  expect(reponse.status()).toBe(200)
  const { hauts_faits } = (await reponse.json()) as { hauts_faits: Haut[] }
  return Object.fromEntries(hauts_faits.map((h) => [h.cle, h]))
}

async function poser(
  request: APIRequestContext,
  termines: string[],
  perdue = false
): Promise<string> {
  const reponse = await request.post('/save_campagne', {
    data: {
      campagne: {
        ...(identifiant ? { id: identifiant } : {}),
        code: 'mut_gen',
        nom: NOM,
        difficulte: 'standard',
        equipe: [{ heros: 'colossus', nomHeros: 'Colossus', identite: ['32001a,32001b'] }],
        termines,
        carnet: {},
        tentatives: {},
        partieEnCours: null,
        ...(perdue ? { perdue: true } : {}),
      },
    },
  })
  expect(reponse.status()).toBe(200)
  return (await reponse.json()).id as string
}

test.beforeAll(async ({ request }) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{
    id: string
    nom?: string
  }>
  for (const c of liste) {
    if (c.nom === NOM) await request.post('/delete_campagne', { data: { id: c.id } })
  }
})

test.afterAll(async ({ request }) => {
  if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
})

test.describe.serial('Hauts faits de campagne', () => {
  test('Une campagne en cours ne compte pas', async ({ request }) => {
    identifiant = await poser(request, SCENARIOS.slice(0, 4))
    const h = await hautsFaits(request)

    expect(h['campagne_1'], "Le haut fait « Chroniqueur » n'est pas servi.").toBeTruthy()
    expect(
      h['campagne_1'].valeur,
      'Quatre scénarios sur cinq comptent déjà comme une campagne terminée.'
    ).toBe(0)
  })

  test('Terminer les cinq scénarios débloque Chroniqueur', async ({ request }) => {
    await poser(request, SCENARIOS)
    const h = await hautsFaits(request)

    expect(h['campagne_1'].valeur, 'La campagne terminée n’est pas comptée.').toBe(1)
    expect(
      h['campagne_1'].debloque,
      'La campagne est comptée mais le haut fait n’a pas été débloqué : ' +
        '/save_campagne n’a pas déclenché l’évaluation.'
    ).toBeTruthy()
    // Une seule boîte : les deux autres restent hors de portée.
    expect(h['campagne_boites_3'].valeur).toBe(1)
    expect(h['campagne_experte'].valeur, 'Une campagne STANDARD a compté comme experte.').toBe(0)
  })

  test('Perdue au dernier scénario, elle ne compte plus', async ({ request }) => {
    await poser(request, SCENARIOS, true)
    const h = await hautsFaits(request)

    expect(
      h['campagne_1'].valeur,
      'Une campagne perdue au dernier scénario compte comme terminée.'
    ).toBe(0)
    // Le haut fait déjà débloqué, lui, reste acquis : c'est la progression
    // qui est vivante, pas le déblocage.
    expect(h['campagne_1'].debloque).toBeTruthy()
  })
})
