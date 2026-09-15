import { describe, expect, it } from 'vitest'
import {
  NOM_OPTION_ANNEXE,
  NOM_OPTION_MANIGANCE,
  demandeHorsPanneauManigance,
  priseDuPanneauManigance,
  maniganceAMontrer,
  ouvertureEncoreVoilee,
  questionDeLaManigance,
} from './manigance-face-a'
import type { Demande, Option } from './ask'
import { questionDansLePanneau } from './ou-va-la-question'
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
    partieFinie: false,
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
      partieFinie: false,
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

  it('⚠ UNE PARTIE FINIE PENDANT LA MISE EN PLACE LEVE LE VOILE', () => {
    // LE CAS QUI COMPTE, ET IL REND UNE PARTIE INJOUABLE.
    // `confirm_main_scheme` est un drapeau de REGLE, vrai pour toute la
    // partie, pas un « une confirmation est en attente ». Si le moteur termine
    // la partie pendant la mise en place (`is_game_over` aux etapes 11, 12 ou
    // 13 de world.py), `round_id` reste 0, aucune demande n'arrive, et le
    // retour anticipe du voile passe AVANT l'ecran de fin de partie :
    // l'affichage restait sur « Connexion a la partie… » pour toujours.
    const finieALaMiseEnPlace = {
      confirmAttendue: true,
      round: 0,
      questionArrivee: false,
      dejaLevee: false,
      demandePresente: false,
      partieFinie: true,
    }
    expect(ouvertureEncoreVoilee(finieALaMiseEnPlace)).toBe(false)
  })
})

describe('demandeHorsPanneauManigance', () => {
  /** Une table qui porte bien sa manigance principale : le panneau peut prendre. */
  const TABLE = {
    area_schemes_main: [{ id: 42, card_type: 'main_scheme', pic_id: '01097a' }],
  } as unknown as World

  it('retire la question du panneau de ce que la table lit', () => {
    // Si cette porte sautait, le menu de la manigance principale rouvrirait :
    // halo sur la carte, option au libelle technique brut, et en mode Detaille
    // un clic qui REPOND a la place du panneau.
    const demande = { options: [option(NOM_OPTION_MANIGANCE)] } as unknown as Demande
    expect(demandeHorsPanneauManigance(demande, TABLE)).toBeUndefined()
  })

  it('rend la MEME demande, a la reference pres, pour toute autre question', () => {
    // La reference compte : un objet neuf a chaque rendu invaliderait les
    // dependances de hook de `useInteraction` et rejouerait la composition en
    // cours a chaque trame.
    const demande = { options: [option('Attack'), option('Thwart')] } as unknown as Demande
    expect(demandeHorsPanneauManigance(demande, TABLE)).toBe(demande)
  })

  it('laisse passer l absence de demande', () => {
    expect(demandeHorsPanneauManigance(undefined, TABLE)).toBeUndefined()
  })
})

// LE PANNEAU NE REVENDIQUE LA QUESTION QUE S'IL PEUT LA MONTRER.
//
// Defaut trouve en relecture le 15/09/2026, et il rend une partie INJOUABLE.
// La revendication (« cette question est prise, que personne d'autre ne
// l'affiche ») et le montage du panneau etaient deux conditions differentes :
// la premiere ne regardait que la question, la seconde exigeait AUSSI la
// carte. Quand `area_schemes_main` est vide ou absente, `maniganceAMontrer`
// rend `undefined` : le panneau ne paraissait pas, mais la barre du bas, le
// panneau central et la scene se taisaient tous les trois. Il ne restait plus
// rien pour repondre, et le moteur attendait pour toujours. Avant la vague, la
// barre affichait encore l'option.
describe('priseDuPanneauManigance', () => {
  const MANIGANCE = 42
  const AVEC_CARTE = {
    area_schemes_main: [{ id: MANIGANCE, card_type: 'main_scheme', pic_id: '01097a' }],
  } as unknown as World

  it('prend la question quand il a la carte a montrer', () => {
    const prise = priseDuPanneauManigance(demande([option(NOM_OPTION_MANIGANCE)]), AVEC_CARTE)
    expect(prise?.question.id).toBe(7)
    expect(prise?.carte.id).toBe(MANIGANCE)
  })

  it('⚠ NE PREND RIEN QUAND LA CARTE EST INTROUVABLE', () => {
    // LE CAS QUI COMPTE. Sans cette gate, la question restait « prise » par un
    // panneau qui ne paraissait jamais : plus un seul bouton a l'ecran.
    const sansZone = {} as unknown as World
    expect(priseDuPanneauManigance(demande([option(NOM_OPTION_MANIGANCE)]), sansZone)).toBeUndefined()
    const zoneVide = { area_schemes_main: [] } as unknown as World
    expect(priseDuPanneauManigance(demande([option(NOM_OPTION_MANIGANCE)]), zoneVide)).toBeUndefined()
    expect(priseDuPanneauManigance(demande([option(NOM_OPTION_MANIGANCE)]), undefined)).toBeUndefined()
  })

  it('ne prend pas une question ordinaire, meme avec une manigance en jeu', () => {
    expect(priseDuPanneauManigance(demande([option('Attack')]), AVEC_CARTE)).toBeUndefined()
  })

  it('rend la main aux panneaux ORDINAIRES quand il ne peut pas montrer la carte', () => {
    // La preuve que la partie reste jouable : la meme condition alimente la
    // demande que la table lit ET le drapeau de `ou-va-la-question.ts`. Si les
    // deux divergeaient, le joueur se retrouverait devant une question sans
    // aucun bouton.
    const question = demande([option(NOM_OPTION_MANIGANCE)])
    const sansZone = {} as unknown as World
    expect(demandeHorsPanneauManigance(question, sansZone)).toBe(question)
    expect(
      questionDansLePanneau({
        moteurAttendLeJoueur: true,
        demandePresente: true,
        effetEnCours: false,
        ciblage: false,
        menuCarte: false,
        sceneCentrale: false,
        phaseMechantEnCours: false,
        questionDeLaManigance: priseDuPanneauManigance(question, sansZone) !== undefined,
      })
    ).toBe(true)
  })

  it('retire bien la question de la table quand le panneau LA PREND', () => {
    const question = demande([option(NOM_OPTION_MANIGANCE)])
    expect(demandeHorsPanneauManigance(question, AVEC_CARTE)).toBeUndefined()
  })
})


// Avenant du 15/09/2026 : le meme panneau sert les manigances ANNEXES que le
// scenario met en jeu. Trace : Klaw pose « Defense Network » (01125) des sa
// mise en place, par la porte unique `SchemeSide2.OnPutIntoPlay`.
describe('la manigance ANNEXE', () => {
  it('est reconnue elle aussi', () => {
    const trouvee = questionDeLaManigance(demande([option(NOM_OPTION_ANNEXE)]))
    expect(trouvee?.id).toBe(7)
  })

  it('se cherche dans la zone des ANNEXES, pas des principales', () => {
    const monde = {
      area_schemes_main: [{ id: 48, card_id: '01116b' }],
      area_schemes_side: [{ id: 81, card_id: '01125' }],
    } as unknown as World
    expect(maniganceAMontrer(monde, 81)?.card_id).toBe('01125')
  })

  it('⚠ refuse toujours un nom qu on ne connait pas', () => {
    // Le temoin : sans lui, elargir la reconnaissance a deux noms pourrait
    // deraper en « n'importe quelle question a une option ».
    expect(questionDeLaManigance(demande([option('Reveal_Something_Else')]))).toBeUndefined()
  })
})
