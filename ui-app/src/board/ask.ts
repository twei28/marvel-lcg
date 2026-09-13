// Ce que le moteur demande au joueur, et comment on lui repond.
//
// Contrat releve sur le moteur (src/game/render/descriptor/effect.py) et sur le
// runtime historique qui le consomme (public/js/marvel/data.js) :
//
//   GET  /get_ask?p=<joueur>   -> { options_json, prompt_text, event_name,
//                                   show_cancel, ability_type, ... }
//   POST /post?p=<joueur>      <- {"id":<option>,"targets":[...],"resources":[...]}
//                                 ou {} pour annuler / passer
//
// Une OPTION est une capacite proposee : jouer une carte, activer un pouvoir,
// terminer son tour. Elle est portee par une carte (bind_id), demande entre
// target_num_range[0] et [1] cibles parmi all_legal_targets, et peut couter des
// ressources (target_payment).

/** Un moyen de payer : un effet de ressource, et le type qu'il fournit. */
export type MoyenDePaiement = {
  effect_id: number
  res_text: string
}

/**
 * « Paye sans cette couleur, ce coup ne produira aucun effet. »
 *
 * Envoye par le moteur (`Effect.Render`, champ `warning`) quand la cible est
 * verrouillee par un mot-cle que la carte n'ignore QU'A CONDITION d'avoir ete
 * payee d'une certaine couleur (Crisis Averted sous une Crise : une mentale).
 * Le plateau ne connait ni la carte ni la regle : il compare les lettres du
 * paiement choisi a `ressource`, et demande confirmation si aucune ne convient.
 */
export type Avertissement = {
  /** Le mot-cle qui verrouille la cible : « Crisis », « Patrol ». */
  mot_cle: string
  /** La couleur exigee, en lettre moteur : R, B, Y, G, L. */
  ressource: string
  /** true : TOUT le paiement doit etre de cette couleur (« using only
   *  [mental] ») ; false : une seule suffit. */
  seulement: boolean
}

/** Le cout d'une cible donnee, et de quoi le payer. */
export type Paiement = {
  /** Cout imprime, tel quel. Souvent un nombre, parfois vide. */
  cost: string
  payment: MoyenDePaiement[]
  /** « UpTo », « SameType », « DifferentType »... */
  rule: string[]
  /** Absent dans l'immense majorite des cas. Voir `Avertissement`. */
  avertissement?: Avertissement
}

export type Option = {
  id: number
  name: string
  /** Carte porteuse de l'option, 0 si aucune. */
  bind_id: number
  bind_player_id: number
  /** Cibles legales, par identifiant d'objet. Les doublons signalent un X. */
  all_legal_targets: number[]
  /** [minimum, maximum] de cibles a choisir. */
  target_num_range: [number, number]
  /** Cout par cible. La cle 0 est le cout quand il n'y a pas de cible. */
  target_payment: Partial<Record<number, Paiement>>
  select_rule: string
  target_must_include_traits: string[]
  /** Renseigne par le moteur quand l'option n'est pas jouable. */
  failure_reason: string
  is_search: boolean
}

export type Demande = {
  options: Option[]
  /**
   * Les options ECARTEES par le moteur, avec leur motif dans
   * `failure_reason`. Canal SEPARE (`refus_json`), voir
   * `Controller.RendreLesRefus` cote moteur.
   *
   * ⚠ NE JAMAIS LES MELER A `options`. Elles ne servent QU'A EXPLIQUER au
   * joueur pourquoi une carte est injouable ; rien ne doit s'en servir pour
   * decider quoi que ce soit. Le jour ou l'une d'elles se retrouve dans une
   * liste de choix, le joueur pourra tenter un coup que le moteur refuse.
   */
  refus: Option[]
  prompt_text: string
  event_name: string
  show_cancel: boolean
  ability_type: string
}

/** Reponse a poster au moteur. */
export type Reponse = {
  id: number
  targets: number[]
  resources: number[]
}

function nombre(valeur: unknown, defaut: number): number {
  return typeof valeur === 'number' && Number.isFinite(valeur) ? valeur : defaut
}

