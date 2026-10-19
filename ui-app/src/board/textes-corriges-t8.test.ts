// T8 (19/10/2026) : textes non traduits ou internes de « Sur la table ».
import { describe, expect, it } from 'vitest'
import { traduireMoteur } from './vocabulaire-moteur'
import { phraseHistorique } from './PhaseDynamique'
import { etapeEnLangue } from './etape-en-langue'
import { calculCoupTable } from './calcul-coup-table'
import type { EtapeDeroule } from './deroule-phase'

const base: EtapeDeroule = { cle: 'x', temps: 'mechant', titre: 'stade-revele', regle: '', boosts: [] }

describe('« stade-revele » ne s’affiche jamais sous sa clé interne', () => {
  it('dit « Klaw passe au stade 2 »', () => {
    expect(phraseHistorique({ ...base, cibleNom: 'Klaw' }, 2)).toBe('Klaw passe au stade 2')
  })
  it('sans numéro connu : « passe au stade suivant »', () => {
    expect(phraseHistorique({ ...base, cibleNom: 'Klaw' })).toBe('Klaw passe au stade suivant')
  })
  it('sans nom : une phrase vague mais française, jamais la clé', () => {
    expect(phraseHistorique(base)).not.toMatch(/stade-revele/)
  })
})

describe('les titres et options du moteur sont en français', () => {
  it('« Ally Limit »', () => {
    expect(traduireMoteur('Ally Limit')).toBe('Limite d’alliés')
  })
  it('Ultron : le texte de règle de la réponse forcée (traduction tirée de son texte français)', () => {
    expect(traduireMoteur('Put the top card of your deck into play facedown, engaged with you as a Drone minion')).toBe(
      'Mettre en jeu la carte du dessus de ton deck, face cachée, engagée avec toi en tant que sbire Drone'
    )
  })
  it('Lay the Beatdown : les deux options (texte français de tk022)', () => {
    expect(traduireMoteur('Deal 2 indirect damage to your hero')).toBe('Infliger 2 dégâts indirects à ton héros')
    expect(traduireMoteur('Stun your hero')).toBe('Sonner ton héros')
  })
})

describe('la source d’une réduction porte le nom français de la carte, comme sur la table', () => {
  const etape: EtapeDeroule = {
    cle: 'a', temps: 'mechant', titre: 'attaque', regle: '', etat: 'resolu', base: 4, baseImprimee: 4, montant: 3, boosts: [], defense: 0,
    reductions: [{ source: 'Energy Barrier', valeur: 1, source_id: 77 }],
  }
  it('Energy Barrier -> Barrière Énergétique dans le calcul', () => {
    const fr = etapeEnLangue(etape, (id) => (id === 77 ? 'Barrière Énergétique' : undefined))
    expect(calculCoupTable(fr)).toContain('− 1 Barrière Énergétique')
    expect(calculCoupTable(fr)).not.toContain('Energy Barrier')
  })
  it('sans identifiant (moteur ancien) : le nom du moteur, inchangé', () => {
    const fr = etapeEnLangue({ ...etape, reductions: [{ source: 'Energy Barrier', valeur: 1 }] }, () => undefined)
    expect(calculCoupTable(fr)).toContain('Energy Barrier')
  })
})
