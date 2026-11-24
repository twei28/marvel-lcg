// Hellfire Hunt (Dipsome), scénario 5 « Cassandra Nova », livret p.16 :
//   « Expert Campaign Only: If the players lose this game, Cassandra Nova eliminates all mutants and the players lose the campaign. »
//   « Victory: Cassandra Nova is defeated, the players win the campaign! »
// Le champ `defaite` du dernier scénario est LU dans le vrai fichier de campagne (jamais en dur ici) : si quelqu'un l'enlève, ce test tombe.
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, expect, it } from 'vitest'
import { verdictDeCampagne, type RegleDefaite } from './defaite-campagne'

const campagne = JSON.parse(
  readFileSync(resolve(__dirname, '../../../../Fusion/marvel-lcg-src/data/campagnes/hellfire_hunt.json'), 'utf8'),
) as { scenarios: Array<{ id: string; numero: number; final?: boolean; defaite?: RegleDefaite }> }

const nova = campagne.scenarios.find((s) => s.id === 'hellfire_cassandra_nova')

describe('Hellfire Hunt : perdre Cassandra Nova', () => {
  it('le dernier scénario déclare la règle du livret (expert seulement, partie perdue)', () => {
    expect(nova?.numero).toBe(5)
    expect(nova?.final).toBe(true)
    expect(nova?.defaite).toMatchObject({ quand: 'partie_perdue', expert_seulement: true })
  })

  it('EN EXPERT, une défaite perd la CAMPAGNE et rend le texte du livret', () => {
    const v = verdictDeCampagne({ final: true, regle: nova?.defaite, gagne: false, expert: true, carnet: {} })
    expect(v.perdue).toBe(true)
    expect(v.texte).toContain('Cassandra Nova')
  })

  it('en STANDARD, une défaite se rejoue sans pénalité', () => {
    expect(verdictDeCampagne({ final: true, regle: nova?.defaite, gagne: false, expert: false, carnet: {} }).perdue).toBe(false)
  })

  it('la VICTOIRE ne perd jamais la campagne, expert ou non', () => {
    expect(verdictDeCampagne({ final: true, regle: nova?.defaite, gagne: true, expert: true, carnet: {} }).perdue).toBe(false)
    expect(verdictDeCampagne({ final: true, regle: nova?.defaite, gagne: true, expert: false, carnet: {} }).perdue).toBe(false)
  })

  it('un scénario INTERMÉDIAIRE perdu en expert se rejoue (aucun des quatre premiers ne porte la règle)', () => {
    for (const s of campagne.scenarios.filter((x) => x.numero < 5)) {
      expect(s.defaite).toBeUndefined()
      expect(verdictDeCampagne({ final: false, regle: s.defaite, gagne: false, expert: true, carnet: {} }).perdue).toBe(false)
    }
  })
})