function texte(valeur: unknown): string {
  return typeof valeur === 'string' ? valeur : ''
}

/**
 * Les moyens de paiement arrivent sous deux formes selon la version du moteur :
 * soit { effect_id, res_text }, soit un objet a une seule cle { "<id>": "<type>" }.
 * Le runtime historique gere les deux, on fait pareil.
 */
function lireMoyen(brut: unknown): MoyenDePaiement | undefined {
  if (typeof brut !== 'object' || brut === null) return undefined
  const objet = brut as Record<string, unknown>

  if (typeof objet.effect_id === 'number') {
    return { effect_id: objet.effect_id, res_text: texte(objet.res_text) }
  }

  const cles = Object.keys(objet)
  if (cles.length !== 1) return undefined
  const id = Number(cles[0])
  return Number.isFinite(id) ? { effect_id: id, res_text: texte(objet[cles[0]!]) } : undefined
}

function lireAvertissement(brut: unknown): Avertissement | undefined {
  if (typeof brut !== 'object' || brut === null) return undefined
  const objet = brut as Record<string, unknown>
  const mot_cle = texte(objet.keyword)
  const ressource = texte(objet.paid_with).toUpperCase()
  const seulement = texte(objet.mode) === 'only'
  return mot_cle && ressource ? { mot_cle, ressource, seulement } : undefined
}

function lirePaiement(brut: unknown): Paiement {
  const objet = (typeof brut === 'object' && brut !== null ? brut : {}) as Record<string, unknown>
  const moyens = Array.isArray(objet.payment) ? objet.payment : []
  const avertissement = lireAvertissement(objet.warning)
  return {
    cost: texte(objet.cost),
    payment: moyens.map(lireMoyen).filter((m): m is MoyenDePaiement => m !== undefined),
    rule: Array.isArray(objet.rule) ? objet.rule.filter((r): r is string => typeof r === 'string') : [],
    ...(avertissement ? { avertissement } : {}),
  }
}

function lireOption(brut: unknown): Option | undefined {
  if (typeof brut !== 'object' || brut === null) return undefined
  const o = brut as Record<string, unknown>
  if (typeof o.id !== 'number') return undefined

  const cibles = Array.isArray(o.all_legal_targets)
    ? o.all_legal_targets.filter((x): x is number => typeof x === 'number')
    : []
  const plage = Array.isArray(o.target_num_range) ? o.target_num_range : []
  const min = nombre(plage[0], 0)
  const max = nombre(plage[1], 0)

  const paiements: Partial<Record<number, Paiement>> = {}
  const brutPaiements = (typeof o.target_payment === 'object' && o.target_payment !== null
    ? o.target_payment
    : {}) as Record<string, unknown>
  for (const [cle, valeur] of Object.entries(brutPaiements)) {
    const id = Number(cle)
    if (Number.isFinite(id)) paiements[id] = lirePaiement(valeur)
  }

  return {
    id: o.id,
    name: texte(o.name),
    bind_id: nombre(o.bind_id, 0),
    bind_player_id: nombre(o.bind_player_id, 0),
    // Un maximum de zero cible veut dire « aucune cible a choisir », meme si le
    // moteur en a liste : le runtime historique fait le meme menage.
    all_legal_targets: max === 0 ? [] : cibles,
    target_num_range: [min, max],
    target_payment: paiements,
    select_rule: texte(o.select_rule),
    target_must_include_traits: Array.isArray(o.target_must_include_traits)
      ? o.target_must_include_traits.filter((t): t is string => typeof t === 'string')
      : [],
    failure_reason: texte(o.failure_reason),
    is_search: o.is_search === true,
  }
}

