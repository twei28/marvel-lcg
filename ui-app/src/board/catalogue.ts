// Les PV maximum imprimes sur les cartes.
//
// /get_world envoie les PV COURANTS (verifie : a la mise en place, round 0, la
// valeur est exactement le HP imprime ; en fin de partie elle tombe a 0). Le
// maximum, lui, n'est pas dans le descripteur : il faut le catalogue.
//
// La source est data/cards.json, servie par la route /get_cards_json du jeu
// (gzip, en cache navigateur). On ne l'embarque PAS dans le build : le serveur
// n'a aucune route pour un .json depose dans public/app/, et 1,7 Mo de JSON
// dans le bundle serait absurde.
//
// Tout est facultatif : sans catalogue, le plateau affiche « 3 PV » au lieu de
// « 1/3 PV ». Rien ne casse.

import { motsClesDeCarte, type MotCle } from './mots-cles'

type CartePapier = {
  card_id?: string
  type?: string
  name?: string
  desc?: Partial<Record<string, string>>
  text?: string
}

/**
 * L'aspect d'une carte de deck de joueur. C'est ce que la COULEUR du cadre
 * dit au joueur d'un coup d'oeil, et c'est precisement ce qu'un effet qui
 * desature efface. Le plateau ne le recoit pas du moteur : `/get_world`
 * n'envoie ni aspect ni set_name. Mais le catalogue, lui, porte `desc.Class`.
 */
export type Aspect =
  | 'aggression'
  | 'justice'
  | 'leadership'
  | 'protection'
  | 'pool'
  | 'determination'
  | 'venomized'
  | 'hero'
  | 'basic'

/**
 * `desc.Class` vaut « Aggression », « Hero », « Basic », « 'Pool »... et
 * parfois plusieurs valeurs separees par un point-virgule (« Hero;Aggression »,
 * « Campaign;Basic »). Un aspect l'emporte sur Hero, qui l'emporte sur Basic :
 * c'est l'information la plus discriminante qui doit gagner. Campaign et
 * Encounter ne disent rien de la couleur du cadre et sont ignores.
 */
export function aspectDeClasse(brut: string | undefined): Aspect | undefined {
  if (!brut) return undefined
  const parts = brut.split(';').map((p) => p.trim())
  const table: Record<string, Aspect> = {
    Aggression: 'aggression',
    Justice: 'justice',
    Leadership: 'leadership',
    Protection: 'protection',
    "'Pool": 'pool',
    // Le cinquieme aspect, fan-made (designhacker.ca), accepte par le moteur
    // depuis e161ffe. Sans cette ligne ses cartes n'ont aucun lisere sous un
    // effet delavant, et le catalogue les compte comme inconnues.
    Determination: 'determination',
    // Le SIXIEME aspect, fan-made lui aussi (ekAugust, set 168), accepte par
    // le moteur depuis le 09/09/2026. Meme raison que Determination : sans
    // cette ligne ses 35 cartes n'ont aucun lisere sous un effet delavant, et
    // `aspect.test.ts` les compte comme une valeur de Class inconnue.
    Venomized: 'venomized',
  }
  for (const p of parts) if (table[p]) return table[p]
  if (parts.includes('Hero')) return 'hero'
  if (parts.includes('Basic')) return 'basic'
  return undefined
}

export type Catalogue = {
  /** PV imprimes, ou undefined si la carte n'en a pas de valeur fixe. */
  pvMax(cardId: string): number | undefined
  /** Stat imprimee sur la carte, utilisee seulement si le moteur n'envoie rien. */
  statImprimee(cardId: string, label: string): number | undefined
  /** Mots-cles de la carte (Guard, Piercing...), avec leur definition. */
  motsCles(cardId: string): MotCle[]
  /**
   * La carte tire-t-elle parti d'un SURPAIEMENT ?
   *
   * Trois cartes recompensent le fait de payer plus que le cout imprime :
   * l'allie Ant-Man et Wasp (un compteur pym par ressource en trop) et Wonder
   * Man. Le moteur ne le signale nulle part — la seule trace est le texte de
   * regles. On le lit donc, plutot que de figer une liste d'identifiants qui
   * vieillirait mal a chaque carte fan-made ajoutee.
   */
  surpayable(cardId: string): boolean
  /** L'aspect de la carte, ou undefined si elle n'est pas une carte de joueur. */
  aspect(cardId: string): Aspect | undefined
  /**
   * Le TYPE imprime de la carte (« SideScheme », « Environment », « Ally »...),
   * tel que cards.json l'ecrit. Sert a orienter une face que le monde ne
   * decrit pas : le verso d'une carte recto-verso n'a pas de `card_type` cote
   * moteur, seul le catalogue sait s'il se lit en paysage.
   */
  type(cardId: string): string | undefined
}

