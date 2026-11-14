// Les cas viennent des six livrets officiels, relevés page par page :
//
//   trors p.15, mts p.25, sm p.17, mut_gen p.19, next_evol p.18
//     « Expert Campaign Only: If the players lose this game, … and the players
//       lose the campaign. »
//   aoa p.20
//     « If the Protect the Professor MISSION side scheme was defeated, the
//       players saved Professor X and win the campaign! If [it] was not
//       defeated, … lose the campaign. »
//
// Ce qui compte ici est autant ce qui PERD la campagne que ce qui ne la perd
// pas : perdre un scénario intermédiaire se rejoue, et perdre le dernier en
// mode standard aussi. Une règle trop large effacerait la progression de
// quelqu'un sans aucun moyen de la lui rendre.
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, expect, it } from 'vitest'
import { verdictDeCampagne, type RegleDefaite } from './defaite-campagne'

const DEFAITE_EXPERTE: RegleDefaite = {
  quand: 'partie_perdue',
  expert_seulement: true,
  texte: 'Crâne Rouge conquiert le monde.',
}

const MISSION_AOA: RegleDefaite = {
  quand: 'cle_absente',
  cle: 'Professor Saved',
  texte: "Vous n'avez pas sauvé le Professeur X.",
}

const base = {
  final: true,
  gagne: false,
  expert: true,
  carnet: {} as Record<string, string>,
}

describe('Les cinq boîtes : perdre le dernier scénario en campagne experte', () => {
  it('perd la campagne, et rend le texte du livret', () => {
    const v = verdictDeCampagne({ ...base, regle: DEFAITE_EXPERTE })
    expect(v.perdue).toBe(true)
    expect(v.texte).toBe('Crâne Rouge conquiert le monde.')
  })

  it('ne perd rien en campagne standard : le scénario se rejoue', () => {
    expect(verdictDeCampagne({ ...base, regle: DEFAITE_EXPERTE, expert: false }).perdue).toBe(false)
  })

  it('ne perd rien si la partie est gagnée', () => {
    expect(verdictDeCampagne({ ...base, regle: DEFAITE_EXPERTE, gagne: true }).perdue).toBe(false)
  })

  it('ne perd rien sur un scénario intermédiaire, même perdu en expert', () => {
    expect(verdictDeCampagne({ ...base, regle: DEFAITE_EXPERTE, final: false }).perdue).toBe(false)
  })

  it('ne perd rien si le scénario ne déclare aucune règle', () => {
    expect(verdictDeCampagne({ ...base, regle: null }).perdue).toBe(false)
  })
})

describe("AoA : la campagne se perd sur la mission, pas sur la défaite", () => {
  it('perd la campagne quand le Professeur n a pas été sauvé, même en standard', () => {
    const v = verdictDeCampagne({ ...base, regle: MISSION_AOA, gagne: true, expert: false })
    expect(v.perdue).toBe(true)
    expect(v.texte).toBe("Vous n'avez pas sauvé le Professeur X.")
  })

  it('ne perd rien quand la clé est au carnet', () => {
    const carnet = { 'Professor Saved': '1' }
    expect(verdictDeCampagne({ ...base, regle: MISSION_AOA, gagne: true, carnet }).perdue).toBe(false)
  })

  it("traite '0' et la chaîne vide comme une mission non accomplie", () => {
    for (const valeur of ['0', '']) {
      const carnet = { 'Professor Saved': valeur }
      expect(verdictDeCampagne({ ...base, regle: MISSION_AOA, gagne: true, carnet }).perdue).toBe(true)
    }
  })

  it('ne perd JAMAIS une campagne sur une règle sans clé déclarée', () => {
    const bancale: RegleDefaite = { quand: 'cle_absente' }
    expect(verdictDeCampagne({ ...base, regle: bancale, gagne: true }).perdue).toBe(false)
  })
})

// La ville ne dort jamais (MC×DC 2026, p.11 du livret FR) : « DÉFAITE : Le Caïd reste le roi de New York… Vous avez perdu la campagne. »
// Décision de l'utilisateur du 22/10/2026 : perdue TOUJOURS (standard comme expert), malgré la règle générale de réessai de l'introduction.
describe('La ville ne dort jamais : défaite au combat 4', () => {
  const definition = JSON.parse(
    readFileSync(resolve(__dirname, '../../../../Fusion/marvel-lcg-src/data/campagnes/punisher_mcdc_2026.json'), 'utf8')
  ) as { scenarios: Array<{ id: string; defaite?: RegleDefaite }> }
  const dernier = definition.scenarios[definition.scenarios.length - 1]!
  const faits = { final: true, regle: dernier.defaite, gagne: false, expert: false, carnet: {} }

  it('Kingsfall est le dernier combat et porte la règle', () => {
    expect(dernier.id).toBe('kingsfall')
    expect(dernier.defaite?.quand).toBe('partie_perdue')
    expect(dernier.defaite?.expert_seulement).toBe(false)
  })
  it('perdre Kingsfall perd la campagne, en standard comme en expert, avec la phrase du livret', () => {
    expect(verdictDeCampagne(faits).perdue).toBe(true)
    expect(verdictDeCampagne(faits).texte).toContain('Vous avez perdu la campagne')
    expect(verdictDeCampagne({ ...faits, expert: true }).perdue).toBe(true)
  })
  it('gagner Kingsfall ne perd pas la campagne', () => {
    expect(verdictDeCampagne({ ...faits, gagne: true }).perdue).toBe(false)
  })
  it('perdre un combat intermédiaire se rejoue : aucune règle sur les combats 1 à 3', () => {
    for (const s of definition.scenarios.slice(0, 3)) {
      expect(s.defaite).toBeUndefined()
      expect(verdictDeCampagne({ ...faits, final: false, regle: s.defaite }).perdue).toBe(false)
    }
  })
})