/** Lit la reponse de /get_ask. Renvoie undefined quand le moteur ne demande rien. */
export function lireDemande(brut: unknown): Demande | undefined {
  if (typeof brut !== 'object' || brut === null) return undefined
  const o = brut as Record<string, unknown>
  if (typeof o.options_json !== 'string') return undefined

  let brutOptions: unknown
  try {
    brutOptions = JSON.parse(o.options_json)
  } catch {
    return undefined
  }
  if (!Array.isArray(brutOptions)) return undefined

  const options = brutOptions.map(lireOption).filter((x): x is Option => x !== undefined)
  if (options.length === 0) return undefined

  // Le canal des refus est FACULTATIF : un moteur plus ancien ne l'envoie pas,
  // et le plateau doit continuer de marcher sans lui. Pas de refus, pas de
  // raison affichee, rien d'autre ne change.
  let refus: Option[] = []
  if (typeof o.refus_json === 'string') {
    try {
      const brutRefus: unknown = JSON.parse(o.refus_json)
      if (Array.isArray(brutRefus)) {
        refus = brutRefus.map(lireOption).filter((x): x is Option => x !== undefined)
      }
    } catch {
      refus = []
    }
  }

  return {
    options,
    refus,
    prompt_text: texte(o.prompt_text),
    event_name: texte(o.event_name),
    show_cancel: o.show_cancel === true,
    ability_type: texte(o.ability_type),
  }
}

/**
 * Le cout a payer pour l'option, compte tenu des cibles deja choisies.
 * Reprend getN()/getCost() du runtime : le cout est indexe par la PREMIERE cible
 * choisie, ou par 0 quand l'option n'a pas de cible.
 */
export function paiementCourant(option: Option, cibles: number[]): Paiement | undefined {
  const premiere = cibles[0] ?? option.all_legal_targets[0] ?? 0
  return option.target_payment[premiere] ?? option.target_payment[0]
}

/** Nombre de ressources a depenser. undefined = le moteur en jugera. */
export function nombreDeRessources(paiement: Paiement | undefined): number | undefined {
  if (!paiement) return undefined
  return totalDuCout(paiement.cost)
}

/**
 * Combien de ressources coute un cout, cout MIXTE compris.
 *
 * Le moteur ecrit le cout en `color_text` (game/element/rbyg.py) : d'abord une
 * lettre par type EXIGE, puis le nombre de ressources libres. Une carte a
 * Requirement paie donc « Y1 » (Thunder Strike : cout 2, dont une energie) ou
 * « YYY2 » (Wrath of Olympus : cout 5, dont trois energies).
 *
 * ⚠ Sans cette lecture, `Number('Y1')` valait NaN : le plateau ne connaissait
 * plus le total, n'affichait aucune pastille de cout, annoncait « Payer le
 * cout » au lieu de « Payer 2 », et se disait pret des l'energie posee. Vu en
 * partie le 12/09/2026 sur Thunder Strike (« il me demande qu'une ressource »).
 * Dix-huit cartes du depot ont ce cout mixte.
 */
export function totalDuCout(cout: string): number | undefined {
  const n = Number(cout)
  if (Number.isInteger(n) && n >= 0) return n
  const decoupe = /^([RBYGLrbygl]*)(\d*)$/.exec(cout)
  if (!decoupe) return undefined
  const total = decoupe[1].length + (decoupe[2] ? Number(decoupe[2]) : 0)
  return total > 0 ? total : undefined
}

/** Nom lisible d'un type de ressource, pour dire au joueur ce qui manque. */
const NOM_TYPE: Record<string, string> = {
  R: 'physical',
  // B et Y etaient INVERSES. Le moteur est clair (game/element/resources.py) :
  // 'b' est mental et 'y' est energy. Le plateau annoncait donc « il te
  // manque 1 energy » quand il manquait une mentale, et l'inverse. Un joueur
  // qui s'y fie construit un modele faux de ses propres ressources.
  B: 'mental',
  Y: 'energy',
  G: 'wild',
  // L'eclair, ressource maison du pack Zeus (11/09/2026).
  L: 'lightning',
}

/**
 * Cout exprime en TYPES de ressources, et non en nombre.
 *
 * « Energy Shield » (04073, sur Crossbones) coute [energy][mental] : le moteur
 * l'ecrit « BY ». Deux ressources quelconques ne le paient pas, il en faut une
 * de chaque. Un cout ordinaire est un nombre (« 2 ») et ne rend rien ici.
 */
export function coutParType(cost: string): Record<string, number> | undefined {
  const lettres = cost.match(/[rbygl]/gi)
  if (!lettres) return undefined
  const exige: Record<string, number> = {}
  for (const lettre of lettres) {
    const type = lettre.toUpperCase()
    exige[type] = (exige[type] ?? 0) + 1
  }
  return exige
}

