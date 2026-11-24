// The Vault (Kajislav, `vt001`-`vt034`) : ce que le plateau DESSINE (PROCESSUS-CARTE étape 8 bis).
// `tools/cas/the_vault*.py` prouvent ce que le moteur FAIT. Ici, ce que le joueur REGARDE :
//   - plusieurs vilains en jeu en même temps (zone des vilains) ;
//   - vt018 The Vault : vilains et sbires glissés SOUS l'environnement, face cachée ;
//   - vt020 Craven Escape : attachement de rencontre posé sur un des vilains ;
//   - vt019 Inspection of the Vault : obligation en jeu devant le premier joueur ;
//   - vt026 Burglary : manigance annexe à Crise, menace dessinée.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const INSPECTION = 2
const BATROC = 10
const MENTALLO = 11
const FUITE = 12
const VAULT = 20
const SOUS_VILAIN = 21
const SOUS_SBIRE = 22
const CAMBRIOLAGE = 30

const monde = () =>
  tableAvec(
    siege({
      area_hero: [carte(IDENTITE, '01001b', 'AlterEgo', 'Peter Parker')],
      obligations_area: [carte(INSPECTION, 'vt019', 'Obligation', 'Inspection of the Vault')],
    }),
    {
      area_villain: [
        carte(BATROC, 'vt001', 'EncounterVillain', 'Batroc'),
        carte(MENTALLO, 'vt003', 'EncounterVillain', 'Mentallo'),
        carte(FUITE, 'vt020', 'Attachment', 'Craven Escape', { bind_object_id: BATROC }),
      ],
      area_environment: [
        carte(VAULT, 'vt018', 'Environment', 'The Vault'),
        carte(SOUS_VILAIN, 'vt005', 'EncounterVillain', 'Grey Gargoyle', { bind_object_id: VAULT, is_face_up: false }),
        carte(SOUS_SBIRE, '01103', 'Minion', 'Shocker', { bind_object_id: VAULT, is_face_up: false }),
      ],
      area_schemes_side: [carte(CAMBRIOLAGE, 'vt026', 'SideScheme', 'Burglary', { info: { k_threat: 3 } })],
    }
  )

describe('plusieurs vilains en jeu', () => {
  it('Batroc et Mentallo sont dessinés tous les deux', () => {
    expect(dessinee(monde(), BATROC)).toBeDefined()
    expect(dessinee(monde(), MENTALLO)).toBeDefined()
  })
})

describe('vt018 The Vault : cartes glissées dessous', () => {
  it('l environnement est dessiné', () => {
    expect(dessinee(monde(), VAULT)).toBeDefined()
  })

  it('le vilain et le sbire glissés dessous sont dessinés, juste derrière l environnement', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(monde(), SOUS_VILAIN)).toBeDefined()
    expect(dessinee(monde(), SOUS_SBIRE)).toBeDefined()
    expect(rang(SOUS_VILAIN)).toBeGreaterThan(rang(VAULT))
    expect(rang(SOUS_SBIRE)).toBeGreaterThan(rang(VAULT))
  })
})

describe('vt020 Craven Escape', () => {
  it('est dessinée, portée par Batroc', () => {
    expect(dessinee(monde(), FUITE)).toBeDefined()
    expect(dessinee(monde(), FUITE)?.portePar).toBe(BATROC)
  })
})

describe('vt019 Inspection of the Vault', () => {
  it('l obligation est dessinée', () => {
    expect(dessinee(monde(), INSPECTION)).toBeDefined()
  })
})

describe('vt026 Burglary', () => {
  it('manigance annexe dessinée avec sa menace', () => {
    expect(dessinee(monde(), CAMBRIOLAGE)).toBeDefined()
    expect(dessinee(monde(), CAMBRIOLAGE)?.menace).toBe(3)
  })
})
