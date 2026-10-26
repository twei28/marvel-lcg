// Les dix packs fan-made du 25-26/10/2026 livrent chacun leur propre Energy / Genius / Strength redessinées
// (« Max 1 per deck. », mêmes règles que 01088 / 01089 / 01090, seule l'image change). Arbitrage du 26/10/2026 :
// ce sont des ARTS ALTERNATIFS des ressources doubles (GUIDE-CREATION-CONTENU §12 bis), proposés comme collection
// au même titre que Gwenpool ou Beast. Wizard : `COLLECTIONS_RESSOURCES` (public/js/prepare/app.js), à garder aligné.
import { existsSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { collectionPourJoueur, picIdAffiche } from './variantes'

// [collection, [Energy, Genius, Strength]] : l'ordre est celui des trois ressources, PAS celui des numéros de carte
// (Warriors Three : wt023 est le Genius, wt024 l'Energy).
const PACKS: Array<[string, [string, string, string]]> = [
  ['roz', ['rz013', 'rz014', 'rz015']],
  ['batgirl', ['bg020', 'bg021', 'bg022']],
  ['batman', ['bm023', 'bm024', 'bm025']],
  ['corsair', ['cr017', 'cr018', 'cr019']],
  ['hepzibah', ['hz016', 'hz017', 'hz018']],
  ['raza', ['rl018', 'rl019', 'rl020']],
  ['chod', ['co017', 'co018', 'co019']],
  ['smasher', ['sz016', 'sz017', 'sz018']],
  ['warriors_three', ['wt024', 'wt023', 'wt025']],
  // Predator (RyCoRan) : pd021 Energy, pd022 Genius, pd023 Strength, meme traitement (26/10/2026, oubli de la premiere passe).
  ['predator', ['pd021', 'pd022', 'pd023']],
]

describe('collections de ressources des packs fan-made de fin octobre 2026', () => {
  it.each(PACKS)('%s : choisie pour un héros, elle est bien appliquée', (code) => {
    expect(collectionPourJoueur('65001a,65001b', 1, { '65001': code })).toBe(code)
  })

  it.each(PACKS)('%s : substitue les trois ressources dans le bon ordre (Energy, Genius, Strength)', (code, [energie, genie, force]) => {
    expect(picIdAffiche('01088', code)).toBe(energie)
    expect(picIdAffiche('01089', code)).toBe(genie)
    expect(picIdAffiche('01090', code)).toBe(force)
  })

  it.each(PACKS)('%s : ne touche à aucune autre carte', (code) => {
    expect(picIdAffiche('01094', code)).toBe('01094')
  })
})

// Le wizard (public/js/prepare/app.js) et le plateau lisent deux tables : un code connu d'un seul côté proposerait un art
// que l'autre n'affiche pas (GUIDE §12 bis : « les deux tables doivent rester alignées »).
const MOTEUR = join(dirname(fileURLToPath(import.meta.url)), '..', '..', '..', 'Fusion', 'marvel-lcg-src')
const APP_JS = readFileSync(join(MOTEUR, 'public', 'js', 'prepare', 'app.js'), 'utf8')

describe('alignement wizard / plateau et images livrées', () => {
  it.each(PACKS)('%s : déclarée dans COLLECTIONS_RESSOURCES du wizard', (code) => {
    expect(APP_JS).toMatch(new RegExp(`\\{ code: "${code}", nom: "[^"]+", apercu: "[a-z0-9]+" \\}`))
  })

  it.each(PACKS)('%s : les trois images existent dans assets/pics', (_code, ids) => {
    for (const id of ids) expect(existsSync(join(MOTEUR, 'assets', 'pics', `${id}.jpg`))).toBe(true)
  })
})