/**
 * Ce qui manque encore, type par type, pour honorer un cout par types.
 *
 * Les jokers [wild] bouchent n'importe quel trou : on les garde pour la fin,
 * sans quoi un joker depense sur un type deja couvert laisserait croire a un
 * manque ailleurs.
 */
export function typesManquants(
  paiement: Paiement | undefined,
  ressources: number[]
): Record<string, number> {
  const exige = paiement && coutParType(paiement.cost)
  if (!paiement || !exige) return {}

  const texteParEffet = new Map<number, string>()
  for (const moyen of paiement.payment) {
    if (!texteParEffet.has(moyen.effect_id)) texteParEffet.set(moyen.effect_id, moyen.res_text)
  }

  const fourni: Record<string, number> = {}
  for (const id of ressources) {
    for (const lettre of (texteParEffet.get(id) ?? '').match(/[rbygl]/gi) ?? []) {
      const type = lettre.toUpperCase()
      fourni[type] = (fourni[type] ?? 0) + 1
    }
  }

  const manquants: Record<string, number> = {}
  let jokers = fourni.G ?? 0
  for (const [type, nombre] of Object.entries(exige)) {
    // Un [wild] EXIGE se paie avec n'importe quoi : il est traite en dernier,
    // avec ce qui reste.
    if (type === 'G') continue
    const manque = Math.max(0, nombre - (fourni[type] ?? 0))
    const comble = Math.min(manque, jokers)
    jokers -= comble
    if (manque - comble > 0) manquants[type] = manque - comble
  }

  const jokersExiges = exige.G ?? 0
  if (jokersExiges > 0) {
    const surplus =
      Object.entries(fourni)
        .filter(([type]) => type !== 'G')
        .reduce((total, [type, n]) => total + Math.max(0, n - (exige[type] ?? 0)), 0) + jokers
    if (surplus < jokersExiges) manquants.G = jokersExiges - surplus
  }
  return manquants
}

/** « UpTo » : on peut payer moins que le cout imprime. */
export function paiementFacultatif(paiement: Paiement | undefined): boolean {
  return paiement?.rule.includes('UpTo') === true
}

/**
 * Combien de fois un meme effet de ressource peut etre depense.
 * Le moteur repete l'effet dans `payment` autant de fois qu'il est disponible.
 */
export function foisDisponible(paiement: Paiement | undefined, effectId: number): number {
  if (!paiement) return 0
  return paiement.payment.filter((moyen) => moyen.effect_id === effectId).length
}

/**
 * Combien de ressources fournit UN moyen de paiement.
 *
 * Le moteur encode une carte a double (ou triple) ressource comme un seul effet
 * dont le `res_text` porte plusieurs icones : « BB » = 2 mentales, « RRR » = 3
 * physiques, « G » = 1 joker. Le texte est deja nettoye cote moteur
 * (Symbol.Clean), il ne reste que les lettres de couleur R/B/Y/G/L. La valeur est
 * donc le nombre de ces lettres. Un effet sans lettre lisible vaut 1 (au moins
 * une ressource, comme l'ancien comptage).
 *
 * ⚠ SAUF UNE REDUCTION DE COUT, qui n'a aucune icone. Le moteur l'ecrit en
 * NEGATIF : « -3 » pour Star-Lord (`Resources.color_text`,
 * game/element/resources.py:55), qui reduit de 3 le cout de la carte jouee.
 * Elle tombait donc dans le repli « au moins 1 » et ne valait qu'UNE ressource :
 * Element Gun, qui coute 3, restait bloquee a 1/3. Signale en partie par Yarro
 * le 13/09/2026.
 */
export function valeurMoyen(resText: string): number {
  const icones = (resText.match(/[rbygl]/gi) ?? []).length
  if (icones > 0) return icones
  const reduction = /^-(\d+)$/.exec(resText.trim())
  if (reduction) return Number(reduction[1])
  return 1
}

