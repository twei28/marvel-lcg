// La couleur d'un bouton d'action, déduite de son libellé.
//
// Le libellé lui arrive DÉJÀ TRADUIT (voir `vocabulaire-moteur.ts`) : un bouton
// dit « Attaquer » en français et « Attack » en anglais. La reconnaissance se
// fait donc dans les deux langues — sinon les pouvoirs de base perdaient leur
// couleur dès qu'on jouait en français, silencieusement.

export type TonaliteAction =
  | 'attack'
  | 'thwart'
  | 'recover'
  | 'defense'
  | 'play'
  | 'change'
  | 'ability'
  | 'general'

/** Un fragment suffit : le libellé peut porter une source ou un suffixe. */
const FRAGMENTS: readonly (readonly [TonaliteAction, readonly string[]])[] = [
  ['attack', ['attack', 'attaquer', 'attaque']],
  ['thwart', ['thwart', 'contrer']],
  ['recover', ['recover', 'récupérer', 'recuperer']],
  ['defense', ['defense', 'defend', 'défendre', 'defendre']],
  ['change', ['change form', 'changer de forme']],
  ['ability', ['action', 'response', 'interrupt', 'réponse', 'reponse', 'interruption']],
]

/** Reconnus seulement à l'identique : « jouer » est trop court pour un `includes`. */
const EXACTS: Readonly<Record<string, TonaliteAction>> = {
  play: 'play',
  jouer: 'play',
}

export function tonaliteAction(nom: string): TonaliteAction {
  const action = nom.toLowerCase()
  const exact = EXACTS[action.trim()]
  if (exact) return exact
  for (const [tonalite, fragments] of FRAGMENTS) {
    if (fragments.some((fragment) => action.includes(fragment))) return tonalite
  }
  return 'general'
}

export function classeTonaliteAction(nom: string): string {
  return `tonalite-${tonaliteAction(nom)}`
}
