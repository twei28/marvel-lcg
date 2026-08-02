export type TonaliteAction =
  | 'attack'
  | 'thwart'
  | 'recover'
  | 'defense'
  | 'play'
  | 'change'
  | 'ability'
  | 'general'

export function tonaliteAction(nom: string): TonaliteAction {
  const action = nom.toLowerCase()
  if (action.includes('attack')) return 'attack'
  if (action.includes('thwart')) return 'thwart'
  if (action.includes('recover')) return 'recover'
  if (action.includes('defense') || action.includes('defend')) return 'defense'
  if (action === 'play') return 'play'
  if (action.includes('change form')) return 'change'
  if (action.includes('action') || action.includes('response') || action.includes('interrupt')) {
    return 'ability'
  }
  return 'general'
}

export function classeTonaliteAction(nom: string): string {
  return `tonalite-${tonaliteAction(nom)}`
}