/**
 * Total REELLEMENT paye par les ressources choisies : la SOMME des valeurs des
 * effets, pas leur nombre. Sans cela une carte double compte pour 1 et « Valider »
 * reste bloque a 1/2.
 */
export function valeurPayee(paiement: Paiement | undefined, ressources: number[]): number {
  if (!paiement) return 0
  const texteParEffet = new Map<number, string>()
  for (const moyen of paiement.payment) {
    if (!texteParEffet.has(moyen.effect_id)) texteParEffet.set(moyen.effect_id, moyen.res_text)
  }
  return ressources.reduce((total, id) => total + valeurMoyen(texteParEffet.get(id) ?? ''), 0)
}

/**
 * Le coup, paye ainsi, ne produira-t-il AUCUN effet ?
 *
 * Renvoie l'avertissement du moteur si le paiement choisi ne porte aucune
 * lettre de la couleur exigee (un joker « G » vaut toute couleur, comme pour
 * `typesManquants`) ; en mode `seulement`, des qu'une lettre d'une AUTRE
 * couleur s'y trouve. Rien choisi : on previent aussi, le moteur ne saurait
 * pas mieux payer a notre place. Undefined = rien a dire.
 *
 * ⚠ Ce n'est PAS un refus : le moteur accepte le coup, la carte est jouable.
 * C'est une confirmation, decidee avec l'utilisateur le 11/09/2026, pour ne
 * plus voir une carte partir en defausse sans rien faire, sans un mot.
 */
export function coupSansEffet(
  paiement: Paiement | undefined,
  ressources: number[]
): Avertissement | undefined {
  const avertissement = paiement?.avertissement
  if (!paiement || !avertissement) return undefined
  const texteParEffet = new Map<number, string>()
  for (const moyen of paiement.payment) {
    if (!texteParEffet.has(moyen.effect_id)) texteParEffet.set(moyen.effect_id, moyen.res_text)
  }
  const exigee = avertissement.ressource.toUpperCase()
  const lettres = ressources.flatMap((id) =>
    ((texteParEffet.get(id) ?? '').match(/[rbygl]/gi) ?? []).map((l) => l.toUpperCase())
  )
  const convient = (type: string) => type === exigee || type === 'G'
  if (avertissement.seulement) {
    return lettres.length > 0 && lettres.every(convient) ? undefined : avertissement
  }
  return lettres.some(convient) ? undefined : avertissement
}

/** L'option est-elle prete a etre envoyee au moteur ? */
export function reponsePrete(
  option: Option,
  cibles: number[],
  ressources: number[]
): { prete: boolean; raison: string } {
  const [min, max] = option.target_num_range
  if (cibles.length < min) {
    return { prete: false, raison: `Choose ${min - cibles.length} more target(s)` }
  }
  if (cibles.length > max) {
    return { prete: false, raison: `Remove ${cibles.length - max} target(s)` }
  }

  const paiement = paiementCourant(option, cibles)

  // Cout exprime en types (« BY », « Y1 ») : le compte de ressources ne dit
  // pas LESQUELLES manquent. Ce controle passe en premier, parce que sa raison
  // est la plus utile au joueur (« Pay 1 mental resource(s) » plutot que
  // « Pay 1 more resource(s) »). Sans lui, l'action se disait prete des la
  // premiere ressource et le moteur la refusait sans explication.
  if (!paiementFacultatif(paiement)) {
    const manquants = Object.entries(typesManquants(paiement, ressources))
    if (manquants.length > 0) {
      const detail = manquants
        .map(([type, nombre]) => `${nombre} ${NOM_TYPE[type] ?? type}`)
        .join(' and ')
      return { prete: false, raison: `Pay ${detail} resource(s)` }
    }
  }

  // Puis le TOTAL. Un cout mixte (« Y1 ») a ses types couverts bien avant son
  // compte : Thunder Strike coute 2, dont une energie.
  const requis = nombreDeRessources(paiement)
  const paye = valeurPayee(paiement, ressources)
  if (requis !== undefined && !paiementFacultatif(paiement) && paye < requis) {
    return {
      prete: false,
      raison: `Pay ${requis - paye} more resource(s)`,
    }
  }

  return { prete: true, raison: '' }
}
