import { describe, expect, it } from 'vitest'
import {
  NOM_OPTION_MANIGANCE,
  maniganceAMontrer,
  ouvertureEncoreVoilee,
  questionDeLaManigance,
} from './manigance-face-a'
import type { Demande, Option } from './ask'
import type { World } from './world'

function option(nom: string): Option {
  return {
    id: 7,
    name: nom,
    bind_id: 0,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
}

function demande(options: Option[]): Demande {
  return {
    options,
    refus: [],
    prompt_text: '',
    event_name: '',
    show_cancel: false,
    ability_type: '',
  }
}

describe('questionDeLaManigance', () => {
  it('reconnaît la question du moteur à son nom technique', () => {
    const trouvee = questionDeLaManigance(demande([option(NOM_OPTION_MANIGANCE)]))
    expect(trouvee?.id).toBe(7)
  })

  it('ne se déclenche pas sur une autre question', () => {
    expect(questionDeLaManigance(demande([option('Attack')]))).toBeUndefined()
  })

  it('ne se déclenche pas quand le moteur ne demande rien', () => {
    expect(questionDeLaManigance(undefined)).toBeUndefined()
  })

  it("refuse une question qui porte AUSSI d'autres options", () => {
    // Une option de plus veut dire que ce n'est pas notre moment : on ne
    // détourne pas une question à laquelle le joueur doit vraiment répondre.
    const melange = demande([option(NOM_OPTION_MANIGANCE), option('Attack')])
    expect(questionDeLaManigance(melange)).toBeUndefined()
  })
})

describe('maniganceAMontrer', () => {
  it('rend la manigance principale en jeu', () => {
    const monde = {
      area_schemes_main: [{ id: 48, card_id: '01097a', name: 'The Break-In!' }],
    } as unknown as World
    expect(maniganceAMontrer(monde)?.card_id).toBe('01097a')
  })

  it('rend undefined quand la zone est vide', () => {
    const monde = { area_schemes_main: [] } as unknown as World
    expect(maniganceAMontrer(monde)).toBeUndefined()
  })

  it('rend undefined sans monde', () => {
    expect(maniganceAMontrer(undefined)).toBeUndefined()
  })
})

describe('ouvertureEncoreVoilee', () => {
  const base = {
    confirmAttendue: true,
    round: 0,
    questionArrivee: false,
    dejaLevee: false,
    demandePresente: false,
  }

  it('voile la table pendant que le moteur monte la partie', () => {
    // Le cas nominal, celui qui doit CONTINUER de voiler : la regle est
    // posee, le moteur n'a encore rien demande, personne n'a rien vu.
    expect(ouvertureEncoreVoilee(base)).toBe(true)
  })

  it('leve le voile des que le moteur demande QUOI QUE CE SOIT au joueur', () => {
    // Si le moteur pose une question au joueur, le joueur doit pouvoir voir sa
    // table pour y repondre. Sans cette porte, un second siege (qui ne recoit
    // jamais la question de la manigance, reservee au premier joueur) reste
    // voile sur son propre mulligan.
    expect(ouvertureEncoreVoilee({ ...base, demandePresente: true })).toBe(false)
  })

  it('⚠ UN RECHARGEMENT DE PAGE ENTRE LE OK ET LE PREMIER ROUND NE BLOQUE PAS LA PARTIE', () => {
    // LE CAS QUI COMPTE. Apres le OK, la question est consommee, le mulligan
    // est en cours et `round_id` vaut encore 0 (world.py:573). Au remontage du
    // composant, le verrou « deja levee » repart a faux : sans la porte
    // ci-dessus, le voile ne se leverait plus JAMAIS et le joueur ne pourrait
    // plus repondre a son mulligan.
    const apresRechargement = {
      confirmAttendue: true,
      round: 0,
      questionArrivee: false,
      dejaLevee: false,
      demandePresente: true,
    }
    expect(ouvertureEncoreVoilee(apresRechargement)).toBe(false)
  })

  it('lève le voile quand la question arrive', () => {
    expect(ouvertureEncoreVoilee({ ...base, questionArrivee: true })).toBe(false)
  })

  it('ne revoile jamais une fois levé', () => {
    expect(ouvertureEncoreVoilee({ ...base, dejaLevee: true })).toBe(false)
  })

  it("ne voile pas une partie qui n'attend aucune question", () => {
    // Sauvegarde antérieure au 15/09/2026, ou puzzle : la règle n'est pas
    // posée, la question ne viendra jamais. Sans cette porte, le plateau
    // resterait voilé pour toujours.
    expect(ouvertureEncoreVoilee({ ...base, confirmAttendue: false })).toBe(false)
  })

  it('ne voile pas une partie déjà commencée', () => {
    expect(ouvertureEncoreVoilee({ ...base, round: 3 })).toBe(false)
  })
})