/** Catalogue absent : le plateau s'affiche quand meme, sans les PV maximum. */
export const catalogueVide: Catalogue = {
  pvMax: () => undefined,
  statImprimee: () => undefined,
  motsCles: () => [],
  surpayable: () => false,
  aspect: () => undefined,
  type: () => undefined,
}

/**
 * « 10 » -> 10. « 18* » et « INF » -> undefined.
 *
 * L'etoile veut dire « voir le texte de la carte » : la plupart des vilains ont
 * des PV qui dependent du nombre de joueurs. Afficher le nombre imprime comme
 * maximum serait faux, donc on ne l'affiche pas.
 */
function pvImprimes(brut: string | undefined): number | undefined {
  if (!brut || !/^\d+$/.test(brut)) return undefined
  return Number(brut)
}

function statImprimee(brut: string | undefined): number | undefined {
  if (!brut || !/^\d+$/.test(brut)) return undefined
  return Number(brut)
}

/** Exportee pour les tests : la construire depuis un catalogue en memoire
 *  evite de dependre du reseau et du fichier de 2,5 Mo. */
export function construire(donnees: unknown): Catalogue {
  if (typeof donnees !== 'object' || donnees === null) return catalogueVide

  const parCarte = new Map<string, number>()
  const statsParCarte = new Map<string, Partial<Record<string, number>>>()
  const motsClesParCarte = new Map<string, MotCle[]>()
  const surpayables = new Set<string>()
  const aspects = new Map<string, Aspect>()
  const types = new Map<string, string>()

  // cards.json = { "<nom de paquet>": [cartes...], "checksum": "<hexa>" }.
  for (const paquet of Object.values(donnees as Record<string, unknown>)) {
    if (!Array.isArray(paquet)) continue
    for (const carte of paquet as CartePapier[]) {
      const id = carte?.card_id
      if (typeof id !== 'string') continue
      const pv = pvImprimes(carte.desc?.HP)
      if (pv !== undefined) parCarte.set(id, pv)
      const stats: Partial<Record<string, number>> = {}
      for (const label of ['THW', 'ATK', 'DEF', 'REC', 'SCH']) {
        const valeur = statImprimee(carte.desc?.[label])
        if (valeur !== undefined) stats[label] = valeur
      }
      if (Object.keys(stats).length > 0) statsParCarte.set(id, stats)
      const motsCles = motsClesDeCarte(carte.desc, carte.text)
      if (motsCles.length > 0) motsClesParCarte.set(id, motsCles)
      // « for each resource you overpaid for X's cost » : la formule est stable
      // sur les trois cartes concernees. On accepte aussi la forme francaise au
      // cas ou les donnees seraient traduites un jour.
      if (/overpaid|overpay|surpay/i.test(carte.text ?? '')) surpayables.add(id)
      // Une carte a COUT X est surpayable par nature, et son texte ne dit
      // jamais « overpay » : il dit « Deal X damage ». Sans cette ligne, les
      // neuf cartes a cout X du catalogue n'allumaient aucun rappel au moment
      // de confirmer. Le joueur validait sans rien depenser, X valait 0, et la
      // carte ne faisait RIEN — signale en jeu sur Tendril Explosion (vr006),
      // mais Speed Cyclone (14006) et Lethal Intent (22010), qui sont
      // officielles, avaient exactement le meme defaut.
      if (carte.desc?.Cost === 'X') surpayables.add(id)
      const aspect = aspectDeClasse(carte.desc?.Class)
      if (aspect) aspects.set(id, aspect)
      if (typeof carte.type === 'string') types.set(id, carte.type)
    }
  }

  return {
    pvMax: (cardId) => parCarte.get(cardId),
    statImprimee: (cardId, label) => statsParCarte.get(cardId)?.[label],
    motsCles: (cardId) => motsClesParCarte.get(cardId) ?? [],
    surpayable: (cardId) => surpayables.has(cardId),
    aspect: (cardId) => aspects.get(cardId),
    type: (cardId) => types.get(cardId),
  }
}

let enCours: Promise<Catalogue> | undefined

/**
 * Charge le catalogue une seule fois par page. Un echec n'est pas une erreur
 * de plateau : on rend un catalogue vide et le plateau continue.
 */
export function chargerCatalogue(): Promise<Catalogue> {
  if (!enCours) {
    enCours = fetch('/get_cards_json')
      .then((reponse) => (reponse.ok ? (reponse.json() as Promise<unknown>) : undefined))
      .then(construire)
      .catch(() => catalogueVide)
  }
  return enCours
}
