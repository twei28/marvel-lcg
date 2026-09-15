import { describe, expect, it } from 'vitest'
import {
  NOM_OPTION_MANIGANCE,
  demandeHorsPanneauManigance,
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
  /** Mode Bataille (21098a) : deux manigances principales en jeu ensemble. */
  const deuxManigances = {
    area_schemes_main: [
      { id: 48, card_id: '21098b', name: 'Déjà retournée' },
      { id: 49, card_id: '21099a', name: 'Celle que le moteur montre' },
    ],
  } as unknown as World

  it('rend la manigance que la question DESIGNE, par son bind_id', () => {
    const monde = {
      area_schemes_main: [{ id: 48, card_id: '01097a', name: 'The Break-In!' }],
    } as unknown as World
    expect(maniganceAMontrer(monde, 48)?.card_id).toBe('01097a')
  })

  it('⚠ AVEC DEUX MANIGANCES PRINCIPALES, MONTRE LA BONNE', () => {
    // LE CAS QUI COMPTE. A la mise en place, le moteur boucle sur TOUTES les
    // manigances principales (world.py:546) et pose donc deux questions
    // d'affilee. A la seconde, l'index 0 porte la carte DEJA RETOURNEE : le
    // panneau montrait la mauvaise carte, et la face B par-dessus le marche.
    //
    // Le moteur remplit `bind_id` avec l'objet qui porte l'effet
    // (effect.py:600, `bind_id = the_effect.this.card.object_id`) ; notre
    // capacite est construite sur `GameRule(scheme)`, donc `bind_id` EST la
    // manigance a montrer. On ne devine plus, on demande a la question.
    expect(maniganceAMontrer(deuxManigances, 49)?.card_id).toBe('21099a')
  })

  it('se replie sur la zone quand bind_id ne designe aucune carte connue', () => {
    // Repli explicite : mieux vaut la premiere manigance de la zone qu'aucun
    // panneau du tout, qui laisserait le moteur attendre sans bouton.
    expect(maniganceAMontrer(deuxManigances, 0)?.card_id).toBe('21098b')
    expect(maniganceAMontrer(deuxManigances, undefined)?.card_id).toBe('21098b')
  })

  it('rend undefined quand la zone est vide', () => {
    const monde = { area_schemes_main: [] } as unknown as World
    expect(maniganceAMontrer(monde, 48)).toBeUndefined()
  })

  it('rend undefined sans monde', () => {
    expect(maniganceAMontrer(undefined, 48)).toBeUndefined()
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

describe('demandeHorsPanneauManigance', () => {
  it('retire la question du panneau de ce que la table lit', () => {
    // Si cette porte sautait, le menu de la manigance principale rouvrirait :
    // halo sur la carte, option au libelle technique brut, et en mode Detaille
    // un clic qui REPOND a la place du panneau.
    const demande = { options: [option(NOM_OPTION_MANIGANCE)] } as unknown as Demande
    expect(demandeHorsPanneauManigance(demande)).toBeUndefined()
  })

  it('rend la MEME demande, a la reference pres, pour toute autre question', () => {
    // La reference compte : un objet neuf a chaque rendu invaliderait les
    // dependances de hook de `useInteraction` et rejouerait la composition en
    // cours a chaque trame.
    const demande = { options: [option('Attack'), option('Thwart')] } as unknown as Demande
    expect(demandeHorsPanneauManigance(demande)).toBe(demande)
  })

  it('laisse passer l absence de demande', () => {
    expect(demandeHorsPanneauManigance(undefined)).toBeUndefined()
  })
})
